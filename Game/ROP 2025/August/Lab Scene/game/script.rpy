default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default location = "hallway"
default selected_elements = []
default element_selection_message = ""

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]
# default correct_dfo_mixture = {"dfo", "hfe", "acetic acid", "methanol"}
# default player_dfo_mixture = {}
# default player_tool = ""
define s = Character(name=("Nina"), image="nina")

init python:
    
    def hide_all_inventory():
        renpy.hide_screen("full_inventory")
        renpy.hide_screen("inventory")
        renpy.hide_screen("toolbox")
        renpy.hide_screen("inv_buttons")
        renpy.hide_screen("close_inv")
        renpy.hide_screen("toolboxpop")
        renpy.hide_screen("inventoryItemMenu")
        renpy.hide_screen("toolboxItemMenu")
        renpy.hide_screen("toolboxPopItemMenu")
        renpy.hide_screen("inspectItem")

    def toolbox_actions(item: str) -> None:
        print("Toolbox action initiated with item:", item)
        global tool
        global ready_to_mix
        global ready_to_digest
        
        # DFO mixing reagents
        if ready_to_mix:
            hide_all_inventory()
            if item == "methanol":
                tool = "methanol"
                renpy.hide_screen("full_inventory")
                renpy.jump("pour_methanol")
            elif item == "dfo":
                tool = "dfo"
                renpy.jump("pour_dfo")
            elif item == "acetic_acid":
                tool = "acetic acid"
                renpy.jump("pour_acetic_acid")
            elif item == "hfe":
                tool = "hfe"
                renpy.jump("pour_hfe")
        
        # Digestion reagents
        if ready_to_digest:
            hide_all_inventory()
            if item == "nitric_acid":
                tool = "nitric acid"
                renpy.hide_screen("full_inventory")
                renpy.jump("pour_nitric_acid")
            elif item == "hydrofluoric_acid":
                tool = "hydrofluoric acid"
                renpy.jump("pour_hydrofluoric_acid")
            elif item == "hydrogen_peroxide":
                tool = "hydrogen peroxide"
                renpy.jump("pour_hydrogen_peroxide")
        
        # Dilution process
        if ready_to_dilute:
            print("Dilution process initiated with item:", item)
            hide_all_inventory()
            if item == "deionized_water":
                tool = "deionized water"
                renpy.hide_screen("full_inventory")
                renpy.jump("add_deionized_water")
    
    def inventory_actions(item: str) -> None:
        global location
        global gin
        global pills
        global imported_print
        global pressed

        if item == "gin":
            if location == "fumehood" and not gin.processed:
                hide_all_inventory()
                renpy.jump("fumehood_bottle")
        elif item == "label" or item == "baked_label":
            label_function_alt()
        elif item == "pills":
            if location == "grinder" and not pills.processed:
                hide_all_inventory()
                renpy.jump("grinder_pills")
        elif item == "grinded_pills":
            if location == "grinder":
                hide_all_inventory()
                renpy.jump("bottle_filling")
        elif item == "teflon_pills":
            if location == "mds":
                hide_all_inventory()
                renpy.jump("microwave_digestion_step1")  # 进入微波消解第一步
        elif item == "digested_sample":
            if location == "dilute":
                hide_all_inventory()
                renpy.jump("transfer_to_polypropylene")  # 转移到聚丙烯容器
        elif item == "diluted_sample":
            if location == "analytical_instruments":
                hide_all_inventory()
                print("进入ICP分析")
                renpy.jump("icp_analysis")  # 进入ICP分析
        elif item == "fingerprint":
            if location == "afis" and pressed == "import":
                imported_print = "print_1"
                renpy.jump("import_print")

