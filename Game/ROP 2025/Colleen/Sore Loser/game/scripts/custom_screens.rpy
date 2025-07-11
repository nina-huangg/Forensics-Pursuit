"""
This file contains all custom screens used in the game.
"""

screen ui():
    # This is the case file displayed on the top left corner of the screen when the player is in the corridor.
    zorder 2

    hbox:
        xpos 0.02 ypos 0.12
        imagebutton:
            auto "case_file_%s.png" at Transform(zoom=2.5) mouse "pointer"
            hovered Notify("evidence")
            action Function(close_menu)
    
    # text "Evidence" xpos 0.023 ypos 0.24 size 32
        

# Contents of casefile ---------------------------------------------------------------------------------------
screen casefile():
    # This is screen displayed after the player clicks on the case file.
    # It allows the player to choose between the physical evidence and the photos.
    zorder 1
    modal True
    add "casefile_inventory.png"
    text "Evidence Collected" xpos 0.42 ypos 0.15

    text "Physical Evidence" xpos 0.27 ypos 0.7
    text "Photo Evidence" xpos 0.565 ypos 0.7

    hbox:
        xpos 0.17 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action Function(close_menu)

    hbox:
        xpos 0.2 ypos 0.23
        imagebutton:
            auto "casefile_evidence_%s.png" at Transform(zoom=0.7) mouse "pointer"
            hovered Notify("collected evidence")
            action [ToggleScreen("casefile"), ToggleScreen("casefile_physical")]
    
    hbox:
        xpos 0.5 ypos 0.27
        imagebutton:
            auto "casefile_photos_%s.png" at Transform(zoom=1.5)
            hovered Notify("photos")
            action [ToggleScreen("casefile"), ToggleScreen("casefile_photos")]
    
    
screen casefile_physical():
    # This is the screen displayed when the player clicks on the physical evidence.
    # It shows all evidence collected. When the player clicks on a piece of evidence,
    # the description of the evidence is displayed on the bottom of the screen.

    # NOTE: This screen will not be used in future iterations of the game. This
    # is a placeholder screen. The inventory that Vivian created will be used instead. 
    zorder 0
    modal True
    add "casefile_inventory.png" at Transform(yzoom=1.1)
    text "Evidence Collected" xpos 0.42 ypos 0.15

    hbox:
        xpos 0.17 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [ToggleScreen("casefile_physical"), SetVariable("evidence_desc", ""), ToggleScreen("casefile")]
    
    showif analyzed["fingerprint"]:
        hbox:
            # xpos 0.5 ypos 0.24
            xpos 0.2 ypos 0.24
            imagebutton:
                auto "fingerprint %s.png" at Transform(zoom=0.7)
                action SetVariable("evidence_desc", "This is the fingerprint we gathered from the light switch next to the counter knob.")
    
    showif analyzed["handprint"]:
        hbox:
            xpos 0.35 ypos 0.24
            imagebutton:
                auto "handprint %s.png" at Transform(zoom=0.7)
                action SetVariable("evidence_desc", "This is the handprint we gathered from the counter. It is slightly degraded.")

    showif analyzed["carpet packaged"]:
        hbox:
            xpos 0.5 ypos 0.24
            imagebutton:
                auto "sample carpet %s.png" at Transform(zoom=0.7)
                action If(analyzed["carpet presumptive"], SetVariable("evidence_desc", "This is blood gathered from the carpet."), SetVariable("evidence_desc", "This is the red substance gathered from the carpet. It is unknown what this substance is at the moment."))

    showif analyzed["drip packaged"]:
        hbox:
            xpos 0.65 ypos 0.24
            imagebutton:
                auto "sample drip %s.png" at Transform(zoom=0.7)
                action If(analyzed["drip presumptive"], SetVariable("evidence_desc", "This is blood gathered from the drip beside the table."), SetVariable("evidence_desc", "This is the red substance gathered from the drip beside the table. It is unknown what this substance is at the moment."))
    
    # showif analyzed["gin"]:
    #     hbox:
    #         xpos 0.2 ypos 0.51
    #         imagebutton:
    #             auto "gin %s.png" at Transform(zoom=0.7)
    #             action SetVariable("evidence_desc", "This is the gin bottle we recovered from the table.")

    text "[evidence_desc]" xalign 0.5 ypos 0.79 size 30 xsize 900 color "#fff"


