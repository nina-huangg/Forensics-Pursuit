## Interactive 96-well PCR plate preparation mini-game (Thermal Cycler).
## Same fill → seal → centrifuge → bubble removal flow as the QuantStudio
## plate game, reusing the same plate art, but loading DNA sample,
## positive control, and negative control instead of Standard/NTC/Sample.

default pcr_plate_phase = "fill"  # fill | seal | centrifuge | bubbles | done
default pcr_selected_reagent = "sample"  # sample | positive | negative
default pcr_wells = {}
default pcr_show_errors = False
default pcr_show_instructions = False
default pcr_plate_sealed = False
default pcr_centrifuge_rpm = 0
default pcr_bubbles_remaining = 0
default pcr_plate_ready = False
default pcr_paint_down = False
default pcr_paint_moved = False
default pcr_paint_pending_clear = None

init -3 python:
    # Reuses the plate layout/assets from images/qpcr/
    PCR_MARGIN_L = 90
    PCR_MARGIN_T = 90
    PCR_WELL = 58
    PCR_GAP = 10
    PCR_COLS = 12
    PCR_ROWS = 8
    PCR_PLATE_X = 60
    PCR_PLATE_Y = 150

    PCR_CORRECT = {
        # DNA sample (from extraction) + its extraction negative control
        "A1": "sample", "B1": "sample",
        # PCR positive control
        "C1": "positive",
        # PCR negative control
        "D1": "negative",
    }

    PCR_WELL_IMAGES = {
        None: "qpcr/well_empty.png",
        "sample": "qpcr/well_sample.png",
        "positive": "qpcr/well_standard.png",
        "negative": "qpcr/well_ntc.png",
        "error": "qpcr/well_error.png",
        "bubble": "qpcr/well_bubble.png",
    }

    def pcr_well_id(row, col):
        return "{}{}".format(chr(ord("A") + row), col + 1)

    def pcr_well_pos(row, col):
        x = PCR_PLATE_X + PCR_MARGIN_L + col * (PCR_WELL + PCR_GAP)
        y = PCR_PLATE_Y + PCR_MARGIN_T + row * (PCR_WELL + PCR_GAP)
        return x, y

    def pcr_plate_reset():
        store.pcr_plate_phase = "fill"
        store.pcr_selected_reagent = "sample"
        store.pcr_wells = {}
        store.pcr_show_errors = False
        store.pcr_show_instructions = False
        store.pcr_plate_sealed = False
        store.pcr_centrifuge_rpm = 0
        store.pcr_bubbles_remaining = 0
        store.pcr_plate_ready = False
        store.pcr_paint_down = False
        store.pcr_paint_moved = False
        store.pcr_paint_pending_clear = None

    def pcr_well_contents(well_id):
        return store.pcr_wells.get(well_id)

    def pcr_select_reagent(reagent):
        store.pcr_selected_reagent = reagent
        renpy.restart_interaction()

    def pcr_set_well(well_id, reagent):
        store.pcr_wells[well_id] = reagent
        store.pcr_show_errors = False

    def pcr_clear_well(well_id):
        if well_id in store.pcr_wells:
            del store.pcr_wells[well_id]
        store.pcr_show_errors = False

    def pcr_well_at_mouse():
        mx, my = renpy.get_mouse_pos()
        for row in range(PCR_ROWS):
            for col in range(PCR_COLS):
                wx, wy = pcr_well_pos(row, col)
                if wx <= mx < wx + PCR_WELL and wy <= my < wy + PCR_WELL:
                    return row, col
        return None

    def pcr_start_paint():
        if store.pcr_plate_phase != "fill":
            return
        hit = pcr_well_at_mouse()
        if hit is None:
            return
        row, col = hit
        store.pcr_paint_down = True
        store.pcr_paint_moved = False
        well_id = pcr_well_id(row, col)
        current = pcr_well_contents(well_id)
        selected = store.pcr_selected_reagent
        if current == selected:
            store.pcr_paint_pending_clear = well_id
        else:
            store.pcr_paint_pending_clear = None
            pcr_set_well(well_id, selected)
        renpy.restart_interaction()

    def pcr_paint_at_mouse():
        if store.pcr_plate_phase != "fill" or not store.pcr_paint_down:
            return
        hit = pcr_well_at_mouse()
        if hit is None:
            return
        row, col = hit
        well_id = pcr_well_id(row, col)
        if store.pcr_paint_pending_clear == well_id and not store.pcr_paint_moved:
            return
        store.pcr_paint_moved = True
        store.pcr_paint_pending_clear = None
        selected = store.pcr_selected_reagent
        if pcr_well_contents(well_id) != selected:
            pcr_set_well(well_id, selected)
            renpy.restart_interaction()

    def pcr_end_paint():
        if store.pcr_paint_down and not store.pcr_paint_moved and store.pcr_paint_pending_clear:
            pcr_clear_well(store.pcr_paint_pending_clear)
        store.pcr_paint_down = False
        store.pcr_paint_moved = False
        store.pcr_paint_pending_clear = None
        renpy.restart_interaction()

    def pcr_tap_bubble(row, col):
        if store.pcr_plate_phase != "bubbles":
            return
        well_id = pcr_well_id(row, col)
        if store.pcr_wells.get(well_id) != "bubble":
            return
        expected = PCR_CORRECT.get(well_id, "sample")
        store.pcr_wells[well_id] = expected
        store.pcr_bubbles_remaining = max(0, store.pcr_bubbles_remaining - 1)
        if store.pcr_bubbles_remaining <= 0:
            store.pcr_plate_phase = "done"
            store.pcr_plate_ready = True
            custom_notify("All bubbles removed. Plate is ready for the thermal cycler!", True)
        renpy.restart_interaction()

    def pcr_layout_errors():
        errors = []
        for well_id, reagent in store.pcr_wells.items():
            expected = PCR_CORRECT.get(well_id)
            if expected != reagent:
                errors.append(well_id)
        for well_id, expected in PCR_CORRECT.items():
            if store.pcr_wells.get(well_id) != expected:
                if well_id not in errors:
                    errors.append(well_id)
        return errors

    def pcr_submit_layout():
        errors = pcr_layout_errors()
        if errors:
            store.pcr_show_errors = True
            custom_notify("Layout incorrect. Check the sample and control wells.", False)
            record_lab_mistake()
            renpy.restart_interaction()
            return

        store.pcr_show_errors = False
        store.pcr_plate_phase = "seal"
        custom_notify("Layout correct! Seal the plate with an optical cover.", True)
        renpy.restart_interaction()

    def pcr_seal_plate():
        if store.pcr_plate_phase != "seal":
            return
        store.pcr_plate_sealed = True
        store.pcr_plate_phase = "centrifuge"
        custom_notify("Optical cover applied. Choose benchtop centrifuge speed.", True)
        renpy.restart_interaction()

    def pcr_run_centrifuge(rpm):
        if store.pcr_plate_phase != "centrifuge":
            return
        store.pcr_centrifuge_rpm = rpm
        if rpm != 3000:
            custom_notify("Incorrect speed. Use 3000 rpm for this plate.", False)
            renpy.restart_interaction()
            return

        bubble_targets = list(PCR_CORRECT.keys())
        for well_id in bubble_targets:
            if well_id in store.pcr_wells:
                store.pcr_wells[well_id] = "bubble"
        store.pcr_bubbles_remaining = len(bubble_targets)
        store.pcr_plate_phase = "bubbles"
        custom_notify("Benchtop centrifuge ran at 3000 rpm. Tap wells to remove remaining bubbles.", True)
        renpy.restart_interaction()

    def pcr_well_display(well_id):
        if store.pcr_show_errors and store.pcr_plate_phase == "fill":
            expected = PCR_CORRECT.get(well_id)
            actual = store.pcr_wells.get(well_id)
            if expected != actual:
                if expected is not None or actual is not None:
                    return "error"
        return store.pcr_wells.get(well_id)

    def pcr_phase_instruction():
        phase = store.pcr_plate_phase
        if phase == "fill":
            return "Select Sample, Positive Control, or Negative Control, then click wells to load 15 µL."
        if phase == "seal":
            return "Seal the plate with an optical cover."
        if phase == "centrifuge":
            return "Place the sealed plate in the benchtop centrifuge and run at 3000 rpm."
        if phase == "bubbles":
            return (
                "Bubbles prevent accurate amplification. Tap each bubbled well to clear it. "
                "Remaining: {}".format(store.pcr_bubbles_remaining)
            )
        if phase == "done":
            return "Plate preparation complete. Continue to run the thermal cycler."
        return ""


