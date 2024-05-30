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
default tools = { "tape" : False, "bag": False, "powder": False, "marker": False, "scalebar": False, "light": False, "lifting_tape": False, 'gel_lift':False}

# whether the item should be examined
default should_be_examined = {'tabletop': False, 'inside_footprints': False, "jewel": False}

# whether the evidence_marker is set
default evidence_marker_set = {'jewel': False, "inside_footprints": False, 'tabletop':False}

# whether tool is enable for this scene
default scene_enable = { "tape" : False, "bag": False, "powder": False, "marker": True, "scalebar": False, "light": True, "lifting_tape": False,'gel_lift':False}

# which evidence has been processed
default processed = []

# scenes
default scenes = ['store_bg']


init python:
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
        
    def set_scene_enable(set_):
        global scene_enable
        if set_:
            for t in scene_enable:
                scene_enable[t] = True
        else:
            for t in scene_enable:
                scene_enable[t] = False
        scene_enable['light'] = True

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

    def finished_process(evidence):
        global processed
        processed.append(evidence)


image lifting:
    "lift1.png"
    pause 0.5
    "lift2.png"
    pause 0.3
    "lift3.png"
    pause 0.2
    "lift4.png"
    pause 0.3
    "lift5.png"
    pause 0.3


label start: 
    scene storefront
    "You've arrived at the crime scene."
    "A robbery has occured in a jewelry store. \n\n Their doors and display cases have been broken through and jewelry were stolen."
    "Let's use your forensics knowledge to solve this crime case!"
    "Do you want to first analyze the storefront floor or the inside?"

    menu:
        "Storefront":
            jump show_storefront

        "Inside":
            jump store_start

label store_start:
    scene store_bg
    with Dissolve(1.0)
    show screen case_files_screen onlayer over_screens
    show screen toolbox_screen onlayer over_toolbox
    call screen scene_store

label show_tabletop:
    hide screen scene_store
    $ on_main_screen = False

    $ check_scene_validation('tabletop')
    show screen back_button_screen('scene_store', 'scene_tabletop') onlayer over_screens
    call screen scene_tabletop
    
label show_jewel:
    # hide screen scene_store
    # $ on_main_screen = False

    # $ check_scene_validation('jewel')
    # show screen back_button_screen('scene_store', 'scene_jewel') onlayer over_screens
    # call screen scene_jewel
    "Jewel to be examined"
    call screen scene_store


label show_inside_footprints:
    hide screen scene_store
    $ on_main_screen = False

    $ check_scene_validation('inside_footprints')
    show screen back_button_screen('scene_store', 'scene_inside_footprints') onlayer over_screens
    call screen scene_inside_footprints
    #to be completed

label show_storefront:
    "Storefront scene to be implemented for checking outside footprint."
    "Let's start with the inside."
    jump store_start

# label show_outside_footprints:
#     hide screen scene_store
#     $ on_main_screen = False

#     $ check_scene_validation('outside_footprints')
#     show screen back_button_screen('scene_store', 'scene_outside_footprints') onlayer over_screens
#     call screen scene_outside_footprints

return