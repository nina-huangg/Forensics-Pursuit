screen sample():
    add "right hand.png" at right_hand
    hbox:
        xpos 0.36 ypos 0.45
        imagebutton:
            idle "red swab"

            action Jump("sample")

screen footprint():
    imagemap:
        idle "footprint discovered"

        hotspot (842, 625, 190, 183) action Jump("footprint")

screen corridor():
    imagemap:
        idle "corridor"

        hotspot (642, 827, 113, 116) action [Jump("investigation")] mouse "hover"

screen draggables():
    zorder 101
    draggroup:
        drag:
            drag_name "sample"
            child "vertical red swab"
            xpos 0.59 ypos 0.32
            draggable True
            droppable True
            dragged item_dragged
        drag:
            drag_name "tube"
            child "test tube" 
            xpos 0.29 ypos 0.32
            draggable False
            droppable True
            dragged item_dragged

screen more_draggables():
    zorder 101
    draggroup:
        drag:
            drag_name "sample in test tube"
            child "large sample in test tube"
            xpos 0.23 ypos 0.32
            draggable True
            droppable False
            dragged item_dragged
        drag:
            drag_name "bag"
            child "bag"
            xpos 0.51 ypos 0.36
            draggable False
            droppable True
            dragged item_dragged

screen last_draggables():
    zorder 101
    draggroup:
        drag:
            drag_name "bag"
            child "bag"
            xpos 0.51 ypos 0.36
            draggable False
            droppable True
            dragged item_dragged
        drag:
            drag_name "tape"
            child "tape"
            xpos 0.35 ypos 0.5
            draggable True
            droppable True
            dragged item_dragged

screen sample_in_evidence():
    hbox:
        xpos 0.4 ypos 0.21
        imagebutton:
            idle "sample in test tube"

            action Jump("sample_information")

screen left_ui_toolbox_unopened():
    zorder 100
    hbox:
        xpos 0 ypos -55
        imagebutton:
            idle "toolbox"
    
    hbox:
        xpos 0.015 ypos 0.2
        imagebutton:
            idle "casefile"
            
            action Jump("evidence")


screen toolbox():
    zorder 100
    hbox:
        xpos 0.88 ypos 0.02
        imagebutton:
            idle "ethanol"

            action SetVariable("default_mouse", "dropper ethanol")
    
    hbox:
        xpos 0.895 ypos 0.26
        imagebutton:
            idle "reagent"

            action SetVariable("default_mouse", "dropper reagent")

    hbox:
        xpos 0.898 ypos 0.5
        imagebutton:
            idle "hydrogen peroxide"

            action SetVariable("default_mouse", "dropper hydrogen peroxide")
    
    hbox:
        xpos 0.898 ypos 0.74
        imagebutton:
            idle "hungarian red"

            action SetVariable("default_mouse", "hungarian red")
    
    hbox:
        xpos 0 ypos -55
        imagebutton:
            idle "toolbox"
    
    hbox:
        xpos 0.025 ypos 0.22
        imagebutton:
            idle "distilled water"

            action If(default_mouse == "swab", SetVariable("default_mouse", "wet swab"))
    
    hbox:
        xpos 0 ypos 0.49
        imagebutton:
            idle "swab pack"

            action SetVariable("default_mouse", "swab")
    
    hbox:
        xpos 0.17 ypos 0.01
        imagebutton:
            idle "camera"

            action ToggleScreen("footprint", flash) # Need to fix because it hides footprint screen we only want the transition
    
    hbox:
        xpos 0.015 ypos 0.62
        imagebutton:
            idle "evidence_bags"

            action Jump("evidence_bags")

screen trash():
    zorder 101
    hbox:
        xpos 0.785 ypos 0.75
        imagebutton:
            idle "trash"

            action Jump("trash")
