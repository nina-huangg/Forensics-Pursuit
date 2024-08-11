screen dont_need_light():
    zorder 52
    tag dont_need_light
    frame:
        xpos 0.35 ypos 0.2
        vbox:
            text "We don't need to use this here."
            textbutton "Okay":
                action Return(True)

# Screen for not being able to use tool here
screen cant_use_here():
    zorder 52
    tag cant_use_here
    frame:
        xpos 0.35 ypos 0.2
        vbox:
            text "Hmm . . . I don't think we need to use this here."
            textbutton "Okay":
                action Return(True)

# Screen for finding no fingerprints
screen no_fingerprints_here():
    zorder 52
    tag no_fingerprints_here
    frame:
        xpos 0.35 ypos 0.2
        vbox:
            text "Hmm . . . I don't think we'll find any fingerprints here."
            textbutton "Okay":
                action Return(True)

### Screens for taking photos
screen camera_screen():
    zorder 51
    tag camera_sccreen
    hbox:
        xpos 0.16 ypos 0.001
        imagebutton:
            idle "camera_idle" at somewhat_smaller_camera
            hover "camera_hover"

            action Jump("took_photo")

# Screen for taking photo of unmarked blood spot
screen blood_spot_camera():
    zorder 51
    tag blood_spot_camera
    hbox:
        xpos 0.215 ypos 0.885
        imagebutton:
            idle "camera_idle" at even_smaller_camera
            hover "camera_hover"

            action Jump("took_photo_unmarked_bloodspot")

# Screen for taking close up photo of dish towel
screen dish_towel_camera():
    zorder 51
    tag dish_towel_camera
    hbox:
        xpos 0.58645833 ypos 0.40925926
        imagebutton:
            idle "camera_idle" at even_smaller_camera
            hover "camera_hover"

            action Jump("took_photo_dish_towel")

# Screen for taking close up photo of unmarked knife
screen knife_unmarked_camera():
    zorder 51
    tag knife_unmarked_camera
    hbox:
        xpos 0.51822917 ypos 0.54444444
        imagebutton:
            idle "camera_idle" at even_smaller_camera
            hover "camera_hover"

            action Jump("took_photo_knife_unmarked")

# Screen for taking close up photo of marked knife
screen knife_marked_camera():
    zorder 51
    tag knife_marked_camera
    hbox:
        xpos 0.51822917 ypos 0.54444444
        imagebutton:
            idle "camera_idle" at even_smaller_camera
            hover "camera_hover"

            action Jump("took_photo_knife_marked")

# SCreen for taking a close up photo of fingerprint
screen fingerprint_camera():
    zorder 51
    tag fingerprint_camera
    hbox:
        xpos 0.38645833 ypos 0.59444444
        imagebutton:
            idle "camera_idle" at even_smaller_camera
            hover "camera_hover"

            action Jump("took_photo_fingerprint")

### Screen for outside the house
screen outside_house():
    tag outside_house
    zorder 0
    imagemap:
        idle "front"
        hover "front_hover"

        hotspot (763, 209, 353, 660) action Return(True)

### Screen for the collected evidence
transform smaller_evidence:
    zoom 0.5

transform smaller_buttons:
    zoom 0.75

transform smaller_camera:
    zoom 0.8

transform somewhat_smaller_camera:
    zoom 0.5

transform even_smaller_camera:
    zoom 0.3

# Screen for next and previous page buttons
screen present_evidence(current_page, num_photos_taken):
    zorder 52
    tag present_evidence
    hbox:
        xpos 0.76 ypos 0.4
        imagebutton:
            insensitive "inventory-arrow-right-disabled"
            idle "inventory-arrow-right-enabled-idle"
            hover "inventory-arrow-right-enabled-hover"

            action Jump("next_page")
            sensitive current_page < num_photos_taken
    
    hbox:
        xpos 0.16 ypos 0.4
        imagebutton:
            insensitive "inventory-arrow-left-disabled"
            idle "inventory-arrow-left-enabled-idle"
            hover "inventory-arrow-left-enabled-hover"

            action Jump("back_page")
            sensitive current_page > 1

    hbox:
        xpos 0.17 ypos 0.14
        imagebutton:
            idle "back_button" at even_smaller_back
            hover "back_button_hover"

            action Jump("hide_images")

