# Variable for mouse
define config.mouse_displayable = MouseDisplayable("mouse_cursor", 0, 0).add("inspect", "magnifying_glass_cursor", 0, 0).add("knife", "knife_cursor", 0, 0).add("swab", "swab_cursor", 0, 0).add("water", "water_cursor", 0, 0).add("unused_hemastix", "unused_hemastix_cursor", 0, 0).add("negative_result", "negative_result_cursor", 0, 0).add("positive_result", "positive_result_cursor", 0, 0).add("dna_tube", "dna_tube_cursor", 0, 0).add("pipette", "pipette_cursor", 0, 173)

# Variable for flash effect
define flash = Fade(.25, 0, .75, color="#fff")

# Variables to keep track of where the player is
define in_hallway = True
define in_materials_lab = False
define in_data_analysis_lab = False
define at_cyanosafe_machine = False
define at_fumehood = False
define at_lab_bench = False
define in_biology_lab = False
define in_chemistry_lab = False
define at_centrifuge = False
define at_open_centrifuge = False
define at_pcr = False
define at_pcr_tray = False
define at_thermal_cycler = False
define at_amplifier_tray = False
define at_detection_plate = False
define at_plate_centrifuge = False
define at_miseq = False
define viewing_table_of_findings = False
define at_afis = False

# Variables for cyanosafe
define cyanosafe_door_open = False
define close_to_cyanosafe = False
define knife_in_cyanosafe = False
define added_water = False
define added_superglue = False
define ran_cyanosafe = False

# Variables for knife:
define determined_blood_on_knife = False
define sample_collected_from_knife = False
define proper_blood_sample_collected = False
define print_lifted_from_knife = False
define knife_in_fumehood = False
define stain_sprayed_on_knife = False
define als_used_on_knife = False
define photographing_knife = False
define scaled_knife = False
define inspecting_fingerprint = False
define sent_knife_sample_to_be_extracted = False
define warned_player_about_fingerprint_before_swabbing = False
define finished_analyzing_knife_sample = False

# Variables for dish towel
define determined_blood_on_towel = False
define sample_collected_from_towel = False
define sent_towel_sample_to_be_extracted = False
define finished_analyzing_towel_sample = False

# Variables for floor sample
define finished_analyzing_floor_sample = False

# Variables to keep track of what is being held
define holding_towel = False
define holding_knife = False
define holding_knife_lifted_print = False
define holding_knife_stain_sprayed = False
define holding_knife_swab = False
define holding_towel_swab = False
define holding_floor_swab = False
define holding_superglue = False
define holding_distilled_water = False
define holding_basic_yellow = False
define holding_scalebar = False
define holding_450nm_flashlight = False
define holding_incorrect_flashlight = False
define holding_hemastix = False
define holding_swab = False
define holding_incubated_knife_sample = False
define holding_incubated_towel_sample = False
define holding_incubated_floor_sample = False
define holding_pipette = False

# Variables for photos taken
define took_photo_fingerprint_scaled = False
define took_photo_fingerprint_scaled_als = False
define took_photo_hemastix_with_towel = False
define took_photo_hemastix_with_knife = False

# Variables for lab bench
define towel_on_lab_bench = False
define knife_on_lab_bench = False
define hemastix_next_to_towel = False
define hemastix_next_to_knife = False

# Variables for if using hemastix or swabbing
define currently_using_hemastix = False
define currently_swabbing = False
define swab_sample_being_looked_at = ""

define filled_table_of_findings = False

# Variables for fingerprint processing
define ready_to_process_knife_fingerprint = False
define processed_stove_fingerprint = False
define processed_knife_fingerprint = False

init python:
    # For presumptive tests and swabbing for evidence
    class EvidenceNeedingSwabbing:
        def __init__(self, name, hemastix_details):
            # Name of piece of evidence
            self.name = name

            # Details for the hemastix screen including xpos and ypos 
            # along with idle and hover images for rubbing the hemastix on 
            # the piece of evidence and for placing the result next to the piece 
            # of evidence (if result is positive)
            self.hemastix_details = hemastix_details

            # Variables to keep track of what goes on during hemastix test
            self.wet_hemastix = False # If false when rubbing on a dried sample, result is negative
            self.swabbed_object = False
            self.wet_before_swabbed = False
            self.finished_hemastix_test = False # Make true after player conducts first test even if player did it incorrectly

            # Variables to keep track of what hemastix to display
            self.display_unused_hemastix = True
            self.display_wet_hemastix = False
            self.display_negative_result = False
            self.display_positive_result = False

            # Variables to keep track of swabbing variables
            self.wet_swab = False
            self.wet_swab_first = False
            self.swabbed_object_with_swab = False
            self.display_swab = True
            self.display_wet_swab = False

    # define the variables for evidence that requires hemastix
    dish_towel = EvidenceNeedingSwabbing(name = "dish towel", 
                                        hemastix_details = {
                                            'xpos_blood_spot': 0.56666667, 
                                            'ypos_blood_spot': 0.36203704, 
                                            'idle_image_blood_spot': "swab_towel_idle", 
                                            'hover_image_blood_spot': "swab_towel_hover", 
                                            'xpos_place_hemastix': 0.6890625, 
                                            'ypos_place_hemastix': 0.3787037, 
                                            'idle_image_place_hemastix': "place_hemastix_by_towel_idle", 
                                            'hover_image_place_hemastix': "place_hemastix_by_towel_hover"
                                            })

    knife = EvidenceNeedingSwabbing(name = "knife", 
                                    hemastix_details = {
                                        'xpos_blood_spot': 0.4265625,
                                        'ypos_blood_spot': 0.02407407,
                                        'idle_image_blood_spot': "swab_knife_idle",
                                        'hover_image_blood_spot': "swab_knife_hover",
                                        'xpos_place_hemastix': 0.39739583,
                                        'ypos_place_hemastix': 0.0962963,
                                        'idle_image_place_hemastix': "place_hemastix_by_knife_idle",
                                        'hover_image_place_hemastix': "place_hemastix_by_knife_hover"
                                    })

    # Set current_evidence to keep track of which evidence is currently active
    current_evidence = dish_towel

    # Class for dna evidence
    class DNAEvidence:
        def __init__(self, name, concentration_value, required_volume):
            # name of piece of evidence the DNA was from
            self.name = name

            self.holding_pipette = False
            self.holding_distilled_water = False

            # variables for extraction process of DNA
            self.centrifuge_open = False
            self.holding_tube = False
            self.holding_incubated_sample = False
            self.in_centrifuge = False
            self.counterweight_in = False
            self.finished_centrifuge = False

            # variables for PCR and quantification process
            self.viewing_tray = False
            self.holding_extracted_dna = False
            self.dna_sample_in = False
            self.negative_solution_in = False
            self.all_pcr_wells_filled = False
            self.holding_tray = False
            self.pcr_open = False
            self.tray_in_pcr = False
            self.finished_pcr = False
            self.concentration_value = concentration_value
            self.required_volume = required_volume
            self.continuing_with_amplification = True
            self.did_correct_calculation = False

            # variables for amplification process
            self.viewing_amp_plate = False
            self.holding_sample = False
            self.holding_positive_control = False
            self.added_sample_to_amp_plate = False
            self.added_positive_control = False
            self.added_negative_control = False
            self.all_plate_wells_filled = False
            self.thermal_cycler_open = False
            self.plate_in_thermal_cycler = False
            self.finished_amplification = False

            # variables for detection process
            self.viewing_detection_plate = False
            # variables holding_sample, thermal_cycler_open, and plate_in_thermal_cycler are also used here
            self.added_sample_to_det_plate = False
            self.plate_centrifuge_open = False
            self.plate_in_centrifuge = False
            self.plate_on_ice = False
            self.miseq_first_open = False
            self.miseq_second_open = False
            self.plate_in_miseq = False
            self.finished_detection_centrifuge = False
            self.finished_detection_thermal_cycler = False
            self.finished_detection = False

            # variables to keep track of messages displayed
            self.displayed_dna_message = False
            self.displayed_water_message = False

    knife_sample = DNAEvidence("knife", "0.353", "2.85")

    towel_sample = DNAEvidence("towel", "0.014", "71.79")

    floor_sample = DNAEvidence("floor", "0.351", "2.86")

    current_dna_evidence = knife_sample

    class TableofFindings:
        def __init__(self):

            self.first_evidence = None
            self.second_evidence = None
            self.display_add_box = False
            self.holding_knife_electropherogram = False
            self.holding_floor_electropherogram = False

    table_of_findings = TableofFindings()


