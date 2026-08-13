init python:
    config.mouse = {
        "default": [("images/ui/cursors/cursor.png", 0, 0)],
        "pointer": [("images/ui/cursors/cursor.png", 0, 0)],
        "magnifying": [("images/ui/cursors/default_cursor.png", 0, 0)],
        "hover": [("images/ui/cursors/hover_cursor.png", 0, 0)],
        "dropper": [("images/ui/cursors/dropper.png", 0, 49)],
        "ethanol": [("images/ui/cursors/dropper_filled.png", 0, 49)],
        "hand": [("images/ui/cursors/default_hand.png", 0, 0)],
        "hand_grab": [("images/ui/cursors/grab_hand.png", 0, 0)],
        "micropipette": [("images/ui/cursors/micropipette.png", 10, 10)]
    }
    
    import json

    tools = load_items("jsons/toolbox.json")

    toolbox.add_to_inventory(tools["Backing Card"])
    toolbox.add_to_inventory(tools["Scalebar"])
    toolbox.add_to_inventory(tools["Tape"])
    toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    toolbox.add_to_inventory(tools["Gel Lifter"])
    toolbox.add_to_inventory(tools["Magnetic Powder"])
    toolbox.add_to_inventory(tools["Druggist Paper"])
    toolbox.add_to_inventory(tools["Evidence Bag"])
    toolbox.add_to_inventory(tools["Envelope"])
    toolbox.add_to_inventory(tools["Roller"])

    evids = load_items("jsons/evidence.json")

    paint_step = 0
    track_step_gel = 0
    track_step_dentalstone = 0

    encountered = {
        "tiretracks": False,
        "paint": False
    }

    analyzing = {
        "tiretracks": False,
        "paint": False
    }

    analyzed = {
        "tiretracks": False,
        "paint": False
    }

    def item_dragging_package(drags):
        """Used to set the mouse cursor to the hand_grab cursor when dragging an item.
        """
        global default_mouse
        default_mouse = "hand_grab"
        return

    def item_dragged_package(drags, drop):
        """Used to set the mouse cursor to the hand_grab cursor when grabbing an item.
        """
        global default_mouse
        default_mouse = "hand_grab"
        
        if not drop:
            default_mouse = "hand"
            return

        # Hide all draggable screens
        renpy.hide_screen("fold_to_bag")
        renpy.hide_screen("bag_to_tape")
        default_mouse = "default"
        return True


define n = Character(name=("Nina"), image="nina")
image bg motorcycle = Transform("motorcycle", xysize=(1920, 1080))

label start:
    scene bg motorcycle
    show nina normal1
    n "Hello detective. I'm Detective Nina."
    n "Late last night, a serious hit and run occurred on this roadway."
    show nina thinknote1
    n "A motorcyclist was struck from behind and left critically injured."
    n "The driver fled the scene before emergency services arrived."
    show nina talk
    n "Our job is to collect and preserve the evidence left behind."
    n "If we're lucky, we'll be able to identify the vehicle that caused the collision."
    show nina normal1
    n "I can already see several pieces of evidence at the scene."
    n "Let's get to work."
    hide nina

    jump game


label game:
    hide screen closeup
    if analyzed["tiretracks"] and analyzed["paint"]:
        show nina normal1
        n "Excellent work, detective."
        n "We've collected all available evidence from the crash scene."
        show nina thinknote1
        n "The lab should be able to analyze` tire impressions and taillight fragments."
        show nina normal1
        n "Let's head back and begin the analysis."
        jump lab_start

    call screen motorcycle


label closeup:

    call screen closeup
    return


##################################################
# tool use labels
##################################################

label backing_card_use_label:
    n "I don't think that tool belongs here."
    jump game

label scalebar_use_label:
    n "You don't need a scale here."
    jump game

label tape_use_label:
    n "I don't think that tool belongs here."
    jump game