screen casefile_photos():
    # This is the screen displayed when the player clicks on the photos. It shows
    # photos of all evidence collected.

    # NOTE: This screen will not be used in future iterations of the game. This
    # is a placeholder screen. The inventory that Vivian created will be used instead. 
    zorder 1
    modal True
    add "casefile_inventory.png"
    text "Evidence Collected" xpos 0.42 ypos 0.15
    hbox:
        xpos 0.17 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [ToggleScreen("casefile_photos"), ToggleScreen("casefile")]
    
    showif encountered["carpet"]:
        hbox:
            xpos 0.18 ypos 0.22
            imagebutton:
                idle "carpet" at Transform(zoom=0.2)

    showif encountered["carpet enhanced"]:
        hbox:
            xpos 0.4 ypos 0.22
            imagebutton:
                idle "carpet enhanced" at Transform(zoom=0.2)

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

    showif encountered["drip"]:
        hbox:
            xpos 0.4 ypos 0.5
            imagebutton:
                idle "drip" at Transform(zoom=0.2)

    # showif encountered["gin"]:
    #     hbox:
    #         xpos 0.62 ypos 0.5
    #         imagebutton:
    #             idle "gin" at Transform(zoom=0.2)

# Contents of toolbox --------------------------------------------------------------------------------------
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
    # This is the toolbox used for the bloody carpet and the drip.
    # It contains the swab and the hungarian red reagent.
    zorder 1
    hbox:
        xpos 0.13 ypos 0.03
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [If(analyzing["drip"], SetDict(analyzing, "drip", False)), If(analyzing["carpet_stain"], SetDict(analyzing, "carpet_stain", False)), If(analyzing["carpet_cut"], SetDict(analyzing, "carpet_cut", False)), Jump("corridor")]
    hbox:
        xpos 0.77 ypos 0.11
        imagebutton:
            sensitive tools["swab"]
            hovered Notify("swab")
            auto "swab_pack_%s.png" at Transform(zoom=0.8)
            action [If(analyzing["drip"], Jump("drip_swab")), If(analyzing["carpet_stain"], Jump("carpet_swab"))]

    # scissors for carpet
    showif analyzing["carpet_stain"] or analyzing["carpet_cut"]:
        hbox:
            xpos 0.895 ypos 0.26
            imagebutton:
                hovered Notify("scissors")
                auto "hungarian_red_%s.png"
                action Jump("cutting")

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
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", True), If(analyzing["drip"] or analyzing["carpet_stain"] or analyzing["carpet_cut"], Jump("drip_packaging_0"))]
    hbox:
        xpos 0.885 ypos 0.32
        imagebutton:
            sensitive tools["bag"]
            auto "evidence_bag_%s" at Transform(zoom=0.9)
            hovered Notify("evidence bag")
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", False), SetDict(tools, "tamper evident tape", True), If(analyzing["fingerprint"] or analyzing["handprint"] or analyzing["gin"], Jump("packaging_1")), If(analyzing["drip"] or analyzing["carpet_stain"] or analyzing["carpet_cut"], Jump("drip_packaging_1"))]
    
    hbox:
        xpos 0.885 ypos 0.51
        imagebutton:
            sensitive tools["tamper evident tape"]
            hovered Notify("tamper evident tape")
            auto "tamper_evident_tape_%s.png" at Transform(zoom=0.9)
            action [SetDict(tools, "tamper evident tape", False), If(analyzing["drip"] or analyzing["carpet_stain"] or analyzing["carpet_cut"], Jump("drip_packaging_2"), Jump("packaging_2"))]

# Drag and drop screens -------------------------------------------------------------------------------

screen sample_to_tube():
    draggroup:
        drag:
            drag_name "sample"
            child "red swab cropped"
            xpos 0.28 ypos 0.3
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

        drag:
            drag_name "tube"
            child "tube"
            xpos 0.59 ypos 0.29
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

# screen gin_to_bag():
#     draggroup:
#         drag:
#             drag_name "gin"
#             child "gin transparent"
#             xpos 0.29 ypos 0.2
#             draggable True
#             droppable True
#             dragging item_dragging_package
#             dragged item_dragged_package

#         drag:
#             drag_name "bag"
#             child "evidence bag large"
#             xpos 0.54 ypos 0.19
#             draggable True
#             droppable True
#             dragging item_dragging_package
#             dragged item_dragged_package