# The game starts here.

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
    $inventory_item_names = ["ALS Flashlights", "UVA Flashlight", "415nm Flashlight", "450nm Flashlight", "530nm Flashlight", 
    "Distilled Water", "Superglue", "Basic Yellow", "Cotton Swab", "Knife", "Dish Towel", "Hemastix", "Scalebar", 
    "Knife With Lifted Fingerprint", "Knife with Basic Yellow", "Photo Of Fingerprint Scaled", "Photo Of Fingerprint Scaled Wtih 450nm", 
    "Photo Of Hemastix Next To Towel", "Photo Of Hemastix Next To Knife", "Sample From Floor", "Sample From Towel", "Sample From Knife", 
    "Incubated Sample From Blood Pool", "Incubated Sample From Towel", "Incubated Sample From Knife", "Extracted DNA From Knife", 
    "Extracted DNA From Towel", "Extracted DNA From Floor", "Filled Plate", "Fingerprint From Stove", "GF Positive Control", 
    "Electropherogram of Knife Sample", "Electropherogram of Towel Sample", "Electropherogram of Floor Sample"] # holds names for inspect pop-up text 
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

    show screen full_inventory

# sets up environment items for first scene - you may add scenes as necessary
label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        addToInventory(["sample_from_floor", "knife", "dish_towel", "fingerprint_from_stove"])
        addToToolbox(["als_flashlights", "distilled_water", "superglue", "basic_yellow", "cotton_swab", "hemastix", "scalebar", "gf_positive_control"])
        addToToolboxPop(["uva_flashlight", "415nm_flashlight", "450nm_flashlight", "530nm_flashlight"])

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
            if item == "lid":
                environment_sprites[-1].width = 300 / 2
                environment_sprites[-1].height = 231 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 500

label entering_lab:
    scene lab_hallway_idle

    "It's now time to analyze the evidence collected from the crime scene."

    call screen in_hallway

label in_lab_hallway:
    scene lab_hallway_idle
    call screen in_hallway

label back:
    hide screen camera_screen
    if inspecting_fingerprint:
        $ inspecting_fingerprint = False
        jump update_knife_scene
    elif holding_450nm_flashlight:
        $ holding_450nm_flashlight = False
        hide screen back_button
        jump update_knife_scene
    elif holding_incorrect_flashlight:
        $ holding_incorrect_flashlight = False
        hide screen back_button
        jump update_knife_scene
    elif photographing_knife and took_photo_fingerprint_scaled_als and not inspecting_fingerprint:
        $ photographing_knife = False
        hide screen inspect_fingerprint
        jump in_chemistry_lab
    elif viewing_table_of_findings:
        $ viewing_table_of_findings = False
        hide screen profiles
        jump enter_data_analysis_lab
    elif at_afis:
        $ at_afis = False
        jump enter_data_analysis_lab
    elif at_fumehood:
        $ at_fumehood = False
        jump in_chemistry_lab
    elif close_to_cyanosafe:
        $ close_to_cyanosafe = False
        jump cyanosafe_machine
    elif at_cyanosafe_machine:
        $ at_cyanosafe_machine = False
        hide screen open_cyanosafe_door
        hide screen inspect_cyanosafe
        jump in_chemistry_lab
    elif at_lab_bench:
        $ at_lab_bench = False
        jump enter_materials_lab
    elif at_centrifuge:
        $ at_centrifuge = False
        $ at_open_centrifuge = False
        hide screen centrifuge_screen
        jump in_biology_lab
    elif at_pcr_tray:
        $ at_pcr_tray = False
        jump in_biology_lab
    elif at_pcr:
        $ at_pcr = False
        hide screen pcr_screen
        jump in_biology_lab
    elif at_amplifier_tray:
        $ at_amplifier_tray = False
        jump in_biology_lab
    elif at_thermal_cycler:
        $ at_thermal_cycler = False
        hide screen thermal_cycler_screen
        jump in_biology_lab
    elif at_detection_plate:
        $ at_detection_plate = False
        jump in_biology_lab
    elif at_plate_centrifuge:
        $ at_plate_centrifuge = False
        hide screen using_plate_centrifuge
        jump in_biology_lab
    elif at_miseq:
        $ at_miseq = False
        hide screen using_miseq
        jump in_biology_lab
    elif in_biology_lab:
        $ in_biology_lab = False
        show screen full_inventory
        hide screen back_button
        hide screen choose_dna_machine
        hide screen centrifuge_info
        hide screen pcr_info
        hide screen thermal_cycler_info
        hide screen plate_centrifuge_info
        hide screen miseq_machine_info
        jump enter_materials_lab
    elif in_chemistry_lab:
        $ in_chemistry_lab = False
        show screen full_inventory
        hide screen back_button
        hide screen choose_machine
        hide screen fumehood_info
        hide screen cyanosafe_info
        jump enter_materials_lab
    elif in_materials_lab:
        show screen full_inventory
        $ in_materials_lab = False
        hide screen back_button
        hide screen choose_lab
        jump in_lab_hallway
    elif in_data_analysis_lab:
        show screen full_inventory
        $ in_data_analysis_lab = False
        hide screen choose_icon
        hide screen back_button
        jump in_lab_hallway
    else:
        jump in_lab_hallway

# --------------- TIMER CODE -----------------
label timer_set:
    
    scene cyanosafe_closed
    
    $ min_hours = 0
    $ min_minutes = 9
    $ min_seconds = 0
    $ max_hours = 0
    $ max_minutes = 11
    $ max_seconds = 0

    # Calculations
    $ min_time = min_hours * 3600 + min_minutes * 60 + min_seconds
    $ max_time = max_hours * 3600 + max_minutes * 60 + max_seconds
    $ true_time = time_numbers[5] + time_numbers[4] * 10 + time_numbers[3] * 60 + time_numbers[2] * 600 + time_numbers[1] * 3600 + time_numbers[0] * 36000

    # Default messsages, customize to your liking
    if true_time >= min_time and true_time <= max_time:
        call screen correct_time
        jump correct_time
    elif true_time < min_time:
        call screen not_enough_time
        jump timer
    elif true_time > max_time:
        call screen too_much_time
        jump timer
