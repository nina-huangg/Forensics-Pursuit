screen cabinet_rat_poison:
    imagemap:
        idle "lower cabinet idle"
        hover "lower cabinet hover"

        # rat poison
        hotspot (653, 0, 756, 719) action Jump("rat_poison") mouse "hover"

label lower_cabinet:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    $ analyzing["lower_cabinet"] = True

    show screen back_button_overlay

    if analyzed["rat_poison"]:
        scene lower cabinet no poison
        s normal2 "There's nothing else to analyze here."
        $ analyzing["lower_cabinet"] = False
        jump corridor
    else:
        call screen cabinet_rat_poison

label rat_poison:
    hide screen back_button_overlay
    scene lower cabinet no poison
    show darken_overlay
    show rat poison at Transform(xpos=0.35, ypos=0.1)

    "{color=#2ac975}It's a bag of rat poison that's half full. The crumbly pellets are a dark green, giving off a garlic-y odour.{/color}"

    s normal2 "This seems suspicious... we should analyze this more closely at the lab."

    $ tools["bag"] = True
    $ addToToolbox(["evidence_bag", "tamper_evident_tape"])
    call screen toolbox