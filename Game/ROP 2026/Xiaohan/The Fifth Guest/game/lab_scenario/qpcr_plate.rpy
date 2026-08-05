## Interactive 96-well qPCR plate preparation mini-game.
## Replaces the one-click qPCR hotspot with fill → seal → centrifuge → bubble removal.

default qpcr_plate_phase = "fill"  # fill | seal | centrifuge | bubbles | done
default qpcr_selected_reagent = "standard"  # standard | ntc | sample
default qpcr_wells = {}
default qpcr_show_errors = False
default qpcr_show_instructions = False
default qpcr_plate_sealed = False
default qpcr_centrifuge_rpm = 0
default qpcr_bubbles_remaining = 0
default qpcr_plate_ready = False
default qpcr_paint_down = False
default qpcr_paint_moved = False
default qpcr_paint_pending_clear = None

init -3 python:
    # Plate layout matches generated assets in images/qpcr/
    QPCR_MARGIN_L = 90
    QPCR_MARGIN_T = 90
    QPCR_WELL = 58
    QPCR_GAP = 10
    QPCR_COLS = 12
    QPCR_ROWS = 8
    QPCR_PLATE_X = 60
    QPCR_PLATE_Y = 150

    QPCR_CORRECT = {
        # Standards A1-E1
        "A1": "standard", "B1": "standard", "C1": "standard",
        "D1": "standard", "E1": "standard",
        # NTC F1
        "F1": "ntc",
        # Samples G1-H1 only (two samples)
        "G1": "sample", "H1": "sample",
    }

    QPCR_WELL_IMAGES = {
        None: "qpcr/well_empty.png",
        "standard": "qpcr/well_standard.png",
        "ntc": "qpcr/well_ntc.png",
        "sample": "qpcr/well_sample.png",
        "error": "qpcr/well_error.png",
        "bubble": "qpcr/well_bubble.png",
    }

    def qpcr_well_id(row, col):
        return "{}{}".format(chr(ord("A") + row), col + 1)

    def qpcr_well_pos(row, col):
        x = QPCR_PLATE_X + QPCR_MARGIN_L + col * (QPCR_WELL + QPCR_GAP)
        y = QPCR_PLATE_Y + QPCR_MARGIN_T + row * (QPCR_WELL + QPCR_GAP)
        return x, y

    def qpcr_reset_plate():
        store.qpcr_plate_phase = "fill"
        store.qpcr_selected_reagent = "standard"
        store.qpcr_wells = {}
        store.qpcr_show_errors = False
        store.qpcr_show_instructions = False
        store.qpcr_plate_sealed = False
        store.qpcr_centrifuge_rpm = 0
        store.qpcr_bubbles_remaining = 0
        store.qpcr_plate_ready = False
        store.qpcr_paint_down = False
        store.qpcr_paint_moved = False
        store.qpcr_paint_pending_clear = None

    def qpcr_well_contents(well_id):
        return store.qpcr_wells.get(well_id)

    def qpcr_sample_unlocked():
        """Sample wells require finished DNA extraction."""
        return bool(store.tasks.get("DNA extraction")) or extraction_complete()

    def qpcr_select_reagent(reagent):
        if reagent == "sample" and not qpcr_sample_unlocked():
            custom_notify(
                "Finish DNA extraction before placing sample on the plate. You can still add Standards and NTC.",
                False,
            )
            return
        store.qpcr_selected_reagent = reagent
        renpy.restart_interaction()

    def qpcr_set_well(well_id, reagent):
        if reagent == "sample" and not qpcr_sample_unlocked():
            custom_notify(
                "Finish DNA extraction before placing sample on the plate.",
                False,
            )
            return
        store.qpcr_wells[well_id] = reagent
        store.qpcr_show_errors = False

    def qpcr_clear_well(well_id):
        if well_id in store.qpcr_wells:
            del store.qpcr_wells[well_id]
        store.qpcr_show_errors = False

    def qpcr_well_at_mouse():
        """Return (row, col) under the cursor, or None."""
        mx, my = renpy.get_mouse_pos()
        for row in range(QPCR_ROWS):
            for col in range(QPCR_COLS):
                wx, wy = qpcr_well_pos(row, col)
                if wx <= mx < wx + QPCR_WELL and wy <= my < wy + QPCR_WELL:
                    return row, col
        return None

    def qpcr_start_paint():
        """Begin click/drag dispense from the well under the cursor."""
        if store.qpcr_plate_phase != "fill":
            return
        if store.qpcr_selected_reagent == "sample" and not qpcr_sample_unlocked():
            custom_notify(
                "Finish DNA extraction before placing sample on the plate.",
                False,
            )
            return
        hit = qpcr_well_at_mouse()
        if hit is None:
            return
        row, col = hit
        store.qpcr_paint_down = True
        store.qpcr_paint_moved = False
        well_id = qpcr_well_id(row, col)
        current = qpcr_well_contents(well_id)
        selected = store.qpcr_selected_reagent
        if current == selected:
            store.qpcr_paint_pending_clear = well_id
        else:
            store.qpcr_paint_pending_clear = None
            qpcr_set_well(well_id, selected)
        renpy.restart_interaction()

    def qpcr_paint_at_mouse():
        """While the mouse is held, keep dispensing into hovered wells."""
        if store.qpcr_plate_phase != "fill" or not store.qpcr_paint_down:
            return
        if store.qpcr_selected_reagent == "sample" and not qpcr_sample_unlocked():
            return
        hit = qpcr_well_at_mouse()
        if hit is None:
            return
        row, col = hit
        well_id = qpcr_well_id(row, col)
        if store.qpcr_paint_pending_clear == well_id and not store.qpcr_paint_moved:
            return
        store.qpcr_paint_moved = True
        store.qpcr_paint_pending_clear = None
        selected = store.qpcr_selected_reagent
        if qpcr_well_contents(well_id) != selected:
            qpcr_set_well(well_id, selected)
            renpy.restart_interaction()

    def qpcr_end_paint():
        if store.qpcr_paint_down and not store.qpcr_paint_moved and store.qpcr_paint_pending_clear:
            qpcr_clear_well(store.qpcr_paint_pending_clear)
        store.qpcr_paint_down = False
        store.qpcr_paint_moved = False
        store.qpcr_paint_pending_clear = None
        renpy.restart_interaction()

    def qpcr_tap_bubble(row, col):
        if store.qpcr_plate_phase != "bubbles":
            return
        well_id = qpcr_well_id(row, col)
        if store.qpcr_wells.get(well_id) != "bubble":
            return
        # Restore correct sample fill after bubble is removed.
        expected = QPCR_CORRECT.get(well_id, "sample")
        store.qpcr_wells[well_id] = expected
        store.qpcr_bubbles_remaining = max(0, store.qpcr_bubbles_remaining - 1)
        if store.qpcr_bubbles_remaining <= 0:
            store.qpcr_plate_phase = "done"
            store.qpcr_plate_ready = True
            custom_notify("All bubbles removed. Plate is ready for QuantStudio!", True)
        renpy.restart_interaction()

    def qpcr_layout_errors():
        """Return well IDs that do not match the required layout."""
        errors = []
        # Wrong or extra fills
        for well_id, reagent in store.qpcr_wells.items():
            expected = QPCR_CORRECT.get(well_id)
            if expected != reagent:
                errors.append(well_id)
        # Missing required fills
        for well_id, expected in QPCR_CORRECT.items():
            if store.qpcr_wells.get(well_id) != expected:
                if well_id not in errors:
                    errors.append(well_id)
        return errors

    def qpcr_submit_layout():
        errors = qpcr_layout_errors()
        if errors:
            store.qpcr_show_errors = True
            custom_notify("Layout incorrect. Check Standards, NTC, and Samples.", False)
            renpy.restart_interaction()
            return

        store.qpcr_show_errors = False
        store.qpcr_plate_phase = "seal"
        custom_notify("Layout correct! Seal the plate with an optical cover.", True)
        renpy.restart_interaction()

    def qpcr_seal_plate():
        if store.qpcr_plate_phase != "seal":
            return
        store.qpcr_plate_sealed = True
        store.qpcr_plate_phase = "centrifuge"
        custom_notify("Optical cover applied. Choose benchtop centrifuge speed.", True)
        renpy.restart_interaction()

    def qpcr_run_centrifuge(rpm):
        if store.qpcr_plate_phase != "centrifuge":
            return
        store.qpcr_centrifuge_rpm = rpm
        if rpm != 3000:
            custom_notify("Incorrect speed. Use 3000 rpm for this plate.", False)
            renpy.restart_interaction()
            return

        # Introduce bubble wells that must be tapped clear (only on filled sample wells).
        bubble_targets = ["G1", "H1"]
        for well_id in bubble_targets:
            if well_id in store.qpcr_wells:
                store.qpcr_wells[well_id] = "bubble"
        store.qpcr_bubbles_remaining = len(bubble_targets)
        store.qpcr_plate_phase = "bubbles"
        custom_notify("Benchtop centrifuge ran at 3000 rpm. Tap wells to remove remaining bubbles.", True)
        renpy.restart_interaction()

    def qpcr_well_display(well_id):
        """Image key for the current well state."""
        if store.qpcr_show_errors and store.qpcr_plate_phase == "fill":
            expected = QPCR_CORRECT.get(well_id)
            actual = store.qpcr_wells.get(well_id)
            if expected != actual:
                # Highlight incorrect / missing required wells, and extras.
                if expected is not None or actual is not None:
                    return "error"
        return store.qpcr_wells.get(well_id)

    def qpcr_phase_instruction():
        phase = store.qpcr_plate_phase
        if phase == "fill":
            return (
                "Select Standard, NTC, or Sample, then click wells to dispense 2 µL. "
                "18 µL reagent mix is already present."
            )
        if phase == "seal":
            return "Seal the plate with an optical cover."
        if phase == "centrifuge":
            return "Place the sealed plate in the benchtop centrifuge and run at 3000 rpm."
        if phase == "bubbles":
            return (
                "Bubbles prevent accurate measurement. Tap each bubbled well to clear it. "
                "Remaining: {}".format(store.qpcr_bubbles_remaining)
            )
        if phase == "done":
            return "Plate preparation complete. Continue to run QuantStudio."
        return ""


