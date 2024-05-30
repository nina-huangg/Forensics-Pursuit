### The script of the game goes in this file.

# variable that describes whether current user is in the center (of all five possible positions)
default middle = True
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
default table_directions = {'up': False, 'down': False, 'left': False, 'right': False}

init python:
    config.keymap['dismiss'].append('K_UP')
    config.keymap['dismiss'].append('K_DOWN')
    config.keymap['dismiss'].append('K_LEFT')
    config.keymap['dismiss'].append('K_RIGHT')

label start:
    call screen opening_screen

label enter_splash_screen:
    scene entering_splash_screen
    with Dissolve(.8)
    call screen splash_screen

label instructions_text:
    scene exterior
    "You've arrived at the crime scene."
    "A break and enter seem to have occured in this jewelry store."
    "Let's use your forensics knowledge to solve this crime case!"
    scene interior_idle
    with Dissolve(1.0)

label investigate_inside:
    call screen inside_screen
    
label examination_table:
    hide screen inside_screen
    scene table
    show screen toolbox
    with Dissolve(.8)
    "You can check the surrounding by clicking < "
    call screen table_screen
    

label tool_expand:
    $ default_mouse = ''
    scene table
    hide screen uv_light_table
    show screen toolbox
    if toolbox_show:
        hide screen expand_tools
        show screen toolbox
        $ toolbox_show = False
    else:
        scene table
        show screen expand_tools
        $ toolbox_show = True
        if first_time_toolbox:
            $ first_time_toolbox = False
            "Let's start by using the flashlight."
    if finish_collection:
        show screen move_on_lab
    scene table
    show screen toolbox

label table_directions:
    if middle:
        if table_directions['left']:
            scene table_left
        $ middle = False
        call screen table_screen
    else:
        scene table
        python:
            middle = True
            for c_d in table_directions:
                table_directions[c_d] = False
        call screen table_screen

label evidence_markers:
    $ default_mouse = 'evidence_markers'
    "These are evidence markers.\n\n\n>>hit space to continue"
    "These are used to mark and illustrate items of evidence at a crime scene.\n\n>>hit space to continue"
    show screen toolbox
    call screen table_screen

label evident_tape:
    $ default_mouse = 'tape'
    # "This is an evidence tape.\n\n>>hit space to continue"
    show screen toolbox
    call screen table_screen
    
label uv_light:
    $ default_mouse = 'uv_light_resized'
    $ toolbox_show = False
    $ tools['powder'] = True
    hide screen toolbox
    hide screen expand_tools
    scene table_fingerprint
    #show screen move_on
    # "This is the flashlight.\n\n\n>>hit space to continue"
    # "The flashlight enables you to perform a visual search and identify evidence that may not have been previously detected.\n\n>>hit space to continue"
    # "Shine the light around the stove top to see what you can find. Remember to use the flashlight on an oblique angle!\n\n>>hit space to continue"
    # "Once you find the evidence, click on it so that you remember its location.\n\n\n>>hit space to continue"
    call screen uv_light_table
    
label finished_uv_light:
    $ default_mouse = ''
    $ tools['light'] = False
    scene table_fingerprint_persist
    hide screen uv_light_table
    show screen toolbox
    show screen expand_tools
    "After the visual search, you now know where the fingerprint is. To help you remember, a marker will be placed beside the evidence.\n\n>>hit space to continue"
    show screen evidence_marker_table
    # "Let's perform dusting to collect the print by clicking on the granular powder.\n\n>>hit space to continue"
    #hide screen move_on
    call screen expand_tools

label magnetic_powder:
    $ default_mouse = 'magnetic_powder_resized'
    $ toolbox_show = False
    $ tools['scalebar'] = True
    scene table_fingerprint_persist
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_table
    #show screen move_on
    # "This is the black granular powder.\n\n\n>>hit space to continue"
    # "Reveal the latent print with the powder by dusting on it.\n\n\n>>hit space to continue"
    call screen magnetic_powder_table

label finished_magnetic_powder:
    $ default_mouse = ''
    $ tools['powder'] = False
    hide screen magnetic_powder_table
    show screen toolbox
    show screen expand_tools
    #show screen move_on
    show screen evidence_marker_table
    scene table_fingerprint_dusted
    # "Following dusting, we have fingerprint collection.\n\n\n>>hit space to continue"
    # "The first step in fingerprint collection is to add a scalebar beside our evidence. Click on the scalebar.\n\n>>hit space to continue"
    #hide screen move_on
    call screen expand_tools

