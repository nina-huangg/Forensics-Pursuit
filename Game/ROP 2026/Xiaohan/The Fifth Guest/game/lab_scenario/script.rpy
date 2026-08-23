define s = Character(name=("Nina"), image="nina")

# Case names live in courtroom_scenario/courtroom_data.rpy (CASE_VICTIM / CASE_SUSPECT).
define suspect_name = CASE_SUSPECT
define victim_name = CASE_VICTIM

default current_cursor = ""
default imported_print = ""
default show_case_files = False
default show_toolbox = False
default location = "bio_station"
default bio_station_view = 1
default notebook_clicked = False
default more_details_clicked = False
default instructions_clicked = False
default swab_is_vortexed_2 = False
default swab_is_incubated_0 = False
default ethanol_added = False
default ethanol_pour_amount = 0
default pour_hold_ticks = 0
default lysate_transfer_amount = 0
default aw1_pour_amount = 0
default ate_pour_amount = 0
default incubator_loaded_tubes = []
default profile_answers = {}
default profile_locus_index = 0
default profile_visited = []
default prep_view = 1
default tube_transfered = False
default lab_gameplay_initialized = False
default analysis_track = "blood"
default notebook_detail_page = 0
default dna_extraction_progress = {}

default tasks = {
    "DNA extraction": False,
    "DNA quantification": False,
    "DNA amplification": False,
    "Capillary Electrophoresis": False,
    "Profile Interpretation": False,
    "Statistics": False,
    "Fingerprint analysis": False,
}

default swab_tasks = {
    "swab_is_cut": False,
    "swab_is_prepped": False,
    "swab_is_vortexed": False,
    "swab_is_incubated": False,
    "swab_is_spun": False,
    "swab_new_tube": False,
    "sample_is_spun": False,
    "sample_new_tube": False,
}

default fingerprint_tasks = {
    "fingerprint_1_analyzed": False,
}

define dna_extraction_steps = [
    ("place_atl_prok", "Prep 2 swab tubes + negative control (ATL + ProK; NC has no swab). Then choose 1 sample."),
    ("vortex_10", "Pulse-vortex sample and negative control for 10 seconds each."),
    ("spin_1", "Mini-centrifuge sample and negative control."),
    ("incubate_56", "Load both tubes into the thermomixer, then set 56°C, 900 rpm, 1 hour once for both."),
    ("set_70", "Set thermomixer to 70°C."),
    ("spin_2", "Mini-centrifuge both tubes."),
    ("add_al", "At Prep: add 300 µL Buffer AL to sample and negative control."),
    ("vortex_al", "Pulse-vortex both tubes for 15 seconds."),
    ("spin_3", "Mini-centrifuge both tubes."),
    ("incubate_70", "Load both tubes into the thermomixer, then set 70°C, 900 rpm, 10 minutes once for both."),
    ("spin_4", "Mini-centrifuge both tubes."),
    ("add_ethanol_150", "Add 150 µL ethanol to both tubes."),
    ("vortex_ethanol", "Pulse-vortex both tubes for 15 seconds."),
    ("spin_5", "Mini-centrifuge both tubes."),
    ("transfer_lysate", "Transfer 700 µL lysate to QIAamp columns (sample + NC)."),
    ("centrifuge_8000_1", "Benchtop centrifuge 8000 rpm / 1 min (balance with NC)."),
    ("add_aw1", "New collection tube + 500 µL Buffer AW1."),
    ("centrifuge_aw1", "Benchtop centrifuge 8000 rpm / 1 min (balance with NC)."),
    ("add_aw2", "New collection tube + 700 µL Buffer AW2."),
    ("centrifuge_aw2", "Benchtop centrifuge 8000 rpm / 1 min (balance with NC)."),
    ("ethanol_new_tube", "Place column in a new collection tube."),
    ("add_ethanol_700", "Add 700 µL ethanol (pour mini-game)."),
    ("centrifuge_ethanol", "Benchtop centrifuge 8000 rpm / 1 min (balance with NC)."),
    ("new_collection_tube", "Place column in a new collection tube."),
    ("centrifuge_14000_3", "Benchtop centrifuge 14000 rpm / 3 min (balance with NC)."),
    ("column_to_labeled_tube", "Place column in a labelled 1.5 mL tube."),
    ("open_incubate_10", "Open lid; room-temp incubate 10 minutes."),
    ("add_ate", "Apply 20–100 µL Buffer ATE to the membrane."),
    ("incubate_1", "Room-temp incubate 1 minute, lid closed."),
    ("centrifuge_14000_1", "Benchtop centrifuge 14000 rpm / 1 min (balance with NC)."),
    ("discard_column", "Discard column; keep the collection tube (DNA extract)."),
]

