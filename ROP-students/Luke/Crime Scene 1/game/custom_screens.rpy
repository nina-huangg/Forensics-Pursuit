

screen choice(items):
    style_prefix "choice"
    vbox:
        style "menu_choice_vbox"
        for i in items:
            textbutton i.caption action i.action

screen start_screen():
    imagemap:
        idle "background_idle"
        hover "background_hover"
        hotspot (1491, 198, 356, 102) action Jump("splash")

screen splash_screen():
    key "K_SPACE" action Jump("doorway")

screen doorway_screen():
    imagemap:
        idle "doorway"
        hover "doorway_hover"
        hotspot (768, 209, 346, 656) action Jump("main_room_intro")

screen main_room_screen():
    if len(collectable) == 0:
        imagemap:
            idle "main_room_empty"
        vbox:
            xalign 0.5
            yalign 0.8
            frame:
                text "You've collected all the evidence in this crime scene. proceed to lab?" 

            frame:
                xalign 0.5
                yalign 0.9
                textbutton "OK" action [Hide("tool_unavailable_screen"), Function(set_cursor, ''), Jump("proceed_to_lab")]

    elif 'bottle' in collectable and 'vase' in collectable:
        imagemap:
            idle "main_room"
            hover "main_room_hover"
            hotspot (1140, 710, 800, 500) action Jump("floor")
            hotspot (0, 470, 755, 600) action Jump("table")
            hotspot (750, 0, 850, 400) action Jump("wall")
    
    elif 'bottle' in collectable:
        imagemap:
            idle "main_room_bottle"
            hover "main_room_bottle_hover"
            hotspot (1140, 710, 800, 500) action Jump("floor")
            hotspot (0, 470, 755, 600) action Jump("table")
            hotspot (750, 0, 850, 400) action Jump("wall")
    elif 'vase' in collectable:
        imagemap:
            idle "main_room_vase"
            hover "main_room_vase_hover"
            hotspot (1140, 710, 800, 500) action Jump("floor")
            hotspot (0, 470, 755, 600) action Jump("table")
            hotspot (750, 0, 850, 400) action Jump("wall")
    else:
        imagemap:
            idle "main_room_empty"
            hover "main_room_empty_hover"
            hotspot (1140, 710, 800, 500) action Jump("floor")
            hotspot (0, 470, 755, 600) action Jump("table")
            hotspot (750, 0, 850, 400) action Jump("wall")


screen shoeprint_marker_screen():
    imagemap:
        idle "shoeprint_marker_idle"
        hover "shoeprint_marker_hover"
        hotspot (500, 390, 400, 400) action Return("marker_placed")

screen shoeprint_duster_screen(dust):
    if dust < 5:
        imagemap:
            idle "shoeprint_dusting_[dust]"
            hover "shoeprint_dusting_hover_[dust]"
            hotspot (610, 600, 700, 550) action Return("next_dust_level")
    if dust == 5:
        image "shoeprint_dusting_5"

    imagebutton:
        idle "checkmark" at Transform(zoom=0.4)
        hover "checkmark_hover"
        action Return("dusting_complete")
        xpos 0.85 ypos 0.78

screen shoeprint_lifter_screen():
    draggroup:
        drag:
            align(0.8, 0.5)
            drag_raise True
            drag_name "lifter"
            draggable True
            droppable False
            dragged dragged_func
            image "/images/floor/lifter_sheet.png" xysize (300, 400)
        drag:
            align(0.49, 0.88)
            drag_name "sheet"
            draggable False 
            droppable True
            dragged dragged_func
            image Solid((165, 165, 165, 128)) xysize (300, 400)

screen shoeprint_flattener_screen():
    imagemap:
        idle "shoeprint_flatten_idle"
        hover "shoeprint_flatten_hover"
        hotspot (770, 580, 450, 450) action Return("flattener_complete")

screen shoeprint_laminate_screen():
    imagebutton:
        idle "shoeprint_lifted" at shoeprint_lifted 
        hover "shoeprint_lifted_hover"  action Return("laminate_complete")
        xpos 0.5
        ypos 0.5
        anchor (0.5, 0.5)

screen shoeprint_evidence_bags_screen():
    imagebutton:
        idle "shoeprint_laminated_idle" at shoeprint_lifted 
        hover "shoeprint_laminated_hover"
        action [Function(remove_collectable, "shoeprint"), Jump("shoeprint_complete")]
        xpos 0.5 ypos 0.5
        anchor (0.5, 0.5)
    frame:
        xalign 0.5 yalign 0.9
        vbox:
            text "Click on the evidence bag to collect this shoeprint"

screen table_screen():
    if 'bottle' in collectable:
        imagebutton:
            idle "bottle_idle" at Transform(zoom=0.5)
            action NullAction()
            xpos 0.6 ypos 0.625
            anchor (0.5, 0.5)
    if 'vase' in collectable:
        imagebutton:
            idle "vase_idle" at Transform(zoom=0.5)
            action NullAction()
            xpos 0.45 ypos 0.645
            anchor (0.5, 0.5)
    frame:
        xalign 0.5 yalign 0.9
        vbox:
            text "Use evidence bags to collect the samples"

