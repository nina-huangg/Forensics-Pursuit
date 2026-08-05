init python:
    import json

    tools = load_items("jsons/toolbox.json")

    evids = load_items("jsons/evidence.json")
    evidences = []
    freezing = False
    active_swab = None   # None, "wall", or "floor" -- which one is currently being processed
    wall_done = False
    floor_done = False
    lysis_done = False
    protein_done = False

    snipped = False
    swab = False
    scalebar = False
    tape = False
    step = 0

define n = Character(name=("Nina"), image="nina")
define lab_fingerprint_done = False
define lab_dna_done = False
define gloves_worn = False

label start:
    $ evidence.add_to_inventory(evids["Fingerprint 1"])
    $ evidence.add_to_inventory(evids["Handprint"])
    scene hallway
    show nina normal1 at left
    n "Hello detective. I'm detective Nina. Welcome to the lab."
    show nina thinknote1 at left
    n "You're gonna need to analyze all the evidence you collected at the crime scene."
    jump game

label game:
    hide screen lab
    hide nina normal1
    hide nina thinknote1
    scene hallway
    show screen inventory
    show screen hallway
    call screen lab_hub
    
################################################################################
## Lab Level
################################################################################
##
## FINGERPRINTS (working): an AFIS terminal. Since fingerprint evidence is
## collected optionally in different spots (door handle is mandatory, the can
## and steering wheel prints are optional), we don't hardcode which evidence
## item name to expect. Instead, on entering the lab we scan `evidence`
## (the same Inventory object used everywhere else) for any collected item
## whose name looks like a print, and wire each one up as importable.
##
## DNA (placeholder, unchanged): gel-band matching minigame. Not the focus
## of this pass.
##
## ---------------------------------------------------------------------------
## ASSET REQUIREMENTS
## ---------------------------------------------------------------------------
##   lab_hallway, data_analysis_lab_idle/hover, materials_lab_idle/hover
##                                  -> the lab hallway hub background + room
##                                     buttons (see screen lab_hub)
##
## AFIS database cards (from your source lab images, ~431x578):
##   print_1, print_2, print_3   -> however you already have these named/
##                                  loaded from your source project. If your
##                                  existing image names differ, just edit
##                                  the `image=` values in afis_prints below.
##
## For the IMPORTED side, each collected print gets its own card. If you
## already have specific art for "the door handle print" etc., add an entry
## to PRINT_EVIDENCE_IMAGES below (evidence item name -> image name) and
## it'll be used automatically. Anything not listed there just falls back
## to that evidence item's own inventory icon, so nothing breaks if you
## haven't made dedicated AFIS art for every possible print yet.
################################################################################