### Screen for the flashlight effect
# define a screen for overlay
screen dark_overlay_with_mouse():
    tag dark_overlay_with_mouse
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())
    # Adding the darkness overlay with the current mouse position
    add "flashlight_effect" pos mouse anchor (0.5, 0.5)

### Kitchen screen (Screen showing what they player can click on)
screen kitchen_screen(discovered_blood_pool, collected_dish_towel):
    zorder 50
    tag kitchen_screen
    hbox:
        xpos 0.37864583 ypos 0.22777778
        imagebutton:
            idle "kitchen_screen_stove_idle"
            hover "kitchen_screen_stove_hover"

            action Jump("stove") mouse "inspect"

    hbox:
        xpos 0.15 ypos 0.88425926
        imagebutton:
            insensitive "transparent"
            idle "kitchen_screen_floor_idle"
            hover "kitchen_screen_floor_hover"

            action Jump("floor") mouse "inspect"
            sensitive discovered_blood_pool

    hbox:
        xpos 0.509375 ypos 0.43055556
        imagebutton:
            idle "kitchen_screen_towel_idle"
            hover "kitchen_screen_towel_hover"

            action Jump("dish_towel") mouse "inspect"
            sensitive not collected_dish_towel

# Screen for placing an evidence marker in the kitchen
screen place_marker_kitchen():
    zorder 50
    tag place_marker_kitchen
    hbox:
        xpos 0.509375 ypos 0.43055556
        imagebutton:
            idle "kitchen_screen_towel_idle"
            hover "kitchen_screen_towel_hover"

            action Jump("placed_marker_dish_towel")

### Screens for the stove
# Screen for back button for the stove
screen stove_buttons():
    zorder 50
    tag stove_buttons
    hbox:
        xpos 0.93 ypos 0.88
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

# Screen for player to find fingerprint
screen dark_stove():
    zorder 50
    tag dark_stove
    hbox:
        xpos 0.288 ypos 0.51296296
        imagebutton:
            idle "finding_fingerprint_transparent"
            hover "finding_fingerprint_transparent"

            action Jump("found_fingerprint") mouse ("important")

# Screen for placing evidence marker on stove
screen place_marker_stove():
    zorder 50
    tag place_marker_stove
    hbox:
        xpos 0.51510417 ypos 0.4537037
        imagebutton:
            idle "knife_idle"
            hover "knife_hover"
            action Jump("placed_knife")

# Screen for collecting knife off of stove
screen collected_knife():
    zorder 50
    tag collected_knife
    hbox:
        xpos 0.51510417 ypos 0.4537037
        imagebutton:
            idle "knife_idle"
            hover "knife_hover"
            action Jump("knife_put_in_tube")

# Screen for taping forensic tube
screen tube_with_knife(sealed_tube_top, sealed_tube_bottom):
    zorder 50
    tag tube_with_knife
    hbox:
        xpos 0.433 ypos 0.152
        imagebutton:
            insensitive "tape_buttons_idle"
            idle "tape_buttons_idle"
            hover "top_tape_button_hover"

            action Jump("sealed_top")
            sensitive not sealed_tube_top

    hbox:
        xpos 0.433 ypos 0.732
        imagebutton:
            insensitive "tape_buttons_idle"
            idle "tape_buttons_idle"
            hover "bottom_tape_button_hover"

            action Jump("sealed_bottom")
            sensitive not sealed_tube_bottom

# Screen for putting forensic tube in evidence bag
screen collect_knife_tube():
    zorder 50
    tag collected_knife_tube
    hbox:
        xpos 0.42 ypos 0.1
        imagebutton:
            idle "taped_tube_idle"
            hover "taped_tube_hover"

            action Jump("collect_knife")

# Screen telling the player the knife has been collected
screen knife_has_been_collected():
    zorder 52
    tag knife_has_been_collected
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You collected the knife!"
            textbutton "Okay":
                action Return(True)

### Screens for fingerprint
# Screen for player to dust fingerprint
screen dust_fingerprint():
    zorder 50
    tag dust_fingerprint
    hbox:
        xpos 0.32291667 ypos 0.54537037
        imagebutton:
            idle "fingerprint_idle"
            hover "fingerprint_hover"
            action Jump("dusted_fingerprint")

