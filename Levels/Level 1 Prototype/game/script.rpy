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
default should_be_examined = {'books': False, 'cabinet': False, 'footprints': True, "screwdriver": True, 'window': True}

# whether the evidence_marker is set
default evidence_marker_set = {'footprints': False, "screwdriver": False, 'window':False, 'exam': False, 'computer': False}

# whether tool is enable for this scene
default scene_enable = { "tape" : False, "bag": False, "powder": False, "marker": True, "scalebar": False, "light": True, "lifting_tape": False,'gel_lift':False}

# which evidence has been processed
default processed = []

# which office perspective to show # 0 == main
default keyboard_scene_counter = 0

# scenes
default scenes = ['office_bg','office_bg_perspective1','office_bg_perspective2','office_bg_perspective3','office_bg_perspective4']

# evidence photos, evidence photos counter
default evidence_photos = ['office_bg_perspective1','office_bg_perspective2','office_bg_perspective3','office_bg_perspective4']
default evidence_photos_counter = 0

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
    
    def keyboard_switch(key):
        global keyboard_scene_counter
        global scenes
        if key == 'right':
            if keyboard_scene_counter == 0:
                keyboard_scene_counter = len(scenes)-1
            else:
                keyboard_scene_counter -= 1
            
        else:
            if keyboard_scene_counter == len(scenes)-1:
                keyboard_scene_counter = 0
            else:
                keyboard_scene_counter += 1
    
    def photo_append(photo):
        global evidence_photos

        pictures = {
            'screwdriver': ['casefile_photos_screwdriver1','casefile_photos_screwdriver2'],
            'exam':['casefile_photos_exam1'],
            'computer':['casefile_photos_computer1']
        }

        for item in pictures[photo]:
            evidence_photos.append(item)

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
    
    scene intro_scene
    "You've arrived at the crime scene."
    "A break and enter seem to have occurred in Professor Smith's office."
    "Let's use your forensics knowledge to solve this crime case!"
    scene office_bg
    with Dissolve(1.0)

    
label office_start:
    show screen case_files_screen onlayer over_screens
    show screen toolbox_screen onlayer over_toolbox
    
    call screen scene_office

label show_office_footprints:
    hide screen scene_office
    $ on_main_screen = False

    $ check_scene_validation('footprints')
    show screen back_button_screen('scene_office', 'scene_footprints') onlayer over_screens
    call screen scene_footprints
    
    # if not evidence_marker_set['footprints']:
    #     show screen screen_examine_ignore('footprints') onlayer over_screens
    
label show_office_screwdriver:
    hide screen scene_office
    $ on_main_screen = False

    $ check_scene_validation('screwdriver')
    show screen back_button_screen('scene_office', 'scene_screwdriver') onlayer over_screens
    # if not evidence_marker_set['screwdriver']:
    #     show screen screen_examine_ignore('screwdriver') onlayer over_screens
    call screen scene_screwdriver

label show_office_exam:
    hide screen scene_office
    $ on_main_screen = False

    $ check_scene_validation('exam')
    show screen back_button_screen('scene_office', 'scene_exam') onlayer over_screens
    call screen scene_exam

label show_office_computer:
    hide screen scene_office
    $ on_main_screen = False

    $ check_scene_validation('computer')
    show screen back_button_screen('scene_office', 'scene_computer') onlayer over_screens
    call screen scene_computer

label show_office_window:
    hide screen scene_office
    $ on_main_screen = False
    
    show screen back_button_screen('scene_office', 'scene_window') onlayer over_screens
    # if not evidence_marker_set['window']:
    #     show screen screen_examine_ignore('window') onlayer over_screens
    call screen scene_window

label show_office_books_cabinet:
    hide screen scene_office
    $ on_main_screen = False

    show screen back_button_screen('scene_office', 'scene_books_cabinet') onlayer over_screens
    # show screen screen_examine_ignore('books') onlayer over_screens
    # show screen scene_books_cabinet
    # "Let's check if there's anything written in these books."
    call screen scene_books_cabinet

label show_office_books_bookshelves:
    hide screen scene_office
    $ on_main_screen = False

    show screen back_button_screen('scene_office', 'scene_books_bookshelves') onlayer over_screens
    call screen scene_books_bookshelves

return