label magnetic_powder_use_label:
    n "I don't think that tool belongs here."
    jump game

label druggist_paper_use_label:
    if analyzing["paint"] and paint_step == 0:
        call screen druggist_paper_use
    else:
        n "You don't need that right now."

        jump game

label druggist_paper_correct_choice:
    "You carefully collect the paint chip fragments."

    "The fragments are placed onto a clean sheet of paper and folded."
    $ paint_step += 1
    jump paint

label envelope_use_label:
    if analyzing["paint"] and paint_step == 1:
        
        "You place the folded paint chip fragments into an envelope."
        # $ call screen fold_to_envelope
        $ paint_step += 1
        jump paint

    if analyzing["tiretracks"] and track_step_gel == 3:
        "You place the lifted tire impression into an envelope."
        call screen impression_to_envelope
        $ toolbox.delete_from_inventory(tools["Gel Lifter Cover"])
        $ track_step_gel += 1
        jump tiretracks

    else:
        n "You don't need that right now."
        jump game

label evidence_bag_use_label:
    if analyzing["paint"] and paint_step == 2:

        "You bag the folded paint chips."
        call screen envelope_to_bag
        $ paint_step += 1
        jump paint
    if analyzing["tiretracks"] and track_step_gel == 4:
        
        "You bag the lifted tire impression."
        call screen envelope_to_bag
        $ track_step_gel += 1
        jump tiretracks
    else:
        n "You don't need that right now."
        jump game

label tamper_evident_tape_use_label:
    if analyzing["paint"] and paint_step == 3:

        "You tape the bag with the folded paint chips."
        call screen bag_to_tape
        $ paint_step += 1 # paint step 3
        "Taped bag added to evidence."
        $ analyzed["paint"] = True
        $ analyzing["paint"] = False
        $ evidence.add_to_inventory(evids["Bagged Paint Transfer"])
        jump game

    if analyzing["tiretracks"] and track_step_gel == 5:
        "You tape the bag with the lifted tire impression."
        call screen bag_to_tape
        $ track_step_gel += 1 # track step 5    
        "Taped bag added to evidence."
        $ analyzed["tiretracks"] = True
        $ analyzing["tiretracks"] = False
        $ evidence.add_to_inventory(evids["Bagged Tire Track Impression"])
        jump game
    else:
        n "You don't need that right now."
        jump game

label gel_lifter_use_label:
    if analyzing["tiretracks"] and track_step_gel == 0:
        "You carefully apply the gel lifter to the tire impressions and store the cover."
        $ toolbox.add_to_inventory(tools["Gel Lifter Cover"])
        $ track_step_gel += 1
        jump tiretracks
    else:
        n "You don't need that right now."
        jump game

label roller_use_label:
    if analyzing["tiretracks"] and track_step_gel == 1:
        "You carefully roll the gel lifter over the tire impressions."
        $ track_step_gel += 1
        jump tiretracks
    else:
        n "You don't need that right now."
        jump game

label gel_lifter_cover_use_label:
    if analyzing["tiretracks"] and track_step_gel == 2:
        "You carefully lift the gel lifter cover and store it for later analysis."
        $ track_step_gel += 1
        jump tiretracks
    if analyzing["tiretracks"] and track_step_gel == 1:
        "You need to do something before you can lift the cover..."
        jump tiretracks
    else:
        n "You don't need that right now."
        jump game

label label_use_label:

        n "That won't help here."

        jump game

#######################################################################
#######################################################################

define n = Character(name=("Nina"), image="nina")

default current_cursor = ''
default imported_print = ''
default show_case_files = False
default show_toolbox = False
default location = "bio_station"

default encountered_stereomicroscope = False
default encountered_ftir = False
default exclude_warning_shown = False
default identification_warning_shown = False
default identified_directly = False
default identified_sample = ""
default ftir_result = None
default ftir_analyzing = False