# ----------- END OF TIMER CODE -----------------

label took_photo:
    # Code for the flash effect
    show screen full_inventory
    show transparent with flash
    hide transparent
    hide screen camera_screen
    if holding_450nm_flashlight and photographing_knife:
        if inspecting_fingerprint:
            $ took_photo_fingerprint_scaled_als = True
            $ ready_to_process_knife_fingerprint = True
            python:
                addToInventory(["photo_of_fingerprint_scaled_with_450nm"])
        jump update_knife_scene
    elif not holding_incorrect_flashlight and photographing_knife:
        if inspecting_fingerprint:
            $ took_photo_fingerprint_scaled = True
            python:
                addToInventory(["photo_of_fingerprint_scaled"])
        jump update_knife_scene
    elif towel_on_lab_bench and current_evidence.name == "dish towel" and current_evidence.finished_hemastix_test:
        $ took_photo_hemastix_with_towel = True
        python:
            addToInventory(["photo_of_hemastix_next_to_towel"])
        scene towel_on_lab_bench
        $ currently_using_hemastix = False
    elif knife_on_lab_bench and current_evidence.name == "knife" and current_evidence.finished_hemastix_test:
        $ took_photo_hemastix_with_knife = True
        python:
            addToInventory(["photo_of_hemastix_next_to_knife"])
        scene knife_on_lab_bench
        $ currently_using_hemastix = False
    call screen full_inventory

label dont_need_flashlight:
    show screen full_inventory
    call screen dont_need
    call screen full_inventory

label enter_data_analysis_lab:
    $ in_hallway = False
    $ in_data_analysis_lab = True
    scene data_analysis_bg
    show screen back_button
    show screen choose_icon
    call screen full_inventory

label enter_materials_lab:
    $ in_hallway = False
    $ in_materials_lab = True
    scene materials_lab_dim
    show screen full_inventory
    show screen back_button
    show screen choose_lab
    call screen full_inventory

label in_biology_lab:
    hide screen choose_lab
    scene materials_lab_dim
    $ in_biology_lab = True
    show screen back_button
    show screen choose_dna_machine
    call screen full_inventory

label in_chemistry_lab:
    hide screen choose_lab
    scene materials_lab_dim
    $ in_chemistry_lab = True
    show screen back_button
    show screen choose_machine
    call screen full_inventory

label lab_bench:
    scene empty_lab_bench
    hide screen choose_lab
    hide screen collect_knife_from_lab_bench
    hide screen collect_towel_from_lab_bench
    show screen back_button
    $ at_lab_bench = True
    $ towel_on_lab_bench = False
    $ knife_on_lab_bench = False
    call screen full_inventory

label towel_on_bench:
    scene towel_on_lab_bench
    hide screen back_button
    $ holding_towel = False
    $ towel_on_lab_bench = True
    python:
        current_evidence = dish_towel
    call screen full_inventory

label knife_on_bench:
    hide screen place_knife_on_lab_bench
    scene knife_on_lab_bench
    hide screen back_button
    $ holding_knife = False
    $ knife_on_lab_bench = True
    python:
        current_evidence = knife
    call screen full_inventory

label something_on_bench:
    show screen full_inventory
    call screen something_already_on_lab_bench
    call screen full_inventory

label fumehood:
    hide screen choose_machine
    hide screen fumehood_info
    hide screen cyanosafe_info
    scene fumehood_bg
    show screen back_button
    $ at_fumehood = True

    call screen full_inventory

label knife_in_fumehood:
    hide screen put_knife_in_fumehood
    hide screen back_button
    scene knife_before_spraying
    $ knife_in_fumehood = True
    $ holding_knife_lifted_print = False
    python:
        removeInventoryItem(inventory_sprites[inventory_items.index("knife_with_lifted_fingerprint")])

    call screen full_inventory

label stained_knife:
    scene knife_after_spraying
    show screen full_inventory
    hide screen spray_knife 
    $ stain_sprayed_on_knife = True
    call screen stained_knife
    call screen collect_stained_knife

label collect_knife_from_fumehood:
    python:
        addToInventory(["knife_with_basic_yellow"])
    $ at_fumehood = False
    $ knife_in_fumehood = False
    jump photograph_knife

label photograph_knife:
    scene knife_without_als
    $ photographing_knife = True
    show screen full_inventory
    call screen scalebar_hint
    call screen full_inventory

label update_scale_variable:
    $ scaled_knife = True
    hide screen place_scalebar
    jump update_knife_scene

label update_inspecting_knife_variable:
    $ inspecting_fingerprint = True
    hide screen inspect_fingerprint
    jump update_knife_scene

label update_knife_scene:
    hide screen back_button
    if holding_450nm_flashlight:
        jump correct_als_flashlight
    elif holding_incorrect_flashlight:
        jump incorrect_als_flashlight
    else:
        if inspecting_fingerprint:
            scene knife_scaled_close_without_als
            show screen back_button
            if not took_photo_fingerprint_scaled:
                show screen camera_screen
        elif scaled_knife and not inspecting_fingerprint:
            scene knife_scaled_without_als
            show screen inspect_fingerprint
        else:
            scene knife_without_als
        if took_photo_fingerprint_scaled_als:
            show screen back_button
        call screen full_inventory

label correct_als_flashlight:
    if inspecting_fingerprint:
        scene knife_scaled_close_450nm
        if not took_photo_fingerprint_scaled_als:
            show screen camera_screen
    elif scaled_knife and not inspecting_fingerprint:
        scene knife_scaled_with_450nm
        show screen inspect_fingerprint
    else:
        scene knife_with_450nm
    show screen full_inventory
    call screen back_button

label incorrect_als_flashlight:
    if inspecting_fingerprint:
        scene knife_scaled_close_wrong_light
    elif scaled_knife and not inspecting_fingerprint:
        scene knife_scaled_wrong_light
        show screen inspect_fingerprint
    else:
        scene knife_wrong_light
    show screen full_inventory
    call screen wrong_light
    call screen back_button

label already_using_light:
    show screen full_inventory
    call screen already_using_light
    call screen full_inventory

label cyanosafe_machine:
    hide screen choose_machine
    hide screen fumehood_info
    hide screen cyanosafe_info
    $ at_cyanosafe_machine = True

    if cyanosafe_door_open:
        scene cyanosafe_far_open
        show screen inspect_cyanosafe
    else:
        scene cyanosafe_far_closed
        show screen open_cyanosafe_door
    call screen full_inventory

label open_cyanosafe:
    hide screen open_cyanosafe_door
    $ cyanosafe_door_open = True
    scene cyanosafe_far_open
    show screen inspect_cyanosafe
    call screen full_inventory

label go_closer_to_cyanosafe:
    hide screen inspect_cyanosafe
    $ close_to_cyanosafe = True
    if knife_in_cyanosafe:
        scene cyanosafe_knife
    else:
        scene cyanosafe_open

    if holding_knife:
        show screen place_knife_in_cyanosafe
    elif holding_superglue:
        show screen add_superglue_to_cyanosafe
    elif holding_distilled_water:
        show screen add_water_to_cyanosafe
    call screen full_inventory

