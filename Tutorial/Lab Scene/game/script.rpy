default show_evidence = False
default show_instruments = False
default show_toolbox = False
default show_case_files = False

default current_inventory_page =1

default instruments = {'altFTIR': False, 'FTIR': False, 'GCMS': False, 'MS': False}
default evidence_process_select = {'firearm': False, 'firearm_fingerprint': False, 'backing_card': False}
default category= 'Inorganic Analysis'
default hang_evidence = False
default cyanoacrylate_in_progress = False
default cyanoacrylate_finish = False
default cyanoacrylate_picture = False

default evidence_process_tool = {'firearm': ['cyanoacrylate'], 'backing_card': ['AFIS'], 'firearm_fingerprint': ['AFIS']}
default evidence_complete_process = {'firearm': False, 'firearm_fingerprint': False, 'backing_card': False}

default current_cursor = ''
default current_evidence = ''

default materials_tutorial = False
default wrong_action = False


default case_file_dict = {'firearm': False, 'stovetop': False}
default current_casefile = {'evidence': False, 'digi_evidence': False, 'report': False}
default casefile_title = {'evidence': 'Physical Evidence', 'digi_evidence': 'Digital Evidence', 'report': 'Report'}

default bool_show_case = False
default bool_show_case_evidence = False
default bool_show_case_digi = False
default bool_show_case_report = False
default case_type_selected = ''

default current_process = ''

init python:
    def next_page():
        global current_inventory_page
        if current_inventory_page < 4:
            current_inventory_page += 1
    def previous_page():
        global current_inventory_page
        if current_inventory_page > 1:
            current_inventory_page -= 1
        
    def set_instruments_false(exclude_ins):
        global instruments
        for ins in instruments:
            if ins!=exclude_ins:
                instruments[ins] = False
    def set_evidence_select(exclude_e):
        global evidence_process_select
        for e in evidence_process_select:
            if e!=exclude_e:
                evidence_process_select[e] = False
        evidence_process_select[exclude_e] = True

        
    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def set_current_evidence(evidence):
        global current_evidence
        current_evidence = evidence

    def set_state_to_processed(evidence):
        global evidence_complete_process
        evidence_complete_process[evidence] = True

    def set_current_casefile(type_case):
        global current_casefile
        global case_type_selected
        for case in current_casefile:
            if case == type_case:
                current_casefile[case] = True
                case_type_selected = casefile_title[case]
            else:
                current_casefile[case] = False



# The game starts here.

image afis_animated_no_match:
    # "AFIS_analysis.png"
    # pause 0.6
    # "AFIS_analysis1.png"
    # pause 0.6
    # "AFIS_analysis2.png"
    # pause 0.6
    # "AFIS_analysis3.png"
    # pause 0.6
    # "AFIS_analysis_progress1.png"
    # pause 0.6
    # "AFIS_analysis_progress2.png"
    # pause 0.6
    # "AFIS_analysis_progress3.png"
    # pause 0.6
    # "AFIS_analysis_fail.png"
    # pause 0.6
    "afis1"
    pause 0.8
    "afis2"
    pause 0.8
    "afis3"
    pause 0.8
    "afis4"
    pause 0.8
    "no_match_afis"
    pause 0.8

image afis_animated_match:
    # "AFIS_analysis.png"
    # pause 0.6
    # "AFIS_analysis1.png"
    # pause 0.6
    # "AFIS_analysis2.png"
    # pause 0.6
    # "AFIS_analysis3.png"
    # pause 0.6
    # "AFIS_analysis_progress1.png"
    # pause 0.6
    # "AFIS_analysis_progress2.png"
    # pause 0.6
    # "AFIS_analysis_progress3.png"
    # pause 0.6
    # "AFIS_analysis_success.png"
    # pause 0.6
    "afis1"
    pause 0.8
    "afis2"
    pause 0.8
    "afis3"
    pause 0.8
    "afis4"
    pause 0.8
    "match_afis"
    pause 0.8


label start:
    scene entering_lab_screen
    with Dissolve(1.5)

# initial interactions
label hallway_intro:
    #show screen evidence_button_screen('') onlayer over_screens
    show screen instruments_button_screen onlayer over_screens
    show screen toolbox_button_screen onlayer over_screens  
    show screen case_files_screen onlayer over_screens    
    scene lab_hallway_idle
    
    with Dissolve(.8)
    "Welcome to the lab!"
    "This is where you will spend time analyzing the evidence you have collected."
    "The icons on the left allow you to view the evidence, instruments, and items in the toolbox respectively."
    #scene lab_hallway_dim
    show screen hallway_screen(active=False)
    "On the left we have the data analysis lab, and on the right we have the materials lab."
    "As part of the tutorial, let's head into the {color=#cc6600}materials lab{/color} to process latent fingerprints first."
    scene lab_hallway_idle
    with Dissolve(.5)
    call screen hallway_screen(active=True)

##

label hallway:
    scene lab_hallway_idle
    with Dissolve(.8)
    $ show_evidence = False
    $ show_instruments = False
    $ show_toolbox = False
    $ current_process = ''
    if wrong_action:
        call screen wrong_action_screen
    call screen hallway_screen(active=True)

label case_file_display:
    $ bool_show_case = True
    if case_file_dict['firearm']:
        $ text = 'Firearm'
    elif case_file_dict['stovetop']:
        $ text = "Stovetop Fingerprint"
    call screen show_case(text) onlayer over_screens  

    if current_casefile['evidence']:
        $ bool_show_case_type = True
        call screen show_case_evidence(current_process) onlayer over_screens  

