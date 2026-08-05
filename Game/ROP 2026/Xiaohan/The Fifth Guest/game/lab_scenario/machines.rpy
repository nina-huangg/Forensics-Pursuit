label use_computer:
    # This machine is the Capillary Electrophoresis station.
    $ open_machine()
    if not tasks["DNA amplification"]:
        $ custom_notify("Amplification isn't done yet — run the Thermal Cycler first.", False)
        $ record_lab_mistake()
        jump return_bio_station
    jump cem



label use_genetic_analyzer:
    $ open_machine()
    if not tasks["DNA amplification"]:
        $ try_complete_machine_step(False, warn_msg="Amplification is not finished yet — capillary electrophoresis comes after PCR.")
        jump return_bio_station
    jump cem

label wait_screen:
    # Generic wait (e.g. PCR). Machine-specific waits use machine_wait + return to that machine.
    if tasks["DNA extraction"]:
        call machine_wait("Running PCR...", None)
    elif extraction_complete():
        call machine_wait("Extraction complete...", None)
    else:
        call machine_wait("Waiting for the run to finish...", None)
    jump return_bio_station


label machine_wait(message="Waiting...", bg=None):
    # Short wait beat on a machine background (or black). Returns to the caller.
    if bg:
        scene expression bg
    else:
        scene black
    show expression Solid("#00000099") as machine_wait_dim
    with dissolve
    show text "{color=#FFFFFF}[message]{/color}" at truecenter, lab_wait_wobble with dissolve
    pause 2.0
    hide text with dissolve
    hide machine_wait_dim
    return


label use_centrifuge:
    $ open_machine()
    $ extraction_ensure_past_prep()
    call screen centrifuge
    jump return_bio_station


label use_spinner:
    $ open_machine()
    $ extraction_ensure_past_prep()
    call screen spinner
    # Spinner screen jumps to spinner_run when clicked; if it Returns, leave.
    jump return_bio_station


label spinner_run:
    scene expression "backgrounds/use_spinner.png"
    show screen open_inv

    if not spinner_is_balanced():
        $ custom_notify("Balance the rotor first: sample in one slot, negative control on the opposite (diagonal) slot.", False)
        jump use_spinner

    $ _r = try_extraction_tool("spinner")
    if _r in ("ok", "wait_tube"):
        call machine_wait("Mini centrifuge spinning...", "backgrounds/use_spinner.png")
    if _r == "ok":
        jump return_bio_station
    # Still need the other tube — stay on the zoomed mini centrifuge.
    jump use_spinner


label use_vortex:
    $ open_machine()
    $ extraction_ensure_past_prep()
    call screen vortex
    jump return_bio_station


label vortex_set_time:
    # Keep the zoomed vortex view — Jump from the screen would otherwise reveal Station 1.
    scene expression "backgrounds/use_vortex.png"
    show screen open_inv
    $ custom_notify("Click the machine to set the time. Equip a tube from Evidence separately to run it.", True)

    $ _cur = extraction_current()
    $ _key = _cur[0] if _cur else ""
    $ _need = 10
    if _key in ("vortex_al", "vortex_ethanol"):
        $ _need = 15

    menu:
        "Set pulse-vortex time:"
        "5 seconds":
            scene expression "backgrounds/use_vortex.png"
            "Too short for this step. Use [_need] seconds."
            $ record_lab_mistake()
            jump use_vortex
        "10 seconds":
            if _need != 10:
                scene expression "backgrounds/use_vortex.png"
                "Incorrect. Use [_need] seconds for this step."
                $ record_lab_mistake()
                jump use_vortex
            jump vortex_apply
        "15 seconds":
            if _need != 15:
                scene expression "backgrounds/use_vortex.png"
                "Incorrect. Use [_need] seconds for this step."
                $ record_lab_mistake()
                jump use_vortex
            jump vortex_apply
        "30 seconds":
            scene expression "backgrounds/use_vortex.png"
            "Too long. Use [_need] seconds for this step."
            $ record_lab_mistake()
            jump use_vortex


