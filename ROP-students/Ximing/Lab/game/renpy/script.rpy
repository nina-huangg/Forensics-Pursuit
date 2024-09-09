init python:
    visited = {'sample1': False, 'sample2': False, 'sample3': False, 'sample4': False, 'sample5': False, 'sample6': False}
    radiograph_checked = {'sample1': False, 'sample2': False, 'sample3': False, 'sample4': False, 'sample5': False, 'sample6': False}
    
    def return_mouse_pos():
        return renpy.get_mouse_pos()

define instruction_text = False

label start:
    scene entering_lab_screen
    with Dissolve(1.5)

label hallway_intro:
    scene lab_hallway_idle
    with Dissolve(.8)
    "Welcome to the lab!"
    "This is where you will spend time analyzing the evidence you have collected."
    "When you were examine the bathroom, another officer found six samples outside."
    "Now you are in charge to examine them in the bone lab."
    # "The icons on the left allow you to view the evidence, instruments, and items in the toolbox respectively."

    show screen hallway_screen
    "On the left we have the DNA analysis lab, and on the right we have the bone lab."
    scene lab_hallway_idle
    with Dissolve(.5)

label hallway:
    call screen hallway_screen()

label enter_DNA_lab:
    scene DNA_lab
    show screen back_button_screen('hallway')
    "Not done yet."

label enter_bone_lab:
    scene bone_lab_idle
    # "This is the bone lab. Firstly, we need to determine whether the discovered samples are bone or not."
    call screen bone_lab
  

label investigate_bone:
    hide screen hallway_screen
    scene filled_tray
    "First, we need to determine whether the six samples discovered are bones."
    "Fortunately, your coworkers have completed the radiograph, and you can click on the desktop icon to view the results."
    "After reviewing the radiograph, a stereomicroscope icon will appear. Click on it to further examine the sample!"
    call screen choose_piece
    
