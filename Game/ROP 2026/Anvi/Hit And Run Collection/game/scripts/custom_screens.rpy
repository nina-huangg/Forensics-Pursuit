###############################
# EVIDENCE COLLECTION SCREENS
###############################

screen motorcycle():

    # Background
    add Transform("motorcycle", xysize=(1920, 1080))

    # Motorcycle hotspot
    imagebutton:
        idle Transform("bike_on_ground", xysize=(633, 282))
        hover Transform("bike_on_ground_hover", xysize=(633, 282))
        xpos 553
        ypos 690
        action Jump("closeup")
        focus_mask True

    # Tire tracks hotspot
    imagebutton:
        idle Transform("tracks_on_ground")
        hover Transform("tracks_on_ground_hover")
        xpos 730
        ypos 406
        action Jump("tiretracks")
        focus_mask True

screen closeup():

    add Transform("closeup", xysize=(1920, 1080))

    # imagemap:
    #     idle Transform("closeup", xysize=(1920, 1080))

    #     hotspot (1698, 547, 90, 69) action Jump("paint")
    imagebutton:
        idle Transform("paint_on_bike")
        hover Transform("paint_on_bike_hover")
        xpos 1745
        ypos 526
        action Jump("paint")
        focus_mask True

screen fold_to_envelope():
    draggroup:
        drag:
            drag_name "druggist_fold"
            child "toolbox-druggist_fold"
            xpos 0.25 ypos 0.23
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "envelope"
            child "toolbox-envelope"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen envelope_to_bag():
    draggroup:
        drag:
            drag_name "envelope"
            child "toolbox-envelope"
            xpos 0.25 ypos 0.23
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "bag"
            child "toolbox-evidence_bag"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen impression_to_envelope():
    draggroup:
        drag:
            drag_name "track_impression_gel"
            child "toolbox-gel_lifter_cover"
            xpos 0.25 ypos 0.23
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "envelope"
            child "toolbox-envelope"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen bag_to_tape():
    draggroup:
        drag:
            drag_name "bag"
            child "toolbox-evidence_bag"
            xpos 0.25 ypos 0.23
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "tape"
            child "toolbox-tamper_evident_tape"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen druggist_paper_use():
    modal True
    tag rack_paper_powder

    add "toolbox-druggist_paper" xalign 0.5 yalign 0.5

    frame:
        background Solid("#00000080")  # black at 50% opacity
        xalign 0.5 yalign 0.8
        xpadding 30 ypadding 30

        vbox:
            spacing 20

            text "What kind of fold would you like to perform?" size 30 color "#FFF"

            textbutton "Simple Fold":
                background Solid("#FFFFFF50")
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("simple_fold_chosen"),
                ]

            textbutton "Envelope Fold":
                background Solid("#FFFFFF50")
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("envelope_fold_chosen"),
                ]

            textbutton "Druggist Fold":
                background Solid("#FFFFFF50") # white at 30% opacity
                padding (10, 5)
                action [
                    Hide("druggist_paper_use"),
                    Jump("druggist_paper_correct_choice")
                ]

            textbutton "No Fold":
                background Solid("#FFFFFF50")
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("no_fold_chosen"),
                ]

label simple_fold_chosen():
    "That won't secure the sample properly."
    call screen druggist_paper_use

label envelope_fold_chosen():
    "That wastes evidence; try again."
    call screen druggist_paper_use

label no_fold_chosen():
    "You need to fold it to keep the paint chips inside."
    call screen druggist_paper_use

###############################
# LAB SCREENS
###############################

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
        xpadding 10
        ypadding 20
        background "images/ui/notebook_paper.png"

        vbox:
            spacing 10
            label " " style "heading_text"

            for i, task in enumerate(tasks, 1):
                if tasks[task]:
                    text f"{i}. {task}" style "strikethrough_text"
                else:
                    text f"{i}. {task}" color "#555555"
            
            # if not more_details_clicked:
            #     textbutton "More Details" at blink:
            #         xalign 1.0
            #         action [
            #             SetVariable("more_details_clicked", True),
            #             ToggleVariable("instructions_clicked"),
            #             ToggleScreen("notebook_instructions_screen")
            #         ]
            #         text_size 20
            #         # text_style "more_details_text"
            # else:
            #     textbutton "More Details":
            #         xalign 1.0
            #         action [
            #             ToggleVariable("instructions_clicked"),
            #             ToggleScreen("notebook_instructions_screen")
            #         ]
            #         text_size 20
            #         # text_style "more_details_text"


