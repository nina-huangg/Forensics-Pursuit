screen lab_notify(message, correct=True):
    zorder 350
    frame at (lab_notify_correct if correct else lab_notify_wrong):
        xpos 30
        ypos 30
        background ("#245c34ee" if correct else "#6b2323ee")
        padding gui.notify_frame_borders.padding
        text ("[('✓' if correct else '✗')]  [message!tq]")
    timer 2.0 action Hide("lab_notify")


screen notebook():
    zorder 100
    imagebutton:
        idle (Animation("images/ui/notebook_icon.png", 0.5, "images/ui/notebook_icon_hover.png", 0.5) if not notebook_clicked else "images/ui/notebook_icon.png")
        hover "images/ui/notebook_icon_hover.png"
        xpos 1830 ypos 20
        at Transform(zoom=0.15)
        action [Function(toggle_notebook), SetVariable("notebook_clicked", True)]


screen notebook_screen():
    zorder 100
    frame:
        xalign 0.92
        yalign 0.02
        xsize 610
        ysize 300
        padding (10, 20)
        background "images/ui/notebook_paper.png"
        vbox:
            spacing 6
            xfill True
            text ("DNA / BIO LAB" if analysis_track == "blood" else "FINGERPRINT LAB"):
                style "lab_notebook_heading"
                xalign 0.96

            $ visible_tasks = notebook_task_names()
            for index, task in enumerate(visible_tasks, 1):
                if task == "DNA extraction" and not tasks[task]:
                    hbox:
                        spacing 10
                        text "[index]. [task]":
                            style "lab_todo_text"
                        # Testing shortcut: completes the whole extraction at
                        # once, so it is developer-only (Ctrl+Shift+D).
                        if dev_mode:
                            textbutton "Skip":
                                text_style "lab_page_button"
                                action [
                                    Function(skip_dna_extraction),
                                    Jump("extraction_finished"),
                                ]
                else:
                    text "[index]. [task]":
                        style ("lab_todo_complete" if tasks[task] else "lab_todo_text")

            textbutton "More Details":
                xalign 1.0
                action [
                    SetVariable("more_details_clicked", True),
                    SetVariable("instructions_clicked", True),
                    Show("notebook_instructions_screen"),
                ]
                text_style "lab_page_button"


screen notebook_instructions_screen():
    zorder 100
    frame:
        xalign 0.92
        yalign 0.5
        xsize 600
        ysize 620
        background "images/ui/notebook_paper_long.png"
        padding (16, 22)
        vbox:
            spacing 7
            xfill True

            if analysis_track == "blood":
                $ page_size = 6
                $ total_pages = (len(dna_extraction_steps) + page_size - 1) // page_size
                $ page_start = notebook_detail_page * page_size
                $ page_steps = dna_extraction_steps[page_start:page_start + page_size]
                $ current_page_number = notebook_detail_page + 1

                text "DNA EXTRACTION PROCEDURE":
                    style "lab_details_heading"
                    xalign 0.0

                text "Page [current_page_number] of [total_pages]":
                    style "lab_page_text"
                    xalign 0.5

                for local_index, step_data in enumerate(page_steps):
                    $ step_key, step_text = step_data
                    $ step_number = page_start + local_index + 1
                    $ is_complete = dna_extraction_progress.get(step_key, False)

                    hbox:
                        spacing 6
                        xalign 0.0

                        text "[step_number].":
                            style ("lab_detail_complete" if is_complete else "lab_detail_text")
                            xminimum 40
                            text_align 1.0

                        text "[step_text]":
                            style ("lab_detail_complete" if is_complete else "lab_detail_text")
                            xmaximum 520
                            text_align 0.0

            else:
                text "FINGERPRINT ANALYSIS":
                    style "lab_details_heading"
                    xalign 0.0
                text "Fingerprint procedure details will be added in the next implementation phase.":
                    style "lab_detail_text"
                    xmaximum 530
                textbutton "Close":
                    xalign 0.5
                    action [
                        Hide("notebook_instructions_screen"),
                        SetVariable("instructions_clicked", False),
                    ]
                    text_style "lab_page_button"

    if analysis_track == "blood":
        hbox:
            xpos 1515
            xanchor 0.5
            ypos 800
            spacing 105

            textbutton "<-":
                sensitive notebook_detail_page > 0
                action SetVariable("notebook_detail_page", notebook_detail_page - 1)
                text_style "lab_page_button"

            textbutton "Close":
                action [
                    Hide("notebook_instructions_screen"),
                    SetVariable("instructions_clicked", False),
                ]
                text_style "lab_page_button"

            textbutton "->":
                sensitive notebook_detail_page < total_pages - 1
                action SetVariable("notebook_detail_page", notebook_detail_page + 1)
                text_style "lab_page_button"


screen bio_station():
    zorder 0
    # Station 1 — extraction / wet-lab bench
    imagemap:
        idle "backgrounds/station1.png"
        hover "backgrounds/station1.png"

        hotspot (171, 422, 212, 243) action Jump("use_vortex") tooltip "pulse-vortex"
        hotspot (534, 453, 219, 227) action Jump("use_spinner") tooltip "mini centrifuge"
        hotspot (880, 469, 281, 194) action Jump("use_centrifuge") tooltip "benchtop centrifuge"
        hotspot (1265, 488, 247, 185) action Jump("use_incubator") tooltip "thermomixer"
        hotspot (1575, 476, 289, 174) action Jump("use_prep") tooltip "Prep"

    $ bio_tip = GetTooltip()
    if bio_tip:
        $ _bio_label_pos = {
            "pulse-vortex": (277, 400),
            "mini centrifuge": (643, 430),
            "benchtop centrifuge": (1020, 450),
            "thermomixer": (1388, 470),
            "Prep": (1719, 455),
        }
        $ _lx, _ly = _bio_label_pos.get(bio_tip, (960, 40))
        text "[bio_tip]" at lab_pop_in:
            xpos _lx
            ypos _ly
            xanchor 0.5
            yanchor 0.5
            size 28
            bold True
            color "#ffffff"
            outlines [ (2, "#000000", 0, 0) ]

    imagebutton:
        xpos 1700
        ypos 900
        idle "ui/right_arrow.png"
        hover "ui/right_arrow_hover.png"
        action Jump("bio_station_2")
        tooltip "Station 2"
        at lab_button_bounce

    key "K_RIGHT" action Jump("bio_station_2")
    key "K_d" action Jump("bio_station_2")


screen bio_station_2():
    zorder 0
    # Station 2 — analysis bench
    imagemap:
        idle "backgrounds/station2.png"
        hover "backgrounds/station2.png"

        hotspot (74, 230, 716, 447) action Jump("use_computer") tooltip "Capillary Electrophoresis"
        hotspot (1042, 322, 239, 388) action Jump("use_thermal_cycler") tooltip "Thermal Cycler"
        hotspot (1470, 359, 288, 334) action Jump("use_qpcr") tooltip "QuantStudio"

    $ bio_tip = GetTooltip()
    if bio_tip:
        $ _bio_label_pos = {
            "Capillary Electrophoresis": (432, 210),
            "Thermal Cycler": (1161, 300),
            "QuantStudio": (1614, 340),
        }
        $ _lx, _ly = _bio_label_pos.get(bio_tip, (960, 40))
        text "[bio_tip]" at lab_pop_in:
            xpos _lx
            ypos _ly
            xanchor 0.5
            yanchor 0.5
            size 28
            bold True
            color "#ffffff"
            outlines [ (2, "#000000", 0, 0) ]

    imagebutton:
        xpos 40
        ypos 900
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        action Jump("bio_station")
        tooltip "Station 1"
        at lab_button_bounce

    imagebutton:
        xpos 1700
        ypos 900
        idle "ui/right_arrow.png"
        hover "ui/right_arrow_hover.png"
        action Jump("impression_station")
        tooltip "Fingerprint / AFIS"
        at lab_button_bounce

    key "K_LEFT" action Jump("bio_station")
    key "K_a" action Jump("bio_station")
    key "K_RIGHT" action Jump("impression_station")
    key "K_d" action Jump("impression_station")