label scalebar:
    scene table_fingerprint_zoomed
    $ default_mouse = "scalebar_resized"
    $ toolbox_show = False
    $ tools['lifting_tape'] = True
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_table
    #show screen move_on
    # "This is the scalebar.\n\n\n>>hit space to continue"
    # "The scalebar helps to indicate the relative size of the evidence which will become helpful in later stages.\n\n>>hit space to continue"
    # "Click on a surface next to the fingerprint to affix the scalebar. Make sure not to obscure the evidence.\n\n>>hit space to continue"
    call screen scalebar_table


label finished_scalebar:
    $ default_mouse = ''
    $ tools['scalebar'] = False
    scene scalebar_taped
    hide screen scalebar_table
    show screen toolbox
    show screen expand_tools
    #show screen move_on
    show screen evidence_marker_table
    # "Now we have to lift the fingerprint and document it on a backing card.\n\n\n>>hit space to continue"
    # "Let's click on the lifting tape and the backing card.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen expand_tools

label lifting_tape:
    scene table_scalebar_taped_zoomed
    $ default_mouse = "lifting_tape"
    $ toolbox_show = False
    $ tools['bag'] = True
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_table
    #show screen move_on
    # "This is the lifting tape.\n\n\n>>hit space to continue"
    # "The tape is used to lift both the fingerprint and the  scalebar at once.\n\n\n>>hit space to continue"
    # "Once lifted, we want to stick it onto a backing card for documentation purposes.\n\n>>hit space to continue"
    # "Click on the fingerprint to lift.\n\n\n>>hit space to continue"
    call screen lifting_tape_table

label lifting_to_backing:
    scene scalebar_lifting_taped
    $ default_mouse = ''
    # "Now we have to lift and stick the tape onto a backing card.\n\n\n>>hit space to continue"
    # "Click the tape to lift it.\n\n\n>>hit space to continue"
    call screen backing_card_table('lift')

label drag_tape:
    $ default_mouse = 'tape_print_scalebar'
    call screen backing_card_table('drag')

label stick_backing:
    $ default_mouse = ''
    show screen backing_card_table('stick')
    # "Great! You have successfully lifted the tape onto the backing card.\n\n\n>>hit space to continue"
    # "Don't forget to fill out the information on the front and add the letter R to indicate directionality!\n\n>>hit space to continue"
    call screen backing_card_table('complete_front')

label finish_lifting_tape:
    $ default_mouse = ''
    $ tools['lifting_tape'] = False
    scene table
    hide screen lifting_tape_table
    show screen toolbox
    show screen expand_tools
    show screen evidence_marker_table
    #show screen move_on
    "With your evidence collected, now we have to package it.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen expand_tools

label evidence_bags:
    $ default_mouse = 'evidence_bags'
    $ toolbox_show = False
    scene table
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_table
    #show screen move_on
    scene table_evidence_bags
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
    scene table
    hide screen current_evidence
    show screen toolbox
    show screen expand_tools
    show screen evidence_marker_table
    #show screen move_on
    #scene stove_fingerprint
    "Lastly, let's secure the bag to prevent tampering of any kind.\n\n\n>>hit space to continue"
    "Click on the tamper evidence tape.\n\n\n>>hit space to continue"
    #hide screen move_on
    #"Congratulations! You have now finished evidence collection for this stage."
    #$ finish_collection = True
    call screen expand_tools

label tamper_tape:
    $ default_mouse = 'tape'
    $ toolbox_show = False
    $ tools['tape'] = False
    scene seal_evidence_bags
    hide screen toolbox
    hide screen expand_tools
    hide screen evidence_marker_stove
    #show screen move_on
    show screen tamper_evident_tape_table(False)
    "Click on the evidence bag to seal it.\n\n\n>>hit space to continue"
    #hide screen move_on
    call screen tamper_evident_tape_table(True)


label  tutorial_finished:
    $ default_mouse = ''
    $ tools['bag'] = False
    scene table
    hide screen current_evidence
    show screen toolbox
    show screen expand_tools
    #show screen move_on
    if not finish_tutorial:
        show screen evidence_marker_table
        "With the evidence collected, we can now remove our evidence marker.\n\n\n>>hit space to continue"
        $ finish_tutorial = True
    hide screen evidence_marker_table
    "Congratulations! You have now finished evidence collection for this stage.\n\n\n>>hit space to continue"
    $ finish_collection = True
    # call screen evidence_to_lab

label enter_lab:
    hide screen table_center
    hide screen move_on_lab
    hide screen toolbox
    hide screen expand_tools
    #hide screen move_on
    scene entering_lab_screen
    with Dissolve(.8)
    call screen temporary_pause

