transform smaller_back_button():
    zoom 0.25

screen back_button():
    hbox:
        xpos 0.9 ypos 0.85
        imagebutton:
            idle "back_button" at smaller_back_button
            hover "back_button_hover"

            action Jump("back")

screen dont_need():
    zorder 52
    tag dont_need
    frame:
        xpos 0.38 ypos 0.4
        vbox:
            text "We don't need to use this here."
            textbutton "Okay":
                action Return(True)

transform smaller_button():
    zoom 0.5

screen camera_screen():
    zorder 51
    tag camera_sccreen
    hbox:
        xpos 0.16 ypos 0.001
        imagebutton:
            idle "camera_idle" at smaller_button
            hover "camera_hover"

            action Jump("took_photo")

# Screen for in the lab hallway
screen in_hallway():
    zorder 50
    hbox:
        xpos 0.21 ypos 0.32
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"

            action Jump("enter_data_analysis_lab")

    hbox:
        xpos 0.51 ypos 0.3
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"

            action Jump("enter_materials_lab")

screen choose_icon():
    zorder 50
    hbox:
        xpos 0.25729167 ypos 0.20185185
        imagebutton:
            idle "afis_icon_idle"
            hover "afis_icon_hover"

            action NullAction()

    hbox:
        xpos 0.3078125 ypos 0.19814815
        imagebutton:
            idle "dna_comparison_icon_idle"
            hover "dna_comparison_icon_hover"

            action Jump("display_table_of_findings")
        
transform smaller_machine():
    zoom 0.1

screen choose_lab():
    zorder 50
    hbox:
        xpos 0.3 ypos 0.25
        imagebutton:
            idle "biology_lab_button_idle"
            hover "biology_lab_button_hover"

            action Jump("in_biology_lab")

    hbox:
        xpos 0.6 ypos 0.25
        imagebutton:
            idle "chemistry_lab_button_idle"
            hover "chemistry_lab_button_hover"

            action Jump("in_chemistry_lab")

    hbox:
        xpos 0.4 ypos 0.5
        imagebutton:
            idle "lab_bench_button_idle"
            hover "lab_bench_button_hover"

            action Jump("lab_bench")

screen choose_machine():
    zorder 50

    hbox:
        xpos 0.25 ypos 0.3
        imagebutton:
            idle "fumehood_idle" at smaller_machine
            hover "fumehood_hover"

            action Jump("fumehood")

    hbox:
        xpos 0.5 ypos 0.3
        imagebutton:
            idle "cyano_idle" at smaller_machine
            hover "cyano_hover"

            action Jump("cyanosafe_machine")

screen open_cyanosafe_door():
    zorder 50
    hbox:
        xpos 0.30729167 ypos 0.36666667
        imagebutton:
            idle "open_cyanosafe_far_idle"
            hover "open_cyanosafe_far_hover"

            action Jump("open_cyanosafe")

screen inspect_cyanosafe():
    zorder 50
    hbox:
        xpos 0.32552083 ypos 0.38888889
        imagebutton:
            idle "inspect_cyanosafe_idle"
            hover "inspect_cyanosafe_hover"

            action Jump("go_closer_to_cyanosafe") mouse ("important")

screen place_knife_in_cyanosafe():
    zorder 50
    tag place_knife_in_cyanosafe
    hbox:
        xpos 0.46822917 ypos 0.13703704
        imagebutton:
            idle "put_knife_in_idle"
            hover "put_knife_in_hover"

            action Jump("added_item_to_cyanosafe")

screen add_superglue_to_cyanosafe():
    zorder 50
    tag add_superglue_to_cyanosafe
    hbox:
        xpos 0.35364583 ypos 0.80092593
        imagebutton:
            idle "add_superglue_idle"
            hover "add_superglue_hover"

            action Jump("added_item_to_cyanosafe")

screen add_superglue_before_knife():
    zorder 50
    tag add_superglue_before_knife
    hbox:
        xpos 0.35052083 ypos 0.77592593
        imagebutton:
            idle "add_superglue_before_knife_idle"
            hover "add_superglue_before_knife_hover"

            action Jump("added_item_to_cyanosafe")

screen add_water_to_cyanosafe():
    zorder 50
    tag add_water_to_cyanosafe
    hbox:
        xpos 0.59322917 ypos 0.81
        imagebutton:
            idle "add_water_idle"
            hover "add_water_hover"

            action Jump("added_item_to_cyanosafe")

screen add_water_before_knife():
    zorder 50
    tag add_water_before_knife
    hbox:
        xpos 0.565 ypos 0.78
        imagebutton:
            idle "add_water_before_knife_idle"
            hover "add_water_before_knife_hover"

            action Jump("added_item_to_cyanosafe")