# TEMPORARILY DISABLED: legacy single-table biology layout.
# screen bio_station_legacy():
#     ...


screen empty_tube_visual(x, y, w, h):
    # A plain, swab-free tube — used for the negative control so it never
    # shows the blood-swab art that "objects/cut_swab.png" bakes in.
    fixed:
        xpos x
        ypos y
        xysize (w, h)
        frame:
            xalign 0.5
            ypos int(h * 0.06)
            xsize int(w * 0.62)
            ysize int(h * 0.9)
            background "#eaf6ffb0"
        frame:
            xalign 0.5
            ypos 0
            xsize int(w * 0.72)
            ysize int(h * 0.08)
            background "#c7d6ddcc"


screen swab_screen():
    zorder 90
    modal True

    # Keep inventory accessible above this prep UI.
    on "show" action Show("open_inv")
    on "hide" action NullAction()

    add ("backgrounds/prep1.png" if prep_view == 1 else "backgrounds/prep2.png")

    if prep_view == 1:
        # Scissors — cut swab into tube
        button:
            xpos 48
            ypos 229
            xysize (377, 578)
            background Solid("#00000000")
            hover_background Solid("#ffffff22")
            action Function(prep_cut_swab)
            tooltip "Scissors"

        button:
            xpos 505
            ypos 369
            xysize (194, 365)
            background (Solid("#8fd3ff44") if prep_atl_selected else Solid("#00000000"))
            hover_background Solid("#8fd3ff55")
            action Function(prep_select_bottle, "atl")
            tooltip "Buffer ATL"

        button:
            xpos 783
            ypos 382
            xysize (135, 354)
            background (Solid("#8fd3ff44") if prep_prok_selected else Solid("#00000000"))
            hover_background Solid("#8fd3ff55")
            action Function(prep_select_bottle, "prok")
            tooltip "Proteinase K"

        button:
            xpos 1009
            ypos 374
            xysize (191, 361)
            background (Solid("#8fd3ff44") if prep_al_selected else Solid("#00000000"))
            hover_background Solid("#8fd3ff55")
            action Function(prep_select_bottle, "al")
            tooltip "Buffer AL"

    else:
        button:
            xpos 154
            ypos 322
            xysize (203, 358)
            background Solid("#00000000")
            hover_background Solid("#8fd3ff55")
            action If(
                extraction_expected_tool() == "ethanol",
                If(
                    prep_equipped_item is not None,
                    [Function(prep_handoff_to_machine), Return("ethanol")],
                    Show("lab_notify", message="Equip your sample tube or Negative Control from Evidence first.", correct=False),
                ),
                [
                    Show(
                        "lab_notify",
                        message=(
                            "Place the column in a new collection tube first, then add ethanol."
                            if extraction_current() is not None and extraction_current()[0] == "ethanol_new_tube"
                            else "Not the ethanol step yet. Check the notebook."
                        ),
                        correct=False,
                    ),
                    Function(record_lab_mistake),
                ],
            )
            tooltip "Ethanol"

        button:
            xpos 472
            ypos 312
            xysize (184, 363)
            background Solid("#00000000")
            hover_background Solid("#8fd3ff55")
            action If(
                extraction_expected_tool() == "column",
                If(
                    prep_equipped_item is not None,
                    [Function(prep_handoff_to_machine), Return("column")],
                    Show("lab_notify", message="Equip your sample tube or Negative Control from Evidence first.", correct=False),
                ),
                [
                    Show("lab_notify", message="Not this step yet. Check the notebook.", correct=False),
                    Function(record_lab_mistake),
                ],
            )
            tooltip (
                "New collection tube"
                if extraction_current() is not None and extraction_current()[0] in ("ethanol_new_tube", "new_collection_tube", "column_to_labeled_tube")
                else "Buffer AW1"
            )

        button:
            xpos 783
            ypos 322
            xysize (170, 367)
            background Solid("#00000000")
            hover_background Solid("#8fd3ff55")
            action If(
                extraction_expected_tool() == "column",
                If(
                    prep_equipped_item is not None,
                    [Function(prep_handoff_to_machine), Return("column")],
                    Show("lab_notify", message="Equip your sample tube or Negative Control from Evidence first.", correct=False),
                ),
                [
                    Show("lab_notify", message="Not this step yet. Check the notebook.", correct=False),
                    Function(record_lab_mistake),
                ],
            )
            tooltip (
                "New collection tube"
                if extraction_current() is not None and extraction_current()[0] in ("ethanol_new_tube", "new_collection_tube", "column_to_labeled_tube")
                else "Buffer AW2"
            )

        button:
            xpos 1055
            ypos 332
            xysize (226, 355)
            background Solid("#00000000")
            hover_background Solid("#8fd3ff55")
            action If(
                extraction_expected_tool() == "ate",
                If(
                    prep_equipped_item is not None,
                    Return("ate"),
                    Show("lab_notify", message="Equip your sample tube or Negative Control from Evidence first.", correct=False),
                ),
                [
                    Show("lab_notify", message="Not the Buffer ATE step yet. Check the notebook.", correct=False),
                    Function(record_lab_mistake),
                ],
            )
            tooltip "Buffer ATE"

    $ _prep_tip = GetTooltip()
    if _prep_tip:
        text "[_prep_tip]":
            xalign 0.5
            ypos 40
            size 30
            bold True
            color "#ffffff"
            outlines [ (2, "#000000", 0, 0) ]

    # Page arrows — flip between the cutting bench (prep1) and wash-buffer bench (prep2).
    imagebutton:
        xpos 40
        ypos 900
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        action SetVariable("prep_view", 1)
        tooltip "Scissors / ATL / ProK / AL"
        at lab_button_bounce

    imagebutton:
        xpos 1700
        ypos 900
        idle "ui/right_arrow.png"
        hover "ui/right_arrow_hover.png"
        action SetVariable("prep_view", 2)
        tooltip "Ethanol / AW1 / AW2 / ATE"
        at lab_button_bounce

    key "K_LEFT" action SetVariable("prep_view", 1)
    key "K_a" action SetVariable("prep_view", 1)
    key "K_RIGHT" action SetVariable("prep_view", 2)
    key "K_d" action SetVariable("prep_view", 2)

    # Tube on the right: whole swab → cut dry tube (no liquid) → pipette adds buffer.
    # Same slot on both pages so the player can flip pages without losing the tube.
    $ _prep_tube_x = 1439
    $ _prep_tube_y = 211
    $ _prep_tube_w = 348
    $ _prep_tube_h = 684

    $ _prep_equipped_is_neg = prep_equipped_item is not None and prep_equipped_source_name == NEG_CONTROL_NAME

    $ _prep_label_x = _prep_tube_x + 20
    $ _prep_label_y = _prep_tube_y - 40
    $ _prep_hint_y = _prep_tube_y + int(_prep_tube_h * 0.33)

    if prep_equipped_item is not None:
        if _prep_equipped_is_neg:
            use empty_tube_visual(_prep_tube_x, _prep_tube_y, _prep_tube_w, _prep_tube_h)
            text "Negative control\n(no swab)":
                xpos _prep_label_x
                ypos _prep_label_y
                size 18
                color "#ffcc66"
                outlines [ (1, "#000000", 0, 0) ]
        elif prep_is_add_al_step() or check_swab_task_complete(["swab_is_cut"]):
            add Transform("objects/cut_swab.png", size=(_prep_tube_w, _prep_tube_h)) pos (_prep_tube_x, _prep_tube_y)
        else:
            add "objects/swab.png" pos (_prep_label_x + 60, _prep_label_y)
    elif prep_negative_active and not prep_is_add_al_step():
        use empty_tube_visual(_prep_tube_x, _prep_tube_y, _prep_tube_w, _prep_tube_h)
        text "Negative control\n(no swab)":
            xpos _prep_label_x
            ypos _prep_label_y
            size 18
            color "#ffcc66"
            outlines [ (1, "#000000", 0, 0) ]
    elif prep_is_add_al_step():
        text "Equip sample or NC here":
            xpos _prep_label_x
            ypos _prep_hint_y
            size 18
            color "#ffffff88"
            outlines [ (1, "#000000", 0, 0) ]
    elif not prep_samples_complete():
        text "Place equipped tube here":
            xpos _prep_label_x
            ypos _prep_hint_y
            size 18
            color "#ffffff88"
            outlines [ (1, "#000000", 0, 0) ]

    # Compact dropdown instructions (top-left) — the tube now lives on the right side.
    frame:
        xpos 24
        ypos 24
        xsize 380
        background "#0d1a24ee"
        padding (16, 12)

        vbox:
            spacing 10
            xfill True

            if prep_is_add_al_step():
                textbutton (("▼ Instructions" if prep_instructions_open else "▶ Instructions") + "  ·  Buffer AL  {}/{}".format(extraction_step_tube_count(), extraction_step_tubes_needed())):
                    xfill True
                    background None
                    hover_background "#1a2e3ccc"
                    padding (8, 6)
                    text_size 20
                    text_bold True
                    text_color "#8fd3ff"
                    text_hover_color "#b8e4ff"
                    action ToggleVariable("prep_instructions_open")

                text ("Bench: " + (prep_equipped_source_name if prep_equipped_item else "empty")):
                    size 15
                    color ("#7ec8ff" if prep_equipped_item else "#9aa7b2")
                    outlines [ (1, "#000000", 0, 0) ]

                text ("Bottle: " + ("Buffer AL ✓" if prep_al_selected else "Buffer AL ·")):
                    size 14
                    color ("#90ee90" if prep_al_selected else "#ffcc66")
                    outlines [ (1, "#000000", 0, 0) ]

                if prep_instructions_open:
                    null height 4
                    text "Steps":
                        size 17
                        bold True
                        color "#ffffff"
                    vbox:
                        spacing 8
                        xfill True
                        hbox:
                            spacing 8
                            text "1." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Equip a tube" size 16 bold True color "#ffffff"
                                text "Evidence → Use sample or Negative Control" size 14 color "#c5d0d8" xmaximum 300
                        hbox:
                            spacing 8
                            text "2." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Select Buffer AL" size 16 bold True color "#ffffff"
                                text "Click the white AL Buffer bottle" size 14 color "#c5d0d8" xmaximum 300
                        hbox:
                            spacing 8
                            text "3." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Add 300 µL to the tube" size 16 bold True color "#ffffff"
                                text "Click the tube, then collect and repeat for both" size 14 color "#c5d0d8" xmaximum 300
                        hbox:
                            spacing 8
                            text "4." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Pulse-vortex next" size 16 bold True color "#ffffff"
                                text "After both tubes have AL, go to the vortex" size 14 color "#c5d0d8" xmaximum 300
            else:
                textbutton (("▼ Instructions" if prep_instructions_open else "▶ Instructions") + "  ·  {}/{} tubes".format(prep_evidence_count(), prep_samples_needed)):
                    xfill True
                    background None
                    hover_background "#1a2e3ccc"
                    padding (8, 6)
                    text_size 20
                    text_bold True
                    text_color "#8fd3ff"
                    text_hover_color "#b8e4ff"
                    action ToggleVariable("prep_instructions_open")

                text ("Bench: " + (
                    prep_equipped_source_name if prep_equipped_item
                    else ("Negative control (empty)" if prep_negative_active else "empty")
                )):
                    size 15
                    color ("#7ec8ff" if (prep_equipped_item or prep_negative_active) else "#9aa7b2")
                    outlines [ (1, "#000000", 0, 0) ]

                text ("Bottles: " + ("ATL ✓  " if prep_atl_selected else "ATL ·  ") + ("ProK ✓" if prep_prok_selected else "ProK ·")):
                    size 14
                    color ("#90ee90" if prep_buffers_ready() else "#ffcc66")
                    outlines [ (1, "#000000", 0, 0) ]

                if prep_instructions_open:
                    null height 4

                    text "Steps":
                        size 17
                        bold True
                        color "#ffffff"

                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            spacing 8
                            text "1." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Equip swab tube" size 16 bold True color "#ffffff"
                                text "Evidence → Use a Tube with Swab" size 14 color "#c5d0d8" xmaximum 300

                        hbox:
                            spacing 8
                            text "2." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Cut the swab" size 16 bold True color "#ffffff"
                                text "Click the scissors" size 14 color "#c5d0d8" xmaximum 300

                        hbox:
                            spacing 8
                            text "3." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Choose Buffer ATL + ProK" size 16 bold True color "#ffffff"
                                text "Click those bottles on the table, then the dry tube" size 14 color "#c5d0d8" xmaximum 300

                        hbox:
                            spacing 8
                            text "4." size 16 bold True color "#8fd3ff"
                            vbox:
                                spacing 1
                                text "Repeat for 2 tubes + negative control" size 16 bold True color "#ffffff"
                                text "Negative control: empty tube + ATL + ProK (no swab)" size 14 color "#c5d0d8" xmaximum 300

                    null height 4

                    text "Progress":
                        size 17
                        bold True
                        color "#ffffff"

                    text "Evidence tubes: [prep_evidence_count()] / [prep_samples_needed]":
                        size 15
                        color ("#90ee90" if prep_samples_complete() else "#ffffff")

                    text ("Negative control: done" if prep_negative_done else "Negative control: not done"):
                        size 15
                        color ("#90ee90" if prep_negative_done else "#ffffff")

                    if prep_equipped_item is not None:
                        text ("Cut: done" if check_swab_task_complete(["swab_is_cut"]) else "Cut: waiting"):
                            size 14
                            color ("#90ee90" if check_swab_task_complete(["swab_is_cut"]) else "#ffcc66")

    # Pipette target: ATL+ProK (initial) or Buffer AL (add_al step).
    if prep_is_add_al_step():
        if prep_al_selected and prep_equipped_item is not None:
            button:
                xpos _prep_tube_x
                ypos _prep_tube_y
                xsize _prep_tube_w
                ysize _prep_tube_h
                background Solid("#8fd3ff33")
                hover_background Solid("#8fd3ff66")
                action [
                    Function(prep_dispense_al),
                    SetVariable("default_mouse", "default"),
                ]
                tooltip "Add 300 µL Buffer AL"
    elif prep_buffers_ready() and (
        (prep_equipped_item is not None and check_swab_task_complete(["swab_is_cut"]))
        or prep_negative_active
    ):
        button:
            xpos _prep_tube_x
            ypos _prep_tube_y
            xsize _prep_tube_w
            ysize _prep_tube_h
            background Solid("#8fd3ff33")
            hover_background Solid("#8fd3ff66")
            action [
                If(
                    prep_negative_active,
                    Function(prep_mark_negative),
                    Function(prep_mark_sample),
                ),
                SetVariable("default_mouse", "default"),
            ]
            tooltip ("Add ATL + ProK to negative control" if prep_negative_active else "Add Buffer ATL + ProK to tube")

    # Action buttons stay bottom-center, clear of the page arrows and the tube.
    vbox:
        xalign 0.5
        ypos 830
        spacing 12
        xsize 380

        if prep_equipped_item is not None:
            textbutton "Return Tube to Inventory":
                style "lab_close_button"
                text_style "lab_close_button_text"
                xfill True
                action Function(prep_return_unequipped)

        if not prep_is_add_al_step():
            if prep_negative_active:
                textbutton "Cancel Negative Control":
                    style "lab_close_button"
                    text_style "lab_close_button_text"
                    xfill True
                    action Function(prep_cancel_negative)
            elif not prep_negative_done:
                textbutton "Start Negative Control":
                    style "lab_close_button"
                    text_style "lab_close_button_text"
                    xfill True
                    action Function(prep_start_negative)

        textbutton "Close":
            style "lab_close_button"
            text_style "lab_close_button_text"
            xfill True
            action [
                If(prep_equipped_item is not None, Function(prep_return_unequipped), NullAction()),
                If(prep_negative_active, Function(prep_cancel_negative), NullAction()),
                Function(prep_reset_bottle_selection),
                Return(),
            ]


