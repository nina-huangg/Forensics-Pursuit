default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default default_mouse = None
define flash = Fade(0.1, 0.0, 0.5, color="#fff")
### entries on afis when search
default afis_search = []
default afis_bg = "software_interface"
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]
default interface_import = False
default interface_imported = False
default interface_search = False
default afis_image_idx = 0
default afis_images = ["blank", "print_1", "print_2", "print_3", "print_4", "print_5", "print_6", "print_7"]
default dna_image_idx = 0
default dna_images = ["blank", "dna_1", "dna_2", "dna_3", "dna_4", "dna_5", "dna_6", "dna_7"]


default case_files = ["bottle", "vase", "swab_from_wall"]

default default_tools = ["default"]
default fingerprint_tools = ["bottle_fingerprint", "uv_light", "duster", "scalebar", "lifting_tape", "backing_card"]
default ca_tools = ["vase_ca", "swab", "glue", "water"]
default headspace_tools = ["bottle_headspace", "pipette"]
default wet_lab_tools = ["vase_wet_lab", "spray", "scalebar", "camera"]

# default current_evidence = ""
default current_lab = ""

default process = ["vase_ca_fuming", "bottle_fingerprint", "bottle_headspace", "swab_vase", "vial_gc", "vase_wet_lab", "swab_wall"]

default steps = {"bottle_fingerprint": 1, "vase_ca": 1, "bottle_headspace": 1, "vase_wet_lab":1}

transform shrink:
    anchor (0.5, 0.5)
    xalign 0.5
    yalign 0.4
    linear 2.0 xzoom 0.9 yzoom 0.9

transform vase_swab:
    xalign 0.5
    yalign 0.4
    zoom 0.275

transform drop_box:
    xalign 0.48 yalign 0.4
    zoom 0.25

