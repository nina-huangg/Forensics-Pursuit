transform smaller_back_button():
    zoom 0.25

screen back_button():
    hbox:
        xpos 0.9 ypos 0.85
        imagebutton:
            idle "back_button" at smaller_back_button
            hover "back_button_hover"

            action Jump("back")

screen dont_need_light():
    zorder 52
    tag dont_need_light
    frame:
        xpos 0.35 ypos 0.2
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

            action NullAction()
            #action Jump("enter_data_analysis_lab")

    hbox:
        xpos 0.51 ypos 0.3
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"

            action Jump("enter_materials_lab")

transform smaller_machine():
    zoom 0.1

screen choose_machine():
    zorder 50
    hbox:
        xpos 0.25 ypos 0.05
        imagebutton:
            idle "lab_bench_button_idle"
            hover "lab_bench_button_hover"

            action Jump("lab_bench")
        
    hbox:
        xpos 0.55 ypos 0.05
        imagebutton:
            idle "instruments_button_idle1"
            hover "instruments_button_hover1"

            action NullAction()

    hbox:
        xpos 0.25 ypos 0.5
        imagebutton:
            idle "fumehood_idle" at smaller_machine
            hover "fumehood_hover"

            action Jump("fumehood")

    hbox:
        xpos 0.5 ypos 0.5
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
    zorder 50
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "Hmm . . . that doesn't seem like the correct time. Think again."
            textbutton "Okay":
                action Return(True)

screen successfully_lifted_print_from_knife():
    zorder 50
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You lifted the print from the knife! It's a bit hard to \nsee though. I wonder if there's something we can do about that?"
            textbutton "I have an idea!":
                action Return(True)
            textbutton "I'm not sure.":
                action Jump("give_stain_hint")

screen stain_hint_message():
    zorder 50
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
    zorder 50
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You stained the knife! Now time to use ALS."
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

screen place_scalebar():
    zorder 50
    hbox:
        xpos 0.52552083 ypos 0.55648148
        imagebutton:
            idle "place_scalebar_by_print_idle"
            hover "place_scalebar_by_print_hover"

            action Jump("update_scale_variable")

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
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "There is already a piece of evidence on the bench."
            textbutton "Okay":
                action Return(True)

screen correct_hemastix_result():
    frame:
        xpos 0.53 ypos 0.15
        vbox:
            text "The sample is positive for blood! Let's get \na picture of the hemastix next to the evidence \nand then we can collect a sample to analyze!"
            textbutton "Okay":
                action Return(True)

screen incorrect_hemastix():
    frame:
        xpos 0.53 ypos 0.15
        vbox:
            text "Hmm. . . something seemed to go wrong. Are you \nsure you did it right? You should \nprobably try again with a new hemastix."
            textbutton "Okay":
                action Return(True)