label vortex_apply:
    # Time is already set — now check the tube before running the pulse.
    scene expression "backgrounds/use_vortex.png"
    show screen open_inv
    if extraction_machine_equipped is None:
        $ custom_notify("Evidence → Use your sample or Negative Control, then click the vortex again.", False)
        jump use_vortex

    scene expression "backgrounds/vortex_swab.png"
    show screen open_inv
    $ _r = try_extraction_tool("vortex")
    if _r in ("ok", "wait_tube"):
        call machine_wait("Pulse-vortexing...", "backgrounds/vortex_swab.png")
    if _r == "ok":
        jump return_bio_station
    # One tube done — stay zoomed so the player can equip the next tube.
    jump use_vortex


label use_prep:
    $ open_machine()
    if not lab_blood_samples and not prep_sample_done and not prep_processed_names:
        $ custom_notify("No blood sample is available.", False)
    if extraction_expected_tool() in ("ethanol", "column", "ate"):
        $ prep_view = 2
    elif extraction_expected_tool() in (None, "prep", "al"):
        $ prep_view = 1
    show screen open_inv
    call screen swab_screen
    if _return == "choose_tube":
        jump nina_choose_extraction_tube
    if _return == "ate":
        jump ate_pour_start
    if _return == "ethanol":
        jump ethanol_pour_start
    if _return == "column":
        jump new_tube
    jump return_bio_station


label ate_pour_start:
    # Pipette mini-game for eluting with Buffer ATE — the protocol allows a 20-100 µL range.
    $ open_machine()
    if prep_equipped_item is None:
        jump return_bio_station
    $ ate_pour_amount = 0
    scene expression "backgrounds/station1.png"
    show screen open_inv
    call screen ate_pour
    if _return == "applied":
        $ prep_dispense_ate()
    jump use_prep


label nina_choose_extraction_tube:
    $ renpy.hide_screen("open_inv")
    $ renpy.hide_screen("inventory")
    $ renpy.hide_screen("lab_notify")
    scene expression "backgrounds/station1.png"
    show nina talk at right
    if len(prep_processed_names) < 2:
        $ _only_processed = PREP_TUBE_PROCESS_MAP.get(prep_processed_names[0], (None, None))[0]
        s "You're missing one of the blood swabs, so we only have one sample and the negative control ready."
        s "We'll only be able to run analysis on the one you have."
        $ choose_extraction_tube(_only_processed)
        s "Next: pulse-vortex your sample, then the negative control."
    else:
        s "We've prepared both samples and the negative control."
        s "The negative control has no swab — it checks for contamination. Keep it for the later steps."
        s "Which sample tube should we continue with?"
        menu:
            "Processed Tube with Swab (Lamp)":
                $ choose_extraction_tube("Processed Tube with Swab (Lamp)")
            "Processed Tube with Swab (Floor)":
                $ choose_extraction_tube("Processed Tube with Swab (Floor)")
        s "I'll set the other sample aside. Next: pulse-vortex your sample, then the negative control."
    hide nina
    $ try_extraction_tool("prep")
    jump return_bio_station


label use_incubator:
    $ open_machine()
    $ extraction_ensure_past_prep()
    $ _tool = extraction_expected_tool()
    if _tool in ("incubator", "wait"):
        jump incubator_question
    call screen incubator
    jump return_bio_station


label use_qpcr:
    # QuantStudio: preps the plate, then runs quantification once it's loaded.
    $ open_machine()
    if not tasks["DNA extraction"]:
        $ try_complete_machine_step(False, warn_msg="DNA extraction is not finished yet — you can still prepare a QuantStudio plate.")

    if not qpcr_plate_ready:
        $ qpcr_reset_plate()
        call screen qpcr_plate_prep
        if _return != "ready":
            jump return_bio_station

    if tasks["DNA quantification"]:
        $ custom_notify("Quantification already complete.", True)
        jump return_bio_station

    $ hide_notebook()
    show nina talk at right
    with vpunch
    s "DNA quantification is complete."
    $ tasks["DNA quantification"] = True
    s "Your sample contains 0.067 ng/µL of DNA, so you'll need to add 15 µL of the DNA extract to the amplification reaction."
    s "Now head to the Thermal Cycler to amplify it."
    hide nina
    jump return_bio_station


