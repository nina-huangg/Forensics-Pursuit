### Screen for outside the house

screen outside_house():
    imagemap:
        idle "front"
        hover "front_hover"

        hotspot (763, 209, 353, 660) action Return(True)

### Screen for the collected evidence
transform smaller_evidence:
    zoom 0.5

transform smaller_buttons:
    zoom 0.75

transform smaller_bags:
    zoom 0.5

transform smaller_camera:
    zoom 0.8

screen collected_evidence_icon():
    hbox:
        xpos 0.03 ypos 0.3
        imagebutton:
            idle "casefile_bin_idle" at smaller_evidence
            hover "casefile_bin_hover"

            action Jump("display_evidence")

    hbox:
        xpos 0.03 ypos 0.48
        imagebutton:
            idle "camera_idle" at smaller_camera
            hover "camera_hover"

            action Jump("display_images")

screen present_evidence(current_page):
    hbox:
        xpos 0.75 ypos 0.4
        imagebutton:
            insensitive "casefile_photos_next"
            idle "casefile_photos_next" at smaller_buttons
            hover "casefile_photos_next_hover"

            action Jump("next_page")
            sensitive current_page < 11
    
    hbox:
        xpos 0.15 ypos 0.4
        imagebutton:
            insensitive "casefile_photos_prev"
            idle "casefile_photos_prev" at smaller_buttons
            hover "casefile_photos_prev_hover"

            action Jump("back_page")
            sensitive current_page > 1

screen dish_towel_evidence_message():
    frame:
        xpos 0.35 ypos 0.02
        vbox:
            text "This bag contains the dish towel."
            textbutton "Okay":
                action Return(True)

screen knife_evidence_message():
    frame:
        xpos 0.35 ypos 0.02
        vbox:
            text "This bag contains the knife."
            textbutton "Okay":
                action Return(True)

screen fingerprint_evidence_message():
    frame:
        xpos 0.25 ypos 0.02
        vbox:
            text "This bag contains the backing card with the fingerprint."
            textbutton "Okay":
                action Return(True)

screen swab_evidence_message():
    frame:
        xpos 0.35 ypos 0.02
        vbox:
            text "This bag contains the swab sample."
            textbutton "Okay":
                action Return(True)

screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab):
    hbox:
        xpos 0.23 ypos 0.15
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence1"
            hover "casefile_evidence1"

            action Jump("dish_towel_message")
            sensitive collected_dish_towel
    
    hbox:
        xpos 0.5 ypos 0.15
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence2"
            hover "casefile_evidence2"

            action Jump("knife_message")
            sensitive collected_knife

    hbox:
        xpos 0.23 ypos 0.44
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence3"
            hover "casefile_evidence3"

            action Jump("fingerprint_message")
            sensitive collected_fingerprint

    hbox:
        xpos 0.5 ypos 0.44
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence4"
            hover "casefile_evidence4"

            action Jump("swab_message")
            sensitive collected_swab

transform page_1_pic():
    zoom 0.25

transform page_2_pic():
    zoom 0.21

transform page_11_pic():
    zoom 0.55