# Screen for player to place scalebar
screen scalebar_screen():
    zorder 50
    tag scalebar_screen
    hbox:
        xpos 0.3125 ypos 0.25740741
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"

            action Jump("placed_scalebar")

# Screen for player to place lifting tape
screen taping_screen():
    zorder 50
    tag taping_screen
    hbox:
        xpos 0.3125 ypos 0.25740741
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"

            action Jump("placed_tape")

# Screen for player to lift fingerprint
screen picking_up_tape():
    zorder 50
    tag picking_up_tape
    hbox:
        xpos 0.24375 ypos 0.15740741
        imagebutton:
            idle "remove_tape_idle"
            hover "remove_tape_hover"
                
            action Jump("lifted_tape")

# Screen for placing the backing_card
screen placing_backing_card():
    zorder 50
    tag placing_backing_card
    hbox:
        xpos 0.309375 ypos 0.55462963
        imagebutton:
            idle "placing_card_idle"
            hover "placing_card_hover"

            action Jump("placed_backing_card")

# Screen for player to place fingerprint on backing card
screen placed_fingerprint():
    zorder 50
    tag placed_fingerprint
    hbox:
        xpos 0.30885417 ypos 0.55462963
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"
            
            action Jump("finished_placing_fingerprint")

# Screen for player to put backing card in evidence bag
screen packed_fingerprint():
    zorder 50
    tag packed_fingerprint
    hbox:
        xpos 0.10416667 ypos 0.28425926
        imagebutton:
            idle "backing_card_transparent"
            hover "backing_card_transparent"

            action Jump("pack_fingerprint")

# Screens telling the player messages about the fingerprint procedure
screen discovered_fingerprint_message():
    zorder 52
    tag discovered_fingerprint_message
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You discovered a latent fingerprint!"
            textbutton "Okay":
                action Return(True)

screen discover_fingerprint_first():
    zorder 52
    tag discover_fingerprint_first
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You need to discover a fingerprint first."
            textbutton "Okay":
                action Return(True)

screen already_dusted():
    zorder 52
    tag already_dusted
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already dusted the fingerprint."
            textbutton "Okay":
                action Return(True)

screen already_scaled():
    zorder 52
    tag already_scaled
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already placed a scale marker."
            textbutton "Okay":
                action Return(True)

screen already_taped():
    zorder 52
    tag already_taped
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already put tape on the fingerprint."
            textbutton "Okay":
                action Return(True)

screen already_put_on_card():
    zorder 52
    tag already_put_on_card
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already put the fingerprint on a backing card."
            textbutton "Okay":
                action Return(True)

screen in_fingerprinting_procedure():
    zorder 52
    tag in_fingerprinting_procedure
    frame:
        xpos 0.25 ypos 0.45
        vbox:
            text "You are currently collecting a fingerprint, you cannot use this now."
            textbutton "Okay":
                action Return(True)

screen fingerprint_has_been_collected():
    zorder 52
    tag fingerprint_has_been_collected
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You successfully collected the fingerprint!"
            textbutton "Okay":
                action Return(True)

screen nothing_to_mark():
    zorder 52
    tag nothing_to_mark
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "There is currently no evidence to mark."
            textbutton "Okay":
                action Return(True)

screen already_collecting_knife():
    zorder 52
    tag already_collecting_knife
    frame:
        xpos 0.3 ypos 0.1
        vbox:
            text "You are currently collecting the knife. Finish that first."
            textbutton "Okay":
                action Return(True)

### Screen for dish towel
# Screen for dish towel back button
screen dish_towel():
    zorder 50
    tag dish_towel
    hbox:
        xpos 0.93 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

# Screen for placing evidence marker for dish towel
screen place_marker_dish_towel():
    zorder 50
    tag place_marker_dish_towel
    hbox:
        xpos 0.44479167 ypos 0.11574074
        imagebutton:
            idle "close_up_towel_idle"
            hover "close_up_towel_hover"

            action Jump("placed_marker_dish_towel")

