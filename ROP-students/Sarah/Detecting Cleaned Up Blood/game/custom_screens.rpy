### Kitchen screen
screen kitchen_screen(discovered_blood_pool):
    imagebutton:
        xpos 0.41302083 ypos 0.40092593
        idle "stove_transparent"
        hover "stove_transparent"

        action Jump("stove") mouse "inspect"

    imagebutton:
        xpos 0.2515625 ypos 0.78981481
        idle "floor_transparent"
        hover "floor_transparent"

        action Jump("floor") mouse "inspect"
        sensitive discovered_blood_pool

screen place_marker_kitchen():
    imagebutton:
        xpos 0.4875 ypos 0.53981481
        idle "dish_towel_transparent"
        hover "dish_towel_transparent"

        action Jump("placed_marker_dish_towel")

### Screens for the stove
screen stove_buttons():
    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

    hbox:
        xpos 0.45 ypos 0.82
        imagebutton:
            idle "down_arrow_idle"
            hover "down_arrow_hover"
            action Jump("look_down")

screen dark_stove():

    hbox:
        xpos 0.415625 ypos 0.8037037
        imagebutton:
            idle "dark_idle"
            hover "dark_hover"

            action Jump("found_fingerprint") mouse ("important")

transform up_arrow():
    rotate 180

screen stove_looking_down():
    imagemap:
        idle "stove_down_idle"
        hover "stove_down_hover"

        hotspot (568, 668, 853, 244) action Jump("dish_towel")

    hbox:
        xpos 0.45 ypos 0.0
        imagebutton:
            idle "down_arrow_idle" at up_arrow
            hover "down_arrow_hover"
            action Jump("look_up")

screen place_marker_stove():
    hbox:
        xpos 0.334375 ypos 0.73240741
        imagebutton:
            idle "fingerprint_transparent"
            hover "fingerprint_transparent"
            action Jump("placed_fingerprint")

    hbox:
        xpos 0.38541667 ypos 0.33333333
        imagebutton:
            idle "knife_transparent"
            hover "knife_transparent"
            action Jump("placed_knife")

screen collected_knife():
    hbox:
        xpos 0.38541667 ypos 0.33333333
        imagebutton:
            idle "knife_transparent"
            hover "knife_transparent"
            action Jump("collect_knife")

screen sealed_knife():
    hbox:
        xpos 0.38125 ypos 0.13703704
        imagebutton:
            idle "evidence_bag_transparent"
            hover "evidence_bag_transparent"
            action Jump("sealed_knife_bag")

### Screen for dish towel
screen dish_towel():
    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

screen collected_dish_towel():
    imagemap:
        idle "dish_towel_uncollected"
        hover "dish_towel_uncollected"

        hotspot (700, 59, 518, 994) action Jump("collect_towel")

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
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

screen swab_procedure():
    imagemap:
        idle "floor_swab_idle"
        hover "floor_swab_hover"

        hotspot (254, 742, 102, 336) action Jump("collect_swab")
        hotspot (1453, 823, 173, 242) action Jump("throw_out_swab")

screen swab_floor():
    imagebutton:
        xpos 0.2 ypos 0.01388889
        idle "swab_transparent"
        hover "swab_transparent"

        action Jump("swabbed_floor")

screen clean_swab():
    imagemap:
        idle "display_clean_swab"
        hover "display_clean_swab"

        hotspot (429, 351, 74, 729) action Jump("pick_up_swab")

screen positive_swab():
    imagebutton:
        xpos 0.46510417 ypos 0.18148148
        idle "display_positive_swab2"
        hover "display_positive_swab2"

        action Jump("pick_up_swab")

screen empty_bottle():
    imagemap:
        idle "empty_bottle"
        hover "empty_bottle"

        hotspot (729, 87, 414, 895) action Jump("selected_bottle")

screen water_bottle():
    imagemap:
        idle "water_bottle"
        hover "water_bottle"

        hotspot (729, 87, 414, 895) action Jump("selected_bottle")

screen luminol_bottle():
    imagebutton:
        xpos 0.3796875 ypos 0.08529412
        idle "luminol_bottle"
        hover "luminol_bottle"

        action Jump("selected_bottle")

screen dark_floor():
    imagemap:
        idle "dark_floor"
        hover "dark_floor"

        hotspot (423, 0, 1526, 951) action Jump("spray_luminol")

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

transform smaller_bottle():
    zoom 0.35

transform larger_powder():
    zoom 2.5

