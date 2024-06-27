### Screen for the collected evidence
transform smaller_evidence:
    zoom 0.5

transform smaller_buttons:
    zoom 0.75

transform smaller_bags:
    zoom 0.5

screen collected_evidence_icon():
    hbox:
        xpos 0.03 ypos 0.3
        imagebutton:
            idle "casefile_bin_idle" at smaller_evidence
            hover "casefile_bin_hover"

            action Jump("display_evidence")

screen present_evidence(current_page):
    hbox:
        xpos 0.75 ypos 0.4
        imagebutton:
            insensitive "casefile_photos_next"
            idle "casefile_photos_next" at smaller_buttons
            hover "casefile_photos_next_hover"

            action Jump("next_page")
            sensitive current_page < 15
    
    hbox:
        xpos 0.15 ypos 0.4
        imagebutton:
            insensitive "casefile_photos_prev"
            idle "casefile_photos_prev" at smaller_buttons
            hover "casefile_photos_prev_hover"

            action Jump("back_page")
            sensitive current_page > 0

screen evidence_background():
    hbox:
        xpos 0.0 ypos 0.05
        imagebutton:
            idle "casefile_inventory"
            hover "casefile_inventory"

            action NullAction()

screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab):
    hbox:
        xpos 0.2 ypos 0.15
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence1"
            hover "casefile_evidence1"

            action NullAction()
            sensitive collected_dish_towel
    
    hbox:
        xpos 0.5 ypos 0.15
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence2"
            hover "casefile_evidence2"

            action NullAction()
            sensitive collected_knife

    hbox:
        xpos 0.2 ypos 0.4
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence3"
            hover "casefile_evidence3"

            action NullAction()
            sensitive collected_fingerprint

    hbox:
        xpos 0.5 ypos 0.4
        imagebutton:
            insensitive "transparent" at smaller_evidence
            idle "casefile_evidence4"
            hover "casefile_evidence4"

            action NullAction()
            sensitive collected_swab



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
        xpos 0.16666667 ypos 0.895
        imagebutton:
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
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

screen dark_stove():
    hbox:
        xpos 0.36614583 ypos 0.57592593
        imagebutton:
            idle "finding_fingerprint_transparent"
            hover "finding_fingerprint_transparent"

            action Jump("found_fingerprint") mouse ("important")

screen place_marker_stove():
    hbox:
        xpos 0.4765625 ypos 0.35648148
        imagebutton:
            idle "place_marker_knife_transparent"
            hover "place_marker_knife_transparent"
            action Jump("placed_knife")

screen collected_knife():
    hbox:
        xpos 0.51822917 ypos 0.4537037
        imagebutton:
            idle "collect_knife_transparent"
            hover "collect_knife_transparent"
            action Jump("collect_knife")

screen sealed_knife():
    hbox:
        xpos 0.38125 ypos 0.13703704
        imagebutton:
            idle "evidence_bag_transparent"
            hover "evidence_bag_transparent"
            action Jump("sealed_knife_bag")

### Screens for fingerprint
screen dust_fingerprint():
    hbox:
        xpos 0.34010417 ypos 0.54722222
        imagebutton:
            idle "dusting_transparent"
            hover "dusting_transparent"
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
        xpos 0.3125 ypos 0.25740741
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
        xpos 0.12083333 ypos 0.1212963
        imagebutton:
            idle "marking_dish_towel_transparent"
            hover "marking_dish_towel_transparent"

            action Jump("placed_marker_dish_towel")

screen collecting_dish_towel():
    hbox:
        xpos 0.44791667 ypos 0.12037037
        imagebutton:
            idle "dish_towel_transparent"
            hover "dish_towel_transparent"

            action Jump("collect_towel")

screen seal_dish_towel():
    imagemap:
        idle "dish_towel_collected_bag"
        hover "dish_towel_collected_bag"

        hotspot (668, 96, 539, 891) action Jump("sealed_towel_bag")

## Screen for kitchen floor
screen kitchen_floor():
    imagemap:
        idle "floor_idle"
        hover "floor_idle"

    hbox:
        xpos 0.01 ypos 0.885
        imagebutton:
            idle "back_button" at even_smaller_back
            hover "back_button_hover"
            action Jump("back")

screen swabbing(display_swabbing_options, swabbing_floor, display_clean_swab, display_positive_swab):
    # Button for packing/collecting the tube
    hbox:
        xpos 0.13229167 ypos 0.68703704
        imagebutton:
            insensitive "transparent"
            idle "tube_idle"
            hover "tube_hover"

            action Jump("collect_swab")
            sensitive display_swabbing_options

    # Button for throwing out the swab
    hbox:
        xpos 0.75677083 ypos 0.76203704
        imagebutton:
            insensitive "transparent"
            idle "garbage_idle"
            hover "garbage_hover"

            action Jump("throw_out_swab")
            sensitive display_swabbing_options

    # Transparent button for swabbing the floor
    hbox:
        xpos 0.23645833 ypos 0.35640148
        imagebutton:
            idle "floor_transparent"
            hover "floor_transparent"

            action Jump("swabbed_floor")
            sensitive swabbing_floor

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

screen dark_floor():
    imagemap:
        idle "dark_floor"
        hover "dark_floor"

        hotspot (454, 385, 929, 574) action Jump("spray_luminol")

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

