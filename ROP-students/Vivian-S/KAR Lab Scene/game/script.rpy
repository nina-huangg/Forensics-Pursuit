default current_cursor = ''
default show_case_files = False
default show_toolbox = False

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]

define config.mouse = { }
define config.mouse['default'] = [ ( "five.png", 0, 0) ]
define config.mouse['pressed_default'] = [ ( "grab.png", 0, 0) ]
define config.mouse['button'] = [ ( "grab.png", 0, 0) ]

init python:
    # define return mouse function under initializer
    def return_mouse_pos():
            return renpy.get_mouse_pos()
    
    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)
    
    class Evidence:
        def __init__(self, name, afis_details):
            self.name = name
            self.afis_details = afis_details
            self.processed = False
    
    ### declare each piece of evidence
    tapeglo_fingerprint = Evidence(name = 'tapeglo_fingerprint',
                                afis_details = {
                                    'image': 'tapeglo_fingerprint',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})
    jar_fingerprint = Evidence(name = 'jar_fingerprint',
                        afis_details = {
                            'image': 'jar_fingerprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '70'})
    
    ### declare afis relevant evidence
    afis_evidence = [tapeglo_fingerprint, jar_fingerprint]

    ### set current_evidence to track which evidence is currently active
    current_evidence = jar_fingerprint


#################################### START #############################################
label start:
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
    $inventory_item_names = ["Tape on acetate", "Tapeglo in bag", "Tape photo", "Duct tape tapeglo", "Distilled water", "Tape in tweezers", "Duct tape", "Tapeglo", "Fingerprint on card", "Backing card","Scalebar", "Lifting tape", "Jar photo", "Lid in tweezers", "Camel brush", "Lid with soot", "Lid", "Camphor smoke", "Lighter", "Tweezers", "Gloves box", "Evidence bag", "Jar in bag", "Tape in bag", "Pvs in bag"] # holds names for inspect pop-up text 
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
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
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
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
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

    $is_lid = False

    $all_pieces = 0

    scene entering_lab_screen
    with Dissolve(1.5)

label lab_hallway_intro:
    python:
        addToToolbox(["gloves_box"])
        addToToolbox(["camphor_smoke"])
        addToToolbox(["lighter"])
        addToToolbox(["tweezers"])
        addToToolbox(["camel_brush"])
        addToInventory(["lid"])
        addToInventory(["duct_tape"])
        addToToolbox(["scalebar"])
        addToToolbox(["lifting_tape"])
        addToToolbox(["tapeglo"])
        addToToolbox(["distilled_water"])
        # addToToolbox(["camera"])
        # addToToolbox(["lid_in_tweezers"])
    show screen full_inventory
    # show screen case_files_screen onlayer over_screens 
    # show screen toolbox_button_screen onlayer over_screens     
    scene lab_hallway_idle
    "Welcome to the lab!"
    "This is where you will spend time analyzing the evidence you have collected."
    "Let's get started!"

label hallway:
    call screen lab_hallway_screen

label data_analysis_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen data_analysis_lab_screen

label afis:
    scene software_interface
    "Welcome to the data analysis lab!"
    "Let's analyze the evidence we just processed."
    "To begin, let's import the image of the lid."
    call screen new_afis_screen

label materials_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label wet_lab:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

# My CODE ----------------------------

label processing_fingerprint:
    scene software_interface
    image loading:
        animation
        "data_analysis_lab/load1.png"
        0.3
        "data_analysis_lab/load2.png"
        0.3
        "data_analysis_lab/load3.png"
        0.3
        "data_analysis_lab/load4.png"
        0.3
        "data_analysis_lab/load5.png"
    show loading at custom_position(0.496, 0.23)
    pause 2.0
    "Great job! Now let's process the Tapeglo image!"
    hide screen lid_image
    hide loading
    hide screen import_image 
    call screen tapeglo_afis

label processing_fingerprint2:
    scene software_interface
    image loading:
        animation
        "data_analysis_lab/load1.png"
        0.3
        "data_analysis_lab/load2.png"
        0.3
        "data_analysis_lab/load3.png"
        0.3
        "data_analysis_lab/load4.png"
        0.3
        "data_analysis_lab/load5_other.png"
    show loading at custom_position(0.496, 0.23)
    pause 2.0
    "We have now analyzed both fingerprints!"
    "Hmm... looks like we've done everything we need to do."
    "What should we do now?"
    "..."
    "Time to go to the courtroom!"
    return


label analyze_evidence:
    show screen back_button_screen('wet_lab') onlayer over_screens
    call screen analyze_evidence_screen

label mason_jar:
    show screen back_button_screen('analyze_evidence') onlayer over_screens
    call screen mason_jar_screen

label duct_tape:
    show screen back_button_screen('analyze_evidence') onlayer over_screens
    call screen duct_tape_screen

label which_technique2:
    show screen back_button_screen('duct_tape') onlayer over_screens
    scene fumehood
    show black_bg
    pass

menu:
    "TapeGlo": 
        jump choices1_b
    "Camphor Smoke":
        jump choices2_b
    "Polyvinylsiloxane":
        jump choices3_b

label choices1_b:
    "That's right!"
    "This is your lab station. Here's where you will be performing the procedure to analyze the evidence."
    "To start things off, we need to put on some protective wear before proceeding."
    jump tapeglo_start  

label choices2_b:
    "This might be better used with a smooth surface!"
    jump duct_tape

label choices3_b:
    "This might be better used on imprints on surfaces."
    jump duct_tape   


label which_technique:
    show screen back_button_screen('mason_jar') onlayer over_screens
    scene fumehood
    show black_bg
    pass

menu:
    "TapeGlo": 
        jump choices1_a
    "Camphor Smoke":
        jump choices2_a
    "Polyvinylsiloxane":
        jump choices3_a

label choices1_a:
    "This might be better used with a sticky surface!"
    jump mason_jar

label choices2_a:
    "That's right!"
    "This is your lab station. Here's where you will be performing the procedure to analyze the evidence."
    "To start things off, we need to put on some protective wear before proceeding."
    jump camphor_smoke  

label choices3_a:
    "This might be better used on imprints on surfaces."
    jump mason_jar   

label camphor_smoke:
    show screen back_button_screen('which_technique') onlayer over_screens
    scene fumehood
    jump setupCamphor
    # call screen camphor_smoke_screen

label tapeglo_start:
    show screen back_button_screen('which_technique') onlayer over_screens
    scene fumehood
    jump setupTapeglo

# sets up environment items for first scene - you may add scenes as necessary
label setupTapeglo:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    $environment_items = ["hands1"]

    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            if item == "hands1":
                environment_sprites[-1].width = 2400 / 2
                environment_sprites[-1].height = 1045 / 2
                environment_sprites[-1].x = 345.6
                environment_sprites[-1].y = 570
        
    # scene scene-1-bg at half_size
    call screen scene1

label setupTapeglo2:
    show blue_tray at custom_position(0.3, 0.65)

    hide screen gloved1

    # --------- ADDING ENVIRONMENT ITEMS ---------
    $environment_items = ["blue_tray"]

    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            if item == "blue_tray":
                environment_sprites[-1].width = 700
                environment_sprites[-1].height = 277
                environment_sprites[-1].x = 576
                environment_sprites[-1].y = 702
        
    # scene scene-1-bg at half_size
    "Let's begin by placing the duct tape in the tray"
    hide blue_tray
    call screen scene1

# sets up environment items for first scene - you may add scenes as necessary
label setupCamphor:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    $environment_items = ["hands"]

    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            if item == "hands":
                environment_sprites[-1].width = 2400 / 2
                environment_sprites[-1].height = 1045 / 2
                environment_sprites[-1].x = 345.6
                environment_sprites[-1].y = 570
        
    # scene scene-1-bg at half_size
    call screen scene1

label setupCamphor2:
    
    show evidence_sign at custom_position(0.68, 0.57)
    show silver_tray at custom_position(0.34, 0.65)
    show evidence_tray at custom_position(0.68, 0.69)

    hide screen gloved

    # --------- ADDING ENVIRONMENT ITEMS ---------
    $environment_items = ["silver_tray", "evidence_tray"]

    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            if item == "silver_tray":
                environment_sprites[-1].width = 1061 / 2
                environment_sprites[-1].height = 716 / 2
                environment_sprites[-1].x = 650
                environment_sprites[-1].y = 700
            elif item == "evidence_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178
                environment_sprites[-1].x = 1300
                environment_sprites[-1].y = 750
                # xpos 0.25 ypos 0.3
        
    # scene scene-1-bg at half_size
    "Right in front of you is a tray you can place items on."
    "On the right is a tray for you to place your evidence for processing."
    "To start things off, go to the evidence bar and place the piece of evidence on the tray marked 'Evidence'."
    hide silver_tray
    hide evidence_tray
    call screen scene1

label tape_in_tray_label:

    show blue_tray at custom_position(0.3, 0.65)

    $environment_items = ["tape_in_tray"]
    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image

            if item == "tape_in_tray":
                environment_sprites[-1].width = 700
                environment_sprites[-1].height = 277
                environment_sprites[-1].x = 576
                environment_sprites[-1].y = 702
    
    "Nice work! Now let's pour TapeGlo fluid into the container."
    # scene scene-1-bg at half_size
    call screen scene1


label lid_on_tray_label:
    $environment_items = ["silver_tray", "evidence_tray", "lid_on_tray"]
    $is_lid = True
    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image

            if item == "lid_on_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178
                if is_lid == True:         
                    environment_sprites[-1].x = 1300
                    environment_sprites[-1].y = 750
                else:
                    environment_sprites[-1].x = 0
                    environment_sprites[-1].y = 3000
            elif item == "evidence_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178
                if is_lid == False:         
                    environment_sprites[-1].x = 1300
                    environment_sprites[-1].y = 750
                else:
                    environment_sprites[-1].x = 0
                    environment_sprites[-1].y = 3000
            elif item == "silver_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178
                environment_sprites[-1].x = 4000
                environment_sprites[-1].y = 4000
    
    hide evidence_tray
    show silver_tray at custom_position(0.34, 0.65)
    show lid_on_tray at custom_position(0.68, 0.69)
    "Nice work! Now, it looks like we might have to light something on fire..."
    hide lid_on_tray
    hide silver_tray
    # scene scene-1-bg at half_size
    call screen scene1


label setupCamphor3:

    
    
    # --------- ADDING ENVIRONMENT ITEMS ---------
    $environment_items = ["silver_tray", "evidence_tray", "camphor_cube", "lid_on_tray"]

    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            
            if item == "camphor_cube":
                environment_sprites[-1].width = 672 / 2
                environment_sprites[-1].height = 648 / 2
                environment_sprites[-1].x = 844.8
                environment_sprites[-1].y = 800
            elif item == "lid_on_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178     
                # environment_sprites[-1].x = 1300
                environment_sprites[-1].x = 3000
                environment_sprites[-1].y = 750
            elif item == "silver_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178
                environment_sprites[-1].x = 4000
                environment_sprites[-1].y = 4000
            elif item == "evidence_tray":
                environment_sprites[-1].width = 300
                environment_sprites[-1].height = 178
                environment_sprites[-1].x = 0
                environment_sprites[-1].y = 3000

    # show camphor_cube at custom_position(0.44, 0.74) 
    # scene scene-1-bg at half_size
    call screen scene1

   
transform custom_position(x, y):
    xpos x
    ypos y

    
label pour_tapeglo:
    image tapeglo_pouring:
        animation
        "materials_lab/wet_lab/tapeglo/tapeglo1.png"
        0.1
        "materials_lab/wet_lab/tapeglo/tapeglo2.png"
        0.1
        "materials_lab/wet_lab/tapeglo/tapeglo3.png"
        0.5
    image tray_filling:
        animation
        "materials_lab/wet_lab/tapeglo/tray1.png"
        0.1
        "materials_lab/wet_lab/tapeglo/tray2.png"
        0.1
        "materials_lab/wet_lab/tapeglo/tray3.png"
        0.5
    show tray_filling at custom_position(0.3, 0.65)
    show tapeglo_pouring at custom_position(0.5, 0.45)
    pause 0.5
    hide tapeglo_pouring

label time_set:
    "Great job! Now let's let the Tapeglo set. How long should we set the timer for?"
    
menu:
    "15-20 seconds": 
        jump choices1_d
    "10-15 seconds":
        jump choices2_d
    "30-35 seconds":
        jump choices3_d

label choices1_d:
    "That's right!"
    show dry_timer at custom_position(0.7, 0.5)
    pause 0.9
    jump timer_completed  

label choices2_d:
    "That might be too short!"
    jump time_set

label choices3_d:
    "That might be too long!"
    jump time_set   

    # # TODO: Input min and max times. If there is no min then input all 0 for min values, and if there is no max then input 9 for all max values.
    # # Example values are for 7min 50sec and 10min 10sec.
    # $ min_hours = 0 # TODO: Replace this with your own value.
    # $ min_minutes = 7 # TODO: Replace this with your own value.
    # $ min_seconds = 15 # TODO: Replace this with your own value.
    # $ max_hours = 0 # TODO: Replace this with your own value.
    # $ max_minutes = 7 # TODO: Replace this with your own value.
    # $ max_seconds = 20 # TODO: Replace this with your own value.

    # # Calculations
    # $ min_time = min_hours * 3600 + min_minutes * 60 + min_seconds
    # $ max_time = max_hours * 3600 + max_minutes * 60 + max_seconds
    # $ true_time = time_numbers[5] + time_numbers[4] * 10 + time_numbers[3] * 60 + time_numbers[2] * 600 + time_numbers[1] * 3600 + time_numbers[0] * 36000

    # # Default messsages, customize to your liking
    # if true_time >= min_time and true_time <= max_time:
    #     "That's correct."
    #     $ string_min_1 = "%d" % time_numbers[2]
    #     $ string_min_2 = "%d" % time_numbers[3]
    #     $ string_sec_1 = "%d" % time_numbers[4]
    #     $ string_sec_2 = "%d" % time_numbers[5]
    #     if string_min_1 == "0":
    #         if string_sec_1 != "0":
    #             "Waiting for [string_min_2] minutes and [string_sec_1][string_sec_2] seconds..."
    #         elif string_sec_2 != "0":
    #             "Waiting for [string_min_2] minutes and [string_sec_2] seconds..."
    #         else:
    #             "Waiting for [string_min_2] minutes..."
    #     else:
    #         if string_sec_1 != "0" and string_sec_2 != "0":
    #             "Waiting for [string_min_1][string_min_2] minutes and [string_sec_1][string_sec_2] seconds..."
    #         elif string_sec_2 != "0":
    #             "Waiting for [string_min_1][string_min_2] minutes and [string_sec_2] seconds..."
    #         else:
    #             "Waiting for [string_min_1][string_min_2] minutes..."
    #     jump timer_completed
    # elif true_time < min_time:
    #     "That's not enough time, try again."
    #     jump timer
    # elif true_time > max_time:
    #     "That's too much time, try again."
    #     jump timer

    # pause
    # pause

label timer_completed:
    show dry_timer
    scene fumehood
    show tray3 at custom_position(0.3, 0.65)
    "Nice! Now we can remove the tape using some tweezers!"
    call screen remove_tape


label tape_removed:
    hide tray3
    show tray_no_tape at custom_position(0.3, 0.65)
    python:
        addToToolbox(["tape_in_tweezers"])
        renpy.show_screen("inspectItem", ["tape_in_tweezers"])

label distilled_water:
    "Now let's wash off the Tapeglo using some distilled water!"
    "Hold the tape over the container and spray distilled water on it to remove excess residue."
    hide tray_no_tape
    call screen spray_water

label water_sprayed:  
    show squirt at custom_position(0.5, 0.5)
    with Dissolve(0.5)
    hide squirt
    show tray_no_tape at custom_position(0.3, 0.65)
    show tape1 at custom_position(0.4, 0.4)
    "Click the distilled water bottle to spray the tape!"
    call screen spray_water2

label water_sprayed2:
    show squirt at custom_position(0.5, 0.5)
    with Dissolve(0.5)
    hide squirt
    hide tape1
    show tape2 at custom_position(0.4, 0.4)
    call screen spray_water3

label water_sprayed3:
    show squirt at custom_position(0.5, 0.5)
    with Dissolve(0.5)
    hide squirt
    hide tape2
    show tape3 at custom_position(0.4, 0.4)
    "That seems to be enough!"
    python:
        addToInventory(["duct_tape_tapeglo"])
        renpy.show_screen("inspectItem", ["duct_tape_tapeglo"])
    hide tape3
    "Awesome job! Now let's move to a lab bench where we will fluoresce the piece of tape."

label lab_bench:
    scene lab_bench1
    call screen paper_towel

label air_dry:
    image dry_timer:
        animation
        "timer1.png"
        0.1
        "timer2.png"
        0.1
        "timer3.png"
        0.1
        "timer4.png"
        0.1
        "timer5.png"
        0.1
        "timer6.png"
        0.1
        "timer7.png"
        0.1
        "timer8.png"
        0.1
        "timer9.png"
        0.1
        "timer10.png"
    python:
        removeInventoryItem(inventory_sprites[inventory_items.index("duct_tape_tapeglo")])
    show towel_with_tape at custom_position(0.3, 0.2)
    "Now let's air-dry this for a few seconds."
    show dry_timer at custom_position(0.7, 0.5)
    pause 0.9
    hide dry_timer

label fluoresce:
    "Now let's flouresce the tape!"
    "Remind me, how many nanometers should we flouresce the tape with?"

menu:
    "630nm - 730nm": 
        jump choices1_c
    "300nm - 400nm":
        jump choices2_c
    "450nm – 530nm":
        jump choices3_c

label choices1_c:
    "Hmm, that might be a bit too high. Let's try again!"
    jump tapeglo_start  

label choices2_c:
    "Hmm, that might be a bit too low. Let's try again!"
    jump duct_tape

label choices3_c:
    "That's right! Now let's flouresce!"
    window hide
    show orange_filter
    pause 5.0
    show screen dark_overlay_with_mouse
    "Look at those fingerprints! Maybe we should photograph this for further analysis."
    

# FLOURESCE STUFF ---------------------

label photograph_tape:
    hide screen dark_overlay_with_mouse
    show screen camera_screen2 onlayer over_screens
    pause
    pause

label take_picture2:
    show camera_flash onlayer over_screens
    with Dissolve(0.5) 
    hide camera_flash onlayer over_screens
    hide camera_screen2 onlayer over_screens
    hide orange_filter
    hide towel_with_tape
    jump collect_tape_photo

label collect_tape_photo:
    python:
        addToInventory(["duct_tape_tapeglo"])
        addToInventory(["tape_photo"])
        renpy.show_screen("inspectItem", ["tape_photo"])
    "Last but not least, let's preserve the tape exhibit on a piece of acetate sheet and re-package it!"
    call screen acetate

label collect_acetate:
    python:
        removeInventoryItem(inventory_sprites[inventory_items.index("duct_tape_tapeglo")])
    call screen collect_acetate_screen

label pack_tape:
    python:
        addToInventory(["tape_on_acetate"])
        renpy.show_screen("inspectItem", ["tape_on_acetate"])
    "Finally, let's package this up in a tamper-seal bag!"
    show screen package_screen2
    pause
    pause

label packaged2:
    python:
        addToInventory(["tapeglo_in_bag"])
        renpy.show_screen("inspectItem", ["tapeglo_in_bag"])
    hide screen package_screen2
    jump done2

label done2:
    hide black_bg
    show screen back_button_screen('wet_lab') onlayer over_screens
    "And... we're done! Great job!"
    "Click the back button to analyze more evidence!"
    pause
    pause
    pause
    

label lit_cube:
    
    # jump evidence_tray
    image smoke:
        animation
        "materials_lab/wet_lab/smoke1.png"
        0.15
        "materials_lab/wet_lab/smoke2.png"
        0.15
        "materials_lab/wet_lab/smoke3.png"
        0.15
        "materials_lab/wet_lab/smoke4.png"
        0.15
        "materials_lab/wet_lab/smoke5.png"
        repeat
    image fire:
        animation
        "materials_lab/wet_lab/fire1.png"
        0.1
        "materials_lab/wet_lab/fire2.png"
        0.1
        "materials_lab/wet_lab/fire3.png"
        0.1
        "materials_lab/wet_lab/fire4.png"
        0.1
        "materials_lab/wet_lab/fire5.png"
        repeat
    
    # python:
    #     removeEnvironmentItem(environment_sprites[environment_items.index("camphor_cube")])
    show silver_tray at custom_position(0.34, 0.65)
    show camphor_cube at custom_position(0.44, 0.74)
    show smoke at custom_position(0.46, 0.65)
    show fire at custom_position(0.46, 0.72)
    show lid_on_tray at custom_position(0.68, 0.69)
    pause
    pause
    pause
    

label too_close:
    show too_close at custom_position(0.5, 0.5)
    pause 1.0
    hide too_close
    pause
    pause

label perfect:
    image bars:
        animation
        "bars/bar1.png"
        1.0
        "bars/bar2.png"
        1.0
        "bars/bar3.png"
        1.0
        "bars/bar4.png"
        1.0
        "bars/bar5.png"
        1.0
        "bars/bar6.png"
        1.0
        "bars/bar7.png"
        1.0
        "bars/bar8.png"
        1.0
        "bars/bar9.png"
        1.0
        "bars/bar10.png"
        1.0
        "bars/bar11.png"
        1.0
    show bars at custom_position(0.2, 0.1)
    pause 10.0
    hide too_close
    hide bars
    python:
        item = toolbox_sprites[toolbox_items.index("lid_in_tweezers")]
        item.x = item.original_x
        item.y = item.original_y
        item.zorder = 0
        # addToToolbox(["lid_with_soot"])
        # renpy.show_screen("inspectItem", ["lid_with_soot"])
    "Now let's extinguish the fire."
    call screen extinguisher_screen
        
label extinguished:
    hide fire
    hide smoke
    "Great! The fire is now out!"
    "Hmm, looks like there's some soot on the lid... maybe we should brush it off."
    python:
        # environment_sprites.pop(environment_sprites.index("silver_tray"))
        removeEnvironmentItem(environment_sprites[environment_items.index("silver_tray")])
        # removeEnvironmentItem(environment_sprites[environment_items.index("camphor_cube")])
        # removeEnvironmentItem(environment_sprites[environment_items.index("camphor_cube")])
        removeEnvironmentItem(environment_sprites[environment_items.index("lid_on_tray")])
        for item in environment_sprites:
            if item.type == "camphor_cube":
                removeEnvironmentItem(item)
        # removeEnvironmentItem(environment_sprites[environment_items.index("evidence_tray")])  
    jump dust_lid


label dust_lid:

    show black_bg
    show lid_fingerprint
    
    # show screen dust_lid_screen onlayer over_screens

    $environment_items = ["piece1", "piece2", "piece3", "piece4"]

    python:
        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------

            if item == "piece1":
                environment_sprites[-1].width = 551
                environment_sprites[-1].height = 506
                environment_sprites[-1].x = 700
                environment_sprites[-1].y = 200
            elif item == "piece2":
                environment_sprites[-1].width = 576
                environment_sprites[-1].height = 461
                environment_sprites[-1].x = 680
                environment_sprites[-1].y = 400
            elif item == "piece3":
                environment_sprites[-1].width = 397
                environment_sprites[-1].height = 323
                environment_sprites[-1].x = 700
                environment_sprites[-1].y = 200
            elif item == "piece4":
                environment_sprites[-1].width = 371
                environment_sprites[-1].height = 451
                environment_sprites[-1].x = 900
                environment_sprites[-1].y = 200
    call screen scene1
    pause
    pause
    pause

label test:
    "Wonderful job! Now let's photograph the lid for further analysis."
    window hide
    # pause
    show screen camera_screen onlayer over_screens
    pause 
    pause

label take_picture:
    show camera_flash onlayer over_screens
    with Dissolve(0.5) 
    
    hide camera_flash onlayer over_screens
    hide camera_screen onlayer over_screens
    jump test1

label test1:
    python:
        addToInventory(["jar_photo"])
        renpy.show_screen("inspectItem", ["jar_photo"])
    "Last but not least, we'll need to record the fingerprint somewhere... HINT: the backing card technique!"
    show screen scalebar_screen
    pause
    pause
    pause
    pause
    pause
    pause
    pause

label add_scalebar:
    show screen add_scalebar
    pause
    pause

label add_lifting_tape:
    show screen add_lifting_tape
    pause
    pause

label remove_tape:
    python:
        addToToolbox(["backing_card"])
        renpy.show_screen("inspectItem", ["backing_card"])
    hide lid_fingerprint
    hide screen scalebar_screen
    hide screen add_scalebar
    hide screen add_lifting_tape
    show screen backing_card_screen
    pause
    pause

label collect_backing_card:
    
    python:
        addToToolbox(["fingerprint_on_card"])
        renpy.show_screen("inspectItem", ["fingerprint_on_card"])
        removeToolboxItem(toolbox_sprites[toolbox_items.index("backing_card")])
    hide screen backing_card_screen
    "Finally, let's package this up in a tamper-seal bag!"
    show screen package_screen
    pause
    pause

label packaged:
    python:
        addToInventory(["lid_in_bag"])
        renpy.show_screen("inspectItem", ["lid_in_bag"])
    hide screen package_screen
    jump done

label done:
    hide black_bg
    show screen back_button_screen('wet_lab') onlayer over_screens
    "And... we're done! Great job!"
    "Click the back button to analyze more evidence!"
    pause
    pause
    pause
    
# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5
    

