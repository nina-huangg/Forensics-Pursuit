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

define flash = Fade(.25, 0, .75, color="#fff")

# which tool is currently enabled (shown on screen)
default tools = {"applicator": False, "bag" : False, "hungarian_red": False, "knife": False, "magnetic_black": False, "magnetic_white": False, "ruler": False, "stone": False, "water": False, "ziplock": False}
# , "tag": False

# whether the item should be examined
default should_be_examined = {'deskfoot': False, 'blood': False, "bullet": False, "cheque": False}

# which evidence has been processed
default processed = []

# scenes
default scenes = ['office_bg']


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

    # Set tool T/F + set cursor to the tool 
    def set_tool(tool):
        set_cursor(tool)
        global tools

        if tools[tool]:
            tools[tool] = False
        else:
            tools[tool] = True
            for t in tools:
                if t!= tool:
                    tools[t] = False

    def on_main_screen():
        if not renpy.current_screen():
            return True
        return False

    # Add evidence to processed list
    def finished_process(evidence):
        global processed
        processed.append(evidence)



label start: 
    scene bahen
    "Yesterday midnight, the Bahen Centre security guard was murdered in an office room."
    "The officer ahead had already placed down the evidence markers.\n\nYour job now is to analyze the scene and collect evidence to find the murderer."

label office_start:
    scene office_bg
    $ default_mouse = ''
    $ toolbox_show = False
    $ case_file_show = False
    $ camera_photo_show = False
    show screen case_files_screen onlayer over_screens
    show screen camera_screen onlayer over_camera
    show screen toolbox_screen onlayer over_toolbox
    if all(evidence in processed for evidence in should_be_examined):
        $ case_file_show = True
        call screen end
    else:
        call screen scene_office

label show_deskfoot:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_deskfoot') onlayer over_screens
    if 'tabletop' not in processed:
        scene deskfoot_zoom
        "Looks like there is a waxy footprint on the desk, you heard from a professor that there 
        had been a popcorn spill in the kitchen next door last night. (click to start development)"
    call screen scene_deskfoot

label take_deskfoot:
    scene deskfoot_tagged
    with flash
    call screen scene_deskfoot_tobag
    
label show_blood:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_blood') onlayer over_screens
    call screen scene_blood

label take_blood:
    scene blood_ruler
    with flash
    call screen scene_blood_tobag
    
label show_bullet:
    hide screen scene_office
    $ on_main_screen = False
    $ toolbox_show = True
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    show screen back_button_screen('office_start', 'scene_bullet') onlayer over_screens
    if 'bullet' not in processed:
        scene bullet_zoom
        "An evidence marker is conveniently placed already!\nNow send bullet to lab for further investigation. (click anywhere to start bagging)"
    call screen scene_bullet

label take_bullet:
    scene bullet_zoom
    with flash
    call screen scene_bullet_tobag
 
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

label take_cheque:
    scene cheque_zoom
    with flash
    call screen scene_cheque_tobag
 
label end:
    hide screen case_files_screen onlayer over_screens
    hide screen camera_screen onlayer over_camera
    hide screen toolbox_screen onlayer over_toolbox
    hide screen scene_office
    scene bahen
    "Lab to be implemented"

return