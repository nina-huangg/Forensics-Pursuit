default active_tool = None
default evidence_inventory = []

default fingerprint_powder = None
default fingerprint_powder_correct = False
default fingerprint_method = None
default fingerprint_dye_applied = False
default fingerprint_water_applied = False
default fingerprint_scalebar_placed = False
default fingerprint_scalebar_label = ""
default fingerprint_circled = False
default fingerprint_camera_equip_lens = False
default fingerprint_camera_equip_flashlight = False
default fingerprint_camera_equip_tripod = False
default fingerprint_photo_taken = False
default fingerprint_tape_applied = False
default fingerprint_roller_used = False
default fingerprint_transferred = False
default fingerprint_collected = False
default evidence_wrong_moves = 0
default evidence_score = 100
default asked_lab_transition = False
default lab_transition_pending = False
default show_leave_button = False
default backing_card_case = ""
default backing_card_date = ""
default backing_card_officer = ""
default backing_card_location = ""
default held_evidence = None
default is_packing_evidence = False
default bag_sealed = False
default evidence_bags_left = 5
default game_route = ""
default lab_blood_samples = []
default lab_fingerprint_loaded = False

# Kastle–Meyer presumptive blood test (per location).
# mask bits: methanol=1, phenolphthalein=2, hydrogen_peroxide=4; all applied = 7
# order string silently tracks application sequence for scoring (no player hints).
default blood_test_lamp_mask = 0
default blood_test_lamp_order = ""
default blood_test_lamp_positive = False
default blood_test_lamp_mistakes = 0
default blood_test_floor_mask = 0
default blood_test_floor_order = ""
default blood_test_floor_positive = False
default blood_test_floor_mistakes = 0
default blood_test_pool_mask = 0
default blood_test_pool_order = ""
default blood_test_pool_positive = False
default blood_test_pool_mistakes = 0
default active_blood_test_location = ""
default camera_hint_level = 0
default pending_photo_location = ""
default pending_photo_accepted = False