init -5 python:

    ############################################################################
    ## AFIS -- fingerprint database
    ############################################################################

    import os

    ## Where your source lab's print_1.png..print_7.png and their
    ## print_i_closeup_j.png files live. Change this if yours are elsewhere.
    DATA_LAB_DIR = "images/data_analysis_lab"

    def afis_file_exists(file_name):
        """file_name must end in .png"""
        file_path = os.path.join(renpy.config.gamedir, DATA_LAB_DIR, file_name)
        return os.path.isfile(file_path)

    NUM_DB_PRINTS = 6

    ## --- Who's who --------------------------------------------------------
    ## Two independent suspects. Each has exactly one real match in the
    ## database: the Left Wall fingerprint matches print_1, and the
    ## Right Wall handprint (zoomed to a fingerprint) matches print_4.
    ## Everything else in the deck (print_2, print_3, print_5, print_6)
    ## is a decoy -- unrelated people on file, no connection to the case.

    LEFT_WALL_SUSPECT_NAME = "Travis Welce"
    RIGHT_WALL_SUSPECT_NAME = "Taylor Shift"

    LEFT_WALL_SOURCE_SCORES = {
        "print_1": (True, 95),
        "print_2": (False, 19),
        "print_3": (False, 14),
        "print_4": (False, 11),
        "print_5": (False, 22),
        "print_6": (False, 17),
    }
    RIGHT_WALL_SOURCE_SCORES = {
        "print_1": (False, 16),
        "print_2": (False, 21),
        "print_3": (False, 13),
        "print_4": (True, 93),
        "print_5": (False, 18),
        "print_6": (False, 20),
    }

    ## Central registry: which database slot is a REAL suspect match, who
    ## it belongs to, what evidence-item keyword routes to it, what score
    ## table applies, and what Nina says on a hit. Add more entries here
    ## if you ever add a third piece of print evidence.
    MATCH_INFO = {
        "print_1": {
            "suspect_name": LEFT_WALL_SUSPECT_NAME,
            "source_keyword": "left",
            "scores": LEFT_WALL_SOURCE_SCORES,
            "description": "Booking record on file: %s." % LEFT_WALL_SUSPECT_NAME,
            "match_lines": [
                "Search complete. The AFIS algorithm reports an optimal minutiae configuration match.",
                "Confirming match. The print recovered from the left wall belongs to %s." % LEFT_WALL_SUSPECT_NAME,
            ],
        },
        "print_4": {
            "suspect_name": RIGHT_WALL_SUSPECT_NAME,
            "source_keyword": "right",
            "scores": RIGHT_WALL_SOURCE_SCORES,
            "description": "Booking record on file: %s." % RIGHT_WALL_SUSPECT_NAME,
            "match_lines": [
                "Search complete. The AFIS algorithm reports an optimal minutiae configuration match.",
                "Confirming match. The isolated fingerprint from the handprint belongs to %s." % RIGHT_WALL_SUSPECT_NAME,
            ],
        },
    }

    PRINT_SOURCE_RULES = [
        ("fingerprint 1", "print_1"),   # -> Travis Welce
        ("handprint", "print_4"),       # -> Taylor Shift, zoomed to a fingerprint
    ]
    PRINT_SOURCE_DEFAULT_DB_KEY = "print_1"   # fallback if neither keyword hits

    PRINT_EVIDENCE_IMAGES = {
        # "Left Wall Fingerprint": "afis-print-left-wall",
        "Right Wall Handprint": "handprint_zoomed_fingerprint",
    }

    PRINT_NAME_KEYWORDS = ["print", "fingerprint"]

    ## --- AfisMCQ: pattern-matching quiz shown after Compare -----------------
    class AfisMCQ(object):
        """
        A multiple-choice pattern-matching question, asked about a database
        print's ridge pattern (whorl/loop/arch/etc.) after Compare and
        before the match result. Answering wrong loops the question again.

        - choices: list of (text, is_correct) tuples
        - responses: list of lists of strings -- responses[i] is what plays
        after picking choice i, whether right or wrong
        """
        def __init__(self, question, choices, responses):
            self.question = question
            self.choices = choices
            self.responses = responses

        def items(self):
            return [(text, i) for i, (text, _correct) in enumerate(self.choices)]

        def is_correct(self, choice):
            if 0 <= choice < len(self.choices):
                return self.choices[choice][1]
            return False

    DB_PRINT_INFO = {
        "print_1": ("print_1", MATCH_INFO["print_1"]["description"]),
        "print_2": ("print_2", "Unrelated record on file, not connected to this case."),
        "print_3": ("print_3", "Unrelated record on file, not connected to this case."),
        "print_4": ("print_4", MATCH_INFO["print_4"]["description"]),
        "print_5": ("print_5", "Unrelated record on file, not connected to this case."),
        "print_6": ("print_6", "Unrelated record on file, not connected to this case."),
    }

    DB_PRINT_MCQS = {
        "print_1": AfisMCQ(
            question="Classify the friction ridge pattern displayed below.",
            choices=[("Arch", False), ("Whorl", False), ("Loop", True)],
            responses=[
                ["That's not an arch pattern.", "Take another look."],
                ["That's not a whorl pattern.", "Take another look."],
                ["That's a loop, the ridges curve and come back out the same side.", "Let's finish the comparison."],
            ],
        ),
        "print_2": AfisMCQ(
            question="What dermatoglyphic classification does this print exhibit?",
            choices=[("Loop", False), ("Whorl", True), ("Arch", False)],
            responses=[
                ["That's not a loop pattern.", "Take another look."],
                ["That's a whorl, the ridges circle back on themselves.", "Let's finish the comparison."],
                ["That's not an arch pattern.", "Take another look."],
            ],
        ),
        "print_3": AfisMCQ(
            question="Identify the focal points to determine the ridge pattern group.",
            choices=[("Whorl", False), ("Loop", False), ("Arch", True)],
            responses=[
                ["That's not a whorl pattern.", "Take another look."],
                ["That's not a loop pattern.", "Take another look."],
                ["That's an arch, the ridges rise in the middle with no backward turn.", "Let's finish the comparison."],
            ],
        ),
        "print_4": AfisMCQ(
            question="Examine the core and delta positioning. What is the primary ridge classification?",
            choices=[("Loop", False), ("Arch", False), ("Whorl", True)],
            responses=[
                ["That's not a loop pattern.", "Take another look."],
                ["That's not an arch pattern.", "Take another look."],
                ["That's a whorl, the ridges circle back on themselves.", "Let's finish the comparison."],
            ],
        ),
        "print_5": AfisMCQ(
            question="Classify the friction ridge pattern displayed below.",
            choices=[("Arch", True), ("Whorl", False), ("Loop", False)],
            responses=[
                ["That's an arch, the ridges rise in the middle with no backward turn.", "Let's finish the comparison."],
                ["That's not a whorl pattern.", "Take another look."],
                ["That's not a loop pattern.", "Take another look."],
            ],
        ),
        "print_6": AfisMCQ(
            question="What dermatoglyphic classification does this print exhibit?",
            choices=[("Loop", True), ("Whorl", False), ("Arch", False)],
            responses=[
                ["That's a loop, the ridges curve and come back out the same side.", "Let's finish the comparison."],
                ["That's not a whorl pattern.", "Take another look."],
                ["That's not an arch pattern.", "Take another look."],
            ],
        ),
    }

    ## --- AfisPrint: a single print card ------------------------------------
    class AfisPrint(object):
        """
        A single print card in the AFIS system.

        - image: the big comparison image (~431x578), no file extension.
        - closeup_1/2/3 (optional): zoomed-in detail shots shown during
        "Compare". Falls back to `image` when unset.
        - description: revealed in dialogue once this print is identified.
        - scores: REQUIRED for imported prints. Maps a database card's key
        to (is_match, consistency_percent).
        - mcq (optional): only meaningful on database cards -- an AfisMCQ
        asked while that card is the one being viewed.
        """
        def __init__(self, image, closeup_1="", closeup_2="", closeup_3="", description="", scores=None, mcq=None):
            self.image = image
            self.closeup_1 = closeup_1
            self.closeup_2 = closeup_2
            self.closeup_3 = closeup_3
            self.description = description
            self.scores = scores or {}
            self.mcq = mcq
            self.processed = False

        def process(self):
            self.processed = True

    def make_afis_print(image, description="", scores=None, mcq=None):
        """Builds an AfisPrint and auto-attaches closeup_1/2/3 if matching
        <image>_closeup_1/2/3.png files exist in DATA_LAB_DIR."""
        p = AfisPrint(image=image, description=description, scores=scores, mcq=mcq)
        for j in range(1, 4):
            closeup_filename = "%s_closeup_%d.png" % (image, j)
            closeup_name = "%s_closeup_%d" % (image, j)
            if afis_file_exists(closeup_filename):
                setattr(p, "closeup_%d" % j, closeup_name)
        return p

    afis_prints = {}
    for _db_key, (_image, _desc) in DB_PRINT_INFO.items():
        afis_prints[_db_key] = make_afis_print(_image, description=_desc)
    for _db_key, _mcq in DB_PRINT_MCQS.items():
        afis_prints[_db_key].mcq = _mcq

    ## Runtime state for the AFIS terminal.
    afis_active = False
    imported_print = None
    print_imported = False
    current_db_print = 1
    afis_import_keys = []
    _compare_left_img = None
    _compare_right_img = None
    identified_suspect_keys = set()

    def is_print_evidence(item):
        name_lower = item.name.lower()
        return any(k in name_lower for k in PRINT_NAME_KEYWORDS)

    def get_print_evidence_items():
        return [item for item in evidence._inventory if is_print_evidence(item)]

    def slugify_print_key(name):
        cleaned = "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")
        return "print_evidence_%s" % cleaned

    def resolve_print_source(item):
        name_lower = item.name.lower()
        for keyword, db_key in PRINT_SOURCE_RULES:
            if keyword in name_lower:
                return db_key
        return PRINT_SOURCE_DEFAULT_DB_KEY

    def register_importable_print(item):
        key = slugify_print_key(item.name)
        if key not in afis_prints:
            source_db_key = resolve_print_source(item)
            default_image = DB_PRINT_INFO[source_db_key][0]
            default_scores = MATCH_INFO[source_db_key]["scores"]
            image = PRINT_EVIDENCE_IMAGES.get(item.name, default_image)
            afis_prints[key] = make_afis_print(
                image,
                description="The %s." % item.name.lower(),
                scores=dict(default_scores),
            )
        return key

    def make_afis_import_action(print_key):
        def _action():
            global imported_print, print_imported
            if not afis_active:
                renpy.notify("Take this to the AFIS terminal first.")
                return
            if afis_prints[print_key].processed:
                renpy.notify("We've already identified this print.")
                return
            imported_print = print_key
            print_imported = True
            renpy.hide_screen("inventory")
            renpy.jump("afis_import_print")
        return _action