# Screen for putting dish towel in evidence bag
screen collecting_dish_towel():
    zorder 50
    tag collecting_dish_towel
    hbox:
        xpos 0.44479167 ypos 0.11574074
        imagebutton:
            idle "close_up_towel_idle"
            hover "close_up_towel_hover"

            action Jump("collect_towel")
# Screen with message telling player they collected the dish towel
screen dish_towel_has_been_collected():
    zorder 52
    tag dish_towel_has_been_collected
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You collected the dish towel!"
            textbutton "Okay":
                action Return(True)

## Screen for kitchen floor
# Screen for back button
screen kitchen_floor():
    zorder 50
    tag kitchen_floor
    hbox:
        xpos 0.93 ypos 0.885
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

# Screen for the swabbing procedure
screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab):
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

    # Transparent button for swabbing the floor
    hbox:
        xpos 0.30260417 ypos 0.3212963
        imagebutton:
            idle "floor_highlight_idle"
            hover "floor_highlight_hover"

            action Jump("swabbed_floor")
            sensitive swabbing_floor

    # Button for placing swab back in place
    hbox:
        xpos 0.24 ypos 0.3
        imagebutton:
            insensitive "transparent"
            idle "swab_placeholder_idle"
            hover "swab_placeholder_hover"

            action Jump("place_swab")
            sensitive not display_clean_swab and not display_positive_swab

    # Button displaying the clean swab
    hbox:
        xpos 0.22 ypos 0.325
        imagebutton:
            insensitive "transparent"
            idle "clean_swab"
            hover "clean_swab"

            action Jump("pick_up_swab")
            sensitive display_clean_swab

    # Button displaying the swab with the positive result of the kastle-meyer test
    hbox:
        xpos 0.22 ypos 0.325
        imagebutton:
            insensitive "transparent"
            idle "kastle_meyer_positive"
            hover "kastle_meyer_positive"

            action Jump("pick_up_swab")
            sensitive display_positive_swab

# Screen for making the luminol
screen luminol(only_water, luminol_ready):
    zorder 50
    tag luminol
    hbox:
        xpos 0.3796875 ypos 0.2
        imagebutton:
            idle "luminol_bottle_button"
            hover "luminol_bottle_button_hover"

            action Jump("selected_bottle")

# Screen for spraying the luminol
screen spraying_luminol():
    zorder 50
    tag spraying_luminol
    hbox:
        xpos 0.29791667 ypos 0.40925926
        imagebutton:
            idle "dark_floor_highlight_idle"
            hover "dark_floor_highlight_hover"

            action Jump("spray_luminol")

# SCreen for taping swab tube
screen taping_swab():
    zorder 50
    tag taping_swab
    hbox:
        xpos 0.4640625 ypos 0.30833333
        imagebutton:
            idle "collected_sample"
            hover "collected_sample_hover"

            action Jump("taped_sample_tube")

# Screen for putting tube in evidence bag
screen packing_swab():
    zorder 50
    tag packing_swab
    hbox:
        xpos 0.4640625 ypos 0.30833333
        imagebutton:
            idle "taped_sample"
            hover "taped_sample_hover"

            action Jump("packaged_swab")

# Screens for messages regarding swabbing and the luminol process
screen correct_kastle_meyer_procedure():
    zorder 52
    tag correct_kastle_meyer_procedure
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "The sample is positive for blood! \nYou can discard this swab and collect a new sample for analysis."
            textbutton "Okay":
                action Return(True)

screen incorrect_kastle_meyer_procedure():
    zorder 52
    tag incorrect_kastle_meyer_procedure
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "Seems like the sample is negative for blood. \nAre you sure you did it correctly?"
            textbutton "Yes, I'm sure.":
                action Return(True)
            textbutton "No.":
                action Jump("not_sure")

screen give_direction():
    zorder 52
    tag give_direction
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You can always redo the kastle-meyer test. \nJust discard the swab and try again!"
            textbutton "Okay":
                action Return(True)

screen incorrect_swab_warning():
    zorder 52
    tag incorrect_swab_warning
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You are trying to package an incorrect sample or \na swab that does not need to be collected. \nEither continue the swabbing process or dispose \nof the swab."
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

screen no_kastle_meyer_test():
    zorder 52
    tag no_kastle_meyer_test
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You have not conducted a kastle-meyer test. \nAre you sure this is blood?"
            textbutton "Yes, I'm sure":
                action Return(True)
            textbutton "No":
                action Jump("more_guidance")

