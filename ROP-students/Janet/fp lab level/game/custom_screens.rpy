# initial screen
screen lab_hallway_screen:
    image "lab_hallway_dim"
    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            hovered Notify("Data Analysis Lab")
            unhovered Notify('')
            action Jump('data_analysis_lab')
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            hovered Notify("Materials Lab")
            unhovered Notify('')
            action Jump('materials_lab')

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "afis_software_idle"
            hover "afis_software_hover"
            action Jump('afis')
    hbox:
        xpos 0.35 yalign 0.28
        imagebutton:
            idle "pdq"
            hover "pdq_hover"
            action Jump('pdq')

screen pre_afis_screen:
    imagemap:
        idle "software_interface"
        hover "software_import_hover"
        hotspot (282,241,680,756) action [Jump('fingerprint_upload')]

screen afis_screen:
    default afis_bg = "software_laptop_fingerprint"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    image afis_bg

    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Search'):
            sensitive not interface_search
            style "afis_button"
            action [
                ToggleLocalVariable('interface_search'),
                SetLocalVariable('afis_bg', 'software_search'),
                Function(calculate_afis, current_evidence),
                Function(set_cursor, '')]

    # showif interface_imported:
    #     hbox:
    #         xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
    #         image current_evidence.afis_details['image']
    
    showif interface_search:
        # for i in range(len(afis_search)):
        hbox:
            xpos 0.61 ypos 0.505
            hbox:
                text("{color=#000000}Crowbar Fingerprint{/color}")
        hbox:
            xpos 0.53 ypos 0.505
            hbox:
                text("{color=#000000}92.2{/color}")
        textbutton('Finish'):
            xpos 0.75 ypos 0.8
            style "afis_button"
            action [Jump('afis_done')]

screen pdq_screen:
    hbox:
        xalign 0.8 yalign 0.95
        imagebutton:
            idle "lab_notes"
    hbox:
        xalign 0.5 yalign 0.344
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.361
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.378
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('correct_car')
    hbox:
        xalign 0.5 yalign 0.395
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.395
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.412
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.429
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.447
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.465
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.482
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.499
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.516
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.534
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.552
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.570
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.588
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.605
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.622
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.639
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    hbox:
        xalign 0.5 yalign 0.658
        imagebutton:
            idle "data_idle"
            hover "data_highlight"
            action Jump('incorrect_car')
    
#################################### MATERIALS ####################################
screen materials_lab_screen:
    image "materials_lab"

    hbox:
        xpos 0.15 yalign 0.5
        imagebutton:
            idle "wet_lab_idle"
            hover "wet_lab_hover"
            hovered Notify("Wet Lab")
            unhovered Notify('')
            action Jump('wet_lab')
    hbox:
        xpos 0.4 yalign 0.5
        imagebutton:
            idle "fingerprint_development_idle"
            hover "fingerprint_development_hover"
            hovered Notify("Fingerprint Development")
            unhovered Notify('')
            action Jump('fingerprint_development')
    
    hbox:
        xpos 0.62 yalign 0.5
        imagebutton:
            idle "analytical_instruments_idle"
            hover "analytical_instruments_hover"
            hovered Notify("Analytical Instruments")
            unhovered Notify('')
            action Jump('analytical_instruments')

screen wet_lab_screen:
    image "fumehood"

screen fingerprint_development_screen:
    image "chamber_outside"
    hbox:
        xalign 0.53 yalign 0.75
        imagebutton:
            idle "chamber_door"
            hover "chamber_door_hover"
            action Jump('crowbar_development')

screen analytical_instruments_screen:
    image "lab_bench"
    hbox:
        xalign 0.47 yalign 0.31
        imagebutton:
            idle "microscope_select"
            hover "microscope_select_hover"
            action [Jump("paint_chip_examine")]
    hbox:
        xalign 0.6 yalign 0.31
        imagebutton:
            idle "centrifuge"
            hover "centrifuge_hover"
            action [SetVariable("instrument_choice", "centrifuge"), Jump("pre_paint")]
    hbox:
        xalign 0.84 yalign 0.4
        imagebutton:
            idle "hot_plate"
            hover "hotplate_hover"
            action [SetVariable("instrument_choice", "hotplate"), Jump("pre_paint")]
    hbox:
        xalign 0.2 yalign 0.61
        imagebutton:
            idle "thermocycler"
            hover "thermocycler_hover"
            action [SetVariable("instrument_choice", "thermocycler"), Jump("pre_paint")]
    hbox:
        xalign 0.47 yalign 0.61
        imagebutton:
            idle "gel"
            hover "gel_hover"
            action [SetVariable("instrument_choice", "gel"), Jump("pre_paint")]

screen crowbar_development:
    hbox:
        xalign 0.49 yalign 0.2
        imagebutton:
            idle "bar_holder"
            hover "bar_holder_hover"
            action [Function(set_cursor, ''), Jump('crowbar_development_cont')]

screen reservoir_dev:
    image "chamber_crowbar"
    if left_complete == False:
        hbox:
            xalign 0.4 yalign 0.68
            imagebutton:
                idle "reservoir"
                hover "reservoir_hover"
                action Jump('reservoir_development_left')
    if right_complete == False:
        hbox:
            xalign 0.58 yalign 0.68
            imagebutton:
                idle "reservoir"
                hover "reservoir_hover"
                action Jump('reservoir_development_right')
    else:
        hbox:
            xalign 0.7 yalign 0.5
            imagebutton:
                idle "close_button"
                hover "close_button_hover"
                action Jump('fumigation')