label added_item_to_cyanosafe:
    hide screen place_knife_in_cyanosafe
    hide screen add_superglue_to_cyanosafe
    hide screen add_water_to_cyanosafe
    hide screen add_water_before_knife
    hide screen add_superglue_before_knife
    hide screen back_button

    if holding_knife:
        $ holding_knife = False
        $ knife_in_cyanosafe = True
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("knife")])
    elif holding_superglue:
        $ holding_superglue = False
        $ added_superglue = True
        show screen full_inventory
    elif holding_distilled_water:
        $ holding_distilled_water = False
        $ added_water = True
        show screen full_inventory

    if knife_in_cyanosafe and added_superglue and added_water:
        jump ready_to_run_cyanosafe
    else:
        jump go_closer_to_cyanosafe

label ready_to_run_cyanosafe:
    show screen full_inventory
    scene cyanosafe_knife_door
    call screen closing_cyanosafe_door

label ready_to_lift_print:
    scene cyanosafe_closed
    $ cyanosafe_door_open = False
    "How long should we set the cyanosafe for?"
    jump timer

label correct_time:
    hide screen full_inventory
    hide screen toolbox
    hide screen toolboxItemMenu
    hide screen inventory
    hide screen inventoryItemMenu
    window hide
    show timer_10_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_10_left
    show timer_5_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_5_left
    show timer_done:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_done
    show screen full_inventory
    $ ran_cyanosafe = True
    call screen open_door_after_processing

label warn_player_about_lifting_print:
    show screen full_inventory
    call screen warn_player_about_knife
    call screen full_inventory

label ready_to_collect_knife:
    scene cyanosafe_knife_done
    $ cyanosafe_door_open = True
    call screen collect_lifted_knife

label collected_knife:
    scene cyanosafe_open
    python:
        addToInventory(["knife_with_lifted_fingerprint"])
    show screen full_inventory
    call screen successfully_lifted_print_from_knife
    $ at_cyanosafe_machine = False
    $ close_to_cyanosafe = False
    $ knife_in_cyanosafe = False
    $ added_superglue = False
    $ added_water = False
    $ print_lifted_from_knife = True
    jump in_chemistry_lab

label give_stain_hint:
    call screen stain_hint_message
    $ at_cyanosafe_machine = False
    $ knife_in_cyanosafe = False
    $ added_superglue = False
    $ added_water = False
    $ print_lifted_from_knife = True
    jump enter_materials_lab

label already_lifted:
    show screen full_inventory
    call screen already_lifted_print
    call screen full_inventory

# ------------------------------------------------ BEGINNING OF DNA CODE ---------------------------------------------------------------
label selected_water:
    if holding_distilled_water:
        $ holding_distilled_water = False
        $ default_mouse = "default"
    else:
        $ holding_distilled_water = True
        $ default_mouse = "water"
    if currently_using_hemastix:
        show screen use_hemastix
    elif currently_swabbing:
        show screen swabbing
    call screen full_inventory

label using_hemastix:
    $ currently_using_hemastix = True
    show screen full_inventory
    show screen use_hemastix
    call screen full_inventory

label throw_out_hemastix:
    if holding_hemastix:
        hide screen use_hemastix 
        $ currently_using_hemastix = False
        $ default_mouse = "default"
        python:
            current_evidence.wet_hemastix = False
            current_evidence.swabbed_object = False
            current_evidence.display_unused_hemastix = True
            current_evidence.display_negative_result = False
            current_evidence.display_positive_result = False
            current_evidence.display_wet_hemastix = False
    call screen full_inventory

label selected_hemastix:
    hide screen use_hemastix
    if holding_distilled_water:
        $ holding_distilled_water = False
        $ default_mouse = "default"
        python:
            current_evidence.wet_hemastix = True
            current_evidence.display_wet_hemastix = True
            current_evidence.display_unused_hemastix = False
        if not current_evidence.swabbed_object:
            python:
                current_evidence.wet_before_swabbed = True
        show screen full_inventory
        show screen use_hemastix
        call screen added_water_to_hemastix
    else:
        if current_evidence.wet_hemastix and current_evidence.swabbed_object and current_evidence.wet_before_swabbed:
            $ default_mouse = "positive_result"
        else: 
            $ default_mouse = "unused_hemastix"
        $ holding_hemastix = True
    show screen use_hemastix
    call screen full_inventory

label finished_hemastix_test:
    $ holding_hemastix = False
    $ default_mouse = "default"
    show screen full_inventory
    hide screen use_hemastix
    # Go through each piece of evidence that applies
    if current_evidence.name == "dish towel":
        # update the scene to show the hemastix by the piece of evidence
        scene hemastix_by_towel 
        # Update variable
        $ hemastix_next_to_towel = True
        # If player hasn't taken a photo, call camera screen
        if not took_photo_hemastix_with_towel:
            call screen camera_screen
    else:
        scene hemastix_by_knife 
        $ hemastix_next_to_knife = True
        if not took_photo_hemastix_with_knife:
            call screen camera_screen
    call screen full_inventory

label completed_hemastix_test:
    show screen full_inventory
    call screen correct_hemastix_result
    call screen full_inventory

label incorrect_hemastix_test:
    show screen full_inventory
    call screen incorrect_hemastix
    call screen full_inventory

label using_swab:
    $ currently_swabbing = True
    show screen full_inventory
    show screen swabbing
    call screen full_inventory

label collect_swab:
    if holding_swab:
        if not current_evidence.wet_swab_first and current_evidence.swabbed_object_with_swab:
            show screen full_inventory
            call screen incorrect_swab_warning
            call screen full_inventory
        hide screen swabbing
        $ default_mouse = "default"
        show screen full_inventory
        # Go through each piece of evidence that applies
        if current_evidence.name == "dish towel":
            if current_evidence.wet_swab_first and current_evidence.swabbed_object_with_swab:
                # Update the correspinding variable
                $ sample_collected_from_towel = True
                $ currently_swabbing = False
                call screen swab_has_been_collected
                call screen full_inventory
            else:
                call screen incorrect_swab_warning
                show screen swabbing
        elif current_evidence.name == "knife":
            if current_evidence.wet_swab_first and current_evidence.swabbed_object_with_swab:
                $ sample_collected_from_knife = True
                if not print_lifted_from_knife:
                    $ proper_blood_sample_collected = True
                $ currently_swabbing = False
                call screen swab_has_been_collected
                call screen full_inventory
            else:
                call screen incorrect_swab_warning
                show screen swabbing
    else:
        call screen full_inventory

label throw_out_swab:
    if holding_swab:
        hide screen swabbing
        $ currently_swabbing = False
        $ holding_swab = False
        $ default_mouse = "default"
        python:
            current_evidence.wet_swab = False
            current_evidence.wet_swab_first = False
            current_evidence.swabbed_object_with_swab = False
            current_evidence.display_swab = True
            current_evidence.display_wet_swab = False
    call screen full_inventory

label selected_swab:
    if holding_distilled_water:
        $ holding_distilled_water = False
        $ default_mouse = "default"
        python:
            current_evidence.wet_swab = True
            current_evidence.display_wet_swab = True
            current_evidence.display_swab = False 
            if not current_evidence.swabbed_object_with_swab:
                current_evidence.wet_swab_first = True
        show screen full_inventory
        call screen added_water_to_swab
    else:
        $ holding_swab = True
        $ default_mouse = "swab"
    show screen swabbing
    call screen full_inventory

