### This file contains the screens for the DNA process including the hemastix and swabbing procedure

# -------------------------------- Screens involving hemastix ----------------------------------------
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
            elif current_evidence.wet_hemastix:
                action [ToggleVariable("current_evidence.display_wet_hemastix"), ToggleVariable("holding_hemastix"), SetVariable("default_mouse", "default")]
            else:
                action [ToggleVariable("current_evidence.display_unused_hemastix"), ToggleVariable("holding_hemastix"), SetVariable("default_mouse", "default")]

            sensitive not current_evidence.display_unused_hemastix and not current_evidence.display_negative_result and not current_evidence.display_positive_result and not current_evidence.display_wet_hemastix

    # Button for displaying the unused hemastix
    hbox:
        xpos 0.2325 ypos 0.48196296
        imagebutton:
            insensitive "transparent"
            idle "hemastix_idle"
            hover "hemastix_hover"

            if not holding_distilled_water:
                action [ToggleVariable("current_evidence.display_unused_hemastix"), Jump("selected_hemastix")]
            else:
                action Jump("selected_hemastix")
            sensitive current_evidence.display_unused_hemastix and not current_evidence.wet_hemastix

    # Button for displaying a wet hemastix:
    hbox:
        xpos 0.2325 ypos 0.48196296
        imagebutton:
            insensitive "transparent"
            idle "wet_hemastix_idle"
            hover "wet_hemastix_hover"

            action [ToggleVariable("current_evidence.display_wet_hemastix"), Jump("selected_hemastix")]
            sensitive current_evidence.display_wet_hemastix
    

    # Button for displaying the negative result
    hbox:
        xpos 0.2325 ypos 0.48196296
        imagebutton:
            insensitive "transparent"
            idle "hemastix_negative_result"
            hover "hemastix_negative_result"

            action [ToggleVariable("current_evidence.display_negative_result"), Jump("selected_hemastix")]
            sensitive current_evidence.display_negative_result

    # Button for displaying the positive result
    hbox:
        xpos 0.2325 ypos 0.48196296
        imagebutton:
            insensitive "transparent"
            idle "hemastix_positive_result_idle"
            hover "hemastix_positive_result_hover"

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

screen correct_hemastix_result():
    zorder 52
    frame:
        xpos 0.22 ypos 0.1
        vbox:
            text "The sample is positive for blood! Let's get a picture of the hemastix \nnext to the evidence and then we can collect a sample to analyze!"
            textbutton "Okay":
                action Return(True)

screen incorrect_hemastix():
    zorder 52
    frame:
        xpos 0.25 ypos 0.37
        vbox:
            text "Hmm. . . something seemed to go wrong. Are you sure you did it right? \nYou should probably try again with a new hemastix."
            textbutton "Okay":
                action Return(True)

screen added_water_to_hemastix():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You put distilled water on the hemastix."
            timer 1.0 action Hide("added_water_to_hemastix", transition=Dissolve(1.0))

screen already_tested_sample():
    zorder 52
    tag already_tested_sample
    frame:
        xpos 0.3 ypos 0.4
        vbox:
            text "You already used a hemastix on this sample."
            textbutton "Okay":
                action Return(True)

screen no_hemastix_test():
    zorder 52
    tag no_hemastix_test
    frame:
        xpos 0.23 ypos 0.4
        vbox:
            text "You don't know what this substance is. Are you sure this is blood?"
            textbutton ". . . I guess not":
                action Return(True)

screen already_using_hemastix():
    zorder 52
    tag already_using_hemastix
    frame:
        xpos 0.27 ypos 0.4
        vbox:
            text "You are currently using a hemastix. Finish that first."
            textbutton "Okay":
                action Return(True)
# ----------------------------------------------------------------------------------------------------

# -------------------------------- Screens involving swabbing ----------------------------------------
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

            action [ToggleVariable("current_evidence.swabbed_object_with_swab"), Show("swabbed_evidence")]
            sensitive not current_evidence.swabbed_object_with_swab and holding_swab

    # Button for placing swab back in place
    hbox:
        xpos 0.24 ypos 0.3
        imagebutton:
            insensitive "transparent"
            idle "swab_placeholder_idle"
            hover "swab_placeholder_hover"

            if current_evidence.wet_swab:
                action [ToggleVariable("holding_swab"), ToggleVariable("current_evidence.display_wet_swab"), SetVariable("default_mouse", "default")]
            else:
                action [ToggleVariable("holding_swab"), ToggleVariable("current_evidence.display_swab"), SetVariable("default_mouse", "default")]
            sensitive not current_evidence.display_swab and not current_evidence.display_wet_swab

    # Button displaying the clean swab
    hbox:
        xpos 0.25 ypos 0.31575
        imagebutton:
            insensitive "transparent"
            idle "clean_swab_idle"
            hover "clean_swab_hover"

            if holding_distilled_water:
                action Jump("selected_swab")
            else:
                action [ToggleVariable("current_evidence.display_swab"), Jump("selected_swab")]
            sensitive current_evidence.display_swab and not current_evidence.display_wet_swab and not current_evidence.wet_swab

    # Button for displaying the wet swab
    hbox:
        xpos 0.25 ypos 0.31575
        imagebutton:
            insensitive "transparent"
            idle "wet_swab_idle"
            hover "wet_swab_hover"

            action [ToggleVariable("current_evidence.display_wet_swab"), Jump("selected_swab")]
            sensitive not current_evidence.display_swab and current_evidence.display_wet_swab

screen added_water_to_swab():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You put distilled water on the swab."
            timer 1.0 action Hide("added_water_to_swab", transition=Dissolve(1.0))

