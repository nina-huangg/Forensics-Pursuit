## Cotton-swab DNA extraction procedure + negative control.
## Machines/tools advance an ordered checklist; free click still warns if early.
## Prep both sample tubes; after prep the player chooses ONE tube to analyze.

default extraction_step_index = 0
default prep_sample_done = False
default prep_negative_done = False
default prep_equipped_item = None
default prep_equipped_source_name = ""
default prep_processed_names = []
default prep_samples_needed = 2
default prep_instructions_open = False
default prep_atl_selected = False
default prep_prok_selected = False
# Empty tube on the prep bench for the negative control (no swab).
default prep_negative_active = False
# Buffer AL selection during the post-lysis add-AL prep step.
default prep_al_selected = False
default extraction_al_added = False
default extraction_ate_added = False
# After prep: player picks one processed tube; Nina removes the other.
default extraction_tube_chosen = False
default extraction_active_tube = ""
# Per-tube progress for the current post-prep extraction step.
default extraction_machine_equipped = None
default extraction_machine_equipped_name = ""
default extraction_step_tubes_done = []
# Benchtop centrifuge balance mini-game (sample + neg control on opposite slots).
default centrifuge_sample_slot = 0
default centrifuge_balance_slot = 0
default centrifuge_sample_item = None
default centrifuge_holding = ""
# Mini centrifuge (spinner) balance — 6-slot rotor, opposite = +3.
default spinner_sample_slot = 0
default spinner_balance_slot = 0
default spinner_sample_item = None
default spinner_holding = ""


# Ordered procedure. Each entry: (step_key, required_tool, success_message)
# required_tool: prep | vortex | spinner | incubator | ethanol | column | centrifuge | trash | ate | wait | al
define EXTRACTION_ACTIONS = [
    ("place_atl_prok", "prep", "Tubes prepped with ATL and ProK."),
    ("vortex_10", "vortex", "Pulse-vortexed for 10 seconds."),
    ("spin_1", "spinner", "Mini centrifuge spin complete."),
    ("incubate_56", "incubator", "Thermomixer: 56°C at 900 rpm for 1 hour."),
    ("set_70", "incubator", "Thermomixer set to 70°C."),
    ("spin_2", "spinner", "Mini centrifuge spin complete."),
    ("add_al", "al", "Added 300 µL Buffer AL. Next: pulse-vortex both tubes."),
    ("vortex_al", "vortex", "Pulse-vortexed for 15 seconds."),
    ("spin_3", "spinner", "Mini centrifuge spin complete."),
    ("incubate_70", "incubator", "Thermomixer: 70°C at 900 rpm for 10 minutes."),
    ("spin_4", "spinner", "Mini centrifuge spin complete."),
    ("add_ethanol_150", "ethanol", "Added 150 µL ethanol."),
    ("vortex_ethanol", "vortex", "Pulse-vortexed for 15 seconds."),
    ("spin_5", "spinner", "Mini centrifuge spin complete."),
    ("transfer_lysate", "column", "Lysate transferred to QIAamp MinElute column."),
    ("centrifuge_8000_1", "centrifuge", "Benchtop centrifuge: 8000 rpm for 1 minute."),
    ("add_aw1", "column", "New collection tube + 500 µL Buffer AW1."),
    ("centrifuge_aw1", "centrifuge", "Benchtop centrifuge: 8000 rpm for 1 minute."),
    ("add_aw2", "column", "New collection tube + 700 µL Buffer AW2."),
    ("centrifuge_aw2", "centrifuge", "Benchtop centrifuge: 8000 rpm for 1 minute."),
    ("add_ethanol_700", "ethanol", "New collection tube + 700 µL ethanol."),
    ("centrifuge_ethanol", "centrifuge", "Benchtop centrifuge: 8000 rpm for 1 minute."),
    ("new_collection_tube", "column", "Columns placed in new collection tubes."),
    ("centrifuge_14000_3", "centrifuge", "Benchtop centrifuge: 14000 rpm for 3 minutes."),
    ("column_to_labeled_tube", "column", "Column placed in labelled 1.5 mL tube."),
    ("open_incubate_10", "wait", "Open lids; room-temperature incubation 10 minutes."),
    ("add_ate", "ate", "Applied Buffer ATE to the membrane."),
    ("incubate_1", "wait", "Room-temperature incubation 1 minute."),
    ("centrifuge_14000_1", "centrifuge", "Benchtop centrifuge: 14000 rpm for 1 minute."),
    ("discard_column", "trash", "Column discarded. Collection tube kept (DNA extract)."),
]

