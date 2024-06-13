### The script of the game goes in this file.

# variable that describes whether current user is in the center (of all five possible positions)
default middle = True
# which direction currently looking at 
default front_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default curr_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default hallway_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default stove_directions = {'up': False, 'down': False, 'left': False, 'right': False}
# whether toolbox is currently displayed
default toolbox_show = False
# first time exploring toolbox?
default first_time_toolbox = True
# which tool is currently enabled (shown on screen)
default tools = { "tape" : False, "bag": False, "powder": False, "marker": False, "scalebar": False, "light": True, "lifting_tape": False}
# finished evidence collection?
default finish_collection = False
# finish tutorial
default finish_tutorial = False

init python:
    config.keymap['dismiss'].append('K_UP')
    config.keymap['dismiss'].append('K_DOWN')
    config.keymap['dismiss'].append('K_LEFT')
    config.keymap['dismiss'].append('K_RIGHT')


define s = Character("Supervisor")

### The game starts here.
label start:
    call screen opening_screen

label enter_splash_screen:
    scene entering_splash_screen
    with Dissolve(.8)
    call screen splash_screen

label instructions_text:
    scene instructions_bg
    with Dissolve(.8)
    call screen instructions_text_screen

label exposition:
    play music "ambient.mp3" volume 0.5
    hide screen instructions_text_screen
    "You sit and ponder whether you should drink you cup of coffee or read today's newspaper. \n\n\n>>hit space to continue"
    scene living_room_bg
    call screen exposition_click()

label coffee:
    call screen coffee_bitter

label newspaper:
    call screen newspaper_close_up

label phone:
    scene instructions_bg_idle
    play sound "phone.mp3"
    pause
    call screen phone_ring()


label supervisor_call:
    "Supervisor: Apologies for calling you in on a weekend but we need you on site ASAP! \n\n\n>>hit space to continue"
    "Supervisor: Come to Robarts Library. There's been a robbery! \n\n\n>>hit space to continue"
    "You quickly get up and head to Robarts. \n\n\n>>hit space to continue"
    scene black
    play sound "driving.mp3"
    "10 minutes later... \n\n\n>>hit space to continue"
    jump robarts_exterior

label robarts_exterior:
    stop music fadeout 1.0
    scene robarts_exterior
    "You finally arrive at Robarts and spot your supervisor. \n\n\n>>hit space to continue"
    show supervisor
    s "You're late."
    s "You're lucky I haven't fired you."
    s "Anyways, a rare and valuable manuscript has been stolen from the first floor of the Thomas Fisher Rare Book Library during a sophisticated heist that took place last night." 
    s "The thief was able to hijack the security system, however, a couple witnesses who were closeby at the time of the theft were able to snap a couple pictures of the thief as he fled the scene."
    s "Our forensics team also retrieved some critical information about the stolen manuscript that you might want to look at."
    s "Here, take a look."
    scene folder
    call screen file_folder()

label inside_library:
    scene robarts_exterior
    show supervisor
    s "Time to go inside!"
    scene task1
    pause
    scene thomas_fisher
    call screen task_1()

label tape:
    call screen tape()

label footprints:
    call screen footprints()

label footprint_collection:
    scene footprints_closeup
    call screen toolbox

label taped:
    if front_directions['left']:
        play sound "tape.mp3"
        scene left_taped
    elif front_directions['right']:
        play sound "tape.mp3"
        scene right_taped

label instructions_key_arrows:
    #show screen move_on
    hide screen instructions_text_screen
    "Great job! Now let's head back!"
    #hide screen move_on
    call screen instructions_key_screen()

