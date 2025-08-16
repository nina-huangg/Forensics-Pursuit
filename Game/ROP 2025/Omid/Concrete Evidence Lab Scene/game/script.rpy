default current_cursor = ''
default show_case_files = False
default show_toolbox = False

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]

### PCR machine variables
default pcr_step = 0  # Current step in PCR process
default pcr_state = "empty"  # empty or filled
default pcr_mistakes = []  # Track mistakes made during process
default pcr_error = ""  # Error message for incorrect answers

### DNA analysis variables
default current_dna_evidence = None
default dna_comparison_result = ""
default dna_samples_added = False

### DNA sample tracking system (replaces inventory)
default dna_samples_available = []  # Available DNA samples after PCR
default dna_samples_status = {}     # Track status of each sample (available, identified, discarded)

### FARO analysis variables
default faro_scenes_analyzed = {"scene1": False, "scene2": False, "scene3": False}

### Completion tracking variables
default male_dna_identified = False
default female_dna_identified = False
default mixed_dna_discarded = False

### FARO scene completion tracking
default scene1_analyzed = False
default scene2_analyzed = False
default scene3_analyzed = False

### Web tracking variables
default username = ""  # Set this when user logs in
default session_start_time = 0
default dna_comparison_results = []  # Track all comparison results
default api_server_url = "http://localhost:3000" 
default api_endpoint = "/api/submit-progress"

init python:
    import time
    import json
    
    def check_analysis_completion():
        """Check if all required analysis tasks are complete using custom tracking"""
        all_scenes_analyzed = scene1_analyzed and scene2_analyzed and scene3_analyzed
        all_dna_identified = male_dna_identified and female_dna_identified and mixed_dna_discarded
        return all_scenes_analyzed and all_dna_identified
    
    def get_current_session_time():
        """Calculate time spent in current session"""
        if session_start_time > 0:
            return time.time() - session_start_time
        return 0

    
    def send_progress_data(username):
        """Send progress data as POST request to server"""
        progress_data = {
            "username": username,
            "pcr_completed": dna_samples_added,
            "dna_matches_found": len([r for r in dna_comparison_results if "MATCH" in r]),
            "mistakes_made": len(pcr_mistakes),
            "time_spent": get_current_session_time(),
            "timestamp": time.time()
        }
        
        try:
            # Build full API URL
            full_api_url = api_server_url + api_endpoint
            
            print(f"Sending progress data for user: {username}")
            print(f"API URL: {full_api_url}")
            print(f"Data: {progress_data}")
            
            result = renpy.fetch(full_api_url, json=progress_data, result="json")
            
            if result:
                print(f"Progress data sent successfully: {result}")
            else:
                print("Progress data sent, but no response received")
                
        except Exception as e:
            print(f"Error sending progress data: {e}")
            print("Progress data (error fallback):", progress_data)

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def add_mistake(mistake_text):
        global pcr_mistakes
        if mistake_text not in pcr_mistakes:
            pcr_mistakes.append(mistake_text)
    
    def add_dna_samples():
        """Add DNA samples to custom tracking system after successful PCR"""
        global dna_samples_added, dna_samples_available, dna_samples_status
        if not dna_samples_added:
            # Initialize DNA samples in custom tracking system
            dna_samples_available = [
                {"id": "dna_sample_1", "name": "DNA Sample 1", "type": "male_dna_profile"},
                {"id": "dna_sample_2", "name": "DNA Sample 2", "type": "female_dna_profile"}, 
                {"id": "dna_sample_3", "name": "DNA Sample 3", "type": "mixed_dna_profile"}
            ]
            
            # Initialize status tracking
            dna_samples_status = {
                "dna_sample_1": "available",
                "dna_sample_2": "available", 
                "dna_sample_3": "available"
            }
            
            dna_samples_added = True
            
            # Send progress data when PCR is completed
            if username:
                send_progress_data(username)
    
    def compare_dna_profiles(evidence_id, warrant_type):
        """Compare DNA evidence with warrant samples using custom tracking"""
        global dna_comparison_result, dna_comparison_results, male_dna_identified, female_dna_identified
        global dna_samples_status
        
        # Get the sample type from our tracking system
        sample_type = None
        for sample in dna_samples_available:
            if sample["id"] == evidence_id:
                sample_type = sample["type"]
                break
        
        if sample_type == "male_dna_profile" and warrant_type == "male":
            dna_comparison_result = "INCLUSION: Evidence is consistent with male suspect warrant sample."
            male_dna_identified = True
            dna_samples_status[evidence_id] = "identified_male"
        elif sample_type == "female_dna_profile" and warrant_type == "female":
            dna_comparison_result = "INCLUSION: Evidence is consistent with female suspect warrant sample."
            female_dna_identified = True
            dna_samples_status[evidence_id] = "identified_female"
        elif sample_type == "mixed_dna_profile":
            dna_comparison_result = "INCONCLUSIVE: Profile does not raise conclusive results."
        else:
            dna_comparison_result = "NO MATCH: Evidence does not match selected warrant sample."
        
        # Track the result for progress monitoring
        dna_comparison_results.append(dna_comparison_result)
        if check_analysis_completion():
            renpy.jump('analysis_complete')
        
        # Send progress data after each comparison (if username is set)
        if username:
            send_progress_data(username)
    
    def discard_mixed_sample(evidence_id):
        """Remove mixed sample from custom tracking system"""
        global dna_comparison_result, mixed_dna_discarded, dna_samples_status
        
        # Get the sample type from our tracking system
        sample_type = None
        for sample in dna_samples_available:
            if sample["id"] == evidence_id:
                sample_type = sample["type"]
                break
        
        if sample_type == "mixed_dna_profile":
            dna_comparison_result = "Mixed sample excluded from analysis."
            mixed_dna_discarded = True
            dna_samples_status[evidence_id] = "discarded"

        if check_analysis_completion():
            renpy.jump('analysis_complete')
    
    def set_dna_evidence_from_cursor():
        """Legacy function - no longer needed with custom DNA selection"""
        pass
        
    
    def get_dna_display_name(sample_id):
        """Get display name for DNA evidence using custom tracking"""
        if not dna_samples_available:
            return "No samples available"
        
        # Find the sample by ID
        for sample in dna_samples_available:
            if sample["id"] == sample_id:
                status = dna_samples_status.get(sample_id, "available")
                
                if status == "identified_male":
                    return "Male Suspect DNA (Identified)"
                elif status == "identified_female":
                    return "Female Suspect DNA (Identified)"
                elif status == "discarded":
                    return "Discarded Sample"
                else:
                    return sample["name"]
        
        return "Unknown Sample"
    
    def get_dna_sample_type(sample_id):
        """Get the DNA sample type for analysis"""
        for sample in dna_samples_available:
            if sample["id"] == sample_id:
                return sample["type"]
        return None
    
    class DNAEvidence:
        def __init__(self, name, display_name):
            self.name = name
            self.display_name = display_name
    
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
    scene entering_lab_screen
    with Dissolve(1.5)
    
    # Initialize session tracking
    python:
        
        # Set session start time for progress tracking
        session_start_time = time.time()
        
        # Try to get username from URL parameters if running in web
        try:
            import renpy.web
            if renpy.web.is_web:
                # Get username from URL params or prompt user
                js_code = """
                const urlParams = new URLSearchParams(window.location.search);
                const user = urlParams.get('username') || 'anonymous_' + Date.now();
                user;
                """
                username = renpy.web.eval_js(js_code) or "anonymous_user"
            else:
                username = "desktop_user"  # Default for desktop testing
        except ImportError:
            username = "desktop_user"
        
        print(f"Session started for user: {username}")

    ########## INVENTORY CODE ###################################################

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
    $inventory_item_names = ["Evidence bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag", "Pvs kit"] # holds names for inspect pop-up text 
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

    # show screen full_inventory onlayer over_screens 
    ################################################################################

    