screen ethanol_pour():
    zorder 115
    modal True
    on "show" action Show("open_inv")

    $ _cur = extraction_current()
    $ _key = _cur[0] if _cur else ""
    $ _target = 700 if _key == "add_ethanol_700" else 150
    $ _max = _target + 250
    $ _fill_frac = min(1.0, ethanol_pour_amount / float(_max))
    $ _tube_w = 130
    $ _tube_h = 460
    $ _on_target = ethanol_pour_amount == _target

    add "backgrounds/station1.png"
    add Solid("#00000099")

    frame:
        xalign 0.5
        ypos 40
        xmaximum 900
        background "#0d1a24ee"
        padding (20, 12)
        vbox:
            spacing 6
            text ("Pour 700 µL ethanol into the new collection tube. Target: exactly [_target] µL" if _key == "add_ethanol_700" else "Pour the ethanol. Target: exactly [_target] µL"):
                size 24
                bold True
                color "#ffffff"
            text "Drag the slider below to pour, tap → for 1 µL, or hold → to pour continuously — it only moves forward, so overshoot means Reset and start again. Ease off as you near the mark, then click Pour.":
                size 17
                color "#c5d0d8"
                xmaximum 860

    key "K_RIGHT" action Function(pour_increment, "ethanol_pour_amount", _max, 1)
    # Holding the key pours continuously; see pour_hold_tick in styles.rpy.
    timer 0.06 repeat True action Function(pour_hold_tick, "ethanol_pour_amount", _max, _target)

    # Tube outline with a rising liquid level tied to the poured amount.
    frame:
        xpos 895
        ypos 220
        xsize _tube_w
        ysize _tube_h
        background "#ffffff22"

        fixed:
            xysize (_tube_w, _tube_h)
            add Solid("#c9e8ffdd" if not _on_target else "#8fffb3dd"):
                xsize (_tube_w - 14)
                ysize int(_tube_h * _fill_frac)
                xalign 0.5
                yalign 1.0

    text "[int(ethanol_pour_amount)] µL":
        xpos 960
        ypos 700
        xanchor 0.5
        size 30
        bold True
        color ("#7dffb3" if _on_target else "#ffffff")
        outlines [ (2, "#000000", 0, 0) ]

    frame:
        xpos 292
        ypos 838
        xsize 1116
        ysize 60
        background "#ffffff33"
        padding (8, 8)

        bar:
            xsize 1100
            ysize 44
            value ForwardOnlyValue("ethanol_pour_amount", _max, step=5)
            left_bar Solid("#35c1ff")
            right_bar Solid("#3a4b55")
            thumb Transform(Solid("#ffffff"), xsize=12, ysize=44)

    textbutton "Pour":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 820
        action If(
            _on_target,
            [
                Function(custom_notify, "Poured {} µL — right on target!".format(int(ethanol_pour_amount)), True),
                Return("poured"),
            ],
            [
                Function(
                    custom_notify,
                    ("Not enough yet — keep pouring." if ethanol_pour_amount < _target else "Too much — reset and try again."),
                    False,
                ),
                Function(record_lab_mistake),
            ],
        )

    textbutton "Reset":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 890
        action SetVariable("ethanol_pour_amount", 0)

    # Dev only: drop straight onto the target volume.
    if dev_mode:
        textbutton "Fill (dev)":
            style "lab_close_button"
            text_style "lab_close_button_text"
            xpos 1460
            ypos 960
            action SetVariable("ethanol_pour_amount", _target)

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 24
        ypos 24
        action Return("cancel")