label busy_using_hemastix:
    show screen full_inventory
    show screen use_hemastix
    call screen already_using_hemastix
    show screen use_hemastix
    call screen full_inventory

label busy_swabbing:
    show screen full_inventory
    show screen swabbing
    call screen cannot_use_now
    show screen swabbing
    call screen full_inventory

label use_hemastix_first:
    show screen full_inventory
    call screen no_hemastix_test
    call screen full_inventory

label add_swab_to_inventory:
    # Just need to replace with your evidence. Add the sample from the evidence to your inventory 
    # and then show the screen to collect the piece of evidence from the lab bench
    if current_evidence.name == "dish towel":
        python:
            addToInventory(["sample_from_towel"])

        show screen collect_towel_from_lab_bench
    elif current_evidence.name == "knife":
        python:
            addToInventory(["sample_from_knife"])

        show screen collect_knife_from_lab_bench
    call screen full_inventory

label collect_evidence_from_lab_bench:
    # Go through each piece of evidence that applies to this
    if current_evidence.name == "dish towel":
        # Call screen to display the incubated sample the player just collected
        call screen display_incubated_towel_sample
        python:
            # Add the incubated sample to the player's inventory
            addToInventory(["incubated_sample_from_towel"])
        # Show screen to collect piece of evidence from lab bench
        show screen collect_towel_from_lab_bench
    elif current_evidence.name == "knife":
        call screen display_incubated_knife_sample
        python:
            addToInventory(["incubated_sample_from_knife"])
        show screen collect_knife_from_lab_bench
    call screen full_inventory

label ask_to_send_for_extraction:
    show screen full_inventory
    call screen send_sample_for_extraction
    call screen full_inventory

label sample_sent_for_extraction:
    show screen full_inventory
    # Go through each piece of evidence that applies
    if swab_sample_being_looked_at == "floor":
        python:
            # Remove the item from the player's inventory
            removeInventoryItem(inventory_sprites[inventory_items.index("sample_from_floor")])

        # Display the screen to show the incubated sample the player collected
        call screen display_incubated_floor_sample

        python:
            addToInventory(["incubated_sample_from_blood_pool"])
    elif swab_sample_being_looked_at == "towel":
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("sample_from_towel")])

        call screen display_incubated_towel_sample

        python:
            addToInventory(["incubated_sample_from_towel"])
    elif swab_sample_being_looked_at == "knife":
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("sample_from_knife")])

        call screen display_incubated_knife_sample

        python:
            addToInventory(["incubated_sample_from_knife"])

    call screen full_inventory

label null_button:
    call screen full_inventory

label already_used_hemastix:
    show screen full_inventory
    call screen already_tested_sample
    call screen full_inventory

label already_swabbed:
    show screen full_inventory
    call screen already_collected_swab
    call screen full_inventory

label using_centrifuge:
    hide screen choose_dna_machine
    hide screen centrifuge_info
    hide screen pcr_info
    hide screen thermal_cycler_info
    hide screen plate_centrifuge_info
    hide screen miseq_machine_info
    $ at_centrifuge = True
    scene centrifuge_bg
    # If you do not have any samples with an insufficient concentration of DNA the following if statement should work:
    # if not current_dna_evidence.finished_detection and current_dna_evidence.finished_centrifuge
    if ((current_dna_evidence.name != "towel" and not current_dna_evidence.finished_detection) or (current_dna_evidence.name == "towel" and current_dna_evidence.continuing_with_amplification)) and current_dna_evidence.finished_centrifuge:
        jump dont_need_to_use_machine
    
    show screen back_button
    show screen centrifuge_screen
    python:
        current_dna_evidence.centrifuge_open = False
    call screen full_inventory

label need_to_add_counterweight:
    show screen full_inventory
    call screen add_balance
    call screen full_inventory

label holding_balance_tube:
    $ default_mouse = "dna_tube"
    python:
        current_dna_evidence.holding_tube = True
    show screen centrifuge_screen
    call screen full_inventory

label already_used_machine:
    show screen full_inventory
    call screen already_ran_machine
    call screen full_inventory

label update_centrifuge_image:
    if current_dna_evidence.holding_incubated_sample:
        hide screen back_button # hides back button, can change to your back button screen
        python:
            current_dna_evidence.holding_incubated_sample = False
            # Go through each piece of evidence that applies
            if current_dna_evidence.name == "knife":
                # Remove the corresponding incubated sample from the player's inventory
                removeInventoryItem(inventory_sprites[inventory_items.index("incubated_sample_from_knife")])
            elif current_dna_evidence.name == "towel":
                removeInventoryItem(inventory_sprites[inventory_items.index("incubated_sample_from_towel")])
            elif current_dna_evidence.name == "floor":
                removeInventoryItem(inventory_sprites[inventory_items.index("incubated_sample_from_blood_pool")])
    if not current_dna_evidence.centrifuge_open:
        scene centrifuge_bg
        show screen back_button
        if current_dna_evidence.in_centrifuge and current_dna_evidence.counterweight_in:
            hide screen back_button
            hide screen centrifuge_screen
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxItemMenu
            hide screen inventory
            hide screen inventoryItemMenu
            window hide
            show timer_10_left:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_10_left
            show timer_5_left:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_5_left
            show timer_done:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_done
            python:
                current_dna_evidence.finished_centrifuge = True
    elif current_dna_evidence.centrifuge_open:
        hide screen back_button
        if current_dna_evidence.in_centrifuge and current_dna_evidence.counterweight_in:
            scene centrifuge_filled
        elif current_dna_evidence.in_centrifuge:
            scene centrifuge_only_top_filled
        else:
            $ at_open_centrifuge = True
            scene centrifuge_open

    show screen centrifuge_screen
    call screen full_inventory

label done_with_centrifuge:
    scene centrifuge_only_bottom_filled
    # Go through each piece of evidence that applies
    if current_dna_evidence.name == "knife":
        python:
            # Add the corresponding extracted DNA tube to the player's inventory
            addToInventory(["extracted_dna_from_knife"])
    elif current_dna_evidence.name == "towel":
        python:
            addToInventory(["extracted_dna_from_towel"])
    elif current_dna_evidence.name == "floor":
        python:
            addToInventory(["extracted_dna_from_floor"])
    hide screen centrifuge_screen
    python:
        current_dna_evidence.centrifuge_open = False
    show screen full_inventory
    call screen finished_with_centrifuge
    $ at_centrifuge = False
    scene pcr_plate_bg
    call screen give_pcr_plate_info
    show screen fill_pcr_plate
    $ at_pcr_tray = True
    call screen full_inventory

label busy_with_another_sample:
    show screen full_inventory  
    call screen already_using_centrifuge
    call screen full_inventory 

label update_pcr_plate_scene:
    if current_dna_evidence.negative_solution_in:
        $ default_mouse = "default"
        scene pcr_plate_both_filled
        show screen full_inventory
        call screen fill_rest_with_water
        scene pcr_plate_all_filled
        python:
            current_dna_evidence.holding_pipette = False
            current_dna_evidence.all_pcr_wells_filled = True
    elif current_dna_evidence.dna_sample_in:
        if not current_dna_evidence.holding_pipette:
            $ default_mouse = "default"
        scene pcr_plate_one_filled
        show screen full_inventory
        if not current_dna_evidence.displayed_water_message:
            call screen add_negative_control
            python:
                current_dna_evidence.displayed_water_message = True
    elif current_dna_evidence.viewing_tray:
        scene pcr_plate_close
    call screen full_inventory

