label needle:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    $ analyzing["needle"] = True

    show darken_overlay
    show needle at Transform(xpos=0.35, ypos=0.25, zoom=0.5)

    "{color=#2ac975}A needle, likely used to inject drugs. It has a small amount of dried blood on it.{/color}"

    s normal2 "We should take this back to the lab for further analysis."
    
    $ tools["bag"] = True
    $ addToToolbox(["evidence_bag", "tamper_evident_tape"])
    
    call screen toolbox