screen display_image(current_page, discovered_blood_pool, dish_towel_marked, knife_marked, collected_fingerprint, captured_luminol):
    hbox:
        xpos 0.235 ypos 0.15
        imagebutton:
            insensitive "transparent"
            idle "mid_range_stove" at page_1_pic
            hover "mid_range_stove"

            action NullAction()
            sensitive current_page == 1

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "untouched_stove" at page_2_pic
            hover "untouched_stove"

            action NullAction()
            sensitive current_page == 2

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "knife_close_up" at page_2_pic
            hover "knife_close_up"

            action NullAction()
            sensitive current_page == 3

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "unmarked_floor" at page_2_pic
            hover "unmarked_floor"

            action NullAction()
            sensitive discovered_blood_pool and current_page == 4

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "marked_floor" at page_2_pic
            hover "makred_floor"

            action NullAction()
            sensitive discovered_blood_pool and current_page == 5

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "towel_with_marker" at page_2_pic
            hover "towel_with_marker"

            action NullAction()
            sensitive dish_towel_marked and current_page == 6

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "towel_very_close" at page_2_pic
            hover "towel_very_close"

            action NullAction()
            sensitive dish_towel_marked and current_page == 7

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "knife_close_up_marked" at page_2_pic
            hover "knife_close_up_marked"

            action NullAction()
            sensitive knife_marked and current_page == 8

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "fingerprint_close" at page_2_pic
            hover "fingerprint_close"

            action NullAction()
            sensitive collected_fingerprint and current_page == 9

    hbox:
        xpos 0.228 ypos 0.16
        imagebutton:
            insensitive "transparent"
            idle "fingerprint_very_close" at page_2_pic
            hover "fingerprint_very_close"

            action NullAction()
            sensitive collected_fingerprint and current_page == 10

    hbox:
        xpos 0.22 ypos 0.17
        imagebutton:
            insensitive "transparent"
            idle "luminol_floor_picture" at page_11_pic
            hover "luminol_floor_picture"

            action NullAction()
            sensitive captured_luminol and current_page == 11

### Screen for the flashlight effect
# define a screen for overlay
screen dark_overlay_with_mouse():
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())
    # Adding the darkness overlay with the current mouse position
    add "flashlight_effect" pos mouse anchor (0.5, 0.5)

### Kitchen screen
screen kitchen_screen(discovered_blood_pool, collected_dish_towel):
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

screen place_marker_kitchen():
    hbox:
        xpos 0.509375 ypos 0.43055556
        imagebutton:
            idle "kitchen_screen_towel_idle"
            hover "kitchen_screen_towel_hover"

            action Jump("placed_marker_dish_towel")

### Screens for the stove
screen stove_buttons():
    hbox:
        xpos 0.01 ypos 0.88
        imagebutton:
            idle "back_button" at even_smaller_back
            hover "back_button_hover"
            action Jump("back")

screen dark_stove():
    hbox:
        xpos 0.288 ypos 0.51296296
        imagebutton:
            idle "finding_fingerprint_transparent"
            hover "finding_fingerprint_transparent"

            action Jump("found_fingerprint") mouse ("important")

screen place_marker_stove():
    hbox:
        xpos 0.51510417 ypos 0.4537037
        imagebutton:
            idle "knife_idle"
            hover "knife_hover"
            action Jump("placed_knife")

screen collected_knife():
    hbox:
        xpos 0.51510417 ypos 0.4537037
        imagebutton:
            idle "knife_idle"
            hover "knife_hover"
            action Jump("knife_put_in_tube")

screen tube_with_knife():
    hbox:
        xpos 0.42 ypos 0.1
        imagebutton:
            idle "filled_tube_idle"
            hover "filled_tube_hover"

            action Jump("sealed_knife_tube")

screen collect_knife_tube():
    hbox:
        xpos 0.42 ypos 0.1
        imagebutton:
            idle "taped_tube_idle"
            hover "taped_tube_hover"

            action Jump("collect_knife")

screen sealed_knife():
    hbox:
        xpos 0.38125 ypos 0.13703704
        imagebutton:
            idle "evidence_bag_transparent"
            hover "evidence_bag_transparent"
            action Jump("sealed_knife_bag")

screen knife_has_been_collected():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You collected the knife!"
            textbutton "Okay":
                action Return(True)

### Screens for fingerprint
screen dust_fingerprint():
    hbox:
        xpos 0.32291667 ypos 0.54537037
        imagebutton:
            idle "fingerprint_idle"
            hover "fingerprint_hover"
            action Jump("dusted_fingerprint")

screen scalebar_screen():
    hbox:
        xpos 0.3125 ypos 0.25740741
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"

            action Jump("placed_scalebar")

screen taping_screen():
    hbox:
        xpos 0.3125 ypos 0.25740741
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"

            action Jump("placed_tape")

screen picking_up_tape():
    hbox:
        xpos 0.3125 ypos 0.25740741
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"
                
            action Jump("lifted_tape")

