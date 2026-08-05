default weighed_net    = {"sample1": False, "sample2": False, "sample3": False}
default weighed_gross   = {"sample1": False, "sample2": False, "sample3": False}
default drug_weights = {
    "sample1": {"net": None, "gross": None},
    "sample2": {"net": None, "gross": None},
    "sample3": {"net": None, "gross": None},
}

default balance_state       = "zero"    # zero or result
default balance_result_type = None      # "net" for small sample or "gross" for the whole bag
default balance_result_drug = None

default weighboat_state  = "empty"      # empty or loaded
default weighboat_sample = None         # which sample is currently on the weighboat
default spatula_sample   = None         # which sample's tube the spatula just scooped from

default analytical_balance_done = False
default lab_notebook_given      = False
default ab_pending_messages     = []
default ab_wait_msg             = None

init python:
    _CORRECT_NET_WEIGHTS   = {"sample1": 2.6703, "sample2": 1.8415, "sample3": 3.1296}
    _CORRECT_GROSS_WEIGHTS = {"sample1": 106.8340, "sample2": 1268.4721, "sample3": 289.5857}
    _SAMPLE_DISPLAY_NAME   = {"sample1": "Sample 1", "sample2": "Sample 2", "sample3": "Sample 3"}

    def weigh_sample(drug, weight_type):
        global analytical_balance_done, gcms_step
        _label = _SAMPLE_DISPLAY_NAME[drug]

        if weight_type == "net":
            store.drug_weights[drug]["net"] = _CORRECT_NET_WEIGHTS[drug]
            store.weighed_net[drug] = True
            store.ab_pending_messages.append(
                "Recorded net weight (pure sample) for presumed %s in lab notebook: %.4f g"
                % (_label, _CORRECT_NET_WEIGHTS[drug])
            )
        else:
            store.drug_weights[drug]["gross"] = _CORRECT_GROSS_WEIGHTS[drug]
            store.weighed_gross[drug] = True
            store.ab_pending_messages.append(
                "Recorded gross weight (sealed evidence bag) for presumed %s in lab notebook: %.4f g"
                % (_label, _CORRECT_GROSS_WEIGHTS[drug])
            )

        store.balance_result_type = weight_type
        store.balance_result_drug = drug
        store.balance_state = "result"

        if all(store.weighed_net.values()) and all(store.weighed_gross.values()):
            analytical_balance_done = True
            gcms_step = 2
            store.ab_pending_messages.append(
                "All samples have been weighed (net and gross) and recorded. Solid Phase Extraction is now available."
            )

    def sample_bag_drop(drags, drop):
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
        _label = _SAMPLE_DISPLAY_NAME[drug]

        if dragged_image == "spatula_idle" and not store.weighed_net[drug]:
            store.selected_tool = "spatula_powder"
            store.spatula_sample = drug
        elif store.weighed_net[drug]:
            store.ab_pending_messages.append("%s's net weight has already been recorded." % _label)
            store.selected_tool = None
        else:
            store.ab_pending_messages.append("Use the spatula to collect a powder sample from the bag.")
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
            if drug and not store.weighed_net[drug]:
                weigh_sample(drug, "net")
                store.weighboat_state  = "empty"
                store.weighboat_sample = None
            else:
                store.ab_pending_messages.append("This sample's net weight has already been recorded.")
            
        elif dragged_image in ("inventory-sample1", "inventory-sample2", "inventory-sample3"):
            drug = dragged_image.replace("inventory-", "")
            if not store.weighed_gross[drug]:
                weigh_sample(drug, "gross")
            else:
                store.ab_pending_messages.append("%s's gross weight has already been recorded." % _SAMPLE_DISPLAY_NAME[drug])

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
        n "In the analytical balance section you'll weigh each presumed drug sample twice."
        n "First, use the spatula to take a sample from the bag and place it on the weighboat."
        n "Weigh the small sample to get the net weight."
        n "Then, weigh the whole sealed evidence bag to get the gross weight."
        n "Don't forget; both weights should be recorded in your lab notebook!"
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