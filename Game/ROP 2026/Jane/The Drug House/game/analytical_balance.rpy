default weighed_gross = {"sample1": False, "sample2": False, "sample3": False}  # exhibit + packaging
default weighed_net   = {"sample1": False, "sample2": False, "sample3": False}  # drug only, packaging removed
default weighed_rep   = {"sample1": False, "sample2": False, "sample3": False}  # small sample for GC-MS

default drug_weights = {
    "sample1": {"gross": None, "net": None, "rep": None},
    "sample2": {"gross": None, "net": None, "rep": None},
    "sample3": {"gross": None, "net": None, "rep": None},
}

default balance_state       = "zero"    # "zero" or "result"
default balance_result_type = None      # "gross" / "net" / "rep"
default balance_result_drug = None

default weighboat_state  = "empty"      # empty or loaded
default weighboat_sample = None
default spatula_sample   = None

default analytical_balance_done = False
default lab_notebook_given      = False
default ab_pending_messages     = []
default ab_wait_msg             = None

init python:
    _CORRECT_GROSS_WEIGHTS = {"sample1": 106.8340, "sample2": 1268.4721, "sample3": 289.5857}
    _CORRECT_NET_WEIGHTS   = {"sample1": 100.1200,  "sample2": 1255.1050, "sample3": 280.9800}
    _CORRECT_REP_WEIGHTS   = {"sample1": 3.0000,   "sample2": 3.0000,   "sample3": 3.0000}
    _SAMPLE_DISPLAY_NAME   = {"sample1": "Sample 1", "sample2": "Sample 2", "sample3": "Sample 3"}

    def weigh_sample(drug, weight_type):
        global analytical_balance_done, gcms_step
        _label = _SAMPLE_DISPLAY_NAME[drug]

        if weight_type == "gross":
            store.drug_weights[drug]["gross"] = _CORRECT_GROSS_WEIGHTS[drug]
            store.weighed_gross[drug] = True
            store.ab_pending_messages.append(
                "Recorded gross weight (exhibit and packaging) for %s: %.4f g"
                % (_label, _CORRECT_GROSS_WEIGHTS[drug])
            )

        elif weight_type == "net":
            store.drug_weights[drug]["net"] = _CORRECT_NET_WEIGHTS[drug]
            store.weighed_net[drug] = True
            store.ab_pending_messages.append(
                "Recorded net weight (drug material only) for %s: %.4f g"
                % (_label, _CORRECT_NET_WEIGHTS[drug])
            )
            store.ab_pending_messages.append(
                "Remember to take a small representative sample with the spatula for the next weighing."
            )

        else:  # "rep"
            store.drug_weights[drug]["rep"] = _CORRECT_REP_WEIGHTS[drug]
            store.weighed_rep[drug] = True
            store.ab_pending_messages.append(
                "Recorded representative sample weight for %s: %.4f g" % (_label, _CORRECT_REP_WEIGHTS[drug])
            )

        store.balance_result_type = weight_type
        store.balance_result_drug = drug
        store.balance_state = "result"

        if all(store.weighed_gross.values()) and all(store.weighed_net.values()) and all(store.weighed_rep.values()):
            analytical_balance_done = True
            gcms_step = 2
            store.ab_pending_messages.append(
                "All exhibits have had gross, net, and representative sample weights recorded. Solid Phase Extraction is now available."
            )

    def remove_packaging_and_weigh(drug):
        """Narrates removing packaging, then immediately records the net weight
        and shows the net-weight result. Replaces the old drag-based net step."""
        _label = _SAMPLE_DISPLAY_NAME[drug]
        say("You remove the packaging and weigh the sample.", n)
        weigh_sample(drug, "net")

    def sample_bag_drop(drags, drop):
        """Spatula collects a small representative sample from the drug material,
        only once net weight has been recorded."""
        if not drop or not drop.drag_name.endswith("_idle") or drop.drag_name == "weighboat_idle":
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        drug = drop.drag_name.replace("_idle", "")
        if drug not in ("sample1", "sample2", "sample3"):
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if not store.weighed_net[drug]:
            store.ab_pending_messages.append("Record the net weight of the drug material before taking a sample.")
            store.selected_tool = None

        elif store.weighed_rep[drug]:
            store.ab_pending_messages.append("A representative sample has already been taken from this exhibit.")
            store.selected_tool = None

        elif dragged_image == "spatula_idle":
            store.selected_tool = "spatula_powder"
            store.spatula_sample = drug
            renpy.restart_interaction()
            return True

        else:
            store.ab_pending_messages.append("Use the spatula to collect a representative sample.")
            store.selected_tool = None

        renpy.restart_interaction()
        return True

    def weighboat_drop(drags, drop):
        if not drop or drop.drag_name != "weighboat_dropzone":
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if dragged_image == "spatula_powder" and store.weighboat_state == "empty":
            store.weighboat_state  = "loaded"
            store.weighboat_sample = store.spatula_sample
            store.spatula_sample   = None
        else:
            store.ab_pending_messages.append("The weighboat isn't ready for that.")

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def analytical_balance_drop(drags, drop):
        """Handles: sealed evidence bag -> gross weight; loaded weighboat -> representative sample weight."""
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if store.balance_state != "zero":
            store.ab_pending_messages.append("Remove the current item from the balance before weighing another.")
            store.selected_tool = None
            renpy.restart_interaction()
            return True

        if dragged_image == "weighboat_loaded":
            drug = store.weighboat_sample
            if drug and store.weighed_net[drug] and not store.weighed_rep[drug]:
                weigh_sample(drug, "rep")
                store.weighboat_state  = "empty"
                store.weighboat_sample = None
            elif drug and store.weighed_rep[drug]:
                store.ab_pending_messages.append("A representative sample has already been taken from this exhibit.")
            else:
                store.ab_pending_messages.append("Record the net weight before taking a representative sample.")

        elif dragged_image in ("inventory-sample1", "inventory-sample2", "inventory-sample3"):
            drug = dragged_image.replace("inventory-", "")
            if not store.weighed_gross[drug]:
                weigh_sample(drug, "gross")
            else:
                store.ab_pending_messages.append("This exhibit's gross weight has already been recorded.")

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def clear_balance():
        store.balance_state       = "zero"
        store.balance_result_type = None
        store.balance_result_drug = None
        renpy.restart_interaction()
label analytical_balance:
    $ hide_all_lab_screens()
    $ hide_all_inventory()
    $ location = "analytical_balance"
    scene lab_counter_bk
    if not lab_notebook_given:
        $ toolbox.add_to_inventory(tools["Lab Notebook"])
        $ lab_notebook_given = True
        show nina normal1
        n "Every exhibit needs three separate weights, recorded in this exact order."
        n "First, weigh the sealed evidence bag as received. That's the gross weight, exhibit plus packaging."
        n "Once that's recorded, the packaging is removed, and you'll weigh the drug material on its own, which is the net weight."
        n "Only after that can you take a small representative sample for GC-MS analysis and weigh it separately."
        n "Recording gross and net first documents the exhibit exactly as it was received, before anything is altered, which protects chain of custody."
        hide nina normal1
    show screen analytical_balance_screen
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens
    jump analytical_balance_idle

label analytical_balance_idle:
    if ab_pending_messages:
        $ ab_wait_msg = ab_pending_messages.pop(0)
        n normal1 "[ab_wait_msg]"
        jump analytical_balance_idle
    $ renpy.pause(0.2)
    jump analytical_balance_idle