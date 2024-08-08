default current_cursor = ''
default show_case_files = False
default show_toolbox = False
define flash = Fade(.25, 0, .75, color="#fff")

### entries on afis when search
default afis_search = ["Crowbar Fingerprint"] #?
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}] #?

init python: # initializing all the global functions we need
    def set_cursor(cursor):
        # resets the cursor to the desired position. If the current cursor and mouse are equal to the
        # cursor passed in, set them to default, otherwise, set them to the value of the cursor passed in.
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def calculate_afis(evidence):
        # Declares a new afis_search array after a piece of evidence is processed.
        # For each piece of evidence in the evidence array, if it is not equal to the passed-in evidence,
        # and has been processed, this function adds it to the new afis_search array.
        global afis_search
        afis_search = []
        # evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e != evidence:
                afis_search.append(e)
    
    class Evidence:
        # A class that keeps track of evidence. Records the name of the evidence, its details (which
        # are stored in a dict), and sets its default processed state to False.
        def __init__(self, name, afis_details):
            self.name = name
            self.afis_details = afis_details
            self.processed = False
    
    ### declare each piece of evidence
    laptop_fingerprint = Evidence(name = 'laptop_fingerprint',
                                afis_details = {
                                    'image': 'laptop_fingerprint',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})
    crowbar = Evidence(name = 'crowbar',
                        afis_details = {
                            'image': 'evidence_crowbar',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '70'})
    
    ### stores the pieces of evidence declared above into an array
    afis_evidence = [laptop_fingerprint, crowbar]

    ### set current_evidence to track which evidence is currently active
    current_evidence = ''
    current_tool = ''

#################################### TIMER #############################################

# label timer:
#     show timer_bg
#     show a0:
#         xalign 0.705 yalign 0.41
#     show b0:
#         xalign 0.635 yalign 0.41
#     show c0:
#         xalign 0.535 yalign 0.41
#     show d0:
#         xalign 0.465 yalign 0.41
#     show e0:
#         xalign 0.365 yalign 0.41
#     show f0:
#         xalign 0.295 yalign 0.41
#     pause

#################################### START #############################################
# label start:
#     scene entering_lab_screen
#     with Dissolve(1.5)

label start:
    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = True # disables rollback
    $quick_menu = True # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
   
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
   
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Evidence bag", "Crowbar", "Chamber Tools", "Water", "Superglue", "Fingerprint Dye Kit", "Crowbar Fingerprint"] # holds names for inspect pop-up text
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 105 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 300 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable


    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    $toolbox_item_names = ["Chamber Tools", "Fingerprint Dye Kit"] # holds names for inspect pop-up text
    $toolbox_db_enabled =  False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_padding = 120 / 2 # sets padding size between toolbox slots
    $toolbox_first_slot_x = 105 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 300 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable


    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    $toolboxpop_item_names = ["Water", "Superglue"] # holds names for inspect pop-up text
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 120 / 2 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable


    $current_scene = "scene1" # keeps track of current scene
   
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item


    # j code
    python:
        addToInventory(["crowbar"])
        addToInventory(["evidence_bag"])
        addToToolbox(["chamber_tools"])
        addToToolboxPop(["superglue"])
        addToToolboxPop(["water"])
        addToToolbox(["fingerprint_dye_kit"])

    default current_path = ''
    default crowbar_complete = False
    default paint_chip_complete = False
    default crowbar_analysis_complete = False
    default paint_chip_analysis_complete = False
    scene entering_lab_screen
    with Dissolve(1.5)
    jump lab_hallway_intro

# sets up environment items for first scene
label setupScene1:


    # environment items to interact with in this scene - remember to put exact file name
    $environment_items = ["key"]


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


            if item == "key":
                environment_sprites[-1].width = 300 / 2
                environment_sprites[-1].height = 231 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 500
        addToInventory(["evidence_bag"])
        addToToolbox(["tip"])
        addToToolboxPop(["tip"])


    # scene scene-1-bg at half_size - sets background image, don't need rn
    call screen scene1

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

label lab_hallway_intro:
    # show screen case_files_screen onlayer over_screens # found in util_screens.rpy
    # show screen toolbox_button_screen onlayer over_screens # found in util_screens.rpy
    show screen study_room3_inventory onlayer over_screens
    scene lab_hallway_idle
    "Welcome to the lab!"
    "This is where you will spend time analyzing the evidence you have collected."
    "Let's get started!"
    # jump setupScene1
    "Which piece of evidence would you like to analyze first?"
    jump options
label pre_options:
    "What would you like to analyze next?"
label options:
    scene lab_hallway_idle