init -3 python:
    import math

    # Collected tubes that can be equipped on the prep bench, and their processed forms.
    # Only two blood samples: lamp + floor blood pool (Pool aliases Floor).
    PREP_TUBE_PROCESS_MAP = {
        "Tube with Swab (Lamp)": ("Processed Tube with Swab (Lamp)", "inventory-processed-swab-lamp"),
        "Tube with Swab (Floor)": ("Processed Tube with Swab (Floor)", "inventory-processed-swab-floor"),
        "Tube with Swab (Pool)": ("Processed Tube with Swab (Floor)", "inventory-processed-swab-floor"),
    }

    PROCESSED_TUBE_NAMES = (
        "Processed Tube with Swab (Lamp)",
        "Processed Tube with Swab (Floor)",
    )

    NEG_CONTROL_NAME = "Negative Control Tube"

    # Benchtop centrifuge rotor (use_centrifuge.png): 12 slots, slot 1 at top.
    CENTRIFUGE_ROTOR_CX = 958
    CENTRIFUGE_ROTOR_CY = 463
    CENTRIFUGE_ROTOR_R = 112
    CENTRIFUGE_SLOT_SIZE = 50

    def centrifuge_slot_rect(slot):
        """Return (x, y, w, h) for rotor slot 1–12."""
        ang = math.radians(-90 + (slot - 1) * 30)
        half = CENTRIFUGE_SLOT_SIZE // 2
        x = int(CENTRIFUGE_ROTOR_CX + CENTRIFUGE_ROTOR_R * math.cos(ang) - half)
        y = int(CENTRIFUGE_ROTOR_CY + CENTRIFUGE_ROTOR_R * math.sin(ang) - half)
        return (x, y, CENTRIFUGE_SLOT_SIZE, CENTRIFUGE_SLOT_SIZE)

    def centrifuge_opposite(slot):
        return ((slot - 1 + 6) % 12) + 1

    def centrifuge_is_balanced():
        if not store.centrifuge_sample_slot:
            return False
        return store.centrifuge_balance_slot == centrifuge_opposite(store.centrifuge_sample_slot)

    def centrifuge_reset_rotor(return_sample=False):
        if return_sample and store.centrifuge_sample_item is not None:
            store.is_packing_evidence = True
            store.evidence.add_to_inventory(store.centrifuge_sample_item)
            store.is_packing_evidence = False
        store.centrifuge_sample_slot = 0
        store.centrifuge_balance_slot = 0
        store.centrifuge_sample_item = None
        store.centrifuge_holding = ""

    def centrifuge_place_in_slot(slot):
        """Place equipped sample or held negative control into a rotor slot."""
        if store.centrifuge_holding == "neg":
            if not store.centrifuge_sample_slot:
                custom_notify("Place your sample tube in a rotor slot first.", False)
                return
            if store.centrifuge_balance_slot:
                custom_notify("Rotor is already balanced.", True)
                return
            opp = centrifuge_opposite(store.centrifuge_sample_slot)
            if slot != opp:
                record_lab_mistake()
                custom_notify(
                    "Wrong slot — place the negative control opposite your sample (slot {}).".format(opp),
                    False,
                )
                return
            store.centrifuge_balance_slot = slot
            store.centrifuge_holding = ""
            custom_notify("Rotor balanced. You can run the benchtop centrifuge.", True)
            renpy.restart_interaction()
            return

        if store.centrifuge_sample_slot:
            custom_notify("Sample already in slot {}. Balance with the negative control.".format(
                store.centrifuge_sample_slot
            ), True)
            return
        if store.extraction_machine_equipped is None:
            custom_notify("Use your processed sample tube from Evidence first, then click a slot.", False)
            return
        if store.extraction_machine_equipped.name == NEG_CONTROL_NAME:
            custom_notify("Place your sample tube in a slot first. Then Use the Negative Control for the opposite slot.", False)
            return

        store.centrifuge_sample_slot = slot
        store.centrifuge_sample_item = store.extraction_machine_equipped
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        store.centrifuge_balance_slot = 0
        opp = centrifuge_opposite(slot)
        custom_notify(
            "Sample in slot {}. Use Negative Control Tube from Evidence, then click slot {}.".format(
                slot, opp
            ),
            True,
        )
        renpy.restart_interaction()

    def centrifuge_pick_neg_control(item=None):
        if not renpy.get_screen("centrifuge"):
            custom_notify("Open the benchtop centrifuge first.", False)
            return
        if not store.centrifuge_sample_slot:
            custom_notify("Place your sample tube in a rotor slot first.", False)
            return
        if centrifuge_is_balanced():
            custom_notify("Rotor is already balanced.", True)
            return
        store.centrifuge_holding = "neg"
        store.held_evidence = None
        renpy.hide_screen("inventory")
        custom_notify(
            "Negative control ready — click slot {} (diagonal opposite).".format(
                centrifuge_opposite(store.centrifuge_sample_slot)
            ),
            True,
        )
        renpy.restart_interaction()

    # Mini centrifuge (spinner): 6 slots on use_spinner.png; opposite pairs 1-4, 2-5, 3-6.
    SPINNER_ROTOR_CX = 980
    SPINNER_ROTOR_CY = 690
    SPINNER_ROTOR_R = 90
    SPINNER_SLOT_SIZE = 44

    def spinner_slot_rect(slot):
        """Return (x, y, w, h) for mini-centrifuge rotor slot 1–6 (slot 1 ≈ 11 o'clock)."""
        ang = math.radians(-120 + (slot - 1) * 60)
        half = SPINNER_SLOT_SIZE // 2
        x = int(SPINNER_ROTOR_CX + SPINNER_ROTOR_R * math.cos(ang) - half)
        y = int(SPINNER_ROTOR_CY + SPINNER_ROTOR_R * math.sin(ang) - half)
        return (x, y, SPINNER_SLOT_SIZE, SPINNER_SLOT_SIZE)

    def spinner_opposite(slot):
        return ((slot - 1 + 3) % 6) + 1

    def spinner_is_balanced():
        if not store.spinner_sample_slot:
            return False
        return store.spinner_balance_slot == spinner_opposite(store.spinner_sample_slot)

    def spinner_reset_rotor(return_sample=False):
        if return_sample and store.spinner_sample_item is not None:
            store.is_packing_evidence = True
            store.evidence.add_to_inventory(store.spinner_sample_item)
            store.is_packing_evidence = False
        store.spinner_sample_slot = 0
        store.spinner_balance_slot = 0
        store.spinner_sample_item = None
        store.spinner_holding = ""

    def spinner_place_in_slot(slot):
        """Place equipped sample or held negative control into a mini-centrifuge slot."""
        if store.spinner_holding == "neg":
            if not store.spinner_sample_slot:
                custom_notify("Place your sample tube in a rotor slot first.", False)
                return
            if store.spinner_balance_slot:
                custom_notify("Rotor is already balanced.", True)
                return
            opp = spinner_opposite(store.spinner_sample_slot)
            if slot != opp:
                record_lab_mistake()
                custom_notify(
                    "Wrong slot — place the negative control opposite your sample (slot {}).".format(opp),
                    False,
                )
                return
            store.spinner_balance_slot = slot
            store.spinner_holding = ""
            custom_notify("Rotor balanced. You can run the mini centrifuge.", True)
            renpy.restart_interaction()
            return

        if store.spinner_sample_slot:
            custom_notify("Sample already in slot {}. Balance with the negative control.".format(
                store.spinner_sample_slot
            ), True)
            return
        if store.extraction_machine_equipped is None:
            custom_notify("Use your processed sample tube from Evidence first, then click a slot.", False)
            return
        if store.extraction_machine_equipped.name == NEG_CONTROL_NAME:
            custom_notify("Place your sample tube in a slot first. Then Use the Negative Control for the opposite slot.", False)
            return

        store.spinner_sample_slot = slot
        store.spinner_sample_item = store.extraction_machine_equipped
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        store.spinner_balance_slot = 0
        opp = spinner_opposite(slot)
        custom_notify(
            "Sample in slot {}. Use Negative Control Tube from Evidence, then click slot {}.".format(
                slot, opp
            ),
            True,
        )
        renpy.restart_interaction()

    def spinner_pick_neg_control(item=None):
        if not renpy.get_screen("spinner"):
            custom_notify("Open the mini centrifuge first.", False)
            return
        if not store.spinner_sample_slot:
            custom_notify("Place your sample tube in a rotor slot first.", False)
            return
        if spinner_is_balanced():
            custom_notify("Rotor is already balanced.", True)
            return
        store.spinner_holding = "neg"
        store.held_evidence = None
        renpy.hide_screen("inventory")
        custom_notify(
            "Negative control ready — click slot {} (diagonal opposite).".format(
                spinner_opposite(store.spinner_sample_slot)
            ),
            True,
        )
        renpy.restart_interaction()

    def ensure_negative_control_in_evidence():
        """Add the negative-control tube used to balance centrifuges."""
        for item in store.evidence._inventory:
            if item is not None and item.name == NEG_CONTROL_NAME:
                return item

        item = Item(
            NEG_CONTROL_NAME,
            "toolbox-tube",
            "Negative control (ATL + ProK, no swab). Use on mini or benchtop centrifuge to balance opposite your sample.",
            True,
            None,
        )
        store.is_packing_evidence = True
        store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False
        return item

    def choose_extraction_tube(keep_name):
        """Keep one processed tube for analysis; Nina removes the other from inventory."""
        store.extraction_active_tube = keep_name
        store.extraction_tube_chosen = True
        # Prep stays 2/2 complete — removing a tube from inventory does not undo prep progress.
        store.prep_sample_done = True

        for item in list(store.evidence._inventory):
            if item is not None and item.name in PROCESSED_TUBE_NAMES and item.name != keep_name:
                store.evidence.delete_from_inventory(item)

        ensure_negative_control_in_evidence()
        custom_notify("Continuing analysis with {}.".format(keep_name), True)

    def prep_samples_complete():
        # Once both tubes were prepped (or a tube was chosen), prep stays complete.
        if store.prep_sample_done or store.extraction_tube_chosen:
            return True
        return prep_evidence_count() >= store.prep_samples_needed

    def prep_sync_sample_done():
        store.prep_sample_done = prep_samples_complete()
        return store.prep_sample_done

    def extraction_reset():
        store.extraction_step_index = 0
        store.prep_sample_done = False
        store.prep_negative_done = False
        store.prep_equipped_item = None
        store.prep_equipped_source_name = ""
        store.prep_processed_names = []
        store.prep_samples_needed = 2
        store.prep_atl_selected = False
        store.prep_prok_selected = False
        store.prep_al_selected = False
        store.prep_negative_active = False
        store.extraction_al_added = False
        store.extraction_ate_added = False
        store.extraction_tube_chosen = False
        store.extraction_active_tube = ""
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        store.extraction_step_tubes_done = []
        centrifuge_reset_rotor(return_sample=False)
        spinner_reset_rotor(return_sample=False)
        store.swab_is_vortexed_2 = False
        store.swab_is_incubated_0 = False
        store.ethanol_added = False
        store.ethanol_pour_amount = 0
        store.lysate_transfer_amount = 0
        store.aw1_pour_amount = 0
        store.ate_pour_amount = 0
        store.incubator_loaded_tubes = []
        store.tube_transfered = False
        store.dna_extraction_progress = {}
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

    def prep_reset_bench_flags():
        store.swab_tasks["swab_is_cut"] = False
        store.swab_tasks["swab_is_prepped"] = False
        store.default_mouse = "default"
        prep_reset_bottle_selection()

    def prep_reset_bottle_selection():
        store.prep_atl_selected = False
        store.prep_prok_selected = False
        store.prep_al_selected = False
        if store.default_mouse == "micropipette":
            store.default_mouse = "default"
            store.current_cursor = ""

    def prep_buffers_ready():
        return store.prep_atl_selected and store.prep_prok_selected

    def prep_is_add_al_step():
        cur = extraction_current()
        return cur is not None and cur[0] == "add_al"

    def prep_is_add_ate_step():
        cur = extraction_current()
        return cur is not None and cur[0] == "add_ate"

    def prep_al_tube_allowed(name):
        """Processed sample or negative control for the Buffer AL prep step."""
        if not name:
            return False
        needed = extraction_required_processed_tubes()
        return name in needed

    def prep_start_negative():
        """Place an empty tube on the bench and prep it like a sample (no swab)."""
        if store.prep_negative_done:
            custom_notify("Negative control is already prepared.", True)
            return
        if store.prep_equipped_item is not None:
            custom_notify("Return the swab tube first — negative control has no swab.", False)
            return
        if store.prep_negative_active:
            custom_notify("Empty negative-control tube is already on the bench.", True)
            return

        store.prep_negative_active = True
        prep_reset_bottle_selection()
        custom_notify(
            "Empty tube ready (negative control). Select Buffer ATL + Proteinase K, then click the tube. No swab — this checks for contamination.",
            True,
        )
        renpy.restart_interaction()

    def prep_cancel_negative():
        if not store.prep_negative_active:
            return
        store.prep_negative_active = False
        prep_reset_bottle_selection()
        custom_notify("Removed empty negative-control tube from the bench.", True)
        renpy.restart_interaction()

    def prep_select_bottle(bottle_id):
        """Click a reagent bottle on the prep table (prep1: ATL / ProK / AL)."""
        labels = {
            "atl": "Buffer ATL",
            "prok": "Proteinase K",
            "al": "Buffer AL",
        }
        label = labels.get(bottle_id, bottle_id)

        # Picking up a table solution always switches to the micropipette cursor.
        store.default_mouse = "micropipette"
        store.current_cursor = "micropipette"

        # Post-lysis: add 300 µL Buffer AL only (its own bottle now).
        if prep_is_add_al_step():
            if bottle_id == "al":
                store.prep_al_selected = True
                if store.prep_equipped_item is not None:
                    custom_notify("Buffer AL selected — click the tube to add 300 µL.", True)
                else:
                    custom_notify("Buffer AL selected. Equip your sample or Negative Control from Evidence, then click the tube.", True)
            else:
                record_lab_mistake()
                custom_notify("Wrong bottle. Select Buffer AL for this step.", False)
            renpy.restart_interaction()
            return

        if bottle_id == "al":
            record_lab_mistake()
            custom_notify("Not the Buffer AL step yet. Check the notebook.", False)
            renpy.restart_interaction()
            return

        if bottle_id == "atl":
            store.prep_atl_selected = True
        elif bottle_id == "prok":
            store.prep_prok_selected = True
        else:
            return

        if prep_buffers_ready():
            if store.prep_equipped_item is not None:
                if not store.swab_tasks.get("swab_is_cut"):
                    custom_notify("Cut the swab into the tube first, then click the dry tube to add ATL + ProK.", False)
                else:
                    custom_notify("ATL + ProK selected — click the dry tube to add them.", True)
            elif store.prep_negative_active:
                custom_notify("ATL + ProK selected — click the empty tube to prep the negative control.", True)
            elif not store.prep_negative_done:
                custom_notify("ATL + ProK ready. Equip a swab tube, or start the negative control (empty tube).", True)
            else:
                custom_notify("ATL + ProK selected. Equip a swab tube if you still need one.", True)
        else:
            missing = "Proteinase K" if store.prep_atl_selected else "Buffer ATL"
            custom_notify("Selected {}. Also select {}.".format(label, missing), True)

        renpy.restart_interaction()

    def prep_cut_swab():
        """Scissors: cut the equipped swab into the tube."""
        if prep_is_add_al_step():
            custom_notify("No cutting needed — select Buffer AL and click the tube.", False)
            return
        if store.prep_negative_active:
            custom_notify("Negative control has no swab — do not cut. Add ATL + ProK to the empty tube.", False)
            return
        if store.prep_equipped_item is None:
            custom_notify("Open inventory and Use a Tube with Swab to equip it first.", False)
            return
        store.swab_tasks["swab_is_cut"] = True
        if prep_buffers_ready():
            store.default_mouse = "micropipette"
            store.current_cursor = "micropipette"
            custom_notify("Swab cut. Click the dry tube to add ATL + ProK.", True)
        else:
            custom_notify("Swab cut. Select Buffer ATL and Proteinase K on the table.", True)
        renpy.restart_interaction()

    def prep_evidence_count():
        return len(store.prep_processed_names)

    def prep_try_finish_step():
        prep_sync_sample_done()
        if store.prep_sample_done and store.prep_negative_done:
            # Cross off the prep notebook step as soon as samples + negative are done.
            store.dna_extraction_progress["place_atl_prok"] = True
            if not store.extraction_tube_chosen:
                ensure_negative_control_in_evidence()
                # Close prep UI so Nina can ask which tube to continue with.
                renpy.end_interaction("choose_tube")
                return True
            try_extraction_tool("prep")
            return True
        return False

    def prep_equip_from_inventory(item):
        """Take a collected tube out of evidence and place it on the prep bench."""
        if item is None:
            return False
        if not renpy.get_screen("swab_screen"):
            return False

        source_name = item.name
        if source_name not in PREP_TUBE_PROCESS_MAP:
            custom_notify("Only collected swab tubes can be equipped here.", False)
            return False
        if source_name in store.prep_processed_names:
            custom_notify("That swab tube is already prepped.", True)
            return False
        if store.prep_equipped_item is not None:
            custom_notify("Finish or return the tube already on the bench first.", False)
            return False
        if store.prep_negative_active:
            store.prep_negative_active = False

        store.evidence.delete_from_inventory(item)
        store.prep_equipped_item = item
        store.prep_equipped_source_name = source_name
        prep_reset_bench_flags()
        store.held_evidence = None
        renpy.hide_screen("inventory")
        custom_notify("Equipped {} on the prep bench.".format(source_name), True)
        renpy.restart_interaction()
        return True

    def prep_equip_al_from_inventory(item):
        """Equip a processed sample or negative control to add Buffer AL."""
        if item is None or not renpy.get_screen("swab_screen"):
            return False
        if not prep_is_add_al_step():
            custom_notify("Not the Buffer AL step yet. Check the notebook.", False)
            return False
        if store.prep_equipped_item is not None:
            custom_notify("Finish or return the tube already on the bench first.", False)
            return False

        name = item.name
        if not prep_al_tube_allowed(name):
            custom_notify("Use your chosen sample tube or the Negative Control Tube.", False)
            return False
        if name in store.extraction_step_tubes_done:
            custom_notify("Buffer AL already added to that tube.", True)
            return False

        store.evidence.delete_from_inventory(item)
        store.prep_equipped_item = item
        store.prep_equipped_source_name = name
        store.prep_negative_active = False
        store.held_evidence = None
        renpy.hide_screen("inventory")
        if store.prep_al_selected:
            store.default_mouse = "micropipette"
            store.current_cursor = "micropipette"
            custom_notify("Tube ready — click it to add 300 µL Buffer AL.", True)
        else:
            custom_notify("Equipped {}. Select Buffer AL on the table, then click the tube.".format(name), True)
        renpy.restart_interaction()
        return True

    def prep_dispense_al():
        """Add 300 µL Buffer AL to the equipped tube and return it to inventory."""
        if not prep_is_add_al_step():
            custom_notify("Not the Buffer AL step.", False)
            return
        item = store.prep_equipped_item
        if item is None:
            custom_notify("Equip your sample or Negative Control from Evidence first.", False)
            return
        if not store.prep_al_selected:
            custom_notify("Select Buffer AL on the table first.", False)
            return

        tube_name = item.name
        if tube_name in store.extraction_step_tubes_done:
            custom_notify("Buffer AL already added to that tube.", True)
            return

        store.extraction_step_tubes_done.append(tube_name)
        store.is_packing_evidence = True
        store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False
        store.prep_equipped_item = None
        store.prep_equipped_source_name = ""
        prep_reset_bottle_selection()

        if extraction_step_tubes_complete():
            store.extraction_al_added = True
            complete_extraction_step()
            return

        remaining = len(extraction_required_processed_tubes()) - extraction_step_tube_count()
        custom_notify(
            "Buffer AL added — tube returned to inventory. Equip the next tube ({} left).".format(remaining),
            True,
        )
        renpy.restart_interaction()

    def prep_equip_ate_tube(item):
        """Equip a processed sample or negative control tube for the Buffer ATE elution step."""
        if item is None or not renpy.get_screen("swab_screen"):
            return False
        if not prep_is_add_ate_step():
            custom_notify("Not the Buffer ATE step yet. Check the notebook.", False)
            return False
        if store.prep_equipped_item is not None:
            custom_notify("Finish or return the tube already on the bench first.", False)
            return False

        name = item.name
        if not prep_al_tube_allowed(name):
            custom_notify("Use your chosen sample tube or the Negative Control Tube.", False)
            return False
        if name in store.extraction_step_tubes_done:
            custom_notify("Buffer ATE already applied to that tube.", True)
            return False

        store.evidence.delete_from_inventory(item)
        store.prep_equipped_item = item
        store.prep_equipped_source_name = name
        store.prep_negative_active = False
        store.held_evidence = None
        renpy.hide_screen("inventory")
        custom_notify("Equipped {}. Click Apply Buffer ATE to elute.".format(name), True)
        renpy.restart_interaction()
        return True

    def prep_dispense_ate():
        """Finish the Buffer ATE elution on the equipped tube and return it to inventory."""
        if not prep_is_add_ate_step():
            custom_notify("Not the Buffer ATE step.", False)
            return
        item = store.prep_equipped_item
        if item is None:
            custom_notify("Equip your sample or Negative Control from Evidence first.", False)
            return

        tube_name = item.name
        if tube_name in store.extraction_step_tubes_done:
            custom_notify("Buffer ATE already applied to that tube.", True)
            return

        store.extraction_step_tubes_done.append(tube_name)
        store.is_packing_evidence = True
        store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False
        store.prep_equipped_item = None
        store.prep_equipped_source_name = ""

        if extraction_step_tubes_complete():
            store.extraction_ate_added = True
            complete_extraction_step()
            return

        remaining = len(extraction_required_processed_tubes()) - extraction_step_tube_count()
        custom_notify(
            "Buffer ATE applied — tube returned to inventory. Equip the next tube ({} left).".format(remaining),
            True,
        )
        renpy.restart_interaction()

    PREP2_BENCH_TOOLS = ("ethanol", "column")

    def prep2_bench_tool_active():
        return extraction_expected_tool() in PREP2_BENCH_TOOLS

    def prep_equip_bench_tube(item):
        """Equip a processed sample or negative-control tube for whichever prep2
        reagent step (Ethanol / AW1 / AW2) is currently active."""
        if item is None or not renpy.get_screen("swab_screen"):
            return False
        if not prep2_bench_tool_active():
            custom_notify("Not a Prep-bench step yet. Check the notebook.", False)
            return False
        if store.prep_equipped_item is not None:
            custom_notify("Finish or return the tube already on the bench first.", False)
            return False

        name = item.name
        if not prep_al_tube_allowed(name):
            custom_notify("Use your chosen sample tube or the Negative Control Tube.", False)
            return False
        if name in store.extraction_step_tubes_done:
            custom_notify("Already done for that tube on this step.", True)
            return False

        store.evidence.delete_from_inventory(item)
        store.prep_equipped_item = item
        store.prep_equipped_source_name = name
        store.prep_negative_active = False
        store.held_evidence = None
        renpy.hide_screen("inventory")
        custom_notify("Equipped {} on the Prep bench.".format(name), True)
        renpy.restart_interaction()
        return True

    def prep_handoff_to_machine():
        """Move a tube from the Prep bench slot onto the generic machine-equip slot,
        for reagent steps that hand off into a separate mini-game (ethanol/column)."""
        item = store.prep_equipped_item
        if item is None:
            return False
        store.extraction_machine_equipped = item
        store.extraction_machine_equipped_name = item.name
        store.prep_equipped_item = None
        store.prep_equipped_source_name = ""
        return True

    def prep_return_unequipped():
        """Put the unequipped (not yet processed) tube back into evidence."""
        item = store.prep_equipped_item
        if item is None:
            return
        store.is_packing_evidence = True
        store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False
        store.prep_equipped_item = None
        store.prep_equipped_source_name = ""
        if prep_is_add_al_step():
            prep_reset_bottle_selection()
        else:
            prep_reset_bench_flags()
        custom_notify("Returned tube to inventory.", True)
        renpy.restart_interaction()

    def extraction_required_processed_tubes():
        """Tubes required each post-prep step: chosen sample + negative control."""
        if store.extraction_active_tube:
            names = [store.extraction_active_tube]
            if store.prep_negative_done:
                names.append(NEG_CONTROL_NAME)
            return names

        names = []
        for source in store.prep_processed_names:
            mapped = PREP_TUBE_PROCESS_MAP.get(source)
            if mapped:
                processed_name = mapped[0]
                if processed_name not in names:
                    names.append(processed_name)
        if not names:
            for item in store.evidence._inventory:
                if item is not None and item.name in PROCESSED_TUBE_NAMES:
                    if item.name not in names:
                        names.append(item.name)
        return names

    def extraction_step_tubes_needed():
        return max(1, len(extraction_required_processed_tubes()))

    def extraction_step_tube_count():
        return len(store.extraction_step_tubes_done)

    def extraction_step_tubes_complete():
        needed = extraction_required_processed_tubes()
        if not needed:
            return False
        return all(name in store.extraction_step_tubes_done for name in needed)

    def extraction_reset_step_tubes():
        store.extraction_step_tubes_done = []
        # Return any tube left on a machine when the step advances.
        if store.extraction_machine_equipped is not None:
            store.is_packing_evidence = True
            store.evidence.add_to_inventory(store.extraction_machine_equipped)
            store.is_packing_evidence = False
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        centrifuge_reset_rotor(return_sample=True)
        spinner_reset_rotor(return_sample=True)

    def extraction_on_machine_screen():
        return any(
            renpy.get_screen(name)
            for name in (
                "centrifuge",
                "spinner",
                "vortex",
                "incubator",
                "swab_screen",
            )
        )

    def extraction_equip_processed_tube(item):
        """Equip a processed tube onto the current machine from Evidence."""
        if item is None:
            return False
        if renpy.get_screen("swab_screen"):
            custom_notify("That tube is already prepped. Use it on the next machine.", True)
            return False

        # If prep is done but the checklist stuck, advance before equipping.
        extraction_ensure_past_prep()

        expected = extraction_expected_tool()
        if expected in (None, "prep") or extraction_complete():
            custom_notify("No extraction machine step needs a tube right now.", False)
            return False

        required = extraction_required_processed_tubes()
        allowed = set(required) | set(PROCESSED_TUBE_NAMES) | {NEG_CONTROL_NAME}
        if item.name not in allowed:
            custom_notify("Equip your processed sample tube or the Negative Control Tube.", False)
            return False
        if required and item.name not in required:
            custom_notify("This step needs: {}.".format(", ".join(required)), False)
            return False
        if item.name in store.extraction_step_tubes_done:
            custom_notify("That tube already finished this step.", True)
            return False
        if store.extraction_machine_equipped is not None or store.centrifuge_sample_item is not None:
            custom_notify("Return or finish the tube already on the machine first.", False)
            return False

        store.evidence.delete_from_inventory(item)
        store.extraction_machine_equipped = item
        store.extraction_machine_equipped_name = item.name
        store.held_evidence = None
        renpy.hide_screen("inventory")
        if (
            (renpy.get_screen("centrifuge") or renpy.get_screen("spinner"))
            and item.name != NEG_CONTROL_NAME
        ):
            custom_notify("Equipped {}. Click a rotor slot to place it.".format(item.name), True)
        else:
            custom_notify("Equipped {} on the machine.".format(item.name), True)
        renpy.restart_interaction()
        return True

    def extraction_return_machine_tube():
        item = store.extraction_machine_equipped
        if item is None and store.centrifuge_sample_item is not None:
            centrifuge_reset_rotor(return_sample=True)
            custom_notify("Returned tube to inventory.", True)
            renpy.restart_interaction()
            return
        if item is None and store.spinner_sample_item is not None:
            spinner_reset_rotor(return_sample=True)
            custom_notify("Returned tube to inventory.", True)
            renpy.restart_interaction()
            return
        if item is None:
            return
        store.is_packing_evidence = True
        store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        centrifuge_reset_rotor(return_sample=False)
        spinner_reset_rotor(return_sample=False)
        custom_notify("Returned tube to inventory.", True)
        renpy.restart_interaction()

    def extraction_current():
        idx = store.extraction_step_index
        if idx < 0 or idx >= len(EXTRACTION_ACTIONS):
            return None
        return EXTRACTION_ACTIONS[idx]

    def extraction_complete():
        return store.extraction_step_index >= len(EXTRACTION_ACTIONS)

    def extraction_expected_tool():
        cur = extraction_current()
        return None if cur is None else cur[1]

    def extraction_sync_legacy_flags():
        """Keep older swab_tasks flags in sync for any leftover checks."""
        done = store.dna_extraction_progress
        if done.get("place_atl_prok"):
            store.swab_tasks["swab_is_cut"] = True
            store.swab_tasks["swab_is_prepped"] = True
        if done.get("vortex_10"):
            store.swab_tasks["swab_is_vortexed"] = True
        if done.get("incubate_56"):
            store.swab_is_incubated_0 = True
        if done.get("vortex_al") or done.get("add_al"):
            store.swab_is_vortexed_2 = True
            store.swab_tasks["swab_is_incubated"] = True
        if done.get("spin_5") or done.get("spin_4"):
            store.swab_tasks["swab_is_spun"] = True
        if done.get("transfer_lysate"):
            store.tube_transfered = True
            store.swab_tasks["swab_new_tube"] = True
        if done.get("centrifuge_8000_1"):
            store.swab_tasks["sample_is_spun"] = True
        if done.get("discard_column"):
            store.swab_tasks["sample_new_tube"] = True
            store.tasks["DNA extraction"] = True

    def complete_extraction_step():
        cur = extraction_current()
        if cur is None:
            return False
        key, _tool, msg = cur
        store.dna_extraction_progress[key] = True
        store.extraction_step_index += 1
        extraction_reset_step_tubes()
        extraction_sync_legacy_flags()
        custom_notify(msg, True)
        if extraction_complete():
            store.tasks["DNA extraction"] = True
            custom_notify("DNA extraction complete!", True)
        renpy.restart_interaction()
        return True

    def skip_dna_extraction():
        """Notebook shortcut: instantly finishes the DNA extraction procedure."""
        incubator_dual_reset()
        for step_key, _tool, _msg in EXTRACTION_ACTIONS:
            store.dna_extraction_progress[step_key] = True
        store.extraction_step_index = len(EXTRACTION_ACTIONS)
        extraction_reset_step_tubes()
        store.prep_sample_done = True
        store.prep_negative_done = True
        store.extraction_tube_chosen = True
        extraction_sync_legacy_flags()
        store.tasks["DNA extraction"] = True
        hide_lab_overlays()
        custom_notify("DNA extraction skipped.", True)

    def incubator_dual_load_add():
        """Move the currently equipped tube into the thermomixer's dual-tube load."""
        if store.extraction_machine_equipped is None:
            return False
        store.incubator_loaded_tubes.append(store.extraction_machine_equipped)
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        return True

    def incubator_dual_missing():
        """Tube names still needed before a dual-tube incubation step can run."""
        needed = extraction_required_processed_tubes()
        loaded_names = [item.name for item in store.incubator_loaded_tubes]
        return [name for name in needed if name not in loaded_names]

    def incubator_dual_complete():
        """Finish steps 4/10 (both tubes incubated together) in a single run."""
        cur = extraction_current()
        if cur is None:
            return False
        key, _tool, msg = cur
        for item in store.incubator_loaded_tubes:
            store.is_packing_evidence = True
            store.evidence.add_to_inventory(item)
            store.is_packing_evidence = False
        store.incubator_loaded_tubes = []
        store.dna_extraction_progress[key] = True
        store.extraction_step_index += 1
        extraction_sync_legacy_flags()
        custom_notify(msg, True)
        if extraction_complete():
            store.tasks["DNA extraction"] = True
            custom_notify("DNA extraction complete!", True)
        renpy.restart_interaction()
        return True

    def incubator_dual_reset():
        """Return any tubes sitting in the thermomixer without finishing the step."""
        for item in store.incubator_loaded_tubes:
            store.is_packing_evidence = True
            store.evidence.add_to_inventory(item)
            store.is_packing_evidence = False
        store.incubator_loaded_tubes = []

    def extraction_ensure_past_prep():
        """If prep is fully done but the checklist never advanced, move to the next step."""
        cur = extraction_current()
        if cur is None or cur[0] != "place_atl_prok":
            return False
        if not (prep_samples_complete() and store.prep_negative_done and store.extraction_tube_chosen):
            return False
        store.prep_sample_done = True
        store.dna_extraction_progress["place_atl_prok"] = True
        complete_extraction_step()
        return True

    def try_extraction_tool(tool):
        """
        Attempt to advance the procedure with this tool/machine.
        Post-prep steps require equipping the chosen processed tube from inventory.
        Returns 'ok', 'wait_prep', 'wait_tube', 'already_done', 'wrong', or 'done'.
        """
        if extraction_complete():
            custom_notify("Extraction is already finished.", True)
            return "done"

        # Recover if Nina's tube choice finished but the prep step index never advanced.
        if tool != "prep":
            extraction_ensure_past_prep()

        cur = extraction_current()
        if cur is None:
            return "done"

        key, expected, _msg = cur

        # Prep must finish sample + negative before leaving the prep step.
        if tool == "prep":
            if expected != "prep":
                # Already advanced past prep (e.g. ensure_past_prep already ran).
                return "ok"
            if not (prep_samples_complete() and store.prep_negative_done):
                custom_notify(
                    "Prep {} evidence tubes and the negative control first.".format(
                        store.prep_samples_needed
                    ),
                    False,
                )
                return "wait_prep"
            if not store.extraction_tube_chosen:
                custom_notify("Choose which processed tube to continue with first.", False)
                return "wait_prep"
            store.prep_sample_done = True
            complete_extraction_step()
            return "ok"

        if expected == "prep":
            custom_notify("Finish Prep first (2 samples + negative control), then choose a tube.", False)
            record_lab_mistake()
            return "wrong"

        if tool != expected:
            # Room-temp incubations can be started from the thermomixer.
            if expected == "wait" and tool == "incubator":
                pass
            else:
                custom_notify("Not the right tool/machine for this step. Check the notebook.", False)
                record_lab_mistake()
                return "wrong"

        # Benchtop centrifuge: sample in a slot + negative control opposite.
        if tool == "centrifuge" or expected == "centrifuge":
            if tool == "centrifuge" and not centrifuge_is_balanced():
                custom_notify(
                    "Balance the rotor first: place your sample, then Use the Negative Control Tube on the opposite slot.",
                    False,
                )
                return "wait_tube"
            if store.centrifuge_sample_item is not None and store.extraction_machine_equipped is None:
                store.extraction_machine_equipped = store.centrifuge_sample_item
                store.extraction_machine_equipped_name = store.centrifuge_sample_item.name
                store.centrifuge_sample_item = None

        # Mini centrifuge: same balance rule (6-slot rotor).
        if tool == "spinner" or expected == "spinner":
            if tool == "spinner" and not spinner_is_balanced():
                custom_notify(
                    "Balance the mini centrifuge first: place your sample, then Use the Negative Control Tube on the opposite slot.",
                    False,
                )
                return "wait_tube"
            if store.spinner_sample_item is not None and store.extraction_machine_equipped is None:
                store.extraction_machine_equipped = store.spinner_sample_item
                store.extraction_machine_equipped_name = store.spinner_sample_item.name
                store.spinner_sample_item = None

        # Setting temperature only — tubes are off the machine.
        if key == "set_70":
            complete_extraction_step()
            return "ok"

        # Every post-prep step: equip the chosen processed tube, run, return.
        equipped = store.extraction_machine_equipped
        if equipped is None:
            custom_notify(
                "Open Evidence and Use your processed swab tube to equip it first ({}/{} this step).".format(
                    extraction_step_tube_count(),
                    len(extraction_required_processed_tubes()) or 1,
                ),
                False,
            )
            return "wait_tube"

        tube_name = store.extraction_machine_equipped_name or equipped.name
        if tube_name in store.extraction_step_tubes_done:
            # Nothing actually ran — don't let callers play a wait/run animation for this.
            custom_notify("That tube already finished this step.", True)
            return "already_done"

        # Special handling for vortex AL step — buffers added as part of the mix.
        if key == "vortex_al":
            store.extraction_al_added = True

        if key in ("add_ethanol_150", "add_ethanol_700"):
            store.ethanol_added = True

        # Mark this tube done and return it to inventory.
        store.extraction_step_tubes_done.append(tube_name)
        # Balanced centrifuge runs process sample + negative control together.
        if tool in ("centrifuge", "spinner") and NEG_CONTROL_NAME not in store.extraction_step_tubes_done:
            if NEG_CONTROL_NAME in extraction_required_processed_tubes():
                store.extraction_step_tubes_done.append(NEG_CONTROL_NAME)

        store.is_packing_evidence = True
        store.evidence.add_to_inventory(equipped)
        store.is_packing_evidence = False
        store.extraction_machine_equipped = None
        store.extraction_machine_equipped_name = ""
        centrifuge_reset_rotor(return_sample=False)
        spinner_reset_rotor(return_sample=False)

        if extraction_step_tubes_complete():
            complete_extraction_step()
            return "ok"

        remaining = len(extraction_required_processed_tubes()) - extraction_step_tube_count()
        custom_notify(
            "Tube finished this step and returned to inventory. Equip the next tube ({} left).".format(
                remaining
            ),
            True,
        )
        renpy.restart_interaction()
        return "wait_tube"

    def prep_mark_sample():
        """Finish ATL/ProK on the equipped tube and return the processed item to inventory."""
        item = store.prep_equipped_item
        source_name = store.prep_equipped_source_name or (item.name if item else "")
        if item is None or source_name not in PREP_TUBE_PROCESS_MAP:
            custom_notify("Equip a collected swab tube from inventory first.", False)
            return
        if not store.swab_tasks.get("swab_is_cut"):
            custom_notify("Cut the swab into the tube first.", False)
            return
        if not prep_buffers_ready():
            custom_notify("Select Buffer ATL and Proteinase K on the table first.", False)
            return

        processed_name, processed_image = PREP_TUBE_PROCESS_MAP[source_name]
        item.name = processed_name
        item.image_name = processed_image
        item.description = (
            "Swab cut into the tube with Buffer ATL and ProK added. Ready for DNA extraction."
        )

        store.is_packing_evidence = True
        store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False

        if source_name not in store.prep_processed_names:
            store.prep_processed_names.append(source_name)

        store.prep_equipped_item = None
        store.prep_equipped_source_name = ""
        store.default_mouse = "default"
        prep_reset_bench_flags()

        remaining = store.prep_samples_needed - prep_evidence_count()
        if prep_try_finish_step():
            return
        elif remaining > 0:
            custom_notify(
                "Processed tube returned to inventory. Equip another swab tube ({} left).".format(
                    remaining
                ),
                True,
            )
        elif not store.prep_negative_done:
            custom_notify(
                "Both evidence tubes ready. Now prepare the negative control (no swab).",
                True,
            )
        else:
            prep_sync_sample_done()

        renpy.restart_interaction()

    def prep_mark_negative():
        """Finish ATL/ProK on the empty negative-control tube (same reagents, no swab)."""
        if not store.prep_negative_active:
            custom_notify("Click Start Negative Control to place an empty tube first.", False)
            renpy.restart_interaction()
            return
        if store.prep_equipped_item is not None:
            custom_notify("Return the swab tube first — negative control has no swab.", False)
            renpy.restart_interaction()
            return
        if not prep_buffers_ready():
            custom_notify("Select Buffer ATL and Proteinase K on the table first (no swab).", False)
            renpy.restart_interaction()
            return

        store.prep_negative_done = True
        store.prep_negative_active = False
        store.default_mouse = "default"
        store.current_cursor = ""
        prep_reset_bottle_selection()
        ensure_negative_control_in_evidence()
        custom_notify(
            "Negative control prepared (ATL + ProK, no swab) — used to check for contamination.",
            True,
        )
        if prep_try_finish_step():
            return
        elif not prep_samples_complete():
            custom_notify(
                "Still need {} evidence tube(s) from inventory.".format(
                    store.prep_samples_needed - prep_evidence_count()
                ),
                True,
            )
        renpy.restart_interaction()
