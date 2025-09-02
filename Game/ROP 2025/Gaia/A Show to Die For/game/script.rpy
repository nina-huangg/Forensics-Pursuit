"""
A Show To Die For
"""

    
#################################### TRANSFORM #############################################

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

#------------ Navigation -------------------# 
default middle = True                                            # variable that describes whether current user is in the center (of all five possible positions)
# which direction currently looking at 
default front_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default curr_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default hallway_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default stove_directions = {'up': False, 'down': False, 'left': False, 'right': False}

#------------ Toolbox -------------------# 
default toolbox_show = False                              # whether toolbox is currently displayed
default first_time_toolbox = True                          # first time exploring toolbox?
    # Used for tool sensitivity in the toolbox screens defined in custom_screens.rpy
default tools = {
    "lipstick_glove": False,                                        # lipstick scene
    "glass_jar": False,
    "paper_bag": False,                                                                                    # also lipstick
    "glass_vial": False,                                               # water scene
    "syringe": False,
    "cooler": False,
    "water_glove": False,
    "evidence_box": False,                                            # smoke scene            # GAIA TODO also lipstick
    "smoke_glove": False,
    "smoke_goggle": False,
    "tamper": False,  # this has to be added to a box to become tamper evident
    "rack_glove": False,                                  # rack scene
    "druggist_paper"  : False,
    "adhesive_tape"  : False,
    "brush"          : False,
    "scalpel"        : False,
    "evidence_bag"   : False
    }
                                                                          # which tool is currently enabled (shown on screen)
default finish_collection = False                           # finished evidence collection?


default got_water  = False
default got_makeup = False
default got_smoke = False
default got_rack = False

default toolbox_items  = []
default toolbox_sprites = []

    


init python:
    #------------ Arrow Keys -------------------# 
    config.keymap['dismiss'].append('K_UP')
    config.keymap['dismiss'].append('K_DOWN')
    config.keymap['dismiss'].append('K_LEFT')
    config.keymap['dismiss'].append('K_RIGHT')
    
    #------------ Mouse Cursors -------------------# 
    config.mouse = {
        "default": [("images/cursor.png", 0, 0)],
        "pointer": [("images/cursor.png", 0, 0)],
        "magnifying": [("images/default_cursor.png", 0, 0)],
        "hover": [("images/hover_cursor.png", 0, 0)],
        "dropper": [("images/dropper.png", 0, 49)],
        "dropper_filled": [("images/dropper_filled.png", 0, 49)],
        "reagent": [("images/dropper_filled.png", 0, 49)],
        "hydrogen": [("images/dropper_filled.png", 0, 49)],
        "hand": [("images/default_hand.png", 0, 0)],
        "glass_jar": [("images/glass_jar_hand.png", 0, 0)],
        "paper_bag": [("images/paper_bag_hand.png", 0, 0)],
        "evidence_box": [("images/evidence_box_hand.png", 0, 0)],
        "tamper": [("images/tamper_mouse.png", 0, 0)],
        "box_tamper": [("images/box_tamper_mouse.png", 0, 0)],
        "scalpel": [("images/scalpel_mouse.png", 0, 0)],
        "scalpel_powder": [("images/scalpel_powder_mouse.png", 0, 0)],
        "druggist_fold": [("images/druggist_fold_mouse.png", 0, 0)],
        "druggist_paper": [("images/druggist_paper_mouse.png", 0, 0)]
    }



    # Used to keep track of player's progress in the game
    analyzing = {
        "lipstick": False,
        "water": False,
        "smoke": False,
        "rack": False
    }

    # Used to keep track of what evidence has been analyzed
    analyzed = {
        "lipstick": False,
        "water": False,
        "smoke": False,
        "rack": False
    }

    # Used to keep track of what evidence has been encountered
    # This is used to display the evidence markers and enable respective photos
    encountered = {
        "lipstick": False,
        "water": False,
        "smoke": False,
        "rack": False
    }

    # Used to ensure that the player is not asked the "How would you like to collect the sample?" question multiple times
    asked = {
        "lipstick_glove": False,
        "lipstick_label": False,
        "water_glove": False,
        "water_collect": False,
    # we’ll track container choice in a simple variable:
        "water_container": "",
        "smoke_glove": False,
        "smoke_goggle": False,
        "rack_glove": False,
        "rack_fold": False,
        "rack_transfer": False
    }


    # Used to display the evidence description in the casefile
    evidence_desc = ""

    # used in water scene
    water_vial_checkpoint = False

    def item_dragging(drags):
        """Used to set the mouse cursor to the hand_grab cursor when dragging an item.
        """
        global default_mouse
        default_mouse = "hand_grab"
        return

    def item_dragged(drags, drop):
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

# Defines the supervisor character "Nina", image="nina" used to facilitate side-images
# See more information on side-images in our wiki: https://github.com/nina-huangg/Forensics-Pursuit/wiki/UI-Elements-Integration#character-sprites-
define s = Character(name=("Nina"), image="nina")

