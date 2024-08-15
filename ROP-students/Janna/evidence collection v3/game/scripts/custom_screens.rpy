screen ui():
    zorder 1
    # hbox:
    #     xpos 0.009 ypos 0.1
    #     imagebutton:
    #         auto "toolbox_%s.png" at Transform(zoom=0.5)
    #         hovered Notify("toolbox")
    #         action NullAction()

    hbox:
        # xpos 0.02 ypos 0.3
        xpos 0.02 ypos 0.12
        imagebutton:
            auto "case_file_%s.png" at Transform(zoom=2.5)
            hovered Notify("evidence")
            action Function(close_menu)

# Contents of casefile ---------------------------------------------------------------------------------------
screen casefile():
    zorder 1
    add "casefile_inventory.png"
    text "Evidence Collected" xpos 0.42 ypos 0.15

    text "Physical Evidence" xpos 0.27 ypos 0.7
    text "Photo Evidence" xpos 0.565 ypos 0.7
    hbox:
        xpos 0.2 ypos 0.23
        imagebutton:
            auto "casefile_evidence_%s.png" at Transform(zoom=0.7)
            hovered Notify("collected evidence")
            action [ToggleScreen("casefile"), ToggleScreen("casefile_physical")]
    
    hbox:
        xpos 0.5 ypos 0.27
        imagebutton:
            auto "casefile_photos_%s.png" at Transform(zoom=1.5)
            hovered Notify("photos")
            action [ToggleScreen("casefile"), ToggleScreen("casefile_photos")]
    
screen casefile_physical():
    zorder 0
    add "casefile_inventory.png"
    text "Evidence Collected" xpos 0.42 ypos 0.15
    hbox:
        xpos 0.17 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [ToggleScreen("casefile_physical"), ToggleScreen("casefile")]

    showif analyzed["gin"]:
        hbox:
            xpos 0.2 ypos 0.51
            imagebutton:
                auto "gin %s.png" at Transform(zoom=0.7)
                action Jump("gin_desc")
    
    showif analyzed["handprint"]:
        hbox:
            xpos 0.35 ypos 0.24
            imagebutton:
                auto "handprint %s.png" at Transform(zoom=0.7)
                action Jump("handprint_desc")
    
    showif analyzed["fingerprint"]:
        hbox:
            xpos 0.5 ypos 0.24
            imagebutton:
                auto "fingerprint %s.png" at Transform(zoom=0.7)
                action Jump("fingerprint_desc")
    
    showif analyzed["splatter packaged"]:
        hbox:
            xpos 0.5 ypos 0.51
            imagebutton:
                auto "sample splatter %s.png" at Transform(zoom=0.7)
                action Jump("sample_splatter_desc")

    showif analyzed["footprint packaged"]:
        hbox:
            xpos 0.35 ypos 0.51
            imagebutton:
                auto "sample footprint %s.png" at Transform(zoom=0.7)
                action Jump("sample_footprint_desc")

screen casefile_photos():
    zorder 1
    add "casefile_inventory.png"
    text "Evidence Collected" xpos 0.42 ypos 0.15
    hbox:
        xpos 0.17 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [ToggleScreen("casefile_photos"), ToggleScreen("casefile")]
    
    showif encountered["footprint"]:
        hbox:
            xpos 0.18 ypos 0.22
            imagebutton:
                idle "footprint" at Transform(zoom=0.2)

    showif encountered["footprint enhanced"]:
        hbox:
            xpos 0.4 ypos 0.22
            imagebutton:
                idle "footprint enhanced" at Transform(zoom=0.2)

    showif encountered["handprint"]:
        hbox:
            xpos 0.62 ypos 0.22
            imagebutton:
                idle "handprint dusted" at Transform(zoom=0.2)

    showif encountered["fingerprint"]:
        hbox:
            xpos 0.18 ypos 0.5
            imagebutton:
                idle "fingerprint dusted" at Transform(zoom=0.2)

    showif encountered["splatter"]:
        hbox:
            xpos 0.4 ypos 0.5
            imagebutton:
                idle "splatter" at Transform(zoom=0.2)

    showif encountered["gin"]:
        hbox:
            xpos 0.62 ypos 0.5
            imagebutton:
                idle "gin" at Transform(zoom=0.2)