label first_sample:
    $ visited['sample1'] = True
    $ all_samples_visited = all(visited[sample] for sample in ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
    if all_samples_visited:
        "Congrats! You’ve now examined all six samples. Click on the checkmark to proceed."
        call screen samples('sample_1', 'show', radiograph_checked['sample1'])
    call screen samples('sample_1', 'no', radiograph_checked['sample1'])
    
label sample_2:
    # $ visited['sample2'] = True
    $ all_samples_visited = all(visited[sample] for sample in ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
    if all_samples_visited:
        "Congrats! You’ve now examined all six samples. Click on the checkmark to proceed."
        call screen samples('sample_2', 'show', radiograph_checked['sample2'])
    call screen samples('sample_2', 'no', radiograph_checked['sample2'])
    

label sample_3:
    # $ visited['sample3'] = True
    $ all_samples_visited = all(visited[sample] for sample in ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
    if all_samples_visited:
        "Congrats! You’ve now examined all six samples. Click on the checkmark to proceed."
        call screen samples('sample_3', 'show', radiograph_checked['sample3'])
    call screen samples('sample_3', 'no', radiograph_checked['sample3'])

label sample_4:
    # $ visited['sample4'] = True
    $ all_samples_visited = all(visited[sample] for sample in ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
    if all_samples_visited:
        "Congrats! You’ve now examined all six samples. Click on the checkmark to proceed."
        call screen samples('sample_4', 'show', radiograph_checked['sample4'])
    call screen samples('sample_4', 'no', radiograph_checked['sample4'])

label sample_5:
    # $ visited['sample5'] = True
    $ all_samples_visited = all(visited[sample] for sample in ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
    if all_samples_visited:
        "Congrats! You’ve now examined all six samples. Click on the checkmark to proceed."
        call screen samples('sample_5', 'show', radiograph_checked['sample5'])
    call screen samples('sample_5', 'no', radiograph_checked['sample5'])

label sample_6:
    # $ visited['sample6'] = True
    $ all_samples_visited = all(visited[sample] for sample in ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
    if all_samples_visited:
        "Congrats! You’ve now examined all six samples. Click on the checkmark to proceed."
        call screen samples('sample_6', 'show', radiograph_checked['sample6'])
    call screen samples('sample_6', 'no', radiograph_checked['sample6'])


label wood_stereo1:
    scene wood_stereo1
    call screen dark_overlay_with_mouse()

label wood_stereo2:
    scene wood_stereo2
    call screen dark_overlay_with_mouse()

label bone2_stereo1:
    scene bone2_stereo1
    call screen dark_overlay_with_mouse()

label bone2_stereo2:
    scene bone2_stereo2
    call screen dark_overlay_with_mouse()

label stone_stereo1:
    scene stone_stereo1
    call screen dark_overlay_with_mouse()

label stone_stereo2:
    scene stone_stereo2
    call screen dark_overlay_with_mouse()

label stone_stereo3:
    scene stone_stereo3
    call screen dark_overlay_with_mouse()

label bone3_stereo1:
    scene bone3_stereo1
    call screen dark_overlay_with_mouse()

label bone3_stereo2:
    scene bone3_stereo2
    call screen dark_overlay_with_mouse()

label metal_stereo1:
    scene metal_stereo1
    call screen dark_overlay_with_mouse()
  
label metal_stereo2:
    scene metal_stereo2
    call screen dark_overlay_with_mouse()

label metal_stereo3:
    scene metal_stereo3
    call screen dark_overlay_with_mouse()  

label microscope2:
    scene wood_hover
    if not instruction_text:
        $ instruction_text = True
        "You can click on the eye symbol to see what the sample looks like under the stereomicroscope."
        "Once you are ready, click the test button to determine whether this sample is bone or not."
    call screen microscope('sample_2')
  
label microscope3:
    scene bone2_hover
    if not instruction_text:
        $ instruction_text = True
        "You can click on the eye symbol to see what the sample looks like under the stereomicroscope. 
        Once finished, click on the back button at the bottom to go back."
        "When you are ready, click the test button to determine whether this sample is bone or not."
    call screen microscope('sample_3') 

label microscope4:
    scene stone_hover
    if not instruction_text:
        $ instruction_text = True
        "You can click on the eye symbol to see what the sample looks like under the stereomicroscope."
        "Once you are ready, click the test button to determine whether this sample is bone or not."
    call screen microscope('sample_4')

label microscope5:
    scene bone3_hover
    if not instruction_text:
        $ instruction_text = True
        "You can click on the eye symbol to see what the sample looks like under the stereomicroscope."
        "Once you are ready, click the test button to determine whether this sample is bone or not."
    call screen microscope('sample_5')

label microscope6:
    scene metal_hover
    if not instruction_text:
        $ instruction_text = True
        "You can click on the eye symbol to see what the sample looks like under the stereomicroscope."
        "Once you are ready, click the test button to determine whether this sample is bone or not."
        "You need to do the same for all six samples to advance to the next part. "
    call screen microscope('sample_6')

label test_2:
    $ visited['sample2'] = True
    scene wood_hover
    menu:
        "Choose the correct option."
        "Bone":
            $ x = 1;
        "Not Bone":
            $ x = 2;
    if x == 1:
        "F"
    else:
        "T"
    jump sample_2

label test_3:
    $ visited['sample3'] = True
    scene bone2_hover
    menu:
        "Choose the correct option."
        "Bone":
            $ x = 1;
        "Not Bone":
            $ x = 2;
    if x == 1:
        "T"
    else:
        "F"
    jump sample_3

label test_4:
    $ visited['sample4'] = True
    scene stone_hover
    menu:
        "Choose the correct option."
        "Bone":
            $ x = 1;
        "Not Bone":
            $ x = 2;
    if x == 1:
        "F"
    else:
        "T"
    jump sample_4

label test_5:
    $ visited['sample5'] = True
    scene bone3_hover
    menu:
        "Choose the correct option."
        "Bone":
            $ x = 1;
        "Not Bone":
            $ x = 2;
    if x == 1:
        "T"
    else:
        "F"
    jump sample_5

label test_6:
    $ visited['sample6'] = True
    scene metal_hover
    menu:
        "Choose the correct option based on the radiograph."
        "Bone":
            $ x = 1;
        "Not Bone":
            $ x = 2;
    if x == 1:
        "F"
    else:
        "T"
    jump sample_6

label result_1:
    scene bone1_radiograph
    $ radiograph_checked['sample1'] = True
    # menu:
    #     "Choose the correct option based on the radiograph."
    #     "Bone":
    #         $ x = 1;
    #     "Not Bone":
    #         $ x = 2;
    # if x == 1:
    #     "T"
    # else:
    #     "F"
    call screen result_finish('sample_1')

label result_2:
    scene wood_radiograph
    $ radiograph_checked['sample2'] = True
    call screen result_finish('sample_2')

label result_3:
    scene bone2_radiograph
    $ radiograph_checked['sample3'] = True
    call screen result_finish('sample_3')

label result_4:
    scene stone_radiograph
    $ radiograph_checked['sample4'] = True
    call screen result_finish('sample_4')

label result_5:
    scene bone3_radiograph
    $ radiograph_checked['sample5'] = True
    call screen result_finish('sample_5')

label result_6:
    scene metal_radiograph
    $ radiograph_checked['sample6'] = True
    call screen result_finish('sample_6')

label finish_first_stage_bone:
    scene bone_lab_idle
    "Now that you have identified the bone samples, you need to determine whether they belong to human or not."
    "We'll test your knowledge of the differences between human and non-human skeletal features through a series of multiple-choice questions."
    menu:
        "Q: Compared to most other mammalian species, the foramen magnum on a human skull is located ___."
        "Posteriorly":
            $ x = 1;
        "Superiorly":
            $ x = 2;
        "Anteriorly":
            $ x = 3;
        "Laterally":
            $ x = 4;
    if x == 1:
        "F"
    elif x == 2:
        "F"
    elif x ==3:
        "T"
    else:
        "F"

    menu:
        "Q: The canines in a human’s dentition are relatively small and will lack ___."
        "Diastema":
            $ y = 1;
        "Carnassia":
            $ y = 2;
        "Prognathia":
            $ y = 3;
        "Symphysis":
            $ y = 4;
    if y == 1:
        "T"
    elif y == 2:
        "F"
    elif y ==3:
        "F"
    else:
        "F"
    
    menu:
        "Q: The costal groove is ___ in humans."
        "Entirely absent":
            $ y = 1;
        "Well-pronounced and found inferiorly":
            $ y = 2;
        "Weakly defined and found superiorly":
            $ y = 3;
        "Well-pronounced and found superiorly":
            $ y = 4;
    if y == 1:
        "F"
    elif y == 2:
        "T"
    elif y ==3:
        "F"
    else:
        "F"





   

return