screen placed_fingerprint():
    hbox:
        xpos 0.30885417 ypos 0.55462963
        imagebutton:
            idle "fingerprint_procedure_transparent"
            hover "fingerprint_procedure_transparent"
            
            action Jump("finished_placing_fingerprint")

screen packed_fingerprint():
    hbox:
        xpos 0.10416667 ypos 0.28425926
        imagebutton:
            idle "backing_card_transparent"
            hover "backing_card_transparent"

            action Jump("pack_fingerprint")

screen discovered_fingerprint_message():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You discovered a latent fingerprint!"
            textbutton "Okay":
                action Return(True)

screen discover_fingerprint_first():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You need to discover a fingerprint first."
            textbutton "Okay":
                action Return(True)

screen already_dusted():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already dusted the fingerprint."
            textbutton "Okay":
                action Return(True)

screen already_scaled():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already placed a scale marker."
            textbutton "Okay":
                action Return(True)

screen already_taped():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already put tape on the fingerprint."
            textbutton "Okay":
                action Return(True)

screen already_put_on_card():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You already put the fingerprint on a backing card."
            textbutton "Okay":
                action Return(True)

screen in_fingerprinting_procedure():
    frame:
        xpos 0.25 ypos 0.45
        vbox:
            text "You are currently collecting a fingerprint, you cannot use this now."
            textbutton "Okay":
                action Return(True)

screen fingerprint_has_been_collected():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You successfully collected the fingeprrint!"
            textbutton "Okay":
                action Return(True)

screen nothing_to_mark():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "There is currently no evidence to mark."
            textbutton "Okay":
                action Return(True)

### Screen for dish towel
screen dish_towel():
    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

screen place_marker_dish_towel():
    hbox:
        xpos 0.44479167 ypos 0.11574074
        imagebutton:
            idle "close_up_towel_idle"
            hover "close_up_towel_hover"

            action Jump("placed_marker_dish_towel")

screen collecting_dish_towel():
    hbox:
        xpos 0.44479167 ypos 0.11574074
        imagebutton:
            idle "close_up_towel_idle"
            hover "close_up_towel_hover"

            action Jump("collect_towel")

screen seal_dish_towel():
    imagemap:
        idle "dish_towel_collected_bag"
        hover "dish_towel_collected_bag"

        hotspot (668, 96, 539, 891) action Jump("sealed_towel_bag")

screen dish_towel_has_been_collected():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You collected the dish towel!"
            textbutton "Okay":
                action Return(True)

## Screen for kitchen floor
screen kitchen_floor():
    hbox:
        xpos 0.01 ypos 0.885
        imagebutton:
            idle "back_button" at even_smaller_back
            hover "back_button_hover"
            action Jump("back")

screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab):
    # Button for packing/collecting the tube
    hbox:
        xpos 0.13229167 ypos 0.68703704
        imagebutton:
            idle "tube_idle"
            hover "tube_hover"

            action Jump("collect_swab")

    # Button for throwing out the swab
    hbox:
        xpos 0.75677083 ypos 0.76203704
        imagebutton:
            idle "garbage_idle"
            hover "garbage_hover"

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
        xpos 0.206 ypos 0.3
        imagebutton:
            insensitive "transparent"
            idle "swab_placeholder_idle"
            hover "swab_placeholder_hover"

            action Jump("place_swab")
            sensitive not display_clean_swab and not display_positive_swab

    # Button displaying the clean swab
    hbox:
        xpos 0.19 ypos 0.325
        imagebutton:
            insensitive "transparent"
            idle "clean_swab"
            hover "clean_swab"

            action Jump("pick_up_swab")
            sensitive display_clean_swab

    # Button displaying the swab with the positive result of the kastle-meyer test
    hbox:
        xpos 0.19 ypos 0.325
        imagebutton:
            insensitive "transparent"
            idle "kastle_meyer_positive"
            hover "kastle_meyer_positive"

            action Jump("pick_up_swab")
            sensitive display_positive_swab