# screen notebook_instructions_screen():
#     zorder 100

#     frame:
#         xalign 0.92
#         yalign 0.5
#         xsize 600
#         ysize 400
#         background "images/ui/notebook_paper_long.png"
#         padding (20, 20)

#         vbox:
#             spacing 15
#             text "Instructions" style "heading_text"

#             for i, (task_key, step) in enumerate(notebook_instructions, 1):
#                 if swab_tasks.get(task_key, False):
#                     text f"{i}. {step}" style "instructions_strikethrough_text"
#                 else:
#                     text f"{i}. {step}" style "instructions_text"

screen notes_notebook():
    zorder 100
    imagebutton:
        idle (Animation("images/ui/notebook_icon.png", 0.5, "images/ui/notebook_icon_hover.png", 0.5) if not notes_notebook_clicked else "images/ui/notebook_icon.png")
        hover "images/ui/notebook_icon_hover.png"
        xalign 0.03 ypos 20
        at Transform(zoom=0.15)
        action [Function(toggle_notes_notebook), SetVariable("notes_notebook_clicked", True)]

screen notes_notebook_screen():

    zorder 100

    frame:
        xalign 0.12 
        yalign 0.02
        xsize 610
        ysize 500
        background "images/ui/notes_notebook_paper.png"
        xpadding 20
        ypadding 20

        vbox:
            spacing 10

            label " " style "heading_text"

            input:
                value VariableInputValue("notebook_notes")
                multiline True
                allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?;:()[]{}<>@#$%^&*-_=+|/\\\"' \n"
                color "#555555" 
                length 5000
                pixel_width 540

# STATIONS
screen bio_station():
    zorder 0
    imagemap:
        idle Transform("backgrounds/stereomicroscope_bg.png", xysize=(1920, 1080)) 
        hover Transform("backgrounds/stereomicroscope_bg_hover.png", xysize=(1920, 1080))

        hotspot (47, 100, 1960, 1000) action Jump("use_computer")
        # hotspot (811, 411, 229, 290) action Jump("use_qpcr")
        # hotspot (1040, 460, 241, 212) action Jump("use_centrifuge")
        # hotspot (1276, 417, 174, 257) action Jump("use_spinner")
        # hotspot (1458, 475, 126, 228) action Jump("use_vortex")
        # hotspot (1594, 571, 184, 174) action Jump("use_incubator")
        # hotspot (1634, 455, 228, 135) action Jump("use_prep")

    imagebutton:
        xpos 1700
        ypos 900
        idle "ui/right_arrow.png"
        hover "ui/right_arrow_hover.png"
        action [Jump("impression_station"), SetVariable(location, "impression_station")]#"chem_station")
    key "K_RIGHT" action [Jump("impression_station"), SetVariable(location, "impression_station")]
    key "K_d" action [Jump("impression_station"), SetVariable(location, "impression_station")]

    imagebutton:
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        xpos 20
        ypos 900
        action [Jump("use_ftir"), SetVariable(location, "ftir_station")]
    key "K_LEFT" action [Jump("use_ftir"), SetVariable(location, "ftir_station")]
    key "K_a" action [Jump("use_ftir"), SetVariable(location, "ftir_station")]
    
screen ftir_station():
    zorder 0

    add Transform("backgrounds/ftir_bg.png", xysize=(1920, 1080))

    imagebutton:
        xpos 1700
        ypos 900
        idle "ui/right_arrow.png"
        hover "ui/right_arrow_hover.png"
        action [Jump("bio_station"), SetVariable(location, "bio_station"), Hide("ftir_display")]
    key "K_RIGHT" action [Jump("bio_station"), SetVariable(location, "bio_station"), Hide("ftir_display")]
    key "K_d" action [Jump("bio_station"), SetVariable(location, "bio_station"), Hide("ftir_display")]