################################################################################
## AFIS screens
################################################################################

screen afis():
    modal True
    add Solid("#000c")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 40
        background Frame("gui/frame.png", gui.frame_borders, tile=False)

        vbox:
            spacing 20
            xalign 0.5

            text "AFIS: Automated Fingerprint Identification System" size 38 xalign 0.5

            hbox:
                xalign 0.5
                spacing 90

                vbox:
                    xalign 0.5
                    spacing 10
                    text "Imported Print" size 24 xalign 0.5
                    frame:
                        xsize 260
                        ysize 350
                        background Solid("#111")
                        if print_imported:
                            add afis_prints[imported_print].image:
                                xalign 0.5
                                yalign 0.5
                                zoom 0.6
                        else:
                            text "No print imported" xalign 0.5 yalign 0.5 size 20

                vbox:
                    xalign 0.5
                    spacing 10
                    text "Database Record [current_db_print]/[NUM_DB_PRINTS]" size 24 xalign 0.5
                    frame:
                        xsize 260
                        ysize 350
                        background Solid("#111")
                        add afis_prints["print_%d" % current_db_print].image:
                            xalign 0.5
                            yalign 0.5
                            zoom 0.6

            hbox:
                xalign 0.5
                spacing 30

                textbutton "Import" action ToggleScreen("inventory")
                textbutton "Prev" action Jump("afis_show_prev") sensitive print_imported
                textbutton "Next" action Jump("afis_show_next") sensitive print_imported
                textbutton "Compare" action Jump("afis_compare") sensitive print_imported
                textbutton "Back to Lab" action Jump("afis_exit")