label selected_pipette:
    if current_dna_evidence.holding_pipette:
        $ default_mouse = "default"
        python:
            current_dna_evidence.holding_pipette = False
            current_dna_evidence.holding_distilled_water = False
            current_dna_evidence.holding_extracted_dna = False
            current_dna_evidence.holding_sample = False
            current_dna_evidence.holding_positive_control = False
    else:
        if current_dna_evidence.viewing_tray or current_dna_evidence.viewing_amp_plate or current_dna_evidence.viewing_detection_plate:
            $ default_mouse = "pipette"
            python:
                current_dna_evidence.holding_pipette = True
        else:
            show screen full_inventory
            call screen dont_need
    call screen full_inventory

label amount_to_add_for_quantification:
    show screen full_inventory
    menu:

        "What amount of our DNA sample should we pipette?"

        "1µL":
            jump incorrect_amount

        "2µL":
            jump correct_amount

        "5µL":
            jump incorrect_amount

label incorrect_amount:
    show screen full_inventory
    call screen wrong_amount
    jump amount_to_add_for_quantification

label correct_amount:
    show screen full_inventory
    call screen correct_amount
    call screen full_inventory

label add_dna_first:
    show screen full_inventory
    call screen need_to_add_sample_first
    call screen full_inventory

label sample_already_in:
    show screen full_inventory
    call screen dna_already_added
    call screen full_inventory

label moving_to_pcr:
    hide screen fill_pcr_plate
    python:
        addToInventory(["filled_plate"])
    scene empty_lab_bench
    show screen full_inventory
    call screen move_to_pcr
    show screen back_button
    call screen full_inventory

label using_pcr:
    hide screen choose_dna_machine
    hide screen centrifuge_info
    hide screen pcr_info
    hide screen thermal_cycler_info
    hide screen plate_centrifuge_info
    hide screen miseq_machine_info
    $ at_pcr = True
    scene pcr_bg 
    if current_dna_evidence.finished_pcr:
        jump dont_need_to_use_machine
    elif not current_dna_evidence.finished_centrifuge:
        jump dont_need_to_use_machine

    show screen back_button
    show screen pcr_screen
    if current_dna_evidence.tray_in_pcr and current_dna_evidence.pcr_open:
        hide screen back_button
        scene filled_pcr
        python:
            current_dna_evidence.holding_tray = False
            removeInventoryItem(inventory_sprites[inventory_items.index("filled_plate")])
    elif current_dna_evidence.pcr_open and not current_dna_evidence.tray_in_pcr:
        hide screen back_button
        scene empty_pcr
    elif not current_dna_evidence.pcr_open:
        scene pcr_bg 
        if current_dna_evidence.tray_in_pcr:
            hide screen back_button
            hide screen pcr_screen
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxItemMenu
            hide screen inventory
            hide screen inventoryItemMenu
            window hide
            show timer_10_left:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_10_left
            show timer_5_left:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_5_left
            show timer_done:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_done
            python:
                current_dna_evidence.finished_pcr = True
            jump quantification_calculation
    call screen full_inventory

label quantification_calculation:
    # display message saying what the concentration of the DNA sample is and ask if player wants to proceed.
    menu:
        "The PCR has calculated the concentration of the DNA sample to be [current_dna_evidence.concentration_value]ng/µL. The industry standard concentration is 0.067ng/µL. Based on this do you wish to continue the process with this sample? If you select no, you will NOT be able to continue with this sample."

        "Yes":
            # If you do not have a sample with insufficient DNA concentration, this entire if statement block can be deleted
            if current_dna_evidence.name == "towel":
                show screen full_inventory
                call screen cant_continue_with_sample
                $ finished_analyzing_towel_sample = True
                python:
                    current_dna_evidence.continuing_with_amplification = False
                jump back
            python:
                current_dna_evidence.continuing_with_amplification = True

        "No":
            if current_dna_evidence.name != "towel":
                call screen wrong_decision

            python:
                current_dna_evidence.continuing_with_amplification = False
            $ finished_analyzing_towel_sample = True
            jump back
    label calculation:
        python:
            player_calculation = renpy.input("The PCR has calculated the concentration of the sample to be [current_dna_evidence.concentration_value]ng/µL. The standard concentration is 0.067ng/µL and the volume of the microcentrifuge is 15µL. What volume of the DNA sample should be used for amplification?")
        if current_dna_evidence.required_volume == player_calculation:
            python:
                current_dna_evidence.did_correct_calculation = True
            call screen correct_calculation
            jump starting_amplification
        else:
            show screen full_inventory
            call screen wrong_calculation
            jump calculation

            label give_formula:
                call screen provide_formula
                jump calculation

label starting_amplification:
    $ at_pcr = False
    $ at_amplifier_tray = True
    scene amplification_plate_bg
    show screen full_inventory
    call screen give_amplification_plate_info
    show screen fill_amplification_plate
    call screen full_inventory

label update_amp_plate_scene:
    if current_dna_evidence.added_sample_to_amp_plate:
        $ default_mouse = "default"
        scene amplification_plate_three_filled
        show screen full_inventory
        call screen fill_rest_with_water
        scene amplification_plate_all_filled
        python:
            current_dna_evidence.holding_pipette = False
            current_dna_evidence.all_plate_wells_filled = True
    elif current_dna_evidence.added_positive_control and current_dna_evidence.added_negative_control:
        if not current_dna_evidence.holding_pipette:
            $ default_mouse = "default"
        scene amplification_plate_two_filled
        show screen full_inventory
        if not current_dna_evidence.displayed_dna_message:
            call screen add_dna_sample
            python:
                current_dna_evidence.displayed_dna_message = True
    elif not current_dna_evidence.added_positive_control:
        if not current_dna_evidence.holding_pipette:
            $ default_mouse = "default"
        scene amplification_plate_one_filled
    elif not current_dna_evidence.added_negative_control:
        if not current_dna_evidence.holding_pipette:
            $ default_mouse = "default"
        scene amplification_plate_one_filled

    if not current_dna_evidence.added_positive_control and not current_dna_evidence.added_negative_control:
        scene amplification_plate_close
    call screen full_inventory

label moving_to_thermal_cycler:
    hide screen fill_amplification_plate
    hide screen using_plate_centrifuge
    python:
        addToInventory(["filled_plate"])
    scene empty_lab_bench
    show screen full_inventory
    call screen move_to_thermal_cycler
    show screen back_button
    call screen full_inventory

label already_added_negative_control:
    show screen full_inventory
    call screen previously_added_negative_control
    call screen full_inventory

label already_added_positive_control:
    show screen full_inventory
    call screen previously_added_positive_control
    call screen full_inventory

