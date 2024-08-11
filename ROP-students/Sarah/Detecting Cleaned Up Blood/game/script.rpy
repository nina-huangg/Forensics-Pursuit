# Variables
# mouse cursors
define config.mouse_displayable = MouseDisplayable("mouse_cursor", 0, 0).add("inspect", "magnifying_glass_cursor", 0, 0).add("important", "exclamation_point_cursor", 0, 0).add("swab", "swab_cursor", 0, 0).add("pipette", "pipette_cursor", 0, 0).add("spray", "spray_cursor", 0, 0).add("uva", "uva_cursor", 0, 0).add("415nm", "415nm_cursor", 0, 0).add("450nm", "450nm_cursor", 0, 0).add("530nm", "530nm_cursor", 0,0).add("powder", "dusting_powder_cursor", 0, 0).add("bag", "evidence_bag_cursor", 0, 0).add("marker", "evidence_marker_cursor", 0, 0).add("tape", "evident_tape_cursor", 0, 0).add("lifting_tape", "lifting_tape_cursor", 0, 0).add("scalebar", "scalebar_cursor", 0, 0).add("water", "water_cursor", 0, 0).add("lifted_print", "lifted_fingerprint_cursor", 0, 0).add("luminol", "luminol_packet_cursor", 0, 0).add("forensic_tube", "forensic_tube_cursor", 0, 0)

# flash transition
define flash = Fade(.25, 0, .75, color="#fff")

# variable for the photos that can currently be viewed by the player
define taken_photos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# variables for the photos which will be added to list of taken_photos
define num_photos_taken = 0
define took_photo_fingerprint_close = False # variable for fingerprint_close
define took_photo_very_close_fingerprint = False # variable for fingerprint_very_close
define took_photo_marked_floor = False # variable for marked_floor
define took_photo_knife_close = False # variable for knife_close_up
define took_photo_knife_close_marked = False # variable for knife_close_up_marked and knife_close_up_marked_no_fingerprint
define took_photo_luminol_floor = False # variable for luminol_floor_picture
define took_photo_mid_range_stove = False # variable for mid_range_stove
define took_photo_towel_close = False  # variable for towel_very_close and towel_very_close_marked
define took_photo_towel_unmarked = False # variable for dish_towel_unmarked
define took_photo_towel_marked = False # variable for towel_with_marker
define took_photo_unmarked_floor = False # variable for unmarked_floor
define took_photo_untouched_stove = False # variable for untouched_stove
define took_photo_scaled_fingerprint = False # variable for scaled_fingerprint

# variables for viewing evidence
define viewing_evidence = False
define current_page = 1
define total_pages = 13
define viewing_pictures = False

# variables for the toolbox
define toolbox_open = False
define toolbox_show = False

# variables for the flashlights
define selecting_als_flashlights = False
define using_uva = False
define using_415nm = False
define using_450nm = False
define using_530nm = False
default using_uv = False

# variables for the player's current location/scene
define in_kitchen = True
define at_stove = False
define viewing_dish_towel = False
define viewing_floor = False

# variables to keep track of placed evidence markers
define fingerprint_marked = False
define knife_marked = False
define blood_marked = False
define dish_towel_marked = False

# variables to keep track of what evidence has been collected
define collected_knife = False
define collected_dish_towel = False
define collected_fingerprint = False
define collected_swab = False

define put_knife_in_tube = False
define knife_tube_sealed = False
define put_knife_in_bag = False
define put_towel_in_bag = False
define knife_not_ready_to_bag = False
define currently_collecting_knife = False
define currently_collecting_towel = False
define sealed_tube_top = False
define sealed_tube_bottom = False

# variables for blood 
define discovered_blood_pool = False
define currently_in_swabbing_process = False
define currently_swabbing = False
define wet_swab = False
define swabbing_floor = False
define swabbed_floor = False
define ethanol_selected = False
define ethanol_applied = False
define phenolphthalein_selected = False
define phenolphthalein_applied = False
define hydrogen_peroxide_selected = False
define hydrogen_peroxide_applied = False
define correct_kastle_meyer_procedure = False
define bag_selected = False
define properly_swabbed_blood = False
define captured_luminol = False
define holding_swab = False
define selected_water = False
define conducted_kastle_meyer_test = False

define put_swab_in_tube = False
define taped_swab_tube = False
define put_swab_in_bag = False

define display_clean_swab = False
define display_positive_swab = False
define display_swabbing_options = False

define delivered_kastle_meyer_message = False
define delivered_positive_message = False
define warning_swab_message = False

# variables for luminol
default currently_spraying_luminol = False
define spray_bottle_selected = False
define selected_water = False
define only_water = False
define selected_luminol_packet = False
define number_of_sprays = 0
define luminol_ready = False
define added_water_to_bottle = False
define added_packet_to_bottle = False

# variables for collecting the fingerprint
define selecting_powder = False
define black_powder_selected = False
define scalebar_selected = False
define lifting_tape_selected = False
define currently_collecting_fingerprint = False
define picking_up = True
define backing_card_placed = False

define discovered_fingerprint = False
define dusted_fingerprint = False
define scaled_fingerprint = False
define taped_fingerprint = False
define put_print_on_card = False
define put_print_in_bag = False

# variables for forensic tool selection
define marker_selected = False
define tamper_tape_selected = False
define forensic_tube_selected = False

define added_knife_to_evidence = False
define added_towel_to_evidence = False
define added_swab_to_evidence = False
define added_fingerprint_to_evidence = False

# The game starts here.