screen select_ALS():
    hbox:
        xpos 0.3 ypos 0.3
        imagebutton:
            idle "uva_flashlight_idle"
            hover "uva_flashlight_hover"

            hovered Notify("UVA flashlight")

            action Jump("selected_uva")

    hbox:
        xpos 0.5 ypos 0.3
        imagebutton:
            idle "415nm_flashlight_idle"
            hover "415nm_flashlight_hover"

            hovered Notify("415nm flashlight")

            action Jump("selected_415nm")
        
    hbox:
        xpos 0.3 ypos 0.5
        imagebutton:
            idle "450nm_flashlight_idle"
            hover "450nm_flashlight_hover"

            hovered Notify("450nm flashlight")

            action Jump("selected_450")

    hbox:
        xpos 0.5 ypos 0.5
        imagebutton:
            idle "530nm_flashlight_idle"
            hover "530nm_flashlight_hover"

            hovered Notify("530nm flashlight")

            action Jump("selected_530")

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
        xpos 0.85 ypos 0.02
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

screen expand_stove_tools():
    hbox:
        xpos 0.9 ypos 0.05
        imagebutton:
            idle "uv_light_idle" at tools_extra_small
            hover "uv_light_hover"
    
            hovered Notify("UV Flashlight")
            unhovered Notify('')

            action Jump('uv_light')

    hbox:
        xpos 0.9 ypos 0.25
        imagebutton:
            idle "granular_powder_idle"
            hover "granular_powder_hover"

            hovered Notify("Granular Powder")
            unhovered Notify('')

            action Jump('select_powder')

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
        xpos 0.05 ypos 0.29
        imagebutton:
            idle "spray_bottle_idle" at smaller_bottle
            hover "spray_bottle_hover"

            hovered Notify("Spray Bottle")
            unhovered Notify('')

            action Jump("spray_bottle")

    hbox:
        xpos 0.04 ypos 0.77
        imagebutton:
            idle "bluestar_luminol_packet_idle" at smaller_tool
            hover "bluestar_luminol_packet_hover"

            hovered Notify("Bluestar Luminol Packet")
            unhovered Notify('')

            action Jump("luminol_packet")
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

screen uva_kitchen():
    imagemap:
        idle "dark_kitchen"
        hover "uva_light_hover"

        hotspot (0, 0, 200, 200) action NullAction()
        hotspot (200, 0, 200, 200) action NullAction()
        hotspot (400, 0, 200, 200) action NullAction()
        hotspot (600, 0, 200, 200) action NullAction()
        hotspot (800, 0, 200, 200) action NullAction()
        hotspot (1000, 0, 200, 200) action NullAction()
        hotspot (1200, 0, 200, 200) action NullAction()
        hotspot (1400, 0, 200, 200) action NullAction()
        hotspot (1600, 0, 200, 200) action NullAction()
        hotspot (1800, 0, 120, 200) action NullAction()
        hotspot (0, 200, 200, 200) action NullAction()
        hotspot (200, 200, 200, 200) action NullAction()
        hotspot (400, 200, 200, 200) action NullAction()
        hotspot (600, 200, 200, 200) action NullAction()
        hotspot (800, 200, 200, 200) action NullAction()
        hotspot (1000, 200, 200, 200) action NullAction()
        hotspot (1200, 200, 200, 200) action NullAction()
        hotspot (1400, 200, 200, 200) action NullAction()
        hotspot (1600, 200, 200, 200) action NullAction()
        hotspot (1800, 200, 120, 200) action NullAction()
        hotspot (0, 400, 200, 200) action NullAction()
        hotspot (200, 400, 200, 200) action NullAction()
        hotspot (400, 400, 200, 200) action NullAction()
        hotspot (600, 400, 200, 200) action NullAction()
        hotspot (800, 400, 200, 200) action NullAction()
        hotspot (1000, 400, 200, 200) action NullAction()
        hotspot (1200, 400, 200, 200) action NullAction()
        hotspot (1400, 400, 200, 200) action NullAction()
        hotspot (1600, 400, 200, 200) action NullAction()
        hotspot (1800, 400, 120, 200) action NullAction()
        hotspot (0, 600, 200, 200) action NullAction()
        hotspot (200, 600, 200, 200) action NullAction()
        hotspot (400, 600, 200, 200) action NullAction()
        hotspot (600, 600, 200, 200) action NullAction()
        hotspot (800, 600, 200, 200) action NullAction()
        hotspot (1000, 600, 200, 200) action NullAction()
        hotspot (1200, 600, 200, 200) action NullAction()
        hotspot (1400, 600, 200, 200) action NullAction()
        hotspot (1600, 600, 200, 200) action NullAction()
        hotspot (1800, 600, 120, 200) action NullAction()
        hotspot (0, 800, 200, 200) action NullAction()
        hotspot (200, 800, 200, 200) action NullAction()
        hotspot (400, 800, 200, 200) action Jump("discovered_floor_blood") mouse ("important")
        hotspot (600, 800, 200, 200) action Jump("discovered_floor_blood") mouse ("important")
        hotspot (800, 800, 200, 200) action NullAction()
        hotspot (1000, 800, 200, 200) action NullAction()
        hotspot (1200, 800, 200, 200) action NullAction()
        hotspot (1400, 800, 200, 200) action NullAction()
        hotspot (1600, 800, 200, 200) action NullAction()
        hotspot (1800, 800, 120, 200) action NullAction()
        hotspot (0, 1000, 200, 80) action NullAction()
        hotspot (200, 1000, 200, 80) action NullAction()
        hotspot (400, 1000, 200, 80) action NullAction()
        hotspot (600, 1000, 200, 80) action NullAction()
        hotspot (800, 1000, 200, 80) action NullAction()
        hotspot (1000, 1000, 200, 80) action NullAction()
        hotspot (1200, 1000, 200, 80) action NullAction()
        hotspot (1400, 1000, 200, 80) action NullAction()
        hotspot (1600, 1000, 200, 80) action NullAction()
        hotspot (1800, 1000, 120, 80) action NullAction()
    hbox:
        xpos 0.01 ypos 0.88 at smaller_tool
        imagebutton:
            idle "uva_flashlight_idle"
            hover "uva_flashlight_hover"

            action Jump("selected_uva")