init python:
    import random
    global interface_import 
    global interface_imported 
    global interface_search
    global afis_bg
    global afis_image_idx 

    # global current_evidence 
    global user_step
    user_step = 0

    def function_restart_interaction():
        renpy.restart_interaction()
    
    def set_image_idx(software, direction):
        global afis_image_idx, dna_image_idx
        if software == 'afis':
            if direction == 'next':
                afis_image_idx = (afis_image_idx + 1) %  6
            else:
                afis_image_idx = (afis_image_idx - 1) % 6
        else:
            if direction == 'next':
                dna_image_idx = (dna_image_idx + 1) %  6
            else:
                dna_image_idx = (dna_image_idx - 1) % 6
        renpy.restart_interaction()
    
    def compare_evidence(evidence):
        global current_evidence
        if current_lab == 'dna':
            if not interface_imported or evidence.name == 'bottle_fingerprint' or evidence.name == 'vase_fingerprint':
                renpy.show_screen('error_score_screen')
            elif evidence.name == 'dna_vase' and dna_images[dna_image_idx] == 'dna_1':
                renpy.show_screen("correct_screen", f"The DNA profiles are 100% consistent. Additionally the DNA belongs to John Doe. This is the victim.")
            elif evidence.name == 'dna_wall' and dna_images[dna_image_idx] == 'dna_2':
                renpy.show_screen("correct_screen", f"The DNA profiles are 100% consistent. Additionally the DNA belongs to John Doe. This is the victim.")
            else:
                renpy.show_screen("dna_score_screen", random.randint(dna_image_idx*10, dna_image_idx*10+5))
        else:
            if not interface_imported or evidence.name == 'dna_wall' or evidence.name == 'dna_vase':
                renpy.show_screen('error_score_screen')
            elif evidence.name == 'vase_fingerprint' and afis_images[afis_image_idx] == 'print_1':
                renpy.show_screen("correct_screen", f"The fingerprints are 100% consistent. Additionally the fingerprint belongs to Alex Parker.")
            elif evidence.name == 'bottle_fingerprint' and afis_images[afis_image_idx] == 'print_2':
                renpy.show_screen("correct_screen", f"The fingerprints are 100% consistent. Additionally the fingerprint belongs to Jordan Taylor.")
            else:
                renpy.show_screen("fingerprint_score_screen", random.randint(afis_image_idx*10, afis_image_idx*10+5))


    def check_valid_evidence(evidence, lab):
        global interface_import, interface_imported, interface_search, afis_bg, afis_image_idx, current_evidence
        if lab == "afis" or lab == 'dna':
            found = False
            for e in afis_evidence:
                if evidence == e.name:
                    current_evidence = e 
                    found = True
                    interface_imported = False
                    interface_search = False 
                    afis_bg = 'software_interface'
                    interface_import = True
                    if evidence == 'dna_wall':
                        set_cursor('dna_wall')
                    elif evidence == 'dna_vase':
                        set_cursor('dna_vase')
                    elif evidence == 'vase_fingerprint':
                        set_cursor('vase_fingerprint')
                    elif evidence == 'bottle_fingerprint':
                        set_cursor('bottle_fingerprint')
                    renpy.restart_interaction()
            
            # if found:
            #         renpy.show_screen("afis_screen")
            if not found:
                renpy.show_screen("invalid_evidence_screen")

        elif evidence in case_files:
            if evidence == "bottle" and lab == "lab_bench":
                if "bottle_fingerprint" in process:
                    process.remove("bottle_fingerprint")
                    if "bottle_headspace" not in process:
                        case_files.remove("bottle")
                    renpy.restart_interaction()
                    renpy.jump("bottle_fingerprint_start")
                else:
                    renpy.show_screen("processed_evidence_screen")
            elif evidence == "bottle" and lab == "lab_headspace":
                if "bottle_headspace" in process:
                    process.remove("bottle_headspace")
                    if "bottle_fingerprint" not in process:
                        case_files.remove("bottle")
                    renpy.restart_interaction()
                    renpy.jump("bottle_headspace_start")
                else:
                    renpy.show_screen("processed_evidence_screen")

            elif evidence == "vase" and lab == "ca_fuming":
                if "vase_ca_fuming" in process:
                    process.remove("vase_ca_fuming")
                    case_files.remove("vase")
                    renpy.restart_interaction()
                    renpy.jump("vase_add_to_ca")
                else:
                    renpy.show_screen("processed_evidence_screen")
            
            elif evidence == "vase_processed" and lab == "wet_lab":
                if "vase_wet_lab" in process:
                    process.remove("vase_wet_lab")
                    case_files.remove("vase_processed")
                    renpy.restart_interaction()
                    renpy.jump("vase_wet_lab_spray")
                else:
                    renpy.show_screen("processed_evidence_screen")

            elif evidence == 'vial' and lab == "lab_headspace":
                if "vial_gc" in process:
                    process.remove("vial_gc")
                    case_files.remove("vial")
                    renpy.restart_interaction()
                    renpy.jump("put_vial_in_gc")
                else:
                    renpy.show_screen("processed_evidence_screen")
            
            elif evidence == 'swab_from_vase' and lab == 'bio_lab':
                if 'swab_vase' in process:
                    # process.remove('swab_vase')
                    # case_files.remove('swab_from_vase')
                    set_cursor('swab_from_vase')
                    renpy.restart_interaction()
                    renpy.jump('bio_lab')
                else:
                    renpy.show_screen("processed_evidence_screen")
            
            elif evidence == 'swab_from_wall' and lab == 'bio_lab':
                if 'swab_wall' in process:
                    # process.remove('swab_wall')
                    # case_files.remove('swab_from_wall')
                    set_cursor('swab_from_wall')
                    renpy.restart_interaction()
                    renpy.jump('bio_lab')
                else:
                    renpy.show_screen("processed_evidence_screen")

            else:
                renpy.show_screen("invalid_evidence_screen")
            
 
    def dragged_func(dragged_items, dropped_on):
        if dropped_on is not None:
            if dragged_items[0].drag_name == "tape" and dropped_on.drag_name == "backing_card":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.jump("bottle_fingerprint_complete")

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)

    
    class Evidence:
        def __init__(self, name, afis_details):
            self.name = name
            self.afis_details = afis_details
            self.processed = False
         
    def set_evidence(name):
        for evidence in afis_evidence:
            if evidence.name == name:
                current_evidence = evidence 
    
    ### declare each piece of evidence
    
    dna_wall = Evidence(name = 'dna_wall',
                                afis_details = {
                                    'image': '/images/data_analysis_lab/dna_wall.png',
                                    'xpos': 0.18, 'ypos': 0.3,
                                    'score': '70'
                                })
    dna_vase = Evidence(name = 'dna_vase',
                                afis_details = {
                                    'image': '/images/data_analysis_lab/dna_vase.png',
                                    'xpos': 0.18, 'ypos': 0.3,
                                    'score': '70'
                                })
    bottle_fingerprint = Evidence(name = 'bottle_fingerprint',
                                afis_details = {
                                    'image': '/images/data_analysis_lab/bottle_fingerprint.png',
                                    'xpos': 0.18, 'ypos': 0.3,
                                    'score': '70'
                                })
    vase_fingerprint = Evidence(name = 'vase_fingerprint',
                                afis_details = {
                                    'image': '/images/data_analysis_lab/vase_fingerprint.png',
                                    'xpos': 0.18, 'ypos': 0.3,
                                    'score': '70'
                                })
    ### declare afis relevant evidence
    afis_evidence = [dna_wall, dna_vase, vase_fingerprint, bottle_fingerprint]

    ### set current_evidence to track which evidence is currently active
    current_evidence = dna_wall
    
    
    config.mouse = {
        "uv_light": [('/images/mouse/uv_light_resized.png', 0, 0)],
        "scalebar": [('/images/mouse/scalebar_resized.png', 0, 0)],
        "lifting_tape": [('/images/mouse/lifting_tape_resized.webp', 0, 0)],
        "duster": [('/images/mouse/magnetic_powder_resized.png', 0, 0)],

        "glue": [('/images/mouse/glue_resized.png', 0, 0)],
        "water": [('/images/mouse/water_resized.png', 0, 0)],

        "pipette": [('/images/mouse/pipette_resized.png', 60, 60)],
        "pipette_full": [('/images/mouse/pipette_full_resized.png', 60, 60)],

        "vial": [('/images/mouse/vial_resized.png', 10, 10)],
        "vase": [('/images/mouse/vase_resized.png', 40, 20)],
        "spray": [('/images/mouse/spray_resized.png', 40, 20)],

        "swab": [('/images/mouse/swab_resized.png', 0, 50)],
        "swab_from_wall": [('/images/mouse/swab_from_wall_resized.png', 20, 20)],
        "swab_from_vase": [('/images/mouse/swab_from_vase_resized.png', 20, 20)],

        "dna_wall": [('/images/mouse/dna_wall.png', 20, 20)],
        "dna_vase": [('/images/mouse/dna_vase.png', 20, 20)],
        "vase_fingerprint": [('/images/mouse/vase_fingerprint.png', 20, 20)],
        "bottle_fingerprint": [('/images/mouse/bottle_fingerprint.png', 20, 20)]
    }