# Screen for hemastix procedure
screen use_hemastix():
    zorder 50
    tag use_hemastix
    
    # Button for throwing out the hemastix
    hbox:
        xpos 0.82 ypos 0.70555556
        imagebutton:
            idle "biohazard_bin_idle"
            hover "biohazard_bin_hover"

            action Jump("throw_out_hemastix")

    # Button for rubbing hemastix on object
    hbox:
        xpos current_evidence.hemastix_details['xpos_blood_spot'] ypos current_evidence.hemastix_details['ypos_blood_spot']
        imagebutton:
            insensitive current_evidence.hemastix_details['idle_image_blood_spot']
            idle current_evidence.hemastix_details['idle_image_blood_spot']
            hover current_evidence.hemastix_details['hover_image_blood_spot']


            if current_evidence.wet_hemastix:
                if current_evidence.name == "knife":
                    action [ToggleVariable("current_evidence.swabbed_object"), SetVariable("default_mouse", "positive_result"), 
                    SetVariable("current_evidence.finished_hemastix_test", True), SetVariable("determined_blood_on_knife", True), Jump("completed_hemastix_test")]
                elif current_evidence.name == "dish towel":
                    action [ToggleVariable("current_evidence.swabbed_object"), SetVariable("default_mouse", "positive_result"), 
                    SetVariable("current_evidence.finished_hemastix_test", True), SetVariable("determined_blood_on_towel", True), Jump("completed_hemastix_test")]
            else:
                action [ToggleVariable("current_evidence.swabbed_object"), SetVariable("default_mouse", "unused_hemastix"), Jump("incorrect_hemastix_test")]
            sensitive not current_evidence.swabbed_object and holding_hemastix

    # Button for placing hemastix back
    hbox:
        xpos 0.22604167 ypos 0.47222222
        imagebutton:
            insensitive "transparent"
            idle "hemastix_placeholder_idle"
            hover "hemastix_placeholder_hover"

            if current_evidence.swabbed_object and current_evidence.wet_hemastix:
                action [ToggleVariable("current_evidence.display_positive_result"), ToggleVariable("holding_hemastix"), SetVariable("default_mouse", "default")]
            else:
                action [ToggleVariable("current_evidence.display_unused_hemastix"), ToggleVariable("holding_hemastix"), SetVariable("default_mouse", "default")]

            sensitive not current_evidence.display_unused_hemastix and not current_evidence.display_negative_result and not current_evidence.display_positive_result

    # Button for displaying the unused hemastix
    hbox:
        xpos 0.2375 ypos 0.48796296
        imagebutton:
            insensitive "transparent"
            idle "blank_hemastix"
            hover "blank_hemastix"

            if not holding_distilled_water:
                action [ToggleVariable("current_evidence.display_unused_hemastix"), Jump("selected_hemastix")]
            else:
                action Jump("selected_hemastix")
            sensitive current_evidence.display_unused_hemastix

    # Button for displaying the negative result
    hbox:
        xpos 0.2375 ypos 0.48796296
        imagebutton:
            insensitive "transparent"
            idle "hemastix_negative_result"
            hover "hemastix_negative_result"

            action [ToggleVariable("current_evidence.display_negative_result"), Jump("selected_hemastix")]
            sensitive current_evidence.display_negative_result

    # Button for displaying the positive result
    hbox:
        xpos 0.2375 ypos 0.48796296
        imagebutton:
            insensitive "transparent"
            idle "hemastix_positive_result"
            hover "hemastix_positive_result"

            action [ToggleVariable("current_evidence.display_positive_result"), Jump("selected_hemastix")]
            sensitive current_evidence.display_positive_result

    # Button for putting positive hemastix next to object
    hbox:
        xpos current_evidence.hemastix_details['xpos_place_hemastix'] ypos current_evidence.hemastix_details['ypos_place_hemastix']
        imagebutton:
            insensitive "transparent"
            idle current_evidence.hemastix_details['idle_image_place_hemastix']
            hover current_evidence.hemastix_details['hover_image_place_hemastix']

            action Jump("finished_hemastix_test")
            sensitive current_evidence.swabbed_object and not current_evidence.display_positive_result and current_evidence.wet_hemastix and current_evidence.wet_before_swabbed

