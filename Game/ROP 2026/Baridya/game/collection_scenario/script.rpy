default default_mouse = "default"

################################################################################
## Custom cursors
################################################################################
## Full set matching the source lab project's own config.mouse. Registers
## a state only if its file actually exists yet, so this can never crash
## at startup regardless of which cursor art has been added so far --
## Ren'Py preloads config.mouse["default"] during its own startup GL test,
## before any of our game code runs, so a missing file there is otherwise
## a hard crash at launch.
init python:
    if config.mouse is None:
        config.mouse = {}

    _cursor_files = {
        "default": ("images/ui/cursors/cursor.png", 0, 0),
        "pointer": ("images/ui/cursors/cursor.png", 0, 0),
        "magnifying": ("images/ui/cursors/default_cursor.png", 0, 0),
        "hover": ("images/ui/cursors/hover_cursor.png", 0, 0),
        "dropper": ("images/ui/cursors/dropper.png", 0, 49),
        "ethanol": ("images/ui/cursors/dropper_filled.png", 0, 49),
        "hand": ("images/ui/cursors/default_hand.png", 0, 0),
        "hand_grab": ("images/ui/cursors/grab_hand.png", 0, 0),
        "micropipette": ("images/ui/cursors/micropipette.png", 10, 10),
    }
    for _cursor_name, (_cursor_path, _hot_x, _hot_y) in _cursor_files.items():
        if renpy.loadable(_cursor_path):
            config.mouse[_cursor_name] = [(_cursor_path, _hot_x, _hot_y)]


init python:
    import json

    ################################################################################
    ## Gloves
    ################################################################################
    ## Adapted from the source project's _glove_animation (bare hands rise,
    ## swap to gloved hands, slide back down) -- but triggered by clicking
    ## the hands directly instead of the source's drag-a-box-onto-hands
    ## system, which we don't have. Worn twice per playthrough: once before
    ## the door handle, once before anything in the lab -- gloves_worn gets
    ## reset to False at the start of each of those two gates, so both
    ## require a fresh glove-up.
    ##
    ## IMPORTANT: this has to be defined before load_items() runs below --
    ## the JSON loader resolves the "action" string straight to a function
    ## by name at load time, so if use_gloves isn't defined yet when
    ## toolbox.json is parsed, the Gloves item silently ends up with no
    ## working action at all.

    gloves_worn = False
    _glove_return_label = None

    def get_toolbox_item(name):
        for item in toolbox._inventory:
            if item.name == name:
                return item
        return None

    def use_gloves():
        """The Gloves toolbox item's action. Safe to call from inside the
        inventory screen's own interaction -- see the magnetic powder quiz
        for why call_in_new_context is required here."""
        global gloves_worn
        if renpy.call_in_new_context("glove_up_sequence"):
            gloves_worn = True
            renpy.hide_screen("inventory")
            renpy.notify("Gloves on.")
            ## Disable so it can't be clicked again until the next gate
            ## explicitly re-enables it -- otherwise it stays clickable
            ## through the rest of evidence collection, which is what was
            ## causing the repeated glove-up bugs.
            _gloves_item = get_toolbox_item("Gloves")
            if _gloves_item:
                _gloves_item.usable = False
            if _glove_return_label:
                renpy.jump(_glove_return_label)

    def has_gloves_item():
        """False until 'Gloves' is actually added to toolbox.json -- lets
        the two gates below skip themselves gracefully instead of soft-
        locking on an item that can't exist yet."""
        return any(item.name == "Gloves" for item in toolbox._inventory)

    tools = load_items("jsons/toolbox.json")
    toolbox.add_to_inventory(tools["Evidence Bag"])
    toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    toolbox.add_to_inventory(tools["Tube"])
    toolbox.add_to_inventory(tools["Swab Pack"])
    toolbox.add_to_inventory(tools["Backing Card"])
    toolbox.add_to_inventory(tools["Magnetic Powder"])
    toolbox.add_to_inventory(tools["Tape"])
    toolbox.add_to_inventory(tools["Scalebar"])
    if "Gloves" in tools:
        toolbox.add_to_inventory(tools["Gloves"])
        ## Force these directly rather than trusting the JSON's "usable"/
        ## "action" fields resolved correctly -- guarantees this works
        ## regardless of what's actually in toolbox.json right now.
        tools["Gloves"].usable = True
        tools["Gloves"].action = use_gloves

transform glove_rise:
    xalign 0.5
    yanchor 1.0
    ypos 1.3
    linear 0.6 ypos 1.0

transform glove_settle:
    xalign 0.5
    yanchor 1.0
    ypos 1.0
    linear 0.4 ypos 1.3

screen glove_click_prompt():
    modal True
    add Solid("#000000aa")
    imagebutton:
        idle "hands"
        hover "hands"
        at glove_rise
        action Return()

label glove_up_sequence:
    show nina talk
    n "Click your hands to put your gloves on."
    call screen glove_click_prompt
    show gloved_hands at glove_rise
    pause 0.8
    show gloved_hands at glove_settle
    pause 0.4
    hide gloved_hands
    hide nina with dissolve
    return True


init python:
    def item_dragged_package(drags, drop):
        global default_mouse
        default_mouse = "hand_grab"

        if not drop:
            default_mouse = "hand"
            return

        store.dragged = drags[0].drag_name
        store.dropped = drop.drag_name
        default_mouse = "default"

        if store.dropped != "bag" and store.dragged != "bag":
            return True

        if renpy.get_screen("drag_to_bag"):
            renpy.hide_screen("drag_to_bag")
            renpy.hide_screen("inventory")
            if store.active_process is not None:
                store.active_process.advance()
                renpy.notify("Now seal the bag with tape.")
                renpy.invoke_in_new_context(renpy.call_screen, "drag_tape_to_bag")

        elif renpy.get_screen("drag_tape_to_bag"):
            renpy.hide_screen("drag_tape_to_bag")
            if store.active_process is not None:
                store.active_process.advance()  # triggers on_complete internally

        return True


define n = Character(name=("Nina"), image="nina")

label start:
    $ evidence.reset_inventory()
    $ fingerprint_process.reset()
    $ can_print_process.reset()
    $ can_dna_process.reset()
    $ can_whole_process.reset()
    $ wheel_print_process.reset()
    $ wheel_dna_process.reset()
    $ active_process = None
    $ did_can = False
    $ can_done = False
    $ wheel_done = False
    $ visited_can = False
    $ visited_wheel = False
    $ visited_interior = False
    scene bg_dispatch with fade
    show nina normal1 at center with moveinright
    n "We have a critical situation. Dispatch logged a forced carjacking; the vehicle owner was hospitalized with severe injuries, and the perpetrator fled the scene."
    show nina talk
    n "The vehicle was located abandoned in a commercial parking lot."
    show nina thinknote1
    n "The MO aligns closely with an active serial carjacking investigation targeting high-end vehicles."
    n "We need to process this scene immediately to establish if the perpetrator is indeed our primary suspect, known as the \"Pontiac Bandit.\""
    hide nina with dissolve
    jump scene_parking