label use_thermal_cycler:
    # Thermal Cycler: runs PCR amplification once quantification is done.
    $ open_machine()
    if not tasks["DNA quantification"]:
        $ custom_notify("Run the QuantStudio sample first — quantification isn't done yet.", False)
        $ record_lab_mistake()
        jump return_bio_station

    if tasks["DNA amplification"]:
        $ custom_notify("Amplification already complete.", True)
        jump return_bio_station

    $ hide_notebook()
    scene use_pcr
    s "Add 15 µL of each DNA sample to the appropriate wells, followed by the positive control and negative control."
    $ pcr_plate_reset()
    call screen pcr_plate_prep
    if _return != "ready":
        jump return_bio_station

    $ tasks["DNA amplification"] = True
    s "Thank you for preparing the samples. While you were working, your colleagues processed the other swabs. Please load the samples into the SeqStudio for capillary electrophoresis."
    jump return_bio_station


label cem:
    scene computer_screen_interface
    pause 1.0
    scene cem_interface
    call screen cem_screen


label cem_finish:
    $ hide_notebook()
    scene cem_screen_idle
    with vpunch
    $ tasks["Capillary Electrophoresis"] = True
    s "This is the DNA profile generated from the under-nail swab."
    s "You'll be examining one of the dye channels while your colleagues analyze the others."
    s "Review the electropherogram and complete the table on the left with the allele calls."
    $ profile_answers_reset()
    call screen profile_input_screen
    if _return == "correct":
        scene black
        show profile_table_filled at truecenter
        with vpunch
        s "Random Match Probability is the probability that a randomly selected individual unrelated to [suspect_name] would coincidentally share the observed DNA profile from a population."
        s "This DNA profile is consistent with [suspect_name]. The results from the other swab are also available, and that profile is consistent with [victim_name]."
        s "Before this DNA evidence can be presented in court, we need to assign statistical weight to this identification."
        s "To do this, we'll calculate the Random Match Probability, or RMP, and report the most conservative result."
        s "The most conservative RMP is the highest probability, meaning the value that represents the most common or most likely to be coincidentally identical."
        $ tasks["Profile Interpretation"] = True
        jump rmp_question
    jump return_bio_station


label rmp_question:
    menu:
        s "Which of the following probabilities should we report?"
        "1 in 330 septillion":
            s "That's not the most conservative estimate — check which value is the highest probability."
            $ record_lab_mistake()
            jump rmp_question
        "1 in 269 septillion":
            s "That's right, the random match probability for this profile is approximately 1 in 269 septillion people. Thank you for the work."
            $ tasks["Statistics"] = True
        "1 in 482 septillion":
            s "That's not the most conservative estimate — check which value is the highest probability."
            $ record_lab_mistake()
            jump rmp_question
    jump return_bio_station


label incubator_question:
    scene expression "backgrounds/use_incubator.png"
    show screen open_inv
    $ _cur = extraction_current()
    $ _key = _cur[0] if _cur else ""

    if _key in ("incubate_56", "incubate_70"):
        jump incubator_dual_load

    if _key == "set_70":
        menu:
            "Set the thermomixer to:"
            "56°C":
                "Collect the tubes and set the thermomixer for 70°C."
                $ record_lab_mistake()
                jump use_incubator
            "70°C":
                $ _r = try_extraction_tool("incubator")
                if _r == "ok":
                    jump return_bio_station
                jump use_incubator
            "Room temperature":
                "Set the thermomixer for 70°C for the next incubation."
                $ record_lab_mistake()
                jump use_incubator

    elif _key in ("open_incubate_10", "incubate_1"):
        menu:
            "Room-temperature incubation:"
            "Skip / continue immediately":
                "Allow the full incubation time."
                $ record_lab_mistake()
                jump use_incubator
            "Incubate at room temperature (proceed)":
                $ _r = try_extraction_tool("wait")
                if _r in ("ok", "wait_tube"):
                    call machine_wait("Room-temperature incubation...", "backgrounds/use_incubator.png")
                if _r == "ok":
                    jump return_bio_station
                jump use_incubator

    else:
        $ custom_notify("Nothing ready for the thermomixer yet.", False)
        $ record_lab_mistake()
        jump return_bio_station


