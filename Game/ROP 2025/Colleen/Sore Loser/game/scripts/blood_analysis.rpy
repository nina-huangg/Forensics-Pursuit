"""
This file contains all labels and functions related to the bloody carpet and
the drip.
"""

label carpet:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    show screen back_button_overlay

    if analyzed["carpet_cut packaged"]:
        scene carpet cut
    else:
        scene carpet

    if analyzed["carpet packaged"] and analyzed["carpet presumptive"] and analyzed["carpet_cut packaged"]:
        $ analyzing["carpet_stain"] = False
        $ analyzing["carpet_cut"] = False
        s normal "You've finished analyzing the carpet stain."

        if not analyzed["luminol"]:
            s write "Thinking about it though... the stain looked oddly suspicious, like it leaked on the floor but someone cleaned it."
            s talk "Let's try analyzing the floorboards more closely."
            jump luminol
        else:
            jump corridor

    elif analyzed["carpet_cut packaged"]:
        $ analyzing["carpet_stain"] = False
        $ analyzing["carpet_cut"] = False
        # s normal2 "You've already enhanced the carpet."
        s write "There's nothing more you can do now."
        
        if not analyzed["luminol"]:
            s write "Thinking about it though... the stain looked oddly suspicious, like it leaked on the floor but someone cleaned it."
            s talk "Let's try analyzing the floorboards more closely."
            jump luminol
        else:
            jump corridor


    $ analyzing["carpet_stain"] = True
    # $ analyzing["carpet_cut"] = False

    if encountered["carpet"] == False:
        $ encountered["carpet"] = True
        "New photo added to evidence."

    if "swab_pack" not in toolbox_items and "scissors" not in toolbox_items:
        $ addToToolbox(["swab_pack", "scissors"])

    call screen toolbox
    call screen toolbox_blood

label drip:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    show screen back_button_overlay
    scene drip

    if analyzed["drip"] and analyzed["drip presumptive"] and analyzed["drip packaged"]:
        $ analyzing["drip"] = False
        s normal "You've finished analyzing the drip."
        jump corridor

    if encountered["drip"] == False:
        $ encountered["drip"] = True
        "New photo added to evidence."

    $ analyzing["drip"] = True

    $ addToToolbox(["swab_pack"])
    call screen toolbox
    call screen toolbox_blood

label carpet_swab:
    # show darken_overlay
    hide screen back_button_overlay

    scene carpet
    if asked["carpet_swab"]:
        show darken_overlay
        show red swab at Transform(xpos=0.4, ypos=0.3)
        "Sample successfully collected."
        jump sample
    
    show darken_overlay
    show clean swab at Transform(xpos=0.4, ypos=0.3)
    menu:
        "How would you like to collect the sample?"
        "Using a wet swab":
            hide clean swab
            show red swab at Transform(xpos=0.4, ypos=0.3)
            "Sample successfully collected."
            $ asked["carpet_swab"] = True
            jump sample
        "Using a dry swab":
            "Remember, we can't collect dry samples using dry swabs."
            jump carpet

label drip_swab:
    show darken_overlay
    hide screen back_button_overlay
    
    scene drip
    if asked["drip_swab"]:
        show darken_overlay
        show red swab at Transform(xpos=0.4, ypos=0.3)
        "Sample successfully collected."
        jump sample
    
    show darken_overlay
    show clean swab at Transform(xpos=0.4, ypos=0.3)
    menu:
        "How would you like to collect the sample?"
        "Using a wet swab":
            $ asked["drip_swab"] = True
            hide clean swab
            show red swab at Transform(xpos=0.4, ypos=0.3)
            "Sample successfully collected."
            jump sample
        "Using a dry swab":
            $ asked["drip_swab"] = True
            hide clean swab
            show red swab at Transform(xpos=0.4, ypos=0.3)
            "Sample successfully collected."
            jump sample

label sample:
    menu:
        "How would you like to proceed?"
        "Package the sample":
            jump drip_alt
        "Run a presumptive test":
            hide red swab
            show darken_overlay
            show screen bloody_swab
            python: 
                removal_list = ["swab_pack", "scissors"]
                for item in removal_list:
                    if item in toolbox_items:
                        removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])
                addToToolbox(["ethanol", "reagent", "hydrogen_peroxide"])
            call screen toolbox

label trash:
    # TODO: show trash icon
    $ default_mouse = "default"
    hide screen toolbox_presumptive
    menu:
        "Should I get rid of this swab?"
        "Yes":
            hide screen bloody_swab
            hide red swab
            $ player_kastle_meyer_order = []
            hide screen toolbox_presumptive
            if analyzing["carpet_stain"]:
                jump carpet
            elif analyzing["drip"]:
                jump drip
        "No":
            show screen bloody_swab
            call screen toolbox