menu:
    "Crowbar":
        if crowbar_complete == False:
            $ current_path = 'crowbar'
            $ crowbar_complete = True
            jump crowbar_treatments
        elif crowbar_analysis_complete == False:
            $ current_path = 'crowbar_analysis'
            $ crowbar_analysis_complete = True
            jump hallway
        else:
            "You already finished all the analysis for this piece of evidence."
            jump pre_options
    "Paint Chip":
        if paint_chip_complete == False:
            $ current_path = 'paint_chip'
            $ paint_chip_complete = True
            jump hallway
        elif paint_chip_analysis_complete == False:
            $ current_path = 'paint_chip_analysis'
            $ paint_chip_analysis_complete = True
            jump hallway
        else:
            "You already finished all the analysis for this piece of evidence."
            jump pre_options

label crowbar_treatments:
    "Looks like there might be fingerprints on this crowbar. Which technique would you like to use to check it out?"
label treatments:
menu:
    "Ninhydrin treatment":
        "Ninhydrin treatment is a chemical reacts with amino acids in sweat to produce a purple color."
        "It is commonly used on porous surfaces such as paper and cardboard, making it less suitable for a metallic surface like a crowbar."
        "Are you sure you want to use ninhydrin treatment? Try something else."
        jump treatments
    "CA Fuming":
        "Great choice! For a metallic, non-porous object like a crowbar, CA (cyanoacrylate) fuming is typically more effective."
        jump hallway
    "Silver Nitrate treatment":
        "This method involves spraying a solution that reacts with the salts in sweat to form silver chloride, which turns dark under UV light."
        "It's more appropriate for porous surfaces and would not be as effective on metal."
        "Are you sure you want to use silver nitrate treatment? Try something else."
        jump treatments
    "Iodine Fuming":
        "Iodine vapors react with fats and oils in fingerprints to produce a temporary brown color."
        "This method is often used for porous surfaces like paper or untreated wood, and the prints are not permanent unless fixed."
        "Are you sure you want to use iodine fuming? Try something else."
        jump treatments

label hallway:
    call screen lab_hallway_screen # found in custom_screens.rpy

label data_analysis_lab:
    scene afis_interface
    if current_path == 'crowbar_analysis' or current_path == 'paint_chip_analysis':
        call screen data_analysis_lab_screen # found in custom_screens.rpy
    else:
        "I don't think you need to be here right now."
        jump hallway

label afis:
    scene software_interface
    if current_path == 'crowbar_analysis':
        call screen pre_afis_screen # found in custom_screens.rpy
    else:
        "I don't think you need to be here right now."
        jump data_analysis_lab

label fingerprint_upload:
    if item_dragged == 'crowbar_fingerprint':
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("crowbar_fingerprint")])
        call screen afis_screen
    else:
        "Please select the correct piece of evidence to submit."
        call screen pre_afis_screen

label pdq:
    scene paint_database 
    if current_path == 'paint_chip_analysis':
        call screen pdq_screen # found in custom_screens.rpy
    else:
        "I don't think you need to be here right now."
        jump data_analysis_lab

label afis_done:
    "Good work! You're all done with the crowbar development."
    jump pre_options

label incorrect_car:
    "That doesn't seem right, try again."
    call screen pdq_screen

label correct_car:
    "Correct! It seems most likely that this vehicle is a 1988 Ford Windstar."
    jump pre_options

label materials_lab:
    scene materials_lab
    if current_path == 'crowbar' or current_path == 'paint_chip':
        call screen materials_lab_screen
    else:
        "I don't think you need to be here right now."
        jump hallway

label wet_lab:
    scene fumehood
    # show screen back_button_screen('materials_lab') onlayer over_screens
    "I don't think we need to be here right now."
    jump materials_lab

label fingerprint_development:
    scene chamber_outside
    # show screen back_button_screen('materials_lab') onlayer over_screens
    if current_path == 'crowbar':
        call screen fingerprint_development_screen
    else:
        "I don't think we need to be here right now."
        jump materials_lab
    
# Implement toolbar in fingerprinting

label crowbar_development:
    default left_complete = False
    default right_complete = False
    scene chamber_inside
    call screen crowbar_development

label crowbar_development_cont:
    if item_dragged == 'crowbar':
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("crowbar")])
        call screen reservoir_dev
    elif item_dragged == '':
        "Please select a piece of evidence to submit."
        jump crowbar_development
    else:
        "Are you sure you want to put that into the chamber?"
        jump crowbar_development