screen kitchen_415nm():
    imagemap:
        idle "415nm_light_idle"
        hover "415nm_light_hover"

        hotspot (472, 849, 347, 163) action Jump("discovered_floor_blood")

    hbox:
        xpos 0.01 ypos 0.88 at smaller_tool
        imagebutton:
            idle "415nm_flashlight_idle"
            hover "415nm_flashlight_hover"

            action Jump("selected_415nm")


screen arrow():
    showif tools['light']:
        hbox:
            xpos 0.85 ypos 0.12
            image "arrow" at tools_extra_small
    showif tools['powder']:
        hbox:
            xpos 0.84 ypos 0.30
            image "arrow" at tools_extra_small
    showif tools['scalebar']:
        hbox:
            xpos 0.84 ypos 0.5
            image "arrow" at tools_extra_small
    showif tools['lifting_tape']:
        hbox:
            xpos 0.84 ypos 0.7
            image "arrow" at tools_extra_small
    showif tools['bag']:
        hbox:
            xpos 0.11 ypos 0.53
            image "arrow_flip" at tools_extra_small
    showif tools['tape']:
        hbox:
            xpos 0.11 ypos 0.33
            image "arrow_flip" at tools_extra_small
                
transform checkmark_small():
    zoom 0.2

transform backing_card():
    zoom 0.31

transform evidence_marker_1():
    zoom 0.07

transform resize_current_evidence():
    zoom .2

transform resize_evidence_bags():
    zoom .1

transform resize_evidence_bags_seal():
    zoom .15


screen current_evidence(action):

    if action=='insensitive':
        hbox:
            xpos 0.33 ypos 0.02
            image "complete_backing_card" at resize_current_evidence
        hbox:
            xpos 0.75 ypos 0.50
            image "stove_evidence_bags_light" at resize_evidence_bags
    else:
        hbox:
            xpos 0.75 ypos 0.50
            imagebutton:
                idle "stove_evidence_bags_light" at resize_evidence_bags
                hover "stove_evidence_bags_light_hover"
                action Jump('put_card_into_bag')

        if action =='show':
            hbox:
                xpos 0.33 ypos 0.02
                imagebutton:
                    idle "complete_backing_card" at resize_current_evidence
                    hover "complete_backing_card_hover"
                    action Jump("drag_card_into_bag")
        
        if action=='put_in':
            image "door_close_up_idle"
            hbox:
                xpos 0.75 ypos 0.50
                image "stove_evidence_bags_light" at resize_evidence_bags
        
            hbox:
                xalign 0.95 yalign 0.93
                imagebutton:
                    idle "checkmark" at checkmark_small
                    hover "checkmark_hover"
                    action Jump("evidence_bags_finished")
        


  

    

screen evidence_bags():
    hbox:
        xpos 0.45 ypos 0.30
        image "stove_evidence_bags_light" at resize_evidence_bags