label scene_parking:
    scene bg_parking_lot with fade
    show nina talk
    show nina thinknote1 at right
    n "Click the licence plate on the vehicle to run the plates first."
    hide nina with dissolve
    call screen parking_screen

screen parking_screen():
    imagemap:
        ground "images/backgrounds/bg_parking_lot.png"
        hover  "images/backgrounds/bg_parking_lot_hover.png"
        hotspot (620, 670, 90, 60) action Jump("ran_plates")

label ran_plates:
    show nina talk at right
    n "Plate verified. This is the victim's vehicle."
    n "This vehicle is now an active crime scene tied to a violent felony. Secure the perimeter and proceed with methodical documentation."
    $ gloves_worn = False
    jump glove_gate_field

label glove_gate_field:
    if gloves_worn or not has_gloves_item():
        jump scence_exterior
    $ _glove_return_label = "glove_gate_field"
    $ _gloves_item = get_toolbox_item("Gloves")
    if _gloves_item:
        $ _gloves_item.usable = True
    n "Let's get gloved up before we touch anything at this scene."
    call screen inventory
    jump glove_gate_field

label scence_exterior:
    scene bg_car_exterior with fade
    show screen field_notebook_icon
    show nina normal1 at right with moveinright
    n "Visual inspection of the exterior indicates the driver-side door handle remains untouched by emergency responders."
    n "This is a primary contact point for the suspect. We will attempt a latent print lift here. Click the door handle to isolate the area."
    hide nina with dissolve
    call screen car_exterior_screen


screen car_exterior_screen():
    imagemap:
        ground "images/backgrounds/bg_car_exterior.png"
        hover  "images/backgrounds/bg_car_exterior_hover.png"
        hotspot (1100, 660, 450, 150) action Jump("hotspot_door_handle")


label magnetic_powder_quiz:
    ## Run via renpy.call_in_new_context() from use_tool() in
    ## inventory_functions.rpy -- that's what lets a menu/dialogue pop up
    ## safely from inside a toolbox item's click action, without clashing
    ## with the inventory screen's already-running interaction. Returns
    ## True/False for whether the right answer was picked; use_tool()
    ## handles actually advancing the process based on that.
    ##
    ## Re-showing evidence_closeup_view here is deliberate: nested contexts
    ## via call_in_new_context don't reliably inherit persistent screens
    ## shown in the parent, which is why the background was flashing back
    ## to the real scene during this quiz before.
    ##
    ## show/hide nina here fixes a separate issue: Nina gets explicitly
    ## hidden right before the inventory loop starts, so without this,
    ## there's no character sprite currently shown for the dialogue box's
    ## side portrait to source from during this quiz.
    show screen evidence_closeup_view
    show nina talk
    n "What color powder should we use here?"
    menu:
        "White powder":
            n "White powder against a dark surface, that'll show up clearly."
            hide nina
            return True

        "Black powder":
            n "Black powder won't show up well against this surface. Let's try again."
            hide nina
            return False


label hotspot_door_handle:
    show nina talk at right
    if fingerprint_process.step_index == 0:
        call flash_camera
        n "Photo taken of the door handle."
        n "Access your field kit to begin processing the latent friction ridges on the surface."
    $ active_process = fingerprint_process
    show screen evidence_closeup_view
    hide nina with dissolve
    call screen inventory
    if fingerprint_process.complete:
        hide screen evidence_closeup_view
        jump fingerprint_complete
    jump hotspot_door_handle


label fingerprint_complete:
    show nina thinknote1 at right
    n "The latent print is successfully lifted, mounted on a backing card, and sealed."
    n "Let's take a look at the interior now."
    jump scene_interior

label scene_interior:
    if did_can:
        scene bg_car_interior_no_soda with fade
    else:
        scene bg_car_interior with fade
    if not visited_interior:
        $ visited_interior = True
        show nina normal1 at right with moveinright
        n "The interior environment is preserved. We need to locate and isolate high-contact surfaces where biological or friction ridge evidence could transfer."
        n "Methodically scan the cabin. Photograph all evidence in situ before executing collection protocols."
        n "Click on any evidence to take a photo and examine it."
    call screen car_interior_screen

label hotspot_soda_can:
    show nina talk at right
    if not visited_can:
        $ visited_can = True
        call flash_camera
        n "Photo taken of the soda can."
        n "This object represents a dual-matrix evidence source: latent prints on the body and potential salivary DNA on the rim."

label can_menu:
    menu:
        "Select the forensic processing protocol you want for the beverage container:"

        "Dust for fingerprints" if not can_print_process.complete and not can_whole_process.complete:
            $ active_process = can_print_process
            show screen evidence_closeup_view
            call screen inventory
            if can_print_process.complete:
                hide screen evidence_closeup_view
            jump can_menu

        "Swab for DNA" if not can_dna_process.complete and not can_whole_process.complete:
            $ active_process = can_dna_process
            show screen evidence_closeup_view
            call screen inventory
            if can_dna_process.complete:
                hide screen evidence_closeup_view
            jump can_menu

        "Collect the whole can" if not can_whole_process.complete:
            $ active_process = can_whole_process
            call screen inventory
            jump can_menu

        "Move on" if (can_print_process.complete or can_dna_process.complete or can_whole_process.complete):
            $ can_done = True
            if can_done and wheel_done:
                jump scene_wrap_up
            jump scene_interior

label hotspot_steering_wheel:
    show nina talk at right
    if not visited_wheel:
        $ visited_wheel = True
        call flash_camera
        n "Photo taken of the steering wheel. Plenty of trace evidence here."
        n "The steering wheel substrate is highly conducive to trapping epithelial cells via friction, though it often yields complex, overlapping mixtures."

label wheel_menu:
    menu:
        "Select the appropriate forensic processing protocol for the steering wheel:"

        "Dust for fingerprints" if not wheel_print_process.complete:
            $ active_process = wheel_print_process
            show screen evidence_closeup_view
            call screen inventory
            if wheel_print_process.complete:
                hide screen evidence_closeup_view
            jump wheel_menu

        "Swab for DNA" if not wheel_dna_process.complete:
            $ active_process = wheel_dna_process
            show screen evidence_closeup_view
            call screen inventory
            if wheel_dna_process.complete:
                hide screen evidence_closeup_view
            jump wheel_menu

        "Move on" if (wheel_print_process.complete or wheel_dna_process.complete):
            $ wheel_done = True
            if can_done and wheel_done:
                jump scene_wrap_up
            jump scene_interior

screen car_interior_screen():
    imagemap:
        ground ("images/backgrounds/bg_car_interior_no_soda.png" if did_can else "images/backgrounds/bg_car_interior.png")
        hover  ("images/backgrounds/bg_car_interior_hover_wheel_no_soda.png" if did_can else "images/backgrounds/bg_car_interior_hover_wheel.png")
        hotspot (20, 180, 610, 670) action Jump("hotspot_steering_wheel") sensitive (not wheel_done)

    imagemap:
        ground Null()
        hover  "images/backgrounds/bg_car_interior_hover_can.png"
        hotspot (1070, 795, 100, 180) action Jump("hotspot_soda_can") sensitive (not can_done)