# Screen for the swabbing procedure
screen swabbing():
    zorder 50
    tag swabbing
    # Button for packing/collecting the tube
    hbox:
        xpos 0.92 ypos 0.68703704
        imagebutton:
            idle "tube_idle"
            hover "tube_hover"

            action Jump("collect_swab")

    # Button for throwing out the swab
    hbox:
        xpos 0.73 ypos 0.725
        imagebutton:
            idle "biohazard_bin_idle"
            hover "biohazard_bin_hover"

            action Jump("throw_out_swab")

    # Transparent button for swabbing the object
    hbox:
        xpos current_evidence.hemastix_details['xpos_blood_spot'] ypos current_evidence.hemastix_details['ypos_blood_spot']
        imagebutton:
            insensitive current_evidence.hemastix_details['idle_image_blood_spot']
            idle current_evidence.hemastix_details['idle_image_blood_spot']
            hover current_evidence.hemastix_details['hover_image_blood_spot']

            action ToggleVariable("current_evidence.swabbed_object_with_swab")
            sensitive not current_evidence.swabbed_object_with_swab and holding_swab

    # Button for placing swab back in place
    hbox:
        xpos 0.24 ypos 0.3
        imagebutton:
            insensitive "transparent"
            idle "swab_placeholder_idle"
            hover "swab_placeholder_hover"

            action [ToggleVariable("holding_swab"), ToggleVariable("current_evidence.display_swab"), SetVariable("default_mouse", "default")]
            sensitive not current_evidence.display_swab

    # Button displaying the clean swab
    hbox:
        xpos 0.22 ypos 0.325
        imagebutton:
            insensitive "transparent"
            idle "clean_swab"
            hover "clean_swab"

            if holding_distilled_water:
                action Jump("selected_swab")
            else:
                action [ToggleVariable("current_evidence.display_swab"), Jump("selected_swab")]
            sensitive current_evidence.display_swab

screen incorrect_swab_warning():
    zorder 52
    tag incorrect_swab_warning
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You are trying to package an incorrect sample. \nEither continue the swabbing process or dispose \nof the swab."
            textbutton "Okay":
                action Return (True)
            
screen already_collected_swab():
    zorder 52
    tag already_collected_swab
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You already collected a sample from here."
            textbutton "Okay":
                action Return(True)

screen already_tested_sample():
    zorder 52
    tag already_tested_sample
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You already used a hemastix on this sample."
            textbutton "Okay":
                action Return(True)

screen no_hemastix_test():
    zorder 52
    tag no_kastle_meyer_test
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You don't know what this substance is. \nAre you sure this is blood?"
            textbutton ". . . I guess not":
                action Return(True)

screen explain_more():
    zorder 52
    tag explain_more
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You can determine if this is blood by \nusing a hemestick"
            textbutton "Okay":
                action Return(True)

screen cannot_use_now():
    zorder 52
    tag cannot_use_now
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You are currently in the middle of swabbing. \nFinish swabbing first."
            textbutton "Okay":
                action Return(True)

screen already_using_hemastix():
    zorder 52
    tag already_using_hemastix
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You are currently using hemastix. \nFinish that first."
            textbutton "Okay":
                action Return(True)

screen swab_has_been_collected():
    zorder 52
    tag swab_has_been_collected
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "You collected a swab of the sample! Do you want to \nsend this off to start the extraction process?"
            textbutton "Yes.":
                if current_evidence.name == "dish towel":
                    action [ToggleVariable("sent_towel_sample_to_be_extracted"), Jump("collect_evidence_from_lab_bench")]
                elif current_evidence.name == "knife":
                    action [ToggleVariable("sent_knife_sample_to_be_extracted"), Jump("collect_evidence_from_lab_bench")]
            textbutton "Not yet.":
                action Jump("add_swab_to_inventory")

screen send_sample_for_extraction():
    zorder 52
    tag send_sample_for_extraction
    frame:
        xpos 0.2 ypos 0.15
        vbox:
            text "Do you want to send this off to start the extraction process?"
            textbutton "Yes.":
                if current_evidence.name == "dish towel":
                    action [ToggleVariable("sent_towel_sample_to_be_extracted"), Jump("sample_sent_for_extraction")]
                elif current_evidence.name == "knife":
                    action [ToggleVariable("sent_knife_sample_to_be_extracted"), Jump("sample_sent_for_extraction")]
            textbutton "Not yet.":
                action Jump("null_button")

screen currently_holding_swab():
    zorder 52
    tag currently_holding_swab
    frame:
        xpos 0.2 ypos 0.1
        vbox:
            text "You cannot use this now, you are holding a swab."
            textbutton "Okay":
                action Return(True)

screen swabbing_in_progress():
    zorder 52
    tag swabbing_in_progress
    frame:
        xpos 0.2 ypos 0.1
        vbox:
            text "You are in the middle of collecting a sample, you cannot use this right now."
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