screen lysate_transfer():
    zorder 115
    modal True
    on "show" action Show("open_inv")

    $ _target = 700
    $ _max = _target + 250
    $ _fill_frac = min(1.0, lysate_transfer_amount / float(_max))
    $ _col_w = 130
    $ _col_h = 460
    $ _on_target = lysate_transfer_amount == _target

    add "backgrounds/station1.png"
    add Solid("#00000099")

    frame:
        xalign 0.5
        ypos 40
        xmaximum 900
        background "#0d1a24ee"
        padding (20, 12)
        vbox:
            spacing 6
            text "Transfer lysate onto the QIAamp column. Target: exactly [_target] µL":
                size 24
                bold True
                color "#ffffff"
            text "Drag the slider below to transfer, tap → for 1 µL, or hold → to transfer continuously — it only moves forward, so overshoot means Reset and start again. Ease off as you near the mark, then click Transfer.":
                size 17
                color "#c5d0d8"
                xmaximum 860

    key "K_RIGHT" action Function(pour_increment, "lysate_transfer_amount", _max, 1)
    # Holding the key pours continuously; see pour_hold_tick in styles.rpy.
    timer 0.06 repeat True action Function(pour_hold_tick, "lysate_transfer_amount", _max, _target)

    # QIAamp column outline with rising lysate level tied to the transferred amount.
    frame:
        xpos 895
        ypos 220
        xsize _col_w
        ysize _col_h
        background "#ffffff22"

        fixed:
            xysize (_col_w, _col_h)
            add Solid("#e8b45bdd" if not _on_target else "#8fffb3dd"):
                xsize (_col_w - 14)
                ysize int(_col_h * _fill_frac)
                xalign 0.5
                yalign 1.0

    text "[int(lysate_transfer_amount)] µL":
        xpos 960
        ypos 700
        xanchor 0.5
        size 30
        bold True
        color ("#7dffb3" if _on_target else "#ffffff")
        outlines [ (2, "#000000", 0, 0) ]

    frame:
        xpos 292
        ypos 838
        xsize 1116
        ysize 60
        background "#ffffff33"
        padding (8, 8)

        bar:
            xsize 1100
            ysize 44
            value ForwardOnlyValue("lysate_transfer_amount", _max, step=5)
            left_bar Solid("#ffb020")
            right_bar Solid("#3a4b55")
            thumb Transform(Solid("#ffffff"), xsize=12, ysize=44)

    textbutton "Transfer":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 820
        action If(
            _on_target,
            [
                Function(custom_notify, "Transferred {} µL onto the column — right on target!".format(int(lysate_transfer_amount)), True),
                Return("transferred"),
            ],
            [
                Function(
                    custom_notify,
                    ("Not enough yet — keep transferring." if lysate_transfer_amount < _target else "Too much — reset and try again."),
                    False,
                ),
                Function(record_lab_mistake),
            ],
        )

    textbutton "Reset":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 890
        action SetVariable("lysate_transfer_amount", 0)

    # Dev only: drop straight onto the target volume.
    if dev_mode:
        textbutton "Fill (dev)":
            style "lab_close_button"
            text_style "lab_close_button_text"
            xpos 1460
            ypos 960
            action SetVariable("lysate_transfer_amount", _target)

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 24
        ypos 24
        action Return("cancel")


