### Kitchen screen
screen kitchen_screen(discovered_blood_pool, discovered_blood_spatter):
    imagemap:
        idle "kitchen_idle"
        hover "kitchen_hover"

        hotspot (793, 433, 394, 577) action Jump("stove") mouse "inspect"

        if discovered_blood_pool:
            hotspot (483, 853, 318, 152) action Jump("floor") mouse "inspect"
        if discovered_blood_spatter:
            hotspot (141, 308, 128, 198) action Jump("wall") mouse "inspect"

screen kitchen_stove():
    imagemap:
        idle "stove_idle"
        hover "stove_hover"

        hotspot (286, 676, 1307, 383) action Jump("oven") mouse "inspect"
        hotspot (807, 680, 363, 378) action Jump("dish_towel") mouse "inspect"

    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

screen oven_screen():
    imagemap:
        idle "oven_idle"
        hover "oven_hover"

        hotspot (462, 409, 308, 220) action Jump("view_knife") mouse "inspect"

    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

screen dish_towel():
    imagemap:
        idle "dish_towel_idle"
        hover "dish_towel_idle"

    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")

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

screen kitchen_wall():
    imagemap:
        idle "wall_idle"
        hover "wall_idle"

    hbox:
        xpos 0.01 ypos 0.86
        imagebutton:
            idle "back_button" at smaller_back
            hover "back_button_hover"
            action Jump("back")


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

transform smaller_flashlight():
    zoom 0.5

transform smaller_als():
    zoom 0.75

transform smaller_back():
    zoom 0.25

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

 
screen expand_tools():
    hbox:
        xpos 0.85 ypos 0.02
        imagebutton:
            insensitive "transparent" at smaller_als
            idle "als_flashlights_idle"
            hover "als_flashlights_hover"

            hovered Notify("ALS Lights")
            unhovered Notify('')

            action Jump("select_light")
            sensitive tools["ALS_lights"]
    hbox:
        xpos 0.888 ypos 0.415
        imagebutton:
            insensitive "transparent"
            idle "scalebar_idle" at tools_extra_small
            hover "scalebar_hover"

            hovered Notify("scale bar")
            unhovered Notify('')

            action Jump('scalebar')
            sensitive tools['scalebar']

    hbox:
        xpos 0.890 ypos 0.590
        imagebutton:
            insensitive "transparent"
            idle "lifting_backing_idle" at tools_extra_small
            hover "lifting_backing_hover"

            hovered Notify("fingerprint lifting tape")
            unhovered Notify('')

            action Jump('lifting_tape')
            sensitive tools['lifting_tape_and_backing']

    hbox:
        xpos 0.013 ypos 0.5
        imagebutton:
            insensitive "transparent"
            idle "evident_tape_idle" at tools_extra_small
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')
            sensitive tools['sealing_tape']

    hbox:
        xpos 0.02 ypos 0.67
        imagebutton:
            insensitive "transparent"
            idle "evidence_bags_idle" at tools_extra_small
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')
            sensitive tools['evidence_bag']