screen table_collect_evidence_screen():
    if 'bottle' not in collectable and 'vase' not in collectable:
        frame:
            xalign 0.5 yalign 0.9
            vbox:
                text "You've collected all the samples here. Click the back arrow to go back to the main room."
    else:
        if 'bottle' in collectable:
            imagebutton:
                idle "bottle_idle" at Transform(zoom=0.5)
                hover "bottle_hover"
                action [If(default_mouse == 'evidence_bags', Function(remove_collectable, 'bottle'), NullAction())]
                xpos 0.6 ypos 0.625
                anchor (0.5, 0.5)
        if 'vase' in collectable:
            imagebutton:
                idle "vase_idle" at Transform(zoom=0.5)
                hover "vase_hover"
                action [If(default_mouse == 'evidence_bags', Function(remove_collectable, 'vase'), NullAction())]
                xpos 0.45 ypos 0.645
                anchor (0.5, 0.5)
        
        frame:  
            xalign 0.5 yalign 0.9
            vbox:
                text "With the evidence bag selected, click on the items on the table to collect them."


screen close_curtains_screen:
    imagemap:
        idle "curtains"
        hover "curtains_hover"
        hotspot (650, 0, 800, 1080) action Jump("curtains_closed")
    frame:  
        xalign 0.5 yalign 0.9
        vbox:
            text "Click on the curtains to close them."

screen dark_overlay_with_mouse():
    modal True
    default mouse = (0, 0)
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "wall_dark"
        hover "wall_blood"
        hotspot (600, 200, 700, 500) action Return("found_blood")

    add "darkness" pos mouse anchor (0.5, 0.5)

screen blood_marker_screen():
    imagemap:
        idle "wall_blood_marker_idle"
        hover "wall_blood_marker_hover"
        hotspot (340, 150, 315, 345) action Return("marker_placed")

screen swab_sample_screen():
    imagemap:
        idle "wall_blood_marked_idle"
        hover "wall_blood_marked_hover"
        hotspot (200, 200, 1500, 700) action [If(default_mouse=="swab", Return("sample_swabbed"), NullAction())]

screen red_swab_screen():
    imagebutton:
        idle "red_swab_idle" at Transform(zoom=0.35)
        xpos 0.5 ypos 0.45
        anchor (0.5, 0.5)
        action [Show("swab_next_step")]

screen ethanol_screen():
    imagebutton:
        idle "red_swab_idle" at Transform(zoom=0.35)
        hover "red_swab_hover"
        xpos 0.5 ypos 0.45
        anchor (0.5, 0.5)
        action [If(default_mouse == 'ethanol', Return("ethanol added"), Show("swab_next_step"))]

screen reagent_screen():
    imagebutton:
        idle "red_swab_idle" at Transform(zoom=0.35)
        hover "red_swab_hover"
        xpos 0.5 ypos 0.45
        anchor (0.5, 0.5)
        action [If(default_mouse == 'reagent', Return("reagent added"), Show("swab_next_step"))]

screen hydrogen_peroxide_screen():
    imagebutton:
        idle "red_swab_idle" at Transform(zoom=0.35)
        hover "red_swab_hover"
        xpos 0.5 ypos 0.45
        anchor (0.5, 0.5)
        action [If(default_mouse == 'hydrogen_peroxide', Return("hydrogen peroxide added"), Show("swab_next_step"))]
    # imagebutton:
    #     idle "red_swab_idle" at Transform(zoom=0.35)
    #     hover "red_swab_hover"
    #     xpos 0.5 ypos 0.45
    #     anchor (0.5, 0.5)
    #     action NullAction()

screen pink_swab_screen():
    imagebutton:
        idle "pink_swab_idle" at Transform(zoom=0.35)
        # hover "pink_swab_hover"
        xpos 0.5 ypos 0.45
        anchor (0.5, 0.5)
        action NullAction()

screen swab_next_step():
    vbox:
        xalign 0.5
        yalign 0.8
        frame:
            text "Try using "+swab_tools[steps["wall"]]

        frame:
            xalign 0.5
            yalign 0.9
            textbutton "OK" action [Hide("swab_next_step"), Function(set_cursor, '')]

screen new_swab_screen():
    imagemap:
        idle "wall_blood_marked_idle"
        hover "wall_blood_marked_hover"
        hotspot (200, 200, 1500, 700) action [If(default_mouse=="swab", Return("sample_swabbed"), NullAction())]

screen collect_swab_screen():
    if 'swab' in collectable:
        imagebutton:
            idle "red_swab_idle" at Transform(zoom=0.35)
            hover "red_swab_hover"
            xpos 0.5 ypos 0.45
            anchor (0.5, 0.5)
            action [If(default_mouse == 'evidence_bags', Function(remove_collectable, 'swab'), NullAction())]
        frame:  
            xalign 0.5 yalign 0.9
            vbox:
                text "Now pack in evidence bag"
    else:
        frame:
            xalign 0.5 yalign 0.9
            vbox:
                text "You've collected all the samples here. Click the back arrow to go back to the main room."

