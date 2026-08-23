init -5 python:

    def item_dragging_package(drags):
        global default_mouse
        default_mouse = "hand_grab"

    _IMAGE_TO_DRAG_NAME = {
        "marker_1": "marker_1",
        "marker_2": "marker_2",
        "marker_3": "marker_3",
        "marker_4": "marker_4",
        "marquis_reagent_idle":      "marquis_reagent_idle",
        "scott_reagent_idle":        "scott_reagent_idle",
        "spatula_idle":              "spatula_idle",
        "tube_idle":                 "tube_idle",
        "evidence_bag_idle":         "evidence_bag_idle",
        "tamper_evident_tape_idle":  "tamper_evident_tape_idle",
        "backing_card_idle":         "backing_card_idle",
        "tape_idle":                 "tape_idle",
        "uv_light_idle":             "uv_light_idle",
        "magnetic_powder_idle":      "magnetic_powder_idle",
        "scalebar_idle":             "scalebar_idle",
        "pen_idle":                  "pen_idle"
    }

    _TOOL_NAME_TO_IMAGE = {
        "Evidence Markers":     "marker_dynamic",
        "Marquis Reagent":      "marquis_reagent_idle",
        "Scott Reagent":        "scott_reagent_idle",
        "Spatula":              "spatula_idle",
        "Tube":                 "tube_idle",
        "Evidence Bag":         "evidence_bag_idle",
        "Tamper Evident Tape":  "tamper_evident_tape_idle",
        "Backing Card":         "backing_card_idle",
        "Tape":                 "tape_idle",
        "UV Light":             "uv_light_idle",
        "Magnetic Powder":      "magnetic_powder_idle",
        "Scalebar":             "scalebar_idle",
        "Pen":                  "pen_idle"
    }

    def _get_current_step():
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_step = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_step == idx:
                    return s
                drag_step += 1
        return None

    def _total_drag_steps(item):
        return sum(1 for s in valid_evidence_steps.get(item, []) if isinstance(s, dict))

    def _current_drop_image():
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_index == idx:
                    return list(s.keys())[0]
                drag_index += 1
        return None

    def _marker_after_index(item, idx):
        """
        Return the string marker immediately following dict step at position idx,
        or None if the next entry is another dict or end of list.
        """
        steps = valid_evidence_steps.get(item, [])
        drag_count = 0
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                if drag_count == idx:
                    if i + 1 < len(steps) and isinstance(steps[i + 1], str):
                        return steps[i + 1]
                    return None
                drag_count += 1
        return None

    def _quiz_is_next():
        if testing_item is None:
            return False
        idx = store.evidence_step_index.get(testing_item, 0)
        return _marker_after_index(testing_item, idx) == "quiz"

    def _fingerprint_collect_is_next():
        """
        True only when the COMPLETED step (idx - 1) has fingerprint_collect
        immediately after it — meaning we just finished the tamper tape step
        that precedes the fingerprint_collect marker.
        """
        if testing_item is None:
            return False
        idx = store.evidence_step_index.get(testing_item, 0)
        if idx == 0:
            return False
        # Check marker after the step we just completed (idx - 1)
        return _marker_after_index(testing_item, idx - 1) == "fingerprint_collect"

    def _collect_step_is_next():
        if testing_item is None:
            return False
        idx = store.evidence_step_index.get(testing_item, 0)
        if idx == 0:
            return False
        return _marker_after_index(testing_item, idx - 1) == "collect_step"

    def _advance_step():
        idx = store.evidence_step_index.get(testing_item, 0)
        store.evidence_step_index[testing_item] = idx + 1

    def generic_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name
        step = _get_current_step()

        if step is None:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        correct_tool_image = list(step.values())[0]

        if correct_tool_image == "marker_dynamic":
            order = store.evidence_visited_order
            expected = "marker_" + str(order.index(store.testing_item) + 1)
            if dragged_image != expected:
                renpy.notify("That's not the right tool for this step.")
                store.selected_tool = None
                renpy.hide_screen("drug_processing_screen")
                renpy.restart_interaction()
                return False
            store.evidence_marker_placed[store.testing_item] = True
            _advance_step()

        elif isinstance(correct_tool_image, list):
            # Reagent packet step: dragged_image is the TOOL (scott/marquis), not the drop target
            if dragged_image not in correct_tool_image:
                renpy.notify("That's not the right tool for this step.")
                store.selected_tool = None
                renpy.hide_screen("drug_processing_screen")
                renpy.restart_interaction()
                return False

            if dragged_image == "marquis_reagent_idle":
                store.current_reagent[store.testing_item] = "marquis"
                store.quiz_pending = True
                store.selected_tool = None
                renpy.restart_interaction()
                return True
            else:  # scott_reagent_idle
                store.current_reagent[store.testing_item] = "scott"
                _advance_step()

        elif dragged_image != correct_tool_image:
            renpy.notify("That's not the right tool for this step.")
            store.selected_tool = None
            renpy.hide_screen("drug_processing_screen")
            renpy.restart_interaction()
            return False

        else:
            _advance_step()

        new_idx = store.evidence_step_index.get(store.testing_item, 0)
        marker = _marker_after_index(store.testing_item, new_idx - 1)

        if marker == "quiz":
            store.quiz_pending = True
        elif marker == "fingerprint_collect":
            store.fingerprint_collect_ready = True
        elif marker == "collect_step":
            store.collect_step_ready = True

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def _use_tool(tool_name):
        image_name = _TOOL_NAME_TO_IMAGE.get(tool_name)
        if image_name is None:
            renpy.notify("This tool can't be used here.")
            return

        # Crime-scene evidence testing requires an inspected item first.
        if store.location not in ("analytical_balance",) and store.testing_item is None:
            renpy.notify("Select an evidence item first.")
            return

        store.selected_tool = image_name
        renpy.restart_interaction()

    def use_evidence_markers():
        if testing_item is None:
            renpy.notify("Select an evidence item first.")
            return
        order = store.evidence_visited_order
        if testing_item not in order:
            renpy.notify("This evidence hasn't been logged yet.")
            return
        num = order.index(testing_item) + 1
        image_name = "marker_" + str(num)
        store.selected_tool = image_name
        renpy.restart_interaction()

    def use_marquis_reagent():      _use_tool("Marquis Reagent")
    def use_scott_reagent():        _use_tool("Scott Reagent")
    def use_tube():                 _use_tool("Tube")
    def use_evidence_bag():         _use_tool("Evidence Bag")
    def use_tamper_evident_tape():  _use_tool("Tamper Evident Tape")
    def use_spatula():              _use_tool("Spatula")
    def use_backing_card():         _use_tool("Backing Card")
    def use_tape():                 _use_tool("Tape")
    def use_uv_light():             _use_tool("UV Light")
    def use_magnetic_powder():      _use_tool("Magnetic Powder")
    def use_scalebar():             _use_tool("Scalebar")
    def use_pen():                  _use_tool("Pen")

    def import_firearm_fingerprint():
        global imported_print
        if location == "afis":
            if not ca_chamber_done:
                say("Process the firearm in the CA chamber before importing a print.")
                return
            imported_print = "firearm_fingerprint"
            renpy.jump("import_print")
        else:
            say("Bring this to AFIS to import it.")

    def use_distilled_water():
        if location != "ca_chamber" and location != "solid_phase_extraction":
            say("Bring this to the CA chamber or Solid Phase Extraction to use it.")
            return
        if location == "solid_phase_extraction":
            renpy.jump("useWater")
        store.selected_tool = "toolbox-distilled_water"
        renpy.restart_interaction()

    def use_superglue():
        if location != "ca_chamber":
            say("Bring this to the CA chamber to use it.")
            return
        store.selected_tool = "toolbox-superglue"
        renpy.restart_interaction()

    def use_firearm():
        if location != "ca_chamber":
            say("Bring this to the CA chamber to use it.")
            return
        if ca_chamber_state != "empty":
            say("The CA chamber isn't ready for the firearm right now.")
            return
        store.selected_tool = "inventory-firearm"
        renpy.restart_interaction()

    def use_methanol():
        if location != "solid_phase_extraction":
            say("Bring this to Solid Phase Extraction to use it.")
            return
        renpy.jump("useMethanol")

    def use_step3():
        if location != "solid_phase_extraction":
            say("Bring this to Solid Phase Extraction to use it.")
            return
        renpy.jump("useStep3")

    def use_01formic():
        if location != "solid_phase_extraction":
            say("Bring this to Solid Phase Extraction to use it.")
            return
        renpy.jump("use01Formic")

    def use_5amm():
        if location != "solid_phase_extraction":
            say("Bring this to Solid Phase Extraction to use it.")
            return
        renpy.jump("use5Amm")

    def use_sample1():
        if location == "analytical_balance":
            analytical_balance_use_sample("sample1")
        elif location == "solid_phase_extraction":
            renpy.jump("useSample1")
        else:
            say("Bring this to the balance or SPE to use it.")

    def use_sample2():
        if location == "analytical_balance":
            analytical_balance_use_sample("sample2")
        elif location == "solid_phase_extraction":
            renpy.jump("useSample2")
        else:
            say("Bring this to the balance or SPE to use it.")

    def use_sample3():
        if location == "analytical_balance":
            analytical_balance_use_sample("sample3")
        elif location == "solid_phase_extraction":
            renpy.jump("useSample3")
        else:
            say("Bring this to the balance or SPE to use it.")

    def analytical_balance_use_sample(drug):
        if store.location != "analytical_balance":
            say("Bring this to the balance to weigh it.")
            return
        if store.balance_state != "zero":
            say("Remove the current item from the balance before weighing another.")
            return
        if store.weighed_gross[drug]:
            say("This sample's gross weight has already been recorded.")
            return
        store.selected_tool = "inventory-" + drug
        renpy.restart_interaction()

    def use_prepared_sample1():
        gcms_use_prepared_sample("sample1")

    def use_prepared_sample2():
        gcms_use_prepared_sample("sample2")

    def use_prepared_sample3():
        gcms_use_prepared_sample("sample3")

    def gcms_use_prepared_sample(drug):
        if location != "gcms":
            say("Bring this to the GC-MS to analyze it.")
            return
        if gcms_step != 3:
            say("The GC-MS isn't ready for a sample right now.")
            return
        if drug != gcms_current_drug:
            say("That's not the sample queued for analysis.")
            return
        store.gcms_step = 4
        say("Sample loaded into the GC autosampler.")
        renpy.restart_interaction()
    
    def say(what, who=None):
        renpy.invoke_in_new_context(renpy.say, who, what)

    def view_lab_notebook():
        renpy.show_screen("lab_notebook")

