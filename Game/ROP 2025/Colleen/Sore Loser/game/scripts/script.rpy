"""
This file notably contains the start and corridor labels which provide case background to
the player and checks if the player has collected all evidence.

The top of this file (init python block) contains the mouse cursor configuration, tools,
and evidence variables which are used in other scripts.
"""

init python:
    # Defines all mouse cursors used in the game
    config.mouse = {
        "default": [("images/cursor.png", 0, 0)],
        "pointer": [("images/cursor.png", 0, 0)],
        "magnifying": [("images/default_cursor.png", 0, 0)],
        "hover": [("images/hover_cursor.png", 0, 0)],
        "dropper": [("images/dropper.png", 0, 49)],
        "ethanol": [("images/dropper_filled.png", 0, 49)],
        "reagent": [("images/dropper_filled.png", 0, 49)],
        "hydrogen": [("images/dropper_filled.png", 0, 49)],
        "hand": [("images/default_hand.png", 0, 0)],
        "hand_grab": [("images/grab_hand.png", 0, 0)],
        "luminol": [("images/luminol_cursor.png", 0, 0)],
        "luminol_tilt": [("images/luminol_cursor_tilt.png", 0, 0)],
    }

    packaging = False  # Used to determine if the player is packaging evidence
    
    # Used for tool sensitivity in the toolbox screens defined in custom_screens.rpy
    tools = {
        "uv light": False,
        "magnetic powder": False,
        "scalebar": False,
        "gel lifter": False,
        "tape": False,
        "backing": False,
        "packaging": False,
        "tube": False,
        "bag": False,
        "tamper evident tape": False,
        "swab": False
    }

    # Used to keep track of player's progress in the game
    analyzing = {
        "cabinet": False,
        "lower_cabinet": False,
        "counter": False,

        "handprint": False,
        "fingerprint": False,

        "drip": False,
        "carpet_stain": False,
        "carpet_cut": False,

        "luminol": False,

        "needle": False,

        "trashcan": False,
        "steroids": False,

        "tylenol": False,

        "pillbox": False,
    }

    # Used to keep track of what evidence has been analyzed
    analyzed = {
        "handprint": False,
        "fingerprint": False,

        # in comparison to analyzing, break blood analysis segments into parts...
        "drip": False,
        "drip presumptive": False,
        "drip packaged": False,

        "carpet": False,
        "carpet packaged": False,
        "carpet presumptive": False,
        "carpet_cut packaged": False,

        "luminol": False,

        "needle": False,

        "steroids": False,
        "tylenol": False,
        "rat_poison": False,

        "pillbox": False,
    }

    # Used to keep track of what evidence has been encountered
    # This is used to display the evidence markers and enable respective photos
    encountered = {
        "cabinet": False,

        "counter": False,

        "trashcan": False,
        "uncovered trash": False,

        "drip": False,
        "carpet": False,
    }

    # Used to ensure that the player is not asked the "How would you like to collect the sample?" question multiple times
    asked = {
        "drip_swab": False,
        "carpet_swab": False
    }

    # Used to compare against the player's Kastle-Meyer order in the presumptive test scene
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

    player_kastle_meyer_order = []

    # Used to display the evidence description in the casefile
    evidence_desc = ""

    def item_dragging_package(drags):
        """Used to set the mouse cursor to the hand_grab cursor when dragging an item.
        """
        global default_mouse
        default_mouse = "hand_grab"
        return

    def item_dragged_package(drags, drop):
        """Used to set the mouse cursor to the hand_grab cursor when grabbing an item.
        """
        global default_mouse
        default_mouse = "hand_grab"
        
        if not drop:
            default_mouse = "hand"
            return

        store.dragged = drags[0].drag_name
        store.dropped = drop.drag_name

        # Hide all draggable screens
        renpy.hide_screen("sample_to_tube")
        renpy.hide_screen("fingerprint_to_bag")
        renpy.hide_screen("handprint_to_bag")
        renpy.hide_screen("tape_to_bag")
        default_mouse = "default"
        return True
    
    def close_menu():
        """Used to close the casefile menu.
        """
        if renpy.get_screen("casefile_physical"):
            evidence_desc = ""
            renpy.hide_screen("casefile_physical")
        elif renpy.get_screen("casefile_photos"):
            renpy.hide_screen("casefile_photos")
        elif renpy.get_screen("casefile"):
            renpy.hide_screen("casefile")
        else:
            renpy.show_screen("casefile")

    def return_to_stage():
        """Used to return to the corridor screen.
        """
        # reset analyzing variables
        for item in analyzing:
            analyzing[item] = False
            
        
        renpy.jump("corridor")