screen luminol(only_water, luminol_ready):
    hbox:
        xpos 0.3796875 ypos 0.2
        imagebutton:
            idle "luminol_bottle_button"
            hover "luminol_bottle_button_hover"

            action Jump("selected_bottle")

screen spraying_luminol():
    hbox:
        xpos 0.29791667 ypos 0.40925926
        imagebutton:
            idle "dark_floor_highlight_idle"
            hover "dark_floor_highlight_hover"

            action Jump("spray_luminol")

screen packing_swab(bag_selected):
    hbox:
        xpos 0.4640625 ypos 0.30833333
        imagebutton:
            insensitive "collected_sample"
            idle "collected_sample"
            hover "collected_sample_hover"

            action Jump("packaged_swab")
            sensitive bag_selected

screen capture_luminol():
    hbox:
        xpos 0.1 ypos 0.1
        imagebutton:
            idle "camera_icon" at smaller_evidence
            hover "camera_icon"

            action Jump("took_picture")

screen incorrect_kastle_meyer_procedure():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "Seems like the sample is negative for blood. \nAre you sure you did it correctly?"
            textbutton "Yes, I'm sure.":
                action Return(True)
            textbutton "No.":
                action Jump("not_sure")

screen give_direction():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You can always redo the kastle-meyer test. \nJust discard the swab and try again!"
            textbutton "Okay":
                action Return(True)

screen incorrect_swab_warning():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You are trying to package an incorrect sample or \na swab that does not need to be collected. \nEither continue the swabbing process or dispose \nof the swab."
            textbutton "Okay":
                action Return (True)
            
screen already_collected_swab():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You already collected a sample from here."
            textbutton "Okay":
                action Return(True)

screen no_kastle_meyer_test():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You have not conducted a kastle-meyer test. \nAre you sure this is blood?"
            textbutton "Yes, I'm sure":
                action Return(True)
            textbutton "No":
                action Jump("more_guidance")

screen explain_more():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You can determine if this is blood by \nconducting a kastle-meyer test"
            textbutton "Okay":
                action Return(True)

screen cannot_use_now():
    frame:
        xpos 0.3 ypos 0.15
        vbox:
            text "You are currently in the middle of swabbing. \nFinish swabbing first."
            textbutton "Okay":
                action Return(True)

screen swab_has_been_collected():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You collected a swab of the sample!"
            textbutton "Okay!":
                action Return(True)

screen finish_collecting():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You are currently packing the evidence. \n Finish that first."
            textbutton "Okay":
                action Return(True)

screen collect_swab_first():
    frame:
        xpos 0.25 ypos 0.45
        vbox:
            text "You haven't collected a sample of the swab. You should do that first."
            textbutton "Okay":
                action Return(True)

screen currently_holding_swab():
    frame:
        xpos 0.3 ypos 0.1
        vbox:
            text "You cannot use this now, you are holding a swab."
            textbutton "Okay":
                action Return(True)

screen swabbed_floor_message():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You swabbed the floor."
            textbutton "Okay":
                action Return(True)

### Screen for evidence bag
screen collected_evidence():
    hbox:
        xpos 0.4 ypos 0.07
        imagebutton:
            idle "packed_evidence_bag"
            hover "packed_evidence_bag"

            action Jump("seal_evidence_bag")

### Toolbox screen
screen toolbox():
    modal False

    hbox:
        xpos 0.03 ypos 0.02
        imagebutton:
            idle "toolbox" at toolbox_smaller
            hover "toolbox_hover"
            action Jump("tool_expand")
 
transform toolbox_smaller():
    zoom 0.1

transform tools_extra_small():
    zoom 0.06

transform resize_tool():
    zoom 0.75

transform smaller_tool():
    zoom 0.5

transform smaller_als():
    zoom 0.75

transform smaller_back():
    zoom 0.25

transform even_smaller_back():
    zoom 0.2

transform smaller_bottle():
    zoom 0.6

transform larger_powder():
    zoom 2.5

