default dressing_hover = None
init python:
    # Make RestartInteraction() available in screen code:
    from renpy.exports import restart_interaction as RestartInteraction

init python:

    # --------------- toolbox things
    def item_dragging(drags):
        """When you pick up a drag, show a grabbing hand."""
        global default_mouse
        default_mouse = "hand_grab"

    def item_dragged(drags, drop):
        """When you drop onto a valid droppable, clean up and reset the cursor."""
        global default_mouse
        default_mouse = "hand"
        if not drop:
            # wasn’t dropped on a droppable target
            return
        # Hide all three screens so the next label can run
        renpy.hide_screen("sample_to_tube")
        renpy.hide_screen("tube_to_bag")
        renpy.hide_screen("tape_to_bag")
        default_mouse = "default"
        return True

screen house_interact():
    modal True
    on "show" action If(
        all([
            analyzed.get("lipstick", False),
            analyzed.get("water",    False),
            analyzed.get("smoke",    False),
            analyzed.get("rack",     False),
        ]),
        Jump("lab_congratulations"),
        NullAction()
    )

    showif analyzed["smoke"]:
            add "marker 1" at Transform(xpos=500, ypos=900, zoom= 0.32)

    showif analyzed["rack"]:
            add "marker 2" at Transform(xpos=1200, ypos=900, zoom= 0.32)

    if not analyzed["smoke"]:
        imagebutton:
            idle      "images/smoke_scene/smoke_machine.png"
            hover   "images/smoke_scene/smoke_machine_hover.png"
            at Transform(zoom=0.4)
            xpos      400 ypos 675
            sensitive not got_smoke
            action    [
                SetVariable("got_smoke", True), 
                Hide("house_interact"),
                Jump("smoke")
            ]
            # 
        
        
    imagebutton:
        idle      "images/rack_scene/rack2_powder.png"
        hover   "images/rack_scene/rack2_powder_hover.png"
        at Transform(zoom=0.7)
        xpos      850 ypos 450
        sensitive not got_rack
        action    [
            SetVariable("got_rack", True), 
            Hide("house_interact"),
            Jump("rack")
        ]
        

    imagebutton:
        idle  "arrow_idle.png"
        hover "arrow_hover.png"
        at Transform(zoom=0.05)
        xpos 1500 ypos 900
        action [ Function(renpy.jump, "backstage"), Hide("house_interact") ]
    
# screen for dressing room wide shot to add waterbottle, makeup
screen dressing_interact():
    modal True
    
    on "show" action If(
        all([
            analyzed.get("lipstick", False),
            analyzed.get("water",    False),
            analyzed.get("smoke",    False),
            analyzed.get("rack",     False),
        ]),
        Jump("lab_congratulations"),
        NullAction()
    )

    showif analyzed["lipstick"]:
            add "marker 3" at Transform(xpos=500, ypos=570, zoom= 0.32)

    showif analyzed["water"]:
            add "marker 4" at Transform(xpos=800, ypos=540, zoom= 0.32)
            
    imagebutton:
        idle      "water"
        hover   "water_hover"
        at Transform(zoom=0.3)
        xpos      800 ypos 340
        sensitive not got_water
        action    [
            Hide("dressing_interact"),
            Jump("water")
        ]
        
    if not analyzed["lipstick"]:
        imagebutton:
            idle      "lipstick"
            hover   "lipstick_hover"
            at Transform(zoom=0.4)
            xpos      500 ypos 470
            sensitive not got_makeup
            action    [
                Hide("dressing_interact"),
                Jump("lipstick")
            ]
        
    imagebutton:
        auto "back_button_%s.png" at Transform(zoom=0.35)
        xpos 1700 ypos 900
        action [Hide("dressing_interact"),
            Jump("backstage"),]






# --------------------------------- large view dressing room -------------------------- #
# just has option to get closer to the table for now and look
transform full_screen_crop_top:
    xalign 0.5
    yalign 1.0
    fit "cover"
    
transform full_screen:
    xpos 0     ypos 0
    xsize config.screen_width
    ysize config.screen_height
    
screen dressing_nav():
    modal True
    imagemap:
        at full_screen_crop_top
        ground "images/backstage/bg dressing_room_wide.JPG"
        hover  "images/backstage/bg dressing_room_wide_hover.JPG"

        hotspot (1610, 2207, 2338, 314) action [Hide("dressing_nav"), Jump("desk")]

        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=1)
            xpos 4912 ypos 3100
            action [Hide("dressin_nav"),
                Function(renpy.jump, "house"),]


label lab_congratulations:
    scene black with fade
    jump finished


screen tape_to_bag():
    draggroup:
        drag:
            drag_name "tape"
            child "tamper evident tape"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
