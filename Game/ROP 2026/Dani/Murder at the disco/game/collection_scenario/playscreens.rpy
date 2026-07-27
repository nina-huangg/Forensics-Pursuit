screen storyboard():
    imagemap:
        idle "storyboard"
        hover "storyboard hover"

        hotspot (628, 695, 580, 390) action Jump("big_splatter")

        hotspot (605, 175, 240, 240) action Jump("left_wall")

        hotspot (1165, 162, 140, 185) action Jump("right_wall")

screen dark_overlay_with_mouse():
    # This is the screen used after pressing the flashlight when analyzing
    # the scissors.
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "left wall idle"
        hover "left wall hover"

        # Handprint
        hotspot (1292, 260, 265, 461) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), SetDict(tools, "gel lifter", True), ToggleScreen("dark_overlay_with_mouse"), Jump("handprint")]

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

screen dark_overlay_with_mouse2():
    # This is the screen used after pressing the flashlight when analyzing
    # the book.
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "baginside idle"
        hover "baginside"

        # Handprint
        hotspot (334, 192, 740, 670) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_with_mouse2"), Jump("fingerprints2")]

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

screen toolbox_print():
    # This is the toolbox used for the fingerprint and the handprint.
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
        xpos 0.88 ypos 0.65
        imagebutton:
            sensitive tools["tape"]
            auto "tape_%s.png" at Transform(zoom=1)
            hovered Notify("tape")
            action [SetDict(tools, "tape", False), SetDict(tools, "backing", True), If(analyzing["handprint"], Jump("handprint_taped"), Jump("fingerprint_taped"))]
    
    hbox:
        xpos 0.885 ypos 0.8
        imagebutton:
            sensitive tools["backing"]
            auto "backing_card_%s.png" at Transform(zoom=0.6)
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
            auto "gel_lifter_%s.png" at Transform(zoom=0.35)
            hovered Notify("gel lifter")
            action [SetDict(tools, "gel lifter", False), SetDict(tools, "packaging", True), Jump("handprint_gel")]

screen toolbox_blood():
    # This is the toolbox used for the bloody footprint and the splatter.
    # It contains the swab and the hungarian red reagent.
    zorder 1
    hbox:
        xpos 0.13 ypos 0.03
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [If(analyzing["splatter"], SetDict(analyzing, "splatter", False), SetDict(analyzing, "footprint", False)), Jump("corridor")]
    hbox:
        xpos 0.77 ypos 0.11
        imagebutton:
            sensitive tools["swab"]
            hovered Notify("swab")
            auto "swab_pack_%s.png" at Transform(zoom=0.8)
            action If(analyzing["footprint"], Jump("footprint_swab"), Jump("splatter_swab"))

screen toolbox_presumptive():
    # This is the toolbox used for the presumptive test.
    zorder 1
    hbox:
        xpos 0.88 ypos 0.02
        imagebutton:
            auto "ethanol_%s.png"
            hovered Notify("ethanol")
            action [SetVariable("default_mouse", "ethanol"), ToggleScreen("toolbox_presumptive")] mouse "dropper"
    
    hbox:
        xpos 0.885 ypos 0.26
        imagebutton:
            auto "reagent_%s.png"
            hovered Notify("reagent")
            action [SetVariable("default_mouse", "reagent"), ToggleScreen("toolbox_presumptive")] mouse "dropper"

    hbox:
        xpos 0.885 ypos 0.5
        imagebutton:
            auto "hydrogen_peroxide_%s.png"
            hovered Notify("hydrogen peroxide")
            action [SetVariable("default_mouse", "hydrogen"), ToggleScreen("toolbox_presumptive")] mouse "dropper"

    hbox:
        xpos 0.898 ypos 0.75
        imagebutton:
            auto "trash_%s"
            hovered Notify("trash")

            action Jump("trash")

screen toolbox_packaging():
    # This is the toolbox used for packaging the evidence.
    zorder 1
    hbox:
        xpos 0.89 ypos 0.13
        imagebutton:
            sensitive tools["tube"]
            hovered Notify("tube")
            auto "tube_%s" at Transform(zoom=0.8)
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", True), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_0"))]
    hbox:
        xpos 0.885 ypos 0.32
        imagebutton:
            sensitive tools["bag"]
            auto "evidence_bag_%s" at Transform(zoom=0.9)
            hovered Notify("evidence bag")
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", False), SetDict(tools, "tamper evident tape", True), If(analyzing["fingerprint"] or analyzing["handprint"] or analyzing["gin"], Jump("packaging_1")), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_1"))]
    
    hbox:
        xpos 0.885 ypos 0.51
        imagebutton:
            sensitive tools["tamper evident tape"]
            hovered Notify("tamper evident tape")
            auto "tamper_evident_tape_%s.png" at Transform(zoom=0.9)
            action [SetDict(tools, "tamper evident tape", False), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_2"), Jump("packaging_2"))]


    