screen swabbed_evidence():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You swabbed the piece of evidence."
            timer 1.0 action Hide("swabbed_evidence", transition=Dissolve(1.0))

screen incorrect_swab_warning():
    zorder 52
    tag incorrect_swab_warning
    frame:
        xpos 0.3 ypos 0.4
        vbox:
            text "You are trying to package an incorrect sample. \nDispose of the swab and try again."
            textbutton "Okay":
                action Return (True)
            
screen already_collected_swab():
    zorder 52
    tag already_collected_swab
    frame:
        xpos 0.3 ypos 0.4
        vbox:
            text "You already collected a sample from here."
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

screen swab_has_been_collected():
    zorder 52
    tag swab_has_been_collected
    frame:
        xpos 0.27 ypos 0.1
        vbox:
            text "You collected a swab of the sample! Do you want to \nsend this off to start the extraction process?"
            textbutton "Yes.":
                if current_evidence.name == "dish towel":
                    action [ToggleVariable("sent_towel_sample_to_be_extracted"), Jump("collect_evidence_from_lab_bench")]
                elif current_evidence.name == "knife":
                    action [ToggleVariable("sent_knife_sample_to_be_extracted"), Jump("collect_evidence_from_lab_bench")]
            textbutton "Not yet.":
                action Jump("add_swab_to_inventory")
# ----------------------------------------------------------------------------------------------------

# -------------------------- Screen for choosing the DNA machine -------------------------------------
transform smaller_info():
    zoom 0.75

screen choose_dna_machine:
    zorder 50
    hbox:
        xpos 0.15833333 ypos 0.2537037
        imagebutton:
            idle "centrifuge_button_idle"
            hover "centrifuge_button_hover"

            action Jump("using_centrifuge")

    # info button for centrifuge
    hbox:
        xpos 0.185 ypos 0.185
        imagebutton:
            idle "info_button_idle" at smaller_info
            hover "info_button_hover"
            action Show("centrifuge_info")

    hbox:
        xpos 0.3 ypos 0.2537037
        imagebutton:
            idle "pcr_button_idle"
            hover "pcr_button_hover"

            action Jump("using_pcr")

    # info button for PCR
    hbox:
        xpos 0.335 ypos 0.185
        imagebutton:
            idle "info_button_idle" at smaller_info
            hover "info_button_hover"
            action Show("pcr_info")

    hbox:
        xpos 0.45 ypos 0.2537037
        imagebutton:
            idle "thermal_cycler_button_idle"
            hover "thermal_cycler_button_hover"

            action Jump("using_thermal_cycler")

    # info button for Thermal Cycler
    hbox:
        xpos 0.485 ypos 0.185
        imagebutton:
            idle "info_button_idle" at smaller_info
            hover "info_button_hover"
            action Show("thermal_cycler_info")

    hbox:
        xpos 0.6 ypos 0.2537037
        imagebutton:
            idle "plate_centrifuge_button_idle"
            hover "plate_centrifuge_button_hover"

            action Jump("using_plate_centrifuge")

    # info button for plate centrifuge
    hbox:
        xpos 0.63 ypos 0.185
        imagebutton:
            idle "info_button_idle" at smaller_info
            hover "info_button_hover"
            action Show("plate_centrifuge_info")

    hbox:
        xpos 0.75 ypos 0.2537037
        imagebutton:
            idle "miseq_button_idle"
            hover "miseq_button_hover"

            action Jump("using_miseq")

    # info button for miseq
    hbox:
        xpos 0.78 ypos 0.185
        imagebutton:
            idle "info_button_idle" at smaller_info
            hover "info_button_hover"

            action Show("miseq_machine_info")

screen centrifuge_info():
    zorder 53
    frame:
        xpos 0.2 ypos 0.4
        vbox:
            text "Used in the extraction stage of DNA analysis. \nSeparates mixtures into their various components based on density."
            textbutton "Okay":
                action Hide("centrifuge_info")

screen pcr_info():
    zorder 53
    frame:
        xpos 0.3 ypos 0.4
        vbox:
            text "Used in the quantification stage of DNA analysis. \nProvides the concentration data for the DNA."
            textbutton "Okay":
                action Hide ("pcr_info")

screen thermal_cycler_info():
    zorder 53
    frame:
        xpos 0.16 ypos 0.4
        vbox:
            text "Used in the amplification and detection stages of DNA analysis. \nAmplifies DNA sequences into more copies by using a polymerase chain reaction."
            textbutton "Okay":
                action Hide("thermal_cycler_info")

screen plate_centrifuge_info():
    zorder 53
    frame:
        xpos 0.21 ypos 0.4
        vbox:
            text "Used in the detection stage of DNA analysis. \nSeparates mixtures into their various components based on density."
            textbutton "Okay":
                action Hide("plate_centrifuge_info")

screen miseq_machine_info():
    zorder 53
    frame:
        xpos 0.19 ypos 0.4
        vbox:
            text "Used in the detection stage of DNA analysis. \nPerforms capillary electrophoresis  and data analysis of said sequencing."
            textbutton "Okay":
                action Hide("miseq_machine_info")
# ---------------------------------------------------------------------------------------------------------