# Non-inventory related functions -----------------------------------
    config.mouse = {
        "default": [("cursor.png", 0, 0)],
        "dropper": [("dropper.png", 0, 49)],
        "dropper filled": [("dropper filled.png", 0, 49)],
        "hand": [("default_hand.png", 0, 0)]
    }

    default_mouse = "default"

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def analyzed_everything() -> None:
        return prints["print_1"].processed and prints["print_4"].processed
    
    def check_all_reagents_added():
        global reagents_added
        return all(reagents_added.values())
    
    def toggle_element(element):
        global selected_elements, element_selection_message
        if element in selected_elements:
            selected_elements.remove(element)
            element_selection_message = f"{element} deselected from analysis."
        else:
            selected_elements.append(element)
            element_selection_message = f"{element} selected for analysis."
        # Clear message after a short time
        renpy.restart_interaction()
    
    def clear_element_message():
        global element_selection_message
        element_selection_message = ""
        renpy.restart_interaction()
    
    def set_timer(item: str):
        item = False
    
    def disable_timer(item: str):
        item = True

    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)

    def close_menu():
        if renpy.get_screen("casefile_physical"):
            renpy.hide_screen("casefile_physical")
        elif renpy.get_screen("casefile_photos"):
            renpy.hide_screen("casefile_photos")
        elif renpy.get_screen("casefile"):
            renpy.hide_screen("casefile")
        else:
            renpy.show_screen("casefile")

    
    class Evidence:
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
    screwdriver = Evidence(name = 'screwdriver',
                        afis_details = {
                            'image': 'screwdriver_fingerprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '70'})
    
    ### declare afis relevant evidence
    afis_evidence = [laptop_fingerprint, screwdriver]

    ### set current_evidence to track which evidence is currently active
    current_evidence = screwdriver


#################################### START #############################################
label start:
    # Dial variables
    $ dial_image = "images/dial.png"
    $ dial_size = (660 / 2, 660 / 2)
    $ t = Transform(child = dial_image, zoom = 0.5)
    $ dial_sprite_manager = SpriteManager(event = dial_events)
    $ dial_sprite = dial_sprite_manager.create(t)
    $ dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
    $ dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
    $ dial_rotate = False
    $ dial_sprite.rotate_amount = 0
    $ dial_offset = 68.2
    $ dial_start_rotate = False
    $ dial_number = 0
    $ dial_text = 0
    $ previous_dial_text = 0
    $ dial_changed = False

    # Other variables
    $ old_mousepos = (0.0, 0.0)
    $ degrees = 0
    $ old_degrees = 0
    $ combinations = {"safe_1" : 50, "safe_2" : [23, 5, 75, 44]}
    $ completed_combination_numbers = {}
    $ combination_check = None
    $ current_safe = 1
    $ combination_length = 0
    scene entering_lab_screen
    with Dissolve(1.5)

label lab_hallway_intro:  
    scene lab_hallway_idle
    show nina normal1 

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

    # python code block
    python:
        addToToolbox(["nitric_acid","hydrofluoric_acid","hydrogen_peroxide","deionized_water"])
        addToInventory(["pills"])
        ready_to_digest = False
        ready_to_dilute = False
        # Track reagent addition status
        reagents_added = {
            "nitric_acid": False,
            "hydrofluoric_acid": False, 
            "hydrogen_peroxide": False
        }


    # scene scene-1-bg at half_size - sets background image, don't need rn

label hallway:
    $ location = ""
    $ hide_all_inventory()
    scene lab_hallway_idle
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    call screen lab_hallway_screen

label data_analysis_lab:
    $ location = ""
    hide screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('hallway') onlayer over_screens  
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen onlayer over_screens
    hide screen full_inventory
    show screen back_button_screen('data_analysis_lab') onlayer over_screens  
    call screen afis_screen

label materials_lab:
    $ location = ""
    $ hide_all_inventory()
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label wet_lab:
    $ location = ""
    show screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    show screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

label mds:
    $ location = "mds"
    show screen full_inventory
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene expression "materials_lab/mds_idle.png"
    
    "Click on the Teflon digestion vessel to start the microwave digestion process."
    
    call screen full_inventory

label end:
    hide screen back_button_screen onlayer over_screens
    show nina normal1 
    s "It looks like you've analyzed all the evidence. Great work!"
    s "I hope you took note of the results. Tomorrow, you'll be testifying in court about your findings."
    show nina normal3 
    s "But for now, give yourself a pat on the back and go get some rest!"
    return

# Microwave Digestion System - Three Step Process
label microwave_digestion_step1:
    scene expression "materials_lab/mds_idle.png"
    show screen back_button_screen('mds') onlayer over_screens
    
    "Step 1 of 3: Setting up the first microwave digestion cycle."
    "Please select the correct power and time settings for the first step:"
    
    menu:
        "5 minutes @ 150W":
            "Incorrect! This power is too low and time too short for effective digestion."
            jump microwave_digestion_step1
        
        "10 minutes @ 250W":
            "Correct! Starting the first digestion cycle: 10 minutes @ 250W"
            jump microwave_digestion_step2
        
        "15 minutes @ 300W":
            "Incorrect! This would be too intense for the initial digestion step."
            jump microwave_digestion_step1

label microwave_digestion_step2:
    scene expression "materials_lab/mds_idle.png"
    show screen back_button_screen('mds') onlayer over_screens
    
    "Step 1 completed successfully! The sample has been partially digested."
    "Step 2 of 3: Setting up the second microwave digestion cycle."
    "Please select the correct power and time settings for the second step:"
    
    menu:
        "10 minutes @ 400W":
            "Correct! Starting the second digestion cycle: 10 minutes @ 400W"
            jump microwave_digestion_step3
        
        "8 minutes @ 350W":
            "Incorrect! The power is too low for this intermediate step."
            jump microwave_digestion_step2
        
        "12 minutes @ 450W":
            "Incorrect! This would be too aggressive for the second step."
            jump microwave_digestion_step2

label microwave_digestion_step3:
    scene expression "materials_lab/mds_idle.png"
    show screen back_button_screen('mds') onlayer over_screens
    
    "Step 2 completed successfully! The sample digestion is progressing well."
    "Step 3 of 3: Setting up the final microwave digestion cycle."
    "Please select the correct power and time settings for the final step:"
    
    menu:
        "10 minutes @ 600W":
            "Correct! Starting the final digestion cycle: 10 minutes @ 600W"
            jump microwave_digestion_complete
        
        "8 minutes @ 550W":
            "Incorrect! The time is too short for complete digestion."
            jump microwave_digestion_step3
        
        "12 minutes @ 650W":
            "Incorrect! This power would be too high and could damage the sample."
            jump microwave_digestion_step3

label microwave_digestion_complete:
    scene expression "materials_lab/mds_idle.png"
    show screen back_button_screen('mds') onlayer over_screens
    
    "Excellent! All three digestion cycles completed successfully!"
    "The sample has been completely digested following the proper protocol:"
    "• Step 1: 10 minutes @ 250W"
    "• Step 2: 10 minutes @ 400W" 
    "• Step 3: 10 minutes @ 600W"
    
    "The Teflon digestion vessel now contains a clear, digested sample ready for dilution."
    
    # Add the digested sample to inventory and proceed
    python:
        addToInventory(["digested_sample"])
        teflon_pills.disable_evidence()  # Remove the undigested vessel
    
    "Digested sample added to inventory. Proceeding to dilution step..."
    
    jump dilute

# Step 4: Dilution Process
label dilute:
    $ location = "dilute"
    # Only set ready_to_dilute to False if not already set by transfer process
    if "ready_to_dilute" not in globals() or not ready_to_dilute:
        $ ready_to_dilute = False
    show screen full_inventory
    show screen back_button_screen('mds') onlayer over_screens
    scene expression "materials_lab/dilute_idle.png"
    
    "Step 4: Dilution - Transfer the digested solution to a polypropylene liner"
    if not ready_to_dilute:
        "Click on the digested sample to transfer it to the polypropylene container."
    else:
        "Now click on deionized water in the toolbox to dilute the sample to 50 mL."
    
    call screen full_inventory

# Dilution process animations
label transfer_to_polypropylene:
    scene expression "materials_lab/dilute_idle.png"
    show screen back_button_screen('dilute') onlayer over_screens
    
    $ transfer_x = 435
    $ transfer_y = 251
    
    # Show the digested sample moving to the polypropylene container
    show expression "Inventory Items/Inventory-digested_sample.png" as sample_transfer:
        xpos 100 ypos 100
        linear 2.0 xpos transfer_x ypos transfer_y - 50
        linear 1.0 rotate 15  # Slight tilt for pouring
    
    "Transferring the digested sample to the polypropylene liner..."
    
    # Pouring effect
    show expression "images/liquid_pour.png" as pour_sample:
        xpos transfer_x ypos transfer_y - 30
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide sample_transfer
    hide pour_sample
    
    "Sample successfully transferred to polypropylene container."
    "Now add deionized water to dilute the solution to 50 mL total volume."
    
    $ ready_to_dilute = True
    
    jump dilute

label add_deionized_water:
    $ print("Adding deionized water...")
    scene expression "materials_lab/dilute_idle.png"
    show screen back_button_screen('dilute') onlayer over_screens
    
    $ dilute_x = 435
    $ dilute_y = 251
    
    # Show the deionized water bottle moving to the container
    show expression "Toolbox Items/toolbox-deionized_water.png" as water_bottle:
        xpos 150 ypos 100
        linear 2.0 xpos dilute_x ypos dilute_y - 80
        linear 1.0 rotate 30  # Tilt for pouring
    
    "Adding deionized water to dilute the solution to 50 mL..."
    
    # Pouring effect for water (longer duration)
    show expression "images/liquid_pour.png" as pour_water:
        xpos dilute_x ypos dilute_y - 50
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 3.0 alpha 1.0  # Longer pour for dilution
        linear 0.5 alpha 0.0
    
    hide water_bottle
    hide pour_water
    
    "Excellent! The sample has been diluted to 50 mL with deionized water."
    "The diluted sample is now ready for ICP analysis."
    
    # Replace digested_sample with diluted_sample
    python:
        addToInventory(["diluted_sample"])
        digested_sample.disable_evidence()
        ready_to_dilute = False
    
    show nina normal1
    s "Perfect! Sample preparation is complete."
    s "Now let's head back to the materials lab to access the analytical instruments for ICP analysis."
    
    jump materials_lab

# ICP Analysis System
label icp_analysis:
    $ location = "icp"
    # show screen full_inventory
    show screen back_button_screen('analytical_instruments') onlayer over_screens
    scene expression "materials_lab/ICP_periodic_idle.png"
    
    "ICP Analysis: Click on elements in the periodic table to analyze their concentration in the sample."
    "Click an element once to select it, click again to deselect."
    
    # Initialize selected elements tracking
    python:
        if "selected_elements" not in globals():
            selected_elements = []
    
    show screen icp_periodic_table

# ICP Periodic Table Screen with Hotspots
# ICP Analysis Results
label icp_results:
    scene expression "materials_lab/ICP_periodic_idle.png"
    show screen back_button_screen('analytical_instruments') onlayer over_screens
    
    "ICP Analysis Results:"
    "Analyzing selected elements: [', '.join(selected_elements)]"
    
    # Generate random concentrations for demonstration
    python:
        analysis_results = {}
        import random
        for element in selected_elements:
            concentration = round(random.uniform(0.1, 100.0), 2)
            analysis_results[element] = concentration
    
    "Analysis complete! Results:"
    
    python:
        result_text = ""
        for element, concentration in analysis_results.items():
            result_text += f"{element}: {concentration} ppm\n"
    
    "[result_text]"
    
    show nina normal1
    s "Excellent work! You've successfully completed the ICP analysis."
    s "These concentration values will be important for your forensic report."
    
    # Mark analysis as complete
    python:
        diluted_sample.processed = True
        addToInventory(["icp_results"])
    
    "ICP analysis results added to inventory."
    
    jump analytical_instruments