# ------------------------------------- Evidence Collection Scene --------------------- #
# breakdown:
    # get the information from nina
    # get brought to backstage view to generally see everything
    # can step forward
    # with desk close up, can examine the makeup and water bottle
    # closer to clothing rack, can look at those clothes
    # looking at the floor, can collect from the smoke machine


label start:
    #------------------- Inventory Things ----------------- #
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


#################################### SET-UP SCENE LABEL #############################################

# sets up environment items for first scene
label setupScene1:

    # environment items to interact with in this scene - remember to put exact file name
    $environment_items = ["lid"]

    # python code block
    python:
        # iterate through environment items list
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
   
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image


            # SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ------------------------------
           
            # for each item, make sure to set width/height to width and height of actual image
            if item == "lid":
                environment_sprites[-1].width = 300 / 2
                environment_sprites[-1].height = 231 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 500

        # adding items to inventory/evidence box and toolbox

        #addToInventory(["evidence_bag"])
        #addToToolbox(["tip"])
        #addToToolboxPop(["tip"])


    show screen full_inventory

    $ default_mouse = "default"
    scene bg theatre_birds at full_screen
    "Click anywhere to begin"
    "August 15th, 2025, Engelhaus Theatre"
    scene bg theatre_house:
        xpos 0 ypos 0
        xysize (config.screen_width, config.screen_height)
    show nina_normal
    s normal1 "Good evening officer. It’s been a pretty intense night here, everyone is really on edge. About an hour ago we started receiving frantic 911 calls from the Engelhouse Theatre where a performance of Wicked was scheduled to occur."
    scene bg theatre_seats:
        xpos 0 ypos 0
        xysize (config.screen_width, config.screen_height)
    show nina_talk  at Transform(xpos=700, ypos=190, zoom=0.7)
    s normal2 "Multiple people in the audience reported that during the final act of the show, the lead actress passed out on stage and would not wake up. The actress, Misty Rious was pronounced dead at 8:03pm."
    s think "We’ve taken statements from individuals who witnessed the incident in the audience, as well as fellow castmates. Take a look:"
    hide nina_talk
    show steve_fancy
    "It was our fifth time performing this week, so I thought maybe she’s just getting tired. The whole night she was all disoriented and kept forgetting lines during rehearsal."
    hide steve_fancy
    show steve_cowboy
    "I noticed she was always extremely dehydrated, just like chugging bottles of water left and right. She’d been complaining of stomach pain and I assumed it was nerves, but maybe it was something else."
    hide steve_cowboy
    show steve_bird
    "There was this moment right as the show was about to end when she just kind of froze. Then she stumbled and fell over, and the other actors rushed to help her."
    scene bg theatre_house at full_screen
    show nina_write
    s normal2 "There's a smoke machine that was used heavily in the scene right before Misty colapsed. Be careful as it might have been tampered with."
    hide nina_write
    show nina_think
    s think "We’ll need your help investigating the area around the stage and dressing room. Let me know what you find!"
    hide nina_think
    jump house

label house:
    $ default_mouse = "magnifying"
    scene bg stage_right with fade:
        xpos 0 ypos 0
        xysize (config.screen_width, config.screen_height)
    call screen house_interact
    return


    jump backstage
    
label backstage:                                                                                              # this is the main backstage view
    $ default_mouse = "magnifying"
    scene bg dressing_room_wide at full_screen_crop_top
    show nina_write
    s normal1 "Welcome backstage! This is Misty Rious's dressing room which she shared with her understudy Susie Picious. They were the only two with access to the space. The items on the desk both belonged to Misty. "
    hide nina_write
    call screen dressing_nav
    return

# gaia what is in the next like 6 lines might be useless
    # if they haven't collected everything, explore
    if not all(analyzed.values()):
        call screen dressing_interact
        jump finished
    # otherwise, they have everything, so go to finished
    jump finished
  

label desk:
    $ default_mouse = "magnifying" 
    scene bg dressing_room_close with fade:
        xpos 0 ypos 0
        xysize (config.screen_width, config.screen_height)
    call screen dressing_interact
    if got_water and got_makeup:
        jump finished
    else:
        jump desk
    return
    
label chairs:
    $ default_mouse = "default"
    show nina_write
    s normal1 "Good instinct to check the chairs but these have already been dusted. We want you to focus on Misty's items on her dressing room table."
    hide nina_write
    call screen dressing_interact
    return
    






label finished:                                                                                               # what to call if they collect everything
        hide screen ui
        scene bg theatre_house:
            xpos 0 ypos 0
            xysize (config.screen_width, config.screen_height)
        show nina_talk
        s normal1 "Well done. It looks like you've processed quite a lot of evidence!"
        hide nina_talk
        show nina_normal
        s normal1 "Tomorrow you can head into the lab to analyze them."
        s normal1 "But for now, give yourself a pat on the back and rest well. Tomorrow's going to be a busy day!"
        return


