"""
This file has all labels and functions related to the fingerprint and handprint analysis.
It also contains labels related to packaging the fingerprint, handprint, and gin bottle.
"""

label counter:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    $ analyzing["counter"] = True

    show screen back_button_overlay
    scene counter
    
    $ addToToolbox(["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter", "evidence_bag"])
    call screen toolbox

label handprint:
    hide screen back_button_overlay
    if analyzed["handprint"]:
        $ tools["magnetic powder"] = False
        $ analyzing["counter"] = False
        $ analyzing["handprint"] = False
        scene handprint on gel lifter
        s normal "You've already analyzed this print."
        jump corridor
    $ analyzing["handprint"] = True

    scene handprint
    call screen toolbox

label handprint_dusted:
    $ encountered["handprint"] = True
    scene handprint dusted
    "New photo added to evidence."
    call screen toolbox

label handprint_gel:
    scene handprint
    s write "Let's remove the gel lifter carefully now..."
    scene handprint on gel lifter
    s talk "Perfect! Now to package it!"
    call screen toolbox

label handprint_scalebar:
    scene handprint scalebar
    call screen toolbox

label handprint_taped:
    scene handprint taped
    call screen toolbox

label handprint_backing:
    scene handprint backing
    call screen toolbox
    # TODO: add backing card labelling option

label cabinet:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos
    hide screen back_to_cabinet

    $ analyzing["cabinet"] = True

    show screen back_button_overlay

    if analyzed["tylenol"]:
        scene cabinet no tylenol idle
    else:
        scene cabinet idle
 

    $ addToToolbox(["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter", "evidence_bag"])
    call screen toolbox

label fingerprint:
    hide screen back_button_overlay

    if analyzed["fingerprint"]:
        $ tools["magnetic powder"] = False
        scene fingerprint backing
        s normal "You've already analyzed this print."
        jump corridor
    $ analyzing["fingerprint"] = True
    scene fingerprint
    call screen toolbox

label fingerprint_dusted:
    $ encountered["fingerprint"] = True
    scene fingerprint dusted
    "New photo added to evidence."
    call screen toolbox

label fingerprint_scalebar:
    scene fingerprint scalebar
    call screen toolbox
    
label fingerprint_taped:
    scene fingerprint taped
    call screen toolbox

label fingerprint_backing:
    scene fingerprint backing
    call screen toolbox

label packaging:
    $ tools["bag"] = True
    if analyzing["fingerprint"]:
        scene cabinet idle 
        show darken_overlay

        show backing fingerprint at Transform(xpos=0.3, ypos=0.2, zoom=1.6)
    elif analyzing["handprint"]:
        scene counter 
        show darken_overlay
        
        show backing handprint at Transform(xpos=0.34, ypos=0.2, zoom=1.5)
    
    python:
        removal_list = ["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])

    $ addToToolbox(["tube", "tamper_evident_tape"])
    call screen toolbox

label packaging_1:
    python:
        removal_list = ["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])

    hide backing fingerprint
    hide backing handprint
    hide steroids
    hide pillbox
    hide capsules
    hide carpet_sample

    show darken_overlay
    
    if analyzing["fingerprint"]:
        call screen fingerprint_to_bag
    elif analyzing["handprint"]:
        call screen handprint_to_bag
    elif analyzing["carpet_cut"]:
        # scene carpet cut
        call screen carpet_to_bag
    elif analyzing["steroids"]:
        call screen steroids_to_bag
    elif analyzing["pillbox"]:
        call screen pillbox_to_bag
    elif analyzing["needle"]:
        hide needle
        call screen needle_to_bag
    elif analyzing["tylenol"]:
        hide tylenol
        hide capsules
        call screen tylenol_to_bag
    elif analyzing["lower_cabinet"]:
        hide rat poison
        call screen rat_posion_to_bag

    $ tools["bag"] = False
    show evidence bag large at Transform(xpos=0.4, ypos=0.15)
    "Sample successfully placed in bag."
    call screen toolbox

label packaging_2:
    hide evidence bag large
    show darken_overlay
    call screen tape_to_bag

label packaging_3:
    play sound "audio/tape.mp3"
    
    show casefile_evidence_idle at Transform(xpos=0.3, ypos=0.24)
    if analyzing["fingerprint"]:
        "The fingerprint has been added to your evidence."
        $ analyzing["fingerprint"] = False
        $ analyzed["fingerprint"] = True
        $ addToInventory(["fingerprint"])
    elif analyzing["handprint"]:
        "The handprint has been added to your evidence."
        $ analyzing["handprint"] = False
        $ analyzed["handprint"] = True
        $ addToInventory(["handprint"])
    elif analyzing["carpet_cut"]:
        "The carpet has been added to your evidence."
        $ analyzing["carpet_cut"] = False
        $ analyzing["carpet_stain"] = False
        $ analyzed["carpet"] = True
        $ analyzed["carpet_cut packaged"] = True
        # TODO $ addToInventory(["gin"])
    elif analyzing["steroids"]:
        "The steroids have been added to your evidence."
        $ analyzing["steroids"] = False
        $ analyzed["steroids"] = True
        # TODO $ addToInventory(["gin"])
    elif analyzing["pillbox"]:
        "The pillbox has been added to your evidence."
        $ analyzing["pillbox"] = False
        $ analyzed["pillbox"] = True
        # TODO $ addToInventory(["gin"])
    elif analyzing["needle"]:
        "The needle has been added to your evidence."
        # $ analyzing["needle"] = False
        $ analyzed["needle"] = True
        # $ addToInventory(["needle"])
    elif analyzing["tylenol"]:
        "The Tylenol has been added to your evidence."
        $ analyzing["tylenol"] = False
        $ analyzed["tylenol"] = True
        $ packaging = False
        # $ addToInventory(["tylenol"])
    elif analyzing["lower_cabinet"]:
        "The rat poison has been added to your evidence."
        $ analyzed["rat_poison"] = True
        # $ addToInventory(["rat_poison"])
    hide casefile_evidence_idle

    python:
        removal_list = ["evidence_bag", "tube", "tamper_evident_tape"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])


    if analyzing["counter"]:
        jump counter
    elif analyzing["cabinet"]:
        jump cabinet
    elif analyzing["lower_cabinet"]:
        jump lower_cabinet
    elif analyzing["trashcan"]:
        jump trashcan
    elif analyzing["needle"]:
        $ analyzing["needle"] = False
        jump corridor
    elif analyzed["carpet"]:
        jump carpet