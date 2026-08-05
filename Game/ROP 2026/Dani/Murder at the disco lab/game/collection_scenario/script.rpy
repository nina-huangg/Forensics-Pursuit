init python:
    import json

    tools = load_items("jsons/toolbox.json")

    evids = load_items("jsons/evidence.json")
    evidences = []
    freezing = False

    snipped = False
    swab = False
    scalebar = False
    tape = False
    step = 0

define n = Character(name=("Nina"), image="nina")


label start:
    scene hallway
    show nina normal1 at left
    n "Hello detective. I'm detective Nina. Welcome to the lab."
    show nina thinknote1 at left
    n "You're gonna need to analyze all the evidence you collected at the crime scene."
    jump game

label game:
    hide nina normal1
    hide nina thinknote1
    show screen inventory
    call screen hallway
    
label data_analysis_lab:
    $ location = ""
    hide screen full_inventory
    show screen back_button_screen('hallway')
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen
    hide screen full_inventory
    show screen back_button_screen('data_analysis_lab')
    call screen afis_screen

label scissors_use_label:
    "Let's take a snip of the swab for evidence..."
    show snip0 zorder 10000
    pause 0.7
    hide snip0
    show snip1 zorder 10000
    pause 0.7
    hide snip1
    show snip2 zorder 10000
    pause 0.7
    hide snip2
    show snip3 zorder 10000
    pause 0.7
    hide snip3
    show snip4 zorder 10000
    pause 0.3
    hide snip4
    $ snipped = True
    $ toolbox.delete_from_inventory(tools["Scissors"])
    $ toolbox.add_to_inventory(tools["Lysis Buffer"])
    $ toolbox.add_to_inventory(tools["Proteinase K"])
    jump laboratory

label lysis_use_label:
    "We need 0.2 ml of lysis buffer."
    $ amt = renpy.input("How much lysis buffer do we need?", allow=set(".0123456789"))
    if amt == "0.2":
        "Perfect!"
        show snip4 zorder 10000
        pause 0.7
        hide snip4
        show lysis zorder 10000
        pause 0.7
        hide lysis
        $ step += 1
        $ toolbox.delete_from_inventory(tools["Lysis Buffer"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump lysis_use_label

label protein_use_label:
    "We need 0.01 ml of proteinase K."
    $ amt = renpy.input("How much proteinase K do we need?", allow=set(".0123456789"))
    if amt == "0.01":
        "Perfect!"
        show snip4 zorder 10000
        pause 0.7
        hide snip4
        show lysis zorder 10000
        pause 0.7
        hide lysis
        $ step += 1
        $ toolbox.delete_from_inventory(tools["Proteinase K"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump protein_use_label


label heat:
    "We should heat it at 56 degrees Celsius for 2 hours."
    $ temp = renpy.input("What temperature should we heat it at?", allow=set("0123456789"))
    if temp == "56":
        $ time = renpy.input("How long in minutes should we heat it for?", allow=set("0123456789"))
        if time == "120":
            'Great! Now we have to wait.'
            show heatskin zorder 10000:
                xpos 500
                ypos 700
            with Dissolve(2.0)
            $ step = 3
            "It should be done. Go ahead and take it out and remove the swab cutting."
            $ toolbox.add_to_inventory(tools["Phenol Chloroform"])
            jump laboratory
        else:
            "Wrong time."
            jump heat
    else:
        'Wrong temperature.'
        jump heat
    
label phenol_use_label:
    "We need an equal volume of phenol-chloroform. We have 0.21 ml of lysate!"
    $ amt = renpy.input("How much phenol chloroform do we need?", allow=set(".0123456789"))
    if amt == "0.21":
        "Perfect!"
        show phen0 zorder 10000
        pause 0.7
        hide phen0
        show phen1 zorder 10000
        pause 0.7
        hide phen1
        $ step = 4
        $ toolbox.delete_from_inventory(tools["Phenol Chloroform"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump phenol_use_label

label vortex:
    show phen1 zorder 10000
    pause 0.3
    hide phen1
    "Vortexing..."
    pause 0.6
    show phen2 zorder 10000
    $ step = 5
    pause 1.0
    "Vortexed complete!"
    hide phen2
    jump laboratory

label centrifuge:
    "We need to centrifuge it for 5 minutes at 13000 rpm."
    $ temp = renpy.input("What speed should we spin it at?", allow=set("0123456789"))
    if temp == "13000":
        $ time = renpy.input("How long in minutes should we spin it for?", allow=set("0123456789"))
        if time == "5":
            'Great! Now we have to wait.'
            pause 0.5
            "It should be done. Go ahead and take it out!"
            $ step = 6
            show phen3 zorder 10000
            pause 1.0
            $ toolbox.add_to_inventory(tools["Pipette"])
            jump laboratory
        else:
            "Wrong time."
            jump centrifuge
    else:
        'Wrong temperature.'
        jump centrifuge

label pipette_use_label:
    "Let's transfer the aqueous layer..."
    show pipe1 zorder 10000
    pause 0.7
    hide pipe1
    show pipe2 zorder 10000
    pause 0.7
    hide pipe2
    show pipe3 zorder 10000
    pause 0.7
    hide pipe3
    show aqueuos zorder 10000
    pause 0.4
    hide aqueuos
    $ step = 7
    $ toolbox.delete_from_inventory(tools["Pipette"])
    $ toolbox.add_to_inventory(tools["Ethanol"])
    jump laboratory

label e_use_label:
    "We need 2.5x a volume of ethanol. We have 1.3 volume in our tube."
    $ amt = renpy.input("How much ethanol do we need?", allow=set(".0123456789"))
    if amt == "3.25":
        "Perfect!"
        show aqueuos zorder 10000
        pause 0.7
        hide aqueuos
        show eth1 zorder 10000
        pause 0.7
        hide eth1
        $ step = 8
        $ toolbox.delete_from_inventory(tools["Ethanol"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump e_use_label

label freezer:
    "We need to freeze it at -30 degrees celsius for 30 minutes."
    $ temp = renpy.input("What temperature should we freeze it at?", allow=set("-0123456789"))
    if temp == "-30":
        $ time = renpy.input("How long in minutes should we freeze it for?", allow=set("0123456789"))
        if time == "30":
            'Great! Now we have to wait.'
            $ freezing = True
            show closed zorder 10000:
                xpos 1400
                ypos 500
            pause 1.0
            "It should be done. Go ahead and take it out!"
            hide closed
            $ freezing = False
            show eth2
            pause 0.7
            hide eth2
            $ toolbox.add_to_inventory(tools["TE Buffer"])
            $ step = 9
            jump laboratory
        else:
            "Wrong time."
            jump freezer
    else:
        'Wrong temperature.'
        jump freezer
label te_use_label:
    "We need 0.02 ml of TE Buffer."
    $ amt = renpy.input("How much TE Buffer do we need?", allow=set(".0123456789"))
    if amt == "0.02":
        "Perfect!"
        show eth2 zorder 10000
        pause 0.7
        hide eth2
        show pcr zorder 10000
        pause 0.7
        hide pcr
        $ step = 10
        $ toolbox.delete_from_inventory(tools["TE Buffer"])
        "Your solution is ready for DNA analysis!"
        jump laboratory
    else:
        "That's the wrong amount."
        jump te_use_label