label scene_wrap_up:
    scene bg_parking_lot with fade
    hide screen field_notebook_icon
    hide screen field_notebook_panel
    show nina normal1 at right with dissolve
    n "Let us review the field documentation and collection sequence before transport:"
    show nina thinknote1 at right
    n "Scene Documentation: Photographic evidence of each item was captured in situ with an appropriate scale bar prior to handling."
    n "Latent Fingerprints: Developed using physical developer, documented with a scale bar, lifted with tape, and secured on a high-contrast backing card."
    n "Biological Materials: Swabbed high-contact areas, focusing on the can rim for salivary epithelial cells to generate an STR profile."
    n "Chain of Custody: Chronological tracking log has been signed, ensuring a continuous, unbroken chain. The integrity of the physical evidence is intact."
    show nina normal1 at right
    n "These are the core steps of physical evidence collection from a vehicle scene."
    n "Transport all sealed packets to the lab for diagnostic analysis."
    hide nina with dissolve
    jump scene_lab


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
    _robber_name = "Denise Cole"
    _owner_name = "Patricia Nguyen"

    ## print_5 and print_6 are both booking-card scans of the SAME finger --
    ## the robber's, taken at two different arrests -- so print_6 is set to
    ## reuse print_5's actual image file below. That's what guarantees they
    ## look identical, not just that they're flagged as a match in code.
    ##
    ## The real matches (robber x2, elimination x1) are deliberately placed
    ## at the END of the browsable deck (print_4/5/6), with pure decoys at
    ## print_1/2/3, so the default starting card is never a match and the
    ## player actually has to browse the whole database instead of winning
    ## on the very first click.
    ROBBER_PRINT_KEYS = ["print_5", "print_6"]
    ELIMINATION_PRINT_KEY = "print_4"

    class AfisMCQ(object):
        """
        A multiple-choice pattern-matching question, asked about a database
        print's ridge pattern (whorl/loop/arch/etc.) after Compare and
        before the match result -- teaches the player to actually look at
        what's on screen instead of just clicking through. Answering wrong
        loops the question again instead of moving on.

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
        # key: (image asset to use, description)
        "print_1": ("print_3", "Unrelated record on file, not connected to this case."),
        "print_2": ("print_2", "Unrelated record on file, not connected to this case."),
        "print_3": ("print_7", "Unrelated record on file, not connected to this case."),
        "print_4": ("print_6", "Elimination print on file for %s, the car's registered owner." % _owner_name),
        "print_5": ("print_1", "Booking record from an arrest two years ago: %s." % _robber_name),
        "print_6": ("print_1", "A second booking record, eight months ago: %s again." % _robber_name),
    }

    ## Pattern-matching quiz per database card, asked after Compare and
    ## before the result. Keyed by which IMAGE each slot actually shows
    ## (per DB_PRINT_INFO above), since the question is about what's
    ## visually on screen, not the slot number.
    DB_PRINT_MCQS = {
        "print_5": AfisMCQ(
            question="Examine the core and delta positioning. What is the primary ridge classification?",
            choices=[("Loop", False), ("Arch", False), ("Whorl", True)],
            responses=[
                ["That's not a loop pattern.", "Take another look."],
                ["That's not an arch pattern.", "Take another look."],
                ["That's a whorl, the ridges circle back on themselves.", "Let's finish the comparison."],
            ],
        ),
        "print_4": AfisMCQ(
            question="Identify the ridge flow pattern shown in this sample.",
            choices=[("Whorl", False), ("Loop", True), ("Arch", False)],
            responses=[
                ["That's not a whorl pattern.", "Take another look."],
                ["That's a loop, the ridges curve and come back out the same side.", "Let's finish the comparison."],
                ["That's not an arch pattern.", "Take another look."],
            ],
        ),
        "print_1": AfisMCQ(
            question="Classify the friction ridge pattern displayed below.",
            choices=[("Arch", True), ("Whorl", False), ("Loop", False)],
            responses=[
                ["That's an arch, the ridges rise in the middle with no backward turn.", "Let's finish the comparison."],
                ["That's not a whorl pattern.", "Take another look."],
                ["That's not a loop pattern.", "Take another look."],
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
    }
    DB_PRINT_MCQS["print_6"] = DB_PRINT_MCQS["print_5"]  # shares print_5's image

    ## Every imported print reuses a database card's image, since it's meant
    ## to be an actual finger already in one of those records -- not a new
    ## unknown person. Which one depends on WHERE it was lifted from:
    ##   - steering wheel  -> the owner's print (elimination, print_4)
    ##   - anything else (door handle, can, ...) -> the robber's print (print_5)
    ## Add more entries to PRINT_SOURCE_RULES below if you add more pickup
    ## spots later (each entry is (keyword-in-item-name, db_key)).
    PRINT_SOURCE_RULES = [
        ("wheel", "print_4"),
    ]
    PRINT_SOURCE_DEFAULT_DB_KEY = "print_5"

    ## Map specific evidence item names to dedicated AFIS card art, if/when
    ## you make some. Anything collected that isn't listed here falls back
    ## to the rule above.
    PRINT_EVIDENCE_IMAGES = {
        # "Fingerprint": "afis-print-door-handle",
        # "Can Fingerprint": "afis-print-can",
        # "Wheel Fingerprint": "afis-print-wheel",
    }

    ## Only evidence items whose name contains one of these (case-insensitive)
    ## are treated as importable prints in the AFIS terminal.
    PRINT_NAME_KEYWORDS = ["print", "fingerprint"]

    ## Score every imported print against each database card. True/False
    ## marks whether it's a match; the number is the displayed consistency %.
    ROBBER_SOURCE_SCORES = {
        "print_1": (False, 18),
        "print_2": (False, 24),
        "print_3": (False, 15),
        "print_4": (False, 9),
        "print_5": (True, 96),
        "print_6": (True, 91),
    }
    OWNER_SOURCE_SCORES = {
        "print_1": (False, 17),
        "print_2": (False, 22),
        "print_3": (False, 16),
        "print_4": (True, 94),
        "print_5": (False, 11),
        "print_6": (False, 13),
    }

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
        <image>_closeup_1/2/3.png files exist in DATA_LAB_DIR -- same
        detection technique your source lab's afis.rpy used."""
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
    afis_active = False        # True only while the terminal is open
    imported_print = None      # key into afis_prints, set by importing evidence
    print_imported = False     # has anything been imported yet this session
    current_db_print = 1       # 1..NUM_DB_PRINTS, which database card is shown
    afis_import_keys = []      # keys of every importable print discovered this visit
    _compare_left_img = None   # currently-shown image in the compare view's left slot
    _compare_right_img = None  # currently-shown image in the compare view's right slot

    def is_print_evidence(item):
        name_lower = item.name.lower()
        return any(k in name_lower for k in PRINT_NAME_KEYWORDS)

    def get_print_evidence_items():
        """All collected evidence items that look like fingerprints."""
        return [item for item in evidence._inventory if is_print_evidence(item)]

    def slugify_print_key(name):
        cleaned = "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")
        return "print_evidence_%s" % cleaned

    def resolve_print_source(item):
        """Decides which database card (and therefore whose scores/image)
        an evidence item's print should be treated as, based on a keyword
        in its name. Falls through to PRINT_SOURCE_DEFAULT_DB_KEY."""
        name_lower = item.name.lower()
        for keyword, db_key in PRINT_SOURCE_RULES:
            if keyword in name_lower:
                return db_key
        return PRINT_SOURCE_DEFAULT_DB_KEY

    def register_importable_print(item):
        """Ensures there's an AfisPrint entry for this evidence item, and
        returns its key. Safe to call repeatedly -- won't wipe out a card
        that's already been processed."""
        key = slugify_print_key(item.name)
        if key not in afis_prints:
            source_db_key = resolve_print_source(item)
            default_image = DB_PRINT_INFO[source_db_key][0]
            default_scores = OWNER_SOURCE_SCORES if source_db_key == ELIMINATION_PRINT_KEY else ROBBER_SOURCE_SCORES
            image = PRINT_EVIDENCE_IMAGES.get(item.name, default_image)
            afis_prints[key] = make_afis_print(
                image,
                description="The %s." % item.name.lower(),
                scores=dict(default_scores),
            )
        return key

    def make_afis_import_action(print_key):
        """Wired onto an evidence item's .action while the AFIS terminal is
        open, so clicking 'Use' on it in the inventory imports it."""
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
        $ lab_fingerprint_done = True
        $ afis_prints[imported_print].process()
        n "Search complete. The AFIS algorithm reports an optimal minutiae configuration match."
        n "Confirming match. The minutiae points match a record within our active database: [afis_prints[_db_key].description]."
    else:
        if _db_key == ELIMINATION_PRINT_KEY:
            n "Search concluded. The configuration returned no corresponding profiles within the repository: [afis_prints[_db_key].description]."
            n "This exclusion is forensically valuable. It confirms the latent print does not belong to the victim, [_owner_name]."
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
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            action Jump("lab_fingerprint_station")
            hovered Notify("\u2713 Fingerprint Matched" if lab_fingerprint_done else "Data Analysis Lab")
            unhovered Notify("")

    ## Materials Lab -> DNA bio station (renamed "DNA Analysis Lab" in the
    ## hover tooltip only; the underlying art/asset name stays
    ## "materials_lab" since that's what the files are actually named)
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            action Jump("dna_lab_entry")
            hovered Notify("\u2713 DNA Matched" if lab_dna_done else "DNA Analysis Lab")
            unhovered Notify("")

    if lab_fingerprint_done and lab_dna_done:
        textbutton "Conclude Case":
            style "custom_button"
            xalign 0.5
            yalign 0.92
            action Jump("lab_conclusion")