# ----------------------- Screens for using the DNA machines and/or using a plate ------------------------
screen centrifuge_screen():
    zorder 50
    tag centrifuge_screen
    # button for opening centrifuge
    hbox:
        xpos 0.39739583 ypos 0.30925926
        imagebutton:
            insensitive "transparent"
            idle "open_centrifuge_idle"
            hover "open_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.centrifuge_open"), Jump("update_centrifuge_image")]
            sensitive not current_dna_evidence.centrifuge_open

    # button for placing dna tube in centrifuge
    hbox:
        xpos 0.47760417 ypos 0.28888889
        imagebutton:
            insensitive "transparent"
            idle "put_tube_in_centrifuge_idle"
            hover "put_tube_in_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.in_centrifuge"), Jump("update_centrifuge_image")]
            sensitive current_dna_evidence.centrifuge_open and not current_dna_evidence.in_centrifuge and current_dna_evidence.holding_incubated_sample

    # button for placing counterweight in centrifuge
    hbox:
        xpos 0.484375 ypos 0.55462963
        imagebutton:
            insensitive "transparent"
            idle "put_counterweight_in_centrifuge_idle"
            hover "put_counterweight_in_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.counterweight_in"), ToggleVariable("current_dna_evidence.holding_tube"), SetVariable("default_mouse", "default"), Jump("update_centrifuge_image")]
            sensitive current_dna_evidence.centrifuge_open and current_dna_evidence.in_centrifuge and not current_dna_evidence.counterweight_in and current_dna_evidence.holding_tube

    # button for closing centrifuge door
    hbox:
        xpos 0.33125 ypos 0.0
        imagebutton:
            insensitive "transparent"
            idle "close_centrifuge_idle"
            hover "close_centrifuge_hover"

            if current_dna_evidence.in_centrifuge and not current_dna_evidence.counterweight_in:
                action Jump("need_to_add_counterweight")
            elif current_dna_evidence.finished_centrifuge and current_dna_evidence.in_centrifuge and current_dna_evidence.counterweight_in:
                action Jump("already_used_machine")
            else:
                action [ToggleVariable("current_dna_evidence.centrifuge_open"), Jump("update_centrifuge_image")]
            sensitive current_dna_evidence.centrifuge_open and not current_dna_evidence.holding_tube and not current_dna_evidence.holding_incubated_sample

    # button for removing DNA tube from centrifuge
    hbox:
        xpos 0.47760417 ypos 0.28888889
        imagebutton:
            insensitive "transparent"
            idle "put_tube_in_centrifuge_idle"
            hover "put_tube_in_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.in_centrifuge"), Jump("done_with_centrifuge")]
            sensitive current_dna_evidence.centrifuge_open and current_dna_evidence.in_centrifuge and current_dna_evidence.finished_centrifuge

    # button for getting the balance tube
    hbox:
        xpos 0.2 ypos 0.1
        imagebutton:
            insensitive "transparent"
            idle "balance_tube_idle"
            hover "balance_tube_hover"

            action Jump("holding_balance_tube")
            sensitive not current_dna_evidence.counterweight_in and not current_dna_evidence.holding_tube and current_dna_evidence.centrifuge_open and current_dna_evidence.in_centrifuge

screen fill_pcr_plate():
    # button to examine plate
    hbox:
        xpos 0.24427083 ypos 0.225
        imagebutton:
            insensitive "transparent"
            idle "examine_pcr_plate_idle"
            hover "examine_pcr_plate_hover"

            action [ToggleVariable("current_dna_evidence.viewing_tray"), Jump("update_pcr_plate_scene")]
            sensitive not current_dna_evidence.viewing_tray

    # button to put DNA sample in well
    hbox:
        xpos 0.22708333 ypos 0.13518519
        imagebutton:
            insensitive "transparent"
            idle "fill_first_well_idle"
            hover "fill_first_well_hover"

            action [ToggleVariable("current_dna_evidence.dna_sample_in"), ToggleVariable("current_dna_evidence.holding_extracted_dna"), Show("added_2uL_sample"),Jump("update_pcr_plate_scene")]
            sensitive not current_dna_evidence.dna_sample_in and current_dna_evidence.holding_extracted_dna and current_dna_evidence.holding_pipette

    # button to put negative solution in well
    hbox:
        xpos 0.23072917 ypos 0.2287037
        imagebutton:
            insensitive "transparent"
            idle "fill_second_well_idle"
            hover "fill_second_well_hover"

            action [ToggleVariable("current_dna_evidence.negative_solution_in"), ToggleVariable("current_dna_evidence.holding_pipette"), ToggleVariable("current_dna_evidence.holding_distilled_water"), Show("added_2uL_water"),Jump("update_pcr_plate_scene")]
            sensitive current_dna_evidence.dna_sample_in and not current_dna_evidence.negative_solution_in and current_dna_evidence.holding_pipette and current_dna_evidence.holding_distilled_water
    
    # button to pick up pcr plate
    hbox:
        xpos 0.1671875 ypos 0.06296296
        imagebutton:
            insensitive "transparent"
            idle "pick_up_pcr_plate_idle"
            hover "pick_up_pcr_plate_hover"

            action [ToggleVariable("current_dna_evidence.viewing_tray"), Jump("moving_to_pcr")]
            sensitive current_dna_evidence.dna_sample_in and current_dna_evidence.negative_solution_in and current_dna_evidence.all_pcr_wells_filled
    
    # button to use pipette
    hbox:
        xpos 0.86 ypos 0.15740741
        imagebutton:
            insensitive "transparent"
            idle "pipette_button_idle"
            hover "pipette_button_hover"

            action Jump("selected_pipette")
            sensitive not current_dna_evidence.holding_pipette and not current_dna_evidence.negative_solution_in and current_dna_evidence.viewing_tray

    # button to put pipette back
    hbox:
        xpos 0.848 ypos 0.13518519
        imagebutton:
            insensitive "transparent"
            idle "pipette_placeholder_idle"
            hover "pipette_placeholder_hover"

            action Jump("selected_pipette")
            sensitive current_dna_evidence.holding_pipette and not current_dna_evidence.negative_solution_in and current_dna_evidence.viewing_tray

