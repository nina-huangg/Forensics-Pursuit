
label door:
    $ default_mouse = "default"
    scene door
    call screen toolbox_print

label handprint:
    if analyzed["handprint"]:
        scene handprint backing
        "I've already analyzed this print."
        jump corridor
    $ analyzing["handprint"] = True
    scene handprint
    call screen toolbox_print

label handprint_dusted:
    scene handprint dusted
    call screen toolbox_print

label handprint_scalebar:
    scene handprint scalebar
    call screen toolbox_print

label handprint_taped:
    scene handprint taped
    call screen toolbox_print

label handprint_backing:
    scene handprint backing
    call screen toolbox_print
    # TODO: add backing card labelling option

label fingerprint:
    if analyzed["fingerprint"]:
        scene fingerprint backing
        "I've already analyzed this print."
        jump corridor
    $ analyzing["fingerprint"] = True
    scene fingerprint
    call screen toolbox_print

label fingerprint_dusted:
    scene fingerprint dusted
    call screen toolbox_print

label fingerprint_scalebar:
    scene fingerprint scalebar
    call screen toolbox_print

label gin:
    $ default_mouse = "default"
    scene gin        
    "We should take this to the lab for further processing."
    "It could have some useful prints."
    $ analyzing["gin"] = True
    $ tools["bag"] = True
    call screen toolbox_packaging
    
label fingerprint_taped:
    scene fingerprint taped
    call screen toolbox_print

label fingerprint_backing:
    scene fingerprint backing
    call screen toolbox_print

label packaging:
    scene door dark
    $ tools["bag"] = True
    if analyzing["fingerprint"]:
        show backing fingerprint at Transform(xpos=0.3, ypos=0.2, zoom=2)
    elif analyzing["handprint"]:
        show backing handprint at Transform(xpos=0.3, ypos=0.2, zoom=2)
    call screen toolbox_packaging

label packaging_1:
    hide backing fingerprint
    hide backing handprint
    if analyzing["fingerprint"]:
        call screen fingerprint_to_bag
    elif analyzing["handprint"]:
        call screen handprint_to_bag
    elif analyzing["gin"]:
        scene gin removed
        call screen gin_to_bag
    $ tools["bag"] = False
    show evidence bag large at Transform(xpos=0.4, ypos=0.15)
    "Sample successfully placed in bag."
    call screen toolbox_packaging

label packaging_2:
    hide evidence bag large
    call screen tape_to_bag

label packaging_3:
    show casefile_evidence_idle at Transform(xpos=0.3, ypos=0.24)
    "Bag successfully secured."
    if analyzing["fingerprint"]:
        "The fingerprint has been added to your evidence."
        $ analyzing["fingerprint"] = False
        $ analyzed["fingerprint"] = True
    elif analyzing["handprint"]:
        "The handprint has been added to your evidence"
        $ analyzing["handprint"] = False
        $ analyzed["handprint"] = True
    elif analyzing["gin"]:
        "The gin bottle has been added to your evidence"
        $ analyzing["gin"] = False
        $ analyzed["gin"] = True
    hide casefile_evidence_idle
    jump corridor