init 1 python:
    # Extend the host cursor map; do not replace the crime-scene cursor setup.
    # Runs after the crime scene's init python (priority 0) has created the map.
    if config.mouse is None:
        config.mouse = {}
    config.mouse["micropipette"] = [("images/cursors/micropipette.png", 10, 10)]


init -4 python:
    def reset_lab_gameplay_state():
        """Reset only state owned by the imported lab scenario."""
        store.current_cursor = ""
        store.imported_print = ""
        store.show_case_files = False
        store.show_toolbox = False
        store.location = "bio_station"
        store.bio_station_view = 1
        store.prep_view = 1
        store.notebook_clicked = False
        store.more_details_clicked = False
        store.instructions_clicked = False
        store.swab_is_vortexed_2 = False
        store.swab_is_incubated_0 = False
        store.ethanol_added = False
        store.tube_transfered = False
        store.analysis_track = "blood"
        store.notebook_detail_page = 0
        store.dna_extraction_progress = {}
        extraction_reset()
        qpcr_reset_plate()
        pcr_plate_reset()

        # If the player only collected one blood sample at the scene, extraction
        # only needs that one tube (+ negative control) instead of always two.
        store.prep_samples_needed = max(1, len(store.lab_blood_samples))

        store.tasks = {
            "DNA extraction": False,
            "DNA quantification": False,
            "DNA amplification": False,
            "Capillary Electrophoresis": False,
            "Profile Interpretation": False,
            "Statistics": False,
            "Fingerprint analysis": False,
        }
        store.swab_tasks = {
            "swab_is_cut": False,
            "swab_is_prepped": False,
            "swab_is_vortexed": False,
            "swab_is_incubated": False,
            "swab_is_spun": False,
            "swab_new_tube": False,
            "sample_is_spun": False,
            "sample_new_tube": False,
        }
        store.fingerprint_tasks = {"fingerprint_1_analyzed": False}

        # AFIS state is defined in afis.rpy.
        store.pressed = ""
        store.print_imported = False
        store.current_print = ""
        store.i = 1
        for lab_print in store.prints.values():
            lab_print.processed = False

        # With no collected sample, DNA work is unavailable rather than fake.
        if not store.lab_blood_samples:
            for task_name in (
                "DNA extraction",
                "DNA quantification",
                "DNA amplification",
                "Capillary Electrophoresis",
                "Profile Interpretation",
                "Statistics",
            ):
                store.tasks[task_name] = True

        store.lab_gameplay_initialized = True

    def complete_dna_step(step_key):
        store.dna_extraction_progress[step_key] = True
        renpy.restart_interaction()

    def complete_dna_steps(*step_keys):
        for step_key in step_keys:
            store.dna_extraction_progress[step_key] = True
        renpy.restart_interaction()

    def complete_next_dna_step(step_keys):
        for step_key in step_keys:
            if not store.dna_extraction_progress.get(step_key, False):
                store.dna_extraction_progress[step_key] = True
                break
        renpy.restart_interaction()

    def notebook_task_names():
        if store.analysis_track == "fingerprint":
            return ["Fingerprint analysis"]
        return [
            "DNA extraction",
            "DNA quantification",
            "DNA amplification",
            "Capillary Electrophoresis",
            "Profile Interpretation",
            "Statistics",
        ]

    def hide_lab_overlays():
        for screen_name in (
            "inventory", "inventory_info", "notebook_screen",
            "notebook_instructions_screen", "lab_notify", "qpcr_plate_prep",
            "pcr_plate_prep",
        ):
            renpy.hide_screen(screen_name)

    def hide_notebook():
        renpy.hide_screen("notebook_screen")
        renpy.hide_screen("notebook_instructions_screen")

    def toggle_screen(name):
        if renpy.get_screen(name):
            renpy.hide_screen(name)
        else:
            renpy.show_screen(name)

    def toggle_notebook():
        toggle_screen("notebook_screen")
        if store.instructions_clicked:
            toggle_screen("notebook_instructions_screen")

    def check_swab_task_complete(task_list):
        return all(store.swab_tasks.get(task, True) for task in task_list)

    def set_cursor(cursor):
        store.default_mouse = cursor or "default"
        store.current_cursor = cursor

    def custom_notify(msg, correct=True):
        renpy.show_screen("lab_notify", message=msg, correct=correct)

    def record_lab_mistake():
        store.evidence_wrong_moves = getattr(store, "evidence_wrong_moves", 0) + 1

    def open_machine():
        """Hide notebook overlays before entering any machine UI."""
        hide_notebook()

    def try_complete_machine_step(required_ok, success_msg=None, warn_msg="Not the right time for this step."):
        """Allow free machine use; only complete progress when prerequisites are met."""
        if required_ok:
            if success_msg:
                custom_notify(success_msg, True)
            return True
        custom_notify(warn_msg, False)
        record_lab_mistake()
        return False

    def reset_lab_cursor():
        """Always enter lab locations with the normal mouse pointer."""
        store.default_mouse = "default"
        store.active_tool = None

