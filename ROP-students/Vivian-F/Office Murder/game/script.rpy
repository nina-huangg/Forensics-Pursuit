# whether the screen in the main screen (office)
default on_main_screen = True
# whether toolbox is currently displayed
default toolbox_show = False
# whether casefiles are currently displayed
default case_file_show = False
# whether evidence inside the casefiles are currently displayed
default case_file_evidence_show = False
# whether camera is currently displayed
default camera_show = False
# whether photos inside the camera is currently displayed
default camera_photo_show = False
# current cursor
default current_cursor = ''

# transition for photo taking flash
define flash = Fade(.25, 0, .75, color="#fff")

# which tool is currently enabled (shown on screen)
default tools = {"magnetic_black": False, "magnetic_white": False, "marker": False, "bag" : False, "tape": False, "tag": False, "ruler": False, "knife": False, "hungarian_red": False, "brush": False, "applicator": False, "ziplock": False, "stone": False, "water": False}
default tools_image_list = ["magnetic_black_idle", "magnetic_white_idle", "marker_idle", "bag_idle", "tape_idle", "tag_idle", "ruler_idle", "knife_idle", "hungarian_red_idle", "brush_idle", "applicator_idle", "ziplock_idle", "stone_idle", "water_idle"]
default tools_name_list = ["magnetic_black", "magnetic_white", "marker", "bag", "tape", "tag", "ruler", "knife", "hungarian_red", "brush", "applicator", "ziplock", "stone", "water"]
default tools_counter = 3

# whether the item should be examined
default should_be_examined = {'deskfoot': False, 'blood': False, "bullet": False, "cheque": False}

# whether the evidence_marker is set
default evidence_marker_set = {'deskfoot': False, 'blood': False, "bullet": False, "cheque": False}

# which evidence has been processed (add once processed)
default processed = []

# evidence photos list (add once processed), evidence photos counter (to flip through camera)
default evidence_photos = []
default evidence_photos_counter = 0

# whether second level toolbox shows for different magnetic powder choices
default mag_powder_show = False


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
    def set_tool(tool):
        global tools

        if tools[tool]:
            set_cursor('')
            tools[tool] = False
        else:
            set_cursor(tool)
            tools[tool] = True
            for t in tools:
                if t!= tool:
                    tools[t] = False

    # Add evidence to processed list
    def finished_process(evidence):
        global processed
        processed.append(evidence)

    # Add photo to camera photo list
    def add_photo(photo):
        global evidence_photos
        pictures = {
            'deskfoot': ['camera_deskfoot'],
            'blood':['camera_blood'],
            'bullet':['camera_bullet'],
            'cheque':['camera_cheque']
        }
        evidence_photos.append(pictures[photo])
    
    # Add/subtract to counter to change current displaying photo index
    def photo_switch(cmd):
        global evidence_photos_counter
        if cmd == 'next':
            if evidence_photos_counter + 1 < len(evidence_photos):
                evidence_photos_counter += 1
        elif cmd == 'prev':
            if evidence_photos_counter - 1 >= 0:
                evidence_photos_counter -= 1
        else:
            evidence_photos_counter = 0
    
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



# Labels of scenes, calls screens in custom_screens
label start: 
    scene bahen
    "Yesterday midnight, the Bahen Centre security guard's body was found in an office room in the building."
    "Your job now is to analyze the scene and collect evidences."

# Main screen, comes back after each evidence collection
# Every time back, change cursor to default and turn off all layovers, only icon
label office_start:
    scene office_bg
    $ set_cursor('')
    $ toolbox_show = False
    $ case_file_show = False
    $ camera_photo_show = False
    show screen case_files_screen onlayer over_screens
    show screen camera_screen onlayer over_camera
    show screen toolbox_screen onlayer over_toolbox
    call screen scene_office

# All evidence scene preps: not main screen, default pop tools, reset cursor, call screen
# Preps deskfoot scene
label show_deskfoot:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_deskfoot') onlayer over_screens
    # Show background prompt first before analyze
    if 'deskfoot' not in processed:
        scene deskfoot_zoom
        "Looks like there is a waxy footprint on the desk, you heard from a professor that there 
        had been a popcorn spill in the kitchen next door last night. (click to start development)"
    call screen scene_deskfoot

# Called back here from screen scene_deskfoot to flash photo-shoot, back to screen to bag
label take_deskfoot:
    scene deskfoot_tagged
    with flash
    call screen scene_deskfoot_tobag

# Preps blood scene
label show_blood:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_blood') onlayer over_screens
    call screen scene_blood

# From screen scene_blood to flash, back to screen to bag
label take_blood:
    scene blood_ruler
    with flash
    call screen scene_blood_tobag

# Preps bullet scene
label show_bullet:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_bullet') onlayer over_screens
    if 'bullet' not in processed:
        scene bullet_zoom
        "An evidence marker with ruler is conveniently placed already!\nNow send bullet to lab for further investigation. (click anywhere to start bagging)"
    call screen scene_bullet

# From screen scene_bullet to flash, back to screen to bag
label take_bullet:
    scene bullet_zoom
    with flash
    call screen scene_bullet_tobag

# Preps cheque scene
label show_cheque:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_cheque') onlayer over_screens
    if 'cheque' not in processed:
        scene cheque_zoom
        "Send cheque to lab for further investigation. (click anywhere to start bagging)"
    call screen scene_cheque

# From screen scene_cheque to flash, back to screen to bag
label take_cheque:
    scene cheque_zoom
    with flash
    call screen scene_cheque_tobag

# Here from screen scene_office once all evidence processed and user pressed to proceed to lab
label end:
    # Turn off all crime scene layers (back to bahen for now as lab is to be implemented)
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    hide screen toolbox_screen onlayer over_toolbox
    hide screen scene_office
    scene bahen
    "Lab to be implemented"

return