screen aw1_pour():
    zorder 115
    modal True
    on "show" action Show("open_inv")

    $ _target = 500
    $ _max = _target + 250
    $ _fill_frac = min(1.0, aw1_pour_amount / float(_max))
    $ _tube_w = 130
    $ _tube_h = 460
    $ _on_target = aw1_pour_amount == _target

    add "backgrounds/station1.png"
    add Solid("#00000099")

    frame:
        xalign 0.5
        ypos 40
        xmaximum 900
        background "#0d1a24ee"
        padding (20, 12)
        vbox:
            spacing 6
            text "Add Buffer AW1 to the new collection tube. Target: exactly [_target] µL":
                size 24
                bold True
                color "#ffffff"
            text "Drag the slider below to pour, tap → for 1 µL, or hold → to pour continuously — it only moves forward, so overshoot means Reset and start again. Ease off as you near the mark, then click Add.":
                size 17
                color "#c5d0d8"
                xmaximum 860

    key "K_RIGHT" action Function(pour_increment, "aw1_pour_amount", _max, 1)
    # Holding the key pours continuously; see pour_hold_tick in styles.rpy.
    timer 0.06 repeat True action Function(pour_hold_tick, "aw1_pour_amount", _max, _target)

    # Collection tube outline with rising Buffer AW1 level tied to the poured amount.
    frame:
        xpos 895
        ypos 220
        xsize _tube_w
        ysize _tube_h
        background "#ffffff22"

        fixed:
            xysize (_tube_w, _tube_h)
            add Solid("#7fe3c9dd" if not _on_target else "#8fffb3dd"):
                xsize (_tube_w - 14)
                ysize int(_tube_h * _fill_frac)
                xalign 0.5
                yalign 1.0

    text "[int(aw1_pour_amount)] µL":
        xpos 960
        ypos 700
        xanchor 0.5
        size 30
        bold True
        color ("#7dffb3" if _on_target else "#ffffff")
        outlines [ (2, "#000000", 0, 0) ]

    frame:
        xpos 292
        ypos 838
        xsize 1116
        ysize 60
        background "#ffffff33"
        padding (8, 8)

        bar:
            xsize 1100
            ysize 44
            value ForwardOnlyValue("aw1_pour_amount", _max, step=5)
            left_bar Solid("#2dd4a7")
            right_bar Solid("#3a4b55")
            thumb Transform(Solid("#ffffff"), xsize=12, ysize=44)

    textbutton "Add":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 820
        action If(
            _on_target,
            [
                Function(custom_notify, "Added {} µL of Buffer AW1 — right on target!".format(int(aw1_pour_amount)), True),
                Return("poured"),
            ],
            [
                Function(
                    custom_notify,
                    ("Not enough yet — keep pouring." if aw1_pour_amount < _target else "Too much — reset and try again."),
                    False,
                ),
                Function(record_lab_mistake),
            ],
        )

    textbutton "Reset":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 890
        action SetVariable("aw1_pour_amount", 0)

    # Dev only: drop straight onto the target volume.
    if dev_mode:
        textbutton "Fill (dev)":
            style "lab_close_button"
            text_style "lab_close_button_text"
            xpos 1460
            ypos 960
            action SetVariable("aw1_pour_amount", _target)

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 24
        ypos 24
        action Return("cancel")


screen ate_pour():
    zorder 115
    modal True
    on "show" action Show("open_inv")

    $ _min_target = 20
    $ _max_target = 100
    $ _max = 150
    $ _fill_frac = min(1.0, ate_pour_amount / float(_max))
    $ _tube_w = 130
    $ _tube_h = 460
    $ _on_target = _min_target <= ate_pour_amount <= _max_target

    add "backgrounds/station1.png"
    add Solid("#00000099")

    frame:
        xalign 0.5
        ypos 40
        xmaximum 900
        background "#0d1a24ee"
        padding (20, 12)
        vbox:
            spacing 6
            text "Apply Buffer ATE to elute the membrane. Target: [_min_target]–[_max_target] µL":
                size 24
                bold True
                color "#ffffff"
            text "Unlike the other reagents, the protocol allows a range here — drag the slider, tap → for 1 µL, or hold → to pour continuously, anywhere between [_min_target] and [_max_target] µL, then click Apply.":
                size 17
                color "#c5d0d8"
                xmaximum 860

    key "K_RIGHT" action Function(pour_increment, "ate_pour_amount", _max, 1)
    # Holding the key pours continuously; see pour_hold_tick in styles.rpy.
    timer 0.06 repeat True action Function(pour_hold_tick, "ate_pour_amount", _max, _min_target)

    # Tube outline with a rising ATE level tied to the applied amount.
    frame:
        xpos 895
        ypos 220
        xsize _tube_w
        ysize _tube_h
        background "#ffffff22"

        fixed:
            xysize (_tube_w, _tube_h)
            add Solid("#d6a9ffdd" if not _on_target else "#8fffb3dd"):
                xsize (_tube_w - 14)
                ysize int(_tube_h * _fill_frac)
                xalign 0.5
                yalign 1.0

    text "[int(ate_pour_amount)] µL":
        xpos 960
        ypos 700
        xanchor 0.5
        size 30
        bold True
        color ("#7dffb3" if _on_target else "#ffffff")
        outlines [ (2, "#000000", 0, 0) ]

    frame:
        xpos 292
        ypos 838
        xsize 1116
        ysize 60
        background "#ffffff33"
        padding (8, 8)

        bar:
            xsize 1100
            ysize 44
            value ForwardOnlyValue("ate_pour_amount", _max, step=5)
            left_bar Solid("#b06bff")
            right_bar Solid("#3a4b55")
            thumb Transform(Solid("#ffffff"), xsize=12, ysize=44)

    textbutton "Apply":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 820
        action If(
            _on_target,
            [
                Function(custom_notify, "Applied {} µL of Buffer ATE — within range!".format(int(ate_pour_amount)), True),
                Return("applied"),
            ],
            [
                Function(
                    custom_notify,
                    (
                        "Not enough yet — the protocol needs at least {} µL.".format(_min_target)
                        if ate_pour_amount < _min_target
                        else "Too much — the protocol caps this at {} µL. Reset and try again.".format(_max_target)
                    ),
                    False,
                ),
                Function(record_lab_mistake),
            ],
        )

    textbutton "Reset":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 1460
        ypos 890
        action SetVariable("ate_pour_amount", 0)

    # Dev only: drop straight onto the target volume.
    if dev_mode:
        textbutton "Fill (dev)":
            style "lab_close_button"
            text_style "lab_close_button_text"
            xpos 1460
            ypos 960
            action SetVariable("ate_pour_amount", _min_target)

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 24
        ypos 24
        action Return("cancel")