screen afis_analyzing():
    frame:
        xalign 0.5
        yalign 0.85
        background Frame("gui/frame.png", gui.frame_borders, tile=False)
        text "Analyzing..." size 34


screen afis_compare_view():
    ## Used for both the import reveal and the closeup zoom-through during
    ## Compare -- same dark backdrop + gui frame as the main afis() screen,
    ## so nothing ever just floats loose on the bare background.
    zorder 60
    add Solid("#000c")
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 40
        background Frame("gui/frame.png", gui.frame_borders, tile=False)

        hbox:
            xalign 0.5
            spacing 90

            vbox:
                xalign 0.5
                spacing 10
                text "Imported Print" size 24 xalign 0.5
                frame:
                    xsize 300
                    ysize 400
                    background Solid("#111")
                    if _compare_left_img:
                        add _compare_left_img:
                            xalign 0.5
                            yalign 0.5
                            xsize 280
                            ysize 380
                            fit "contain"

            vbox:
                xalign 0.5
                spacing 10
                text "Database Record" size 24 xalign 0.5
                frame:
                    xsize 300
                    ysize 400
                    background Solid("#111")
                    if _compare_right_img:
                        add _compare_right_img:
                            xalign 0.5
                            yalign 0.5
                            xsize 280
                            ysize 380
                            fit "contain"