label reservoir_development_left:
    if item_dragged == 'superglue':
        $ left_complete = True
        $ default_mouse = ''
        call screen reservoir_dev
    elif item_dragged == '':
        "Please put something in the left chamber."
        call screen reservoir_dev
    else:
        "I don't think that's the correct thing to use here."
        call screen reservoir_dev

label reservoir_development_right:
    if item_dragged == 'water':
        $ right_complete = True
        $ default_mouse = ''
        call screen reservoir_dev
    elif item_dragged == '':
        "Please put something in the right chamber."
        call screen reservoir_dev
    else:
        "I don't think that's the correct thing to use here."
        call screen reservoir_dev

label fumigation:
    scene chamber_outside
    "Let's time this. How long should the fuming process take?"
    jump timer

label timer_set:
    scene chamber_outside

    $ min_hours = 0
    $ min_minutes = 7
    $ min_seconds = 50
    $ max_hours = 0
    $ max_minutes = 10
    $ max_seconds = 10

    $ min_time = min_hours * 3600 + min_minutes * 60 + min_seconds
    $ max_time = max_hours * 3600 + max_minutes * 60 + max_seconds
    $ true_time = time_numbers[5] + time_numbers[4] * 10 + time_numbers[3] * 60 + time_numbers[2] * 600 + time_numbers[1] * 3600 + time_numbers[0] * 36000

    if true_time >= min_time and true_time <= max_time:
    # if ((time_numbers[3] >= 8 and time_numbers[2] == 0) or (time_numbers[3] == 0 and time_numbers[2] == 1)) and (time_numbers[1] == 0 and time_numbers[0] == 0):
        "That's correct."
        $ string_min_1 = "%d" % time_numbers[2]
        $ string_min_2 = "%d" % time_numbers[3]
        $ string_sec_1 = "%d" % time_numbers[4]
        $ string_sec_2 = "%d" % time_numbers[5]
        if string_min_1 == "0":
            if string_sec_1 != "0":
                "Waiting for [string_min_2] minutes and [string_sec_1][string_sec_2] seconds... (press space to continue)"
            elif string_sec_2 != "0":
                "Waiting for [string_min_2] minutes and [string_sec_2] seconds... (press space to continue)"
            else:
                "Waiting for [string_min_2] minutes... (press space to continue)"
        else:
            if string_sec_1 != "0" and string_sec_2 != "0":
                "Waiting for [string_min_1][string_min_2] minutes and [string_sec_1][string_sec_2] seconds... (press space to continue)"
            elif string_sec_2 != "0":
                "Waiting for [string_min_1][string_min_2] minutes and [string_sec_2] seconds... (press space to continue)"
            else:
                "Waiting for [string_min_1][string_min_2] minutes... (press space to continue)"
        jump timer_completed
    elif true_time < min_time:
        "That's not enough time, try again."
        jump timer
    elif true_time > max_time:
        "That's too much time, try again."
        jump timer

label timer_completed:
    scene fuming with dissolve
    "Time's up! Let's take it out of the oven and examine what we have."

label dye:
    scene dye_1
    "What sort of fingerprint dye would you like to use to examine the print?"
    call screen dyes
label n_chosen:
    "Not quite. Ninhydrin is commonly used for developing fingerprints on porous surfaces like paper and cardboard."
    "It is not suitable for non-porous surfaces like metal. Try again."
    call screen dyes
label s_chosen:
    "Not quite. Silver Nitrate is typically used on porous surfaces."
    "This method is not effective for non-porous surfaces such as metal. Try again."
    call screen dyes
label r_chosen:
    "Good choice. Rhodamine 6G is one of two choices of dye you can make here. Apply the dye until you get good coverage."
    pause
    scene dye_2
    pause
    scene dye_3
    pause
    scene dye_4
    $ default_mouse = ''
    "Let's examine this with our light source."
    scene dye_light
    pause
    #choose light source
    "Wow, look at that fingerprint! We can now run our database analysis on it to see if there are any coinciding pieces of evidence."
    scene dye_light
    with flash
    "A photo of the print has been added to your inventory."
    python:
        addToInventory(["crowbar_fingerprint"])
    jump pre_options
label a_chosen:
    "Good choice. Ardrox is one of two choices of dye you can make here. Apply the dye until you get good coverage."
    pause
    scene a_dye_2
    pause
    scene a_dye_3
    pause
    scene a_dye_4
    $ default_mouse = ''
    "Let's examine this with our light source."
    scene a_dye_light
    #choose light source
    "Wow, look at that fingerprint! We can now run our database analysis on it to see if there are any coinciding pieces of evidence."
    scene a_dye_light
    with flash
    "A photo of the print has been added to your inventory."
    python:
        addToInventory(["crowbar_fingerprint"])
    jump pre_options