init -5 python:
    def reset_collection_state():
        """Reset mutable crime-scene state shared by both entry routes."""
        store.active_tool = None
        store.default_mouse = "default"
        store.selected_inventory = store.toolbox
        store.inventory_open = False
        store.evidence_inventory = []
        store.held_evidence = None
        store.is_packing_evidence = False
        store.bag_sealed = False
        store.evidence_bags_left = 5
        store.evidence_wrong_moves = 0
        store.evidence_score = 100
        store.asked_lab_transition = False
        store.lab_transition_pending = False
        store.show_leave_button = False
        store.first_study_visit = True
        store.scalebar_placed = False

        store.fingerprint_powder = None
        store.fingerprint_powder_correct = False
        store.fingerprint_method = None
        store.fingerprint_dye_applied = False
        store.fingerprint_water_applied = False
        store.fingerprint_scalebar_placed = False
        store.fingerprint_scalebar_label = ""
        store.fingerprint_circled = False
        store.fingerprint_camera_equip_lens = False
        store.fingerprint_camera_equip_flashlight = False
        store.fingerprint_camera_equip_tripod = False
        store.fingerprint_photo_taken = False
        store.fingerprint_tape_applied = False
        store.fingerprint_roller_used = False
        store.fingerprint_transferred = False
        store.fingerprint_collected = False

        store.blood_test_lamp_mask = 0
        store.blood_test_lamp_order = ""
        store.blood_test_lamp_positive = False
        store.blood_test_lamp_mistakes = 0
        store.blood_test_floor_mask = 0
        store.blood_test_floor_order = ""
        store.blood_test_floor_positive = False
        store.blood_test_floor_mistakes = 0
        store.blood_test_pool_mask = 0
        store.blood_test_pool_order = ""
        store.blood_test_pool_positive = False
        store.blood_test_pool_mistakes = 0
        store.active_blood_test_location = ""
        store.camera_hint_level = 0
        store.pending_photo_location = ""
        store.pending_photo_accepted = False

        store.lab_blood_samples = []
        store.lab_fingerprint_loaded = False
        store.lab_gameplay_initialized = False

        # Inventory instances are created during init, so they must be cleared
        # explicitly whenever a new route starts.
        store.toolbox.reset_inventory()
        store.evidence.reset_inventory()
        store.evids = load_items("jsons/evidence.json")
        store.tools = load_items("jsons/toolbox.json")

        # Fresh camera overlay state for New Game / route resets.
        # Direct lab route still gets a clean camera state but does not use it.
        initialize_camera_system()

    def initialize_collection_route():
        reset_collection_state()
        store.game_route = "collection"
        for tool in store.tools.values():
            store.toolbox.add_to_inventory(tool)

    def initialize_standalone_lab_route():
        reset_collection_state()
        store.game_route = "lab_only"
        store.asked_lab_transition = True
        store.lab_blood_samples = [
            "Tube with Swab (Lamp)",
            "Tube with Swab (Floor)",
        ]
        store.lab_fingerprint_loaded = True

        # Suppress collection prompts while preparing the lab-only evidence.
        store.is_packing_evidence = True
        for item_name in store.lab_blood_samples:
            item = store.evids.get(item_name)
            if item is not None:
                store.evidence.add_to_inventory(item)
        store.is_packing_evidence = False
        store.held_evidence = None
        prepare_lab_toolbox()

    LAB_REQUIRED_PHYSICAL_EVIDENCE = (
        # "Gel-Lifted Shoeprint",  # Temporarily disabled with shoeprint scene.
        "Tube with Swab (Lamp)",
        "Tube with Swab (Floor)",  # floor blood pool (lamp + pool = two blood swabs)
        "Fingerprint",
    )

    LAB_EVIDENCE_SHORT_NAMES = {
        "Gel-Lifted Shoeprint": "gel-lifted shoeprint",
        "Tube with Swab (Lamp)": "lamp blood swab",
        "Tube with Swab (Floor)": "floor blood pool swab",
        "Tube with Swab (Pool)": "floor blood pool swab",
        "Fingerprint": "lifted fingerprint",
    }

    def lab_transfer_issue_text(item_names):
        """Create a readable evidence list for Nina's warning dialogue."""
        labels = [
            LAB_EVIDENCE_SHORT_NAMES.get(name, name)
            for name in item_names
        ]
        if not labels:
            return ""
        if len(labels) == 1:
            return labels[0]
        if len(labels) == 2:
            return "{} and {}".format(labels[0], labels[1])
        return "{}, and {}".format(", ".join(labels[:-1]), labels[-1])

    def collection_lab_transfer_issues():
        """Find missing, loose, and unsealed physical evidence before the lab."""
        items = [
            item for item in store.evidence._inventory
            if item is not None
        ]
        collected_names = set(item.name for item in items)

        missing = []
        for name in LAB_REQUIRED_PHYSICAL_EVIDENCE:
            if name in collected_names:
                continue
            # Floor blood pool may still be labeled Pool from older saves.
            if name == "Tube with Swab (Floor)" and "Tube with Swab (Pool)" in collected_names:
                continue
            missing.append(name)
        unbagged = []
        unsealed = []

        for item in items:
            # Photographs transfer electronically and do not need evidence bags.
            if "Photo" in item.name:
                continue

            description = item.description or ""
            if "(Packed & Sealed)" in description:
                continue
            if "(Packed but UNSEALED)" in description:
                unsealed.append(item.name)
            else:
                unbagged.append(item.name)

        return {
            "missing": missing,
            "unbagged": unbagged,
            "unsealed": unsealed,
            "missing_text": lab_transfer_issue_text(missing),
            "unbagged_text": lab_transfer_issue_text(unbagged),
            "unsealed_text": lab_transfer_issue_text(unsealed),
            "has_issues": bool(missing or unbagged or unsealed),
        }

    def prepare_lab_toolbox():
        """Stock the lab-only toolbox (Column + Collection Tube)."""
        store.toolbox.reset_inventory()
        lab_tools = load_items("jsons/lab_toolbox.json")
        for item in lab_tools.values():
            store.toolbox.add_to_inventory(item)
        store.selected_inventory = store.toolbox
        remove_lab_buffer_from_evidence()

    def remove_lab_buffer_from_evidence():
        """Buffer ATL / ProK live on the prep table, not in inventory."""
        buffer_name = "Buffer ATL + ProK"
        for item in list(store.evidence._inventory):
            if item is not None and item.name == buffer_name:
                store.evidence.delete_from_inventory(item)

    def ensure_lab_buffer_in_evidence():
        """Deprecated — reagents are on the prep table. Kept as a no-op for old callers."""
        remove_lab_buffer_from_evidence()

    def use_buffer_atl_prok():
        """Legacy inventory action — point players at the table bottles."""
        renpy.hide_screen("inventory_info")
        renpy.hide_screen("inventory")
        if not renpy.get_screen("swab_screen"):
            renpy.notify("Open Prep and click Buffer ATL and Proteinase K on the table.")
            renpy.show_screen("open_inv")
            return
        custom_notify("Click Buffer ATL and Proteinase K on the table (not PBS).", True)
        renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def prepare_collected_evidence_for_lab():
        """Translate collected crime-scene evidence into lab input state."""
        fresh_evidence = load_items("jsons/evidence.json")
        transferred_items = []

        for item in store.evidence._inventory:
            if item is None:
                continue

            is_photo = "Photo" in item.name
            is_bagged = "(Packed & Sealed)" in (item.description or "")

            # Loose or unsealed physical evidence stays at the crime scene.
            # Photographs do not require a bag and may always be transferred.
            if not is_photo and not is_bagged:
                continue

            # In the lab, show the evidence itself rather than the generic bag.
            original_item = fresh_evidence.get(item.name)
            if original_item is not None:
                item.image_name = original_item.image_name

            item.description = item.description.replace(
                "\n(Packed & Sealed)", ""
            ).replace(
                "\n(Packed but UNSEALED)", ""
            )
            transferred_items.append(item)

        store.evidence.set_inventory(transferred_items)

        sample_names = (
            "Tube with Swab (Lamp)",
            "Tube with Swab (Floor)",
        )
        # Normalize legacy Pool tubes into Floor (floor blood pool).
        for item in list(store.evidence._inventory):
            if item is not None and item.name == "Tube with Swab (Pool)":
                item.name = "Tube with Swab (Floor)"
                floor_item = fresh_evidence.get("Tube with Swab (Floor)")
                if floor_item is not None:
                    item.image_name = floor_item.image_name
                    item.description = floor_item.description
            elif item is not None and item.name == "Swab with Blood (Pool)":
                item.name = "Swab with Blood (Floor)"
                floor_swab = fresh_evidence.get("Swab with Blood (Floor)")
                if floor_swab is not None:
                    item.image_name = floor_swab.image_name
                    item.description = floor_swab.description

        collected_names = [
            item.name for item in store.evidence._inventory if item is not None
        ]
        fingerprint_names = (
            "Fingerprint",
            "Fingerprint Photo",
            "Fingerprint Alone Photo",
            "Fingerprint Circled Photo",
        )

        store.game_route = "collection"
        store.lab_blood_samples = [
            name for name in sample_names if name in collected_names
        ]
        store.lab_fingerprint_loaded = any(
            name in collected_names for name in fingerprint_names
        )
        store.asked_lab_transition = True
        store.held_evidence = None

        # Crime-scene tools do not carry over; stock lab consumables instead.
        prepare_lab_toolbox()

    def collect_evidence(item_id):
        if item_id not in store.evidence_inventory:
            store.evidence_inventory.append(item_id)
            renpy.notify("Collected: {}".format(item_id))
        else:
            renpy.notify("You already collected this.")

    def add_evidence(item_id):
        if item_id not in store.evidence_inventory:
            store.evidence_inventory.append(item_id)
            renpy.notify("Added to evidence: {}".format(item_id))

    def handle_shoeprint_click():
        if store.active_tool != "camera":
            renpy.notify("You need to select the camera first.")
            return
        renpy.show_screen("shoeprint_photo_screen")

    def use_camera():
        if store.active_tool == "camera":
            reset_tool()
            renpy.notify("Camera unequipped.")
        else:
            store.active_tool = "camera"
            store.default_mouse = "camera"
            renpy.notify("Camera equipped. Mouse cursor changed.")
            renpy.hide_screen("inventory")
            renpy.show_screen("open_inv")

    def reset_tool():
        store.active_tool = None
        store.default_mouse = "default"

    def use_swab_pack():
        if store.active_tool == "swab_pack":
            reset_tool()
            renpy.notify("Swab Pack unequipped.")
        else:
            store.active_tool = "swab_pack"
            store.default_mouse = "swab_pack"
            renpy.notify("Swab Pack equipped. Mouse cursor changed.")
            renpy.hide_screen("inventory")
            renpy.show_screen("open_inv")

    def use_tube():
        swab_lamp = store.evids.get("Swab with Blood (Lamp)")
        tube_lamp = store.evids.get("Tube with Swab (Lamp)")
        swab_floor = store.evids.get("Swab with Blood (Floor)")
        tube_floor = store.evids.get("Tube with Swab (Floor)")
        swab_pool = store.evids.get("Swab with Blood (Pool)")
        tube_pool = store.evids.get("Tube with Swab (Pool)")
        
        processed = False
        
        # Check if the swab is currently held (since we intercept it on collection)
        if getattr(store, "held_evidence", None) is not None:
            held = store.held_evidence
            if held == swab_lamp:
                store.evidence.delete_from_inventory(swab_lamp)
                store.is_packing_evidence = True
                store.evidence.add_to_inventory(tube_lamp)
                store.is_packing_evidence = False
                store.held_evidence = tube_lamp
                processed = True
                renpy.notify("Placed Lamp blood swab into the tube. You are now holding: {}".format(tube_lamp.name))
            elif held == swab_floor:
                store.evidence.delete_from_inventory(swab_floor)
                store.is_packing_evidence = True
                store.evidence.add_to_inventory(tube_floor)
                store.is_packing_evidence = False
                store.held_evidence = tube_floor
                processed = True
                renpy.notify("Placed floor blood pool swab into the tube. You are now holding: {}".format(tube_floor.name))
            elif held == swab_pool:
                store.evidence.delete_from_inventory(swab_pool)
                store.is_packing_evidence = True
                store.evidence.add_to_inventory(tube_floor)
                store.is_packing_evidence = False
                store.held_evidence = tube_floor
                processed = True
                renpy.notify("Placed floor blood pool swab into the tube. You are now holding: {}".format(tube_floor.name))
        
        # Fallback to checking the inventory (just in case)
        if not processed:
            if swab_lamp in store.evidence._inventory:
                store.evidence.delete_from_inventory(swab_lamp)
                if tube_lamp:
                    store.evidence.add_to_inventory(tube_lamp)
                    processed = True
                    renpy.notify("Placed Lamp blood swab into the tube. Tube with Swab (Lamp) added to evidence!")
            
            elif swab_floor in store.evidence._inventory:
                store.evidence.delete_from_inventory(swab_floor)
                if tube_floor:
                    store.evidence.add_to_inventory(tube_floor)
                    processed = True
                    renpy.notify("Placed floor blood pool swab into the tube. Tube with Swab (Floor) added to evidence!")
            
            elif swab_pool in store.evidence._inventory:
                store.evidence.delete_from_inventory(swab_pool)
                if tube_floor:
                    store.evidence.add_to_inventory(tube_floor)
                    processed = True
                    renpy.notify("Placed floor blood pool swab into the tube. Tube with Swab (Floor) added to evidence!")
        
        if not processed:
            renpy.notify("You need to collect a blood sample on a swab first.")
        
        store.active_tool = None
        store.default_mouse = "default"
        renpy.restart_interaction()

    def use_scalebar():
        if store.active_tool == "scalebar":
            reset_tool()
            renpy.notify("Scalebar unequipped.")
        else:
            store.active_tool = "scalebar"
            store.default_mouse = "scalebar"
            renpy.notify("Scalebar equipped. Mouse cursor changed.")
            renpy.hide_screen("inventory")
            renpy.show_screen("open_inv")

    def click_shoeprint_direct_or_scalebar():
        gel_item_check = store.evids.get("Gel-Lifted Shoeprint")
        is_lifted = gel_item_check in store.evidence._inventory if gel_item_check else False
        
        if store.active_tool == "scalebar":
            if is_lifted:
                renpy.notify("The shoeprint has already been lifted.")
                store.active_tool = None
                store.default_mouse = "default"
                renpy.restart_interaction()
                return
            store.scalebar_placed = True
            renpy.notify("Scalebar placed next to shoeprint.")
            store.active_tool = None
            store.default_mouse = "default"
            renpy.restart_interaction()
        elif store.active_tool == "camera":
            if is_lifted:
                renpy.notify("The shoeprint has already been lifted. You cannot photograph it.")
                store.active_tool = None
                store.default_mouse = "default"
                renpy.restart_interaction()
                return
            if store.scalebar_placed:
                open_crime_scene_camera(
                    "shoeprint_scale",
                    already_msg="You already have a photo with the scalebar.",
                )
            else:
                open_crime_scene_camera(
                    "shoeprint",
                    already_msg="You already have a photo without the scalebar.",
                )
        elif store.active_tool == "gel_lifter":
            gel_item = store.evids.get("Gel-Lifted Shoeprint")
            if gel_item in store.evidence._inventory:
                renpy.notify("You have already lifted this shoeprint.")
            else:
                if gel_item:
                    photo_normal = store.evids.get("Photo of Shoeprint")
                    photo_scale = store.evids.get("Photo of Shoeprint with Scalebar")
                    if (photo_normal not in store.evidence._inventory) or (photo_scale not in store.evidence._inventory):
                        store.evidence_wrong_moves += 1
                        
                    store.evidence.add_to_inventory(gel_item)
                    renpy.notify("Gel-Lifted Shoeprint collected as evidence!")
                    store.active_tool = None
                    store.default_mouse = "default"
                    renpy.restart_interaction()
        elif store.active_tool is None:
            if store.scalebar_placed:
                store.scalebar_placed = False
                renpy.notify("Scalebar removed.")
                renpy.restart_interaction()

    def click_blood_splatter_direct():
        if store.active_tool == "camera":
            open_crime_scene_camera("blood_splatter")

    def click_lamp_far_direct():
        if store.active_tool == "camera":
            open_crime_scene_camera("lamp_far")

    def click_lamp_direct():
        if store.active_tool == "camera":
            open_crime_scene_camera("lamp_close")

    def click_lamp_blood_direct():
        handle_blood_hotspot("lamp")

    def click_floor_blood_direct():
        handle_blood_hotspot("floor")

    def use_tool_generic(tool_id, cursor_name):
        if store.active_tool == tool_id:
            reset_tool()
            renpy.notify("{} unequipped.".format(tool_id.replace("_", " ").title()))
        else:
            store.active_tool = tool_id
            store.default_mouse = cursor_name
            renpy.notify("{} equipped.".format(tool_id.replace("_", " ").title()))
            renpy.hide_screen("inventory")
            renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def install_camera_attachment(flag_name, label, already_msg):
        """Install a fingerprint-camera accessory onto the camera body."""
        if getattr(store, flag_name, False):
            renpy.notify(already_msg)
            reset_tool()
            renpy.hide_screen("inventory")
            renpy.show_screen("open_inv")
            renpy.restart_interaction()
            return

        setattr(store, flag_name, True)
        renpy.notify("{} attached to the camera.".format(label))
        reset_tool()
        renpy.hide_screen("inventory")
        renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def fingerprint_camera_attachments_ready():
        return (
            store.fingerprint_camera_equip_lens
            and store.fingerprint_camera_equip_flashlight
            and store.fingerprint_camera_equip_tripod
        )

    def missing_fingerprint_camera_attachment():
        if not store.fingerprint_camera_equip_lens:
            return "Macro Lens"
        if not store.fingerprint_camera_equip_flashlight:
            return "Camera Flashlight"
        if not store.fingerprint_camera_equip_tripod:
            return "Tripod"
        return None

    def use_black_granular_powder():
        use_tool_generic("black_granular_powder", "black_granular_powder")

    def use_gray_granular_powder():
        use_tool_generic("gray_granular_powder", "gray_granular_powder")

    def use_gray_magnetic_powder():
        use_tool_generic("gray_magnetic_powder", "gray_magnetic_powder")

    def use_hungarian_red():
        use_tool_generic("hungarian_red", "hungarian_red")

    def use_distilled_water():
        use_tool_generic("distilled_water", "distilled_water")

    def use_roller():
        use_tool_generic("roller", "roller")

    def use_gel_lifter():
        use_tool_generic("gel_lifter", "gel_lifter")

    def use_fingerprint_tape():
        use_tool_generic("fingerprint_tape", "fingerprint_tape")

    def use_macro_lens():
        install_camera_attachment(
            "fingerprint_camera_equip_lens",
            "Macro Lens",
            "The Macro Lens is already attached to the camera.",
        )

    def use_pencil_crayon():
        use_tool_generic("pencil_crayon", "pencil_crayon")

    def use_camera_flashlight():
        install_camera_attachment(
            "fingerprint_camera_equip_flashlight",
            "Camera Flashlight",
            "The Camera Flashlight is already attached to the camera.",
        )

    def use_tripod():
        install_camera_attachment(
            "fingerprint_camera_equip_tripod",
            "Tripod",
            "The Tripod is already attached to the camera.",
        )

    def use_backing_card():
        use_tool_generic("backing_card", "backing_card")

    def use_methanol():
        use_tool_generic("methanol", "methanol")

    def use_phenolphthalein():
        use_tool_generic("phenolphthalein", "phenolphthalein")

    def use_hydrogen_peroxide():
        use_tool_generic("hydrogen_peroxide", "hydrogen_peroxide")

    def use_column():
        """Lab spin-column / collection-tube column steps."""
        renpy.hide_screen("inventory")
        renpy.hide_screen("inventory_info")
        renpy.hide_screen("open_inv")
        renpy.jump("new_tube")

    def use_collection_tube():
        """Collection-tube steps in the extraction checklist."""
        renpy.hide_screen("inventory")
        renpy.hide_screen("inventory_info")
        renpy.hide_screen("open_inv")
        renpy.jump("new_tube")

    def use_lab_ethanol():
        """Ethanol additions during extraction — plays out as a pour mini-game."""
        renpy.hide_screen("inventory")
        renpy.hide_screen("inventory_info")
        renpy.hide_screen("open_inv")
        renpy.jump("ethanol_pour_start")

    def use_lab_tube():
        """Empty tube for negative-control prep, or column/tube transfer steps."""
        renpy.hide_screen("inventory")
        renpy.hide_screen("inventory_info")
        if renpy.get_screen("swab_screen"):
            prep_start_negative()
            renpy.show_screen("open_inv")
            return
        renpy.hide_screen("open_inv")
        renpy.jump("new_tube")

    def use_lab_trash():
        """Discard column at the end of extraction."""
        renpy.hide_screen("inventory")
        renpy.hide_screen("inventory_info")
        renpy.hide_screen("open_inv")
        renpy.jump("discard_sample")

    # ---- Kastle–Meyer presumptive blood test ----

    BLOOD_TEST_LOCATIONS = ("lamp", "floor", "pool")
    BLOOD_TEST_REAGENTS = ("methanol", "phenolphthalein", "hydrogen_peroxide")
    # Correct procedure order (used only for silent scoring — never shown to player).
    BLOOD_TEST_CORRECT_ORDER = ("methanol", "phenolphthalein", "hydrogen_peroxide")
    BLOOD_TEST_REAGENT_BITS = {
        "methanol": 1,
        "phenolphthalein": 2,
        "hydrogen_peroxide": 4,
    }
    BLOOD_TEST_ALL_BITS = 7
    BLOOD_TEST_LABELS = {
        "lamp": "lamp blood stain",
        "floor": "floor blood pool",
        "pool": "floor blood pool",
    }
    BLOOD_TEST_SWAB_ITEMS = {
        "lamp": "Swab with Blood (Lamp)",
        "floor": "Swab with Blood (Floor)",
        # Pool and floor are the same evidence sample.
        "pool": "Swab with Blood (Floor)",
    }

    def blood_test_mask_attr(location):
        return "blood_test_{}_mask".format(location)

    def blood_test_order_attr(location):
        return "blood_test_{}_order".format(location)

    def blood_test_positive_attr(location):
        return "blood_test_{}_positive".format(location)

    def blood_test_mistakes_attr(location):
        return "blood_test_{}_mistakes".format(location)

    def get_blood_test_mask(location):
        return getattr(store, blood_test_mask_attr(location), 0)

    def get_blood_test_order(location):
        return getattr(store, blood_test_order_attr(location), "") or ""

    def get_blood_test_positive(location):
        return bool(getattr(store, blood_test_positive_attr(location), False))

    def set_blood_test_mask(location, mask):
        setattr(store, blood_test_mask_attr(location), mask)

    def set_blood_test_order(location, order):
        setattr(store, blood_test_order_attr(location), order)

    def set_blood_test_positive(location, value):
        setattr(store, blood_test_positive_attr(location), value)

    def get_blood_test_mistakes(location):
        return getattr(store, blood_test_mistakes_attr(location), 0)

    def add_blood_test_mistake(location):
        setattr(
            store,
            blood_test_mistakes_attr(location),
            get_blood_test_mistakes(location) + 1,
        )

    def blood_test_has_reagent(location, reagent):
        bit = BLOOD_TEST_REAGENT_BITS.get(reagent, 0)
        return bool(get_blood_test_mask(location) & bit)

    def blood_test_applied_count(location):
        mask = get_blood_test_mask(location)
        return bin(mask).count("1")

    def blood_test_game_score(location):
        """Per-location mini-game score; incorrect procedure quietly costs points."""
        return max(0, 100 - (get_blood_test_mistakes(location) * 25))

    def reset_blood_test_sequence(location):
        set_blood_test_mask(location, 0)
        set_blood_test_order(location, "")
        set_blood_test_positive(location, False)

    def blood_test_instruction(location):
        """Vague guidance only — never names solutions or order."""
        if get_blood_test_positive(location):
            return (
                "A pink color appeared. This is a presumptive positive only — "
                "it does not confirm human blood. You may now collect a clean evidentiary swab."
            )
        applied = blood_test_applied_count(location)
        if applied == 0:
            return (
                "Select reagents from your toolbox and apply them to this stain. "
                "Watch the swab for a reaction."
            )
        return "Continue testing this stain. Watch the swab for a reaction."

    def open_blood_test_screen(location):
        store.active_blood_test_location = location
        renpy.hide_screen("inventory")
        renpy.show_screen("blood_test_screen", location=location)
        renpy.restart_interaction()

    def close_blood_test_screen():
        renpy.hide_screen("blood_test_screen")
        store.active_blood_test_location = ""
        if not renpy.get_screen("inventory"):
            renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def apply_blood_test_reagent(location, reagent):
        """Apply any unused reagent. Any order is accepted; incorrect order is scored quietly."""
        if location not in BLOOD_TEST_LOCATIONS:
            return

        if reagent not in BLOOD_TEST_REAGENT_BITS:
            return

        if get_blood_test_positive(location):
            renpy.notify(
                "Presumptive testing is already complete for the {}. Collect a swab.".format(
                    BLOOD_TEST_LABELS[location]
                )
            )
            reset_tool()
            return

        if blood_test_has_reagent(location, reagent):
            renpy.notify("That solution was already applied here.")
            reset_tool()
            return

        bit = BLOOD_TEST_REAGENT_BITS[reagent]
        new_mask = get_blood_test_mask(location) | bit
        set_blood_test_mask(location, new_mask)

        order = get_blood_test_order(location)
        if order:
            order = order + "|" + reagent
        else:
            order = reagent
        set_blood_test_order(location, order)

        renpy.notify("Solution applied.")

        if new_mask == BLOOD_TEST_ALL_BITS:
            applied_order = tuple(order.split("|"))
            if applied_order != BLOOD_TEST_CORRECT_ORDER:
                # Accept incorrect procedure, but record it without tutoring the player.
                store.evidence_wrong_moves += 1
                store.evidence_score = max(0, store.evidence_score - 10)
                add_blood_test_mistake(location)

            set_blood_test_positive(location, True)
            renpy.notify(
                "Pink reaction on the {}. Presumptive positive.".format(
                    BLOOD_TEST_LABELS[location]
                )
            )
            reset_tool()
            # Show the result panel only after all three solutions are applied.
            open_blood_test_screen(location)
            return

        reset_tool()
        # Mid-test applications stay silent — inspect by clicking the stain.

    def collect_blood_swab(location):
        item_name = BLOOD_TEST_SWAB_ITEMS.get(location)
        item = store.evids.get(item_name) if item_name else None
        if item is None:
            renpy.notify("Missing swab evidence definition.")
            return

        if item in store.evidence._inventory:
            renpy.notify("You already collected this sample.")
            reset_tool()
            renpy.restart_interaction()
            return

        store.evidence.add_to_inventory(item)
        renpy.notify(
            "{} collected! Place it in a tube from your toolbox.".format(item_name)
        )
        reset_tool()
        renpy.restart_interaction()

    def handle_blood_hotspot(location):
        """Route blood hotspot clicks: reagents, swab collection, or inspect panel."""
        tool = store.active_tool

        if tool in BLOOD_TEST_REAGENTS:
            apply_blood_test_reagent(location, tool)
            return

        if tool == "swab_pack":
            if not get_blood_test_positive(location):
                store.evidence_wrong_moves += 1
                store.evidence_score = max(0, store.evidence_score - 10)
                reset_tool()
                renpy.call_in_new_context("nina_blood_test_required_warning")
                return
            collect_blood_swab(location)
            return

        # Bare click on the stain: open the inspect / reaction panel only.
        open_blood_test_screen(location)

    def click_pool_blood_direct():
        handle_blood_hotspot("pool")

    def click_pool_photo_direct():
        if store.active_tool == "camera":
            open_crime_scene_camera("blood_pool")

    def submit_scalebar_label(is_correct=True):
        if not is_correct:
            store.evidence_wrong_moves += 1
            store.evidence_score = max(0, store.evidence_score - 10)
            renpy.notify("Incorrect scale selected! (Mistake recorded)")
        else:
            renpy.notify("Correct scale selected!")
        
        store.fingerprint_scalebar_placed = True
        renpy.hide_screen("scalebar_label_screen")
        reset_tool()
        renpy.restart_interaction()

    def take_fingerprint_photo():
        # Legacy fingerprint camera_setup_screen path — deactivated in favor of
        # the overlay camera module. Kept as a no-op guard if the old screen is shown.
        renpy.hide_screen("camera_setup_screen")
        open_crime_scene_camera("fingerprint")

    def submit_backing_card(is_correct):
        if not is_correct:
            store.evidence_wrong_moves += 1
            renpy.call_in_new_context("nina_backing_card_wrong")
            return
            
        fp_item = store.evids.get("Fingerprint")
        if fp_item:
            development_labels = {
                "black": "Black Granular Powder",
                "white": "Gray Granular Powder",
                "hungarian_red": "Hungarian Red + Distilled Water",
            }
            desc = (
                "A fingerprint recovered from the study lamp.\n"
                "Case: 2026-10A\n"
                "Date: Today\n"
                "Officer: Detective\n"
                "Location: Study Lamp\n"
                "Method: Tape lift (Roller: {}).\n"
                "Development: {}."
            ).format(
                "Yes" if store.fingerprint_roller_used else "No",
                development_labels.get(store.fingerprint_powder, "Unknown")
            )
            fp_item.description = desc
            store.evidence.add_to_inventory(fp_item)
            store.fingerprint_collected = True
            
        renpy.hide_screen("backing_card_form_screen")
        renpy.notify("Fingerprint evidence added to inventory!")
        reset_tool()
        renpy.restart_interaction()

    def collection_letter_grade():
        """Map collection evidence_score to a letter grade."""
        score = getattr(store, "evidence_score", 100)
        if score >= 90:
            return "A"
        if score >= 80:
            return "B"
        if score >= 70:
            return "C"
        if score >= 60:
            return "D"
        return "F"

    def check_lab_transition():
        # Queue Nina's dialogue once at least three items have been collected.
        # A screen timer starts it later so collecting/packing is not interrupted.
        if (
            not store.asked_lab_transition
            and not store.lab_transition_pending
            and len(store.evidence._inventory) >= 3
        ):
            store.lab_transition_pending = True
            renpy.show_screen("deferred_lab_transition")

    def begin_pending_lab_transition():
        if not store.lab_transition_pending:
            renpy.hide_screen("deferred_lab_transition")
            return

        blocking_screens = (
            "evidence_collected_notice",
            "inventory",
            "inventory_info",
            "pack_evidence_screen",
            "camera_setup_screen",
            "camera_preview_ui",
            "photo_score_display",
            "photo_album",
            "photo_viewer",
            "backing_card_form_screen",
            "scalebar_label_screen",
            "blood_test_screen",
            "camera_hint_overlay",
        )

        if any(renpy.get_screen(name) for name in blocking_screens):
            return

        # If the player chose to hold evidence, allow them to finish packing or
        # release it before Nina begins speaking.
        if getattr(store, "held_evidence", None) is not None:
            return

        store.lab_transition_pending = False
        store.asked_lab_transition = True
        renpy.hide_screen("deferred_lab_transition")
        renpy.jump("nina_lab_transition_dialogue")

    def click_fingerprint_hotspot():
        tool = store.active_tool
        
        # Camera: require attachments, then open overlay viewfinder
        if tool == "camera":
            missing = missing_fingerprint_camera_attachment()
            if missing is not None:
                reset_tool()
                renpy.call_in_new_context(
                    "nina_fingerprint_camera_setup_warning",
                    missing,
                )
                renpy.restart_interaction()
                return
            open_crime_scene_camera("fingerprint")
            return
            
        # If swab is used, trigger warning, log mistake, and do NOT collect it
        if tool == "swab_pack":
            store.evidence_wrong_moves += 1
            store.evidence_score = max(0, store.evidence_score - 10)
            renpy.call_in_new_context("nina_fingerprint_swab_warning")
            reset_tool()
            renpy.restart_interaction()
            return
            
        # Powder application (allowed, but flagged by Nina at the end of the scene
        # as a suboptimal method for this metal surface — Hungarian Red + water is
        # the preferred method here).
        if tool in ["black_granular_powder", "gray_granular_powder", "gray_magnetic_powder"]:
            if store.fingerprint_powder or store.fingerprint_dye_applied:
                renpy.notify("This print has already been developed — no need for powder.")
                reset_tool()
                renpy.restart_interaction()
                return

            if tool == "black_granular_powder":
                store.fingerprint_powder = "black"
                store.fingerprint_powder_correct = True
                store.fingerprint_method = "powder"
                renpy.notify("Powder applied, revealing the print.")
                reset_tool()
            elif tool == "gray_granular_powder":
                store.fingerprint_powder = "white"
                store.fingerprint_powder_correct = True
                store.fingerprint_method = "powder"
                renpy.notify("Powder applied, revealing the print.")
                reset_tool()
            elif tool == "gray_magnetic_powder":
                store.evidence_wrong_moves += 1
                store.evidence_score = max(0, store.evidence_score - 10)
                renpy.call_in_new_context("nina_magnetic_powder_warning")
                reset_tool()
            renpy.restart_interaction()
            return

        # Hungarian Red dye — preferred method for this metal surface.
        if tool == "hungarian_red":
            if store.fingerprint_powder or store.fingerprint_dye_applied:
                renpy.notify("This print has already been developed — no need for Hungarian Red.")
                reset_tool()
                renpy.restart_interaction()
                return
            store.fingerprint_dye_applied = True
            renpy.notify("Hungarian Red applied to the print.")
            reset_tool()
            renpy.restart_interaction()
            return

        # Distilled water — rinses the dye and develops the print.
        if tool == "distilled_water":
            if store.fingerprint_powder:
                renpy.notify("This print has already been developed.")
                reset_tool()
                renpy.restart_interaction()
                return
            if not store.fingerprint_dye_applied:
                renpy.notify("Apply Hungarian Red before rinsing with water.")
                renpy.restart_interaction()
                return
            if store.fingerprint_water_applied:
                renpy.restart_interaction()
                return
            store.fingerprint_water_applied = True
            store.fingerprint_powder = "hungarian_red"
            store.fingerprint_powder_correct = True
            store.fingerprint_method = "hungarian_red_water"
            renpy.notify("Water applied, revealing the print.")
            reset_tool()
            renpy.restart_interaction()
            return
            
        # Scalebar
        if tool == "scalebar":
            if not store.fingerprint_scalebar_placed:
                if not store.fingerprint_powder:
                    store.evidence_wrong_moves += 1
                    store.evidence_score = max(0, store.evidence_score - 10)
                renpy.show_screen("scalebar_label_screen")
            renpy.restart_interaction()
            return
            
        # Pencil Crayon
        if tool == "pencil_crayon":
            if not store.fingerprint_circled:
                if not store.fingerprint_powder:
                    store.evidence_wrong_moves += 1
                    store.evidence_score = max(0, store.evidence_score - 10)
                    renpy.notify("Fingerprint circled with pencil crayon (Mistake recorded).")
                else:
                    renpy.notify("Fingerprint circled with pencil crayon.")
                store.fingerprint_circled = True
                reset_tool()
            renpy.restart_interaction()
            return
            
        # Fingerprint Tape
        if tool == "fingerprint_tape":
            if not store.fingerprint_tape_applied:
                if not store.fingerprint_powder:
                    store.evidence_wrong_moves += 1
                    store.evidence_score = max(0, store.evidence_score - 10)
                if not store.fingerprint_scalebar_placed:
                    store.evidence_wrong_moves += 1
                    store.evidence_score = max(0, store.evidence_score - 10)
                if not store.fingerprint_photo_taken:
                    store.evidence_wrong_moves += 1
                    store.evidence_score = max(0, store.evidence_score - 10)
                    
                store.fingerprint_tape_applied = True
                renpy.notify("Fingerprint tape applied over the print.")
                reset_tool()
            renpy.restart_interaction()
            return
            
        # Roller
        if tool == "roller":
            if not store.fingerprint_tape_applied:
                store.evidence_wrong_moves += 1
                store.evidence_score = max(0, store.evidence_score - 10)
                renpy.notify("Mistake: You must apply tape first!")
                reset_tool()
            elif not store.fingerprint_roller_used:
                store.fingerprint_roller_used = True
                renpy.notify("Roller used on the tape to ensure a smooth lift.")
                reset_tool()
            renpy.restart_interaction()
            return
            
        # Backing Card
        if tool == "backing_card":
            if not store.fingerprint_tape_applied:
                store.evidence_wrong_moves += 1
                store.evidence_score = max(0, store.evidence_score - 10)
                renpy.notify("Mistake: You must apply tape before lifting!")
                reset_tool()
            elif not store.fingerprint_transferred:
                store.fingerprint_transferred = True
                renpy.show_screen("backing_card_form_screen")
                reset_tool()
            renpy.restart_interaction()
            return

        # Any other tools do nothing here
        renpy.restart_interaction()

    def use_evidence_bag():
        if getattr(store, "held_evidence", None) is None:
            renpy.notify("You are not holding any evidence to pack.")
            return
            
        if store.evidence_bags_left <= 0:
            renpy.notify("You have no evidence bags left!")
            return
        
        # Check if they are trying to pack a raw swab
        if store.held_evidence.name.startswith("Swab with Blood"):
            # Trigger Nina's warning, record a mistake, and don't open the packing screen!
            store.evidence_wrong_moves += 1
            store.evidence_score = max(0, store.evidence_score - 10)
            renpy.hide_screen("inventory")
            renpy.call_in_new_context("nina_swab_warning")
            # Re-open inventory so they can continue
            renpy.show_screen("inventory")
            renpy.restart_interaction()
            return
            
        # Hide the inventory screen to show the packing screen clearly
        renpy.hide_screen("inventory")
        # Show the packing screen
        renpy.show_screen("pack_evidence_screen")
        renpy.restart_interaction()

    def finish_packing_evidence():
        if not store.bag_sealed:
            # Mistake recorded!
            store.evidence_wrong_moves += 1
            store.evidence_score = max(0, store.evidence_score - 10)
            renpy.notify("Mistake: You forgot to seal the evidence bag!")
        else:
            renpy.notify("Evidence packed and sealed successfully!")
        
        # Modify the held evidence item
        item = store.held_evidence
        item.image_name = "inventory-evidence_bag"
        if store.bag_sealed:
            item.description += "\n(Packed & Sealed)"
        else:
            item.description += "\n(Packed but UNSEALED)"
        
        # Refresh the inventory tab display visually
        store.evidence.refresh_visible_inventory()
        
        # Decrement bags count
        store.evidence_bags_left = max(0, store.evidence_bags_left - 1)
        
        # Reset state
        store.held_evidence = None
        store.bag_sealed = False
        renpy.hide_screen("pack_evidence_screen")
        
        # Re-open inventory to the evidence tab so they can see the newly packed bag!
        if not store.asked_lab_transition:
            store.selected_inventory = store.evidence
            renpy.show_screen("inventory")
        renpy.restart_interaction()

    def toggle_hold_evidence(item):
        # During DNA prep, Use on a collected tube equips it onto the bench.
        if renpy.get_screen("swab_screen") and item is not None:
            if prep_is_add_al_step() or prep_is_add_ate_step() or prep2_bench_tool_active():
                if item.name.startswith("Processed Tube with Swab") or item.name == getattr(
                    store, "NEG_CONTROL_NAME", "Negative Control Tube"
                ):
                    if prep_is_add_ate_step():
                        prep_equip_ate_tube(item)
                    elif prep_is_add_al_step():
                        prep_equip_al_from_inventory(item)
                    else:
                        prep_equip_bench_tube(item)
                    return
                renpy.notify(
                    "Equip your sample tube or Negative Control to add Buffer ATE."
                    if prep_is_add_ate_step()
                    else ("Equip your sample tube or Negative Control to add Buffer AL." if prep_is_add_al_step()
                    else "Equip your sample tube or Negative Control for this reagent.")
                )
                return
            tube_map = getattr(store, "PREP_TUBE_PROCESS_MAP", {})
            if item.name in tube_map:
                prep_equip_from_inventory(item)
                return
            if item.name.startswith("Processed Tube with Swab"):
                renpy.notify("That tube is already prepped. Use it on vortex / centrifuge next.")
                return

        # Centrifuge balance: Use negative control after placing the sample.
        # On other machines, Use equips it like the sample tube (same procedure steps).
        if item is not None and item.name == getattr(store, "NEG_CONTROL_NAME", "Negative Control Tube"):
            if renpy.get_screen("centrifuge"):
                centrifuge_pick_neg_control(item)
                return
            if renpy.get_screen("spinner"):
                spinner_pick_neg_control(item)
                return
            expected = extraction_expected_tool()
            if expected == "al":
                renpy.notify("Open Prep, then Use the Negative Control Tube to add Buffer AL.")
                return
            if expected not in (None, "prep") and not extraction_complete():
                extraction_equip_processed_tube(item)
                return
            renpy.notify("Use the Negative Control Tube on extraction machines, or on a centrifuge to balance.")
            return

        # Post-prep extraction: Use a processed tube to equip it on the machine.
        if item is not None and item.name.startswith("Processed Tube with Swab"):
            expected = extraction_expected_tool()
            if expected == "al":
                renpy.notify("Open Prep, then Use the tube to add Buffer AL.")
                return
            if expected not in (None, "prep") and not extraction_complete():
                extraction_equip_processed_tube(item)
                return

        if getattr(store, "held_evidence", None) == item:
            store.held_evidence = None
            renpy.notify("Unheld: {}".format(item.name))
        else:
            store.held_evidence = item
            if getattr(store, "asked_lab_transition", False):
                renpy.notify("Holding: {}.".format(item.name))
            else:
                renpy.notify("Holding: {}. Open Toolbox to pack it in an Evidence Bag.".format(item.name))
                store.selected_inventory = store.toolbox
        renpy.restart_interaction()