screen carpet_to_bag():
    draggroup:
        drag:
            drag_name "carpet_sample"
            child "carpet_sample"
            xpos 0.15 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.54 ypos 0.19
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen steroids_to_bag():
    draggroup:
        drag:
            drag_name "steroids"
            child "steroids small"
            xpos 0.3 ypos 0.3
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.54 ypos 0.19
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen pillbox_to_bag():
    draggroup:
        drag:
            drag_name "pillbox"
            child "pillbox_small"
            xpos 0.15 ypos 0.35
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.54 ypos 0.19
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen tube_to_bag():
    draggroup:
        drag:
            drag_name "sample test tube"
            child "sample test tube"
            xpos 0.23 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.54 ypos 0.19
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen fingerprint_to_bag():
    draggroup:
        drag:
            drag_name "fingerprint"
            child "backing fingerprint"
            xpos 0.15 ypos 0.3     
            transform zoom 0.002
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

screen handprint_to_bag():
    draggroup:
        drag:
            drag_name "fingerprint"
            child "backing handprint"
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

screen needle_to_bag():
    draggroup:
        drag:
            drag_name "needle"
            child "needle small"
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

screen tylenol_to_bag():
    draggroup:
        drag:
            drag_name "tylenol"
            child "tylenol"
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

screen rat_posion_to_bag():
    draggroup:
        drag:
            drag_name "rat poison"
            child "rat poison"
            xpos 0.2 ypos 0.25
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



# Backgrounds -------------------------------------------------------------------------------------------

screen apt():
    # This is the screen displayed when the player is in the corridor.

    imagemap:
        if not analyzed["carpet_cut packaged"]:
            idle "apt"
            hover "apt hover"
        else:
            idle "apt cut"
            hover "apt cut hover"

        # drip
        hotspot (1050, 710, 200, 150) action [SetDict(tools, "swab", True), SetDict(encountered, "drip", True), Jump("drip")] mouse "hover"

        # carpet stain
        hotspot (1500, 760, 200, 200) action [SetDict(tools, "swab", True), Jump("carpet")] mouse "hover"

        showif not analyzed["needle"]:
            # needle
            hotspot (770, 390, 200, 200) action [Jump("needle")] mouse "hover"

        # counter
        hotspot (1250, 250, 450, 150) action [SetDict(tools, "uv light", True), SetDict(encountered, "counter", True), Jump("counter")] mouse "hover"

        # cabinet
        hotspot (1230, 0, 600, 130) action [SetDict(tools, "uv light", True), SetDict(encountered, "cabinet", True), Jump("cabinet")] mouse "hover"

        # lower cabinet
        hotspot (1400, 373, 235, 357) action [SetDict(tools, "uv light", True), Jump("lower_cabinet")] mouse "hover"

        # trashcan
        hotspot (0, 640, 100, 380) action [SetDict(tools, "uv light", True), Jump("trashcan")] mouse "hover"

        showif encountered["drip"]:
            add "marker 4" at Transform(xpos=0.63, ypos=0.74, zoom=0.3)
        
        showif encountered["carpet"]:
            add "marker 2" at Transform(xpos=0.9, ypos=0.83, zoom=0.33)
        
        showif encountered["counter"]:
            add "marker 1" at Transform(xpos=0.7, ypos=0.23, zoom= 0.32)
    
    showif not analyzed["needle"]:
        add "needle" at Transform(xpos=0.41, ypos=0.4, zoom=0.1) 


screen bloody_swab():
    # This is the screen used to allow the player to add drops of chemicals
    # to the swab during the presumptive test.
    imagebutton:
        idle "red swab" at Transform(xpos=0.4, ypos=0.3)
        action Jump("presumptive")

screen dark_overlay_counter():
    # This is the screen used after pressing the flashlight when analyzing
    # the counter.
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "counter flashlight idle"
        hover "counter flashlight hover"

        # Handprint
        hotspot (450, 730, 500, 500) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_counter"), Jump("handprint")] 

        # # Fingerprint
        # hotspot (419, 351, 99, 104) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_with_mouse"), Jump("fingerprint")]

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

screen dark_overlay_cabinet():
    # This is the screen used after pressing the flashlight when analyzing
    # the counter.
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    showif not analyzed["tylenol"]:
        imagemap:
            idle "cabinet flashlight idle"
            hover "cabinet flashlight hover"

            # Fingerprint
            hotspot (200, 800, 600, 600) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_cabinet"), Jump("fingerprint")] mouse "hover"
    
    showif analyzed["tylenol"]:
        imagemap:
            idle "cabinet no tylenol flashlight idle"
            hover "cabinet no tylenol flashlight hover"

            # Fingerprint
            hotspot (200, 800, 600, 600) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_cabinet"), Jump("fingerprint")] mouse "hover"

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)