################################################################################
## DNA Lab -- Bio Station
################################################################################
## Adapted from the source project's machines.rpy / custom_screens.rpy DNA
## pipeline. Everything in this section is prefixed dna_ so it's fully
## self-contained -- nothing here should ever need to touch AFIS, evidence
## collection, or anything outside this block, which is exactly what makes
## it safe to debug in isolation later.
##
## Two things were deliberately changed from the source:
##   1. Blood -> touch DNA in the narration only; the extraction chemistry
##      (lysis, ethanol precipitation, spin-column washes) is identical
##      regardless of sample type, so no mechanical changes were needed.
##   2. The three steps originally gated behind clicking "ethanol"/"tube"/
##      "trash" items in a different inventory system (which we don't have)
##      now auto-advance immediately after the step that unlocks them,
##      instead of requiring a separate tool click. Per your "keep it
##      simple" call.
##
## Both can + wheel swabs (if collected) lead into this same single
## procedure and the same result -- no per-swab branching, as requested.
##
## ASSET REQUIREMENTS: this reuses the source project's exact filenames
## (backgrounds/bio_station.png, objects/swab.png, etc.) verbatim, since
## you already have that art. If any path doesn't match your actual folder
## layout, it's a one-line fix wherever that string appears below.
################################################################################

init -5 python:

    ## Which evidence items count as a DNA swab.
    DNA_NAME_KEYWORDS = ["swab", "dna"]

    def has_dna_evidence():
        for item in evidence._inventory:
            name_lower = item.name.lower()
            if any(k in name_lower for k in DNA_NAME_KEYWORDS):
                return True
        return False

    ## Swab prep checklist -- every extraction step, in order.
    dna_swab_tasks = {
        "swab_is_cut": False,
        "swab_is_prepped": False,
        "swab_is_vortexed": False,
        "swab_is_incubated": False,
        "swab_is_spun": False,
        "swab_new_tube": False,
        "sample_is_spun": False,
        "sample_new_tube": False,
    }

    ## Bigger milestones -- gate the qPCR machine and the final result.
    dna_tasks = {
        "Prep swab for DNA analysis": False,
        "Run qPCR machine": False,
        "Analyze DNA results": False,
    }

    ## One-off flags used partway through the sequence (names kept close to
    ## the source so its branching logic ports over unchanged).
    dna_swab_is_vortexed_2 = False
    dna_swab_is_incubated_0 = False
    dna_ethanol_added = False
    dna_tube_transfered = False

    ## The quantification tray.
    dna_tray_top_filled = False
    dna_tray_bottom_filled = False
    dna_tray_side_filled = False
    dna_tray_prepped = False
    dna_tray_placements = {
        "top": "reaction_mix",
        "bottom": "diluted_dna",
        "side": "nuclease_free_water",
    }

    ## Lab toolbox -- completely separate from the field evidence toolbox.
    ## Only exists while working the DNA bio station, and only ever
    ## contains these 3 items, matching the source project's ethanol/tube/
    ## trash inventory steps.
    lab_toolbox = Inventory()

    def dna_use_ethanol():
        if dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated"]) and not dna_ethanol_added:
            renpy.jump("dna_add_ethanol")
        else:
            dna_notify_msg("Nothing to add ethanol to yet.", correct=False)

    def dna_use_tube():
        if dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated", "swab_is_spun"]) and not dna_swab_tasks["swab_new_tube"]:
            renpy.jump("dna_new_tube")
        else:
            dna_notify_msg("No sample ready to transfer yet.", correct=False)

    def dna_use_trash():
        if dna_swab_tasks["sample_is_spun"] and not dna_swab_tasks["sample_new_tube"]:
            renpy.jump("dna_discard_sample")
        else:
            dna_notify_msg("Nothing to discard yet.", correct=False)

    def dna_setup_lab_toolbox():
        """Populates the lab toolbox fresh. Safe to call every time the DNA
        lab is entered -- these 3 items never change."""
        lab_toolbox.reset_inventory()
        lab_toolbox.add_to_inventory(Item("Ethanol", "lab-ethanol", usable=True, action=dna_use_ethanol))
        lab_toolbox.add_to_inventory(Item("Tube", "lab-tube", usable=True, action=dna_use_tube))
        lab_toolbox.add_to_inventory(Item("Trash", "lab-trash", usable=True, action=dna_use_trash))

    ## Retractable notebook state.
    dna_notebook_clicked = False       # has the notebook icon ever been clicked

    def dna_toggle_screen(name):
        if renpy.get_screen(name):
            renpy.hide_screen(name)
        else:
            renpy.show_screen(name)

    def dna_toggle_notebook():
        global dna_notebook_clicked
        dna_notebook_clicked = True
        dna_toggle_screen("dna_notebook_panel")

    def dna_reset():
        global dna_swab_is_vortexed_2, dna_swab_is_incubated_0, dna_ethanol_added, dna_tube_transfered
        global dna_tray_top_filled, dna_tray_bottom_filled, dna_tray_side_filled, dna_tray_prepped
        for k in dna_tasks:
            dna_tasks[k] = False
        for k in dna_swab_tasks:
            dna_swab_tasks[k] = False
        dna_swab_is_vortexed_2 = False
        dna_swab_is_incubated_0 = False
        dna_ethanol_added = False
        dna_tube_transfered = False
        dna_tray_top_filled = False
        dna_tray_bottom_filled = False
        dna_tray_side_filled = False
        dna_tray_prepped = False

    def dna_check_task_complete(task_list):
        return all(dna_swab_tasks.get(t, True) for t in task_list)

    def dna_notify_msg(msg, correct=True):
        renpy.show_screen("dna_notify", message=msg, correct=correct)

    def dna_item_dragging_package(drags):
        global default_mouse
        default_mouse = "hand_grab"

    def dna_item_dragged_package(drags, drop):
        global default_mouse, dna_tray_top_filled, dna_tray_bottom_filled, dna_tray_side_filled
        default_mouse = "hand_grab"
        if not drop:
            default_mouse = "hand"
            return None

        if drop.drag_name == "top":
            dna_tray_top_filled = True
            dna_notify_msg("Top filled!", correct=True)
        elif drop.drag_name == "bottom":
            dna_tray_bottom_filled = True
            dna_notify_msg("Bottom filled!", correct=True)
        elif drop.drag_name == "side":
            dna_tray_side_filled = True
            dna_notify_msg("Side filled!", correct=True)

        renpy.restart_interaction()

        if drop.drag_name in dna_tray_placements:
            dna_tray_placements[drop.drag_name] = drags[0].drag_name

        default_mouse = "default"
        return None

    def dna_check_tray_placements():
        global dna_tray_prepped
        if not (dna_tray_top_filled and dna_tray_bottom_filled and dna_tray_side_filled):
            dna_notify_msg("Place all required components on the tray", correct=False)
            return

        correct = True
        messages = []

        if dna_tray_placements.get("top") != "reaction_mix":
            correct = False
            messages.append("You need to place the reaction mix at the top")
        if dna_tray_placements.get("bottom") != "diluted_dna":
            correct = False
            messages.append("You need to place the diluted extracted DNA at the bottom")
        if dna_tray_placements.get("side") != "nuclease_free_water":
            correct = False
            messages.append("You need to place the negative control (nuclease-free water) at the side")

        if correct:
            dna_notify_msg("All tray placements are correct!", correct=True)
            dna_tray_prepped = True
            renpy.jump("dna_bio_station")
        else:
            for message in messages:
                dna_notify_msg(message, correct=False)


