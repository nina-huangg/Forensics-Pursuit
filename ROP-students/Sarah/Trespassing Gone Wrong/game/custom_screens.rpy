## Opening screen ###############################################################
screen opening_screen():
    imagemap:
        idle "background_idle"
        hover "background_hover"
        ground "background_idle"
        hotspot (1491, 198, 356, 102) action Jump("enter_splash_screen")

screen splash_screen():
    key "K_SPACE" action Jump("instructions_text")

screen move_on():
    frame:
        xpos 0.80 ypos 0.70
        hbox:
            spacing 3
            text "hit space to continue >>"

screen instructions_text_screen():
    frame:
        xcenter 0.5 ycenter 0.5
        hbox:
            spacing 5
            xsize 800
            text "Before we enter the crime scene, let's make sure you know how to navigate your surroundings.\n\n>>hit space to continue"
    key "K_SPACE" action Jump("instructions_key_arrows")

screen instructions_key_screen():
    if middle:
        key "K_UP" action [ToggleDict(front_directions, 'up'), Jump("jump_directions")]
        key "K_DOWN" action [ToggleDict(front_directions, 'down'), Jump("jump_directions")]
        key "K_RIGHT" action [ToggleDict(front_directions, 'right'), Jump("jump_directions")]
        key "K_LEFT" action [ToggleDict(front_directions, 'left'), Jump("jump_directions")]
    else:
        if curr_directions['up']:
            key "K_DOWN" action Jump("jump_directions")
        elif curr_directions['down']:
            key "K_UP" action Jump("jump_directions")
        if curr_directions['right']:
            key "K_LEFT" action Jump("jump_directions")
        elif curr_directions['left']:
            key "K_RIGHT" action Jump("jump_directions")


screen opening(word):
    frame:
        xalign 0.5 ypos 50
        vbox:
            text "You are at the front door, [word]."
  

screen instructions_move_on_screen():
    frame:
        xalign 0.5 yalign 0.5
        vbox:
            text "Are you ready to move on?"
            textbutton "Yes":
                action Jump("enter_scene")
            textbutton "Keep exploring the keys":
                action Jump("keep_exploring")

### entering scene 
screen entering_screen():
    imagemap:
        idle "instructions_bg"
        hover "front_hover"
        ground "instructions_bg"
        hotspot (768, 209, 346, 656) action Jump("hallway")

screen hallway_screen():
    if middle:
        key "K_UP" action [ToggleDict(hallway_directions, 'up'), Jump("hallway_directions")]
        key "K_DOWN" action [ToggleDict(hallway_directions, 'down'), Jump("hallway_directions")]
        key "K_RIGHT" action [ToggleDict(hallway_directions, 'right'), Jump("hallway_directions")]
        key "K_LEFT" action [ToggleDict(hallway_directions, 'left'), Jump("hallway_directions")]
    else:
        if curr_directions['up']:
            key "K_DOWN" action Jump("hallway_directions")
        elif curr_directions['down']:
            key "K_UP" action Jump("hallway_directions")
        if curr_directions['right']:
            key "K_LEFT" action Jump("hallway_directions")
        elif curr_directions['left']:
            key "K_RIGHT" action Jump("hallway_directions")
    key "K_SPACE" action Jump("examination_kitchen")

### kitchen scene
screen stove_screen():
    key "K_UP" action [ToggleDict(stove_directions, 'up'), Jump("stove_directions")]
    key "K_DOWN" action [ToggleDict(stove_directions, 'down'), Jump("stove_directions")]
    key "K_RIGHT" action [ToggleDict(stove_directions, 'right'), Jump("stove_directions")]
    key "K_LEFT" action [ToggleDict(stove_directions, 'left'), Jump("stove_directions")]

screen kitchen_screen():
    imagemap:
        idle "kitchen_idle"
        hover "kitchen_hover"
        ground "kitchen_idle"
        hotspot (245, 685, 438, 400) action Jump("examination_stove")

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

transform dental_stone_powder_size():
    zoom 0.5
 
screen expand_tools():
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
            sensitive tools['lifting_tape']

    hbox:
        xpos 0.013 ypos 0.5
        imagebutton:
            insensitive "transparent"
            idle "evident_tape_idle" at tools_extra_small
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')
            sensitive tools['tape']

    hbox:
        xpos 0.02 ypos 0.67
        imagebutton:
            insensitive "transparent"
            idle "evidence_bags_idle" at tools_extra_small
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')
            sensitive tools['bag']

    hbox:
        xpos 0.895 ypos 0.238
        imagebutton:   
            insensitive "transparent"
            idle "magnetic_powder" at tools_extra_small
            hover "hover_magnetic_powder"

            hovered Notify("granular powder")
            unhovered Notify('')

            action Jump('magnetic_powder')
            sensitive tools['powder']

    hbox:
        xpos 0.03 ypos 0.3
        imagebutton:
            insensitive "transparent"
            idle "evidence_markers" at tools_extra_small
            hover "evidence_markers_hover"
    
            hovered Notify("evidence markers")
            unhovered Notify('')

            action Jump('evidence_markers')
            sensitive tools['marker']

    hbox:
        xpos 0.89 ypos 0.03
        imagebutton:
            insensitive "transparent"
            idle "uv_light_idle" at tools_extra_small
            hover "uv_light_hover"
    
            hovered Notify("flashlight")
            unhovered Notify('')

            action Jump('uv_light')
            sensitive tools['light']

    hbox:
        xpos 0.85 ypos 0.05
        imagebutton:
            insensitive "transparent"
            idle "fixative_idle" at resize_tool
            hover "fixative_hover"

            hovered Notify("fixative")
            unhovered Notify('')

            action Jump("fixative")
            sensitive tools["fixative"]

    hbox:
        xpos 0.89 ypos 0.3
        imagebutton:
            insensitive "transparent"
            idle "dental_stone_powder_idle" at dental_stone_powder_size
            hover "dental_stone_powder_hover"

            hovered Notify("dental stone powder")
            unhovered Notify('')

            action Jump("dental_stone_powder")
            sensitive tools["dental_stone_powder"]

    hbox:
        xpos 0.87 ypos 0.5
        imagebutton:
            insensitive "transparent"
            idle "water_pitcher_idle" at resize_tool
            hover "water_pitcher_hover"

            hovered Notify("water")
            unhovered Notify('')

            action Jump("water")
            sensitive tools["water"]

    hbox:
        xpos 0.87 ypos 0.7
        imagebutton:
            insensitive "transparent"
            idle "spatula_idle" at resize_tool
            hover "spatula_hover"

            hovered Notify("spatula")
            unhovered Notify('')

            action Jump("spatula")
            sensitive tools["spatula"]

    hbox:
        xpos 0.02 ypos 0.83
        imagebutton:
            insensitive "transparent"
            idle "timer_idle" at resize_tool
            hover "timer_hover"

            hovered Notify("timer")
            unhovered Notify('')

            action Jump("timer")
            sensitive tools["timer"]

    hbox:
        xpos 0.02 ypos 0.68
        imagebutton:
            insensitive "transparent"
            idle "open_box_idle" at resize_tool
            hover"open_box_hover"

            hovered Notify("box")
            unhovered Notify('')

            action Jump("open_box")
            sensitive tools["box"]

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