# misc
default notebook_clicked = False
default notes_notebook_clicked = False
default notebook_notes = ""
# default more_details_clicked = False
# default instructions_clicked = False
default stereomicroscope_focus = renpy.random.choice(
    [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]
)
default paint_sample = "known_paint"

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]

default default_mouse = "default"
define config.mouse = { }
define config.mouse['default'] = [ ( "five.png", 0, 0) ]
define config.mouse['pressed_default'] = [ ( "grab.png", 0, 0) ]
define config.mouse['button'] = [ ( "grab.png", 0, 0) ]

default tasks = {
        "Run stereomicroscope on all samples": False,
        "Analyze remaining samples via FTIR": False,
        "Perform tire track analysis": False
    }

default paint_tasks = {
        "known_paint_analyzed": False,
        "unknown1_paint_analyzed": False,
        "unknown2_paint_analyzed": False,
        "unknown3_paint_analyzed": False
    }

default paint_ftir = {
        "known_paint_analyzed": False,
        "unknown1_paint_analyzed": False,
        "unknown2_paint_analyzed": False,
        "unknown3_paint_analyzed": False
    }

default fingerprint_tasks = {
        "fingerprint_1_analyzed": False,
    }

init -5 python:
    import json

    tools = load_items("jsons/toolbox.json")

    evids = load_items("jsons/evidence.json")

    # notebook_instructions = [
    #     ("swab_is_cut", "Cut (scissors) the cotton swab for it to fit into a 2 mL tube."),
    #     ("swab_is_prepped", "Add 400 μL Buffer AL, 20 μL Protease/Proteinase K, and 400 μL PBS to the sample."),
    #     ("swab_is_vortexed", "Vortex for 10 to 15 seconds."),
    #     ("swab_is_incubated", "Incubate at 56 °C for 10 minutes and spin it in the centrifuge."),
    #     ("swab_is_spun", "Add 400 μL of Ethanol (inventory), vortex for 10 to 15 seconds and spin it in the centrifuge."),
    #     ("swab_new_tube", "Place the Spin Column (the tube) on top of a new 2 mL tube (inventory) and add 700 μL of the sample into the column."),
    #     ("sample_is_spun", "Centrifuge it at 6000 RCF for 1 minute."),
    #     ("sample_new_tube", "Discard the 2 mL tube (inventory) with the liquid and place the column into a new 2mL tube.")
    # ]
    
    config.mouse = {
        "default": [("images/ui/cursors/cursor.png", 0, 0)],
        "pointer": [("images/ui/cursors/cursor.png", 0, 0)],
        "magnifying": [("images/ui/cursors/default_cursor.png", 0, 0)],
        "hover": [("images/ui/cursors/hover_cursor.png", 0, 0)],
        "dropper": [("images/ui/cursors/dropper.png", 0, 49)],
        "ethanol": [("images/ui/cursors/dropper_filled.png", 0, 49)],
        "hand": [("images/ui/cursors/default_hand.png", 0, 0)],
        "hand_grab": [("images/ui/cursors/grab_hand.png", 0, 0)],
        "micropipette": [("images/ui/cursors/micropipette.png", 10, 10)]
    }

    def hide_notebook():
        screens = [
            # "notebook_instructions_screen", 
            "notebook_screen", "notes_notebook_screen"
        ]
        for scr in screens:
            renpy.hide_screen(scr)

    def hide_afis():
        screens = [
            "data_analysis_lab_screen", "afis_screen", "afis", "analyzing", "show_results"
        ]
        for scr in screens:
            renpy.hide_screen(scr)

    def toggle_screen(name):
        if renpy.get_screen(name):
            renpy.hide_screen(name)
        else:
            renpy.show_screen(name)

    def toggle_notebook():
        toggle_screen("notebook_screen")
        # if instructions_clicked:
        #     toggle_screen("notebook_instructions_screen")

    def toggle_notes_notebook():
        toggle_screen("notes_notebook_screen")

    def check_swab_task_complete(task_list):
        return all(swab_tasks.get(task, True) for task in task_list)

    # define return mouse function under initializer
    def return_mouse_pos():
            return renpy.get_mouse_pos()
    
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

    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)

    def custom_notify(msg, correct=True):
        renpy.show_screen("notify", message=msg, correct=correct)

    def item_dragging_package(drags):
        """Used to set the mouse cursor to the hand_grab cursor when dragging an item.
        """
        global default_mouse
        default_mouse = "hand_grab"
        # return

    def item_dragged_package(drags, drop):
        """Used to set the mouse cursor to the hand_grab cursor when grabbing an item.
        """
        global default_mouse, tray_top_filled, tray_bottom_filled, tray_side_filled
        default_mouse = "hand_grab"
        
        if not drop:
            default_mouse = "hand"
            return None

        store.dragged = drags[0].drag_name
        store.dropped = drop.drag_name

        if drop.drag_name == "top":
            tray_top_filled = True
            custom_notify("Top filled!", correct=True)
        elif drop.drag_name == "bottom":
            tray_bottom_filled = True
            custom_notify("Bottom filled!", correct=True)
        elif drop.drag_name == "side":
            tray_side_filled = True
            custom_notify("Side filled!", correct=True)

        renpy.restart_interaction()

        if drop.drag_name in tray_placements:
            tray_placements[drop.drag_name] = drags[0].drag_name

        # Hide all draggable screens
        renpy.hide_screen("sample_to_tube")
        renpy.hide_screen("fingerprint_to_bag")
        renpy.hide_screen("tape_to_bag")
        renpy.hide_screen("folder_to_bag")
        renpy.hide_screen("letters_to_bag")
        default_mouse = "default"
        return None

