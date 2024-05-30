
screen footprint_tools():
    zorder 100
    hbox:
        xpos 0.87 ypos 0.025
        imagebutton:
            idle "electrostatic dust print lifter"
            hover "electrostatic dust print lifter"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("electrostatic")
            sensitive tools["electrostatic dust print lifter"]
    
    hbox:
        xpos 0.9 ypos 0.19
        imagebutton:
            idle "conductive film"
            hover "conductive film"
            hover_sound "audio/sfx-pichoop.wav"
            
            action Jump("conductive_film")
            sensitive tools["conductive film"]

    hbox:
        xpos 0.87 ypos 0.33
        imagebutton:
            idle "lint roller"
            hover "lint roller"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("lint_roller")
            sensitive tools["lint roller"]

 
screen expand_tools():
    zorder 100
    hbox:
        xpos 0.888 ypos 0.415
        imagebutton:
            idle "scalebar_idle"
            hover "scalebar_hover"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("backing")
            sensitive tools["scalebar"]

    hbox:
        xpos 0.890 ypos 0.590
        imagebutton:
            idle "lifting_backing_idle"
            hover "lifting_backing_hover"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("backing_2")
            sensitive tools["backing card"]

    hbox:
        xpos 0.037 ypos 0.1
        imagebutton:
            idle "evident_tape_idle"
            hover "evident_tape_hover"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("tape")
            sensitive tools["tape"]

    hbox:
        xpos 0.048 ypos 0.238
        imagebutton:
            idle "evidence_bags_idle"
            hover "evidence_bags_hover"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("bag")
            sensitive tools["bag"]

    hbox:
        xpos 0.895 ypos 0.238
        imagebutton:   
            idle "magnetic_powder"
            hover "hover_magnetic_powder"
            hover_sound "audio/sfx-pichoop.wav"
            
            action Jump("scalebar")
            sensitive tools["dust"]

    hbox:
        xpos 0.89 ypos 0.03
        imagebutton:
            idle "uv_light_idle"
            hover "uv_light_hover"
            hover_sound "audio/sfx-pichoop.wav"

            action Jump("uv_light")
            sensitive tools["uv light"]


screen opening_screen():
    imagemap:
        idle "car inside.png"
        hover "car inside.png"
        ground "car inside.png"

        # Footprint next to the brakes
        hotspot (617, 671, 118, 90) action Jump("enter_splash_screen") mouse "hover" hover_sound "audio/sfx-pichoop.wav"

        # Steering wheel
        hotspot (699, 236, 164, 262) action Jump("another_label") mouse "hover" hover_sound "audio/sfx-pichoop.wav"

        # Arrow
        hotspot (300, 791, 297, 258) action Call("car_side") mouse "move" hover_sound "audio/sfx-pichoop.wav"

screen car_side():
    imagemap:
        idle "car side"
        hover "car side"
        ground "car side"

        hotspot (1418, 498, 297, 230) action Call("car_back_unopened") mouse "move" hover_sound "audio/sfx-pichoop.wav"

        hotspot (601, 379, 348, 376) action Call("car_inside") mouse "move" hover_sound "audio/sfx-pichoop.wav"

screen car_back_unopened():
    imagemap:
        idle "car back unopened"
        hover "car back unopened"
        ground "car back unopened"

        hotspot (570, 362, 834, 374) action Call("car_back_opened") mouse "hover" hover_sound "audio/sfx-pichoop.wav"

        hotspot (242, 17, 259, 943) action Call("car_side") mouse "move" hover_sound "audio/sfx-pichoop.wav"

screen car_back_opened():
    imagemap:
        idle "car back opened"
        hover "car back opened"
        ground "car back opened"

screen luminol():
    imagemap:
        idle "car back opened luminol"
        hover "car back opened luminol found"
        ground "car back opened luminol"

        hotspot (605, 566, 353, 107) action Jump("blood_found") mouse "hover" hover_sound "audio/sfx-pichoop.wav"

screen wheel_flashlight():
    imagemap:
        idle "wheel flashlight"
        hover "wheel flashlight print"
        ground "wheel flashlight"

        hotspot (640, 159, 58, 80) action Jump("dust") mouse "hover" hover_sound "audio/sfx-pichoop.wav"

screen wheel_print_found():
    imagemap:
        idle "wheel print found"
        hover "wheel print found"
        ground "wheel print found"


screen footprint_untouched():
    imagemap:
        idle "footprint untouched"

screen footprint_covered():
    imagemap:
        idle "footprint covered"

screen footprint_flattened():
    imagemap:
        idle "footprint flattened"

screen footprint_acquired():
    imagemap:
        idle "footprint acquired"

screen wheel_flashlight_print():
    imagemap:
        idle "wheel flashlight print"

screen wheel_print_dusted():
    imagemap:
        idle "wheel print dusted"
        hover "wheel print dusted"
        ground "wheel print dusted"

screen wheel_zoomed():
    imagemap:
        idle "wheel zoomed in"

screen wheel_zoomed_scalebar():
    imagemap:
        idle "wheel zoomed in scalebar"

screen wheel_backing():
    imagemap:
        idle "wheel backing"

screen wheel():
    imagemap:
        idle "wheel"