transform smaller_evidence_tools():
    zoom 0.7

transform even_smaller_evidence_tools():
    zoom 0.6

screen select_ALS():
    hbox:
        xpos 0.375 ypos 0.25
        imagebutton:
            idle "uva_flashlight_idle"
            hover "uva_flashlight_hover"

            hovered Notify("UVA flashlight")

            action Jump("selected_uva")

    hbox:
        xpos 0.475 ypos 0.25
        imagebutton:
            idle "415nm_flashlight_idle"
            hover "415nm_flashlight_hover"

            hovered Notify("415nm flashlight")

            action Jump("selected_415nm")
        
    hbox:
        xpos 0.375 ypos 0.55
        imagebutton:
            idle "450nm_flashlight_idle"
            hover "450nm_flashlight_hover"

            hovered Notify("450nm flashlight")

            action Jump("selected_450nm")

    hbox:
        xpos 0.475 ypos 0.55
        imagebutton:
            idle "530nm_flashlight_idle"
            hover "530nm_flashlight_hover"

            hovered Notify("530nm flashlight")

            action Jump("selected_530nm")

screen discovered_blood_with_flashlight():
    frame:
        xpos 0.35 ypos 0.45
        vbox:
            text "You discovered some potential blood!"
            textbutton "Okay":
                action Return(True)
 
screen expand_kitchen_tools():
    hbox:
        xpos 0.02 ypos 0.47
        imagebutton:
            idle "als_flashlights_idle" at smaller_als
            hover "als_flashlights_hover"

            hovered Notify("ALS Lights")
            unhovered Notify('')

            action Jump("select_light")
    hbox:
        xpos 0.03 ypos 0.27
        imagebutton:
            idle "evidence_markers" at smaller_evidence_tools
            hover "evidence_markers_hover"

            hovered Notify("Evidence markers")
            
            action Jump("place_evidence_marker")

screen expand_stove_tools():
    hbox:
        xpos 0.9 ypos 0.03
        imagebutton:
            idle "uv_light_idle" at smaller_evidence_tools
            hover "uv_light_hover"
    
            hovered Notify("UV Flashlight")
            unhovered Notify('')

            action Jump('uv_light')

    hbox:
        xpos 0.9 ypos 0.25
        imagebutton:
            idle "magnetic_powder" at smaller_evidence_tools
            hover "hover_magnetic_powder"

            hovered Notify("Black Granular Powder")
            unhovered Notify("")

            action Jump("select_black_powder")

    hbox:
        xpos 0.915 ypos 0.46
        imagebutton:
            idle "scalebar_idle" at smaller_tool
            hover "scalebar_hover"

            hovered Notify("Scalebar")
            unhovered Notify('')

            action Jump("selected_scalebar")

    hbox:
        xpos 0.91 ypos 0.62
        imagebutton:
            idle "lifting_tape_idle" at even_smaller_evidence_tools
            hover "lifting_tape_hover"

            hovered Notify("lifting_tape")
            unhovered Notify('')

            action Jump("selected_lifting_tape")

    hbox:
        xpos 0.9 ypos 0.79
        imagebutton:
            idle "backing_cards_idle" at even_smaller_evidence_tools
            hover "backing_cards_hover"

            hovered Notify("Backing Cards")
            unhovered Notify('')

            action Jump("selected_backing_card")

    hbox:
        xpos 0.03 ypos 0.27
        imagebutton:
            idle "evidence_markers" at even_smaller_evidence_tools
            hover "evidence_markers_hover"

            hovered Notify("Evidence markers")
            
            action Jump("place_evidence_marker")

    hbox:
        xpos 0.02 ypos 0.39
        imagebutton:
            idle "evident_tape_idle" at even_smaller_evidence_tools
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')

    hbox:
        xpos 0.026 ypos 0.53
        imagebutton:
            idle "evidence_bags_idle" at even_smaller_evidence_tools
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')

    hbox:
        xpos 0.025 ypos 0.71
        imagebutton:
            idle "forensic_tube_idle" at even_smaller_evidence_tools
            hover "forensic_tube_hover"

            hovered Notify("Forensic Tube")
            unhovered Notify('')

            action Jump("selected_forensic_tube")

