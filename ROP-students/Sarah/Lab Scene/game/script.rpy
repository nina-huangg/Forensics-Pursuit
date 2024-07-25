# Variable for mouse
define config.mouse_displayable = MouseDisplayable("mouse_cursor", 0, 0).add("inspect", "magnifying_glass_cursor", 0, 0).add("knife", "knife_cursor", 0, 0).add("swab", "swab_cursor", 0, 0).add("water", "water_cursor", 0, 0).add("unused_hemastix", "unused_hemastix_cursor", 0, 0).add("negative_result", "negative_result_cursor", 0, 0).add("positive_result", "positive_result_cursor", 0, 0)

# Variables to keep track of where the player is
define in_hallway = True
define in_materials_lab = False
define in_data_analysis_lab = False
define at_cyanosafe_machine = False
define at_fumehood = False
define at_lab_bench = False

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

# Variables for dish towel
define determined_blood_on_towel = False
define sample_collected_from_towel = False
define sent_towel_sample_to_be_extracted = False

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
            self.display_negative_result = False
            self.display_positive_result = False

            # Variables to keep track of swabbing variables
            self.wet_swab = False
            self.wet_swab_first = False
            self.swabbed_object_with_swab = False
            self.display_swab = True

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

    # Set current_evidence to keep trackof which evidence is currently active
    current_evidence = dish_towel

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
    "Photo Of Hemastix Next To Towel", "Photo Of Hemastix Next To Knife", "Sample From Floor", "Sample From Towel", "Sample From Knife"] # holds names for inspect pop-up text 
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
        addToInventory(["knife", "dish_towel", "sample_from_floor"])
        addToToolbox(["als_flashlights", "distilled_water", "superglue", "basic_yellow", "cotton_swab", "hemastix", "scalebar"])
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
        jump enter_materials_lab
    elif at_fumehood:
        $ at_fumehood = False
        jump enter_materials_lab
    elif at_cyanosafe_machine:
        $ at_cyanosafe_machine = False
        jump enter_materials_lab
    elif at_lab_bench:
        $ at_lab_bench = False
        jump enter_materials_lab
    elif in_materials_lab:
        show screen full_inventory
        $ in_materials_lab = False
        hide screen back_button
        jump in_lab_hallway

label took_photo:
    hide screen camera_screen
    if holding_450nm_flashlight and photographing_knife:
        if inspecting_fingerprint:
            $ took_photo_fingerprint_scaled_als = True
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
    call screen dont_need_light
    call screen full_inventory

label enter_data_analysis_lab:


label enter_materials_lab:
    $ in_hallway = False
    $ in_materials_lab = True
    scene materials_lab_dim
    show screen full_inventory
    show screen back_button
    call screen choose_machine

label lab_bench:
    scene empty_lab_bench
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
    call screen back_button

label cyanosafe_machine:
    $ at_cyanosafe_machine = True

    if cyanosafe_door_open:
        scene cyanosafe_far_open
        call screen inspect_cyanosafe
    else:
        scene cyanosafe_far_closed
        call screen open_cyanosafe_door

label open_cyanosafe:
    hide screen open_cyanosafe_door
    $ cyanosafe_door_open = True
    scene cyanosafe_far_open
    call screen inspect_cyanosafe

label go_closer_to_cyanosafe:
    $ close_to_cyanosafe = True
    if knife_in_cyanosafe:
        scene cyanosafe_knife
    else:
        scene cyanosafe_open

    if holding_knife:
        call screen place_knife_in_cyanosafe
    elif holding_superglue:
        call screen add_superglue_to_cyanosafe
    elif holding_distilled_water:
        call screen add_water_to_cyanosafe
    else:
        call screen full_inventory

label added_item_to_cyanosafe:
    hide screen place_knife_in_cyanosafe
    hide screen add_superglue_to_cyanosafe
    hide screen add_water_to_cyanosafe
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
    jump ask_player_how_long

label ask_player_how_long:
    menu:
        "How long should we set the cyanosafe for?"

        "1 minute":
            jump incorrect_time

        "5 minutes":
            jump incorrect_time

        "10 minutes":
            jump correct_time

        "15 minutes":
            jump incorrect_time

label incorrect_time:
    call screen incorrect_time_message
    jump ask_player_how_long

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
    call screen open_door_after_processing

label warn_player_about_lifting_print:
    show screen full_inventory
    call screen warn_player_about_knife
    $ warned_player_about_fingerprint_before_swabbing = True
    call screen full_inventory

label ready_to_collect_knife:
    scene cyanosafe_knife_done
    $ cyanosafe_door_open = True
    call screen collect_lifted_knife

label collected_knife:
    scene cyanosafe_open
    python:
        addToInventory(["knife_with_lifted_fingerprint"])
    call screen successfully_lifted_print_from_knife
    $ at_cyanosafe_machine = False
    $ knife_in_cyanosafe = False
    $ added_superglue = False
    $ added_water = False
    $ print_lifted_from_knife = True
    jump enter_materials_lab

label give_stain_hint:
    call screen stain_hint_message
    $ at_cyanosafe_machine = False
    $ knife_in_cyanosafe = False
    $ added_superglue = False
    $ added_water = False
    $ print_lifted_from_knife = True
    jump enter_materials_lab

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
    call screen full_inventory

label selected_hemastix:
    hide screen use_hemastix
    if holding_distilled_water:
        $ holding_distilled_water = False
        $ default_mouse = "default"
        python:
            current_evidence.wet_hemastix = True
        if not current_evidence.swabbed_object:
            python:
                current_evidence.wet_before_swabbed = True
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
    if current_evidence.name == "dish towel":
        scene hemastix_by_towel 
        $ hemastix_next_to_towel = True
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
        if current_evidence.name == "dish towel":
            if current_evidence.wet_swab_first and current_evidence.swabbed_object_with_swab:
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
    call screen full_inventory

label selected_swab:
    if holding_distilled_water:
        $ holding_distilled_water = False
        $ default_mouse = "default"
        python:
            current_evidence.wet_swab = True 
            if not current_evidence.swabbed_object_with_swab:
                current_evidence.wet_swab_first = True
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
    if current_evidence.name == "dish towel":
        show screen collect_towel_from_lab_bench
    elif current_evidence.name == "knife":
        show screen collect_knife_from_lab_bench
    call screen full_inventory

label ask_to_send_for_extraction:
    show screen full_inventory
    call screen send_sample_for_extraction
    call screen full_inventory

label sample_sent_for_extraction:
    show screen full_inventory
    if swab_sample_being_looked_at == "floor":
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("sample_from_floor")])
    elif swab_sample_being_looked_at == "towel":
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("sample_from_towel")])
    elif swab_sample_being_looked_at == "knfie":
        python:
            removeInventoryItem(inventory_sprites[inventory_items.index("sample_from_knife")])

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

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5