label jump_directions:
    hide screen opening
    if middle:
        if front_directions['up']:
            $ curr_directions['up'] = True
            scene front_up
            show screen opening('looking up')
        elif front_directions['down']:
            $ curr_directions['down'] = True
            scene front_down
            show screen opening('looking down')
            show screen toolbox
        elif front_directions['right']:
            $ curr_directions['right'] = True
            scene right
            show screen opening('looking to the right')
        elif front_directions['left']:
            $ curr_directions['left'] = True
            scene left
            show screen opening('looking to the left')
        $ middle = False
        call screen instructions_key_screen()

    else:
        scene thomas_fisher
        show screen opening('back in center')
        python:
            middle = True
            for c_d in front_directions:
                front_directions[c_d] = False
            for c_d in curr_directions:
                curr_directions[c_d] = False
        call screen instructions_move_on_screen
        call screen instructions_key_screen()

label keep_exploring:
    call screen instructions_key_screen()

### entering scene 
label enter_scene:
    hide screen opening
    #show screen move_on
    "Great job! Let's move onto the next task! \n\n\n>>hit space to continue"
    scene task2
    pause
    #hide screen move_on
    scene manuscript_loc
    call screen task_2()
    
label hallway:
    hide screen entering_screen
    scene hallway
    with Dissolve(.8)
    #show screen move_on
    "You are looking at the hallway.\n\n\n>>hit space to continue"
    "You may click the arrow keys to explore the hallway. Once you are ready to move on, hit space.\n\n>>hit space to continue"
    call screen hallway_screen

label hallway_directions:
    if middle:
        if hallway_directions['up']:
            $ curr_directions['up'] = True
            scene hallway_up
        elif hallway_directions['down']:
            $ curr_directions['down'] = True
            scene hallway_down
        elif hallway_directions['right']:
            $ curr_directions['right'] = True
            scene hallway_right
        elif hallway_directions['left']:
            $ curr_directions['left'] = True
            scene hallway_left
        $ middle = False
        call screen hallway_screen
    else:
        scene hallway
        python:
            middle = True
            for c_d in hallway_directions:
                hallway_directions[c_d] = False
            for c_d in curr_directions:
                curr_directions[c_d] = False
        call screen hallway_screen

### kitchen scene
label stove_directions:
    if middle:
        if stove_directions['up']:
            scene stove_up
        elif stove_directions['down']:
            scene stove_down
        elif stove_directions['right']:
            scene stove_right
        elif stove_directions['left']:
            scene stove_left
        $ middle = False
        call screen stove_screen
    else:
        scene footprints_closeup
        python:
            middle = True
            for c_d in stove_directions:
                stove_directions[c_d] = False
        call screen stove_screen

label examination_kitchen:
    hide screen hallway_screen
    #show screen move_on
    scene kitchen_idle
    "This is the kitchen of the crime scene.\n\n\n>>hit space to continue"
    "Move your cursor around to find a surface to explore in greater detail.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen kitchen_screen

label examination_stove:
    hide screen kitchen_screen
    scene footprints_closeup
    show screen toolbox
    with Dissolve(.8)
    #show screen move_on
    "You are looking at the stove.\n\n\n>>hit space to continue"
    "Again, you may use the arrow keys to look around the stove.\n\n\n>>hit space to continue"
    "Once you are done exploring, try clicking on the toolbox.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen stove_screen
    
label tool_expand:
    $ default_mouse = ''

    scene footprints_closeup
    hide screen uv_light_stove
    show screen toolbox
    if toolbox_show:
        hide screen expand_tools
        show screen toolbox
        $ toolbox_show = False
    else:
        scene footprints_closeup
        show screen expand_tools
        $ toolbox_show = True
        if first_time_toolbox:
            $ first_time_toolbox = False
            #show screen move_on
            show screen arrow
            "You found some muddy footprints. Great job!"
            "The toolbox holds the various tools you may need to collect evidence in this stage.\n\n>>hit space to continue"
            show screen arrow
    if finish_collection:
        #hide screen move_on
        show screen move_on_lab
    call screen stove_screen
    show screen toolbox

label evidence_markers:
    $ default_mouse = 'evidence_markers'
    "These are evidence markers.\n\n\n>>hit space to continue"
    "These are used to mark and illustrate items of evidence at a crime scene.\n\n>>hit space to continue"
    show screen toolbox
    call screen stove_screen