# screen analyzing_ftir:
#     text "Analyzing..." xpos 0.725 ypos 0.385 size 50 color "#ffffff"

# screen analysis_result:
#     add Transform("ftir_results/ftir_[paint_sample].png", xysize=(750, 560)):
#         xpos 500
#         ypos 210

screen ftir_display():

    if ftir_analyzing:
        text "Analyzing..." xpos 0.525 ypos 0.25 size 50 color "#ffffff"

    elif ftir_result is not None:
        add Transform(
            "ftir_results/ftir_[ftir_result].png",
            xysize=(850, 450)
        ):
            xpos 712
            ypos 100

screen computer_screen():
    zorder 0
    modal False

    add Transform("backgrounds/stereomicroscope_ui.png", xysize=(1920, 1080))

    # $ img = f"{paint_sample}/paint_{abs(stereomicroscope_focus)}.png"

    add Transform("[paint_sample]/paint_[abs(stereomicroscope_focus)].png", xysize=(750, 560)):
        xpos 500
        ypos 210

    imagebutton:
        idle "ui/right_arrow.png"
        hover "ui/right_arrow_hover.png"
        xpos 1550
        ypos 300
        action If(
            stereomicroscope_focus < 6,
            SetVariable("stereomicroscope_focus", stereomicroscope_focus + 1),
            Function(
                lambda:
                    custom_notify("Cannot adjust further in this direction", correct=False)
            )
        )

    imagebutton:
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        xpos 1350
        ypos 300
        action If(
            stereomicroscope_focus > -6,
            SetVariable("stereomicroscope_focus", stereomicroscope_focus - 1),
            Function(
                lambda:
                    custom_notify("Cannot adjust further in this direction", correct=False)
            )
        )

    imagebutton:
        idle "ui/checkmark.png"
        hover "ui/checkmark-hover.png"
        xpos 1450
        ypos 500
        action If(
            -1 <= stereomicroscope_focus <= 1,
            If(
                paint_sample == "known_paint",
                Show("stereomicroscope_layer_check"),
                Show("stereomicroscope_unknown_check"),
            ),
            Function(
                lambda:
                    custom_notify("Image needs to be more focused", correct=False)
            )
        )

screen stereomicroscope_layer_check():
    modal True
    zorder 100

    frame:
        background Solid("#00000080")  # black at 50% opacity
        xalign 0.5 yalign 0.8
        xpadding 30 ypadding 30

        vbox:
            spacing 20

            text "How many layers are visible?" size 30 color "#FFF"

            textbutton "2":
                background Solid("#13121250")
                padding (10, 5)
                action [
                    Function(
                        lambda:
                            custom_notify("Are you sure?", correct=False)
                    )
                ]

            textbutton "3":
                background Solid("#13121250")
                padding (10, 5)
                action [
                    Hide("stereomicroscope_layer_check"),
                    Jump("stereomicroscope_check_correct_layer_choice"),
                ]

            textbutton "4":
                background Solid("#13121250") # white at 30% opacity
                padding (10, 5)
                action [
                    Function(
                        lambda:
                            custom_notify("Are you sure?", correct=False)
                    )
                ]

init python:
    def check_exclude_button():
        global exclude_warning_shown

        if paint_sample in ("unknown2_paint"):
            if not exclude_warning_shown:
                exclude_warning_shown = True
                custom_notify("Are you sure?", correct=False)
            else:
                renpy.hide_screen("stereomicroscope_unknown_check")
                renpy.jump("stereomicroscope_check_exclude")
        else:
            renpy.hide_screen("stereomicroscope_unknown_check")
            renpy.jump("stereomicroscope_check_exclude")

    def check_identification_button():
        global identification_warning_shown

        if not identification_warning_shown:
                identification_warning_shown = True
                custom_notify("Are you sure?", correct=False)
        else:
            renpy.hide_screen("stereomicroscope_unknown_check")
            renpy.jump("stereomicroscope_check_identification")