#################################### START #############################################
label start:
    scene entering_lab_screen
    with Dissolve(1.5)

label lab_hallway_intro:
    show screen case_files_screen(case_files) onlayer over_screens 
    show screen toolbox_button_screen(default_tools) onlayer over_screens     
    scene lab_hallway_idle
    "Welcome to the lab!"
    "This is where you will spend time analyzing the evidence you have collected."
    "Let's get started!"

label hallway:
    call screen lab_hallway_screen

label data_analysis_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('data_analysis_lab') onlayer over_screens
    $ current_lab = 'afis'
    call screen afis_screen

label dna:
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('data_analysis_lab') onlayer over_screens
    $ current_lab = 'dna'
    call screen dna_screen

label materials_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen


label analytical_instruments:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

label fingerprint_development:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen fingerprint_development_screen



label fingerprint_lab_bench:
    hide screen checkmark_button_screen
    hide screen toolbox_button_screen onlayer over_screens
    show screen back_button_screen('fingerprint_development') onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens 
    scene lab_bench_empty
    $ current_lab = "lab_bench"
    "You are currently at the lab bench where you can dust for fingerprints."
    "Select a peice of evidence that needs dusting to get started."
    window hide 
    $ renpy.pause(hard=True)


label bottle_fingerprint_start:
    hide screen checkmark_button_screen
    hide screen back_button_screen onlayer over_screens
    scene lab_bench_background
    show screen add_bottle_screen
    hide screen case_files_screen onlayer over_screens
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(fingerprint_tools) onlayer over_screens
    "You have selected the alcohol bottle, which needs dusting. Tap on toolbox for additional tools to start fingerprint development."
    jump open_fingerprint_toolbox

label open_fingerprint_toolbox:
    if show_toolbox:
        "Start with the flashlight"
        jump bottle_fingerprint_uv_light
    else:
        "Tap on the toolbox to see additional tools."
        window hide
        jump open_fingerprint_toolbox
    