# sets up environment items for first scene - you may add scenes as necessary
label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    #$environment_items = ["lid"]

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        # addToInventory(["screwdriver", "laptop_fingerprint"])
        # addToToolbox(["camera", "water", "superglue", "lifting_tape"])
        #addToToolboxPop(["tip"])

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
            # if item == "lid":
            #     environment_sprites[-1].width = 300 / 2
            #     environment_sprites[-1].height = 231 / 2
            #     environment_sprites[-1].x = 1000
            #     environment_sprites[-1].y = 500
        
    # scene scene-1-bg at half_size - sets background image
    show screen scene1

transform half_size:
    zoom 0.5


label lab_hallway_intro:
    #show screen case_files_screen onlayer over_screens 
    #show screen toolbox_button_screen onlayer over_screens     
    scene lab_hallway_idle
    "Welcome to the lab!"
    "Thanks to an increase in budget, you've been assigned a lab assistant to help you with your investigations."
    "They will mainly assist you with the Materials Lab. Let's get started!"

label hallway:
    hide screen inventory
    call screen lab_hallway_screen

label data_analysis_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen data_analysis_lab_screen

label afis:
    call screen afis_screen

label dna_analysis:
    call screen dna_analysis_screen

label faro_analysis:
    call screen faro_analysis_screen

label materials_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label fumehood:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen fumehood_screen

label analytical_instruments:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

label pcr_machine:
    show screen back_button_screen('analytical_instruments') onlayer over_screens
    call screen pcr_machine_screen

label analysis_complete:
    call screen analysis_complete_screen
    
return
