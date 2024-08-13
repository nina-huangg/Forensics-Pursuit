# whether the screen in the main screen (office)
default on_main_screen = True
# whether casefiles are currently displayed
default case_file_show = False
# whether photos inside the camera is currently displayed
default camera_photo_show = False
# current cursor
default current_cursor = ''

# transition for photo taking flash (0 in/out so middle screen don't last long)
define flash = Fade(.25, 0, 0, color="#fff")

# whether the item should be examined
default should_be_examined = {'deskfoot': False, 'blood': False, "bullet": False, "cheque": False}
# whether the evidence_marker is set
default evidence_marker_set = {'deskfoot': False, 'blood': False, "bullet": False, "cheque": False}
# which evidence has been processed (add once processed)
default processed = []
default photoed = []
# counter to flip through camera for evidences photos
default photo_counter = 0

# hold evidence marker number for each evidence
default num_deskfoot = ''
default num_blood = ''
default num_bullet = ''
default num_cheque = ''

# tools list and which are currently enabled (shown on screen)
default inventory_item_names = ["Magnetic Black ", "Magnetic White", "Marker", "Bag", "Tape", "Tag", "Ruler", "Knife", "Hungarian Red", "Brush", "Applicator", "Ziplock", "Stone", "Water", "Camera", "Evidences"] # holds names for inspect pop-up text 
default tools = {"magnetic_black": False, "magnetic_white": False, "marker": False, "bag" : False, "tape": False, "tag": False, "ruler": False, "knife": False, "hungarian_red": False, "brush": False, "applicator": False, "ziplock": False, "stone": False, "water": False}
default tools_counter = 3


# Python helper functions
init python:
    # Change cursor
    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor

    # Toggle tool in tools list & set cursor to the tool 
    def set_tool(tool_name):
        global tools

        if tools[tool_name]:
            set_cursor('')
            tools[tool_name] = False
        else:
            set_cursor(tool_name)
            tools[tool_name] = True
            for t in tools:
                if t!= tool_name:
                    tools[t] = False

    # Add evidence to processed list
    def finished_process(evidence):
        global processed
        processed.append(evidence)
    
    def add_photo(evidence):
        global photoed
        photoed.append(evidence)

    # Add/subtract to counter to change current displaying photo index
    def photo_switch(cmd):
        global photo_counter
        if cmd == 'next':
            if photo_counter + 1 < len(photoed):
                photo_counter += 1
        elif cmd == 'prev':
            if photo_counter - 1 >= 0:
                photo_counter -= 1
        else:
            photo_counter = 0
    
    # Add/subtract to counter to change current displaying photo index
    def tools_switch(cmd):
        global tools_counter
        if cmd == 'next':
            if tools_counter + 4 < len(tools):
                tools_counter += 1
        elif cmd == 'prev':
            if tools_counter - 1 >= 3:
                tools_counter -= 1
        else:
            tools_counter = 3

transform half_size:
    zoom 0.5

# Labels of scenes, calls screens in custom_screens
# Start scenes: bahen
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
        addToInventory(["bag", "tape", "camera", "evidences"])
        addToToolbox(["marker", "ruler", "tag", "brush", "applicator", "hungarian_red", "knife", 
        "ziplock", "stone", "water"])
        addToToolboxPop(["magnetic_black", "magnetic_white"])

    scene bahen
    "Yesterday midnight, the Bahen Centre security guard's body was found in an office room in the building."
    "Your job now is to analyze the scene and collect evidences."
    # jump gloves_start
    jump office_start

# Gloves code currently commented out until found grey/non-colored hands
# label gloves_start:
#     scene office_bg
#     "First, put on your gloves!"
#     show hands
#     call screen gloves

# label gloves2:
#     hide hands
#     "Now let's enter the scene!"
#     jump office_start

# Main screen, comes back after each evidence collection
# Every time back, change cursor to default and turn off all layovers, only icon
label office_start:
    scene office_bg
    show screen full_inventory
    hide screen back_button_screen onlayer over_screens
    $ set_cursor('')
    if not all(evidence_marker_set[evidence] for evidence in evidence_marker_set):
        "Spot the evidence locations and mark them with the evidence markers in tools before analyzing its details."
    call screen scene_office
    

# All evidence scene preps: not main screen, default pop tools, reset cursor, call screen
# Preps deskfoot scene
label show_deskfoot:
    hide screen scene_office
    hide screen camera_screen onlayer over_camera
    hide screen case_files_screen onlayer over_screens
    $ on_main_screen = False
    # Show background prompt first before analyze
    if 'deskfoot' not in processed:
        scene deskfoot_zoom
        "Looks like there is a waxy footprint on the desk, you heard from a professor that there 
        had been a popcorn spill in the kitchen next door last night. (click to start development)"
    else:
        show screen back_button_screen('office_start', 'scene_deskfoot') onlayer over_screens
    call screen scene_deskfoot

label deskfoot_dusted:
    scene deskfoot_dust_clear
    "Now with a clear dusted print, you want to cast it using the KNAAP technique"
    "Start with grabbing an empty clean ziplock bag, put a layer of dental stone powder, then gradually add water to make a mix of correct consisitency"
    call screen scene_deskfoot_tomix

# Called back here from screen scene_deskfoot to flash photo-shoot, back to screen to bag
label take_deskfoot:
    scene deskfoot_tagged
    with flash
    call screen scene_deskfoot_tobag

# Preps blood scene
label show_blood:
    hide screen scene_office
    $ on_main_screen = False
    if 'blood' not in processed:
        scene blood_zoom
        "First, place down the ruler in preparation of an initial photo of the blood stain before proceeding to develop print."
    else:
        show screen back_button_screen('office_start', 'scene_blood') onlayer over_screens
    call screen scene_blood

# From screen scene_blood to flash, back to screen to bag
label take_blood:
    scene camera_blood
    with flash
    scene blood_ruler
    "Now you can proceed with using the appropriate chemical"
    call screen scene_blood_tospray

label blood_tocut:
    scene blood_sprayed
    "Note: no print seems to show, it turns out that hungarian red spraying on carpet material will not reveal clear blood patterns since we cannot wash off the excess."
    "Now proceed to carve out the area of carpet you would file as evidence before photographing this"
    call screen scene_blood_tocut

label take_blood_sprayed:
    scene camera_blood_sprayed
    with flash
    call screen scene_blood_tobag

# Preps bullet scene
label show_bullet:
    hide screen scene_office
    $ on_main_screen = False
    if 'bullet' not in processed:
        scene bullet_zoom
        "Record this evidence and send it to lab for further investigation. (click anywhere to proceed)"
    else:
        show screen back_button_screen('office_start', 'scene_bullet') onlayer over_screens
    call screen scene_bullet

# From screen scene_bullet to flash, back to screen to bag
label take_bullet:
    scene camera_bullet
    with flash
    call screen scene_bullet_tobag

# Preps cheque scene
label show_cheque:
    hide screen scene_office
    $ on_main_screen = False
    if 'cheque' not in processed:
        scene cheque_zoom
        "Record this evidence and send it to lab for further investigation. (click anywhere to proceed)"
    else:
        show screen back_button_screen('office_start', 'scene_cheque') onlayer over_screens
    call screen scene_cheque

# From screen scene_cheque to flash, back to screen to bag
label take_cheque:
    scene camera_cheque
    with flash
    call screen scene_cheque_tobag

# Here from screen scene_office once all evidence processed and user pressed to proceed to lab
label end:
    # Turn off all crime scene layers (back to bahen for now as lab is to be implemented)
    hide screen scene_office
    scene bahen
    "Lab to be implemented"

return