screen pcr_screen():
    # button to open PCR
    hbox:
        xpos 0.3328125 ypos 0.60833333
        imagebutton:
            insensitive "transparent"
            idle "use_pcr_idle"
            hover "use_pcr_hover"

            if current_dna_evidence.finished_pcr:
                action Jump("already_used_machine")
            else:
                action [ToggleVariable("current_dna_evidence.pcr_open"), Jump("using_pcr")]
            sensitive not current_dna_evidence.pcr_open

    # button to place plate in PCR
    hbox:
        xpos 0.29947917 ypos 0.25
        imagebutton:
            insensitive "transparent"
            idle "put_tray_in_pcr_idle"
            hover "put_tray_in_pcr_hover"

            action [ToggleVariable("current_dna_evidence.tray_in_pcr"), Jump("using_pcr")]
            sensitive current_dna_evidence.pcr_open and not current_dna_evidence.tray_in_pcr and current_dna_evidence.holding_tray

    # button to close PCR
    hbox:
        xpos 0.0 ypos 0.19351852
        imagebutton:
            insensitive "transparent"
            idle "close_pcr_idle"
            hover "close_pcr_hover"

            if current_dna_evidence.tray_in_pcr and current_dna_evidence.finished_pcr:
                action Jump("already_used_machine")
            else:
                action [ToggleVariable("current_dna_evidence.pcr_open"), Jump("using_pcr")]
            sensitive current_dna_evidence.pcr_open and not current_dna_evidence.holding_tray

screen fill_amplification_plate():
    # button to examine plate
    hbox:
        xpos 0.24427083 ypos 0.225
        imagebutton:
            insensitive "transparent"
            idle "examine_pcr_plate_idle"
            hover "examine_pcr_plate_hover"

            action [ToggleVariable("current_dna_evidence.viewing_amp_plate"), Jump("update_amp_plate_scene")]
            sensitive not current_dna_evidence.viewing_amp_plate

    # button to fill first well
    hbox:
        xpos 0.22708333 ypos 0.13518519
        imagebutton:
            insensitive "transparent"
            idle "fill_first_well_idle"
            hover "fill_first_well_hover"

            if current_dna_evidence.holding_positive_control:
                action [ToggleVariable("current_dna_evidence.holding_positive_control"), ToggleVariable("current_dna_evidence.added_positive_control"), Show("added_positive_control"), Jump("update_amp_plate_scene")]
            elif current_dna_evidence.holding_distilled_water:
                action [ToggleVariable("current_dna_evidence.holding_distilled_water"), ToggleVariable("current_dna_evidence.added_negative_control"), Show("added_negative_control"), Jump("update_amp_plate_scene")]

            sensitive current_dna_evidence.holding_pipette and ((current_dna_evidence.holding_positive_control and not current_dna_evidence.added_positive_control) or (current_dna_evidence.holding_distilled_water and not current_dna_evidence.added_negative_control)) and (not current_dna_evidence.added_negative_control and not current_dna_evidence.added_positive_control)

    # button to fill second well
    hbox:
        xpos 0.23072917 ypos 0.2287037
        imagebutton:
            insensitive "transparent"
            idle "fill_second_well_idle"
            hover "fill_second_well_hover"

            if current_dna_evidence.holding_positive_control:
                action [ToggleVariable("current_dna_evidence.holding_positive_control"), ToggleVariable("current_dna_evidence.added_positive_control"), Show("added_positive_control"), Jump("update_amp_plate_scene")]
            elif current_dna_evidence.holding_distilled_water:
                action [ToggleVariable("current_dna_evidence.holding_distilled_water"), ToggleVariable("current_dna_evidence.added_negative_control"), Show("added_negative_control"), Jump("update_amp_plate_scene")]

            sensitive current_dna_evidence.holding_pipette and ((current_dna_evidence.holding_positive_control and not current_dna_evidence.added_positive_control and current_dna_evidence.added_negative_control) or (current_dna_evidence.holding_distilled_water and not current_dna_evidence.added_negative_control and current_dna_evidence.added_positive_control))

    # button to fill third well
    hbox:
        xpos 0.23177083 ypos 0.30925926
        imagebutton:
            insensitive "transparent"
            idle "fill_third_well_idle"
            hover "fill_third_well_hover"

            action [ToggleVariable("current_dna_evidence.added_sample_to_amp_plate"), ToggleVariable("current_dna_evidence.holding_sample"), ToggleVariable("current_dna_evidence.holding_pipette"), Show("added_dna_sample"), Jump("update_amp_plate_scene")]
            sensitive current_dna_evidence.holding_pipette and current_dna_evidence.holding_sample and current_dna_evidence.added_positive_control and current_dna_evidence.added_negative_control and not current_dna_evidence.added_sample_to_amp_plate

    # button to pick up pcr plate
    hbox:
        xpos 0.1671875 ypos 0.06296296
        imagebutton:
            insensitive "transparent"
            idle "pick_up_pcr_plate_idle"
            hover "pick_up_pcr_plate_hover"

            action [ToggleVariable("current_dna_evidence.viewing_tray"), Jump("moving_to_thermal_cycler")]
            sensitive current_dna_evidence.added_sample_to_amp_plate and current_dna_evidence.added_negative_control and current_dna_evidence.added_positive_control and current_dna_evidence.all_plate_wells_filled

    # button to use pipette
    hbox:
        xpos 0.86 ypos 0.15740741
        imagebutton:
            insensitive "transparent"
            idle "pipette_button_idle"
            hover "pipette_button_hover"

            action Jump("selected_pipette")
            sensitive not current_dna_evidence.holding_pipette and not current_dna_evidence.added_sample_to_amp_plate and current_dna_evidence.viewing_amp_plate

    # button to put pipette back
    hbox:
        xpos 0.848 ypos 0.13518519
        imagebutton:
            insensitive "transparent"
            idle "pipette_placeholder_idle"
            hover "pipette_placeholder_hover"

            action Jump("selected_pipette")
            sensitive current_dna_evidence.holding_pipette and not current_dna_evidence.added_sample_to_amp_plate and current_dna_evidence.viewing_amp_plate