label presumptive:
    if default_mouse == "ethanol":
        $ player_kastle_meyer_order.append("e")
        $ default_mouse = "default"
        play sound "audio/waterdrop.mp3"
        "A drop of ethanol has been added to the sample."
    elif default_mouse == "reagent":
        $ player_kastle_meyer_order.append("r")
        $ default_mouse = "default"
        play sound "audio/waterdrop.mp3"
        "A drop of phenolpthalin has been added to the sample."
    elif default_mouse == "hydrogen":
        $ player_kastle_meyer_order.append("h")
        $ default_mouse = "default"
        play sound "audio/waterdrop.mp3"
        "A drop of hydrogen peroxide has been added to the sample."

    if len(player_kastle_meyer_order) > 5:
        $ default_mouse = "default"
        s sweat "I think you put in too many drops... you should try again."
        hide screen bloody_swab
        hide red swab
        $ player_kastle_meyer_order = []
        
        python:
            removal_list = ["ethanol", "reagent", "hydrogen_peroxide"]
            for item in removal_list:
                if item in toolbox_items:
                    removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])

        hide screen toolbox_presumptive
        if analyzing["carpet_stain"] or analyzing["carpet_cut"]:
            jump carpet
        elif analyzing["drip"]:
            jump drip

    if player_kastle_meyer_order in valid_kastle_meyer_orders:
        hide screen toolbox_presumptive
        hide screen bloody_swab
        hide red swab
        # show darken_overlay
        show pink swab at Transform(xpos=0.4, ypos=0.3)
        "The results of this test show that this substance is indeed blood."
        $ player_kastle_meyer_order = []

        python:
            removal_list = ["ethanol", "reagent", "hydrogen_peroxide"]
            for item in removal_list:
                if item in toolbox_items:
                    removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])

        if analyzing["carpet_stain"]:
            $ analyzed["carpet presumptive"] = True
            jump carpet
        elif analyzing["drip"]:
            $ analyzed["drip presumptive"] = True
            jump drip
    else:
        show screen bloody_swab
        call screen toolbox

label cutting:
    $ analyzing["carpet_cut"] = True
    scene carpet cut

    show darken_overlay
    show carpet_sample
    s talk "Perfect! Let's package this."
    # will not allow player to sample blood from the carpet again
    python:
        removal_list = ["swab_pack", "scissors"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])
        
        addToToolbox(["evidence_bag", "tamper_evident_tape"])
    $ tools["bag"] = True
    hide carpet_sample
    show carpet_sample at Transform(xpos=0.4, ypos=0.3)

    call screen toolbox

    # hide evidence bag large
    # call screen tape_to_bag

    # "The carpet has been added to your evidence."
    # $ analyzing["carpet"] = False
    # $ analyzed["carpet_cut packaged"] = True
    # # TODO $ addToInventory(["carpet_cut"])

    # $ analyzed["carpet"] = True
    
    # jump corridor

# drip packaging
label drip_alt:
    python:
        removal_list = ["swab_pack", "scissors"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])
        
        addToToolbox(["evidence_bag", "tube", "tamper_evident_tape"])
    if analyzing["drip"]:
        scene drip
    else:
        scene carpet

    show darken_overlay
    show red swab at Transform(xpos=0.4, ypos=0.3)
    $ tools["tube"] = True
    call screen toolbox

label drip_packaging_0:
    hide red swab
    call screen sample_to_tube
    show darken_overlay
    show sample test tube at Transform(xpos=0.4, ypos=0.2)
    "Sample successfully placed in tube."
    call screen toolbox

label drip_packaging_1:
    hide sample test tube
    call screen tube_to_bag
    show darken_overlay
    show evidence bag large at Transform(xpos=0.4, ypos=0.15)
    "Sample successfully placed in bag."
    call screen toolbox

label drip_packaging_2:

    hide evidence bag large
    call screen tape_to_bag
    show darken_overlay

    python:
        removal_list = ["evidence_bag", "tube", "tamper_evident_tape"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])

    show casefile_evidence_idle at Transform(xpos=0.3, ypos=0.24)
    play sound "audio/tape.mp3"
    
    if analyzing["carpet_stain"]:
        "The carpet sample has been added to your evidence."
        $ analyzed["carpet packaged"] = True
        # TODO $ addToInventory(["drip"])
        hide casefile_evidence_idle
        jump carpet
    else:
        "The drip sample has been added to your evidence."
        $ analyzing["drip"] = False
        $ analyzed["drip"] = True
        $ analyzed["drip packaged"] = True
        # TODO $ addToInventory(["drip"])
        hide casefile_evidence_idle
        jump drip
