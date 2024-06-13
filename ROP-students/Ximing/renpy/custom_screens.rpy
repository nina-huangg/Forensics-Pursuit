screen opening_screen():
    imagemap:
        idle "background_idle"
        hover "background_hover"
        ground "background_idle"
        hotspot (1491, 198, 356, 102) action Jump("enter_splash_screen")

screen splash_screen():
    key "K_SPACE" action Jump("instructions_text")

screen inside_screen:
    imagemap:
        idle "interior_idle"
        hover "interior_hover"
        ground "interior_idle"
        hotspot (590, 295, 535, 222) action Jump("examination_table")

screen table_screen:
    key "K_LEFT" action [ToggleDict(table_directions, 'left'), Jump("table_directions")]
    key "K_RIGHT" action [ToggleDict(table_directions, 'right'), Jump("table_directions")]


screen toolbox():
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

screen uv_light_table():
    default discover = False
    imagemap:
        idle "table_fingerprint"
        hover "table_fingerprint_hover"
        ground "table_fingerprint"
        hotspot (601, 858, 70, 70) action SetLocalVariable('discover', True)

    showif discover:
        image "table_fingerprint_hover"
        # frame:
        #     xalign 0.6 yalign 0.5
        #     text "You've discovered a latent fingerprint!"
        hbox:
            xalign 0.95 yalign 0.93
            imagebutton:
                idle "checkmark" at checkmark_small
                hover "checkmark_hover"
                action Jump("finished_uv_light")

screen expand_tools():
    hbox:
        xpos 0.888 ypos 0.415
        imagebutton:
            insensitive "scalebar_insensitive" at tools_extra_small
            idle "scalebar_idle"
            hover "scalebar_hover"

            hovered Notify("scale bar")
            unhovered Notify('')

            action Jump('scalebar')
            sensitive tools['scalebar']

    hbox:
        xpos 0.890 ypos 0.590
        imagebutton:
            insensitive "lifting_backing_insensitive" at tools_extra_small
            idle "lifting_backing_idle"
            hover "lifting_backing_hover"

            hovered Notify("fingerprint lifting tape")
            unhovered Notify('')

            action Jump('lifting_tape')
            sensitive tools['lifting_tape']

    hbox:
        xpos 0.004 ypos 0.3
        imagebutton:
            insensitive "evident_tape_insensitive" at tools_extra_small
            idle "evident_tape_idle"
            hover "evident_tape_hover"

            hovered Notify("evident tape")
            unhovered Notify('')

            action Jump('tamper_tape')
            sensitive tools['tape']

    hbox:
        xpos 0.038 ypos 0.47
        imagebutton:
            insensitive "evidence_bags_insensitive" at tools_extra_small
            idle "evidence_bags_idle"
            hover "evidence_bags_hover"

            hovered Notify("evidence bags")
            unhovered Notify('')

            action Jump('evidence_bags')
            sensitive tools['bag']

    hbox:
        xpos 0.895 ypos 0.238
        imagebutton:   
            insensitive "magnetic_powder_insensitive" at tools_extra_small
            idle "magnetic_powder"
            hover "hover_magnetic_powder"

            hovered Notify("granular powder")
            unhovered Notify('')

            action Jump('magnetic_powder')
            sensitive tools['powder']

    hbox:
        xpos 0.021 ypos 0.67
        imagebutton:
            insensitive "evidence_markers_insensitive" at tools_extra_small
            idle "evidence_markers"
            hover "evidence_markers_hover"
    
            hovered Notify("evidence markers")
            unhovered Notify('')

            action Jump('evidence_markers')
            sensitive tools['marker']

    hbox:
        xpos 0.89 ypos 0.03
        imagebutton:
            insensitive "uv_light_insensitive"
            idle "uv_light_idle" at tools_extra_small
            hover "uv_light_hover"
    
            hovered Notify("flashlight")
            unhovered Notify('')

            action Jump('uv_light')
            sensitive tools['light']

screen evidence_marker_table():
    hbox:
        xpos 0.26 yalign 0.78
        image "evidence_marker_1" at evidence_marker_1

transform checkmark_small():
    zoom 0.2

transform backing_card():
    zoom 0.31

transform evidence_marker_1():
    zoom 0.07

screen magnetic_powder_table():
    default dusted = False
    imagemap:
        idle "table_fingerprint_persist"
        hover "table_fingerprint_persist"
        hotspot (601, 858, 70, 70) action SetLocalVariable('dusted', True)
    
    showif dusted:
        image "table_fingerprint_dusted"
        frame:
            xalign 0.54 yalign 0.5
            text "You've dusted the fingerprint!"
        hbox:
            xalign 0.95 yalign 0.93
            imagebutton:
                idle "checkmark" at checkmark_small
                hover "checkmark_hover"
                action Jump("finished_magnetic_powder")

screen scalebar_table():
    default taped = False
    imagemap:
        idle "table_fingerprint_zoomed"
        hover "table_fingerprint_zoomed"
        hotspot (827,398,318,208) action SetLocalVariable('taped', True)
    
    showif taped:
        add "table_scalebar_taped_zoomed"
        # frame:
        #     xalign 0.6 yalign 0.38
        #     text "You've added the scalebar!"
        # add "stove_fingerprint_tape"
        hbox:
            xalign 0.95 yalign 0.93
            imagebutton:
                idle "checkmark" at checkmark_small
                hover "checkmark_hover"
                action Jump("finished_scalebar")

screen lifting_tape_table():
    default taped = False
    imagemap:
        idle "table_scalebar_taped_zoomed"
        hover "table_scalebar_taped_zoomed"
        hotspot (873,376,309,206) action Jump("lifting_to_backing")

screen backing_card_table(action):
    image "lifting_to_backing"
    if action=='lift':
        hbox:
            xpos 0.1 yalign 0.8
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

transform resize_current_evidence():
    zoom .2

transform resize_evidence_bags():
    zoom .1

transform resize_evidence_bags_seal():
    zoom .15


screen current_evidence(action):
    hbox:
        xalign 0.5 yalign 0.30
        text "current evidence collected":
            size 28

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
            image "table_evidence_bags"
            frame:
                xalign 0.65 yalign 0.6
                text "You've packaged your evidence!"
            hbox:
                xalign 0.5 yalign 0.30
                text "current evidence collected":
                    size 28
            hbox:
                xpos 0.75 ypos 0.50
                image "stove_evidence_bags_light" at resize_evidence_bags
        
            hbox:
                xalign 0.95 yalign 0.93
                imagebutton:
                    idle "checkmark" at checkmark_small
                    hover "checkmark_hover"
                    action Jump("evidence_bags_finished")
        
  

    

screen evidence_bags_table():
    hbox:
        xpos 0.45 ypos 0.30
        image "stove_evidence_bags_light" at resize_evidence_bags


screen tamper_evident_tape_table(sensitive):
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
            
        frame:
            xalign 0.6 yalign 0.5
            text "You've sealed the bag!"
        hbox:
            xalign 0.95 yalign 0.93
            imagebutton:
                idle "checkmark" at checkmark_small
                hover "checkmark_hover"
                action Jump("tutorial_finished")


screen move_on_lab():
    key "K_m" action Jump('tutorial_finished')
    frame:
        xpos 0.80 ypos 0.95
        hbox:
            spacing 3
            text "hit m to head to lab >>"

screen temporary_pause:
    key "K_SPACE" action NullAction()             