screen thermal_cycler_screen():
    # button to open thermal cycler
    hbox:
        xpos 0.14947917 ypos 0.03148148
        imagebutton:
            insensitive "transparent"
            idle "open_thermal_cycler_idle"
            hover "open_thermal_cycler_hover"

            action [ToggleVariable("current_dna_evidence.thermal_cycler_open"), Jump("using_thermal_cycler")]
            sensitive not current_dna_evidence.thermal_cycler_open and (current_dna_evidence.plate_in_thermal_cycler or not current_dna_evidence.finished_amplification or (current_dna_evidence.finished_detection_centrifuge and not current_dna_evidence.finished_detection_thermal_cycler))

    # button to place plate in thermal cycler
    hbox:
        xpos 0.475 ypos 0.4287037
        imagebutton:
            insensitive "transparent"
            idle "put_tray_in_thermal_cycler_idle"
            hover "put_tray_in_thermal_cycler_hover"

            action [ToggleVariable("current_dna_evidence.plate_in_thermal_cycler"), ToggleVariable("current_dna_evidence.holding_tray"), Jump("using_thermal_cycler")]
            sensitive current_dna_evidence.thermal_cycler_open and not current_dna_evidence.plate_in_thermal_cycler and current_dna_evidence.holding_tray

    # button to close thermal cycler
    hbox:
        xpos 0.4234375 ypos 0.01759259
        imagebutton:
            insensitive "transparent"
            idle "close_thermal_cycler_idle"
            hover "close_thermal_cycler_hover"

            if current_dna_evidence.plate_in_thermal_cycler and current_dna_evidence.finished_amplification and (not current_dna_evidence.finished_detection_centrifuge or current_dna_evidence.finished_detection_thermal_cycler):
                action Jump("already_used_machine")
            else:
                action [ToggleVariable("current_dna_evidence.thermal_cycler_open"), Jump("using_thermal_cycler")]
            sensitive current_dna_evidence.thermal_cycler_open and not current_dna_evidence.holding_tray

    # button to collect plate from thermal cycler
    hbox:
        xpos 0.475 ypos 0.4287037
        imagebutton:
            insensitive "transparent"
            idle "put_tray_in_thermal_cycler_idle"
            hover "put_tray_in_thermal_cycler_hover"

            action [ToggleVariable("current_dna_evidence.plate_in_thermal_cycler"), Jump("collected_plate_from_thermal_cycler")]
            sensitive current_dna_evidence.thermal_cycler_open and current_dna_evidence.plate_in_thermal_cycler and not current_dna_evidence.holding_tray

screen fill_detection_plate():
    # button to examine plate
    hbox:
        xpos 0.24427083 ypos 0.225
        imagebutton:
            insensitive "transparent"
            idle "examine_pcr_plate_idle"
            hover "examine_pcr_plate_hover"

            action [ToggleVariable("current_dna_evidence.viewing_detection_plate"), Jump("update_detection_plate_scene")]
            sensitive not current_dna_evidence.viewing_detection_plate

    # button to fill first well
    hbox:
        xpos 0.22708333 ypos 0.13518519
        imagebutton:
            insensitive "transparent"
            idle "fill_first_well_idle"
            hover "fill_first_well_hover"

            action [ToggleVariable("current_dna_evidence.holding_sample"), ToggleVariable("current_dna_evidence.added_sample_to_det_plate"), ToggleVariable("current_dna_evidence.holding_pipette"), Show("added_1uL_sample"), Jump("update_detection_plate_scene")]

            sensitive current_dna_evidence.holding_pipette and current_dna_evidence.holding_sample and not current_dna_evidence.added_sample_to_det_plate and current_dna_evidence.viewing_detection_plate

    # button to pick up detection plate
    hbox:
        xpos 0.1671875 ypos 0.06296296
        imagebutton:
            insensitive "transparent"
            idle "pick_up_pcr_plate_idle"
            hover "pick_up_pcr_plate_hover"

            action [ToggleVariable("current_dna_evidence.viewing_detection_plate"), Jump("moving_to_plate_centrifuge")]
            sensitive current_dna_evidence.added_sample_to_det_plate

    # button to use pipette
    hbox:
        xpos 0.86 ypos 0.15740741
        imagebutton:
            insensitive "transparent"
            idle "pipette_button_idle"
            hover "pipette_button_hover"

            action Jump("selected_pipette")
            sensitive not current_dna_evidence.holding_pipette and not current_dna_evidence.added_sample_to_det_plate and current_dna_evidence.viewing_detection_plate

    # button to put pipette back
    hbox:
        xpos 0.848 ypos 0.13518519
        imagebutton:
            insensitive "transparent"
            idle "pipette_placeholder_idle"
            hover "pipette_placeholder_hover"

            action Jump("selected_pipette")
            sensitive current_dna_evidence.holding_pipette and not current_dna_evidence.added_sample_to_det_plate and current_dna_evidence.viewing_detection_plate