screen explain_more():
    zorder 52
    tag explain_more
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You can determine if this is blood by \nconducting a kastle-meyer test"
            textbutton "Okay":
                action Return(True)

screen cannot_use_now():
    zorder 52
    tag cannot_use_now
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You are currently in the middle of swabbing. \nFinish swabbing first."
            textbutton "Okay":
                action Return(True)

screen swab_has_been_collected():
    zorder 52
    tag swab_has_been_collected
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You collected a swab of the sample!"
            textbutton "Okay!":
                action Return(True)

screen finish_collecting():
    zorder 52
    tag finish_collecting
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You are currently packing the evidence. \n Finish that first."
            textbutton "Okay":
                action Return(True)

screen collect_swab_first():
    zorder 52
    tag collect_swab_first
    frame:
        xpos 0.25 ypos 0.45
        vbox:
            text "You haven't collected a sample of the swab. \nLuminol can degrade the DNA, you should collect a sample first."
            textbutton "Okay":
                action Return(True)

screen currently_holding_swab():
    zorder 52
    tag currently_holding_swab
    frame:
        xpos 0.3 ypos 0.1
        vbox:
            text "You cannot use this now, you are holding a swab."
            textbutton "Okay":
                action Return(True)

screen swabbed_floor_message():
    zorder 52
    tag swabbed_floor_message
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You swabbed the floor."
            textbutton "Okay":
                action Return(True)

screen swabbing_in_progress():
    zorder 52
    tag swabbing_in_progress
    frame:
        xpos 0.25 ypos 0.1
        vbox:
            text "You are in the middle of collecting a sample, you cannot use this right now."
            textbutton "Okay":
                action Return(True)

screen in_luminol_process():
    zorder 52
    tag in_luminol_process
    frame:
        xpos 0.3 ypos 0.1
        vbox:
            text "You are currently making luminol, you cannot use this now."
            textbutton "Okay":
                action Return(True)

### Screen for sealing the evidence bag
screen collected_evidence():
    zorder 50
    tag collected_evidence
    hbox:
        xpos 0.4 ypos 0.07
        imagebutton:
            idle "packed_evidence_bag"
            hover "packed_evidence_bag_hover"

            action Jump("seal_evidence_bag")
 
transform smaller_back():
    zoom 0.25

transform even_smaller_back():
    zoom 0.2

# Screen telling player they discovered potential blood
screen discovered_blood_with_flashlight():
    tag discovered_blood_with_flashlight
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You discovered some potential blood!"
            textbutton "Okay":
                action Return(True)

screen uv_back_button():
    zorder 50
    tag uv_back_button
    hbox:
        xpos 0.93 ypos 0.88 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("uv_light")

# Screen for when player is using UVA flashlight
screen uva_kitchen():
    zorder 50
    tag uva_kitchen
    hbox:
        xpos 0.133 ypos 0.82407407
        imagebutton:
            idle "blood_transparent"
            hover "blood_transparent"

            action Jump("discovered_floor_blood") mouse ("important")
    hbox:
        xpos 0.93 ypos 0.88 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_uva")

# Screen for when player is using 415nm flashlight
screen kitchen_415nm():
    zorder 50
    tag kitchen_415nm
    hbox:
        xpos 0.133 ypos 0.82407407
        imagebutton:
            idle "blood_transparent"
            hover "blood_transparent"

            action Jump("discovered_floor_blood") mouse ("important")
    hbox:
        xpos 0.93 ypos 0.88 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_415nm")

# Screen for whn player is using 450nm flashlight
screen kitchen_450nm():
    tag kitchen_450nm
    hbox:
        xpos 0.93 ypos 0.88 at smaller_back        
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_450nm")

# Screen for when the player is using the 530nm flashlight
screen kitchen_530nm():
    tag kitchen_530nm
    hbox:
        xpos 0.93 ypos 0.88 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_530nm")

screen finished_collecting_evidence():
    frame:
        xpos 0.2 ypos 0.4
        vbox:
            text "You've finished collecting all the evidence! It's now time to analyze it in the lab."
            textbutton "Okay":
                action Return(True)