# Contents of toolbox --------------------------------------------------------------------------------------
screen toolbox_front_corridor():
    zorder 1
    hbox:
        xpos 0.89 ypos 0.084
        imagebutton:
            auto "uv_light_%s.png" at Transform(zoom=0.06)
            hovered Notify("flashlight")
            action NullAction()
    
    hbox:
        xpos 0.88 ypos 0.27
        imagebutton:
            auto "evidence_markers_%s.png" at Transform(zoom=0.06)
            hovered Notify("evidence markers")
            action NullAction()

screen toolbox_print():
    zorder 1
    hbox:
        xpos 0.89 ypos 0.084
        imagebutton:
            sensitive tools["uv light"]
            auto "uv_light_%s.png" at Transform(zoom=0.06)
            hovered Notify("flashlight")
            action [SetDict(tools, "uv light", False), Show("dark_overlay_with_mouse")]
    
    hbox:
        xpos 0.88 ypos 0.27
        imagebutton:
            sensitive tools["magnetic powder"]
            auto "magnetic_powder_%s.png" at Transform(zoom=0.06)
            hovered Notify("magnetic powder")
            action [SetDict(tools, "magnetic powder", False), If(analyzing["handprint"], [SetDict(tools, "gel lifter", True), Jump("handprint_dusted")], [SetDict(tools, "scalebar", True), Jump("fingerprint_dusted")])]
    
    hbox:
        xpos 0.885 ypos 0.5
        imagebutton:
            sensitive tools["scalebar"]
            auto "scalebar_%s.png" at Transform(zoom=0.6)
            hovered Notify("scalebar")
            action [SetDict(tools, "scalebar", False), SetDict(tools, "tape", True), If(analyzing["handprint"], Jump("handprint_scalebar"), Jump("fingerprint_scalebar"))]
        
    hbox:
        xpos 0.88 ypos 0.68
        imagebutton:
            sensitive tools["tape"]
            auto "tape_%s.png" at Transform(zoom=0.2)
            hovered Notify("tape")
            action [SetDict(tools, "tape", False), SetDict(tools, "backing", True), If(analyzing["handprint"], Jump("handprint_taped"), Jump("fingerprint_taped"))]
    
    hbox:
        xpos 0.88 ypos 0.85
        imagebutton:
            sensitive tools["backing"]
            auto "backing_card_%s.png" at Transform(zoom=0.4)
            hovered Notify("backing card")
            action [SetDict(tools, "backing", False), SetDict(tools, "packaging", True), If(analyzing["handprint"], Jump("handprint_backing"), Jump("fingerprint_backing"))]
    
    hbox:
        xpos 0 ypos 0.13
        imagebutton:
            sensitive tools["packaging"]
            auto "casefile_evidence_%s.png" at Transform(zoom=0.3)
            hovered Notify("packaging")
            action [SetDict(tools, "packaging", False), SetDict(tools, "tube", True), Jump("packaging")]
    
    hbox:
        xpos 0 ypos 0.34
        imagebutton:
            sensitive tools["gel lifter"]
            idle "gel lifter.png" at Transform(zoom=0.35)
            hovered Notify("gel lifter")
            action [SetDict(tools, "gel lifter", False), SetDict(tools, "packaging", True), Jump("handprint_gel")]

screen toolbox_blood():
    zorder 1
    hbox:
        xpos 0.13 ypos 0.03
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [If(analyzing["splatter"], SetDict(analyzing, "splatter", False), SetDict(analyzing, "footprint", False)), Jump("corridor")]
    hbox:
        xpos 0.74 ypos 0.11
        imagebutton:
            sensitive tools["swab"]
            auto "swab pack %s.png"
            action If(analyzing["footprint"], Jump("footprint_swab"), Jump("splatter_swab"))

    showif analyzing["footprint"]:
        hbox:
            xpos 0.895 ypos 0.26
            imagebutton:
                auto "hungarian red %s.png"
                action Jump("enhancement")

screen toolbox_presumptive():
    zorder 1
    hbox:
        xpos 0.88 ypos 0.02
        imagebutton:
            auto "ethanol %s.png"
            action [SetVariable("default_mouse", "ethanol"), ToggleScreen("toolbox_presumptive")] mouse "dropper"
    
    hbox:
        xpos 0.895 ypos 0.26
        imagebutton:
            auto "reagent %s.png"
            action [SetVariable("default_mouse", "reagent"), ToggleScreen("toolbox_presumptive")] mouse "dropper"

    hbox:
        xpos 0.898 ypos 0.5
        imagebutton:
            auto "hydrogen peroxide %s.png"
            action [SetVariable("default_mouse", "hydrogen"), ToggleScreen("toolbox_presumptive")] mouse "dropper"

    hbox:
        xpos 0.898 ypos 0.75
        imagebutton:
            idle "trash"

            action Jump("trash")