label bottle_fingerprint_uv_light:
    call screen bottle_uv_light_screen
    $ steps["bottle_fingerprint"] += 1
    hide screen add_bottle_screen
    show screen add_bottle_with_outline_screen
    "You've identified a fingerprint using oblique lighting."
    "A faint outline has been marked so you remember where this is, but this is not actually in the crime scene."
    "Since the surface is dark, we need to use white dusting powder."
    window hide 
    $ renpy.pause(hard=True)

label bottle_fingerprint_duster:
    call screen bottle_duster_screen 
    $ steps["bottle_fingerprint"] += 1 
    hide screen add_bottle_with_outline_screen
    show screen add_bottle_duster
    "The fingerprint has been identified after dusting. Now add a scalebar."
    window hide  
    $ renpy.pause(hard=True)

label bottle_fingerprint_scalebar:
    call screen bottle_scalebar_screen
    $ steps["bottle_fingerprint"] += 1
    hide screen add_bottle_duster
    show screen add_bottle_scalebar
    "Scalebar has been added. Now the fingerprint may be lifted."
    window hide
    $ renpy.pause(hard=True)

label bottle_fingerprint_lifting_tape:
    call screen bottle_lifting_tape_screen 
    hide screen add_bottle_scalebar
    show screen add_bottle_lifting_tape
    "The fingerprint has been lifted. Now put it on a backing card."
    $ steps["bottle_fingerprint"] += 1
    window hide 
    $ renpy.pause(hard=True)

label bottle_fingerprint_backing_card:
    hide screen add_bottle_lifting_tape 
    call screen bottle_backing_card_screen
    window hide 
    $ renpy.pause(hard=True)

label bottle_fingerprint_complete:
    call screen bottle_backing_card_complete_screen
    scene lab_bench_empty
    show screen back_button_screen('fingerprint_development') onlayer over_screens
    hide screen toolbox_button_screen onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    "Great now it is ready to be sent off to the data analysis lab. You may leave this lab."
    $ case_files.append("bottle_fingerprint")
    $ show_toolbox = False
    $ renpy.restart_interaction()
    window hide  
    $ renpy.pause(hard=True)



label fingerprint_ca_fuming:
    show screen back_button_screen('fingerprint_development') onlayer over_screens
    hide screen toolbox_button_screen onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    scene cyanosafe_far_closed
    call screen open_cyanosafe_screen
    window hide 
    $ renpy.pause(hard=True)
    
label vase_ca_opened:
    scene cyanosafe_far_open
    call screen cyanosafe_enter_chamber_screen

label vase_select:
    hide screen back_button_screen onlayer over_screens
    scene cyanosafe_open
    $ current_lab = "ca_fuming"
    "You are currently at a cyanosafe fuming station."
    "Select a peice of evidence that needs fuming to get started."
    window hide
    $ renpy.pause(hard=True)

label vase_add_to_ca:
    scene cyanosafe_with_overlay
    show expression "/cyanosafe/vase_swab.png" at vase_swab
    
    "You have selected the vase, which has blood on it. Since you already did the presumptive test before, this part has been omitted for simplicity, but you may assume the substance on the vase is blood."
    "Get a swab sample of the blood on the vase before proceeding with the Cyanosafe fuming."

    
    hide screen toolbox_button_screen onlayer over_screens
    show screen toolbox_button_screen(ca_tools) onlayer over_screens
    window hide
    $ renpy.pause(hard=True)

label vase_ca_swab:
    hide expression "/cyanosafe/vase_swab.png"
    call screen swab_vase_screen
    $ steps["vase_ca"] += 1
    $ default_mouse = None
    jump vase_ca_swab_added


label vase_ca_swab_added:
    $ case_files.append('swab_from_vase')
    call screen vase_after_swabbed
    scene cyanosafe_open 
    "Now put the vase in the chamber"

    call screen cyanosafe_add_vase_screen
    $ default_mouse = None
    scene cyanosafe_with_vase
    
    "Now open the toolbox and add the supplements needed to run the cyanosafe fuming."
    window hide
    $ renpy.pause(hard=True)

label vase_ca_glue:
    call screen vase_ca_glue_screen
    scene cyanosafe_water_idle
    show screen vase_glue_added_screen
    $ steps["vase_ca"] += 1
    window hide 
    $ renpy.pause(hard=True)