label using_thermal_cycler:
    hide screen choose_dna_machine
    hide screen centrifuge_info
    hide screen pcr_info
    hide screen thermal_cycler_info
    hide screen plate_centrifuge_info
    hide screen miseq_machine_info
    $ at_thermal_cycler = True
    scene thermal_cycler_closed 
    if current_dna_evidence.finished_detection_thermal_cycler and current_dna_evidence.plate_on_ice and not current_dna_evidence.plate_in_thermal_cycler and not current_dna_evidence.thermal_cycler_open:
        jump dont_need_to_use_machine
    elif current_dna_evidence.finished_amplification and not current_dna_evidence.plate_in_thermal_cycler and not current_dna_evidence.thermal_cycler_open and not current_dna_evidence.finished_detection_centrifuge and current_dna_evidence.added_sample_to_det_plate:
        jump dont_need_to_use_machine
    elif not current_dna_evidence.finished_pcr:
        jump dont_need_to_use_machine

    show screen thermal_cycler_screen
    show screen back_button
    if not current_dna_evidence.finished_detection_centrifuge:
        if current_dna_evidence.plate_in_thermal_cycler and current_dna_evidence.thermal_cycler_open:
            hide screen back_button
            scene thermal_cycler_open_full
            if not current_dna_evidence.finished_amplification:
                python:
                    current_dna_evidence.holding_tray = False
                    removeInventoryItem(inventory_sprites[inventory_items.index("filled_plate")])
        elif current_dna_evidence.thermal_cycler_open and not current_dna_evidence.plate_in_thermal_cycler:
            hide screen back_button
            scene thermal_cycler_open
        elif not current_dna_evidence.thermal_cycler_open:
            show screen back_button
            scene thermal_cycler_closed
            if current_dna_evidence.plate_in_thermal_cycler:
                hide screen back_button
                hide screen thermal_cycler_screen
                hide screen full_inventory
                hide screen toolbox
                hide screen toolboxItemMenu
                hide screen inventory
                hide screen inventoryItemMenu
                window hide
                show timer_10_left:
                    xpos 0.45
                    ypos 0.4
                $ renpy.pause(1.0)
                hide timer_10_left
                show timer_5_left:
                    xpos 0.45
                    ypos 0.4
                $ renpy.pause(1.0)
                hide timer_5_left
                show timer_done:
                    xpos 0.45
                    ypos 0.4
                $ renpy.pause(1.0)
                hide timer_done
                python:
                    current_dna_evidence.finished_amplification = True
                show screen full_inventory
                call screen finished_amplification
                show screen thermal_cycler_screen
            elif not current_dna_evidence.plate_in_thermal_cycler and current_dna_evidence.finished_amplification:
                hide screen back_button
                $ at_thermal_cycler = False
                show detection_plate_bg
                $ at_detection_plate = True
                show screen full_inventory
                call screen give_detection_plate_info
                show screen fill_detection_plate
    elif current_dna_evidence.finished_detection_centrifuge:
        if current_dna_evidence.plate_in_thermal_cycler and current_dna_evidence.thermal_cycler_open:
            hide screen back_button
            scene thermal_cycler_open_full
            if not current_dna_evidence.finished_detection_thermal_cycler:
                python:
                    current_dna_evidence.holding_tray = False
                    removeInventoryItem(inventory_sprites[inventory_items.index("filled_plate")])
        elif current_dna_evidence.thermal_cycler_open and not current_dna_evidence.plate_in_thermal_cycler:
            hide screen back_button
            scene thermal_cycler_open
        elif not current_dna_evidence.thermal_cycler_open:
            scene thermal_cycler_closed
            if current_dna_evidence.plate_in_thermal_cycler:
                hide screen back_button
                hide screen thermal_cycler_screen
                hide screen full_inventory
                hide screen toolbox
                hide screen toolboxItemMenu
                hide screen inventory
                hide screen inventoryItemMenu
                window hide
                show timer_10_left:
                    xpos 0.45
                    ypos 0.4
                $ renpy.pause(1.0)
                hide timer_10_left
                show timer_5_left:
                    xpos 0.45
                    ypos 0.4
                $ renpy.pause(1.0)
                hide timer_5_left
                show timer_done:
                    xpos 0.45
                    ypos 0.4
                $ renpy.pause(1.0)
                hide timer_done
                python:
                    current_dna_evidence.finished_detection_thermal_cycler = True
                show screen full_inventory
                call screen put_on_ice
                show screen thermal_cycler_screen
            elif not current_dna_evidence.plate_in_thermal_cycler and current_dna_evidence.finished_detection_thermal_cycler:
                hide screen back_button
                show screen full_inventory
                scene ice_box_bg
                show screen put_plate_on_ice

    call screen full_inventory

label collected_plate_from_thermal_cycler:
    scene thermal_cycler_open
    python:
        addToInventory(["filled_plate"])
    call screen full_inventory

label update_detection_plate_scene:
    scene detection_plate_all_filled
    if current_dna_evidence.added_sample_to_det_plate:
        $ default_mouse = "default"
        hide screen fill_detection_plate
        show screen full_inventory
        call screen finished_detection_plate
        jump back
    call screen full_inventory

label dont_use_this_anymore:
    show screen full_inventory
    call screen dont_use_sample
    call screen full_inventory

label using_plate_centrifuge:
    hide screen choose_dna_machine
    hide screen centrifuge_info
    hide screen pcr_info
    hide screen thermal_cycler_info
    hide screen plate_centrifuge_info
    hide screen miseq_machine_info
    $ at_plate_centrifuge = True
    scene plate_centrifuge_bg
    if current_dna_evidence.finished_detection_centrifuge and not current_dna_evidence.plate_in_centrifuge and not current_dna_evidence.plate_centrifuge_open:
        jump dont_need_to_use_machine
    elif not current_dna_evidence.finished_amplification:
        jump dont_need_to_use_machine
    show screen using_plate_centrifuge
    call screen full_inventory

label update_plate_centrifuge_scene:
    scene plate_centrifuge_bg
    show screen back_button
    if current_dna_evidence.plate_in_centrifuge and current_dna_evidence.plate_centrifuge_open:
        hide screen back_button
        scene plate_centrifuge_open_full
        if not current_dna_evidence.finished_detection_centrifuge:
            python:
                current_dna_evidence.holding_tray = False
                removeInventoryItem(inventory_sprites[inventory_items.index("filled_plate")])
    elif not current_dna_evidence.plate_in_centrifuge and current_dna_evidence.plate_centrifuge_open:
        hide screen back_button
        scene plate_centrifuge_open
    elif not current_dna_evidence.plate_centrifuge_open:
        scene plate_centrifuge_bg
        if current_dna_evidence.plate_in_centrifuge:
            hide screen back_button
            hide screen using_plate_centrifuge
            hide screen thermal_cycler_screen
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxItemMenu
            hide screen inventory
            hide screen inventoryItemMenu
            window hide
            show timer_10_left:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_10_left
            show timer_5_left:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_5_left
            show timer_done:
                xpos 0.45
                ypos 0.4
            $ renpy.pause(1.0)
            hide timer_done
            python:
                current_dna_evidence.finished_detection_centrifuge = True
            call screen finished_with_plate_centrifuge
            show screen using_plate_centrifuge
        elif not current_dna_evidence.plate_in_centrifuge and current_dna_evidence.finished_detection_centrifuge:
            hide screen using_plate_centrifuge
            show screen back_button
    call screen full_inventory

label collected_plate_from_plate_centrifuge:
    scene plate_centrifuge_open
    python:
        addToInventory(["filled_plate"])
    call screen full_inventory