screen using_plate_centrifuge():
    # button for opening plate centrifuge
    hbox:
        xpos 0.27552083 ypos 0.15648148
        imagebutton:
            insensitive "transparent"
            idle "open_plate_centrifuge_idle"
            hover "open_plate_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.plate_centrifuge_open"), Jump("update_plate_centrifuge_scene")]
            sensitive not current_dna_evidence.plate_centrifuge_open and not (not current_dna_evidence.plate_in_centrifuge and current_dna_evidence.finished_detection_centrifuge)

    # button for placing plate in plate centrifuge
    hbox:
        xpos 0.55989583 ypos 0.5287037
        imagebutton:
            insensitive "transparent"
            idle "put_plate_in_centrifuge_idle"
            hover "put_plate_in_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.plate_in_centrifuge"), Jump("update_plate_centrifuge_scene")]
            sensitive current_dna_evidence.plate_centrifuge_open and current_dna_evidence.holding_tray and not current_dna_evidence.plate_in_centrifuge

    # button for closing plate centrifuge
    hbox:
        xpos 0.34270833 ypos 0.00648148
        imagebutton:
            insensitive "transparent"
            idle "close_plate_centrifuge_idle"
            hover "close_plate_centrifuge_hover"

            if current_dna_evidence.plate_in_centrifuge and current_dna_evidence.finished_detection_centrifuge:
                action Jump("already_used_machine")
            else:
                action [ToggleVariable("current_dna_evidence.plate_centrifuge_open"), Jump("update_plate_centrifuge_scene")]
            sensitive current_dna_evidence.plate_centrifuge_open and not current_dna_evidence.holding_tray

    # button for taking plate out of plate centrifuge
    hbox:
        xpos 0.55989583 ypos 0.5287037
        imagebutton:
            insensitive "transparent"
            idle "put_plate_in_centrifuge_idle"
            hover "put_plate_in_centrifuge_hover"

            action [ToggleVariable("current_dna_evidence.plate_in_centrifuge"), Jump("collected_plate_from_plate_centrifuge")]
            sensitive current_dna_evidence.plate_centrifuge_open and current_dna_evidence.plate_in_centrifuge and not current_dna_evidence.holding_tray

screen put_plate_on_ice():
    # button to place plate on ice
    hbox:
        xpos 0.18072917 ypos 0.14722222
        imagebutton:
            insensitive "transparent"
            idle "place_on_ice_idle"
            hover "place_on_ice_hover"

            action [ToggleVariable("current_dna_evidence.plate_on_ice"), Jump("plate_is_on_ice")]
            sensitive current_dna_evidence.holding_tray

screen using_miseq():
    zorder 50
    # button for opening first door
    hbox:
        xpos 0.32239583 ypos 0.5537037
        imagebutton:
            insensitive "transparent"
            idle "open_miseq_idle"
            hover "open_miseq_hover"

            action [ToggleVariable("current_dna_evidence.miseq_first_open"), Jump("update_miseq_scene")]
            sensitive not current_dna_evidence.miseq_first_open and not current_dna_evidence.plate_in_miseq

    # button for opening second door
    hbox:
        xpos 0.31666667 ypos 0.29074074
        imagebutton:
            insensitive "transparent"
            idle "open_again_idle"
            hover "open_again_hover"

            action [ToggleVariable("current_dna_evidence.miseq_second_open"), Jump("update_miseq_scene")]
            sensitive not current_dna_evidence.miseq_second_open and current_dna_evidence.miseq_first_open and not current_dna_evidence.plate_in_miseq

    # button for putting plate in
    hbox:
        xpos 0.2796875 ypos 0.15925926
        imagebutton:
            insensitive "transparent"
            idle "put_plate_in_miseq_idle"
            hover "put_plate_in_miseq_hover"

            action [ToggleVariable("current_dna_evidence.plate_in_miseq"), Jump("update_miseq_scene")]
            sensitive current_dna_evidence.miseq_second_open and not current_dna_evidence.plate_in_miseq and current_dna_evidence.holding_tray

    # button for closing second door
    hbox:
        xpos 0.1046875 ypos 0.0
        imagebutton:
            insensitive "transparent"
            idle "close_second_door_idle"
            hover "close_second_door_hover"

            action [ToggleVariable("current_dna_evidence.miseq_second_open"), Jump("update_miseq_scene")]
            sensitive current_dna_evidence.miseq_second_open and not current_dna_evidence.holding_tray

    # button for closing first door
    hbox:
        xpos 0.09166667 ypos 0.0
        imagebutton:
            insensitive "transparent"
            idle "close_first_miseq_door_idle"
            hover "close_first_miseq_door_hover"

            action [ToggleVariable("current_dna_evidence.miseq_first_open"), Jump("update_miseq_scene")]
            sensitive current_dna_evidence.miseq_first_open and not current_dna_evidence.miseq_second_open and not current_dna_evidence.holding_tray

# --------------------------------------------------------------------------------------------------------

# -------------------------- Screens with messages regarding the DNA process -----------------------------
screen received_dna():
    zorder 52
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "You received the sample from the incubator! Now it's time to put the sample in the centrifuge."
            textbutton "Great!":
                action Return(True)

screen add_balance():
    zorder 52
    frame:
        xpos 0.15 ypos 0.4
        vbox:
            text "You need to add a tube to balance the weight in the centrifuge before you can use it."
            textbutton "Okay":
                action Return(True)