# UNUSED: the CE run now advances to cem_finish on a timer instead of waiting
# for a click. Kept in case the click-to-continue gate is ever wanted back.
screen cem_screen():
    zorder 110
    modal True
    imagemap:
        ground "backgrounds/cem_screen_idle.png"
        idle "backgrounds/cem_screen_idle.png"
        hover "backgrounds/cem_screen_idle.png"
        hotspot (486, 300, 140, 648) action Jump("cem_finish")


init -3 python:
    # Matches the Locus / Observed Genotype worksheet the player fills in.
    PROFILE_ANSWERS = [
        ("D3S1358", "16", "18"),
        ("VWA", "17", "18"),
        ("CSF1PO", "11", "12"),
        ("TPOX", "8", "8"),
        ("D8S1179", "14", "16"),
    ]

    class DictInputValue(InputValue):
        def __init__(self, d, key):
            self.d = d
            self.key = key

        def get_text(self):
            return self.d.get(self.key, "")

        def set_text(self, s):
            self.d[self.key] = s
            renpy.restart_interaction()

    def dev_fill_profile_answers():
        """Dev only: fill the worksheet from the answer key already in PROFILE_ANSWERS."""
        for marker, a1, a2 in PROFILE_ANSWERS:
            store.profile_answers[marker] = "{}, {}".format(a1, a2)
            if marker not in store.profile_visited:
                store.profile_visited.append(marker)
        renpy.restart_interaction()

    def profile_answers_reset():
        store.profile_answers = {}
        store.profile_locus_index = 0
        store.profile_visited = []

    def profile_locus_state(marker):
        """'' = nothing typed, 'ok' = matches, 'bad' = filled but does not match."""
        raw = store.profile_answers.get(marker, "")
        if not raw.strip():
            return ""
        for m, a1, a2 in PROFILE_ANSWERS:
            if m == marker:
                parts = [p.strip().upper() for p in raw.replace("/", ",").split(",") if p.strip()]
                return "ok" if sorted(parts) == sorted([a1.upper(), a2.upper()]) else "bad"
        return ""

    def profile_entered_count():
        return sum(1 for m, a1, a2 in PROFILE_ANSWERS if store.profile_answers.get(m, "").strip())

    def profile_flagged_count():
        return sum(1 for m, a1, a2 in PROFILE_ANSWERS if profile_locus_state(m) == "bad")

    def profile_leave_locus():
        """A locus is only marked once the player moves off it, so feedback
        never fires halfway through typing."""
        marker = PROFILE_ANSWERS[store.profile_locus_index][0]
        if marker not in store.profile_visited:
            store.profile_visited.append(marker)

    def profile_go_to(index):
        profile_leave_locus()
        store.profile_locus_index = index
        renpy.restart_interaction()

    def profile_go_next():
        profile_leave_locus()
        store.profile_locus_index = min(store.profile_locus_index + 1, len(PROFILE_ANSWERS) - 1)
        renpy.restart_interaction()

    def profile_go_previous():
        profile_leave_locus()
        store.profile_locus_index = max(store.profile_locus_index - 1, 0)
        renpy.restart_interaction()

    def profile_check_answers():
        wrong = []
        for marker, a1, a2 in PROFILE_ANSWERS:
            raw = store.profile_answers.get(marker, "")
            parts = [p.strip().upper() for p in raw.replace("/", ",").split(",") if p.strip()]
            entered = sorted(parts)
            expected = sorted([a1.upper(), a2.upper()])
            if entered != expected:
                wrong.append(marker)
        if wrong:
            preview = ", ".join(wrong[:4]) + ("…" if len(wrong) > 4 else "")
            custom_notify("{} of {} markers incorrect: {}".format(len(wrong), len(PROFILE_ANSWERS), preview), False)
            record_lab_mistake()
            return False
        custom_notify("All {} markers correctly called!".format(len(PROFILE_ANSWERS)), True)
        return True

    def profile_submit():
        if profile_check_answers():
            renpy.end_interaction("correct")