label plate_is_on_ice:
    hide screen put_plate_on_ice
    scene ice_box_with_plate
    show screen full_inventory
    call screen move_to_miseq_machine
    jump back

label using_miseq:
    $ at_miseq = True
    hide screen choose_dna_machine
    hide screen centrifuge_info
    hide screen pcr_info
    hide screen thermal_cycler_info
    hide screen plate_centrifuge_info
    hide screen miseq_machine_info
    scene miseq_bg
    if current_dna_evidence.finished_detection:
        jump dont_need_to_use_machine
    elif not current_dna_evidence.finished_detection_thermal_cycler:
        jump dont_need_to_use_machine
    show screen full_inventory
    call screen miseq_info
    show screen using_miseq
    call screen full_inventory

label update_miseq_scene:
    scene miseq_bg
    show screen back_button
    if current_dna_evidence.plate_in_miseq and current_dna_evidence.miseq_second_open:
        hide screen back_button
        scene plate_in_miseq
        if not current_dna_evidence.finished_detection:
            python:
                current_dna_evidence.holding_tray = False
                removeInventoryItem(inventory_sprites[inventory_items.index("filled_plate")])
    elif not current_dna_evidence.plate_in_miseq and current_dna_evidence.miseq_second_open:
        hide screen back_button
        scene no_plate_miseq
    elif not current_dna_evidence.miseq_second_open and current_dna_evidence.miseq_first_open:
        hide screen back_button
        scene close_miseq
    else:
        scene miseq_bg
        if current_dna_evidence.plate_in_miseq:
            hide screen back_button
            hide screen using_miseq
            show screen full_inventory
            python:
                current_dna_evidence.finished_detection = True
            # Go through each piece of evidence that applies
            if current_dna_evidence.name == "floor":
                # Set the variable to keep track of the completion of analysis to be True
                $ finished_analyzing_floor_sample = True
                python:
                    # Add the electropherogram to the player's inventory
                    addToInventory(["electropherogram_of_floor_sample"])
            elif current_dna_evidence.name == "knife":
                $ finished_analyzing_knife_sample = True
                python:
                    addToInventory(["electropherogram_of_knife_sample"])
            call screen finished_detection
            show screen back_button
    call screen full_inventory

label dont_need_to_use_machine:
    show screen full_inventory
    call screen dont_need_to_use
    jump back

label display_table_of_findings:
    $ viewing_table_of_findings = True
    hide screen choose_icon
    scene empty_table_of_figures
    # Go through each combination of what the table of findings can look like
    if table_of_findings.second_evidence == "knife":
        # If floor profile was first, then knife profile
        scene table_floor_knife
    elif table_of_findings.second_evidence == "floor":
        # If knife profile was first then floor profile
        scene table_knife_floor
    elif table_of_findings.first_evidence == "knife":
        # If there is only a knife profile
        scene table_knife
    elif table_of_findings.first_evidence == "floor":
        # If there is only a floor profile
        scene table_floor
    show screen profiles
    call screen full_inventory

label add_to_table:
    if table_of_findings.first_evidence != None:
        # Go through each possible electropherogram the player could be holding
        if table_of_findings.holding_knife_electropherogram:
            # change the scene for the table fo findings
            scene table_floor_knife
            python:
                # Change value of holding the electropherogram to be False
                table_of_findings.holding_knife_electropherogram = False
                # Update the value of the second piece of evidence added
                table_of_findings.second_evidence = "knife"
                # Remove the electropherogram from the player's inventory
                removeInventoryItem(inventory_sprites[inventory_items.index("electropherogram_of_knife_sample")])
        elif table_of_findings.holding_floor_electropherogram:
            scene table_knife_floor
            python:
                table_of_findings.holding_floor_electropherogram = False
                table_of_findings.second_evidence = "floor"
                removeInventoryItem(inventory_sprites[inventory_items.index("electropherogram_of_floor_sample")])
        $ filled_table_of_findings = True

        show screen full_inventory
        # Explain the results of the table of findings
        # Starting with the victim's profile:
        show highlight_table_column:
            xpos 0.36822917 # Can change according to how big your table of findings is
            ypos 0.03240741
        "This is the genetic profile of the victim Kurt Adams, collected from his toothbrush in his home."
        # Explain the suspect's profile
        show highlight_table_column:
            xpos 0.45416667
            ypos 0.03240741
        "This is the genetic profile of Jenny Adams, the wife of Kurt Adams."
        # Explain the next column in the table
        show highlight_table_column:
            xpos 0.54166667
            ypos 0.03240741
        # Go through every piece of evidence it could be
        if table_of_findings.first_evidence == "floor":
            "This is the genetic profile of the sample collected from the floor."
            "Based on the likelihood ratio, it is 2.25 x 10^20 times more likely that the evidence originated from Kurt Adams, the victim, rather than an unknown individual."
        elif table_of_findings.first_evidence == "knife":
            "This is the genetic profile of the sample collected from the knife."
            "The profile shows that the sample was contaminated. Based on the likelihood ratio, it is 2.46 x 10^20 times more likely that the evidence originated from Kurt Adams, the victim rather than an unknown individual."
            "It is also 2.73 x 10^20 times more likely that the evidence originated from Jenny Adams, Kurt's wife, rather than an unknown individual."
        # Explain the next colum in the table
        show highlight_table_column:
            xpos 0.628125
            ypos 0.03240741
        if table_of_findings.second_evidence == "floor":
            "This is the genetic profile of the sample collected from the floor."
            "Based on the likelihood ratio, it is 2.25 x 10^20 times more likely that the evidence originated from Kurt Adams, the victim, rather than an unknown individual."
        elif table_of_findings.second_evidence == "knife":
            "This is the genetic profile of the sample collected from the knife."
            "The profile shows that the sample was contaminated. Based on the likelihood ratio, it is 2.46 x 10^20 times more likely that the evidence originated from Kurt Adams, the victim rather than an unknown individual."
            "It is also 2.73 x 10^20 times more likely that the evidence originated from Jenny Adams, Kurt's wife rather than an unknown individual."
        hide highlight_table_column

        if processed_stove_fingerprint and processed_knife_fingerprint and filled_table_of_findings and finished_analyzing_towel_sample:
            jump analyzed_all
    else:
        # Go through each possible electropherogram the player could be holding
        if table_of_findings.holding_knife_electropherogram:
            # Change the scene
            scene table_knife
            python:
                # Update the variables for what electropherogram is being held by the player
                table_of_findings.holding_knife_electropherogram = False
                # Update the first piece if evidence that has been added
                table_of_findings.first_evidence = "knife"
                # Remove the elctropherogram from the player's inventory
                removeInventoryItem(inventory_sprites[inventory_items.index("electropherogram_of_knife_sample")])
        elif table_of_findings.holding_floor_electropherogram:
            scene table_floor
            python:
                table_of_findings.holding_floor_electropherogram = False
                table_of_findings.first_evidence = "floor"
                removeInventoryItem(inventory_sprites[inventory_items.index("electropherogram_of_floor_sample")])
    call screen full_inventory

label already_analyzed_sample:
    show screen full_inventory
    call screen already_analyzed
    call screen full_inventory

label dont_need_tool:
    show screen full_inventory
    call screen dont_need
    call screen full_inventory

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

label analyzed_all:
    show screen full_inventory
    call screen analyzed_all_evidence
    $ renpy.quit()