## ---- Screen ----

screen pcr_plate_prep():
    modal True
    zorder 120
    add Solid("#0b1620")

    add "qpcr/plate_base.png":
        xpos PCR_PLATE_X
        ypos PCR_PLATE_Y

    for row in range(PCR_ROWS):
        for col in range(PCR_COLS):
            $ well_id = pcr_well_id(row, col)
            $ wx, wy = pcr_well_pos(row, col)
            $ state = pcr_well_display(well_id)

            if state == "bubble":
                # Keep the well's real reagent colour visible under the bubble marks.
                $ _bubble_base = PCR_CORRECT.get(well_id, "sample")
                add PCR_WELL_IMAGES.get(_bubble_base, PCR_WELL_IMAGES[None]):
                    xpos wx
                    ypos wy
                add "qpcr/well_bubble_overlay.png":
                    xpos wx
                    ypos wy
            else:
                $ img = PCR_WELL_IMAGES.get(state, PCR_WELL_IMAGES[None])
                add img:
                    xpos wx
                    ypos wy

            if pcr_plate_phase == "fill":
                button:
                    xpos wx
                    ypos wy
                    xysize (PCR_WELL, PCR_WELL)
                    background None
                    action NullAction()
                    tooltip well_id
            elif pcr_plate_phase == "bubbles" and pcr_wells.get(well_id) == "bubble":
                button:
                    xpos wx
                    ypos wy
                    xysize (PCR_WELL, PCR_WELL)
                    background None
                    action Function(pcr_tap_bubble, row, col)
                    tooltip "Tap to remove bubble"

    if pcr_plate_sealed:
        add "qpcr/plate_cover.png":
            xpos PCR_PLATE_X
            ypos PCR_PLATE_Y

    if pcr_plate_phase == "fill":
        key "mousedown_1" action Function(pcr_start_paint)
        key "mouseup_1" action Function(pcr_end_paint)
        timer 0.04 repeat True action Function(pcr_paint_at_mouse)

    frame:
        xpos 1280
        ypos 40
        xsize 600
        ysize 1000
        background "#17354aee"
        padding (24, 22)

        $ _phase_text = pcr_phase_instruction()

        vbox:
            spacing 14
            xfill True

            text "PCR Plate Preparation":
                size 32
                color "#ffffff"
                bold True

            text "[_phase_text]":
                size 18
                color "#d8e8f2"

            null height 6

            if pcr_plate_phase == "fill":
                text "Load 15 µL of:":
                    size 20
                    color "#7ec8e3"
                    bold True

                text "Hold and drag across wells to load. Click a filled well again to clear it.":
                    size 15
                    color "#b8c9d4"

                hbox:
                    spacing 10
                    textbutton "Sample":
                        background ("#2d6f8f" if pcr_selected_reagent == "sample" else "#1f4b63")
                        hover_background "#3a8bb0"
                        padding (12, 8)
                        text_size 18
                        action Function(pcr_select_reagent, "sample")
                    textbutton "Positive Control":
                        background ("#2d6f8f" if pcr_selected_reagent == "positive" else "#1f4b63")
                        hover_background "#3a8bb0"
                        padding (12, 8)
                        text_size 18
                        action Function(pcr_select_reagent, "positive")
                    textbutton "Negative Control":
                        background ("#2d6f8f" if pcr_selected_reagent == "negative" else "#1f4b63")
                        hover_background "#3a8bb0"
                        padding (12, 8)
                        text_size 18
                        action Function(pcr_select_reagent, "negative")

                $ _sample_needed = list(PCR_CORRECT.values()).count("sample")
                $ _positive_needed = list(PCR_CORRECT.values()).count("positive")
                $ _negative_needed = list(PCR_CORRECT.values()).count("negative")
                $ _sample_have = list(pcr_wells.values()).count("sample")
                $ _positive_have = list(pcr_wells.values()).count("positive")
                $ _negative_have = list(pcr_wells.values()).count("negative")

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
                        text "Sample: [_sample_have]/[_sample_needed]":
                            size 16
                            color ("#7dffb3" if _sample_have == _sample_needed else "#c4a574")
                        text "Positive Control: [_positive_have]/[_positive_needed]":
                            size 16
                            color ("#7dffb3" if _positive_have == _positive_needed else "#e8d5a3")
                        text "Negative Control: [_negative_have]/[_negative_needed]":
                            size 16
                            color ("#7dffb3" if _negative_have == _negative_needed else "#6b7a3a")

                text "Target layout: DNA Sample + extraction Negative Control A1–B1, Positive Control C1, Negative Control D1.":
                    size 15
                    color "#b8c9d4"

                textbutton "Submit Layout":
                    xalign 0.0
                    background "#2ecc71"
                    hover_background "#27ae60"
                    padding (16, 10)
                    text_size 22
                    text_color "#ffffff"
                    action Function(pcr_submit_layout)

                textbutton "Clear Plate":
                    background "#7f8c8d"
                    hover_background "#95a5a6"
                    padding (16, 10)
                    text_size 18
                    text_color "#ffffff"
                    action Function(pcr_plate_reset)

            elif pcr_plate_phase == "seal":
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
                    action Function(pcr_seal_plate)

            elif pcr_plate_phase == "centrifuge":
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
                        action Function(pcr_run_centrifuge, 1000)
                    textbutton "3000 rpm":
                        background "#1f4b63"
                        hover_background "#2d6f8f"
                        padding (16, 10)
                        text_size 20
                        action Function(pcr_run_centrifuge, 3000)
                    textbutton "6000 rpm":
                        background "#1f4b63"
                        hover_background "#2d6f8f"
                        padding (16, 10)
                        text_size 20
                        action Function(pcr_run_centrifuge, 6000)

            elif pcr_plate_phase == "bubbles":
                text "Tap bubbled wells on the plate to clear them.":
                    size 18
                    color "#f1c40f"

            elif pcr_plate_phase == "done":
                text "Ready for amplification.":
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

        textbutton ("Preparing a Plate for the Thermal Cycler  ▲" if pcr_show_instructions else "Preparing a Plate for the Thermal Cycler  ▼"):
            background "#1e4d6b"
            hover_background "#2d6f8f"
            padding (20, 14)
            text_size 26
            text_color "#ffffff"
            text_bold True
            action ToggleVariable("pcr_show_instructions")

        if pcr_show_instructions:
            frame:
                background "#f4f7fa"
                padding (28, 24)
                xfill True
                vbox:
                    spacing 16

                    text "Preparing a Plate for the Thermal Cycler":
                        size 30
                        bold True
                        color "#153a52"

                    text "1. Use a PCR plate.":
                        size 24
                        color "#1a1a1a"
                    text "2. Load 15 µL of each DNA sample.":
                        size 24
                        color "#1a1a1a"
                    text "3. Add the positive control, then the negative control.":
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
                        add Solid("#c4a574", xysize=(22, 22))
                        text "DNA Sample + extraction Negative Control A1–B1 (2 samples)":
                            size 24
                            color "#1a1a1a"
                            yalign 0.5

                    hbox:
                        spacing 14
                        yalign 0.5
                        add Solid("#e8d5a3", xysize=(22, 22))
                        text "Positive Control C1":
                            size 24
                            color "#1a1a1a"
                            yalign 0.5

                    hbox:
                        spacing 14
                        yalign 0.5
                        add Solid("#6b7a3a", xysize=(22, 22))
                        text "Negative Control D1":
                            size 24
                            color "#1a1a1a"
                            yalign 0.5

                    null height 6

                    text "Bubbles prevent accurate amplification.":
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
                        action SetVariable("pcr_show_instructions", False)

    $ tooltip = GetTooltip()
    if tooltip:
        frame:
            background "#000000cc"
            padding (10, 6)
            xalign 0.5
            ypos 20
            text "[tooltip]" size 18 color "#ffffff"
