default gcms_step = 1
default gcms_queue_done = {"sample1": False, "sample2": False, "sample3": False}
default gcms_current_drug = None
default gcms_selected_peak = None
default gcms_identified_adulterants = {"sample1": set(), "sample2": set(), "sample3": set()}

init python:
    _SAMPLE_DISPLAY_NAME = {"sample1": "Sample 1", "sample2": "Sample 2", "sample3": "Sample 3"}

    # Every evidence sample shows the same four peaks in this dataset as they are all cocaine

    _GCMS_PEAKS = ["lidocaine", "caffeine", "cocaine", "levamisole"]
    _GCMS_PEAK_POSITIONS = {
        "lidocaine":  0.475,   # retention time 13.902
        "caffeine":   0.505,   # retention time 14.461
        "cocaine":    0.55,   # retention time 15.425
        "levamisole": 0.60,   # retention time 16.365
    }
    _GCMS_ADULTERANT_NOTE = {
        "lidocaine":  "Lidocaine is a local anesthetic commonly used as a cutting agent to mimic cocaine's numbing effect.",
        "caffeine":   "Caffeine is a common cutting agent used to add bulk and a mild stimulant effect.",
        "levamisole": "Levamisole is a veterinary dewormer frequently used to cut cocaine and add bulk/weight.",
    }

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
    "A chromatogram appears on the monitor, displaying several separated peaks in the sample."

    $ gcms_step = 6
    "You note the retention times where each peak appears."

    $ gcms_step = 7
    "Generating mass spectra for the sample's peaks..."
    "The mass spectra for the sample have been generated."

    show nina normal1
    n "A lab certified cocaine reference standard has already been analyzed under the same GC-MS laboratory conditions used for the evidence samples."
    hide nina normal1
    show nina thinknote1
    n "Click through the peaks in your sample's chromatogram and compare each one's mass spectrum to the reference standard to find the primary compound."
    hide nina thinknote1

    $ gcms_step = 8
    show screen gcms_screen zorder 0
    show screen gcms_checklist zorder 10
    jump gcms_idle

label gcms_compare_interface:
    hide screen gcms_screen
    $ gcms_selected_peak = None
    call screen gcms_compare_screen

label gcms_identify:
    $ sample_label = _SAMPLE_DISPLAY_NAME[gcms_current_drug]

    if gcms_selected_peak == "cocaine":
        $ gcms_step = 9
        "The retention time and mass spectrum for this peak in [sample_label] match the reference standard for cocaine."
        "You've identified the primary compound in [sample_label] as cocaine."

        $ presumptive_result = evidence_found.get(gcms_current_drug + "_presumptive", False)
        show nina thinknote1
        n "Does this result match your presumptive field tests from evidence collection?"
        menu:
            "Yes, it is consistent":
                if presumptive_result:
                    n "Correct! The presumptive test was consistent with this result."
                    $ gcms_step += 1
                else:
                    n "Incorrect. The presumptive test result does not match this GC-MS identification."
                    jump gcms_identify
            "No, it isn't consistent":
                if not presumptive_result:
                    n "Correct! The presumptive test was inconsistent with this result."
                    $ gcms_step += 1
                else:
                    n "Incorrect. The presumptive test result matches this GC-MS identification."
                    jump gcms_identify
        hide nina thinknote1

        $ other_peaks = [p for p in _GCMS_PEAKS if p != "cocaine"]
        show nina normal1
        n "The other peaks in this chromatogram are common cutting agents, not the primary compound."
        python:
            for _p in other_peaks:
                say(_GCMS_ADULTERANT_NOTE[_p], n)
        hide nina normal1

        $ gcms_queue_done[gcms_current_drug] = True
        $ evidence.add_to_inventory(evids["Identified Cocaine " + sample_label])
        $ gcms_current_drug = None
        $ gcms_selected_peak = None
        if analyzed_everything():
            jump lab_end
        jump gcms
    else:
        "The mass spectrum for this peak does not match the cocaine reference standard."
        "This peak is likely [gcms_selected_peak], a cutting agent rather than the primary compound. Review the other peaks in [sample_label]'s chromatogram."
        $ gcms_selected_peak = None
        call screen gcms_compare_screen