label data_analysis_lab:
    scene afis_workstation_idle
    with Dissolve(.8)
    #show screen evidence_button_screen('AFIS') onlayer over_screens
    show screen instruments_button_screen onlayer over_screens
    show screen toolbox_button_screen onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    show screen case_files_screen onlayer over_screens  
    $ current_process = 'AFIS'
    "This is the AFIS workstation."
    "AFIS allows you to match fingerprints against a database of known and unknown prints."
    "Pick the fingerprint backing card from our evidence collection to run it on AFIS."
    call screen data_analysis_lab_screen
    show afis_animated_no_match
    pause 5
    # scene afis_processing
    # with Dissolve(1.5)
    # scene afis_processed
    # with Dissolve(1.5)
    "You have processed the fingerprint."
    "It seems like there is no match found."
    scene dim_afis
    show screen caution_screen
    "Check out the notification!" 
    "It seems like the latent fingerprint from the fuming chamber has finished processing."
    $ cyanoacrylate_finish = True
    "Let's go check it out!"
    jump hallway

label materials_lab:
    if not materials_tutorial:
        scene materials_lab
        with Dissolve(.8)
        #show screen evidence_button_screen('') onlayer over_screens
        show screen instruments_button_screen onlayer over_screens
        show screen toolbox_button_screen onlayer over_screens
        show screen case_files_screen onlayer over_screens  
        
        "This is the materials lab." 
        "Here is where you get to analyze your evidence using chemical methods."
        "We want to develop the latent fingerprints on the evidence gun.\nLet's click on the fingerprint development button."
        $ materials_tutorial = True

label materials_lab_tools: 
    show screen back_button_screen('hallway') onlayer over_screens
    scene materials_lab_dim
    with Dissolve(.5)
    call screen materials_lab_screen

label cyano_machine:
    if not (cyanoacrylate_in_progress or cyanoacrylate_finish):
        show screen back_button_screen('materials_lab_tools') onlayer over_screens
        scene fingerprint_development_bg
        with Dissolve(.7)
        "This is the cyanoacrylate chamber."
        "The chamber helps to develop and process latent fingerprints found on evidentiary items."
        show screen cyano_screen
        $ current_process = 'cyanoacrylate'
        #show screen evidence_button_screen('cyanoacrylate')onlayer over_screens
        show screen case_files_screen onlayer over_screens 
        "Let's start the process by opening the chamber."
        call screen cyano_screen
         
        show screen cyano_process_screen
        "Now, let's hang the appropriate evidence in the chamber using the clips."
        "Take a look at our existing evidence, using the {color=#cc6600}case file{/color} icon on the top left, and pick the appropriate evidence to process."
        call screen cyano_process_screen
        scene cyano_hang_evidence
        "Great! You've identified the correct piece of evidence to analyze."
        "Now, we have to put {color=#cc6600}superglue{/color}  in the left chamber and fill the right reservoir with {color=#cc6600}water{/color} to start the process."
        "You can find these materials by clicking the toolbox icon."
        call screen cyano_process_screen
        jump close_cyano_machine
    elif cyanoacrylate_finish:
        show screen cyano_finish_screen
        "The latent fingerprints have been processed."
        "Now, we have to take a picture of it and upload it to AFIS."
        "Use the camera in the toolbox to help you."
        call screen cyano_finish_screen
        hide screen caution_screen
        scene cyano_hang_evidence
        $ cyanocrylate_picture = True
        "Great job!"
        "Now we can return to the data analysis lab to analyze the result of this fingerprint."
        $ set_cursor('')
        $ show_toolbox = False
        jump materials_lab_tools

    else:
        show screen back_button_screen('materials_lab_tools') onlayer over_screens
        call screen cyano_in_progress_screen


label close_cyano_machine:
    scene cyano_close
    "The chamber is now ready to begin the fumigation process."
    scene cyano_close_dim
    call screen cyano_start_screen
    scene cyano_in_process
    with Dissolve(.7)
    "The fumigation process has begun."
    "We will come back in 15 minutes once it is finished."
    $ cyanoacrylate_in_progress = True
    "In the meantime, let's go to the data analysis lab to process the fingerprint we collected from the crime scene."
    jump hallway

label wet_lab:
    scene fumehood_bg
    with Dissolve(.7)
    call screen wet_lab_screen

label analytical_instruments:
    show screen back_button_screen('materials_lab_tools') onlayer over_screens
    scene analytical_instruments_bg
    with Dissolve(.7)
    call screen instrument_dropdown_screen 
    call screen analytical_instruments_screen

label process_firearm_fingerprint:
    scene afis_workstation_idle
    $ current_process = 'AFIS'
    with Dissolve(.8)
    "Let's process the newly developed fingerprints on our database."
    call screen data_analysis_lab_screen
    show afis_animated_match
    pause 5.5
    "There's a match!"
    show screen show_match
    $ cyanoacrylate_finish = True
    "There is a 80\% match between the fingerprints we collected on the stove up and the firearm."
    "This knowledge will be helpful later in your testimony."
    jump end_lab_tutorial

label wrong_action:
    scene afis_workstation_idle
    "Oops... you're not supposed to be here yet!"
    jump hallway
 
label end_lab_tutorial:
    scene lab_hallway_idle
    hide screen show_match
    "Congratulations! You have finished the lab scene part of the tutorial."
    "Let's head on over to the court room."
    scene enter_courtroom_screen 
    with Dissolve(1.2)



    return