screen tamper_evident_tape(sensitive):
    default taped = False
    if not sensitive:
        hbox:
            xpos 0.42 ypos 0.30
            image 'evidence_bags_idle' at resize_evidence_bags_seal
    else:
        hbox:
            xpos 0.42 ypos 0.30
            imagebutton:
                idle "evidence_bags_idle" at resize_evidence_bags_seal
                hover "evidence_bags_hover"
                action SetLocalVariable('taped', True)
    
    if taped:
        hbox:
            xpos 0.39 ypos 0.28
            image "evidence_bags_packed" at resize_evidence_bags_seal
            
        hbox:
            xalign 0.95 yalign 0.93
            imagebutton:
                idle "checkmark" at checkmark_small
                hover "checkmark_hover"
                action Jump("finished_fingerprint")


screen explore_outside():

    imagemap:
        idle "abandoned_house_idle.jpg"
        hover "abandoned_house_hover.jpg"

        hotspot (585, 830, 126, 172) action Jump("selected_footprints")
        hotspot (1205, 588, 125, 172) action Jump("selected_door")

screen explore_outside_marked():
    imagemap:
        idle "abandoned_house_marked_idle.jpg"
        hover "abandoned_house_hover.jpg"

        hotspot (585, 830, 126, 172) action Jump("selected_footprints")
        hotspot (1205, 588, 125, 172) action Jump("selected_door")


screen apply_fixative():
    imagemap:
        idle "footprint_idle.jpg"
        hover "footprint_idle.jpg"

        hotspot (725, 111, 520, 908) action Jump("applied_fixative")


screen powder_in_bag():
    imagemap:
        idle "empty_bag_idle.jpg"
        hover "empty_bag_hover.jpg"

        hotspot (669, 24, 661, 1009) action Jump("placed_powder")

screen add_water():
    imagemap:
        idle "with_powder_idle.jpg"
        hover "with_powder_hover.jpg"

        hotspot (669, 24, 661, 1009) action Jump("placed_water")

screen cast_footprint():
    imagemap:
        idle "mixed_idle.jpg"
        hover "mixed_hover.jpg"

        hotspot (669, 24, 661, 1009) action Jump("casted")

screen remove_cast():
    imagemap:
        idle "casted_footprint.jpg"
        hover "casted_footprint.jpg"

        hotspot (655, 44, 621, 1013) action Jump("removed_cast")

screen tape_box():
    imagemap:
        idle "closed_box_idle.jpg"
        hover "closed_box_hover.jpg"

        hotspot (514, 101, 884, 853) action Jump("finished_cast")

screen front_door():
    imagemap:
        idle "front_door_idle"
        hover "front_door_hover"

        hotspot (676, 22, 558, 1000) action Jump("inside")
        hotspot (1083, 552, 82, 165) action Jump("door_handle")

screen uv_light_door():
    imagemap:
        idle "door_close_up_dark_idle"
        hover "door_close_up_hover"

        hotspot (1342, 219, 119, 138) action Jump("found_fingerprint")

screen dust_door():
    imagemap:
        idle "door_close_up_idle"
        hover "door_close_up_idle"

        hotspot (1342, 219, 119, 138) action Jump("dusted")

screen scale_print():
    imagemap:
        idle "dusted_fingerprint"
        hover "dusted_fingerprint"

        hotspot (882, 284, 323, 263) action Jump("scaled")

screen lift_fingerprint():
    imagemap:
        idle "scaled_fingerprint"
        hover "scaled_fingerprint"

        hotspot (882, 284, 323, 263) action Jump("taped")

screen add_backing(action):
    image "door_close_up_dark_idle"
    if action=='lift':
        hbox:
            xpos 0.0003 yalign 0.8
            imagebutton:
                idle "tape_print_scalebar"
                hover "tape_print_scalebar_hover"
                action Jump("drag_tape")
        hbox:
            xpos 0.5 yalign 0.8
            image "backing_card" at backing_card
    elif action=='drag':
        hbox:
            xpos 0.5 yalign 0.8
            imagebutton:
                idle "backing_card" at backing_card
                hover "backing_card"
                action Jump("stick_backing")
    elif action=='stick':
        hbox:
            xpos 0.5 yalign 0.8
            image "complete_backing_card" at backing_card
    else:
        hbox:
            xpos 0.5 yalign 0.8
            image "complete_backing_card_r" at backing_card
        hbox:
            xpos 0.1 yalign 0.8
            image "complete_backing_card_front" at backing_card
        
        hbox:
            xalign 0.95 yalign 0.93
            imagebutton:
                idle "checkmark" at checkmark_small
                hover "checkmark_hover"
                action Jump("finish_lifting_tape")