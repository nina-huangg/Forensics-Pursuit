init python:
    config.mouse = {
        "glove": [("glove.png", 0, 0)],
        "dropper": [("dropper.png", 0, 95)],
        "dropper ethanol": [("dropper liquid.png", 0, 95)],
        "dropper reagent": [("dropper reagent.png", 0, 95)],
        "dropper hydrogen peroxide": [("dropper liquid.png", 0, 95)],
        "swab": [("swab.png", 0, 318)],
        "wet swab": [("wet swab.png", 0, 324)],
        "hungarian red": [("enhancer.png", 0, 0)],
        "hover": [("hover cursor.png", 0, 0)],
        "magnifying glass": [("default cursor.png", 0, 0)]
    }

    valid_kastle_meyer_orders = [
        ["e", "r", "h"],
        ["e", "r", "r", "h"],
        ["e", "r", "h", "h"],
        ["e", "r", "r", "h", "h"],
        ["e", "e", "r", "h"],
        ["e", "e", "r", "r", "h"],
        ["e", "e", "r", "h", "h"],
        ["e", "e", "r", "r", "h", "h"]
    ]

    def item_dragged(drags, drop):
        if not drop:
            return

        store.dragged = drags[0].drag_name
        store.dropped = drop.drag_name

        return True

define flash = Fade(0.1, 0.0, 0.5, color="#fff")

default player_kastle_meyer_order = []

default presumptive_completed = False

default evidence_opened = False

default sample_acquired = False

default sample_active = False

label evidence_bags:
    if sample_active:
        hide screen trash
        hide screen toolbox
        call screen draggables
        call screen more_draggables
        call screen last_draggables
        $ sample_active = False
        $ sample_acquired = True
        show sealed bag at center
        "Everything is packaged. I'll add it to my list of evidence."
        hide sealed bag
    
    show screen toolbox
    call screen footprint

label footprint:
    if default_mouse == "wet swab":
        $ default_mouse = "glove"
        scene footprint discovered
        $ sample_active = True
        hide screen footprint
        show screen trash
        call screen sample
    elif default_mouse == "hungarian red":
        $ default_mouse = "glove"
        hide screen trash
        hide screen toolbox
        hide screen footprint
        scene footprint enhanced
        "There's nothing more for me to do here."
        "The physical print will be delivered to my lab."
        jump front
        return
    else:
        call screen footprint

label sample:
    if default_mouse == "dropper ethanol":
        $ player_kastle_meyer_order.append("e")
        $ default_mouse = "dropper"
    elif default_mouse == "dropper reagent":
        $ player_kastle_meyer_order.append("r")
        $ default_mouse = "dropper"
    elif default_mouse == "dropper hydrogen peroxide":
        $ player_kastle_meyer_order.append("h")
        $ default_mouse = "dropper"

    if player_kastle_meyer_order in valid_kastle_meyer_orders:
        hide screen sample
        hide screen trash
        show pink swab at pink_swab
        show right hand at right_hand
        "The results of this test show that this substance is indeed blood."
        $ presumptive_completed = True
        hide pink swab
        $ sample_active = False
        $ player_kastle_meyer_order = []
        show screen toolbox
        call screen footprint
    else:
        call screen sample


label trash:
    "Would you like to dispose of the current swab?"
    menu:
        "Yes.":
            $ player_kastle_meyer_order = []
            hide screen sample
            hide screen trash
            call screen footprint
        "No.":
            call screen sample

label investigation:
    $ default_mouse = "glove"
    hide screen left_ui_toolbox_unopened
    hide screen corridor
    scene footprint discovered
    "You are free to use any tools at your disposal."
    "Play around with them and see where it takes you!"
    show screen toolbox
    call screen footprint
    return

label start:
    $ default_mouse = "magnifying glass"
    scene corridor
    "You've arrived at the scene."
    "A murder has occurred in a university dorm room."
    "Look around carefully for any evidence to uncover."

label front:
    $ default_mouse = "magnifying glass"
    scene corridor
    show screen left_ui_toolbox_unopened
    call screen corridor
    return


label sample_information:
    show screen left_ui_toolbox_unopened
    show screen sample_in_evidence
    if presumptive_completed:
        "This is a sample of blood gathered from the footprint. It is unknown who this blood belongs to at the moment."
    else:
        "This is a sample of the red substance gathered from the footprint."
    call screen sample_in_evidence

label evidence:
    if evidence_opened:
        $ evidence_opened = not evidence_opened
        if sample_acquired:
            hide screen sample_in_evidence
        scene corridor
        show screen corridor
    else:
        $ evidence_opened = not evidence_opened
        hide screen corridor
        scene evidence
        if sample_acquired:
            show screen sample_in_evidence
    call screen left_ui_toolbox_unopened