screen afis_quiz_images():
    ## Used only during the pattern-matching quiz -- deliberately NO dark
    ## backdrop and NO frame here, since the full afis_compare_view was
    ## covering the question text. Negative zorder keeps this behind the
    ## dialogue box and menu choices, but it still renders above the base
    ## scene since screens always sit above the master layer.
    ##
    ## Just the database record, single and large -- that's the print the
    ## question is actually asking about, so no need for the imported
    ## print alongside it here.
    zorder -5
    if _compare_right_img:
        add _compare_right_img:
            xalign 0.5
            yalign 0.4
            xsize 420
            ysize 560
            fit "contain"


################################################################################
## AFIS labels
################################################################################

label lab_fingerprint_station:
    $ afis_active = True
    $ current_db_print = 1
    hide screen hallway
    hide afis_print_l
    hide afis_print_r
    show nina thinknote1 at right
    $ _print_items = get_print_evidence_items()
    if not _print_items:
        n "The automated fingerprint identification system (AFIS) requires a high-resolution digitized input file. We cannot run a database query until the scene processing is finalized."
        jump afis_exit
    $ afis_import_keys = []
    python:
        for _item in _print_items:
            _key = register_importable_print(_item)
            _item.usable = True
            _item.action = make_afis_import_action(_key)
            afis_import_keys.append(_key)
    call screen afis


label afis_exit:
    $ afis_active = False
    hide afis_print_l
    hide afis_print_r
    hide nina with dissolve
    show screen hallway
    jump lab_hub_loop


label afis_import_print:
    call screen afis


label afis_show_prev:
    $ current_db_print = NUM_DB_PRINTS if current_db_print <= 1 else current_db_print - 1
    call screen afis


label afis_show_next:
    $ current_db_print = 1 if current_db_print >= NUM_DB_PRINTS else current_db_print + 1
    call screen afis


label afis_compare:
    show screen afis_analyzing
    $ _db_key = "print_%d" % current_db_print
    $ _left = afis_prints[imported_print]
    $ _right = afis_prints[_db_key]
    $ _left_shots = [_left.closeup_1, _left.closeup_2, _left.closeup_3, _left.image]
    $ _right_shots = [_right.closeup_1, _right.closeup_2, _right.closeup_3, _right.image]
    show screen afis_compare_view
    python:
        for _m in range(4):
            _compare_left_img = _left_shots[_m] if _left_shots[_m] else _left.image
            _compare_right_img = _right_shots[_m] if _right_shots[_m] else _right.image
            renpy.restart_interaction()
            renpy.pause(0.6)
    hide screen afis_analyzing
    hide screen afis_compare_view
    show screen afis_quiz_images
    jump afis_quiz


label afis_quiz:
    $ _quiz = afis_prints[_db_key].mcq
    if _quiz is None:
        jump afis_show_results
    python:
        renpy.say(n, _quiz.question)
        _quiz_choice = renpy.display_menu(_quiz.items())
        for _quiz_line in _quiz.responses[_quiz_choice]:
            renpy.say(n, _quiz_line)
        _quiz_correct = _quiz.is_correct(_quiz_choice)
    if _quiz_correct:
        jump afis_show_results
    else:
        jump afis_quiz