#################################### START #############################################
label lab_start:
    python:
        toolbox.delete_from_inventory(tools["Backing Card"])
        toolbox.delete_from_inventory(tools["Scalebar"])
        toolbox.delete_from_inventory(tools["Tape"])
        toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
        toolbox.delete_from_inventory(tools["Gel Lifter"])
        toolbox.delete_from_inventory(tools["Magnetic Powder"])
        toolbox.delete_from_inventory(tools["Druggist Paper"])
        toolbox.delete_from_inventory(tools["Evidence Bag"])
        toolbox.delete_from_inventory(tools["Envelope"])
        toolbox.delete_from_inventory(tools["Roller"])
        evidence.delete_from_inventory(evids["Bagged Tire Track Impression"])
        evidence.delete_from_inventory(evids["Bagged Paint Transfer"])

        evidence.add_to_inventory(evids["Known Paint Sample"])
        evidence.add_to_inventory(evids["Unknown Paint Sample 1"])
        evidence.add_to_inventory(evids["Unknown Paint Sample 2"])
        evidence.add_to_inventory(evids["Unknown Paint Sample 3"])
        evidence.add_to_inventory(evids["Fingerprint 1"])

    $current_scene = "scene1" # keeps track of current scene

    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    $all_pieces = 0

    scene entering_lab_screen
    with Dissolve(1.0)

image bg stereomicroscope = Transform("backgrounds/stereomicroscope_bg.png", xysize=(1920, 1080))
image bg ftir = Transform("backgrounds/ftir_bg.png", xysize=(1920, 1080))

label lab_hallway_intro:
    # python:
    #     addToToolbox(["ethanol", "tube", "trash"])
    #     addToInventory(["fingerprint_1", "fingerprint_2"])
    scene hallway
    show nina talk
    n "Welcome to the lab!"
    n "This is where you will spend time analyzing the evidence you have collected."
    scene bg stereomicroscope
    n "Click the arrows or use your keyboard arrow keys to switch stations."
    jump bio_station

# label move_mouse:
#     $ renpy.set_mouse_pos(1695, 504)
#     return