label lab_transition_loading:
    $ reset_lab_cursor()
    $ hide_lab_overlays()
    $ renpy.hide_screen("open_inv")
    $ renpy.hide_screen("deferred_lab_transition")
    $ renpy.hide_screen("evidence_collected_notice")

    window hide
    scene entering_lab_screen
    with Dissolve(1.0)
    $ renpy.pause(2.0)

    jump lab_hallway_intro


label lab_hallway_intro:
    $ reset_lab_cursor()
    if not lab_gameplay_initialized:
        $ reset_lab_gameplay_state()

    $ renpy.hide_screen("inventory")
    $ renpy.hide_screen("open_inv")
    scene hallway
    show nina talk
    s "Welcome to the lab!"
    s "This is where you will analyze the evidence you collected."
    s "You can choose DNA analysis or fingerprint analysis."
    s "What would you like to analyze first?"

    menu:
        "DNA analysis":
            $ analysis_track = "blood"
            $ notebook_detail_page = 0
            s "The forensic pathologist has completed the examination. The cause of death was blunt force trauma to the head, and the mechanism of death was hemorrhage."
            s "Skin tissue was also recovered from beneath the victim's fingernails. Here is the swab containing the sample. Your colleague will help perform DNA analysis on it."
            $ under_nail_swab = Item("Under-Nail Swab", "inventory-swab", "Skin tissue recovered from beneath the victim's fingernails. Your colleague is running DNA analysis on this sample.", False, None)
            $ is_packing_evidence = True
            $ evidence.add_to_inventory(under_nail_swab)
            $ is_packing_evidence = False
            scene expression "backgrounds/station1.png"
            show nina talk at right
            s "We'll begin with DNA extraction from the collected blood swabs."
            s "Prepare a negative control at the same time — follow every step, but do not add a swab."
            s "First, which DNA extraction method should we use?"
            jump choose_dna_extraction_method

        "Fingerprint analysis":
            $ analysis_track = "fingerprint"
            scene afis_interface
            show nina talk at right
            s "We'll begin by comparing the collected fingerprint in AFIS."
            hide nina
            jump impression_station


label choose_dna_extraction_method:
    show nina talk at right

    menu:
        "QIAamp":
            s "Correct. QIAamp is the appropriate extraction method for these blood swabs."
            s "Open the notebook at any time to review the procedure."
            hide nina
            jump bio_station

        "Chelex":
            s "That method is not appropriate for these samples."
            s "Chelex extraction is primarily used for sexual-assault case samples. Please choose again."
            jump choose_dna_extraction_method


label bio_station:
    $ reset_lab_cursor()
    $ bio_station_view = 1
    $ location = "bio_station"
    $ analysis_track = "blood"
    if extraction_complete():
        $ tasks["DNA extraction"] = True
    if all(tasks.values()):
        jump finish_lab
    show screen open_inv
    show screen notebook
    scene expression "backgrounds/station1.png"
    call screen bio_station
    jump bio_station


label bio_station_2:
    $ reset_lab_cursor()
    $ bio_station_view = 2
    $ location = "bio_station"
    $ analysis_track = "blood"
    if extraction_complete():
        $ tasks["DNA extraction"] = True
    if all(tasks.values()):
        jump finish_lab
    show screen open_inv
    show screen notebook
    scene expression "backgrounds/station2.png"
    call screen bio_station_2
    jump bio_station_2


label return_bio_station:
    if bio_station_view == 2:
        jump bio_station_2
    jump bio_station


label use_swab:
    show screen notebook
    call screen swab_screen
    jump return_bio_station


label impression_station:
    $ reset_lab_cursor()
    $ location = "afis"
    $ analysis_track = "fingerprint"
    if all(fingerprint_tasks.values()):
        $ tasks["Fingerprint analysis"] = True
    if all(tasks.values()):
        jump finish_lab
    show screen open_inv
    show screen notebook
    call screen data_analysis_lab_screen


label finish_lab:
    $ hide_lab_overlays()
    $ renpy.hide_screen("open_inv")
    $ renpy.hide_screen("notebook")
    with Dissolve(1.0)
    scene hallway
    show nina talk at right
    with hpunch
    s "Great job, you've finished all the available lab tasks!"
    s "The analysis is done, but the case isn't. You'll be called to testify about your findings as an expert witness."
    hide nina
    $ reset_courtroom_state()

    # Without an API key there is no examination to play; end here instead.
    if not courtroom_api_key_available():
        call screen courtroom_api_key_missing
        if not courtroom_api_key_available():
            jump end_game

    jump courtroom_transition_loading


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
