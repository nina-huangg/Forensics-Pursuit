init python:
    def dragged_func(dragged_items, dropped_on):
        if dropped_on is not None:
            if dragged_items[0].drag_name == "black" and dropped_on.drag_name == "gray":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.jump("shoeprint_lifter_complete")
    
    def return_mouse_pos():
        return renpy.get_mouse_pos()

    config.layers.append("overlay")

screen opening_screen():
    imagemap:
        idle "background_idle"
        hover "background_hover"
        ground "background_idle"
        hotspot (1491, 198, 356, 102) action Jump("enter_splash_screen")

screen splash_screen():
    key "K_SPACE" action Jump("intro")

screen entrance_screen():
    imagemap:
        idle "front"
        hover "front_hover"
        ground "front"
        hotspot (768, 209, 346, 656) action Jump("room")
    frame:
        xalign 0.5 yalign 0.9
        vbox:
            text "Click the door to enter the house"

screen inspect_room():
    imagemap:
        idle "room_side"
        hover "room_side_hover"
        ground "room_side"
        hotspot (1140, 710, 800, 500) action Jump("examine_shoeprint")
        hotspot (60, 470, 720, 600) action Jump("center")

transform toolbox_small():
    zoom 0.06

transform tools_small():
    zoom 0.1

screen shoeprint_toolbox_contracted():
    hbox:
        xpos 0.03 ypos 0.02
        imagebutton:
            idle "toolbox" at toolbox_small
            hover "toolbox_hover"
            action Jump("shoeprint_toolbox")
    frame:
        xalign 0.5 yalign 0.8
        vbox:
            text "Click on the toolbox for equipment to analyze this shoeprint."

screen shoeprint_toolbox_expanded():
    zorder 10
    hbox:
        xpos 0.03 ypos 0.02
        imagebutton:
            idle "toolbox" at toolbox_small
            hover "toolbox_hover"
            action Jump("shoeprint_toolbox")

    hbox:
        xpos 0.85 ypos 0.01
        imagebutton:
            idle "duster" at tools_small
            hover "duster_hover" 
            hovered Notify("duster")
            unhovered Notify('')
            action Jump('shoeprint_duster')

    hbox:
        xpos 0.85 ypos 0.25
        imagebutton:   
            idle "lifter" at tools_small
            hover "lifter_hover"
            hovered Notify("lifter")
            unhovered Notify('')
            action Jump('drag_lifter')
    
    hbox:
        xpos 0.85 ypos 0.5
        imagebutton:
            idle "flattener" at tools_small
            hover "flattener_hover" 
            hovered Notify("flattener")
            unhovered Notify('')
            action Jump('shoeprint_flattener')

    hbox:
        xpos 0.85 ypos 0.75
        imagebutton:
            idle "laminate" at tools_small
            hover "laminate_hover"
            hovered Notify("laminate")
            unhovered Notify('')
            action Jump('shoeprint_laminate')

transform checkmark:
    zoom 0.3

screen update_dust():
    imagemap:
        idle "room_floor_[dust]"
        hover "room_floor_hover_[dust]"
        hotspot (610, 600, 700, 550) action Return("next_dust_level")

    imagebutton:
        idle "checkmark" at checkmark
        hover "checkmark_hover"
        action Return("complete_dusting")
        xpos 1400
        ypos 850

screen lifter_drag_drop:
    draggroup:
        drag:
            align(0.3, 0.5)
            drag_raise True
            drag_name "black"
            dragged dragged_func
            image "/images/shoeprint_toolbox/lifter_sheet.png" xysize (300, 400)
        drag:
            align(0.49, 0.88)
            drag_raise True
            drag_name "gray"
            dragged dragged_func
            image Solid((165, 165, 165, 128)) xysize (300, 400)

screen flattener:
    imagemap:
        idle "room_floor_lifter"
        hover "room_floor_lifter_hover"
        hotspot (770, 580, 450, 450) action Jump("shoeprint_flattener_complete")

screen laminate_screen():
    imagebutton:
        idle "shoeprint_lifted" at shoeprint_lifted 
        hover "shoeprint_lifted_hover"  
        action Jump("shoeprint_complete")
        xpos 0.5
        ypos 0.5
        anchor (0.5, 0.5)

screen examine_center():
    imagemap:
        idle "room_front"
        hover "room_front_hover"
        hotspot (450, 5, 900, 400) action Jump("examine_wall")

screen close_curtains:
    imagemap:
        idle "curtains"
        hover "curtains_hover"
        hotspot (650, 0, 800, 1080) action Jump("curtains_closed")
    frame:
        xalign 0.5 yalign 0.9
        vbox:
            text "Click on the curtains to close them."

screen blood_toolbox_contracted():
    hbox:
        xpos 0.03 ypos 0.02
        imagebutton:
            idle "toolbox" at toolbox_small
            hover "toolbox_hover"
            action Jump("blood_toolbox")
    frame:
        xalign 0.5 yalign 0.8
        vbox:
            text "Click on the toolbox for equipment to analyze the wall."

screen blood_toolbox_expanded():
    zorder 10
    hbox:
        xpos 0.03 ypos 0.02
        imagebutton:
            idle "toolbox" at toolbox_small
            hover "toolbox_hover"
            action Jump("blood_toolbox")

    hbox:
        xpos 0.85 ypos 0.01
        imagebutton:
            idle "uv_light_idle" at tools_small
            hover "uv_light_hover" 
            hovered Notify("uv_light")
            unhovered Notify('')
            action Jump('blood_uv_light')

    
screen dark_overlay_with_mouse():
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "wall_als"
        hover "wall_als_hover"
        hotspot (600, 200, 700, 500) action Jump("presumptive_test")

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