################################################################################
## DNA screens
################################################################################

screen dna_notify(message, correct):
    zorder 200
    frame:
        xalign 0.5
        yalign 0.08
        background Solid("#1a7a3ae6" if correct else "#7a1a1ae6")
        padding (24, 14)
        text message size 26 color "#ffffff"
    timer 2.0 action Hide("dna_notify")


screen dna_lab_toolbox():
    zorder 90
    vbox:
        xalign 0.02
        yalign 0.5
        spacing 24

        for _lab_item in lab_toolbox._inventory:
            fixed:
                xysize (110, 110)

                add "inventory-slot"
                add _lab_item.image_name:
                    zoom 0.45
                    xoffset 18
                    yoffset 18

                button:
                    xysize (110, 110)
                    background None
                    action Function(_lab_item.action)

                text _lab_item.name:
                    xalign 0.5
                    yalign 1.0
                    size 16
                    color "#ffffff"


screen dna_notebook_icon():
    zorder 110
    imagebutton:
        idle (Animation("images/ui/notebook_icon.png", 0.5, "images/ui/notebook_icon_hover.png", 0.5) if not dna_notebook_clicked else "images/ui/notebook_icon.png")
        hover "images/ui/notebook_icon_hover.png"
        xpos 1830 ypos 20
        at Transform(zoom=0.15)
        action Function(dna_toggle_notebook)


screen dna_notebook_panel():
    zorder 100
    add "images/ui/dna_notebook.png":
        xalign 0.92
        yalign 0.02


################################################################################
## Field notebook -- same idea as the DNA lab one, for the evidence
## collection phase (door handle / can / wheel).
################################################################################

init python:
    field_notebook_clicked = False

    def field_toggle_notebook():
        global field_notebook_clicked
        field_notebook_clicked = True
        dna_toggle_screen("field_notebook_panel")

screen field_notebook_icon():
    zorder 110
    imagebutton:
        idle (Animation("images/ui/notebook_icon.png", 0.5, "images/ui/notebook_icon_hover.png", 0.5) if not field_notebook_clicked else "images/ui/notebook_icon.png")
        hover "images/ui/notebook_icon_hover.png"
        xpos 1830 ypos 20
        at Transform(zoom=0.15)
        action Function(field_toggle_notebook)

screen field_notebook_panel():
    zorder 100
    add "images/ui/field_notebook.png":
        xalign 0.92
        yalign 0.02


screen dna_bio_station():
    imagemap:
        idle "backgrounds/bio_station.png"
        hover "backgrounds/bio_station_hover.png"

        hotspot (811, 411, 229, 290) action Jump("dna_use_qpcr")
        hotspot (1040, 460, 241, 212) action Jump("dna_use_centrifuge")
        hotspot (1276, 417, 174, 257) action Jump("dna_use_spinner")
        hotspot (1458, 475, 126, 228) action Jump("dna_use_vortex")
        hotspot (1594, 571, 184, 174) action Jump("dna_use_incubator")
        hotspot (1634, 455, 228, 135) action Jump("dna_use_prep")

    textbutton "Back to Lab":
        xalign 0.02
        yalign 0.95
        background Solid("#000000aa")
        xpadding 20
        ypadding 10
        action Jump("dna_exit")