screen already_ran_machine():
    zorder 52
    frame:
        xpos 0.15 ypos 0.4
        vbox:
            text "You've already used this machine on the sample. You need to remove the sample."
            textbutton "Okay":
                action Return(True)

screen already_using_centrifuge():
    zorder 52
    frame:
        xpos 0.18 ypos 0.4
        vbox:
            text "You are already analysing a sample. You can't run samples from the same crime \nscene in the same cycle to avoid intercontamination."
            textbutton "Okay":
                action Return(True)

screen finished_with_centrifuge():
    zorder 52
    frame:
        xpos 0.2 ypos 0.05
        vbox:
            text "You've extracted the DNA! Time to start the quantification process."
            textbutton "Okay":
                action Return(True)

screen added_2uL_sample():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You added 2µL of the DNA sample"
            timer 1.0 action Hide("added_2uL_sample", transition=Dissolve(1.0))

screen added_2uL_water():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You added 2µL of distilled water."
            timer 1.0 action Hide("added_2uL_water", transition=Dissolve(1.0))

screen add_negative_control():
    zorder 52
    frame:
        xpos 0.25 ypos 0.1
        vbox:
            text "It's now time to add the negative control which is distilled water."
            textbutton "Okay":
                action Return(True)

screen give_pcr_plate_info():
    zorder 52
    frame:
        xpos 0.2 ypos 0.05
        vbox:
            text "This is the plate for the PCR. Mastermix has already been added to all of the \nwells. We now need to add the DNA sample."
            textbutton "Okay":
                action Return(True)

screen fill_rest_with_water():
    zorder 52
    frame:
        xpos 0.25 ypos 0.1
        vbox:
            text "It's now time to fill the rest of the wells with distilled water."
            textbutton "Okay":
                action Return(True)

screen need_to_add_sample_first():
    zorder 52
    frame:
        xpos 0.3 ypos 0.4
        vbox:
            text "You need to put the DNA sample in a well first."
            textbutton "Okay":
                action Return(True)

screen dna_already_added():
    zorder 52
    frame:
        xpos 0.35 ypos 0.4
        vbox:
            text "You already added the DNA sample."
            textbutton "Okay":
                action Return(True)

screen wrong_amount():
    zorder 52
    frame:
        xpos 0.25 ypos 0.4
        vbox:
            text "Hmm . . . that doesn't seem like the correct amount. Try again."
            textbutton "Okay":
                action Return(True)

screen correct_amount():
    zorder 52
    frame:
        xpos 0.3 ypos 0.05
        vbox:
            text "That's the correct amount! Let's put it in the well."
            textbutton "Okay":
                action Return(True)

screen move_to_pcr():
    zorder 52
    frame:
        xpos 0.32 ypos 0.05
        vbox:
            text "It's now time to put the plate into the PCR."
            textbutton "Okay":
                action Return(True)

screen wrong_decision():
    zorder 52
    frame:
        xpos 0.25 ypos 0.4
        vbox:
            text "Take a look at the concentration value provided and try again."
            textbutton "Okay":
                action Jump("quantification_calculation")

screen wrong_calculation:
    zorder 52
    frame:
        xpos 0.15 ypos 0.4
        vbox:
            text "Hmm . . . that's not the correct volume, are you sure you did the calculation correct?"
            textbutton "Yes":
                action Return(True)
            textbutton "I'm not sure":
                action Jump("give_formula")

screen provide_formula():
    zorder 52
    frame:
        xpos 0.29 ypos 0.4
        vbox:
            text "The calculation uses the formula C1 * V1 = C2 * V2."
            textbutton "Okay":
                action Return(True)

screen correct_calculation():
    zorder 52
    frame:
        xpos 0.25 ypos 0.05
        vbox:
            text "That's correct! Now it's time to start the amplification process"
            textbutton "Okay":
                action Return(True)

screen give_amplification_plate_info():
    zorder 52
    frame:
        xpos 0.17 ypos 0.05
        vbox:
            text "The reagents from the STR kit have already been added to all of the wells. \nWe now need to add the positive and negative controls and our DNA sample."
            textbutton "Okay":
                action Return(True)

screen added_positive_control():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You added [current_dna_evidence.required_volume]µL of GF positive control."
            timer 1.0 action Hide("added_positive_control", transition=Dissolve(1.0))

screen added_negative_control():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You added [current_dna_evidence.required_volume]µL of distilled water."
            timer 1.0 action Hide("added_negative_control", transition=Dissolve(1.0))

screen added_dna_sample():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You added [current_dna_evidence.required_volume]µL of the DNA sample."
            timer 1.0 action Hide("added_dna_sample", transition=Dissolve(1.0))

screen add_dna_sample():
    zorder 52
    frame:
        xpos 0.35 ypos 0.1
        vbox:
            text "It's now time to add the DNA."
            textbutton "Okay":
                action Return(True)

screen move_to_thermal_cycler():
    zorder 52
    frame:
        xpos 0.27 ypos 0.05
        vbox:
            text "The plate is now ready to go into the thermal cycler!"
            textbutton "Okay":
                action Return(True)

screen previously_added_negative_control():
    zorder 52
    frame:
        xpos 0.35 ypos 0.4
        vbox:
            text "You already added the negative control."
            textbutton "Okay":
                action Return(True)

screen previously_added_positive_control():
    zorder 52
    frame:
        xpos 0.35 ypos 0.4
        vbox:
            text "You already added the positive control."
            textbutton "Okay":
                action Return(True)

screen finished_amplification():
    zorder 52
    frame:
        xpos 0.2 ypos 0.05
        vbox:
            text "You finished the amplification process! Let's collect the plate and \nstart the detection process."
            textbutton "Okay":
                action Return(True)