label incubator_dual_load:
    $ custom_notify("You can place both tubes in the thermomixer, then set the temperature and time once for both.", True)
    if extraction_machine_equipped is not None:
        $ _loaded_name = extraction_machine_equipped_name
        $ incubator_dual_load_add()
        $ custom_notify(
            "Loaded {} into the thermomixer ({}/{}).".format(
                _loaded_name, len(incubator_loaded_tubes), len(extraction_required_processed_tubes())
            ),
            True,
        )

    $ _missing = incubator_dual_missing()
    if _missing:
        $ custom_notify("Still need: {}. Equip it from Evidence, then use the thermomixer again.".format(", ".join(_missing)), False)
        jump return_bio_station

    $ _cur = extraction_current()
    $ _key = _cur[0] if _cur else ""

    if _key == "incubate_56":
        menu:
            "Thermomixer settings for both tubes (lysis):"
            "37°C, 900 rpm, 15 minutes":
                "Incorrect. Use 56°C with shaking at 900 rpm for 1 hour."
                $ record_lab_mistake()
                jump incubator_dual_load
            "56°C, 900 rpm, 1 hour":
                $ incubator_dual_complete()
                call machine_wait("Incubating both tubes at 56°C...", "backgrounds/use_incubator.png")
                jump return_bio_station
            "95°C, no shaking, 5 minutes":
                "That is a PCR denaturation setting. Use 56°C at 900 rpm for 1 hour."
                $ record_lab_mistake()
                jump incubator_dual_load
    else:
        menu:
            "Thermomixer settings for both tubes:"
            "56°C, 900 rpm, 1 hour":
                "Incorrect. This step is 70°C at 900 rpm for 10 minutes."
                $ record_lab_mistake()
                jump incubator_dual_load
            "70°C, 900 rpm, 10 minutes":
                $ incubator_dual_complete()
                call machine_wait("Incubating both tubes at 70°C...", "backgrounds/use_incubator.png")
                jump return_bio_station
            "70°C, no shaking, 1 minute":
                "Use shaking at 900 rpm for 10 minutes."
                $ record_lab_mistake()
                jump incubator_dual_load


label centrifuge_run:
    # Keep zoomed centrifuge under the speed/time menu.
    scene expression "backgrounds/use_centrifuge.png"
    show screen open_inv

    if not centrifuge_is_balanced():
        $ custom_notify("Balance the rotor first: sample in one slot, negative control on the opposite (diagonal) slot.", False)
        jump use_centrifuge

    $ _cur = extraction_current()
    $ _key = _cur[0] if _cur else ""

    if _key in ("centrifuge_8000_1", "centrifuge_aw1", "centrifuge_aw2", "centrifuge_ethanol"):
        menu:
            "Benchtop centrifuge speed and time:"
            "3000 rpm for 1 minute":
                "Incorrect. Use 8000 rpm for 1 minute."
                $ record_lab_mistake()
                jump use_centrifuge
            "8000 rpm for 1 minute":
                jump centrifuge_apply
            "14000 rpm for 3 minutes":
                "Not for this step. Use 8000 rpm for 1 minute."
                $ record_lab_mistake()
                jump use_centrifuge

    elif _key == "centrifuge_14000_3":
        menu:
            "Benchtop centrifuge speed and time:"
            "8000 rpm for 1 minute":
                "Incorrect. Use 14000 rpm for 3 minutes."
                $ record_lab_mistake()
                jump use_centrifuge
            "14000 rpm for 3 minutes":
                jump centrifuge_apply
            "14000 rpm for 1 minute":
                "Close — this drying spin needs 3 minutes."
                $ record_lab_mistake()
                jump use_centrifuge

    elif _key == "centrifuge_14000_1":
        menu:
            "Benchtop centrifuge speed and time:"
            "8000 rpm for 1 minute":
                "Incorrect. Use 14000 rpm for 1 minute."
                $ record_lab_mistake()
                jump use_centrifuge
            "14000 rpm for 3 minutes":
                "Too long for elution. Use 14000 rpm for 1 minute."
                $ record_lab_mistake()
                jump use_centrifuge
            "14000 rpm for 1 minute":
                jump centrifuge_apply

    else:
        jump centrifuge_apply