screen dna_swab_screen():
    zorder 1
    modal True

    imagemap:
        ground "backgrounds/swab_screen.png"
        idle "backgrounds/swab_screen_idle.png"
        hover "backgrounds/swab_screen_hover.png"

        hotspot (84, 178, 349, 727):
            action SetDict(dna_swab_tasks, "swab_is_cut", True)
        hotspot (488, 333, 767, 516):
            action Function(
                lambda:
                    dna_notify_msg("You need to cut the swab first...", correct=False)
                    if not dna_check_task_complete(["swab_is_cut"])
                    else renpy.store.__setattr__("default_mouse", "micropipette")
            )

    if dna_check_task_complete(["swab_is_prepped"]):
        add "objects/cut_swab_filled.png" pos (1400, 250)
    elif dna_check_task_complete(["swab_is_cut"]):
        add "objects/cut_swab.png" pos (1400, 250)
    else:
        add "objects/swab.png" pos (1500, 200)

    if default_mouse == "micropipette":
        imagebutton:
            xpos 1450
            ypos 200
            idle "images/ui/transparent.png"
            hover "images/ui/transparent.png"
            mouse "micropipette"
            action [
                SetDict(dna_swab_tasks, "swab_is_prepped", True),
                SetVariable("default_mouse", "default"),
                Show("dna_notify", message="Swab extraction phase initiated.", correct=True),
                Return(),
            ]

    textbutton "Close":
        action Return()
        align (0.0, 0.0)
        xpadding 30
        ypadding 10
        background Solid("#2a2a2ae6")
        hover_background Solid("#4a90d9")
        text_color "#ffffff"
        text_hover_color "#ffffff"


screen dna_centrifuge():
    zorder 99
    modal True

    imagemap:
        ground "backgrounds/use_centrifuge.png"
        idle "backgrounds/use_centrifuge.png"
        hover "backgrounds/use_centrifuge_hover.png"

        hotspot (784, 295, 349, 335):
            action If(
                dna_check_task_complete([
                    "swab_is_cut", "swab_is_prepped", "swab_is_vortexed",
                    "swab_is_incubated", "swab_is_spun", "swab_new_tube",
                ]),
                [SetDict(dna_swab_tasks, "sample_is_spun", True),
                 Show("dna_notify", message="Centrifuge cycle complete.", correct=True),
                 Jump("dna_wait_screen")],
                [Show("dna_notify", message="Protocol error: Incorrect step order.", correct=False), Return()],
            )


screen dna_spinner():
    zorder 99
    modal True

    imagemap:
        ground "backgrounds/use_spinner.png"
        idle "backgrounds/use_spinner.png"
        hover "backgrounds/use_spinner_hover.png"

        hotspot (810, 559, 350, 327):
            action [
                If(
                    dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated"]) and dna_swab_is_vortexed_2,
                    SetDict(dna_swab_tasks, "swab_is_spun", True),
                    If(
                        dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed"]) and dna_swab_is_incubated_0,
                        SetDict(dna_swab_tasks, "swab_is_incubated", True),
                        [Show("dna_notify", message="Protocol error: Incubation skipped out of sequence.", correct=False), Jump("dna_bio_station")],
                    ),
                ),
                Show("dna_notify", message="Separation column spun successfully.", correct=True),
                Return(),
            ]


screen dna_vortex():
    zorder 99
    modal True

    default vortex_clicked = False

    if not vortex_clicked:
        imagemap:
            ground "backgrounds/use_vortex.png"
            idle "backgrounds/use_vortex.png"
            hover "backgrounds/use_vortex_hover.png"

            hotspot (842, 429, 329, 552):
                action If(
                    dna_check_task_complete(["swab_is_cut", "swab_is_prepped"]),
                    SetScreenVariable("vortex_clicked", True),
                    [Show("dna_notify", message="Action error: Tube is empty. Nothing to vortex.", correct=False), Jump("dna_bio_station")],
                )
    else:
        imagemap:
            ground "backgrounds/vortex_swab.png"
            idle "backgrounds/vortex_swab.png"
            hover "backgrounds/vortex_swab_hover.png"

            hotspot (981, 695, 181, 180):
                action [
                    If(
                        dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated"]),
                        SetVariable("dna_swab_is_vortexed_2", True),
                        If(
                            dna_check_task_complete(["swab_is_cut", "swab_is_prepped"]),
                            SetDict(dna_swab_tasks, "swab_is_vortexed", True),
                        ),
                    ),
                    Show("dna_notify", message="Sample mixed. Vortexed for 15 seconds.", correct=True),
                    Return(),
                ]


screen dna_incubator():
    zorder 99
    modal True

    imagemap:
        ground "backgrounds/use_incubator.png"
        idle "backgrounds/use_incubator.png"
        hover "backgrounds/use_incubator_hover.png"

        hotspot (599, 157, 719, 815):
            action If(
                dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed"]),
                Jump("dna_incubator_question"),
                [Show("dna_notify", message="Action error: Incubator is empty. Load your sample.", correct=False), Jump("dna_bio_station")],
            )


screen dna_qpcr():
    zorder 99
    modal True

    imagemap:
        ground "backgrounds/use_qpcr.png"
        idle "backgrounds/use_qpcr.png"
        hover "backgrounds/use_qpcr_hover.png"

        hotspot (860, 561, 301, 156):
            action If(
                dna_tasks["Prep swab for DNA analysis"],
                Jump("dna_pcr"),
                [Show("dna_notify", message="Protocol error: Incorrect step order.", correct=False), Jump("dna_bio_station")],
            )


screen dna_cem_screen():
    zorder 99
    modal True

    imagemap:
        ground "backgrounds/cem_screen_idle.png"
        idle "backgrounds/cem_screen_idle.png"
        hover "backgrounds/cem_screen_hover.png"

        hotspot (486, 300, 140, 648):
            action Jump("dna_cem_finish")

    textbutton "Close":
        action Return()
        align (0.0, 0.0)
        xpadding 30
        ypadding 10
        background Solid("#2a2a2ae6")
        hover_background Solid("#4a90d9")
        text_color "#ffffff"
        text_hover_color "#ffffff"


screen dna_tray_drag():
    tag dna_tray_drag
    modal True
    add Solid("#000000cc")
    image "tray"

    draggroup:
        drag:
            drag_name "top"
            child ("tray_top_filled" if dna_tray_top_filled else "tray_top")
            xpos 590 ypos 170
            draggable False
            droppable True
            dragging dna_item_dragging_package
            dragged dna_item_dragged_package

        drag:
            drag_name "reaction_mix"
            child "textbox_1"
            xpos 300 ypos 890
            draggable True
            droppable True
            dragging dna_item_dragging_package
            dragged dna_item_dragged_package

    draggroup:
        drag:
            drag_name "nuclease_free_water"
            child "textbox_3"
            xpos 1300 ypos 890
            draggable True
            droppable True
            dragging dna_item_dragging_package
            dragged dna_item_dragged_package

        drag:
            drag_name "side"
            child ("tray_side_filled" if dna_tray_side_filled else "tray_side")
            xpos 510 ypos 170
            draggable False
            droppable True
            dragging dna_item_dragging_package
            dragged dna_item_dragged_package

    draggroup:
        drag:
            drag_name "bottom"
            child ("tray_bottom_filled" if dna_tray_bottom_filled else "tray_top")
            xpos 590 ypos 715
            draggable False
            droppable True
            dragging dna_item_dragging_package
            dragged dna_item_dragged_package

        drag:
            drag_name "diluted_dna"
            child "textbox_2"
            xpos 800 ypos 890
            draggable True
            droppable True
            dragging dna_item_dragging_package
            dragged dna_item_dragged_package

    textbutton "Reset":
        action [
            SetVariable("dna_tray_top_filled", False),
            SetVariable("dna_tray_bottom_filled", False),
            SetVariable("dna_tray_side_filled", False),
        ]
        xpos 0.1
        ypos 0.4
        xpadding 30
        ypadding 10
        background Solid("#2a2a2ae6")
        hover_background Solid("#4a90d9")
        text_color "#ffffff"
        text_hover_color "#ffffff"

    textbutton "Submit":
        action Function(dna_check_tray_placements)
        xpos 0.85
        ypos 0.4
        xpadding 30
        ypadding 10
        background Solid("#2a2a2ae6")
        hover_background Solid("#4a90d9")
        text_color "#ffffff"
        text_hover_color "#ffffff"

    textbutton "Close":
        action Jump("dna_bio_station")
        align (0.0, 0.0)
        xpadding 30
        ypadding 10
        background Solid("#2a2a2ae6")
        hover_background Solid("#4a90d9")
        text_color "#ffffff"
        text_hover_color "#ffffff"