screen stereomicroscope_unknown_check():
    modal True
    zorder 100

    frame:
        background Solid("#00000080")  # black at 50% opacity
        xalign 0.5 yalign 0.8
        xpadding 30 ypadding 30

        vbox:
            spacing 20

            text "Comparing this sample to the known, what conclusion can you draw?" size 30 color "#FFF"

            textbutton "Exclude - does not match known sample at all":
                background Solid("#13121250")
                padding (10, 5)
                action Function(check_exclude_button)
                # action [
                #     Function(
                #         lambda:
                #             custom_notify("Are you sure?", correct=False)
                #     )
                # ]

            textbutton "Cannot exclude - may match known sample":
                background Solid("#13121250")
                padding (10, 5)
                action [
                    Hide("stereomicroscope_unknown_check"),
                    Jump("stereomicroscope_check_cannot_exclude"),
                ]

            textbutton "Identification - matches known sample":
                background Solid("#13121250") # white at 30% opacity
                padding (10, 5)
                action Function(check_identification_button)

screen final_paint_check():
    modal True
    zorder 100

    frame:
        background Solid("#00000080")  # black at 50% opacity
        xalign 0.5 yalign 0.8
        xpadding 30 ypadding 30

        vbox:
            spacing 20

            text "Which unknown sample is most similar to the one found at the scene? (No warnings will be given now.)" size 30 color "#FFF"

            if "unknown1_paint_analyzed" in paint_ftir:
                textbutton "Unknown Sample 1":
                    background Solid("#FFFFFF50")
                    padding (10, 5)
                    action [SetVariable(paint_sample, "unknown1_paint"),
                        Hide("final_paint_check"),
                        Jump("final_paint_check_choice"),
                    ]

            if "unknown2_paint_analyzed" in paint_ftir:
                textbutton "Unknown Sample 2":
                    background Solid("#FFFFFF50")
                    padding (10, 5)
                    action [SetVariable(paint_sample, "unknown2_paint"),
                        Hide("final_paint_check"),
                        Jump("final_paint_check_choice"),
                    ]

            if "unknown3_paint_analyzed" in paint_ftir:
                textbutton "Unknown Sample 3":
                    background Solid("#FFFFFF50") # white at 30% opacity
                    padding (10, 5)
                    action [SetVariable(paint_sample, "unknown3_paint"),
                        Hide("final_paint_check"),
                        Jump("final_paint_check_choice"),
                    ]
            
            textbutton "I'm not sure yet... I need more time!":
                background Solid("#FFFFFF50") # white at 30% opacity
                padding (10, 5)
                action [SetVariable(paint_sample, "unknown3_paint"),
                    Hide("final_paint_check"),
                    Jump("final_paint_check_start_over"),
                ]

label incorrect_final_paint_choice():
    n "Incorrect; recall the appearance of each sample carefully!"
    show screen computer_screen
    call screen final_paint_check

screen impression_station():
    imagebutton:
        xpos 20
        ypos 900
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        action [Jump("bio_station"), SetVariable(location, "bio_station")]
    key "K_LEFT" action [Jump("bio_station"), SetVariable(location, "bio_station")]
    key "K_a" action [Jump("bio_station"), SetVariable(location, "bio_station")]

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    imagebutton:
        xpos 20
        ypos 900
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        action Jump("bio_station")#"chem_station")
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "afis_software_idle"
            hover "afis_software_hover"
            action Jump("computer")
        key "K_LEFT" action Jump("bio_station")#"chem_station")

screen afis_screen:
    default afis_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    add afis_bg

    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleLocalVariable('interface_import'),
                ToggleVariable('show_case_files'),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('interface_search', False),
                SetLocalVariable('afis_bg', 'software_interface'),
                Function(set_cursor, '')]
    
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
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            hotspot (282,241,680,756) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    showif interface_search:
        if afis_search:
            for i in range(len(afis_search)):
                hbox:
                    xpos afis_search_coordinates[i]['xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].name+"{/color}")
                hbox:
                    xpos afis_search_coordinates[i]['score_xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['score']+"{/color}")
            
        else:
            hbox:
                xpos 0.57 yalign 0.85
                hbox:
                    text("{color=#000000}No match found in records.{/color}")