# Defines the supervisor character "Nina", image="nina" used to facilitate side-images
# See more information on side-images in our wiki: https://github.com/nina-huangg/Forensics-Pursuit/wiki/UI-Elements-Integration#character-sprites-
define s = Character(name=("Nina"), image="nina")

label start:
    $ default_mouse = "default"
    scene apt

    "June 13, 2025 12:20 PM. 15 Walmer Road."
    show nina talk
    s "Officer, it's good to see you."
    show nina normal 
    s "Sorry to call you in during your break, but we got an urgent call from this apartment at {color=#00ff00}11:45 AM{/color}."
    show nina normal
    s "The victim, Eaton Poisson, was found dead in his living room by his roomate, Chet Erv"
    s "He says he had come back from a morning run and found Eaton lying on the floor, unresponsice and with blood dripping out of a puncture in his thigh."
    show nina talk
    s "Let me give you a quick rundown of what we know so far."
    show nina write
    s "The victim is 19 years old, and he and his roommate are both varisty track-and-field athletes on the University of Rotonro team."
    s "Eaton was apparently one of the best runners on the team, in great health and with no underlying medical conditions."
    s "Him and his roommate are both on a strict diet, taking vitamin supplements and not permitted to drink alcohol."
    show nina think
    s "However, over a week ago, Eaton started to complain of {color=#00ff00}random bruising and pain.{/color}"
    s "His doctor thought it was related to a vitamin deficiency, and prescribed him some vitamin K supplements."
    s "However, it seems like that didn't help with his condition."
    show nina talk
    s "Furthermore, when the police arrived at the scene, they noted that there was an {color=#00ff00}unusual amount of blood coming from the puncture wound.{/color}"
    show nina normal
    s "There were no signs of a struggle or any other serious wounds, so we believe this might be the work of some toxin."
    s "And that's all we know so far."
    show nina talk
    s "The body has been moved to the morgue, but the room itself remains untouched."
    s "I need you to be thorough."
    s "Look for any relevant evidence and collect fingerprints."
    show nina normal
    s "Remember, time is of the essence. We need to gather all the evidence we can before it gets contaminated or lost."
    # s "You can check your collected evidence at anytime through the {color=#00ff00}casefile{/color} on the top left corner"
    s "Good luck, Officer. We're counting on you to help us solve this case."
    jump corridor  

label corridor:
    $ default_mouse = "magnifying"
    hide screen back_button_overlay
    hide screen luminol1
    hide screen luminol2
    hide screen luminol3 

    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Tape on acetate", "Tapeglo in bag", "Tape photo", "Duct tape tapeglo", "Distilled water", "Tape in tweezers", "Duct tape", "Tapeglo", 
    "Fingerprint on card", "Backing card","Scalebar", "Lifting tape", "Jar photo", "Lid in tweezers", "Camel brush", "Lid with soot", "Lid", "Camphor smoke", "Lighter", 
    "Tweezers", "Gloves box", "Evidence bag", "Jar in bag", "Tape in bag", "Pvs in bag"] # holds names for inspect pop-up text 
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 110 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 175 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    # $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_size = (100, 100)
    # $toolbox_slot_padding = 125 / 2 # sets padding size between toolbox slots
    $toolbox_slot_padding = 69
    $toolbox_first_slot_x = 110 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 175 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (100, 100) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 69 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 406 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 445 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    $all_pieces = 0

    # This changes the background image depending on whether or not the player has...
    if analyzed["carpet_cut packaged"]:
        scene apt cut
    else:
        scene apt

    # This checks if the player has collected all the evidence
    # TODO
    # if all(value == True for value in analyzed.values()):
    if analyzed["fingerprint"] and analyzed["handprint"] and analyzed["carpet"] and analyzed["drip"] and analyzed["steroids"] and analyzed["pillbox"] and analyzed["needle"] and analyzed["tylenol"] and analyzed["rat_poison"]:
        $ hide_all_inventory()
        show nina talk
        s "Well done. It looks like you've processed quite a lot of evidence!"
        show nina normal
        s "Tomorrow you can head into the lab to analyze them."
        s "But for now, give yourself a pat on the back and rest well. Tomorrow's going to be a busy day!"
        return
    call screen apt


transform half_size:
    zoom 0.5    