screen uva_kitchen():
    imagemap:
        idle "dark_kitchen"
        hover "uva_light_hover"

        hotspot (0, 0, 200, 200) action Jump("nothing")
        hotspot (200, 0, 200, 200) action Jump("nothing")
        hotspot (400, 0, 200, 200) action Jump("nothing")
        hotspot (600, 0, 200, 200) action Jump("nothing")
        hotspot (800, 0, 200, 200) action Jump("nothing")
        hotspot (1000, 0, 200, 200) action Jump("nothing")
        hotspot (1200, 0, 200, 200) action Jump("nothing")
        hotspot (1400, 0, 200, 200) action Jump("nothing")
        hotspot (1600, 0, 200, 200) action Jump("nothing")
        hotspot (1800, 0, 120, 200) action Jump("nothing")
        hotspot (0, 200, 200, 200) action Jump("discovered_wall_spatter")
        hotspot (200, 200, 200, 200) action Jump("discovered_wall_spatter")
        hotspot (400, 200, 200, 200) action Jump("nothing")
        hotspot (600, 200, 200, 200) action Jump("nothing")
        hotspot (800, 200, 200, 200) action Jump("nothing")
        hotspot (1000, 200, 200, 200) action Jump("nothing")
        hotspot (1200, 200, 200, 200) action Jump("nothing")
        hotspot (1400, 200, 200, 200) action Jump("nothing")
        hotspot (1600, 200, 200, 200) action Jump("nothing")
        hotspot (1800, 200, 120, 200) action Jump("nothing")
        hotspot (0, 400, 200, 200) action Jump("discovered_wall_spatter")
        hotspot (200, 400, 200, 200) action Jump("discovered_wall_spatter")
        hotspot (400, 400, 200, 200) action Jump("nothing")
        hotspot (600, 400, 200, 200) action Jump("nothing")
        hotspot (800, 400, 200, 200) action Jump("nothing")
        hotspot (1000, 400, 200, 200) action Jump("nothing")
        hotspot (1200, 400, 200, 200) action Jump("nothing")
        hotspot (1400, 400, 200, 200) action Jump("nothing")
        hotspot (1600, 400, 200, 200) action Jump("nothing")
        hotspot (1800, 400, 120, 200) action Jump("nothing")
        hotspot (0, 600, 200, 200) action Jump("nothing")
        hotspot (200, 600, 200, 200) action Jump("nothing")
        hotspot (400, 600, 200, 200) action Jump("nothing")
        hotspot (600, 600, 200, 200) action Jump("nothing")
        hotspot (800, 600, 200, 200) action Jump("nothing")
        hotspot (1000, 600, 200, 200) action Jump("nothing")
        hotspot (1200, 600, 200, 200) action Jump("nothing")
        hotspot (1400, 600, 200, 200) action Jump("nothing")
        hotspot (1600, 600, 200, 200) action Jump("nothing")
        hotspot (1800, 600, 120, 200) action Jump("nothing")
        hotspot (0, 800, 200, 200) action Jump("nothing")
        hotspot (200, 800, 200, 200) action Jump("nothing")
        hotspot (400, 800, 200, 200) action Jump("discovered_floor_blood")
        hotspot (600, 800, 200, 200) action Jump("discovered_floor_blood")
        hotspot (800, 800, 200, 200) action Jump("nothing")
        hotspot (1000, 800, 200, 200) action Jump("nothing")
        hotspot (1200, 800, 200, 200) action Jump("nothing")
        hotspot (1400, 800, 200, 200) action Jump("nothing")
        hotspot (1600, 800, 200, 200) action Jump("nothing")
        hotspot (1800, 800, 120, 200) action Jump("nothing")
        hotspot (0, 1000, 200, 80) action Jump("nothing")
        hotspot (200, 1000, 200, 80) action Jump("nothing")
        hotspot (400, 1000, 200, 80) action Jump("nothing")
        hotspot (600, 1000, 200, 80) action Jump("nothing")
        hotspot (800, 1000, 200, 80) action Jump("nothing")
        hotspot (1000, 1000, 200, 80) action Jump("nothing")
        hotspot (1200, 1000, 200, 80) action Jump("nothing")
        hotspot (1400, 1000, 200, 80) action Jump("nothing")
        hotspot (1600, 1000, 200, 80) action Jump("nothing")
        hotspot (1800, 1000, 120, 80) action Jump("nothing")
    hbox:
        xpos 0.01 ypos 0.88 at smaller_flashlight
        imagebutton:
            idle "uva_flashlight_idle"
            hover "uva_flashlight_hover"

            action Jump("selected_uva")

screen kitchen_415nm():
    imagemap:
        idle "415nm_light_idle"
        hover "415nm_light_hover"

        hotspot (472, 849, 347, 163) action Jump("discovered_floor_blood")
        hotspot(136, 311, 134, 196) action Jump("discovered_wall_spatter")

    hbox:
        xpos 0.01 ypos 0.88 at smaller_flashlight
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

screen mark_footprints():

    imagemap:
        idle "abandoned_house_idle"
        hover "abandoned_house_idle"

        hotspot (585, 830, 126, 172) action Jump("placed_marker")
                
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