label needle:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    $ analyzing["needle"] = True

    show darken_overlay
    show needle at Transform(xpos=0.35, ypos=0.25, zoom=0.5)

    s write "We should take this back to the lab for further analysis."
    
    $ tools["bag"] = True
    $ addToToolbox(["evidence_bag", "tamper_evident_tape"])
    
    call screen toolbox