label centrifuge_apply:
    $ _r = try_extraction_tool("centrifuge")
    if _r in ("ok", "wait_tube"):
        call machine_wait("Benchtop centrifuge running...", "backgrounds/use_centrifuge.png")
    if _r == "ok":
        jump return_bio_station
    # Stay on centrifuge if another tube is still needed for this step.
    jump use_centrifuge


label ethanol_pour_start:
    # Pour mini-game: drag to the target volume before it actually gets added.
    $ open_machine()
    if extraction_expected_tool() != "ethanol":
        $ custom_notify("Not the right step for ethanol yet. Check the notebook.", False)
        $ record_lab_mistake()
        jump return_bio_station
    if extraction_machine_equipped is None:
        $ custom_notify("Open Evidence and Use your processed tube (or Negative Control) first, then use Ethanol.", False)
        jump return_bio_station
    $ ethanol_pour_amount = 0
    scene expression "backgrounds/station1.png"
    show screen open_inv
    call screen ethanol_pour
    if _return == "poured":
        jump add_ethanol
    jump return_bio_station


label add_ethanol:
    $ _r = try_extraction_tool("ethanol")
    if _r == "ok" and extraction_current() and extraction_current()[0] == "vortex_ethanol":
        $ custom_notify("Next: pulse-vortex for 15 seconds.", True)
    if _r == "wait_tube":
        $ custom_notify("Equip the other processed tube from Evidence, then use Ethanol again.", True)
    jump return_bio_station


label new_tube:
    $ _cur = extraction_current()
    $ _key = _cur[0] if _cur else ""
    if _key == "transfer_lysate":
        jump lysate_transfer_start
    if _key == "add_aw1":
        jump aw1_pour_start
    $ _r = try_extraction_tool("column")
    if _r == "wait_tube":
        $ custom_notify("Equip the other processed tube from Evidence, then use Column / Collection Tube again.", True)
    jump return_bio_station


label lysate_transfer_start:
    # Pipette mini-game for transferring 700 µL lysate onto the QIAamp column.
    $ open_machine()
    if extraction_machine_equipped is None:
        $ custom_notify("Open Evidence and Use your processed tube (or Negative Control) first, then use the Column.", False)
        jump return_bio_station
    $ lysate_transfer_amount = 0
    scene expression "backgrounds/station1.png"
    show screen open_inv
    call screen lysate_transfer
    if _return == "transferred":
        $ _r = try_extraction_tool("column")
        if _r == "wait_tube":
            $ custom_notify("Equip the other processed tube from Evidence, then use Column / Collection Tube again.", True)
    jump return_bio_station


label aw1_pour_start:
    # Pipette mini-game for adding 500 µL Buffer AW1 to the new collection tube.
    $ open_machine()
    if extraction_machine_equipped is None:
        $ custom_notify("Open Evidence and Use your processed tube (or Negative Control) first, then use the Column.", False)
        jump return_bio_station
    $ aw1_pour_amount = 0
    scene expression "backgrounds/station1.png"
    show screen open_inv
    call screen aw1_pour
    if _return == "poured":
        $ _r = try_extraction_tool("column")
        if _r == "wait_tube":
            $ custom_notify("Equip the other processed tube from Evidence, then use Column / Collection Tube again.", True)
    jump return_bio_station


label transfer_tube:
    jump new_tube


label discard_sample:
    $ _r = try_extraction_tool("trash")
    if _r == "wait_tube":
        $ custom_notify("Equip the other processed tube from Evidence, then use Biohazard Waste again.", True)
    if extraction_complete():
        jump extraction_finished
    jump return_bio_station


label apply_ate:
    $ _r = try_extraction_tool("ate")
    if _r == "wait_tube":
        $ custom_notify("Equip the other processed tube from Evidence, then apply ATE again.", True)
    jump return_bio_station


label extraction_finished:
    scene expression "backgrounds/station1.png"
    show nina talk at right
    with vpunch
    s "Great work — the evidence swab and negative control extracts are ready."
    s "Now let's find out how much DNA we have. Use the QuantStudio to run quantification."
    hide nina
    jump return_bio_station