################################################################################
## DNA labels -- entry / exit
################################################################################

label dna_lab_entry:
    hide screen inventory
    hide screen open_inv
    show nina thinknote1 at right
    if not has_dna_evidence():
        n "We can't extract DNA from thin air. Go back to the vehicle and collect a physical sample first."
        hide nina with dissolve
        jump lab_hub_loop
    $ dna_setup_lab_toolbox()
    show screen dna_lab_toolbox
    show screen dna_notebook_icon
    jump dna_bio_station

label dna_exit:
    hide screen dna_lab_toolbox
    hide screen dna_notebook_icon
    hide screen dna_notebook_panel
    hide nina with dissolve
    scene lab_hallway with dissolve
    jump lab_hub_loop

label dna_bio_station:
    python:
        if all(dna_swab_tasks.values()):
            dna_tasks["Prep swab for DNA analysis"] = True
    call screen dna_bio_station
    jump dna_bio_station


################################################################################
## DNA labels -- swab prep machines
################################################################################

label dna_use_prep:
    if dna_swab_tasks["swab_is_cut"] and dna_swab_tasks["swab_is_prepped"]:
        $ dna_notify_msg("Already prepped!", correct=False)
        jump dna_bio_station
    call screen dna_swab_screen
    jump dna_bio_station

label dna_use_vortex:
    if (dna_swab_is_incubated_0 and not dna_swab_tasks["swab_is_incubated"]) or dna_swab_tasks["swab_is_spun"]:
        $ dna_notify_msg("Protocol error: Incorrect step order.", correct=False)
        jump dna_bio_station
    call screen dna_vortex
    jump dna_bio_station

label dna_use_incubator:
    if dna_swab_tasks["swab_is_incubated"]:
        $ dna_notify_msg("Protocol error: Incorrect step order.", correct=False)
        jump dna_bio_station
    call screen dna_incubator
    jump dna_bio_station

label dna_incubator_question:
    scene use_incubator
    show nina thinknote1 at right
    n "Set the incubator temperature and timer for cell lysis:"
    menu:
        "37\u00b0C for 15 minutes":
            n "That temperature is too low. We need 56\u00b0C for 10 minutes to activate the Proteinase K enzyme and break open the cell membranes. Try again."
            jump dna_use_incubator

        "56\u00b0C for 10 minutes":
            $ dna_swab_is_incubated_0 = True
            jump dna_wait_screen

        "95\u00b0C for 5 minutes":
            n "Too hot. 95\u00b0C will destroy our active enzymes before they can do their job. Save that heat for the PCR machine later. Set it to 56\u00b0C."
            jump dna_use_incubator

label dna_use_spinner:
    if (dna_ethanol_added and not dna_swab_is_vortexed_2) or dna_swab_tasks["swab_is_spun"] or not dna_swab_is_incubated_0:
        $ dna_notify_msg("Protocol error: Incorrect step order.", correct=False)
        jump dna_bio_station
    call screen dna_spinner
    jump dna_bio_station

label dna_add_ethanol:
    $ dna_ethanol_added = True
    if dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated"]):
        scene add_ethanol_1
        pause 1.0
        scene add_ethanol_2
        pause 0.5
        scene add_ethanol_3
        pause 1.0
        scene add_ethanol_4
        pause 1.0
        $ dna_notify_msg("Added 400uL of ethanol!", correct=True)
    jump dna_bio_station

label dna_new_tube:
    if dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated", "swab_is_spun"]):
        scene new_tube_1
        pause 1.0
        scene new_tube_2
        pause 0.5
        scene new_tube_3
        pause 1.0
        $ dna_notify_msg("Transferred to a new 2mL tube!", correct=True)
        $ dna_tube_transfered = True
        $ dna_swab_tasks["swab_new_tube"] = True
    jump dna_bio_station

label dna_use_centrifuge:
    if dna_swab_tasks["sample_is_spun"]:
        $ dna_notify_msg("Protocol error: Incorrect step order.", correct=False)
        jump dna_bio_station
    call screen dna_centrifuge
    jump dna_bio_station

label dna_wait_screen:
    scene black with dissolve
    if dna_tasks["Prep swab for DNA analysis"]:
        show text "{color=#ffffff}We run the PCR machine...{/color}" at truecenter with dissolve
    elif dna_check_task_complete(["swab_new_tube"]):
        show text "{color=#ffffff}We spin at 6000 RCF for 1 minute...{/color}" at truecenter with dissolve
    else:
        show text "{color=#ffffff}We wait for 10 minutes...{/color}" at truecenter with dissolve
    pause 2.0
    hide text with dissolve
    jump dna_bio_station

label dna_discard_sample:
    if dna_check_task_complete(["swab_is_cut", "swab_is_prepped", "swab_is_vortexed", "swab_is_incubated", "swab_is_spun", "swab_new_tube", "sample_is_spun"]):
        scene discard_sample_1
        pause 1.0
        scene discard_sample_2
        pause 0.5
        scene discard_sample_3
        pause 0.5
        scene discard_sample_4
        pause 0.5
        scene discard_sample_5
        pause 0.5
        scene discard_sample_6
        pause 0.5
        scene discard_sample_7
        pause 1.0
        $ dna_notify_msg("Sample transferred!", correct=True)
        $ dna_swab_tasks["sample_new_tube"] = True
        jump dna_finish_step_1
    jump dna_bio_station

label dna_finish_step_1:
    scene bio_station
    show nina talk at right
    n "Lysis complete. The cells are broken down and the DNA is suspended in the liquid lysate."
    show nina thinknote1 at right
    n "Now we begin the purification steps to separate the DNA from unwanted proteins and fats. Keep your pipetting precise."
    scene table_tube_dark
    show nina thinknote1 at right
    n "That's the final wash done. The spin column is dry and ready for us to collect the clean DNA."
    jump dna_swab_question_1