## ---- Screens ----

screen qpcr_plate_prep():
    modal True
    zorder 120
    add Solid("#0b1620")

    # Main plate
    add "qpcr/plate_base.png":
        xpos QPCR_PLATE_X
        ypos QPCR_PLATE_Y

    # Wells + hotspots
    for row in range(QPCR_ROWS):
        for col in range(QPCR_COLS):
            $ well_id = qpcr_well_id(row, col)
            $ wx, wy = qpcr_well_pos(row, col)
            $ state = qpcr_well_display(well_id)

            if state == "bubble":
                # Keep the well's real reagent colour visible under the bubble marks.
                $ _bubble_base = QPCR_CORRECT.get(well_id, "sample")
                add QPCR_WELL_IMAGES.get(_bubble_base, QPCR_WELL_IMAGES[None]):
                    xpos wx
                    ypos wy
                add "qpcr/well_bubble_overlay.png":
                    xpos wx
                    ypos wy
            else:
                $ img = QPCR_WELL_IMAGES.get(state, QPCR_WELL_IMAGES[None])
                add img:
                    xpos wx
                    ypos wy

            if qpcr_plate_phase == "fill":
                button:
                    xpos wx
                    ypos wy
                    xysize (QPCR_WELL, QPCR_WELL)
                    background None
                    action NullAction()
                    tooltip well_id
            elif qpcr_plate_phase == "bubbles" and qpcr_wells.get(well_id) == "bubble":
                button:
                    xpos wx
                    ypos wy
                    xysize (QPCR_WELL, QPCR_WELL)
                    background None
                    action Function(qpcr_tap_bubble, row, col)
                    tooltip "Tap to remove bubble"

    if qpcr_plate_sealed:
        add "qpcr/plate_cover.png":
            xpos QPCR_PLATE_X
            ypos QPCR_PLATE_Y

    # Click-and-drag dispense across wells (mousedown starts, timer paints, mouseup ends).
    if qpcr_plate_phase == "fill":
        key "mousedown_1" action Function(qpcr_start_paint)
        key "mouseup_1" action Function(qpcr_end_paint)
        timer 0.04 repeat True action Function(qpcr_paint_at_mouse)

    # Right control panel
    frame:
        xpos 1280
        ypos 40
        xsize 600
        ysize 1000
        background "#17354aee"
        padding (24, 22)

        $ _phase_text = qpcr_phase_instruction()

        vbox:
            spacing 14
            xfill True

            text "QuantStudio Plate Preparation":
                size 32
                color "#ffffff"
                bold True

            text "[_phase_text]":
                size 18
                color "#d8e8f2"

            null height 6

            if qpcr_plate_phase == "fill":
                text "Dispense 2 µL of:":
                    size 20
                    color "#7ec8e3"
                    bold True

                text "Hold and drag across wells to dispense. Click a filled well again to clear it.":
                    size 15
                    color "#b8c9d4"

                hbox:
                    spacing 10
                    textbutton "Standard":
                        background ("#2d6f8f" if qpcr_selected_reagent == "standard" else "#1f4b63")
                        hover_background "#3a8bb0"
                        padding (12, 8)
                        text_size 18
                        action Function(qpcr_select_reagent, "standard")
                    textbutton "NTC":
                        background ("#2d6f8f" if qpcr_selected_reagent == "ntc" else "#1f4b63")
                        hover_background "#3a8bb0"
                        padding (12, 8)
                        text_size 18
                        action Function(qpcr_select_reagent, "ntc")
                    textbutton "Sample":
                        background ("#2d6f8f" if qpcr_selected_reagent == "sample" else "#1f4b63")
                        hover_background "#3a8bb0"
                        padding (12, 8)
                        text_size 18
                        action Function(qpcr_select_reagent, "sample")

                if not qpcr_sample_unlocked():
                    text "Sample locked — finish DNA extraction first. Standards and NTC are available now.":
                        size 15
                        color "#ffcc66"

                $ _std_needed = list(QPCR_CORRECT.values()).count("standard")
                $ _ntc_needed = list(QPCR_CORRECT.values()).count("ntc")
                $ _sample_needed = list(QPCR_CORRECT.values()).count("sample")
                $ _std_have = list(qpcr_wells.values()).count("standard")
                $ _ntc_have = list(qpcr_wells.values()).count("ntc")
                $ _sample_have = list(qpcr_wells.values()).count("sample")

                frame:
                    background "#0d2636cc"
                    padding (14, 10)
                    xfill True
                    vbox:
                        spacing 4
                        text "Wells filled:":
                            size 16
                            bold True
                            color "#ffffff"
                        text "Standard: [_std_have]/[_std_needed]":
                            size 16
                            color ("#7dffb3" if _std_have == _std_needed else "#e8d5a3")
                        text "NTC: [_ntc_have]/[_ntc_needed]":
                            size 16
                            color ("#7dffb3" if _ntc_have == _ntc_needed else "#6b7a3a")
                        text "Sample: [_sample_have]/[_sample_needed]":
                            size 16
                            color ("#7dffb3" if _sample_have == _sample_needed else "#c4a574")

                add "qpcr/legend.png"

                text "Target layout: Standards A1–E1, NTC F1, Samples G1–H1 only.":
                    size 15
                    color "#b8c9d4"

                textbutton "Submit Layout":
                    xalign 0.0
                    background "#2ecc71"
                    hover_background "#27ae60"
                    padding (16, 10)
                    text_size 22
                    text_color "#ffffff"
                    action Function(qpcr_submit_layout)

                textbutton "Clear Plate":
                    background "#7f8c8d"
                    hover_background "#95a5a6"
                    padding (16, 10)
                    text_size 18
                    text_color "#ffffff"
                    action Function(qpcr_reset_plate)

            elif qpcr_plate_phase == "seal":
                text "Apply optical cover:":
                    size 20
                    color "#7ec8e3"
                    bold True
                textbutton "Seal with Optical Cover":
                    background "#3498db"
                    hover_background "#2980b9"
                    padding (16, 12)
                    text_size 22
                    text_color "#ffffff"
                    action Function(qpcr_seal_plate)

            elif qpcr_plate_phase == "centrifuge":
                text "Benchtop centrifuge speed:":
                    size 20
                    color "#7ec8e3"
                    bold True
                vbox:
                    spacing 10
                    textbutton "1000 rpm":
                        background "#1f4b63"
                        hover_background "#2d6f8f"
                        padding (16, 10)
                        text_size 20
                        action Function(qpcr_run_centrifuge, 1000)
                    textbutton "3000 rpm":
                        background "#1f4b63"
                        hover_background "#2d6f8f"
                        padding (16, 10)
                        text_size 20
                        action Function(qpcr_run_centrifuge, 3000)
                    textbutton "6000 rpm":
                        background "#1f4b63"
                        hover_background "#2d6f8f"
                        padding (16, 10)
                        text_size 20
                        action Function(qpcr_run_centrifuge, 6000)

            elif qpcr_plate_phase == "bubbles":
                text "Tap bubbled wells on the plate to clear them.":
                    size 18
                    color "#f1c40f"

            elif qpcr_plate_phase == "done":
                text "Ready for quantification.":
                    size 22
                    color "#2ecc71"
                    bold True
                textbutton "Continue":
                    background "#2ecc71"
                    hover_background "#27ae60"
                    padding (18, 12)
                    text_size 24
                    text_color "#ffffff"
                    action Return("ready")

            null height 20

            textbutton "Close":
                style "lab_close_button"
                text_style "lab_close_button_text"
                action Return("cancel")

    # Instructions dropdown — large readable text, drawn above the plate.
    vbox:
        xpos 20
        ypos 16
        spacing 0
        xmaximum 640

        textbutton ("Preparing a Plate for QuantStudio  ▲" if qpcr_show_instructions else "Preparing a Plate for QuantStudio  ▼"):
            background "#1e4d6b"
            hover_background "#2d6f8f"
            padding (20, 14)
            text_size 26
            text_color "#ffffff"
            text_bold True
            action ToggleVariable("qpcr_show_instructions")

        if qpcr_show_instructions:
            frame:
                background "#f4f7fa"
                padding (28, 24)
                xfill True
                vbox:
                    spacing 16

                    text "Preparing a Plate for QuantStudio":
                        size 30
                        bold True
                        color "#153a52"

                    text "1. Use an optical 96-well plate.":
                        size 24
                        color "#1a1a1a"
                    text "2. 18 µL reagent mix is already in each used well.":
                        size 24
                        color "#1a1a1a"
                    text "3. Dispense 2 µL of each Standard, Sample, and Control.":
                        size 24
                        color "#1a1a1a"
                    text "4. Seal the plate with an optical cover.":
                        size 24
                        color "#1a1a1a"
                    text "5. Run the benchtop centrifuge at 3000 rpm.":
                        size 24
                        color "#1a1a1a"
                    text "6. Remove all bubbles (centrifuge + tap plate).":
                        size 24
                        color "#1a1a1a"

                    null height 8

                    text "Correct layout:":
                        size 26
                        bold True
                        color "#153a52"

                    hbox:
                        spacing 14
                        yalign 0.5
                        add Solid("#e8d5a3", xysize=(22, 22))
                        text "Standards A1–E1":
                            size 24
                            color "#1a1a1a"
                            yalign 0.5

                    hbox:
                        spacing 14
                        yalign 0.5
                        add Solid("#6b7a3a", xysize=(22, 22))
                        text "NTC F1":
                            size 24
                            color "#1a1a1a"
                            yalign 0.5

                    hbox:
                        spacing 14
                        yalign 0.5
                        add Solid("#c4a574", xysize=(22, 22))
                        text "Samples G1–H1 (2 samples)":
                            size 24
                            color "#1a1a1a"
                            yalign 0.5

                    null height 6

                    text "Bubbles prevent accurate measurement.":
                        size 24
                        bold True
                        color "#a01818"

                    textbutton "Collapse":
                        xalign 1.0
                        background "#315f86"
                        hover_background "#3a8bb0"
                        padding (16, 10)
                        text_size 20
                        text_color "#ffffff"
                        action SetVariable("qpcr_show_instructions", False)

    $ tooltip = GetTooltip()
    if tooltip:
        frame:
            background "#000000cc"
            padding (10, 6)
            xalign 0.5
            ypos 20
            text "[tooltip]" size 18 color "#ffffff"