label afis_show_results:
    hide screen afis_quiz_images
    $ is_match, score = afis_prints[imported_print].scores[_db_key]
    n "[score]%% consistency."

    if is_match:
        $ afis_prints[imported_print].process()
        $ identified_suspect_keys.add(_db_key)
        python:
            for _line in MATCH_INFO[_db_key]["match_lines"]:
                renpy.say(n, _line)
        if identified_suspect_keys >= set(MATCH_INFO.keys()):
            $ lab_fingerprint_done = True
    else:
        n "No matching fingerprint records identified within the database."

    call screen afis


################################################################################
## Lab hub
################################################################################

label scene_lab:
    scene lab_hallway with fade
    $ lab_fingerprint_done = False
    $ lab_dna_done = False
    $ dna_reset()
    $ gloves_worn = False
    show nina normal1 at right with moveinright
    n "Welcome to the lab. Now we let the physical evidence tell the story."
    n "Take the latent print card over to the Data Analysis desk for AFIS scanning. Then, we'll head to the DNA bench to extract our biological sample."
    hide nina with dissolve
    jump glove_gate_lab

label glove_gate_lab:
    if gloves_worn or not has_gloves_item():
        hide nina with dissolve
        jump lab_hub_loop
    $ _glove_return_label = "glove_gate_lab"
    $ _gloves_item = get_toolbox_item("Gloves")
    if _gloves_item:
        $ _gloves_item.usable = True
    show nina thinknote1 at right
    n "Fresh gloves before we handle anything in here."
    call screen inventory
    jump glove_gate_lab

label lab_hub_loop:
    call screen lab_hub
    jump lab_hub_loop


screen lab_hub():

    ## Data Analysis Lab -> AFIS (fingerprints)
    hbox:
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            action Jump("lab_fingerprint_station")
            hovered Notify("\u2713 Fingerprint Matched" if lab_fingerprint_done else "Data Analysis Lab")
            unhovered Notify("")
            xpos 1000
            ypos 400

    if lab_fingerprint_done and lab_dna_done:
        textbutton "Conclude Case":
            style "custom_button"
            xalign 0.5
            yalign 0.92
            action Jump("lab_conclusion")

label scissors_use_label:
    if active_swab == None:
        "What piece of evidence would you like to cut?"
        $ evidence.add_to_inventory(evids["Splatter"])
        $ evidence.add_to_inventory(evids["Splatter 2"])
        call screen inventory
    "Let's take a snip of the swab for evidence..."
    show snip0 zorder 10000
    pause 0.7
    hide snip0
    show snip1 zorder 10000
    pause 0.7
    hide snip1
    show snip2 zorder 10000
    pause 0.7
    hide snip2
    show snip3 zorder 10000
    pause 0.7
    hide snip3
    show snip4 zorder 10000
    pause 0.3
    hide snip4
    $ snipped = True
    $ toolbox.delete_from_inventory(tools["Scissors"])
    $ toolbox.add_to_inventory(tools["Lysis Buffer"])
    $ toolbox.add_to_inventory(tools["Proteinase K"])
    if active_swab == "floor":
        $ evidence.delete_from_inventory(evids["Splatter"])
    else:
        $ evidence.delete_from_inventory(evids["Splatter 2"])
    $ evidence.add_to_inventory(evids["Swab Cutting in Tube"])
    jump laboratory

label wall_use_label:
    if active_swab is not None:
        "You're already processing the [active_swab] swab. Finish that before starting another."
    elif wall_done:
        "You've already finished processing the wall swab."
    else:
        $ active_swab = "wall"
        jump scissors_use_label
    jump laboratory