screen select_powder():
    hbox:
        xpos 0.25 ypos 0.3
        imagebutton:
            idle "black_granular_powder_idle" at larger_powder
            hover "black_granular_powder_hover"

            action NullAction()

    hbox:
        xpos 0.45 ypos 0.3
        imagebutton:
            idle "white_granular_powder_idle" at larger_powder
            hover "white_granular_powder_hover"

            action NullAction()
 
screen expand_kitchen_tools():
    hbox:
        xpos 0.85 ypos 0.05
        imagebutton:
            idle "als_flashlights_idle" at smaller_als
            hover "als_flashlights_hover"

            hovered Notify("ALS Lights")
            unhovered Notify('')

            action Jump("select_light")
    hbox:
        xpos 0.03 ypos 0.23
        imagebutton:
            idle "evidence_markers" at tools_extra_small
            hover "evidence_markers_hover"

            hovered Notify("Evidence markers")
            
            action Jump("place_evidence_marker")

screen expand_stove_tools():
    hbox:
        xpos 0.9 ypos 0.05
        imagebutton:
            idle "uv_light_idle" at tools_extra_small
            hover "uv_light_hover"
    
            hovered Notify("UV Flashlight")
            unhovered Notify('')

            action Jump('uv_light')

    #hbox:
        #xpos 0.9 ypos 0.25
        #imagebutton:
            #idle "granular_powder_idle"
            #hover "granular_powder_hover"

            #hovered Notify("Granular Powder")
            #unhovered Notify('')

            #action Jump('select_powder')

    hbox:
        xpos 0.9 ypos 0.3
        imagebutton:
            idle "magnetic_powder" at tools_extra_small
            hover "hover_magnetic_powder"

            hovered Notify("Black Granular Powder")
            unhovered Notify("")

            action Jump("select_black_powder")

    hbox:
        xpos 0.9 ypos 0.5
        imagebutton:
            idle "scalebar_idle" at tools_extra_small
            hover "scalebar_hover"

            hovered Notify("Scalebar")
            unhovered Notify('')

            action Jump("selected_scalebar")

    hbox:
        xpos 0.9 ypos 0.7
        imagebutton:
            idle "lifting_backing_idle" at tools_extra_small
            hover "lifting_backing_hover"

            hovered Notify("Lifting Tape and Backing Card")
            unhovered Notify('')

            action Jump("selected_lifting_tape")

    hbox:
        xpos 0.03 ypos 0.23
        imagebutton:
            idle "evidence_markers" at tools_extra_small
            hover "evidence_markers_hover"

            hovered Notify("Evidence markers")
            
            action Jump("place_evidence_marker")

    hbox:
        xpos 0.013 ypos 0.44
        imagebutton:
            idle "evident_tape_idle" at tools_extra_small
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')

    hbox:
        xpos 0.035 ypos 0.56
        imagebutton:
            idle "evidence_bags_idle" at tools_extra_small
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')

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
        xpos 0.013 ypos 0.265
        imagebutton:
            idle "evident_tape_idle" at tools_extra_small
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')

    hbox:
        xpos 0.035 ypos 0.39
        imagebutton:
            idle "evidence_bags_idle" at tools_extra_small
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')

screen expand_dish_towel_tools():
    hbox:
        xpos 0.013 ypos 0.44
        imagebutton:
            idle "evident_tape_idle" at tools_extra_small
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')

    hbox:
        xpos 0.035 ypos 0.56
        imagebutton:
            idle "evidence_bags_idle" at tools_extra_small
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')
    
    hbox:
        xpos 0.03 ypos 0.23
        imagebutton:
            idle "evidence_markers" at tools_extra_small
            hover "evidence_markers_hover"

            hovered Notify("Evidence markers")
            
            action Jump("place_evidence_marker")


screen uva_kitchen():
    hbox:
        xpos 0.17916667 ypos 0.88148148
        imagebutton:
            idle "blood_transparent"
            hover "blood_transparent"

            action Jump("discovered_floor_blood") mouse ("important")
    hbox:
        xpos 0.01 ypos 0.85 at smaller_tool
        imagebutton:
            idle "uva_flashlight_idle"
            hover "uva_flashlight_hover"

            action Jump("selected_uva")

screen kitchen_415nm():
    hbox:
        xpos 0.17916667 ypos 0.88148148
        imagebutton:
            idle "blood_transparent"
            hover "blood_transparent"

            action Jump("discovered_floor_blood") mouse ("important")
    hbox:
        xpos 0.01 ypos 0.85 at smaller_tool
        imagebutton:
            idle "415nm_flashlight_idle"
            hover "415nm_flashlight_hover"

            action Jump("selected_415nm")

screen kitchen_450nm():
    hbox:
        xpos 0.01 ypos 0.85 at smaller_tool
        imagebutton:
            idle "450nm_flashlight_idle"
            hover "450nm_flashlight_hover"

            action Jump("selected_450nm")

screen kitchen_530nm():
    hbox:
        xpos 0.01 ypos 0.85 at smaller_tool
        imagebutton:
            idle "530nm_flashlight_idle"
            hover "530nm_flashlight_hover"

            action Jump("selected_530nm")