screen toolbox_packaging():
    zorder 1
    hbox:
        xpos 0.92 ypos 0.13
        imagebutton:
            sensitive tools["tube"]
            idle "tube" at Transform(zoom=0.3)
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", True), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_0"))]
    hbox:
        xpos 0.895 ypos 0.32
        imagebutton:
            sensitive tools["bag"]
            idle "evidence bag" at Transform(zoom=0.8)
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", False), SetDict(tools, "tamper evident tape", True), If(analyzing["fingerprint"] or analyzing["handprint"] or analyzing["gin"], Jump("packaging_1")), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_1"))]
    
    hbox:
        xpos 0.87 ypos 0.53
        imagebutton:
            sensitive tools["tamper evident tape"]
            auto "evident_tape_%s.png" at Transform(zoom=0.06)
            action [SetDict(tools, "tamper evident tape", False), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_2"), Jump("packaging_2"))]
    
screen sample_to_tube():
    draggroup:
        drag:
            drag_name "sample"
            child "red swab cropped"
            xpos 0.28 ypos 0.3
            draggable True
            droppable True
            dragged item_dragged

        drag:
            drag_name "tube"
            child "tube"
            xpos 0.59 ypos 0.29
            draggable True
            droppable True
            dragged item_dragged

screen gin_to_bag():
    draggroup:
        drag:
            drag_name "gin"
            child "gin transparent"
            xpos 0.29 ypos 0.2
            draggable True
            droppable True
            dragged item_dragged

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.54 ypos 0.19
            draggable True
            droppable True
            dragged item_dragged

screen tube_to_bag():
    draggroup:
        drag:
            drag_name "sample test tube"
            child "sample test tube"
            xpos 0.23 ypos 0.2
            draggable True
            droppable True
            dragged item_dragged

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.54 ypos 0.19
            draggable True
            droppable True
            dragged item_dragged


screen fingerprint_to_bag():
    draggroup:
        drag:
            drag_name "fingerprint"
            child "backing fingerprint"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragged item_dragged

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragged item_dragged

screen handprint_to_bag():
    draggroup:
        drag:
            drag_name "fingerprint"
            child "backing handprint"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragged item_dragged

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragged item_dragged

screen tape_to_bag():
    draggroup:
        drag:
            drag_name "tape"
            child "tamper evident tape"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragged item_dragged
        
        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragged item_dragged

# Backgrounds ---------------------------------------------------------------------------------------------

screen front_corridor():
    imagemap:
        if not analyzed["gin"]:
            idle "front corridor"
            hover "front corridor hover"
        else:
            idle "no gin"
            hover "no gin hover"

        # Door
        hotspot (890, 115, 368, 714) action [ToggleScreen("ui"), SetDict(tools, "uv light", True), SetDict(encountered, "door", True), Jump("door")] mouse "hover"

        # Footprint
        hotspot (1063, 865, 166, 163) action [ToggleScreen("ui"), SetDict(tools, "swab", True), Jump("footprint")] mouse "hover"

        # Gin
        showif not analyzed["gin"]:
            hotspot (602, 494, 159, 160) action [ToggleScreen("ui"), Jump("gin")] mouse "hover"

        # Splatter
        hotspot (465, 960, 209, 109) action [ToggleScreen("ui"), SetDict(tools, "swab", True), Jump("splatter")] mouse "hover"

        showif encountered["door"]:
            add "marker 4" at Transform(xpos=0.63, ypos=0.74, zoom=0.3)
        
        showif encountered["splatter"]:
            add "marker 2" at Transform(xpos=0.32, ypos=0.83, zoom=0.33)
        
        showif encountered["footprint"]:
            add "marker 1" at Transform(xpos=0.54, ypos=0.77, zoom= 0.32)
            

screen bloody_swab():
    imagebutton:
        idle "red swab" at Transform(xpos=0.4, ypos=0.3)
        action Jump("presumptive")

screen dark_overlay_with_mouse():
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "door flashlight idle"
        hover "door flashlight hover"

        # Handprint
        hotspot (601, 368, 197, 208) action [SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_with_mouse"), Jump("handprint")]

        # Fingerprint
        hotspot (419, 351, 99, 104) action [SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_with_mouse"), Jump("fingerprint")]

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)