################################################################################
## DNA labels -- extraction quiz + quantification
################################################################################

label dna_swab_question_1:
    scene table_tube_dark
    show nina thinknote1 at right
    n "The sample is loaded into the spin column, and the DNA is bound to the filter matrix. Next, we need a purification wash using Buffer AW1."
    n "How much Buffer AW1 should be pipetted into the column?"
    menu:
        "200\u00b5L Buffer AW1":
            n "Not enough volume. 200\u00b5L won't wash away all the leftover proteins, leaving our final sample contaminated. We need exactly 500\u00b5L."
            scene black with dissolve
            jump dna_swab_question_1

        "500\u00b5L Buffer AW1":
            $ dna_notify_msg("500\u00b5L Buffer AW1 added!", correct=True)
            jump dna_swab_question_2

        "1000\u00b5L Buffer AW1":
            n "That will flood the column assembly and ruin the wash. Bring it back down to 500\u00b5L."
            scene black with dissolve
            jump dna_swab_question_1

label dna_swab_question_2:
    show nina thinknote1 at right
    n "After the first wash, Buffer AW2 is added to remove remaining salts. How long should we spin the sample in the centrifuge for this step?"
    menu:
        "1 minute":
            n "Too short. A 1-minute spin leaves residual ethanol in the filter, which will completely ruin our later PCR reactions. It needs a full 3 minutes."
            scene black with dissolve
            jump dna_swab_question_1

        "3 minutes":
            $ dna_notify_msg("Centrifuged for 3 minutes!", correct=True)
            jump dna_swab_question_3

        "10 minutes":
            n "Spinning for 10 minutes is overkill and risks tearing the DNA apart under intense friction. Stick to the standard 3 minutes."
            scene black with dissolve
            jump dna_swab_question_1

label dna_swab_question_3:
    show nina thinknote1 at right
    n "The purified DNA is ready to be washed off the filter into a clean tube. How much of this extracted DNA template should go into our 50\u00b5L PCR reaction mix?"
    menu:
        "1\u00b5L extracted DNA":
            $ dna_notify_msg("DNA diluted!", correct=True)
            jump dna_finish_swab

        "5\u00b5L extracted DNA":
            n "If the sample is too concentrated, leftover chemicals from the extraction will overwhelm the DNA polymerase. Keep it to a clean 1\u00b5L."
            scene black with dissolve
            jump dna_swab_question_2

        "10\u00b5L extracted DNA":
            n "That much volume will stall out the reaction entirely. 1\u00b5L is all it takes for a 50\u00b5L target mix."
            scene black with dissolve
            jump dna_swab_question_2

label dna_finish_swab:
    scene bio_station
    show nina talk at right
    n "Clean yield. The DNA is isolated, purified, and ready in the tube."
    n "Let's run a quick qPCR assay to measure exactly how much human DNA we recovered from the car."
    jump dna_reaction_question_1

label dna_reaction_question_1:
    scene table_tube_dark
    show nina thinknote1 at right
    n "Which of these components is NOT used in a standard DNA profiling mix?"
    menu:
        "Master mix":
            n "Incorrect. The master mix holds the essential polymerase and building blocks for replication. We definitely need it."
            scene black with dissolve
            jump dna_reaction_question_1

        "Forward and reverse primers":
            n "Incorrect. Primers act as chemical markers to target the specific DNA regions we want to look at."
            scene black with dissolve
            jump dna_reaction_question_1

        "Nuclease-free water":
            n "Incorrect. We use it to bring the chemical mix up to volume safely without degrading the DNA."
            scene black with dissolve
            jump dna_reaction_question_1

        "Reverse transcriptase":
            n "Correct. That enzyme is used to copy RNA, not DNA. It has no place in an STR profiling kit."
            $ dna_notify_msg("Reaction mix prepared!", correct=True)
            jump dna_reaction_question_2

        "Magnesium chloride":
            n "Incorrect. Magnesium ions are required to catalyze the duplication process."
            scene black with dissolve
            jump dna_reaction_question_1

label dna_reaction_question_2:
    scene table_tube_dark
    show nina thinknote1 at right
    n "What size microcentrifuge tube should be used to prepare this mix?"
    menu:
        "1.0 mL tube":
            n "Non-standard size. Grab a standard 1.5 mL tube so we have enough room to mix the reagents safely."
            scene black with dissolve
            jump dna_reaction_question_1

        "1.5 mL tube":
            $ dna_notify_msg("Mix put into a 1.5 mL tube!", correct=True)
            jump dna_reaction_question_3

        "2.0 mL tube":
            n "Too large. A 2.0 mL tube won't sit properly in our benchtop centrifuges, and it makes it harder to see the liquid pellet. Stick to 1.5 mL."
            scene black with dissolve
            jump dna_reaction_question_1

label dna_reaction_question_3:
    n "Good. Dilute the purified DNA 1:1 with nuclease-free water to stabilize our final working solution."
    call screen dna_tray_drag
    jump dna_bio_station


################################################################################
## DNA labels -- qPCR / PCR / capillary electrophoresis / result
################################################################################

label dna_use_qpcr:
    call screen dna_qpcr
    jump dna_bio_station

label dna_pcr:
    $ dna_tasks["Run qPCR machine"] = True
    n "The quantification data looks great. We have more than enough DNA to get a profile."
    scene use_pcr
    show nina thinknote1 at right
    n "Now for the real test. We'll load the DNA, the master mix, and the fluorescent primers into the thermal cycler to copy our target forensic markers."
    n "Amplification is complete. The markers are copied millions of times over. Let's move the tube to the capillary electrophoresis unit to read the data."
    jump dna_cem

label dna_cem:
    scene computer_screen_interface
    pause 1.0
    scene cem_interface
    call screen dna_cem_screen
    jump dna_bio_station

label dna_cem_finish:
    scene cem_screen_results
    show nina thinknote1 at right
    n "The electropherogram results are printing out now."
    n "It's a clean, single-source profile. The lack of genetic noise means we pulled skin cells from touch transfer, not fluid."
    n "Running the data through the criminal database now... We have an exact match for [_robber_name]."
    $ dna_tasks["Analyze DNA results"] = True
    $ lab_dna_done = True
    $ dna_notify_msg("DNA analysis complete, profile matched!", correct=True)
    n "That solidifies our biological evidence. Let's head back to the main desk and wrap this up."
    jump dna_exit


################################################################################
## Conclusion
################################################################################

label lab_conclusion:
    scene bg_debrief with dissolve
    show nina thinknote1 at center with dissolve
    n "The forensic data is clear. The fingerprint minutiae from the outside handle and the DNA markers from the cabin lead to one person: [_robber_name], our Pontiac Bandit."
    n "We have undeniable physical proof placing him inside that vehicle. I'm calling the District Attorney to get a felony arrest warrant signed."
    show nina normal1 at center
    n "Excellent protocol work today. The evidence is airtight. Case closed."
    hide nina with dissolve
    return