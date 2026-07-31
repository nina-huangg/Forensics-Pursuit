default gcms_step = 1
default gcms_queue_done = {"sample1": False, "sample2": False, "sample3": False}
default gcms_current_drug = None
default gcms_ref_index = 0

init python:
    _SAMPLE_DISPLAY_NAME = {"sample1": "Sample 1", "sample2": "Sample 2", "sample3": "Sample 3"}

    def say(what, who=None):
        renpy.invoke_in_new_context(renpy.say, who, what)

    def get_next_gcms_drug():
        """Return the next prepared sample still awaiting GC-MS analysis, or None."""
        prepared = {
            "sample1":      has_SPE_sample1,
            "sample2":      has_SPE_sample2,
            "sample3":      has_SPE_sample3,
        }
        for drug in ("sample1", "sample2", "sample3"):
            if prepared[drug] and not gcms_queue_done[drug]:
                return drug
        return None

    def gcms_autosampler_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name
        expected = {
            "sample1":      "inventory-prepared_sample1",
            "sample2":      "inventory-prepared_sample2",
            "sample3":      "inventory-prepared_sample3",
        }[store.gcms_current_drug]

        if dragged_image == expected:
            store.gcms_step = 4
            say("Sample loaded into the GC autosampler.")
        else:
            say("That's not the right prepared sample.")
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        store.selected_tool = None
        renpy.restart_interaction()
        return True

label gcms:
    $ hide_all_lab_screens()
    $ location = "gcms"

    if not analytical_balance_done or choice_SPE != "COMPLETED":
        show nina talk
        n "You'll need to weigh all three presumed samples on the analytical balance and complete Solid Phase Extraction for each before you can begin GC-MS analysis."
        hide nina talk
        jump materials_lab

    if get_next_gcms_drug() is None:
        show nina talk
        n "All samples have been run through the GC-MS. Great work."
        hide nina talk
        jump materials_lab

    scene gcms_background
    show nina talk
    n "Which prepared sample would you like to analyze?"
    hide nina talk

    menu:
        "Sample 1" if has_SPE_sample1 and not gcms_queue_done["sample1"]:
            $ gcms_current_drug = "sample1"
        "Sample 2" if has_SPE_sample2 and not gcms_queue_done["sample2"]:
            $ gcms_current_drug = "sample2"
        "Sample 3" if has_SPE_sample3 and not gcms_queue_done["sample3"]:
            $ gcms_current_drug = "sample3"

    $ gcms_step = 3
    show nina normal1
    n "Head over to the autosampler and insert the sample vial to begin."
    hide nina normal1

    show screen gcms_open_autosampler zorder 0
    show screen gcms_checklist zorder 10
    show screen inventory zorder 20
    show screen back_button_screen('materials_lab') onlayer over_screens
    jump gcms_idle

label gcms_load_autosampler:
    hide screen gcms_open_autosampler
    show screen gcms_screen zorder 0
    show screen gcms_checklist zorder 10
    show screen inventory zorder 20
    jump gcms_idle

label gcms_idle:
    $ renpy.pause(3600)
    jump gcms_idle

label gcms_set_time:
    hide screen gcms_screen
    "Set the GC-MS to run for how many minutes?"
    menu:
        "4 minutes":
            "Wrong."
            jump gcms_set_time
        "6 minutes":
            jump gcms_run
        "12 minutes":
            "Wrong."
            jump gcms_set_time

label gcms_run:
    $ gcms_step = 5
    "Running the sample through the GC-MS..."
    "A chromatogram appears on the monitor, displaying the separated compounds of the sample."

    $ gcms_step = 6
    "You note the relative retention times (RRT) where the major peaks appear."

    $ gcms_step = 7
    "Generating the mass spectrum for the sample..."
    "The mass spectrum for the sample has been generated."

    show nina normal1
    n "A lab certified cocaine reference standard has already been analyzed under the same GC-MS laboratory conditions used for the evidence samples."
    hide nina normal1
    show nina thinknote1
    n "Use the reference chromatogram and mass spectrum to identify the most prominent peak in the evidence samples and determine whether the unknown samples are consistent with cocaine."
    hide nina thinknote1

    $ gcms_step = 8
    show screen gcms_screen zorder 0
    show screen gcms_checklist zorder 10
    jump gcms_idle

label gcms_compare_interface:
    hide screen gcms_screen
    $ gcms_ref_index = 0
    call screen gcms_compare_screen

label gcms_compare_prev:
    $ gcms_ref_index = (gcms_ref_index - 1) % 3
    call screen gcms_compare_screen

label gcms_compare_next:
    $ gcms_ref_index = (gcms_ref_index + 1) % 3
    call screen gcms_compare_screen

label gcms_identify:
    $ ref_keys = ["cocaine", "mdma", "meth"]
    $ chosen = ref_keys[gcms_ref_index]
    $ sample_label = _SAMPLE_DISPLAY_NAME[gcms_current_drug]

    if chosen == "cocaine":
        $ gcms_step = 9
        "The RRT and mass spectrum for [sample_label] match the reference standard for cocaine."
        "You've identified [sample_label] as cocaine."

        $ presumptive_result = evidence_found.get(gcms_current_drug + "_presumptive", False)
        show nina thinknote1
        n "Does this result match your presumptive field tests from evidence collection?"
        menu:
            "Yes, it is consistent":
                if presumptive_result:
                    n "Correct! The presumptive test was consistent with this result."
                else:
                    n "Incorrect. The presumptive test result does not match this GC-MS identification."
                    jump gcms_identify
            "No, it isn't consistent":
                if not presumptive_result:
                    n "Correct! The presumptive test was inconsistent with this result."
                else:
                    n "Incorrect. The presumptive test result matches this GC-MS identification."
                    jump gcms_identify
        hide nina thinknote1
        $ gcms_queue_done[gcms_current_drug] = True
        $ evidence.add_to_inventory(evids["Identified Cocaine " + sample_label])
        $ gcms_current_drug = None
        jump gcms
    else:
        "That is not the correct reference standard for [sample_label]. Review the chromatogram and mass spectrum again."
        call screen gcms_compare_screen