screen profile_input_screen():
    modal True
    zorder 120
    add Solid("#0b1620")

    $ _locus_i = profile_locus_index
    $ _marker, _a1, _a2 = PROFILE_ANSWERS[_locus_i]
    $ _table_x = 80
    $ _table_y = 340
    $ _table_row_h = 620 // 6
    $ _graph_zoom = 0.606
    $ _graph_w = int(1701 * _graph_zoom)

    text "Read the electropherogram below to determine each genotype:":
        xalign 0.5
        ypos 4
        size 20
        bold True
        color "#ffffff"

    add "backgrounds/graph.png":
        zoom _graph_zoom
        xpos (1920 - _graph_w) // 2
        ypos 40

    add "backgrounds/profile_table_blank.png":
        xpos _table_x
        ypos _table_y

    # Highlight the row the player is currently filling in.
    add Solid("#ffe08055"):
        xpos _table_x
        ypos _table_y + (_locus_i + 1) * _table_row_h
        xsize 900
        ysize _table_row_h

    # Each row's "Observed Genotype" cell: the active locus gets a live text
    # box (type directly on the table); other rows show what's typed so far
    # and can be clicked to jump straight to that locus's entry.
    for _row_i, _row_marker, _row_a1, _row_a2 in [(i, m, a1, a2) for i, (m, a1, a2) in enumerate(PROFILE_ANSWERS)]:
        if _row_i == _locus_i:
            frame:
                xpos _table_x + 350
                ypos _table_y + (_row_i + 1) * _table_row_h + (_table_row_h - 50) // 2
                xsize 520
                ysize 50
                background "#0d1a24"
                padding (10, 6)
                input:
                    value DictInputValue(profile_answers, _row_marker)
                    length 20
                    color "#ffffff"
                    size 26
                    xfill True
        else:
            button:
                xpos _table_x + 340
                ypos _table_y + (_row_i + 1) * _table_row_h
                xsize 560
                ysize _table_row_h
                background Solid("#00000000")
                hover_background Solid("#ffe08033")
                action Function(profile_go_to, _row_i)
                tooltip "Enter [_row_marker]"

                text "[profile_answers.get(_row_marker, '')]":
                    xalign 0.0
                    yalign 0.5
                    xoffset 16
                    size 26
                    color "#1a1a1a"

            # Rows the player has moved on from show whether the call matched.
            $ _row_state = profile_locus_state(_row_marker)
            if _row_state == "ok":
                text "✓":
                    xpos _table_x + 915
                    ypos _table_y + (_row_i + 1) * _table_row_h + 6
                    size 32
                    bold True
                    color "#2ecc71"
            elif _row_state == "bad":
                text "✗":
                    xpos _table_x + 915
                    ypos _table_y + (_row_i + 1) * _table_row_h + 6
                    size 32
                    bold True
                    color "#e6a23c"

    frame:
        xpos 1050
        ypos 360
        xsize 800
        # The dev fill button adds a row, so the panel needs the extra height
        # only when it is present.
        ysize (545 if dev_mode else 470)
        background "#17354aee"
        padding (24, 20)

        vbox:
            spacing 18
            xfill True

            text "Locus [_locus_i + 1] of [len(PROFILE_ANSWERS)]":
                size 18
                color "#7ec8e3"
                bold True

            text "[_marker]":
                size 30
                bold True
                color "#ffffff"

            text "Type the observed genotype directly on the table (e.g. 16, 18):":
                size 18
                color "#c5d0d8"
                xmaximum 750

            $ _entered = profile_entered_count()
            $ _flagged = profile_flagged_count()
            $ _cur_state = profile_locus_state(_marker)

            text "[_entered] of [len(PROFILE_ANSWERS)] loci called.":
                size 18
                color "#8fa6b4"

            # Only warn once the player has left the locus, so the message does
            # not flicker while a genotype is still being typed.
            if _cur_state == "bad" and _marker in profile_visited:
                text "This call does not match [_marker]. Read the two tallest peaks in this locus's window.":
                    size 17
                    color "#e6a23c"
                    xmaximum 750
            elif _flagged:
                text "[_flagged] locus/loci marked ✗ - revisit those rows before submitting.":
                    size 17
                    color "#e6a23c"
                    xmaximum 750

            null height 6

            hbox:
                spacing 12
                textbutton "◀ Previous":
                    style "lab_close_button"
                    text_style "lab_close_button_text"
                    sensitive _locus_i > 0
                    action Function(profile_go_previous)
                textbutton "Next ▶":
                    style "lab_close_button"
                    text_style "lab_close_button_text"
                    sensitive _locus_i < len(PROFILE_ANSWERS) - 1
                    action Function(profile_go_next)

            null height 6

            if dev_mode:
                textbutton "Fill all (dev)":
                    style "lab_close_button"
                    text_style "lab_close_button_text"
                    xfill True
                    action Function(dev_fill_profile_answers)

            textbutton "Submit Profile":
                background "#2ecc71"
                hover_background "#27ae60"
                padding (16, 10)
                text_size 22
                text_color "#ffffff"
                xfill True
                action Function(profile_submit)

            textbutton "Close":
                style "lab_close_button"
                text_style "lab_close_button_text"
                xfill True
                action Return("cancel")

    # Nina's brief stays on screen for the whole task rather than scrolling past
    # in a dialogue box before the table opens.
    frame:
        xpos 1050
        ypos (925 if dev_mode else 850)
        xsize 800
        background "#17354aee"
        padding (20, 16)

        hbox:
            spacing 18

            add "side nina talk":
                zoom 0.42
                yalign 0.5

            vbox:
                spacing 6
                yalign 0.5

                text "Nina":
                    size 20
                    bold True
                    color "#7ec8e3"

                text "Read the electropherogram above and enter the two alleles you see at each locus. Work down the table -- I'll mark anything that doesn't match once you move on.":
                    size 17
                    color "#e2edf3"
                    xmaximum 580

    key "K_RIGHT" action Function(profile_go_next)
    key "K_LEFT" action Function(profile_go_previous)


screen extraction_tube_hud():
    # Shared status for equipping processed tubes on machines.
    zorder 120
    frame:
        xpos 24
        ypos 100
        xmaximum 520
        background "#0d1a24ee"
        padding (16, 12)
        vbox:
            spacing 8
            text "Tubes this step: [extraction_step_tube_count()] / [extraction_step_tubes_needed()] (sample + negative control)":
                size 18
                color "#ffffff"
            $ _rotor_hint = (
                ("in rotor slot " + str(centrifuge_sample_slot)) if centrifuge_sample_slot
                else (("in rotor slot " + str(spinner_sample_slot)) if spinner_sample_slot else "")
            )
            text ("Equipped: " + (extraction_machine_equipped_name if extraction_machine_equipped else (_rotor_hint if _rotor_hint else "none — Use a processed tube from Evidence"))):
                size 16
                color ("#7ec8ff" if (extraction_machine_equipped or centrifuge_sample_slot or spinner_sample_slot) else "#ffcc66")
            if extraction_machine_equipped is not None or centrifuge_sample_item is not None or spinner_sample_item is not None:
                textbutton "Return Tube to Inventory":
                    style "lab_close_button"
                    text_style "lab_close_button_text"
                    action Function(extraction_return_machine_tube)


screen centrifuge():
    zorder 110
    modal True
    on "show" action Show("open_inv")
    use extraction_tube_hud

    add "backgrounds/use_centrifuge.png"

    $ _opp_slot = centrifuge_opposite(centrifuge_sample_slot) if centrifuge_sample_slot else 0

    # Balance status
    frame:
        xpos 24
        ypos 250
        xmaximum 520
        background "#0d1a24ee"
        padding (16, 12)
        vbox:
            spacing 6
            text "Balance the rotor":
                size 18
                color "#ffffff"
            if not centrifuge_sample_slot:
                text "1. Equip your sample tube, then click a numbered slot.":
                    size 15
                    color "#ffcc66"
            elif not centrifuge_balance_slot:
                text "2. Use Negative Control Tube, then click slot [_opp_slot] (opposite).":
                    size 15
                    color ("#7ec8ff" if centrifuge_holding == "neg" else "#ffcc66")
            else:
                text "Rotor balanced — click Run Centrifuge.":
                    size 15
                    color "#7dffb3"
            if centrifuge_holding == "neg":
                text "Holding: Negative Control — click the opposite slot.":
                    size 15
                    color "#7ec8ff"

    # Tube markers in occupied slots
    if centrifuge_sample_slot:
        $ _srect = centrifuge_slot_rect(centrifuge_sample_slot)
        fixed:
            xpos _srect[0]
            ypos _srect[1]
            xysize (_srect[2], _srect[3])
            add Solid("#3aa0ffaa")
            text "S":
                size 18
                color "#ffffff"
                xalign 0.5
                yalign 0.5
    if centrifuge_balance_slot:
        $ _nrect = centrifuge_slot_rect(centrifuge_balance_slot)
        fixed:
            xpos _nrect[0]
            ypos _nrect[1]
            xysize (_nrect[2], _nrect[3])
            add Solid("#ffcc33aa")
            text "N":
                size 18
                color "#1a1a1a"
                xalign 0.5
                yalign 0.5

    # Clickable rotor slots (1–12)
    for _slot in range(1, 13):
        $ _rect = centrifuge_slot_rect(_slot)
        button:
            xpos _rect[0]
            ypos _rect[1]
            xysize (_rect[2], _rect[3])
            background Solid("#ffffff22")
            hover_background Solid("#ffffff55")
            action Function(centrifuge_place_in_slot, _slot)
            tooltip "Slot {}".format(_slot)

    textbutton "Run Centrifuge":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 820
        ypos 780
        action If(
            centrifuge_is_balanced(),
            Jump("centrifuge_run"),
            Show("lab_notify", message="Balance the rotor first: sample + negative control on opposite slots.", correct=False),
        )

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        action [
            If(
                extraction_machine_equipped is not None or centrifuge_sample_item is not None,
                Function(extraction_return_machine_tube),
                NullAction(),
            ),
            Return(),
        ]
        xpos 24
        ypos 24