label evident_tape:
    $ default_mouse = 'tape'
    "This is an evidence tape.\n\n>>hit space to continue"
    show screen toolbox
    call screen stove_screen
    
label uv_light:
    hide screen arrow
    $ default_mouse = 'uv_light'
    $ toolbox_show = False
    $ tools['powder'] = True
    hide screen toolbox
    hide screen expand_tools
    scene stove_fingerprint
    #show screen move_on
    "This is the flashlight.\n\n\n>>hit space to continue"
    "The flashlight enables you to perform a visual search and identify evidence that may not have been previously detected.\n\n>>hit space to continue"
    "Shine the light around the stove top to see what you can find. Remember to use the flashlight on an oblique angle!\n\n>>hit space to continue"
    "Once you find the evidence, click on it so that you remember its location.\n\n\n>>hit space to continue"
    call screen uv_light_stove
    
label finished_uv_light:
    $ default_mouse = ''
    $ tools['light'] = False
    scene stove_fingerprint_persist
    hide screen uv_light_stove
    show screen toolbox
    show screen expand_tools
    "After the visual search, you now know where the fingerprint is. To help you remember, a marker will be placed beside the evidence.\n\n>>hit space to continue"
    show screen evidence_marker_stove
    "Let's perform dusting to collect the print by clicking on the granular powder.\n\n>>hit space to continue"
    show screen arrow
    #hide screen move_on
    call screen expand_tools

label magnetic_powder:
    hide screen arrow
    $ default_mouse = 'magnetic_powder'
    $ toolbox_show = False
    $ tools['scalebar'] = True
    scene stove_fingerprint_persist
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_stove
    #show screen move_on
    "This is the black granular powder.\n\n\n>>hit space to continue"
    "Reveal the latent print with the powder by dusting on it.\n\n\n>>hit space to continue"
    call screen magnetic_powder_stove

label finished_magnetic_powder:
    $ default_mouse = ''
    $ tools['powder'] = False
    hide screen magnetic_powder_stove
    show screen toolbox
    show screen expand_tools
    #show screen move_on
    show screen evidence_marker_stove
    scene stove_fingerprint_dusted
    "Following dusting, we have fingerprint collection.\n\n\n>>hit space to continue"
    "The first step in fingerprint collection is to add a scalebar beside our evidence. Click on the scalebar.\n\n>>hit space to continue"
    show screen arrow
    #hide screen move_on
    call screen expand_tools

label scalebar:
    scene stove_fingerprint_zoomed
    hide screen arrow
    $ default_mouse = "scalebar"
    $ toolbox_show = False
    $ tools['lifting_tape'] = True
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_stove
    #show screen move_on
    "This is the scalebar.\n\n\n>>hit space to continue"
    "The scalebar helps to indicate the relative size of the evidence which will become helpful in later stages.\n\n>>hit space to continue"
    "Click on a surface next to the fingerprint to affix the scalebar. Make sure not to obscure the evidence.\n\n>>hit space to continue"
    call screen scalebar_stove


label finished_scalebar:
    $ default_mouse = ''
    $ tools['scalebar'] = False
    scene scalebar_taped
    hide screen scalebar_stove
    show screen toolbox
    show screen expand_tools
    #show screen move_on
    show screen evidence_marker_stove
    "Now we have to lift the fingerprint and document it on a backing card.\n\n\n>>hit space to continue"
    "Let's click on the lifting tape and the backing card.\n\n\n>>hit space to continue"
    show screen arrow
    #hide screen move_on
    call screen expand_tools

label lifting_tape:
    scene scalebar_lifting
    hide screen arrow
    $ default_mouse = "lifting_tape"
    $ toolbox_show = False
    $ tools['bag'] = True
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_stove
    #show screen move_on
    "This is the lifting tape.\n\n\n>>hit space to continue"
    "The tape is used to lift both the fingerprint and the  scalebar at once.\n\n\n>>hit space to continue"
    "Once lifted, we want to stick it onto a backing card for documentation purposes.\n\n>>hit space to continue"
    "Click on the fingerprint to lift.\n\n\n>>hit space to continue"
    call screen lifting_tape_stove