label fingerprint_1_use_label:
    if location == "afis" and pressed == "import":
        $ imported_print = "print_1"
        jump import_print

label fingerprint_2_use_label:
    if location == "afis" and pressed == "import":
        $ imported_print = "print_2"
        jump import_print

label bio_station:
    hide screen inventory
    show screen notebook
    show screen notes_notebook
    call screen bio_station

label ftir_station:
    show screen notebook
    show screen notes_notebook
    call screen ftir_station

label use_swab:
    show screen notebook
    call screen swab_screen
    jump swab_sequence

label stereomicroscope_check_correct_layer_choice:

    if paint_sample == "known_paint":
        n "Correct! Known paint sample observed successfully."
        $ paint_tasks["known_paint_analyzed"] = True

    elif paint_sample == "unknown1_paint":
        n "Correct! Unknown Sample 1 observed successfully."
        $ paint_tasks["unknown1_paint_analyzed"] = True

    elif paint_sample == "unknown2_paint":
        n "Correct! Unknown Sample 2 observed successfully."
        $ paint_tasks["unknown2_paint_analyzed"] = True

    elif paint_sample == "unknown3_paint":
        n "Correct! Unknown Sample 3 observed successfully."
        $ paint_tasks["unknown3_paint_analyzed"] = True

    if all(paint_tasks.values()):
        n "You have completed the stereomicroscope analysis for all samples."
        $ tasks["Run stereomicroscope on all samples"] = True
        # n "You have successfully analyzed all paint samples using the stereomicroscope."
        # $ tasks["Run stereomicroscope on all samples"] = True
        # n "You have successfully observed all paint samples using the stereomicroscope. Now..."
        # call screen final_paint_check
        jump bio_station

label stereomicroscope_check_exclude:
    if paint_sample == "unknown1_paint":
        n "Unknown Sample 1 excluded."
        $ evidence.delete_from_inventory(evids["Unknown Paint Sample 1"])
        $ paint_tasks["unknown1_paint_analyzed"] = True
        $ del paint_ftir["unknown1_paint_analyzed"]
        $ paint_sample = "known_paint"
    elif paint_sample == "unknown2_paint":
        n "Unknown Sample 2 excluded."
        $ evidence.delete_from_inventory(evids["Unknown Paint Sample 2"])
        $ paint_tasks["unknown2_paint_analyzed"] = True
        $ del paint_ftir["unknown2_paint_analyzed"]
        $ paint_sample = "known_paint"
    elif paint_sample == "unknown3_paint":
        n "Unknown Sample 3 excluded."
        $ evidence.delete_from_inventory(evids["Unknown Paint Sample 3"])
        $ paint_tasks["unknown3_paint_analyzed"] = True
        $ del paint_ftir["unknown3_paint_analyzed"]
        $ paint_sample = "known_paint"

    if all(paint_tasks.values()):
        n "You have completed the stereomicroscope analysis for all samples."
        $ tasks["Run stereomicroscope on all samples"] = True
    if set(paint_ftir.keys()) == {"known_paint_analyzed"}:
        n "You cannot exclude all paint samples. Please try again."
        return
    jump bio_station

label stereomicroscope_check_cannot_exclude:
    if paint_sample == "unknown1_paint":
        n "You have decided that Unknown Sample 1 cannot be excluded."
        $ paint_tasks["unknown1_paint_analyzed"] = True
    elif paint_sample == "unknown2_paint":
        n "You have decided that Unknown Sample 2 cannot be excluded."
        $ paint_tasks["unknown2_paint_analyzed"] = True
    elif paint_sample == "unknown3_paint":
        n "You have decided that Unknown Sample 3 cannot be excluded."
        $ paint_tasks["unknown3_paint_analyzed"] = True

    if all(paint_tasks.values()):
        n "You have completed the stereomicroscope analysis for all samples."
        $ tasks["Run stereomicroscope on all samples"] = True
    jump bio_station