screen give_detection_plate_info():
    zorder 52
    frame:
        xpos 0.22 ypos 0.05
        vbox:
            text "All the wells have already been filled with 10µL of standard solution. \nNow we need to add 1µL of the DNA sample to a well."
            textbutton "Okay":
                action Return(True)

screen added_1uL_sample():
    zorder 52
    frame:
        xpos 0.165 ypos 0.03
        vbox:
            text "You added 1µL of the sample."
            timer 1.0 action Hide("added_1uL_sample", transition=Dissolve(1.0))

screen dont_need_to_use():
    zorder 52
    frame:
        xpos 0.3 ypos 0.4
        vbox:
            text "We don't need to use this machine right now."
            textbutton "Okay":
                action Return(True)

screen finished_detection_plate():
    zorder 52
    frame:
        xpos 0.2 ypos 0.1
        vbox:
            text "The plate is finished! Now it's time to put the plate in the plate centrifuge."
            textbutton "Okay":
                action Return(True)

screen dont_use_sample():
    zorder 52
    frame:
        xpos 0.15 ypos 0.4
        vbox:
            text "This sample is now being saved, you need to use the sample from the amplification plate."
            textbutton "Okay":
                action Return(True)

screen finished_with_plate_centrifuge():
    frame:
        xpos 0.15 ypos 0.05
        vbox:
            text "The plate centrifuge is done. Let's collect the plate and put it in the thermal cycler."
            textbutton "Okay":
                action Return(True)

screen put_on_ice():
    zorder 52
    frame:
        xpos 0.25 ypos 0.05
        vbox:
            text "We're done with the thermal cycler. Let's put the plate on \nice to cool down back to room temperature."
            textbutton "Okay":
                action Return(True)

screen move_to_miseq_machine():
    zorder 52
    frame:
        xpos 0.23 ypos 0.05
        vbox:
            text "We're done with the thermal cycler. Let's move to the MiSeq machine to \nstart capillary electrophoresis."
            textbutton "Okay":
                action Return(True)

screen miseq_info():
    zorder 52
    frame:
        xpos 0.2 ypos 0.05
        vbox:
            text "The reagents and buffer have already been loaded into the machine. \nAll that's left to do is put the plate in."
            textbutton "Okay":
                action Return(True)

screen finished_detection():
    zorder 52
    frame:
        xpos 0.2 ypos 0.05
        vbox:
            text "You've finished the detection stage! An electropherogram has been made \nfor this sample. Finish analysing all other samples before comparing their \ngenetic profiles."
            textbutton "Okay":
                action Return(True)

screen cant_continue_with_sample():
    zorder 52
    frame:
        xpos 0.2 ypos 0.4
        vbox:
            text "The concentration of this sample is below the standard concentration \nrequired. A genetic profile cannot be made from this."
            textbutton "Okay":
                action Return(True)

screen already_analyzed():
    frame:
        xpos 0.33 ypos 0.4
        vbox:
            text "You already analyzed this sample."
            textbutton "Okay.":
                action Return(True)

screen send_sample_for_extraction():
    zorder 52
    tag send_sample_for_extraction
    frame:
        xpos 0.25 ypos 0.1
        vbox:
            text "Do you want to send this off to start the extraction process?"
            textbutton "Yes.":
                action [Jump("sample_sent_for_extraction")]
            textbutton "Not yet.":
                action [SetVariable("swab_sample_being_looked_at", ""), Jump("null_button")]

# Screens for displaying the incubated sample collected
screen display_incubated_floor_sample():
    zorder 53
    hbox:
        xpos 0.0 ypos 0.0
        imagebutton:
            idle "received_dna_from_blood_pool"
            hover "received_dna_from_blood_pool"

            action NullAction()
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "You received the sample from the incubator! Now it's time to put the sample in the centrifuge."
            textbutton "Great!":
                action Return(True)

screen display_incubated_knife_sample():
    zorder 53
    hbox:
        xpos 0.0 ypos 0.0
        imagebutton:
            idle "received_dna_from_knife"
            hover "received_dna_from_knife"

            action NullAction()
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "You received the sample from the incubator! Now it's time to put the sample in the centrifuge."
            textbutton "Great!":
                action Return(True)

screen display_incubated_towel_sample():
    zorder 53
    hbox:
        xpos 0.0 ypos 0.0
        imagebutton:
            idle "received_dna_from_towel"
            hover "received_dna_from_towel"

            action NullAction()
    frame:
        xpos 0.15 ypos 0.15
        vbox:
            text "You received the sample from the incubator! Now it's time to put the sample in the centrifuge."
            textbutton "Great!":
                action Return(True)

# ---------------------------------------------------------------------------------------------------------


# -----------------------  Screens for comparing the DNA profiles: -----------------------------------
screen profiles():
    zorder 50

    # button for adding profile
    hbox:
        xpos 0.84739583 ypos 0.01759259
        imagebutton:
            insensitive "transparent"
            idle "add_profile_idle"
            hover "add_profile_hover"

            action ToggleVariable("table_of_findings.display_add_box")
            sensitive (table_of_findings.first_evidence == None) or (table_of_findings.second_evidence == None)

    # button to place the profile
    hbox:
        xpos 0.19583333 ypos 0.21018519
        imagebutton:
            insensitive "transparent"
            idle "place_profile_idle"
            hover "place_profile_hover"

            action [ToggleVariable("table_of_findings.display_add_box"), Jump("add_to_table")]

            sensitive table_of_findings.display_add_box
# ----------------------------------------------------------------------------------------------------------