screen dyes:
    hbox:
        xalign 0.2 yalign 0.5
        imagebutton:
            idle "ninhydrin"
            hover "ninhydrin_hover"
            action [Function(set_cursor, ''), Jump('n_chosen')]
    hbox:
        xalign 0.4 yalign 0.5
        imagebutton:
            idle "rhodamine"
            hover "rhodamine_hover"
            action [Function(set_cursor, 'r_dropper'), Jump('r_chosen')]
    hbox:
        xalign 0.6 yalign 0.5
        imagebutton:
            idle "silver_nitrate"
            hover "silver_nitrate_hover"
            action [Function(set_cursor, ''), Jump('s_chosen')]
    hbox:
        xalign 0.8 yalign 0.5
        imagebutton:
            idle "ardrox"
            hover "ardrox_hover"
            action [Function(set_cursor, 'a_dropper'), Jump('a_chosen')]

screen drag_paint_chip:
    if chip_picked == False:
        hbox:
            xalign 0.15 yalign 0.6
            imagebutton:
                idle "paint_select"
                hover "paint_hover"
                action [Function(set_cursor, 'tweezer_chip'), SetVariable("chip_picked", True)]
    else: 
        hbox:
            xalign 0.6 yalign 0.45
            imagebutton:
                idle "evidence_drop"
                hover "evidence_drop_hover"
                action [Function(set_cursor, ''), Jump('microscope_chip')]

screen identify_layers:
    if layer1_clicked == False:
        hbox:
            xalign 0.5 yalign 0.5
            imagebutton:
                idle "layer1"
                hover "layer1_hover"
                action [SetVariable("just_clicked", 1), SetVariable("layer1_clicked", True), Jump("layer_quiz")]
    if layer2_clicked == False:
        hbox:
            xalign 0.5 yalign 0.6
            imagebutton:
                idle "layer2"
                hover "layer2_hover"
                action [SetVariable("just_clicked", 2), SetVariable("layer2_clicked", True), Jump("layer_quiz")]
    if layer3_clicked == False:
        hbox:
            xalign 0.5 yalign 0.7
            imagebutton:
                idle "layer3"
                hover "layer3_hover"
                action [SetVariable("just_clicked", 3), SetVariable("layer3_clicked", True), Jump("layer_quiz")]
    if layer4_clicked == False:
        hbox:
            xalign 0.5 yalign 0.75
            imagebutton:
                idle "layer4"
                hover "layer4_hover"
                action [SetVariable("just_clicked", 4), SetVariable("layer4_clicked", True), Jump("layer_quiz")]

screen scalpel_orientation:
    if orientation == "correct":
        hbox:
            xalign 0.6 yalign 0.7
            imagebutton:
                idle "scalpel_correct"
    if orientation == "incorrect":
        hbox:
            xalign 0.6 yalign 0.7
            imagebutton:
                idle "scalpel_incorrect"
    hbox:
        xalign 0.5 yalign 0.8
        imagebutton:
            idle "arrow_left"
            hover "arrow_left_hover"
            action [SetVariable("orientation", "correct"), Jump('orient')]
    hbox:
        xalign 0.9 yalign 0.8
        imagebutton:
            idle "arrow_right"
            hover "arrow_right_hover"
            action [SetVariable("orientation", "incorrect"), Jump('orient')]
    hbox:
        xalign 0.3 yalign 0.8
        imagebutton:
            idle "set_button"
            hover "set_button_hover"
            action [Jump('put_blade')]

screen check_layers:
    if layer1_clicked == False:
        hbox:
            xalign 0.5 yalign 0.5
            imagebutton:
                idle "layer1_hover"
                hover "layer1_hover"
                action [SetVariable("just_clicked", 1), SetVariable("layer1_clicked", True), Jump("layer_check_call")]
    else:
        hbox:
            xalign 0.7 yalign 0.5
            imagebutton:
                idle "checkmark"
    if layer2_clicked == False:
        hbox:
            xalign 0.5 yalign 0.6
            imagebutton:
                idle "layer2_hover"
                hover "layer2_hover"
                action [SetVariable("just_clicked", 2), SetVariable("layer2_clicked", True), Jump("layer_check_call")]
    else:
        hbox:
            xalign 0.7 yalign 0.6
            imagebutton:
                idle "checkmark"
    if layer3_clicked == False:
        hbox:
            xalign 0.5 yalign 0.7
            imagebutton:
                idle "layer3_hover"
                hover "layer3_hover"
                action [SetVariable("just_clicked", 3), SetVariable("layer3_clicked", True), Jump("layer_check_call")]
    else:
        hbox:
            xalign 0.7 yalign 0.7
            imagebutton:
                idle "checkmark"
    if layer4_clicked == False:
        hbox:
            xalign 0.5 yalign 0.75
            imagebutton:
                idle "layer4_hover"
                hover "layer4_hover"
                action [SetVariable("just_clicked", 4), SetVariable("layer4_clicked", True), Jump("layer_check_call")]
    else:
        hbox:
            xalign 0.7 yalign 0.75
            imagebutton:
                idle "checkmark"