# Needed global variables and default values
default show_evidence = False
default show_toolbox = False

default evidence_complete_process = {'gun_blue': False, 'ninhydrin': False, 'bullet_AFIS': False, 'cheque_AFIS': False, 'deskfoot_AFIS': False}

default current_cursor = ''
default current_process = ''
default process_fumehood = False
default process_afis = False

default show_physical = False
default show_digital = False

default inventory_item_names = ["Gun Blue", "Water", "Bottle", "Ninhydrin", "Bag", "Tape", "Physical Evidence", "Digital Evidence"] # holds names for inspect pop-up text 
default tools = {'gun_blue': False, 'water': False, 'bottle': False, 'ninhydrin': False, 'bag': False, 'tape': False}

# entries on afis when search
default afis_search = []
default afis_search_coordinates = {'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}
default importing = False

# transition for photo taking flash (0 in/out so middle screen don't last long)
define flash = Fade(.25, 0, 0, color="#fff")

default curr_timer = ''

init python:
    style.choice_frame.background = "#ffffff"

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def set_tool(tool):
        global tools
        if tool == '':
            set_cursor('')
            for t in tools:
                if t!= tool:
                    tools[t] = False
        elif tools[tool]:
            set_cursor('')
            tools[tool] = False
        else:
            set_cursor(tool)
            tools[tool] = True
            for t in tools:
                if t!= tool:
                    tools[t] = False
    
    def set_state_to_processed(process):
        global evidence_complete_process
        evidence_complete_process[process] = True

    def add_afis(evidence):
        afis_search.append(evidence)
        evidence.afis_processed = True
    
    class Evidence:
        def __init__(self, name, afis_details, afis_processed):
            self.name = name
            self.afis_details = afis_details
            self.afis_processed = False
    
    # declare each piece of evidence
    no_evidence = Evidence(name = '', afis_details = {}, afis_processed = False)

    bullet = Evidence(name = 'bullet',
                        afis_details = {
                            'image': 'bullet_fingerprint',
                            'xpos': 0.18, 'ypos': 0.3,
                            'score': '0',
                            'compare': 'None'},
                        afis_processed = False)
    cheque = Evidence(name = 'cheque',
                        afis_details = {
                            'image': 'cheque_fingerprint',
                            'xpos':0.22, 'ypos':0.28,
                            'score': '80',
                            'compare': 'Mr. X'},
                        afis_processed = False)
    deskfoot = Evidence(name = 'deskfoot',
                        afis_details = {
                            'image': 'deskfoot_footprint',
                            'xpos':0.22, 'ypos':0.28,
                            'score': '40',
                            'compare': 'Nike Pegasus size 9'},
                        afis_processed = False)
    blood = Evidence(name = 'blood',
                        afis_details = {
                            'image': 'blood_footprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '0',
                            'compare': 'None'},
                        afis_processed = False)
    
    # declare afis relevant evidence
    afis_evidence = [bullet, cheque, deskfoot, blood]
    current_evidence = no_evidence

transform half_size:
    zoom 0.5

# The game starts here.
label start:
    $slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for inventory
    $slot_padding = 120 / 2
    $distance_slot = slot_size[0] + slot_padding
    $first_slot_x = 105 # inventory and toolbox
    $first_slot_y = 300 # inventory and toolbox
    $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    
    # inventory
    $inventory_SM = SpriteManager(event = inventoryEvents) # sprite manager that manages inventory items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all inventory sprite objects
    $inventory_items = [] # holds inventory items
    $inventory_db_enabled = False # determines whether down arrow on inventory hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether up arrow on inventory hotbar is enabled or not

    # toolbox:
    $toolbox_SM = SpriteManager(event = toolboxEvents)
    $toolbox_sprites = []
    $toolbox_items = []
    $toolbox_db_enabled = False
    $toolbox_ub_enabled = False

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(event = toolboxPopupEvents)
    $toolboxpop_sprites = []
    $toolboxpop_items = []
    $toolboxpop_db_enabled = False
    $toolboxpop_ub_enabled = False

    python:
        addToInventory(["bag", "tape", "physical_evidence", "digital_evidence"])
        addToToolbox(["gun_blue", "water", "bottle", "ninhydrin"])

    scene entering_lab_screen

label hallway_intro:
    scene lab_hallway_idle
    "Welcome to the lab!\nThis is where you can analyze the evidences you have collected from the scene."
    show screen full_inventory
    "All of your evidences can be accessed from the case files inside the evidences tab on the left."
    "Remember, you have to be in the correct room to be able to select evidences to conduct corresponding processes.\n(click anywhere to proceed)"
    call screen hallway_screen

label hallway:
    hide screen backtrack onlayer over_screens
    scene lab_hallway_idle
    hide screen afis_screen
    $ show_evidence = False
    $ show_toolbox = False
    $ current_evidence = no_evidence
    $ set_tool('')
    hide screen back_button_screen onlayer over_screens
    call screen hallway_screen

label data_analysis_lab:
    hide screen backtrack onlayer over_screens
    scene afis_interface
    show screen back_button_screen('hallway') onlayer over_screens
    $ set_tool('')
    "Pick digital evidence data in the digital evidences to compare prints against known prints using the print comparison software.\n(click anywhere to proceed)"
    call screen data_analysis_lab_screen

label materials_lab:
    hide screen backtrack onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    $ set_tool('')
    call screen materials_lab_screen

label fumehood_lab:
    $ set_tool('')
    scene fumehood_bg
    show screen back_button_screen('hallway') onlayer over_screens
    "Analyze your evidence using chemical methods here inside the fumehood."
    "Now pick an evidence from the physical evidences to analyze\n(click anywhere to proceed)"
    hide gloved_hands
    $ process_fumehood = True
    show screen inventory
    call screen fumehood_idle

label process_prompt:
    show screen back_button_screen('fumehood_lab') onlayer over_screens
    if current_evidence == bullet:
        scene bullet_placed
        "Start developing prints on the bullet casing (a metal and non-porous surface)"
        "First place clean bottles on mat and pour the needed liquids inside.\n(click anywhere to proceed)"
        hide screen inventory
        show screen toolbox
        call screen fumehood_screen
    elif current_evidence == cheque:
        scene cheque_placed
        "Start developing prints on the cheque (a paper surface)"
        call screen fumehood_screen
    else: 
        call screen fumehood_idle


# Bullet
label bullet_prep:
    hide fumehood_screen
    show screen backtrack onlayer over_screens
    scene bottle_placed_zoom
    "Prepare the water before starting to mix in the required chemical"
    call screen gun_blue_screen

label proceed_ten:
    hide screen gun_blue_ten
    show screen backtrack onlayer over_screens
    scene gb_ten
    "This is too much water, it could wash away our latent fingerprint impression evidence or develop it very slowly." 
    "Add more Gun Blue acid to this water to use it efficiently and enhance this evidence.\n(click anywhere to try again)"
    call screen gun_blue_ten

label proceed_fifty:
    hide screen gun_blue_ten
    hide screen gun_blue_fifty
    show screen backtrack onlayer over_screens
    $ set_tool('')
    scene bottle_gb
    "That is correct! This is the optimal dilution ratio because the acid is still able to work efficiently while the water level slows the reaction down enough for us to be able to keep a watchful eye on it."
    jump bullet_to_dip

label bullet_to_dip:
    hide gun_blue_fifty
    show screen backtrack onlayer over_screens
    $ set_tool('')
    scene bottle_gb
    "Now begin the development process by picking up the bullet with tweezers and dipping it into he chemicals.\n(click anywhere to proceed)"
    call screen bullet_dip

label gun_blue_ninty:
    hide screen gun_blue_ten
    hide screen gun_blue_fifty
    show screen backtrack onlayer over_screens
    scene gb_ninty
    "This is too much Gun Blue acid without any water dilution and the reaction will occur too quickly for us to watch carefully.\n(click anywhere to proceed with the 50:50 solution)"
    jump bullet_to_dip

label bullet_to_water:
    hide bullet_dip
    show screen backtrack onlayer over_screens
    scene bullet_dip_gb
    "Lift the exhibit out of 50:50 solution and place it in plain distilled water." 
    "The water will stop the reaction of the Gun Blue acid on the exhibit effectively so that it does not overdevelop and destroy the evidence.\n(click anywhere to proceed)"
    $ set_cursor('tweezer_bullet')
    call screen bullet_water

label bullet_to_photo:
    hide bullet_water
    show screen backtrack onlayer over_screens
    scene bullet_lift_water
    "The print development process is now complete. Proceed to Set up for photo (white background, evidence clipped to stand with ruler on side)\n(click anywhere to proceed)"
    call screen bullet_set_photo

label take_bullet:
    hide bullet_set_photo
    show screen backtrack onlayer over_screens
    $ set_tool('')
    scene bullet_take_photo with flash
    "Note: The fingerprint on the bullet casing did not develop so clearly that the photo can catch a complete print and its details."
    "Hence this print and photo will not be able to be processed by print comparison softwares with other prints."
    "Now secure the processed physical evidence into a new evidence bag and tape to store safely.\n(click anywhere to proceed)"
    hide screen toolbox
    show screen inventory
    call screen gun_blue_tobag


# Cheque        
label cheque_prep:
    hide fumehood_screen
    show screen backtrack onlayer over_screens
    scene cheque_placed
    "That is right! Ninhydrin is great for developing latent fingerprints on porous surfaces like paper."
    "Furthermore, it develops fingerprints into Ruhemann’s purple, great for contrast on white paper like ours here!"
    "Now pour the chemical into the tray and submerge the cheque inside.\n(click anywhere to proceed)"
    hide screen inventory
    show screen toolbox
    call screen ninhydrin_screen

label cheque_to_cabinet:
    hide ninhydrin_screen
    show screen backtrack onlayer over_screens
    scene cheque_pickup
    "Now bring the entire exhibit to the heating cabinet to dry off the excess.\n(click anywhere to proceed)"
    $ set_cursor('tray_cheque')
    call screen ninhydrin_cabinets

label cabinet_timer:
    scene cabinet_humidified
    $ curr_timer = 'cabinet'
    # Min and max time allowed as correct
    $ min_hours = 0 
    $ min_minutes = 4
    $ min_seconds = 0
    $ max_hours = 0
    $ max_minutes = 7
    $ max_seconds = 0
    jump timer

label dip_timer:
    scene bullet_dip_gb
    $ curr_timer = 'dip'
    "Wait for the Gun Blue to react and develop print"
    # Min and max time allowed as correct
    $ min_hours = 0 
    $ min_minutes = 0
    $ min_seconds = 10
    $ max_hours = 0
    $ max_minutes = 0
    $ max_seconds = 10
    jump timer

label timer_set:
    if curr_timer == 'cabinet':
        scene cabinet_humidified
    else:
        scene bullet_dip_gb

    # Calculations
    $ min_time = min_hours * 3600 + min_minutes * 60 + min_seconds
    $ max_time = max_hours * 3600 + max_minutes * 60 + max_seconds
    $ true_time = time_numbers[5] + time_numbers[4] * 10 + time_numbers[3] * 60 + time_numbers[2] * 600 + time_numbers[1] * 3600 + time_numbers[0] * 36000

    # Default messsages, customize to your liking
    if true_time >= min_time and true_time <= max_time:
        "That's correct."
        $ string_min_1 = "%d" % time_numbers[2]
        $ string_min_2 = "%d" % time_numbers[3]
        $ string_sec_1 = "%d" % time_numbers[4]
        $ string_sec_2 = "%d" % time_numbers[5]
        if string_min_1 == "0":
            if string_sec_1 != "0":
                "Waiting for [string_min_2] minutes and [string_sec_1][string_sec_2] seconds... (click anywhere to continue)"
            elif string_sec_2 != "0":
                "Waiting for [string_min_2] minutes and [string_sec_2] seconds... (click anywhere to continue)"
            else:
                "Waiting for [string_min_2] minutes... (click anywhere to continue)"
        else:
            if string_sec_1 != "0" and string_sec_2 != "0":
                "Waiting for [string_min_1][string_min_2] minutes and [string_sec_1][string_sec_2] seconds... (click anywhere to continue)"
            elif string_sec_2 != "0":
                "Waiting for [string_min_1][string_min_2] minutes and [string_sec_2] seconds... (click anywhere to continue)"
            else:
                "Waiting for [string_min_1][string_min_2] minutes... (click anywhere to continue)"
        if curr_timer == 'cabinet':
            jump cheque_to_photo
        else:
            jump bullet_to_water
    elif true_time < min_time:
        "That's not enough time, try again."
        jump timer
    elif true_time > max_time:
        "That's too much time, try again."
        jump timer

label cheque_to_photo:
    hide ninhydrin_cabinets
    show screen backtrack onlayer over_screens
    scene cabinet_done
    "The print development process is now complete. Fingerprints has shown at the back of the cheque."
    "Proceed to set up for photo (white background, evidence clipped to stand with ruler on side)\n(click anywhere to proceed)"
    call screen ninhydrin_set_photo

label take_cheque:
    hide ninhydrin_set_photo
    show screen backtrack onlayer over_screens
    $ set_tool('')
    scene ninhydrin_take_photo with flash
    "Now secure the processed physical evidence into a new evidence bag and tape to store safely.\n(click anywhere to proceed)"
    hide screen toolbox
    show screen inventory
    call screen ninhydrin_tobag


# To be called
label end:
    hide screen back_button_screen onlayer over_screens
    $ set_tool('')
    hide screen toolbox
    hide screen inventory
    scene lab_hallway_idle
    "Congratulations! You have finished the lab analysis portion."
    "Let's head on over to the court room."
    scene enter_courtroom_screen 

    return