label vase_ca_water:
    call screen vase_ca_water_screen
    scene cyanosafe_done
    call screen vase_water_added_screen
    $ steps["vase_ca"] += 1
    jump vase_ca_close_chamber

label vase_ca_close_chamber:
    $ show_toolbox = False
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    scene cyanosafe_close_chamber_idle 
    "Now close the cyanosafe chamber."
    call screen vase_close_chamber_screen
    jump run_ca_question
    
label run_ca_question:
    scene cyanosafe_far_closed
    menu:
        "Choose a time to leave the cyanosafe fuming"

        "1 minute":
            jump run_ca_incorrect

        "5 minutes":
            jump run_ca_incorrect

        "10 minutes":
            jump run_ca_correct

        "15 minutes":
            jump run_ca_incorrect

label run_ca_incorrect:
    call screen incorrect_time_message
    jump run_ca_question

label run_ca_correct:
    hide screen toolbox_button_screen onlayer over_screens
    hide screen case_files_screen onlayer over_screens
    window hide
    show timer_10_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_10_left
    show timer_5_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_5_left
    show timer_done:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_done
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    show screen case_files_screen(case_files) onlayer over_screens
    call screen get_vase_from_chamber
    scene cyanosafe_with_background
    call screen vase_ca_complete
    hide screen vase_ca_complete
    $ case_files.append('vase_processed')
    show screen back_button_screen('fingerprint_development')
    $ show_toolbox = False
    scene cyanosafe_far_open
    window hide   
    $ renpy.pause(hard=True)



label wet_lab:
    scene fumehood
    hide screen back_button_screen onlayer over_screens
    hide screen toolbox_button_screen onlayer over_screens
    hide screen case_files_screen onlayer over_screens
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    $ current_lab = "wet_lab"
    $ show_toolbox = False
    "You are currently in the wet lab."
    "Select a peice of evidence that needs wet lab processing to get started."
    window hide
    $ renpy.pause(hard=True)

label vase_wet_lab_spray:
    show screen vase_wet_lab_screen
    show screen toolbox_button_screen(wet_lab_tools) onlayer over_screens
    window hide 
    $ renpy.pause(hard=True)

label vase_wet_lab_sprayed:
    scene fumehood_light_idle
    $ default_mouse = None
    hide screen vase_wet_lab_screen
    show screen vase_sprayed_screen onlayer over_screens
    call screen vase_wet_lab_light_screen

label vase_wet_lab_light:
    scene fumehood_with_light

    hide screen vase_sprayed_screen onlayer over_screens
    show screen vase_light_fingerprint 

    "Now add scalebar"
    $ steps["vase_wet_lab"] += 1

    window hide 
    $ renpy.pause(hard=True)

label vase_wet_lab_scalebar:
    scene fumehood_with_light

    call screen vase_wet_lab_scale 
    hide screen vase_light_fingerprint 
    show screen vase_scale_hover_screen

    $ steps["vase_wet_lab"] += 1
    "Now click camera to take a photo"

    window hide
    $ renpy.pause(hard=True)

label vase_wet_lab_camera:
    hide screen vase_scale_hover_screen
    scene fumehood_with_overlay
    show expression "/wet_lab/vase_fingerprint_picture.png" at shrink with flash
    call screen vase_picture_taken
    hide expression "/wet_lab/vase_fingerprint_picture.png"
    scene fumehood_with_vase
    show screen back_button_screen('materials_lab')
    $ case_files.append('vase_fingerprint')
    $ renpy.restart_interaction()

    hide screen toolbox_button_screen onlayer over_screens
    hide screen case_files_screen onlayer over_screens
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    window hide
    $ renpy.pause(hard=True)




label bio_lab:
    scene bio_lab_overlay
    hide screen back_button_screen onlayer over_screens
    $ current_lab = 'bio_lab'
    $ result = renpy.call_screen("drop_box_screen")
    
    if result == "swab_from_vase" and "swab_from_vase" in case_files:
        $ process.remove('swab_vase')
        $ case_files.remove("swab_from_vase")
        $ default_mouse = None
        if "swab_from_vase" not in case_files and "swab_from_wall" not in case_files:
            show expression "/bio_lab/drop_box.png" at drop_box
            call screen text_screen("Send off to the bio lab")
            jump test2
        else:
            jump bio_lab
    elif result == "swab_from_wall" and "swab_from_wall" in case_files:
        $ process.remove('swab_wall')
        $ case_files.remove("swab_from_wall")
        $ default_mouse = None
        if "swab_from_vase" not in case_files and "swab_from_wall" not in case_files:
            show expression "/bio_lab/drop_box.png" at drop_box
            call screen text_screen("Send off to the bio lab")
            jump test2
        else:
            jump bio_lab
    else:
        show screen try_something_else

    show screen back_button_screen('materials_lab')
    window hide
    $ renpy.pause(hard=True)