label analytical_instruments:
    # show screen back_button_screen('materials_lab') onlayer over_screens
    scene lab_bench
    if current_path != "paint_chip":
        "I don't think we need to be here right now."
        jump materials_lab
    "Choose the instrument you think we need to examine the paint chip."
    default instrument_choice = ""
    call screen analytical_instruments_screen

label pre_paint:
    if instrument_choice == "centrifuge":
        show centrifuge
        "That's a centrifuge. A centrifuge helps separate different substances within a mixture."
        "It's commonly used for blood testing, purifying cells, DNA extraction, and sample preparation."
        "I don't think we need this for our paint chip. Try another one."
        hide centrifuge
    elif instrument_choice == "hotplate":
        show hot_plate
        "This is a hot plate. A hot plate is a portable heating device."
        "It's used to heat chemicals, solutions, or samples to a specific temperature for experiments or reactions."
        "I don't think we need this for our paint chip. Try another one."
        hide hot_plate
    elif instrument_choice == "thermocycler":
        show thermocycler
        "That's a thermocycler. A thermocycler repeatedly heats and cools DNA samples to allow specific chemical reactions to occur, like PCR."
        "I don't think we need this for our paint chip. Try another one."
        hide thermocycler
    elif instrument_choice == "gel":
        show gel
        "This is a gel electrophoresis machine, which runs an electric current through a gel to separate small molecules, such as DNA, RNA, or proteins."
        "I don't think we need this for our paint chip. Try another one."
        hide gel
    call screen analytical_instruments_screen

label paint_chip_examine:
    "Correct! We will want to examine our paint chip closely, and a microscope is the tool we need to do that."
    $ default_mouse = 'tweezers'
    $ current_cursor = 'tweezers'
    scene microscope_outside
    default chip_picked = False
    call screen drag_paint_chip

label microscope_chip:
    scene close_paint
    "Click through the layers to identify each one."
    # scramble multiple choice
    default layer1_clicked = False
    default layer2_clicked = False
    default layer3_clicked = False
    default layer4_clicked = False
    default just_clicked = 0
    call screen identify_layers

label layer_quiz:
    "Which paint chip layer is this?"
menu:
    "Silver substrate body":
        if just_clicked == 4:
            jump post_quiz
        else:
            "That's not correct, try again."
            jump layer_quiz
    "Black basecoat":
        if just_clicked == 2:
            jump post_quiz
        else:
            "That's not correct, try again."
            jump layer_quiz
    "Clear top coat":
        if just_clicked == 1:
            jump post_quiz
        else:
            "That's not correct, try again."
            jump layer_quiz
    "Dark grey primer":
        if just_clicked == 3:
            jump post_quiz
        else:
            "That's not correct, try again."
            jump layer_quiz

label post_quiz:
    "Correct! Documenting..."
    if layer1_clicked == True and layer2_clicked == True and layer3_clicked == True and layer4_clicked == True:
        jump scalpel_prep
    else:
        call screen identify_layers

label scalpel_prep:
    scene scalpel_bg
    default orientation = "correct"
    call screen scalpel_orientation

label orient:
    call screen scalpel_orientation

label put_blade:
    if orientation == 'correct':
        scene scalpel_unwrap
        "Placing the blade onto the scalpel..."
        scene table
        call screen pick_scalpel
    else:
        "Incorrect orientation, try again."
        call screen scalpel_orientation

screen pick_scalpel:
    hbox:
        xalign 0.5 yalign 0.75
        imagebutton:
            idle "scalpel_collect"
            hover "scalpel_collect_hover"
            action [Function(set_cursor, 'scalpel'), Jump('check_scalpel')]

label check_scalpel:
    scene close_paint
    "Some layers are difficult to distinguish, so we must confirm their presence with a scalpel."
    "Holding the scalpel at approximately 45°, relative to the paint fragment, begin to carefully scrape each layer."
    "Click through each of the layers to perform this action."
    $ layer1_clicked = False
    $ layer2_clicked = False
    $ layer3_clicked = False
    $ layer4_clicked = False
    call screen check_layers

label layer_check_call:
    if layer1_clicked == False or layer2_clicked == False or layer3_clicked == False or layer4_clicked == False:
        call screen check_layers
    else:
        $ default_mouse = ''
        $ current_cursor = ''
        "All done! We can now run our evidence through the database analysis."
        jump pre_options

# TODO: implement mousing for tools
# implement timers for fumigation
# "All done! We can now run our evidence through the database analysis."
return