screen expand_floor_tools():
    hbox:
        xpos 0.85 ypos 0.003
        imagebutton:
            idle "cotton_swab_idle" at resize_tool
            hover "cotton_swab_hover"

            hovered Notify("Cotton Swab")
            unhovered Notify('')

            action Jump('selected_swab')

    hbox:
        xpos 0.86 ypos 0.13
        imagebutton:
            idle "distilled_water_idle" at resize_tool
            hover "distilled_water_hover"

            hovered Notify("Distilled Water")
            unhovered Notify('')

            action Jump('wet')

    hbox:
        xpos 0.87 ypos 0.34
        imagebutton:
            idle "ethanol_idle" at resize_tool
            hover "ethanol_hover"

            hovered Notify("Ethanol")
            unhovered Notify('')

            action Jump('ethanol')
    hbox:
        xpos 0.87 ypos 0.56
        imagebutton:
            idle "phenolphthalein_idle" at resize_tool
            hover "phenolphthalein_hover"

            hovered Notify("Phenolphthalein")
            unhovered Notify('')

            action Jump('phenolphthalein')

    hbox:
        xpos 0.87 ypos 0.78
        imagebutton:
            idle "hydrogen_peroxide_idle" at resize_tool
            hover "hydrogen_peroxide_hover"

            hovered Notify("Hydrogen Peroxide")
            unhovered Notify('')

            action Jump("hydrogen_peroxide")

    hbox:
        xpos 0.03 ypos 0.59
        imagebutton:
            idle "spray_bottle_idle" at smaller_bottle
            hover "spray_bottle_hover"

            hovered Notify("Spray Bottle")
            unhovered Notify('')

            action Jump("spray_bottle")

    hbox:
        xpos 0.035 ypos 0.76
        imagebutton:
            idle "bluestar_luminol_packet_idle" at smaller_tool
            hover "bluestar_luminol_packet_hover"

            hovered Notify("Bluestar Luminol Packet")
            unhovered Notify('')

            action Jump("luminol_packet")
    hbox:
        xpos 0.02 ypos 0.26
        imagebutton:
            idle "evident_tape_idle" at even_smaller_evidence_tools
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')

    hbox:
        xpos 0.02 ypos 0.4
        imagebutton:
            idle "evidence_bags_idle" at smaller_evidence_tools
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')

screen expand_dish_towel_tools():
    hbox:
        xpos 0.02 ypos 0.42
        imagebutton:
            idle "evident_tape_idle" at smaller_evidence_tools
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')

    hbox:
        xpos 0.027 ypos 0.59
        imagebutton:
            idle "evidence_bags_idle" at smaller_evidence_tools
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')
    
    hbox:
        xpos 0.03 ypos 0.27
        imagebutton:
            idle "evidence_markers" at smaller_evidence_tools
            hover "evidence_markers_hover"

            hovered Notify("Evidence markers")
            
            action Jump("place_evidence_marker")


screen uva_kitchen():
    hbox:
        xpos 0.133 ypos 0.82407407
        imagebutton:
            idle "blood_transparent"
            hover "blood_transparent"

            action Jump("discovered_floor_blood") mouse ("important")
    hbox:
        xpos 0.01 ypos 0.85 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_uva")

screen kitchen_415nm():
    hbox:
        xpos 0.133 ypos 0.82407407
        imagebutton:
            idle "blood_transparent"
            hover "blood_transparent"

            action Jump("discovered_floor_blood") mouse ("important")
    hbox:
        xpos 0.01 ypos 0.85 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_415nm")

screen kitchen_450nm():
    hbox:
        xpos 0.01 ypos 0.85 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_450nm")

screen kitchen_530nm():
    hbox:
        xpos 0.01 ypos 0.85 at smaller_back
        imagebutton:
            idle "back_button"
            hover "back_button_hover"

            action Jump("selected_530nm")