label start:

    # ----------------------------- CODE FOR INVENTORY -----------------------------

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
    $inventory_item_names = ["415nm Flashlight", "450nm Flashlight", "530nm Flashlight", "Backing Cards", "Black Granular Powder", 
    "Cotton Swab", "Distilled Water", "Ethanol", "Evidence Markers", "Flashlights", "Forensic Tube", "Hydrogen Peroxide", "Lifting Tape", 
    "Luminol Packet", "Phenolphthalein", "Scalebar", "Spray Bottle", "UV Flashlight", "UVA Flashlight", "Camera", "Evidence Bag", "Fingerprint in Bag", 
    "Knife in Bag", "Swab in Bag", "Tamper Tape", "Towel in Bag"] # holds names for inspect pop-up text 
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

    # ----------------------------- END OF CODE FOR INVENTORY ------------------------------

    # ----------------------------- SETUP CODE ------------------------------------

        # sets up environment items for first scene - you may add scenes as necessary
    label setupScene1:

        # --------- ADDING ENVIRONMENT ITEMS ---------
        # $environment_items = ["lid"]

        python:
            # --------- ADDING ITEMS TO INVENTORY ---------
            # change these parameters as necessary
            addToInventory(["evidence_bag", "tamper_tape", "camera"])
            addToToolbox(["evidence_markers", "flashlights", "black_granular_powder", "scalebar", "lifting_tape", 
            "backing_cards", "forensic_tube", "cotton_swab", "distilled_water", "ethanol", "phenolphthalein", 
            "hydrogen_peroxide", "luminol_packet", "spray_bottle"])
            addToToolboxPop(["uv_flashlight", "uva_flashlight", "415nm_flashlight", "450nm_flashlight", "530nm_flashlight"])

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
            
        # scene scene-1-bg at half_size - sets background image
        # call screen scene1
    
    # ------------------------ END OF SETUP CODE ------------------------------------


    # Scene that debriefs the player on the scenario (still temporary)
    hide screen full_inventory
    $ currently_spraying_luminol = False
    scene front

    "You've just arrived at the crime scene. During a welfare check for an individual who is now missing, blood was found on a dish cloth."

    "Your job is to collect the dish cloth and look for additional evidence to solve this disappearance. Enter the house and investigate the scene."

    call screen outside_house
    scene kitchen_idle

    # Code to determine the correct scene that should be displayed
    label select_screen:
        if viewing_floor:
            scene floor_idle
            if put_swab_in_bag:
                show packed_evidence_bag: # Display if the swab is in an evidence bag but has not been taped yet
                    xpos 0.4
                    ypos 0.07
            elif put_swab_in_tube and taped_swab_tube and not put_swab_in_bag:
                show taped_sample:
                    xpos 0.4640625 
                    ypos 0.30833333
            elif put_swab_in_tube and not put_swab_in_bag: # display if swab is in the tube but not in the evidence bag
                show collected_sample:
                    xpos 0.4640625 
                    ypos 0.30833333
            # Determine what camera options need to be available
            if not took_photo_marked_floor and not conducted_kastle_meyer_test:
                show screen camera_screen
            if not currently_swabbing:
                show screen kitchen_floor
        elif viewing_dish_towel:
            jump select_dish_towel_view
        elif at_stove:
            jump select_stove_view
        elif in_kitchen:
            if collected_knife and collected_dish_towel:
                jump select_kitchen_view_all_collected
            elif collected_knife:
                jump select_kitchen_view_knife_collected
            elif collected_dish_towel:
                jump select_kitchen_view_dish_towel_collected
            else:
                jump select_kitchen_view_nothing_collected

            show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        
        call screen full_inventory

    # Code to select the correct kitchen scene when both the towel and knife have been collected
    label select_kitchen_view_all_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene all_all
                elif knife_marked:
                    scene all_blood_towel_knife
                elif collected_fingerprint:
                    scene all_blood_towel_fingerprint
                else:
                    scene all_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene all_blood_fingerprint_knife
                elif knife_marked:
                    scene all_blood_knife
                elif collected_fingerprint:
                    scene all_blood_fingerprint
                else:
                    scene all_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene all_towel_fingerprint_knife
                elif knife_marked:
                    scene all_towel_knife
                elif collected_fingerprint:
                    scene all_towel_fingerprint
                else:
                    scene all_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene all_fingerprint_knife
                elif knife_marked:
                    scene all_knife
                elif collected_fingerprint:
                    scene all_fingerprint
                else:
                    scene all_none
            
        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)

        # Determine if blood spot can be photographed
        if not took_photo_unmarked_floor and blood_marked and not collected_swab and not conducted_kastle_meyer_test:
            show screen blood_spot_camera
        
        call screen full_inventory

    # Code to select the correct screen for the kitchen when only the knife has been collected
    label select_kitchen_view_knife_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene knife_all
                elif knife_marked:
                    scene knife_blood_towel_knife
                elif fingerprint_marked:
                    scene knife_blood_towel_fingerprint
                else:
                    scene knife_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene knife_blood_fingerprint_knife
                elif knife_marked:
                    scene knife_blood_knife
                elif fingerprint_marked:
                    scene knife_blood_fingerprint
                else:
                    scene knife_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene knife_towel_fingerprint_knife
                elif knife_marked:
                    scene knife_towel_knife
                elif fingerprint_marked:
                    scene knife_towel_fingerprint
                else:
                    scene knife_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene knife_fingerprint_knife
                elif knife_marked:
                    scene knife_knife
                elif fingerprint_marked:
                    scene knife_fingerprint
                else:
                    scene knife_none

        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)

        # Determine if blood pool can be photographed
        if not took_photo_unmarked_floor and blood_marked and not collected_swab and not conducted_kastle_meyer_test:
            show screen blood_spot_camera
        
        call screen full_inventory

    # Code to select the correct kitchen scene when only the dish towel has been collected
    label select_kitchen_view_dish_towel_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene towel_all
                elif knife_marked:
                    scene towel_blood_towel_knife
                elif fingerprint_marked:
                    scene towel_blood_towel_fingerprint
                else:
                    scene towel_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene towel_blood_fingerprint_knife
                elif knife_marked:
                    scene towel_blood_knife
                elif fingerprint_marked:
                    scene towel_blood_fingerprint
                else:
                    scene towel_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene towel_towel_fingerprint_knife
                elif knife_marked:
                    scene towel_towel_knife
                elif fingerprint_marked:
                    scene towel_towel_fingerprint
                else:
                    scene towel_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene towel_fingerprint_knife
                elif knife_marked:
                    scene towel_knife
                elif fingerprint_marked:
                    scene towel_fingerprint
                else:
                    scene towel_none

        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)

        # Determine of the blood pool can be photographed
        if not took_photo_unmarked_floor and blood_marked and not collected_swab and not conducted_kastle_meyer_test:
            show screen blood_spot_camera

        call screen full_inventory

    # Code to determine the correct kitchen scene when niether the knife nor dish towel has been collected
    label select_kitchen_view_nothing_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene none_all
                elif knife_marked:
                    scene none_blood_towel_knife
                elif fingerprint_marked:
                    scene none_blood_towel_fingerprint
                else:
                    scene none_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene none_blood_fingerprint_knife
                elif knife_marked:
                    scene none_blood_knife
                elif fingerprint_marked:
                    scene none_blood_fingerprint
                else:
                    scene none_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene none_towel_fingerprint_knife
                elif knife_marked:
                    scene none_towel_knife
                elif fingerprint_marked:
                    scene none_towel_fingerprint
                else:
                    scene none_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene none_fingerprint_knife
                elif knife_marked:
                    scene none_knife
                elif fingerprint_marked:
                    scene none_fingerprint
                else:
                    scene none_none

        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        # Determine if the scene needs to photographed (only can if the player hasn't collected nor marked anything yet)
        if not took_photo_mid_range_stove and not fingerprint_marked and not knife_marked and not blood_marked and not dish_towel_marked and not collected_knife and not collected_dish_towel:
            show screen camera_screen
        # Determine if the blood pool can be photographed
        if not took_photo_unmarked_floor and blood_marked and not collected_swab and not conducted_kastle_meyer_test:
            show screen blood_spot_camera
        
        call screen full_inventory

    # Code to determine the correct scene for the stove
    label select_stove_view:
        if collected_fingerprint:
            if currently_collecting_knife or collected_knife:
                hide screen knife_screen
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker_knife_dusty
                elif fingerprint_marked:
                    scene stove_fingerprint_knife_dusty
                elif knife_marked:
                    scene stove_marker_knife_dusty
                else:
                    scene stove_knife_dusty
            else:
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker_dusty
                elif fingerprint_marked:
                    scene stove_fingerprint_dusty
                elif knife_marked:
                    scene stove_marker_dusty
                else:
                    scene stove_none_dusty
        else:
            if currently_collecting_knife or collected_knife:
                hide screen knife_screen
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker_knife
                elif fingerprint_marked:
                    scene stove_fingerprint_knife
                elif knife_marked:
                    scene stove_marker_knife
                else:
                    scene stove_knife
            else:
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker
                elif fingerprint_marked:
                    scene stove_fingerprint
                elif knife_marked:
                    scene stove_marker
                else:
                    scene stove_none
        if put_knife_in_bag: # Display if the knife is in the evidence bag but not sealed with tamper tape
            show packed_evidence_bag:
                xpos 0.4
                ypos 0.07
        elif sealed_tube_top and not knife_tube_sealed and not collected_knife:
            show tube_top_taped:
                xpos 0.42
                ypos 0.1
        elif sealed_tube_bottom and not knife_tube_sealed and not collected_knife:
            show tube_bottom_taped:
                xpos 0.42
                ypos 0.1
        elif knife_tube_sealed and not put_knife_in_bag: # Display if knife is in the taped tube but not yet in the evidence bag
            show taped_tube_idle:
                xpos 0.42
                ypos 0.1
        elif put_knife_in_tube and not put_knife_in_bag: # Display if knife is in tube but not sealed with tamper tape
            show filled_tube:
                xpos 0.42
                ypos 0.1

        # Determine if the stove can be photographed in its current state
        if not took_photo_untouched_stove and not knife_marked and not fingerprint_marked and not collected_fingerprint and not collected_knife and not put_knife_in_tube and not put_knife_in_bag:
            show screen camera_screen

        # Determine if the knife can be photographed
        if not collected_knife and not put_knife_in_tube and not put_knife_in_bag and not knife_marked and not took_photo_knife_close:
            show screen knife_unmarked_camera
        elif knife_marked and not collected_knife and not put_knife_in_tube and not put_knife_in_bag and not took_photo_knife_close_marked:
            show screen knife_marked_camera
        
        # Determine if the fingerprint can be photographed
        if not took_photo_fingerprint_close and collected_fingerprint and not put_knife_in_tube and not put_knife_in_bag:
            show screen fingerprint_camera
        
        show screen stove_buttons
        call screen full_inventory

    # Code to select the correct scene when viewing the dish towel close up
    label select_dish_towel_view:
        if dish_towel_marked and (collected_dish_towel or currently_collecting_towel):
            scene dish_towel_marker
        elif dish_towel_marked:
            scene dish_towel_all
        elif collected_dish_towel or currently_collecting_towel:
            scene dish_towel_none
        else:
            scene dish_towel_towel
        if put_towel_in_bag: # Display if the dish towel is in an evidence bag but not sealed with tape
            show packed_evidence_bag:
                xpos 0.4
                ypos 0.07
        
        # Determine if the towel and area can be photographed
        if (not took_photo_towel_unmarked or not took_photo_towel_marked) and not collected_dish_towel and not put_towel_in_bag:
            show screen camera_screen
        
        # Determine if the towel can be photographed up close
        if not took_photo_towel_close and not collected_dish_towel and not put_towel_in_bag:
            show screen dish_towel_camera
        
        show screen dish_towel
        call screen full_inventory

    # Code to determine what photo was taken, and add it to the list of photos taken
    label took_photo:
        hide screen camera_screen
        $ num_photos_taken = num_photos_taken + 1
        # Code for the flash effect
        show screen full_inventory
        show transparent with flash
        hide transparent

        # Iterate through the list of taken photos, find the first empty spot and fill it with the photo taken
        $ i = 0
        while i < 12:
            if taken_photos[i] == 0:
                if not took_photo_very_close_fingerprint and currently_collecting_fingerprint and dusted_fingerprint and not scaled_fingerprint:
                    $ taken_photos[i] = "fingerprint_very_close.jpg"
                    $ took_photo_very_close_fingerprint = True
                elif not took_photo_scaled_fingerprint and currently_collecting_fingerprint and scaled_fingerprint and not taped_fingerprint:
                    $ taken_photos[i] = "scaled_fingerprint.jpg"
                    $ took_photo_scaled_fingerprint = True
                elif not took_photo_marked_floor and viewing_floor and not conducted_kastle_meyer_test:
                    $ taken_photos[i] = "marked_floor.jpg"
                    $ took_photo_marked_floor = True
                elif not took_photo_luminol_floor and viewing_floor and number_of_sprays == 3:
                    $ taken_photos[i] = "luminol_floor_picture.jpg"
                    $ took_photo_luminol_floor = True
                    $ captured_luminol = True
                    $ number_of_sprays = 0
                    $ only_water = False
                    $ luminol_ready = False
                    $ spray_bottle_selected = False
                    $ currently_spraying_luminol = False
                    scene floor_idle
                    show screen kitchen_floor

                    if collected_knife and collected_dish_towel and collected_swab and collected_fingerprint and captured_luminol:
                        jump finished_collecting
                elif not took_photo_mid_range_stove and not blood_marked and not fingerprint_marked and not knife_marked and not dish_towel_marked and not collected_knife and not collected_dish_towel and not at_stove and not viewing_dish_towel and not viewing_floor:
                    $ taken_photos[i] = "mid_range_stove.jpg"
                    $ took_photo_mid_range_stove = True
                elif not took_photo_towel_unmarked and not dish_towel_marked and not collected_dish_towel and not put_towel_in_bag and viewing_dish_towel:
                    $ taken_photos[i] = "dish_towel_unmarked.jpg"
                    $ took_photo_towel_unmarked = True
                elif not took_photo_towel_marked and dish_towel_marked and not collected_dish_towel and not put_towel_in_bag and viewing_dish_towel:
                    $ taken_photos[i] = "towel_with_marker.jpg"
                    $ took_photo_towel_marked = True
                elif not took_photo_untouched_stove and not knife_marked and not fingerprint_marked and not collected_fingerprint and not collected_knife and not put_knife_in_tube and not put_knife_in_bag and at_stove:
                    $ taken_photos[i] = "untouched_stove.jpg"
                    $ took_photo_untouched_stove = True
                $ i = 20
            else:
                $ i = i + 1
        call screen full_inventory

    # If a photo has been taken of the unmarked blood spot
    label took_photo_unmarked_bloodspot:
        hide screen blood_spot_camera
        $ took_photo_unmarked_floor = True
        $ num_photos_taken = num_photos_taken + 1
        # Code for the flash effect
        show screen full_inventory
        show transparent with flash
        hide transparent

        # Iterate through the list of taken photos, find the first empty spot and fill it with the photo taken
        $ i = 0
        while i < 12:
            if taken_photos[i] == 0:
                $ taken_photos[i] = "unmarked_floor.jpg"
                $ i = 20
            else:
                $ i = i +  1
        call screen full_inventory

    label took_photo_dish_towel:
        hide screen dish_towel_camera
        $ took_photo_towel_close = True
        $ num_photos_taken = num_photos_taken + 1
        # Code for camera flash effect
        show screen full_inventory
        show transparent with flash
        hide transparent

        # Iterate through the list of taken photos, find the first empty spot and fill it with the photo taken
        $ i = 0
        while i < 12:
            if taken_photos[i] == 0:
                if dish_towel_marked:
                    $ taken_photos[i] = "towel_very_close_marked.jpg"
                else:
                    $ taken_photos[i] = "towel_very_close.jpg"
                $ i = 20
            else:
                $ i = i +  1
        call screen full_inventory

    label took_photo_knife_unmarked:
        hide screen knife_unmarked_camera
        $ took_photo_knife_close = True
        $ num_photos_taken = num_photos_taken + 1
        # Code for camera flash effect
        show screen full_inventory
        show transparent with flash
        hide transparent

        # Iterate through the list of taken photos, find the first empty spot and fill it with the photo taken
        $ i = 0
        while i < 12:
            if taken_photos[i] == 0:
                $ taken_photos[i] = "knife_close_up.jpg"
                $ i = 20
            else:
                $ i = i +  1
        call screen full_inventory

    label took_photo_knife_marked:
        hide screen knife_marked_camera
        $ took_photo_knife_close_marked = True
        $ num_photos_taken = num_photos_taken + 1
        # Code for camera flash effect
        show screen full_inventory
        show transparent with flash
        hide transparent

        # Iterate through the list of taken photos, find the first empty spot and fill it with the photo taken
        $ i = 0
        while i < 12:
            if taken_photos[i] == 0:
                if fingerprint_marked:
                    $ taken_photos[i] = "knife_close_up_marked.jpg"
                else:
                    $ taken_photos[i] = "knife_close_up_marked_no_fingerprint.jpg"
                $ i = 20
            else:
                $ i = i +  1
        call screen full_inventory

    label took_photo_fingerprint:
        hide screen fingerprint_camera
        $ took_photo_fingerprint_close = True
        $ num_photos_taken = num_photos_taken + 1
        # Code for camera flash effect
        show screen full_inventory
        show transparent with flash
        hide transparent

        # Iterate through the list of taken photos, find the first empty spot and fill it with the photo taken
        $ i = 0
        while i < 12:
            if taken_photos[i] == 0:
                $ taken_photos[i] = "fingerprint_close.jpg"
                $ i = 20
            else:
                $ i = i + 1
        call screen full_inventory

    label hide_images:
        $ current_page = 1
        hide casefile_inventory
        hide fingerprint_close
        hide fingerprint_very_close
        hide marked_floor
        hide knife_close_up
        hide knife_close_up_marked
        hide knife_close_up_marked_no_fingerprint
        hide luminol_floor_picture
        hide mid_range_stove
        hide towel_very_close
        hide towel_very_close_marked
        hide towel_with_marker
        hide unmarked_floor
        hide untouched_stove
        hide dish_towel_unmarked
        hide scaled_fingerprint
        hide screen present_evidence
        if not currently_collecting_fingerprint:
            jump select_screen
        else:
            call screen full_inventory


    # If the player clicks on the camera to view the taken pictures
    label display_images:
        if viewing_pictures: # if currently viewing pictures, hide them
            $ viewing_pictures = False
            $ current_page = 1
            hide casefile_inventory
            hide fingerprint_close
            hide fingerprint_very_close
            hide marked_floor
            hide knife_close_up
            hide knife_close_up_marked
            hide knife_close_up_marked_no_fingerprint
            hide luminol_floor_picture
            hide mid_range_stove
            hide towel_very_close
            hide towel_very_close_marked
            hide towel_with_marker
            hide unmarked_floor
            hide untouched_stove
            hide dish_towel_unmarked
            hide scaled_fingerprint
            hide screen present_evidence
            if not currently_collecting_fingerprint:
                jump select_screen
            else:
                call screen full_inventory
        else: # If not currently viewing pictures, display the menu to view them
            hide screen kitchen_screen
            hide screen show_evidence_bags
            hide screen camera_screen
            hide screen blood_spot_camera
            hide screen dish_towel_camera
            hide screen knife_unmarked_camera
            hide screen knife_marked_camera
            hide screen fingerprint_camera
            $ viewing_evidence = False
            $ viewing_pictures = True
            show casefile_inventory:
                ypos 0.05
            jump show_image

    # Code to display the appropriate image based on the current page the player is viewing in the menu
    label show_image:
        # Hide all images
        hide fingerprint_close
        hide fingerprint_very_close
        hide marked_floor
        hide knife_close_up
        hide knife_close_up_marked
        hide knife_close_up_marked_no_fingerprint
        hide luminol_floor_picture
        hide mid_range_stove
        hide towel_very_close
        hide towel_very_close_marked
        hide towel_with_marker
        hide unmarked_floor
        hide untouched_stove
        hide dish_towel_unmarked
        hide scaled_fingerprint
        # Go through each image, if taken_photos[current_page - 1] is that image, show it
        if taken_photos[current_page - 1] == "fingerprint_close.jpg":
            show fingerprint_close:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "fingerprint_very_close.jpg":
            show fingerprint_very_close:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "marked_floor.jpg":
            show marked_floor:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "knife_close_up.jpg":
            show knife_close_up:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "knife_close_up_marked.jpg":
            show knife_close_up_marked:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "knife_close_up_marked_no_fingerprint.jpg":
            show knife_close_up_marked_no_fingerprint:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "luminol_floor_picture.jpg":
            show luminol_floor_picture:
                xpos 0.22
                ypos 0.17
                zoom 0.55
        elif taken_photos[current_page - 1] == "mid_range_stove.jpg":
            show mid_range_stove:
                xpos 0.235
                ypos 0.15
                zoom 0.25
        elif taken_photos[current_page - 1] == "towel_very_close.jpg":
            show towel_very_close:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "towel_very_close_marked.jpg":
            show towel_very_close_marked:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "towel_with_marker.jpg":
            show towel_with_marker:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "unmarked_floor.jpg":
            show unmarked_floor:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "untouched_stove.jpg":
            show untouched_stove:
                xpos 0.228
                ypos 0.16
                zoom 0.21
        elif taken_photos[current_page - 1] == "dish_towel_unmarked.jpg":
            show dish_towel_unmarked:
                xpos 0.228
                ypos 0.2
                zoom 0.5
        elif taken_photos[current_page - 1] == "scaled_fingerprint.jpg":
            show scaled_fingerprint:
                xpos 0.228
                ypos 0.2
                zoom 0.5
        # Show other necessary screens
        show screen present_evidence(current_page, num_photos_taken)
        call screen full_inventory

    # Code to update variables and show the next image
    label next_page:
        $ current_page = current_page + 1
        jump show_image

    # Code to update variables and show the previous image
    label back_page:
        $ current_page = current_page - 1
        jump show_image

    # Code for if the player picked the 530nm flashlight (the player won't be able to see the blood pool)
    label selected_530nm:
        if using_530nm:
            $ using_530nm = False
            $ default_mouse = "default"
            hide filter_530nm
            hide screen kitchen_530nm
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_530nm = True
            $ default_mouse = "530nm"
            hide screen kitchen_screen
            hide screen camera_screen
            hide screen blood_spot_camera
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxpop
            hide screen toolboxItemMenu
            hide screen toolboxPopItemMenu
            show filter_530nm
            show screen dark_overlay_with_mouse
            call screen kitchen_530nm

    # Code for if the player selects the 450nm flashight (the player won't be able to see the blood pool)
    label selected_450nm:
        if using_450nm:
            $ using_450nm = False
            $ default_mouse = "default"
            hide filter_450nm
            hide screen kitchen_450nm
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_450nm = True
            $ default_mouse = "450nm"
            hide screen kitchen_screen
            hide screen camera_screen
            hide screen blood_spot_camera
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxpop
            hide screen toolboxItemMenu
            hide screen toolboxPopItemMenu
            show filter_450nm
            show screen dark_overlay_with_mouse
            call screen kitchen_450nm

    # Code for if the player selects the 415nm flashlight (the player will be able to see the blood pool)
    label selected_415nm:
        if using_415nm:
            $ using_415nm = False
            $ default_mouse = "default"
            hide blood_spot
            hide filter_415nm
            hide screen kitchen_415nm
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_415nm = True
            $ default_mouse = "415nm"
            hide screen kitchen_screen
            hide screen camera_screen
            hide screen blood_spot_camera
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxpop
            hide screen toolboxItemMenu
            hide screen toolboxPopItemMenu
            show blood_spot
            show filter_415nm
            show screen dark_overlay_with_mouse
            call screen kitchen_415nm


    # Code for if the player selected the UVA flashlight (the player will be able to see the blood spot)
    label selected_uva:
        if using_uva:
            $ using_uva = False
            $ default_mouse = "default"
            hide blood_spot
            hide uva_filter
            hide screen uva_kitchen
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_uva = True
            $ default_mouse = "uva"
            hide screen kitchen_screen
            hide screen camera_screen
            hide screen blood_spot_camera
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxpop
            hide screen toolboxItemMenu
            hide screen toolboxPopItemMenu
            show blood_spot
            show uva_filter
            show screen dark_overlay_with_mouse
            call screen uva_kitchen

    label dont_need:
        show screen full_inventory
        call screen dont_need_light
        call screen full_inventory

    # Code for when the player discovers the pool of blood with either the UVA or 415nm flashlights
    label discovered_floor_blood:
        $ discovered_blood_pool = True
        $ blood_marked = True
        show screen full_inventory
        call screen discovered_blood_with_flashlight # inform the player they discovered potential blood
        if using_uva:
            call screen uva_kitchen
        elif using_415nm:
            call screen kitchen_415nm

        hide screen dark_overlay_with_mouse
        hide screen uva_kitchen
        hide screen kitchen_415nm
        jump select_screen

    # Code for moving from the kitchen to the stove
    label stove:
        hide screen kitchen_screen
        hide screen camera_screen
        $ at_stove = True

        jump select_screen

    # Code for moving from the kitchen to a close up of the dish towel
    label dish_towel:
        hide screen kitchen_screen
        hide screen camera_screen
        $ viewing_dish_towel = True
        jump select_dish_towel_view

    # Code for whenever the back button is pressed
    label back:
        # If the player is in the middle of collecting evidence, inform them that they need to finish collecting it first before they can leave
        if currently_collecting_fingerprint or currently_collecting_knife or currently_spraying_luminol or currently_in_swabbing_process or currently_collecting_towel:
            show screen full_inventory
            call screen finish_collecting
            call screen full_inventory
        hide screen dish_towel_camera
        hide screen knife_unmarked_camera
        hide screen knife_marked_camera
        hide screen fingerprint_camera
        hide screen camera_screen
        hide casefile_inventory
        hide fingerprint_close
        hide fingerprint_very_close
        hide marked_floor
        hide knife_close_up
        hide knife_close_up_marked
        hide knife_close_up_marked_no_fingerprint
        hide luminol_floor_picture
        hide mid_range_stove
        hide towel_very_close
        hide towel_very_close_marked
        hide towel_with_marker
        hide unmarked_floor
        hide untouched_stove
        hide dish_towel_unmarked
        hide scaled_fingerprint
        hide screen present_evidence
        $ viewing_pictures = False
        if viewing_floor: # if currently viewing floor, move back to viewing kitchen
            $ viewing_floor = False
            hide screen kitchen_floor
        elif viewing_dish_towel: # If viewing dish towel, move back to kitchen
            $ viewing_dish_towel = False
            hide screen dish_towel
        elif at_stove: # If at stove, move back to kitchen
            $ at_stove = False
            hide screen kitchen_stove
            hide screen stove_buttons
            hide screen collected_knife
            hide screen place_marker_stove
        
        jump select_screen

    # Code for if the player places an evidence marker for the dish towel
    label placed_marker_dish_towel:
        hide screen place_marker_dish_towel
        hide screen place_marker_kitchen
        hide screen camera_screen
        $ default_mouse = "default"
        $ marker_selected = False
        $ dish_towel_marked = True
        jump select_screen

    # Code for if the player places an evidence marker for the knife
    label placed_knife:
        hide screen place_marker_stove
        hide screen camera_screen
        $ default_mouse = "default"
        $ marker_selected = False
        $ knife_marked = True
        jump select_screen

    label no_fingerprint:
        show screen full_inventory
        call screen no_fingerprints_here
        jump select_screen

    label taking_fingerprint:
        show screen full_inventory
        call screen in_fingerprinting_procedure
        call screen full_inventory

    label collecting_knife_on_stove:
        show screen full_inventory
        call screen already_collecting_knife
        jump select_screen

    label no_fingerprints:
        show screen full_inventory
        call screen no_fingerprints_here
        call screen full_inventory

    # If the player selects the UV flashlight button
    label uv_light:
        if using_uv: # If player is currently using the flashlight, put it away
            $ using_uv = False
            $ default_mouse = "default"
            hide screen dark_stove
            hide screen dark_overlay_with_mouse
            hide uv_fingerprint
            hide uv_fingerprint_collected

            # Determine what photos the player can take
            if not collected_knife and not put_knife_in_tube and not put_knife_in_bag and not knife_marked and not took_photo_knife_close:
                show screen knife_unmarked_camera
            elif knife_marked and not collected_knife and not put_knife_in_tube and not put_knife_in_bag and not took_photo_knife_close_marked:
                show screen knife_marked_camera

            if not took_photo_untouched_stove and not knife_marked and not fingerprint_marked and not collected_fingerprint and not collected_knife and not put_knife_in_tube and not put_knife_in_bag:
                show screen camera_screen
            
            show screen stove_buttons
            call screen full_inventory
        else: # If the player is not using the flashlight, turn it on
            $ using_uv = True
            $ default_mouse = "uva"
            hide screen full_inventory
            hide screen toolbox
            hide screen toolboxpop
            hide screen toolboxItemMenu
            hide screen toolboxPopItemMenu
            hide screen stove_buttons
            hide screen camera_screen
            hide screen knife_unmarked_camera
            hide screen knife_marked_camera
            if collected_fingerprint:
                show uv_fingerprint_collected
            else:
                show uv_fingerprint
            show screen dark_overlay_with_mouse
            if not collected_fingerprint:
                show screen dark_stove # screen to find/highlight the fingerprint

            call screen uv_back_button

    # Code for when the player finds the fingerprint on the stove
    label found_fingerprint:
        $ default_mouse = "default"
        show screen full_inventory
        call screen discovered_fingerprint_message
        hide screen dark_stove
        hide screen dark_overlay_with_mouse
        hide uv_fingerprint
        $ discovered_fingerprint = True
        $ using_uv = False
        $ fingerprint_marked = True
        jump select_screen

    label has_been_dusted:
        show screen full_inventory
        call screen already_dusted
        call screen full_inventory

    label find_fingerprint_first:
        show screen full_inventory
        call screen discover_fingerprint_first
        call screen full_inventory

    # Code for after player has dusted the fingerprint
    label dusted_fingerprint:
        $ default_mouse = "default"
        $ black_powder_selected = False
        $ dusted_fingerprint = True
        hide screen stove_buttons
        $ currently_collecting_fingerprint = True
        hide screen knife_unmarked_camera
        hide screen knife_marked_camera
        scene dusted_fingerprint
        hide screen dust_fingerprint
        show screen camera_screen # Allow player to take a picture of the dusted print
        call screen full_inventory

    label has_been_scaled:
        show screen full_inventory
        call screen already_scaled
        call screen full_inventory

    # Code for when the player places the scalebar
    label placed_scalebar:
        $ default_mouse = "default"
        $ scaled_fingerprint = True
        scene dusted_fingerprint_scaled
        $ scalebar_selected = False
        hide screen scalebar_screen
        hide screen camera_screen
        show screen camera_screen # Allow player to take a picture of the scaled fingerprint
        call screen full_inventory

    label has_been_taped:
        show screen full_inventory
        call screen already_taped
        call screen full_inventory
    
    # Code for when the player places the tape on the fingerprint
    label placed_tape:
        $ default_mouse = "default"
        $ lifitng_tape_selected = False
        $ picking_up = False
        $ taped_fingerprint = True
        hide screen taping_screen
        hide screen camera_screen # Hide the camera screen since the player is no longer able to take a photo of the scene
        scene dusted_fingerprint_scaled_taped
        
        call screen full_inventory

    # Code for when the player has lifted the fingerprint
    label lifted_tape:
        $ default_mouse = "lifted_print"
        hide screen picking_up_tape
        if backing_card_placed: # If a backing card has been placed, allow player to place fingerprint on backing card
            scene fingerprint_removed_backing_card
            show screen placed_fingerprint
        else: # if backing card has not been placed, show the stovetop without the fingerprint
            scene fingerprint_removed
            $ picking_up = True
        call screen full_inventory

    label has_been_put_on_card:
        show screen full_inventory
        call screen already_put_on_card
        call screen full_inventory

    label placed_backing_card:
        scene empty_backing_card
        hide screen placing_backing_card
        $ backing_card_placed = True
        show screen picking_up_tape
        call screen full_inventory

    # Code for the finished backing card
    label finished_placing_fingerprint:
        $ default_mouse = "default"
        $ backing_card_placed = True
        hide screen placed_fingerprint
        scene filled_backing_card
        $ put_print_on_card = True
        call screen full_inventory

    label busy_swabbing:
        show screen full_inventory
        call screen swabbing_in_progress
        call screen full_inventory

    label busy_luminol:
        show screen full_inventory
        call screen in_luminol_process
        call screen full_inventory

    label busy_holding_swab:
        show screen full_inventory
        call screen currently_holding_swab
        call screen full_invetory

    # Code for when the player puts the knife in the forensic tube
    label knife_put_in_tube:
        $ currently_collecting_knife = True
        # Show correct scene
        if knife_marked and fingerprint_marked:
            scene stove_fingerprint_marker_knife
        elif knife_marked:
            scene stove_marker_knife
        elif fingerprint_marked:
            scene stove_fingerprint_knife
        else:
            scene stove_knife
        $ forensic_tube_selected = False
        $ default_mouse = "default"
        hide screen collected_knife
        $ knife_not_ready_to_bag = True
        $ put_knife_in_tube = True
        show filled_tube: # Display the forensic tube with the knife 
            xpos 0.42
            ypos 0.1
        call screen full_inventory

    label sealed_top:
        hide filled_tube
        hide screen tube_with_knife
        $ sealed_tube_top = True
        if sealed_tube_top and sealed_tube_bottom:
            jump sealed_knife_tube
        else:
            show tube_top_taped:
                xpos 0.42
                ypos 0.1
            show screen tube_with_knife(sealed_tube_top, sealed_tube_bottom)
            call screen full_inventory
    
    label sealed_bottom:
        hide filled_tube
        hide screen tube_with_knife
        $ sealed_tube_bottom = True
        if sealed_tube_top and sealed_tube_bottom:
            jump sealed_knife_tube
        else:
            show tube_bottom_taped:
                xpos 0.42
                ypos 0.1
            show screen tube_with_knife(sealed_tube_top, sealed_tube_bottom)
            call screen full_inventory

    # Code for when the player seals the forensic tube with the tamper tape
    label sealed_knife_tube:
        hide tube_top_taped
        hide tube_bottom_taped
        hide screen tube_with_knife
        $ tamper_tape_selected = False
        $ default_mouse = "default"
        $ knife_not_ready_to_bag = False
        $ knife_tube_sealed = True
        show taped_tube_idle: # Display the forensic tube with the knife, sealed with tamper tape
            xpos 0.42
            ypos 0.1
        call screen full_inventory

    # Code for when the player seals an evidence bag with tamper tape
    label seal_evidence_bag:
        $ default_mouse = "default"
        hide screen collected_evidence
        #if tamper_tape_selected: # if tamper tape if being used, seal evidence bag
        hide packed_evidence_bag
        $ tamper_tape_selected = False
        hide screen collected_evidence
        show screen full_inventory
        show sealed_evidence_bag: # Display sealed evidence bag
            xpos 0.4
            ypos 0.07
        if currently_collecting_fingerprint: # if fingerprint has just been collected, display appropriate message
            $ collected_fingerprint = True
            show screen full_inventory
            call screen fingerprint_has_been_collected
            $ added_fingerprint_to_evidence = True

            if collected_knife and collected_dish_towel and collected_swab and collected_fingerprint and captured_luminol:
                jump finished_collecting

            python:
                addToInventory(["fingerprint_in_bag"])
            
        if put_towel_in_bag: # If towel has just been collected, display appropriate message
            $ put_towel_in_bag = False
            $ collected_dish_towel = True
            show screen full_inventory
            call screen dish_towel_has_been_collected
            $ added_towel_to_evidence = True

            if collected_knife and collected_dish_towel and collected_swab and collected_fingerprint and captured_luminol:
                jump finished_collecting

            python:
                addToInventory(["towel_in_bag"])
            
        if put_knife_in_bag: # If knife has just been collected, display appropriate message
            $ put_knife_in_bag = False
            $ collected_knife = True
            $ knife_tube_sealed = False
            $ put_knife_in_tube = False
            show screen full_inventory
            call screen knife_has_been_collected
            $ added_knife_to_evidence = True

            if collected_knife and collected_dish_towel and collected_swab and collected_fingerprint and captured_luminol:
                jump finished_collecting

            python:
                addToInventory(["knife_in_bag"])

        if put_swab_in_bag: # If swab has just been collected, display appropriate message
            $ put_swab_in_bag = False
            $ put_swab_in_tube = False
            $ taped_swab_tube = False
            $ collected_swab = True
            $ currently_swabbing = False
            show screen full_inventory
            call screen swab_has_been_collected
            $ added_swab_to_evidence = True
            python:
                addToInventory(["swab_in_bag"])
        jump select_screen
        call screen full_inventory

    # Code for when player has put the dish towel in an evidence bag
    label collect_towel:
        hide screen camera_screen
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen stove_buttons
        hide screen collecting_dish_towel
        $ put_towel_in_bag = True
        $ currently_collecting_towel = True
        if dish_towel_marked: # Dteermine correct scene to display
            scene dish_towel_marker
        else:
            scene dish_towel_none
        show packed_evidence_bag: # Display a packed but not sealed evidence bag
            xpos 0.4
            ypos 0.07
        call screen full_inventory

    # Code for when the player places the forensic tube with the knife in an evidence bag
    label collect_knife:
        hide taped_tube_idle
        hide filled_tube
        hide screen camera_screen
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen collect_knife_tube
        $ put_knife_in_bag = True
        show packed_evidence_bag: # Display a packed but not sealed evidence bag
            xpos 0.4
            ypos 0.07
        call screen full_inventory

    label taped_sample_tube:
        hide screen taping_swab
        $ taped_swab_tube = True
        show taped_sample:
            xpos 0.4640625 
            ypos 0.30833333
        call screen full_inventory

    # Code for when the player puts the swab in the evidence bag 
    label packaged_swab:
        hide screen camera_screen
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen packing_swab
        $ put_swab_in_bag = True
        show packed_evidence_bag: # Display a packed, but not sealed evidence bag
            xpos 0.4
            ypos 0.07
        call screen full_inventory

    # Code foe when the player puts the fingerprint backing card in an evidence bag
    label pack_fingerprint:
        hide screen camera_screen
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen packed_fingerprint
        $ put_print_in_bag = True
        scene fingerprint_removed
        show packed_evidence_bag: # Display a packed but not sealed evidence bag
            xpos 0.4
            ypos 0.07
        call screen full_inventory

    label put_away_tamper_tape:
        hide screen tube_with_knife
        if viewing_floor and currently_in_swabbing_process and collected_swab:
            $ currently_in_swabbing_process = False
            hide screen collected_evidence
            if not added_swab_to_evidence:
                python:
                    addToInventory(["swab_in_bag"])
        elif at_stove and currently_collecting_fingerprint and collected_fingerprint:
            $ currently_collecting_fingerprint = False
            hide screen collected_evidence
            if not added_fingerprint_to_evidence:
                python:
                    addToInventory(["fingerprint_in_bag"])
        elif at_stove and currently_collecting_knife and collected_knife:
            $ currently_collecting_knife = False
            hide screen collected_evidence
            if not added_knife_to_evidence:
                python:
                    addToInventory(["knife_in_bag"])
        elif viewing_dish_towel and currently_collecting_towel and collected_dish_towel:
            $ currently_collecting_towel = False
            hide screen collected_evidence
            if not added_towel_to_evidence:
                python:
                    addToInventory(["towel_in_bag"])

        if viewing_floor and not taped_swab_tube:
            hide screen taping_swab
            show collected_sample:
                xpos 0.4640625 
                ypos 0.30833333

        if not knife_not_ready_to_bag or not at_stove or currently_collecting_fingerprint:
            show packed_evidence_bag:
                xpos 0.4
                ypos 0.07
        if not currently_collecting_fingerprint:
            jump select_screen
        else:
            call screen full_inventory

    # Code for moving from kitchen to floor
    label floor:
        hide screen kitchen_screen
        hide screen blood_spot_camera
        hide screen camera_screen
        scene floor_idle
        $ viewing_floor = True
        jump select_screen

    label already_collecting_sample:
        show screen full_inventory
        call screen finish_collecting
        call screen full_inventory

    label already_collected_sample:
        show screen full_inventory
        call screen already_collected_swab
        call screen full_inventory

    label already_swabbing:
        show screen full_inventory
        call screen cannot_use_now
        call screen full_inventory

    label start_swabbing:
        hide screen camera_screen
        $ currently_swabbing = True
        $ display_clean_swab = True
        $ currently_in_swabbing_process = True
        hide screen kitchen_floor
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for when the player selects the distilled water
    label wet:
        if selected_water: # If using water, put away
            $ selected_water = False
            $ default_mouse = "default"
            hide screen swabbing
        else: # If not using water, put in player's hand
            $ selected_water = True
            $ default_mouse = "water"
            if currently_swabbing:
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            
        if currently_swabbing: # DIsplay swabbing screen if the player is in the swabbing process
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for when the swab tube is selected
    label collect_swab:
        if holding_swab: # If holding the swab, the player collects the swab
            # Check if the blood pool has been properly swabbed/collected
            if not ethanol_applied and not phenolphthalein_applied and not hydrogen_peroxide_applied and properly_swabbed_blood:
                $ properly_swabbed_blood = True
            else:
                $ properly_swabbed_blood = False

            if not properly_swabbed_blood: # If sample has not been collected properly, tell player to retry
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                show screen full_inventory
                call screen incorrect_swab_warning
                $ warning_swab_message = True
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                call screen full_inventory
            if not conducted_kastle_meyer_test: # If player has collected a sample without conducting a kastle-meyer test, ask if they are sure this is blood
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                show screen full_inventory
                call screen no_kastle_meyer_test
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                call screen full_inventory
            # If the sample has been properly collected
            $ default_mouse = "default"
            $ display_clean_swab = False
            $ display_positive_swab = False
            $ display_swabing_options = False
            $ put_swab_in_tube = True
            $ holding_swab = False
            $ warning_swab_message = False
            hide screen swabbing
            $ bag_selected = False
            $ delivered_kastle_meyer_message = False
            $ currently_swabbing = False
            show collected_sample: # Display the tube with the swab
                    xpos 0.4640625 
                    ypos 0.30833333
        call screen full_inventory

    # Code to display guidance for conducting a kastle-meyer test
    label more_guidance:
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen full_inventory
        call screen explain_more
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for when the player selects the biohazard bin 
    label throw_out_swab:
        if holding_swab: # If holding swab, the player throws out the swab
            $ default_mouse = "default"
            $ currently_swabbing = False
            $ wet_swab = False
            $ ethanol_selected = False
            $ ethanol_applied = False
            $ phenolphthalein_selected = False
            $ phenolphthalein_applied = False
            $ hydrogen_peroxide_selected = False
            $ hydrogen_peroxide_applied = False
            $ correct_kastle_meyer_procedure = False
            $ display_clean_swab = False
            $ display_posiitve_swab = False
            $ display_swabbing_options = False
            $ swabbed_floor = False
            $ holding_swab = False
            $ delivered_kastle_meyer_message = False
            $ warning_swab_message = False
            $ currently_in_swabbing_process = False
            hide screen swabbing
            jump select_screen
        else: # If not holding a swab, nothing happens
            call screen full_inventory

    # Code for when the player swabs the floor with a swab
    label swabbed_floor:
        $ default_mouse = "default"
        $ swabbing_floor = False
        $ swabbed_floor = True
        $ display_clean_swab = True
        $ display_swabbing_options = True
        $ holding_swab = False
        if wet_swab:
            $ properly_swabbed_blood = True
        show screen full_inventory
        call screen swabbed_floor_message # Tell the player that they swabbed the floor
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for placing the swab back in its position in the swabing procedure screen
    label place_swab:
        $ default_mouse = "default"
        $ holding_swab = False
        # Determine if the positive result of the kastle-meyer test needs to be displayed
        if correct_kastle_meyer_procedure and ethanol_applied and phenolphthalein_applied and hydrogen_peroxide_applied and wet_swab:
            $ display_positive_swab = True 
        else:
            $ display_clean_swab = True
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for when the player clicks on the swab
    label pick_up_swab:
        if selected_water: # If the player is holding water, water is added on the swab
            $ wet_swab = True
            $ default_mouse = "default"
            $ selected_water = False
        elif ethanol_selected: # If the player is holding ethanol, ethanol is added on the swab
            $ ethanol_applied = True
            # Determine if the procedure so far has been correct
            if phenolphthalein_applied or hydrogen_peroxide_applied or not wet_swab or not swabbed_floor:
                $ correct_kastle_meyer_procedure = False
            else:
                $ correct_kastle_meyer_procedure = True
            $ ethanol_selected = False
            $ default_mouse = "default"
        elif phenolphthalein_selected: # If the player is holding phenolphthalein, phenolphthalein is added on the swab
            $ phenolphthalein_applied = True
            # Determine if the procedure so far has been correct
            if not ethanol_applied or hydrogen_peroxide_applied:
                $ correct_kastle_meyer_procedure = False
            $ phenolphthalein_selected = False
            $ default_mouse = "default"
        elif hydrogen_peroxide_selected: # If player is holding hydrogen peroxide, hydrogen peroxide is added on the swab
            $ hydrogen_peroxide_applied = True
            # Determine if the procedure so far is correct
            if ethanol_applied and phenolphthalein_applied and correct_kastle_meyer_procedure:
                $ hydrogen_peroxide_selected = False
                $ default_mouse = "default"
                $ display_positive_swab = True
                $ conducted_kastle_meyer_test = True
            $ hydrogen_peroxide_selected = False
            $ default_mouse = "default"
        else : # If the player is picks up the swab
            if not swabbed_floor:
                $ swabbing_floor = True
            else:
                $ swabbing_floor = False

            $ display_clean_swab = False
            $ display_positive_swab = False
            $ default_mouse = "swab"
            $ holding_swab = True
        
        # Determine if the kastle-meyer procedure has been done correctly or not and display the sppropriate message
        if ethanol_applied and phenolphthalein_applied and hydrogen_peroxide_applied and not correct_kastle_meyer_procedure and not delivered_kastle_meyer_message:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            show screen full_inventory
            $ delivered_kastle_meyer_message = True
            $ conducted_kastle_meyer_test = True
            call screen incorrect_kastle_meyer_procedure
        elif ethanol_applied and phenolphthalein_applied and hydrogen_peroxide_applied and correct_kastle_meyer_procedure and not delivered_positive_message:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            show screen full_inventory
            $ delivered_positive_message = True
            call screen correct_kastle_meyer_procedure

        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code to provide further direction for retrying the kastle-meyer procedure
    label not_sure:
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen full_inventory
        call screen give_direction
        call screen full_inventory

    # Code for if player selects the ethanol
    label ethanol:
        if ethanol_selected: # If ethanol is being used, put away
            $ default_mouse = "default"
            $ ethanol_selected = False
        else: # If ethanol is not being used, put in player's hand
            $ default_mouse = "pipette"
            $ ethanol_selected = True

        # Display swabbing screen if needed
        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for when the player selects the phenolphthalein
    label phenolphthalein:
        if phenolphthalein_selected: # if using phenolphthalein, put away
            $ default_mouse = "default"
            $ phenolphthalein_selected = False
        else: # If not using phenolphthalein, put in player's hand
            $ default_mouse = "pipette"
            $ phenolphthalein_selected = True

        # Display swabbing screen if needed
        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    # Code for when the player selects the hydrogen peroxide
    label hydrogen_peroxide:
        if hydrogen_peroxide_selected: # If using hydrogen peroxide, put away
            $ default_mouse = "default"
            $ hydrogen_peroxide_selected = False
        else: # If not using hydrogen peroxide, put in player's hand
            $ default_mouse = "pipette"
            $ hydrogen_peroxide_selected = True

        # Display swabbing screen if needed
        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        call screen full_inventory

    label get_sample:
        show screen full_inventory
        call screen collect_swab_first
        call screen full_inventory

    label start_luminol_process:
        $ spray_bottle_selected = True
        $ currently_spraying_luminol = True
        show screen luminol(only_water, luminol_ready)
        call screen full_inventory

    # Code for when the player selects the luminol packet
    label luminol_packet:
        if selected_luminol_packet: # If packet is being used, put away
            $ selected_luminol_packet = False
            $ default_mouse = "default"
        else: # If packet is not being used, put in player's hand
            $ selected_luminol_packet = True
            $ default_mouse = "luminol"
        
        call screen full_inventory

    label cannot_use_here:
        show screen full_inventory
        call screen cant_use_here
        call screen full_inventory

    # Code for when the player clicks on the spray bottle
    label selected_bottle:
        if selected_water: # If player is holding water, water is added to the spray bottle
            $ selected_water = False
            $ default_mouse = "default"
            $ only_water = True
            $ added_water_to_bottle = True
            if added_water_to_bottle and added_packet_to_bottle:
                $ luminol_ready = True
            show screen luminol(only_water, luminol_ready)
        elif selected_luminol_packet: # If player is holding the luminol packet, the luminol tablet is added to the spray bottle
            $ default_mouse = "default"
            $ only_water = False
            $ added_packet_to_bottle = True
            $ selected_luminol_packet = False
            if added_water_to_bottle and added_packet_to_bottle:
                $ luminol_ready = True
            show screen luminol(only_water, luminol_ready)
        elif luminol_ready: # If the luminol is ready to be sprayed and the player is not holding anything, the player hods the bottle and can spray the luminol
            hide screen luminol
            $ default_mouse = "spray"
            scene dark_floor
            show screen spraying_luminol
        
        call screen full_inventory

    # Code for when the player is spraying the luminol
    label spray_luminol:
        $ number_of_sprays = number_of_sprays + 1

        if number_of_sprays == 3: # If the player has sprayed enough luminol
            $ default_mouse = "default"
            hide screen spraying_luminol
            hide screen kitchen_floor
            scene luminol_floor
            show screen full_inventory
            call screen camera_screen
        else: 
            scene dark_floor
            show screen spraying_luminol
            call screen full_inventory

label finished_collecting:
    show screen full_inventory
    call screen finished_collecting_evidence
    $ renpy.quit()

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5