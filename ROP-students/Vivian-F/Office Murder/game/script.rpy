# whether the screen in the main screen (office)
default on_main_screen = True
# whether uv_light is currently activated
default uv_light = False
# whether toolbox is currently displayed
default toolbox_show = False
# whether casefiles are currently displayed
default case_file_show = False
# whether evidence inside the casefiles are currently displayed
default case_file_evidence_show = False
# current cursor
default current_cursor = ''


# which tool is currently enabled (shown on screen)
default tools = { "marker" : False, "light": False, "magnetic": False, "stone": False, "ruler_tag": False, "bucket": False, "water": False, "hungarian_red": False, "knife": False, "bag": False}

# whether tool is enable for this scene
default scene_enable = { "marker" : False, "light": False, "magnetic": False, "stone": False, "ruler_tag": False, "bucket": False, "water": False, "hungarian_red": False, "knife": False, "bag": False}

# whether the item should be examined
default should_be_examined = {'deskfoot': False, 'blood': False, "bullet": False, "cheque": False}

# whether the evidence_marker is set
default evidence_marker_set = {'deskfoot': False, "blood": False, 'bullet': False, 'cheque': False}

# which evidence has been processed
default evidence_list = ['deskfoot', "blood", 'bullet', 'cheque']
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
        global uv_light

        if tools[tool]:
            tools[tool] = False
            if tool == 'light': uv_light = False
        else:
            tools[tool] = True
            for t in tools:
                if t!= tool:
                    tools[t] = False
            if tool != 'light' or tool == '':
                uv_light = False
            else:
                uv_light = True
        
    # Enable tool in scene
    def set_scene_enable(set_):
        global scene_enable
        if set_:
            for t in scene_enable:
                scene_enable[t] = True
        else:
            for t in scene_enable:
                scene_enable[t] = False
        scene_enable['light'] = True

    # Proceed if placed markers
    def check_scene_validation(scene):
        global evidence_marker_set
        global scene_enable
        global tools
        if not evidence_marker_set[scene]: 
            set_scene_enable(False)
            return False
        set_scene_enable(True)
        tools['marker'] = False
        return True

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
    "Your job now is to analyze the scene and collect evidence to find the murderer."

label store_start:
    scene office_bg
    with Dissolve(1.0)
    show screen case_files_screen onlayer over_screens
    show screen toolbox_screen onlayer over_toolbox
    call screen scene_office

label show_deskfoot:
    hide screen scene_office
    $ on_main_screen = False

    # $ check_scene_validation('deskfoot')
    # if 'tabletop' not in processed:
    #     image "deskfoot_zoom"
    #     "Looks like there is a waxy footprint on the desk, you heard from a professor that there had been a popcorn spill in the kitchen next door last night."
    show screen back_button_screen('scene_office', 'scene_deskfoot') onlayer over_screens
    call screen scene_deskfoot
    
label show_blood:
    hide screen scene_office
    $ on_main_screen = False

    # $ check_scene_validation('blood')
    show screen back_button_screen('scene_office', 'scene_blood') onlayer over_screens
    call screen scene_blood

label show_bullet:
    hide screen scene_office
    $ on_main_screen = False

    # $ check_scene_validation('bullet')
    # if 'bullet' not in processed:
    #     image "bullet_zoom"
    #     "Send bullet to lab for further investigation."
    show screen back_button_screen('scene_office', 'scene_bullet') onlayer over_screens
    call screen scene_bullet

label show_cheque:
    hide screen scene_office
    $ on_main_screen = False

    # $ check_scene_validation('cheque')
    # if 'cheque' not in processed:
    #     image "cheque_zoom"
    #     "Send cheque to lab for further investigation."
    show screen back_button_screen('scene_office', 'scene_cheque') onlayer over_screens
    call screen scene_cheque

label end:
    if processed == evidence_list:
        "You have collected all evidences on site, now proceed to the lab!"

return