screen closing_cyanosafe_door():
    zorder 50
    hbox:
        xpos 0.8640625 ypos 0.0
        imagebutton:
            idle "close_cyanosafe_idle"
            hover "close_cyanosafe_hover"

            action Jump("ready_to_lift_print")

screen open_door_after_processing():
    zorder 50
    hbox:
        xpos 0.125 ypos 0.0
        imagebutton:
            idle "open_cyanosafe_close_idle"
            hover "open_cyanosafe_close_hover"

            action Jump("ready_to_collect_knife")

screen collect_lifted_knife():
    zorder 50
    hbox:
        xpos 0.434375 ypos 0.20833333
        imagebutton:
            idle "collect_knife_from_cyanosafe_idle"
            hover "collect_knife_from_cyanosafe_hover"

            action Jump("collected_knife")

screen incorrect_time_message():
    zorder 52
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "Hmm . . . that doesn't seem like the correct time. Think again."
            textbutton "Okay":
                action Return(True)

screen successfully_lifted_print_from_knife():
    zorder 52
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You lifted the print from the knife! It's a bit hard to \nsee though. I wonder if there's something we can do about that?"
            textbutton "I have an idea!":
                action Return(True)
            textbutton "I'm not sure.":
                action Jump("give_stain_hint")

screen stain_hint_message():
    zorder 52
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "I'm sure you could use a stain to make the print fluoresce under ALS."
            textbutton "Okay":
                action Return(True)

screen put_knife_in_fumehood():
    zorder 50
    hbox:
        xpos 0.35677083 ypos 0.15185185
        imagebutton:
            idle "place_knife_in_fumehood_idle"
            hover "place_knife_in_fumehood_hover"

            action Jump("knife_in_fumehood")

screen spray_knife():
    zorder 50
    hbox:
        xpos 0.4640625 ypos 0.34537037
        imagebutton:
            idle "spray_knife_idle"
            hover "spray_knife_hover"

            action Jump("stained_knife")

screen stained_knife():
    zorder 52
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You stained the knife! Let's collect the knife and then photograph the print using ALS."
            textbutton "Okay":
                action Return(True)

screen collect_stained_knife():
    zorder 50
    hbox:
        xpos 0.31614583 ypos 0.21851852
        imagebutton:
            idle "collect_knife_from_fumehood_idle"
            hover "collect_knife_from_fumehood_hover"

            action Jump("collect_knife_from_fumehood")

screen scalebar_hint():
    zorder 52
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "Remember to place a scalebar next to the fingerprint before taking photos."
            textbutton "Okay":
                action Return(True)

screen place_scalebar():
    zorder 50
    hbox:
        xpos 0.43697917 ypos 0.39351852
        imagebutton:
            idle "place_scalebar_by_print_idle"
            hover "place_scalebar_by_print_hover"

            action Jump("update_scale_variable")

screen wrong_light():
    zorder 52
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "Hmm . . . seems light you picked the wrong light. You should probably try again."
            textbutton "Okay":
                action Return(True)

screen already_using_light():
    zorder 52
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "You're already using a flashlight. Put that one away first."
            textbutton "Okay":
                action Return(True)

screen inspect_fingerprint():
    zorder 50
    hbox:
        xpos 0.43802083 ypos 0.31944444
        imagebutton:
            idle "inspect_print_idle"
            hover "inspect_print_hover"

            action Jump("update_inspecting_knife_variable") mouse ("inspect")

screen place_towel_on_lab_bench():
    hbox:
        xpos 0.30208333 ypos 0.09814815
        imagebutton:
            idle "towel_on_lab_bench_idle"
            hover "towel_on_lab_bench_hover"

            action Jump("towel_on_bench")

screen collect_towel_from_lab_bench():
    hbox:
        xpos 0.30208333 ypos 0.09814815
        imagebutton:
            idle "towel_on_lab_bench_idle"
            hover "towel_on_lab_bench_hover"

            action Jump("lab_bench")

screen place_knife_on_lab_bench():
    hbox:
        xpos 0.4265625 ypos 0.02592593
        imagebutton:
            idle "knife_on_lab_bench_idle"
            hover "knife_on_lab_bench_hover"

            action Jump("knife_on_bench")

screen collect_knife_from_lab_bench():
    hbox:
        xpos 0.4265625 ypos 0.02592593
        imagebutton:
            idle "knife_on_lab_bench_idle"
            hover "knife_on_lab_bench_hover"

            action Jump("lab_bench")

screen something_already_on_lab_bench():
    zorder 52
    frame:
        xpos 0.27 ypos 0.4
        vbox:
            text "There is already a piece of evidence on the bench."
            textbutton "Okay":
                action Return(True)

screen warn_player_about_knife():
    zorder 52
    tag warn_player_about_knife
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "Wait! You don't know if there is any DNA evidence \non the knife since blood was found on the crime scene. \nYou should probably check for that first."
            textbutton "Okay":
                action Return(True)