label floor_use_label:
    if active_swab is not None:
        "You're already processing the [active_swab] swab. Finish that before starting another."
    elif floor_done:
        "You've already finished processing the floor swab."
    else:
        $ active_swab = "floor"
        jump scissors_use_label
    jump laboratory

label lysis_use_label:
    if lysis_done:
        "We've already added the lysis buffer."
        jump laboratory
    "We need 0.2 ml of lysis buffer."
    $ amt = renpy.input("How much lysis buffer do we need?", allow=set(".0123456789"))
    if amt == "0.2":
        "Perfect!"
        show snip4 zorder 10000
        pause 0.7
        hide snip4
        show lysis zorder 10000
        pause 0.7
        hide lysis
        $ step += 1
        $ lysis_done = True
        $ toolbox.delete_from_inventory(tools["Lysis Buffer"])
        if not protein_done:
            $ evidence.delete_from_inventory(evids["Swab Cutting in Tube"])
            $ evidence.add_to_inventory(evids["Swab Cutting Solution"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump lysis_use_label

label protein_use_label:
    if protein_done:
        "We've already added the proteinase K."
        jump laboratory
    "We need 0.01 ml of proteinase K."
    $ amt = renpy.input("How much proteinase K do we need?", allow=set(".0123456789"))
    if amt == "0.01":
        "Perfect!"
        show snip4 zorder 10000
        pause 0.7
        hide snip4
        show lysis zorder 10000
        pause 0.7
        hide lysis
        $ step += 1
        $ protein_done = True
        $ toolbox.delete_from_inventory(tools["Proteinase K"])
        if not lysis_done:
            $ evidence.delete_from_inventory(evids["Swab Cutting in Tube"])
            $ evidence.add_to_inventory(evids["Swab Cutting Solution"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump protein_use_label


label heat:
    "We should heat it at 56 degrees Celsius for 2 hours."
    $ temp = renpy.input("What temperature should we heat it at?", allow=set("0123456789"))
    if temp == "56":
        $ time = renpy.input("How long in minutes should we heat it for?", allow=set("0123456789"))
        if time == "120":
            'Great! Now we have to wait.'
            show heatskin zorder 10000:
                xpos 500
                ypos 700
            with Dissolve(2.0)
            $ step = 3
            "It should be done. Go ahead and take it out and remove the swab cutting."
            $ evidence.delete_from_inventory(evids["Swab Cutting Solution"])
            $ evidence.add_to_inventory(evids["Swab Cutting After Heating"])
            $ toolbox.add_to_inventory(tools["Phenol Chloroform"])
            jump laboratory
        else:
            "Wrong time."
            jump heat
    else:
        'Wrong temperature.'
        jump heat

label phenol_use_label:
    "We need an equal volume of phenol-chloroform. We have 0.21 ml of lysate!"
    $ amt = renpy.input("How much phenol chloroform do we need?", allow=set(".0123456789"))
    if amt == "0.21":
        "Perfect!"
        show phen0 zorder 10000
        pause 0.7
        hide phen0
        show phen1 zorder 10000
        pause 0.7
        hide phen1
        $ step = 4
        $ evidence.delete_from_inventory(evids["Swab Cutting After Heating"])
        $ evidence.add_to_inventory(evids["Solution after Phenol-Chloroform"])
        $ toolbox.delete_from_inventory(tools["Phenol Chloroform"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump phenol_use_label

label vortex:
    show phen1 zorder 10000
    pause 0.3
    hide phen1
    "Vortexing..."
    pause 0.6
    show phen2 zorder 10000
    $ step = 5
    $ evidence.delete_from_inventory(evids["Solution after Phenol-Chloroform"])
    $ evidence.add_to_inventory(evids["Solution after Vortexing"])
    pause 1.0
    "Vortexed complete!"
    hide phen2
    jump laboratory

label centrifuge:
    "We need to centrifuge it for 5 minutes at 13000 rpm."
    $ temp = renpy.input("What speed should we spin it at?", allow=set("0123456789"))
    if temp == "13000":
        $ time = renpy.input("How long in minutes should we spin it for?", allow=set("0123456789"))
        if time == "5":
            'Great! Now we have to wait.'
            pause 0.5
            "It should be done. Go ahead and take it out!"
            $ step = 6
            $ evidence.delete_from_inventory(evids["Solution after Vortexing"])
            $ evidence.add_to_inventory(evids["Solution after First Centrifuging"])
            show phen3 zorder 10000
            pause 1.0
            $ toolbox.add_to_inventory(tools["Pipette"])
            jump laboratory
        else:
            "Wrong time."
            jump centrifuge
    else:
        'Wrong temperature.'
        jump centrifuge

label pipette_use_label:
    "Let's transfer the aqueous layer..."
    show pipe1 zorder 10000
    pause 0.7
    hide pipe1
    show pipe2 zorder 10000
    pause 0.7
    hide pipe2
    show pipe3 zorder 10000
    pause 0.7
    hide pipe3
    show aqueuos zorder 10000
    pause 0.4
    hide aqueuos
    $ step = 7
    $ evidence.delete_from_inventory(evids["Solution after First Centrifuging"])
    $ evidence.add_to_inventory(evids["Solution after Pipetting"])
    $ toolbox.delete_from_inventory(tools["Pipette"])
    $ toolbox.add_to_inventory(tools["Ethanol"])
    jump laboratory

label e_use_label:
    "We need 2.5x a volume of ethanol. We have 1.3 volume in our tube."
    $ amt = renpy.input("How much ethanol do we need?", allow=set(".0123456789"))
    if amt == "3.25":
        "Perfect!"
        show aqueuos zorder 10000
        pause 0.7
        hide aqueuos
        show eth1 zorder 10000
        pause 0.7
        hide eth1
        $ step = 8
        $ evidence.delete_from_inventory(evids["Solution after Pipetting"])
        $ evidence.add_to_inventory(evids["Solution after Ethanol"])
        $ toolbox.delete_from_inventory(tools["Ethanol"])
        jump laboratory
    else:
        "That's the wrong amount."
        jump e_use_label

label freezer:
    "We need to freeze it at -30 degrees celsius for 30 minutes."
    $ temp = renpy.input("What temperature should we freeze it at?", allow=set("-0123456789"))
    if temp == "-30":
        $ time = renpy.input("How long in minutes should we freeze it for?", allow=set("0123456789"))
        if time == "30":
            'Great! Now we have to wait.'
            $ freezing = True
            show closed zorder 10000:
                xpos 1400
                ypos 500
            pause 1.0
            "It should be done. Go ahead and take it out!"
            hide closed
            $ freezing = False
            show eth2
            pause 0.7
            hide eth2
            $ evidence.delete_from_inventory(evids["Solution after Ethanol"])
            $ evidence.add_to_inventory(evids["Solution after Freezing"])
            $ toolbox.add_to_inventory(tools["TE Buffer"])
            $ step = 9
            jump laboratory
        else:
            "Wrong time."
            jump freezer
    else:
        'Wrong temperature.'
        jump freezer

label te_use_label:
    "We need 0.02 ml of TE Buffer."
    $ amt = renpy.input("How much TE Buffer do we need?", allow=set(".0123456789"))
    if amt == "0.02":
        "Perfect!"
        show eth2 zorder 10000
        pause 0.7
        hide eth2
        show pcr zorder 10000
        pause 0.7
        hide pcr
        $ step = 10
        $ evidence.delete_from_inventory(evids["Solution after Freezing"])
        $ evidence.add_to_inventory(evids["Solution after TE Buffer"])
        $ toolbox.delete_from_inventory(tools["TE Buffer"])
        if active_swab == "wall":
            $ wall_done = True
        else:
            $ floor_done = True
        $ active_swab = None
        $ lysis_done = False
        $ protein_done = False
        "Your solution is ready for DNA analysis!"
        jump game
    else:
        "That's the wrong amount."
        jump te_use_label