label stereomicroscope_check_identification:
    $ identified_directly = True

    if paint_sample == "unknown1_paint":
        n "You have identified the known paint sample to match Unknown Sample 1."
        $ identified_sample = "unknown1_paint"
    if paint_sample == "unknown2_paint":
        n "You have identified the known paint sample to match Unknown Sample 2."
        $ identified_sample = "unknown2_paint"
    if paint_sample == "unknown3_paint":
        n "You have identified the known paint sample to match Unknown Sample 3."
        $ identified_sample = "unknown3_paint"

    $ tasks["Run stereomicroscope on all samples"] = True
    $ tasks["Analyze remaining samples via FTIR"] = True
    if all(tasks.values()):
        jump finish_lab
    jump bio_station
    
    
label final_paint_check_choice:
    n "You have chosen a sample you find consistent with evidence using the stereomicroscope and FTIR machine."
    $ identified_sample = paint_ftir
    $ tasks["Analyze remaining samples via FTIR"] = True
    hide screen ftir_display
    jump ftir_station

label final_paint_check_start_over:
    n "Since you're not sure, you can redo the analysis."
    $ paint_ftir = {key: False for key in paint_ftir}
    jump ftir_station

label ftir_station_use_label:
    $ ftir_analyzing = True
    $ ftir_result = None
    if not tasks["Run stereomicroscope on all samples"]:
        n "You have to analyze all samples via stereomicroscope before using the FTIR machine."
        jump ftir_station

    "You load the sample into the FTIR machine and run the analysis..."
    show screen ftir_display


    pause 1.0

    $ ftir_analyzing = False
    $ ftir_result = paint_sample

    if paint_sample == "known_paint":
        $ paint_ftir["known_paint_analyzed"] = True
    elif paint_sample == "unknown1_paint":
        $ paint_ftir["unknown1_paint_analyzed"] = True
    elif paint_sample == "unknown2_paint":
        $ paint_ftir["unknown2_paint_analyzed"] = True
    elif paint_sample == "unknown3_paint":
        $ paint_ftir["unknown3_paint_analyzed"] = True

    if all(paint_ftir.values()):
        n "You have performed the FTIR analysis on all available samples. Now..."
        call screen final_paint_check
    if all(tasks.values()):
        jump finish_lab
    pause 
    $ ftir_analyzing = True
    $ ftir_result = None
    jump ftir_station

# label chem_station:
#     show screen full_inventory
#     show screen notebook
#     call screen chem_station

label impression_station:
    show screen inventory
    python:
        if all(fingerprint_tasks.values()):
            tasks["Perform tire track analysis"] = True
        if all(tasks.values()):
            renpy.jump("finish_lab")
    show screen notebook
    show screen notes_notebook
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen onlayer over_screens
    hide screen inventory
    show screen back_button_screen('data_analysis_lab') onlayer over_screens  
    call screen afis_screen

label wait_screen:
    scene black with dissolve
    if tasks["Prep swab for DNA analysis"]:
        show text "{color=#FFFFFF}We run the PCR machine...{/color}" at truecenter with dissolve
    elif check_swab_task_complete(["swab_new_tube"]):
        show text "{color=#FFFFFF}We spin at 6000 RCF for 1 minute...{/color}" at truecenter with dissolve
    else:
        show text "{color=#FFFFFF}We wait for 10 minutes...{/color}" at truecenter with dissolve
    pause 2.0
    hide text with dissolve
    jump bio_station

label finish_lab:
    hide screen inventory
    with Dissolve(1.0)
    scene hallway
    show nina talk at right
    n "Great job, you've finished all the tasks!"
    jump end_game

label end_game:
    scene black
    with Dissolve(2.5)
    return

transform half_size:
    zoom 0.5

transform blink:
    alpha 1.0
    linear 0.5 alpha 0.35
    linear 0.5 alpha 1.0
    repeat