label lifting_to_backing:
    scene scalebar_lifting_taped
    $ default_mouse = ''
    "Now we have to lift and stick the tape onto a backing card.\n\n\n>>hit space to continue"
    "Click the tape to lift it.\n\n\n>>hit space to continue"
    call screen backing_card_stove('lift')

label drag_tape:
    $ default_mouse = 'tape_print_scalebar'
    call screen backing_card_stove('drag')

label stick_backing:
    $ default_mouse = ''
    show screen backing_card_stove('stick')
    "Great! You have successfully lifted the tape onto the backing card.\n\n\n>>hit space to continue"
    "Don't forget to fill out the information on the front and add the letter R to indicate directionality!\n\n>>hit space to continue"
    call screen backing_card_stove('complete_front')

label finish_lifting_tape:
    $ default_mouse = ''
    $ tools['lifting_tape'] = False
    scene footprints_closeup
    hide screen lifting_tape_stove
    show screen toolbox
    show screen expand_tools
    show screen evidence_marker_stove
    #show screen move_on
    "With your evidence collected, now we have to package it.\n\n\n>>hit space to continue"
    "Click on the evidence bags to package the collected fingerprint.\n\n\n>>hit space to continue"
    show screen arrow
    #hide screen move_on
    call screen expand_tools

label evidence_bags:
    $ default_mouse = 'evidence_bags'
    $ toolbox_show = False
    hide screen arrow
    scene footprints_closeup
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_stove
    #show screen move_on
    scene stove_evidence_bags
    with Dissolve(.5)
    show screen current_evidence('insensitive')
    "Here is the evidence you have gathered so far.\n\n\n>>hit space to continue"
    "To package a piece of evidence, drag it into the bag.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen current_evidence('show')

label drag_card_into_bag:
    $ default_mouse = 'tape_print_scalebar'
    call screen current_evidence('drag')

label put_card_into_bag:
    $ default_mouse = ''
    call screen current_evidence('put_in')

label evidence_bags_finished:
    $ default_mouse = ''
    $ tools['bag'] = False
    $ tools['tape'] = True
    scene footprints_closeup
    hide screen current_evidence
    show screen toolbox
    show screen expand_tools
    show screen evidence_marker_stove
    #show screen move_on
    #scene stove_fingerprint
    "Lastly, let's secure the bag to prevent tampering of any kind.\n\n\n>>hit space to continue"
    "Click on the tamper evidence tape.\n\n\n>>hit space to continue"
    show screen arrow
    #hide screen move_on
    #"Congratulations! You have now finished evidence collection for this stage."
    #$ finish_collection = True
    call screen expand_tools

label tamper_tape:
    hide screen arrow
    $ default_mouse = 'tape'
    $ toolbox_show = False
    $ tools['tape'] = False
    scene seal_evidence_bags
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_stove
    #show screen move_on
    show screen tamper_evident_tape_stove(False)
    "Click on the evidence bag to seal it.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen tamper_evident_tape_stove(True)


label  tutorial_finished:
    $ default_mouse = ''
    $ tools['bag'] = False
    scene footprints_closeup
    hide screen current_evidence
    show screen toolbox
    show screen expand_tools
    #show screen move_on
    if not finish_tutorial:
        show screen evidence_marker_stove
        "With the evidence collected, we can now remove our evidence marker.\n\n\n>>hit space to continue"
        $ finish_tutorial = True
    hide screen evidence_marker_stove
    "Congratulations! You have now finished evidence collection for this stage.\n\n\n>>hit space to continue"
    $ finish_collection = True
    call screen evidence_to_lab

label enter_lab:
    hide screen stove_center
    hide screen move_on_lab
    hide screen toolbox
    hide screen expand_tools
    #hide screen move_on
    scene entering_lab_screen
    with Dissolve(.8)
    call screen temporary_pause


    return