label test2:
    scene bio_lab
    "Sent off to bio lab. Lets wait a little bit for the results."
    window hide
    show timer_15_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_15_left

    show timer_10_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_10_left

    show timer_5_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_5_left

    show timer_done:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_done
    window hide
    $ case_files.append('dna_wall')
    $ case_files.append('dna_vase')
    $ renpy.restart_interaction()
    show screen back_button_screen('materials_lab') onlayer over_screens
    "We got the dna results and can leave the lab now."
    $ renpy.pause(hard=True)


label headspace_gc:
    hide screen back_button_screen onlayer over_screens
    hide screen toolbox_button_screen onlayer over_screens
    hide screen case_files_screen onlayer over_screens
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    scene gc_background 
    $ current_lab = "lab_headspace"
    $ show_toolbox = False
    "You are currently in front of the headspace GC instrument."
    "Select a peice of evidence that needs chemical processing to get started."
    window hide 
    $ renpy.pause(hard=True)

label bottle_headspace_start:
    scene gc_background_overlay
    show screen bottle_headspace_start_screen
    show screen toolbox_button_screen(headspace_tools) onlayer over_screens
    "Use tools in toolbox to get fluid out."
    window hide 
    $ renpy.pause(hard=True)

label bottle_headspace_pipette:
    hide screen bottle_headspace_start_screen
    call screen bottle_pipette 

label bottle_headspace_jar_full:
    scene gc_background_overlay
    show screen bottle_headspace_jar_complete
    "complete"
    hide screen bottle_headspace_jar_complete
    scene gc_background
    $ default_mouse = None 
    $ case_files.append('vial')
    hide screen toolbox_button_screen onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    $ renpy.restart_interaction()
    "added vial to inventory"
    "get the vial from inventory"
    window hide
    $ renpy.pause(hard=True) 

label put_vial_in_gc:
    $ default_mouse = "vial"
    call screen put_jar_in_gc
    window hide
    $ renpy.pause(hard=True)

label test:
    $ default_mouse = "pipette_full"
    call screen bottle_pipette

label run_gc_questions:
    scene gc_instrument_added_vial
    menu:
        "If we suspect that the bottle contains Diphenhydramine, how long should our retention time be?"

        "5 minute":
            jump run_gc_incorrect

        "10 minutes":
            jump run_gc_10_correct

        "15 minutes":
            jump run_gc_15_correct

        "20 minutes":
            jump run_gc_incorrect

label run_gc_incorrect:
    call screen incorrect_time_message
    jump run_gc_questions

label run_gc_10_correct:
    window hide
    scene gc_spin_1
    show timer_10_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_10_left
    scene gc_spin_2
    show timer_5_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_5_left
    scene gc_spin_3
    show timer_done:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_done
    scene gc_instrument_added_vial
    $ renpy.pause(1.0)
    jump gc_spectograph

label run_gc_15_correct:
    window hide
    scene gc_spin_1
    show timer_15_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_15_left
    scene gc_spin_2
    show timer_10_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_10_left
    scene gc_spin_3
    show timer_5_left:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_5_left
    scene gc_spin_4
    show timer_done:
        xpos 0.45
        ypos 0.4
    $ renpy.pause(1.0)
    hide timer_done
    scene gc_instrument_added_vial
    $ renpy.pause(1.0)
    jump gc_spectograph
    
label gc_spectograph:
    scene gc_spectrograph 
    show screen gc_spectrograph_result_screen
    window hide 
    $ renpy.pause(hard=True)

label gc_complete:
    scene gc_instrument
    "We have identified Diphenhydramine present. We are done with the Gas Chromatography Spectometer, and can leave this lab."
    show screen back_button_screen('analytical_instruments')
    $ show_toolbox = False
    window hide
    $ renpy.pause(hard=True)


# label 


    
    