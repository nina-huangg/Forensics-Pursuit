init python:
    asked = {
        "splatter_swab": False,
        "footprint_swab": False
    }

label footprint:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    if analyzed["footprint"]:
        $ analyzing["footprint"] = False
        scene footprint enhanced
        "I've already enhanced the footprint."
        "There's nothing more I can do now."
        jump corridor

    $ analyzing["footprint"] = True
    scene footprint

    if encountered["footprint"] == False:
        $ encountered["footprint"] = True
        "{color=#30b002}New photo added to evidence.{/color}"

    call screen toolbox_blood

label splatter:
    $ default_mouse = "default"
    scene splatter
    hide screen casefile_physical
    hide screen casefile_photos

    if analyzed["splatter"] and analyzed["splatter presumptive"] and analyzed["splatter packaged"]:
        $ analyzing["splatter"] = False
        "I've finished analyzing the splatter."
        jump corridor

    if encountered["splatter"] == False:
        $ encountered["splatter"] = True
        "{color=#30b002}New photo added to evidence.{/color}"

    $ analyzing["splatter"] = True
    call screen toolbox_blood

label footprint_swab:
    scene footprint dark
    if asked["footprint_swab"]:
        show red swab at Transform(xpos=0.4, ypos=0.3)
        "{color=#30b002}Sample successfully collected.{/color}"
        jump sample
    
    show clean swab at Transform(xpos=0.4, ypos=0.3)
    "How would you like to collect the sample?"
    menu:
        "Using a wet swab":
            hide clean swab
            show red swab at Transform(xpos=0.4, ypos=0.3)
            "{color=#30b002}Sample successfully collected.{/color}"
            $ asked["footprint_swab"] = True
            jump sample
        "Using a dry swab":
            "Remember, we can't collect dry samples using dry swabs."
            jump footprint

label splatter_swab:
    scene splatter dark
    if asked["splatter_swab"]:
        show red swab at Transform(xpos=0.4, ypos=0.3)
        "{color=#30b002}Sample successfully collected.{/color}"
        jump sample
    
    show clean swab at Transform(xpos=0.4, ypos=0.3)
    "How would you like to collect the sample?"
    menu:
        "Using a wet swab":
            $ asked["splatter_swab"] = True
            hide clean swab
            show red swab at Transform(xpos=0.4, ypos=0.3)
            "{color=#30b002}Sample successfully collected.{/color}"
            jump sample
        "Using a dry swab":
            $ asked["splatter_swab"] = True
            hide clean swab
            show red swab at Transform(xpos=0.4, ypos=0.3)
            "{color=#30b002}Sample successfully collected.{/color}"
            jump sample

label sample:
    "How would you like to proceed?"
    menu:
        "Package the sample":
            jump splatter_alt
        "Run a presumptive test":
            hide red swab
            show screen bloody_swab
            call screen toolbox_presumptive

label trash:
    $ default_mouse = "default"
    hide screen toolbox_presumptive
    "Should I get rid of this swab?"
    menu:
        "Yes":
            hide screen bloody_swab
            hide red swab
            $ player_kastle_meyer_order = []
            hide screen toolbox_presumptive
            if analyzing["footprint"]:
                jump footprint
            elif analyzing["splatter"]:
                jump splatter
        "No":
            show screen bloody_swab
            call screen toolbox_presumptive

label presumptive:
    if default_mouse == "ethanol":
        $ player_kastle_meyer_order.append("e")
        $ default_mouse = "default"
        "{color=#30b002}A drop of ethanol has been added to the sample.{/color}"
    elif default_mouse == "reagent":
        $ player_kastle_meyer_order.append("r")
        $ default_mouse = "default"
        "{color=#30b002}A drop of phenolpthalin has been added to the sample.{/color}"
    elif default_mouse == "hydrogen":
        $ player_kastle_meyer_order.append("h")
        $ default_mouse = "default"
        "{color=#30b002}A drop of hydrogen peroxide has been added to the sample.{/color}"

    if len(player_kastle_meyer_order) > 5:
        $ default_mouse = "default"
        "I think I put in too many drops... I better try again."
        hide screen bloody_swab
        hide red swab
        $ player_kastle_meyer_order = []
        hide screen toolbox_presumptive
        if analyzing["footprint"]:
            jump footprint
        elif analyzing["splatter"]:
            jump splatter

    if player_kastle_meyer_order in valid_kastle_meyer_orders:
        hide screen toolbox_presumptive
        hide screen bloody_swab
        hide red swab
        show pink swab at Transform(xpos=0.4, ypos=0.3)
        "The results of this test show that this substance is indeed blood."
        $ player_kastle_meyer_order = []
        if analyzing["footprint"]:
            $ analyzed["footprint presumptive"] = True
            jump footprint
        elif analyzing["splatter"]:
            $ analyzed["splatter presumptive"] = True
            jump splatter
    else:
        show screen bloody_swab
        call screen toolbox_presumptive

label enhancement:
    $ encountered["footprint enhanced"] = True
    scene footprint enhanced
    "The flooring with the print will be taken back to the lab for further examination."
    $ analyzing["footprint"] = False
    $ analyzed["footprint"] = True
    jump corridor

# Splatter packaging
label splatter_alt:
    if analyzing["splatter"]:
        scene splatter dark
    else:
        scene footprint dark
    show red swab at Transform(xpos=0.4, ypos=0.3)
    $ tools["tube"] = True
    call screen toolbox_packaging

label splatter_packaging_0:
    hide red swab
    call screen sample_to_tube
    show sample test tube at Transform(xpos=0.4, ypos=0.2)
    "{color=#30b002}Sample successfully placed in tube.{/color}"
    call screen toolbox_packaging

label splatter_packaging_1:
    hide sample test tube
    call screen tube_to_bag
    show evidence bag large at Transform(xpos=0.4, ypos=0.15)
    "{color=#30b002}Sample successfully placed in bag.{/color}"
    call screen toolbox_packaging

label splatter_packaging_2:
    hide evidence bag large
    call screen tape_to_bag

label splatter_packaging_3:
    show casefile_evidence_idle at Transform(xpos=0.3, ypos=0.24)
    if analyzing["footprint"]:
        "{color=#30b002}The footprint sample has been added to your evidence.{/color}"
        $ analyzed["footprint packaged"] = True
        hide casefile_evidence_idle
        jump footprint
    else:
        "{color=#30b002}The splatter sample has been added to your evidence.{/color}"
        $ analyzing["splatter"] = False
        $ analyzed["splatter"] = True
        $ analyzed["splatter packaged"] = True
        hide casefile_evidence_idle
        jump splatter