screen spinner():
    zorder 110
    modal True
    on "show" action Show("open_inv")
    use extraction_tube_hud

    add "backgrounds/use_spinner.png"

    $ _opp_slot = spinner_opposite(spinner_sample_slot) if spinner_sample_slot else 0

    frame:
        xpos 24
        ypos 220
        xmaximum 480
        background "#0d1a24ee"
        padding (16, 12)
        vbox:
            spacing 6
            text "Balance the mini centrifuge (6-slot rotor):":
                size 17
                color "#ffffff"
            if extraction_expected_tool() != "spinner":
                text "Not the mini-centrifuge step yet — check the notebook.":
                    size 15
                    color "#ff8888"
            if not spinner_sample_slot:
                text "1. Equip your sample tube, then click a numbered slot.":
                    size 15
                    color "#ffcc66"
            elif not spinner_balance_slot:
                text "2. Use Negative Control Tube, then click slot [_opp_slot] (opposite).":
                    size 15
                    color ("#7ec8ff" if spinner_holding == "neg" else "#ffcc66")
            else:
                text "Rotor balanced — click Run Mini Centrifuge.":
                    size 15
                    color "#7dffb3"
            if spinner_holding == "neg":
                text "Holding: Negative Control — click the opposite slot.":
                    size 15
                    color "#7ec8ff"

    if spinner_sample_slot:
        $ _srect = spinner_slot_rect(spinner_sample_slot)
        fixed:
            xpos _srect[0]
            ypos _srect[1]
            xysize (_srect[2], _srect[3])
            add Solid("#3aa0ffaa")
            text "S":
                size 18
                color "#ffffff"
                xalign 0.5
                yalign 0.5
    if spinner_balance_slot:
        $ _nrect = spinner_slot_rect(spinner_balance_slot)
        fixed:
            xpos _nrect[0]
            ypos _nrect[1]
            xysize (_nrect[2], _nrect[3])
            add Solid("#ffcc33aa")
            text "N":
                size 18
                color "#1a1a1a"
                xalign 0.5
                yalign 0.5

    for _slot in range(1, 7):
        $ _rect = spinner_slot_rect(_slot)
        button:
            xpos _rect[0]
            ypos _rect[1]
            xysize (_rect[2], _rect[3])
            background Solid("#ffffff22")
            hover_background Solid("#ffffff55")
            action Function(spinner_place_in_slot, _slot)
            tooltip "Slot {}".format(_slot)

    textbutton "Run Mini Centrifuge":
        style "lab_close_button"
        text_style "lab_close_button_text"
        xpos 780
        ypos 900
        action If(
            extraction_expected_tool() != "spinner",
            [
                Show("lab_notify", message="Not the mini-centrifuge step yet. Check the notebook.", correct=False),
                Function(record_lab_mistake),
            ],
            If(
                spinner_is_balanced(),
                Jump("spinner_run"),
                Show("lab_notify", message="Balance the rotor first: sample + negative control on opposite slots.", correct=False),
            ),
        )

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        action [
            If(
                extraction_machine_equipped is not None or spinner_sample_item is not None,
                Function(extraction_return_machine_tube),
                NullAction(),
            ),
            Return(),
        ]
        xpos 24
        ypos 24


screen vortex():
    zorder 110
    modal True
    on "show" action Show("open_inv")
    use extraction_tube_hud
    imagemap:
        ground "backgrounds/use_vortex.png"
        idle "backgrounds/use_vortex.png"
        hover "backgrounds/use_vortex_hover.png"
        hotspot (842, 429, 329, 552):
            action If(
                extraction_expected_tool() == "vortex",
                Jump("vortex_set_time"),
                [
                    Show(
                        "lab_notify",
                        message=(
                            "Add Buffer AL at Prep first, then come back to vortex."
                            if extraction_expected_tool() == "al"
                            else (
                                "Next step needs a different machine. Check the notebook."
                                if extraction_expected_tool() not in (None, "prep")
                                else "Finish Prep and choose a tube first, then come back."
                            )
                        ),
                        correct=False,
                    ),
                    Function(record_lab_mistake),
                ],
            )
    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        action [
            If(extraction_machine_equipped is not None, Function(extraction_return_machine_tube), NullAction()),
            Return(),
        ]
        xpos 24
        ypos 24


screen incubator():
    zorder 110
    modal True
    on "show" action Show("open_inv")
    # set_70 only changes temperature — no tube on the machine.
    if extraction_current() is None or extraction_current()[0] != "set_70":
        use extraction_tube_hud
    imagemap:
        ground "backgrounds/use_incubator.png"
        idle "backgrounds/use_incubator.png"
        hover "backgrounds/use_incubator_hover.png"
        hotspot (599, 157, 719, 815):
            action If(
                extraction_expected_tool() in ("incubator", "wait"),
                If(
                    (extraction_current() is not None and extraction_current()[0] == "set_70")
                    or extraction_machine_equipped is not None,
                    Jump("incubator_question"),
                    Show("lab_notify", message="Equip a processed swab tube from Evidence first.", correct=False),
                ),
                [
                    Show("lab_notify", message="Nothing ready for the thermomixer yet.", correct=False),
                    Function(record_lab_mistake),
                ],
            )
    if incubator_loaded_tubes:
        frame:
            xpos 24
            ypos 180
            xmaximum 480
            background "#0d1a24ee"
            padding (16, 12)
            vbox:
                spacing 6
                text "Loaded in thermomixer ({}/{}):".format(
                    len(incubator_loaded_tubes), len(extraction_required_processed_tubes())
                ):
                    size 16
                    color "#ffffff"
                for _loaded_item in incubator_loaded_tubes:
                    text "• [_loaded_item.name]":
                        size 15
                        color "#7ec8ff"

    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        action [
            If(extraction_machine_equipped is not None, Function(extraction_return_machine_tube), NullAction()),
            If(bool(incubator_loaded_tubes), Function(incubator_dual_reset), NullAction()),
            Return(),
        ]
        xpos 24
        ypos 24


screen qpcr():
    # Legacy one-click tray hotspot. Kept as a fallback entry that now launches
    # the interactive plate-preparation mini-game.
    zorder 110
    modal True
    imagemap:
        ground "backgrounds/use_qpcr.png"
        idle "backgrounds/use_qpcr.png"
        hover "backgrounds/use_qpcr_hover.png"
        hotspot (860, 561, 301, 156):
            action Jump("use_qpcr")
    textbutton "Close":
        style "lab_close_button"
        text_style "lab_close_button_text"
        action Return()
        xpos 24
        ypos 24


screen data_analysis_lab_screen():
    add "afis_interface"
    imagebutton:
        xpos 20
        ypos 900
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        action Jump("return_bio_station")
    imagebutton:
        idle "afis_software_idle"
        hover "afis_software_hover"
        xpos 480
        ypos 220
        action Jump("lab_computer")
    key "K_LEFT" action Jump("return_bio_station")
