"""
Logic for trashcan sequence.
"""

screen trashcan_steroids():
    imagemap:
        idle "trashcan steroids idle"
        hover "trashcan steroids hover"

        # drip
        hotspot (650, 600, 500, 500) action [SetDict(tools, "uv light", True), Jump("steroids")] mouse "hover"

screen trashcan_pillbox():
    imagemap:
        idle "trashcan pills idle"
        hover "trashcan pills hover"

        # drip
        hotspot (800, 450, 500, 500) action [SetDict(tools, "uv light", True), Jump("pillbox_analysis")] mouse "hover"

screen dig():
    imagemap:
        idle "trashcan dig idle"
        hover "trashcan dig hover"

        # paper
        hotspot (376, 22, 1161, 1150) action [Play("sound", "audio/crumple.mp3"), SetDict(tools, "uv light", True), SetDict(analyzing, "pillbox", True), Jump("pillbox")] mouse "hover"

label trashcan:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    show screen back_button_overlay

    $ analyzing["trashcan"] = True
    
    # $ addToToolbox(["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter", "evidence_bag"])



    if analyzed["steroids"] and analyzed["pillbox"]:
        scene trashcan empty
        $ analyzing["trashcan"] = False
        s normal "There's more nothing else to analyze here."
        jump corridor
    elif encountered["uncovered trash"]:
        $ analyzing["pillbox"] = True
        scene trashcan pills idle
        # call 
    elif analyzed["steroids"]:
        scene trashcan dig idle
        call screen dig
    else:
        $ analyzing["steroids"] = True
        scene trashcan steroids idle
        call screen trashcan_steroids
    
    if not encountered["trashcan"]:
        $ encountered["trashcan"] = True
        "New photo added to evidence."
    
    # # $ addToToolbox(["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter", "evidence_bag"])
    # $ addToToolbox(["evidence_bag"])
    # call screen toolbox
transform centered:
    xpos 0.43
    ypos 0.25

label steroids:
    scene trashcan dig idle
    hide screen toolbox
    show darken_overlay
    show steroids small at centered
    # $ analyzing["steroids"] = False
    # $ analyzed["steroids"] = True

    "{color=#88F3FF}It's a vial of steroids, about half full. The label reads <DRUG NAME> XX mL'.{/color}"

    s write "This seems suspicious... we should analyze this vial more closely at the lab."

    hide screen back_button_overlay

    $ tools["bag"] = True
    $ addToToolbox(["evidence_bag", "tamper_evident_tape"])
    call screen toolbox

label pillbox:
    call screen trashcan_pillbox

transform pillbox:
    xpos 0.31
    ypos 0.1
    zoom 0.75

label pillbox_analysis:
    scene trashcan pills idle
    hide screen toolbox_blood
    show darken_overlay
    show pillbox at pillbox
    show capsules at Transform(xpos=0.6, ypos=0.38, zoom=0.7, rotate=0.1)

    "{color=#88F3FF}A pill box filled with assorted tablets. It has a faint odor of garlic and a light yellow powder dusts the insides of the containers.{/color}"

    s write "This seems suspicious... we should analyze this more closely at the lab."

    hide screen back_button_overlay

    $ tools["bag"] = True
    $ addToToolbox(["evidence_bag", "tamper_evident_tape"])
    call screen toolbox


