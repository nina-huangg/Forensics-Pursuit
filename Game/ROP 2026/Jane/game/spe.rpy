# CODE BELOW IS FOR THE LAB ------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# LAB VARS ---
default in_lab = False
# SPE
default spe_difficulty = 0 # 0 = full checklist, 1 = half checklist, 2 = low checklist
default has_SPE_sample1 = False
default has_SPE_sample2 = False
default has_SPE_sample3 = False
default step_SPE = ""
default step_num_SPE = 1 # see ipad notes for specifics, relates to which step to do, related to the spe_spo
default inv_call_SPE = ""
default choice_SPE = ""
default current_SPE_drug = ""
default spe_handoff_offered = False
default spe_skipped_sample  = None   # "sample1" / "sample2" / "sample3" / None

init python:
    _SPE_PREPARED_ITEM = {
        "sample1": "Prepared Sample 1",
        "sample2": "Prepared Sample 2",
        "sample3": "Prepared Sample 3",
    }
    _SPE_EVIDENCE_ITEM = {
        "sample1": "Sample 1",
        "sample2": "Sample 2",
        "sample3": "Sample 3"
    }

    def spe_hand_off(drug):
        store.spe_skipped_sample = drug
        store.spe_handoff_offered = True

    def spe_check_completion():
        if store.spe_skipped_sample:
            others = [d for d in ("sample1", "sample2", "sample3") if d != store.spe_skipped_sample]
            if all(globals()["has_SPE_" + d] for d in others):
                skipped = store.spe_skipped_sample
                if not globals()["has_SPE_" + skipped]:
                    globals()["has_SPE_" + skipped] = True
                    evidence.delete_from_inventory(evids[_SPE_EVIDENCE_ITEM[skipped]])
                    evidence.add_to_inventory(evids[_SPE_PREPARED_ITEM[skipped]])
                    renpy.notify("The lab assistant finished preparing the handed-off sample.")
                store.spe_skipped_sample = None

        if has_SPE_sample1 and has_SPE_sample2 and has_SPE_sample3:
            store.gcms_step = 3
            store.choice_SPE = "COMPLETED"

# LAB LABELS ----------
label lab:
    scene black
    $ in_lab = True
    "What would you like to start with?"
    jump materials_lab

# SOLID PHASE EXTRACTION CODE
# there are 5 steps for drugs too, 1. dilute the mixture, 2. condition the cartridge, 
# 3. load it with the sample, 4. wash the cartridge, 5. elution (obtain the extracted compound)
label solid_phase_extraction:
    $ hide_all_lab_screens()
    $ location = "solid_phase_extraction"
    scene lab_counter_bk
    if not analytical_balance_done:
        show nina normal1
        n "You'll need to weigh all three presumed samples on the analytical balance before you can begin extraction."
        hide nina normal1
        jump materials_lab

    if has_SPE_sample1 and has_SPE_sample2 and has_SPE_sample3:
        show nina normal1
        n "All three samples have already been through Solid Phase Extraction."
        n "Head to the GC-MS to continue the analysis."
        hide nina normal1
        jump materials_lab

    # hand off to assistant
    if not spe_handoff_offered and current_SPE_drug == "" and step_num_SPE == 1:
        show nina normal1
        n "Solid Phase Extraction takes a while for each sample."
        n "If you'd like, you can hand one off to the lab assistant to prepare while you run the other two yourself."
        hide nina normal1
        menu:
            "Hand over Sample 1" if not has_SPE_sample1:
                $ spe_hand_off("sample1")
            "Hand over Sample 2" if not has_SPE_sample2:
                $ spe_hand_off("sample2")
            "Hand over Sample 3" if not has_SPE_sample3:
                $ spe_hand_off("sample3")
            "No, I'll do all three myself":
                $ spe_handoff_offered = True
        if spe_skipped_sample:
            show nina normal1
            n "I'll get that one started for you. Go ahead and prepare the other two."
            hide nina normal1

    #PRE-TREATMENT
    hide screen back_button_screen onlayer over_screens
    show beaker_empty:
        xalign 0.5
        yalign 0.5
    show nina talk
    n "Before you do anything, you'll need to pre-treat your sample and dilute it 1:1 with an acidic buffer."
    n "Which drug sample do you want to dilute?"
    hide nina talk
    menu:
        "Sample 1" if not has_SPE_sample1 and spe_skipped_sample != "sample1":
            $ current_SPE_drug = "sample1"
            show beaker_sample1:
                xalign 0.5
                yalign 0.5
        "Sample 2" if not has_SPE_sample2 and spe_skipped_sample != "sample2":
            $ current_SPE_drug = "sample2"
            show beaker_sample2:
                xalign 0.5
                yalign 0.5
        "Sample 3" if not has_SPE_sample3 and spe_skipped_sample != "sample3":
            $ current_SPE_drug = "sample3"
            show beaker_sample3:
                xalign 0.5
                yalign 0.5
    jump SPE_dilute_question

label SPE_dilute_question:
    $ inv_call_SPE = "SPE_dilute_question"
    $ step_SPE = "SPE_condition"
    "What will you use to dilute the drug sample?"
    call screen inventory
    return

label SPE_condition:
    scene spe11
    show screen spe_spo
    $ inv_call_SPE = "SPE_condition"
    $ step_SPE = "SPE_condition1"
    call screen inventory

label SPE_condition1:
    scene spe12
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            $ step_num_SPE = 2
            jump SPE_condition2
        "1 mL/minute":
            "Wrong."
            jump SPE_condition1

label SPE_condition2:
    $ inv_call_SPE = "SPE_condition2"
    $ step_SPE = "SPE_condition3" #1% formic acid or water
    scene spe13
    call screen inventory

label SPE_condition3:
    scene spe14
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            $ step_num_SPE = 3 # catridge has been reinsed with formic or water waiting for loading
            jump SPE_loading
        "1 mL/minute":
            "Wrong. Try again."
            jump SPE_condition3

label SPE_loading:
    scene spe13
    $ renpy.pause(0.5, hard=True)
    scene spe21
    $ inv_call_SPE = "SPE_loading"
    $ step_SPE = "SPE_loading1"
    call screen inventory

label SPE_loading1:
    scene spe22
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong. Try again."
            jump SPE_loading1
        "1 mL/minute":
            $ step_num_SPE = 4 # drugs in, next wash w/formic
            jump SPE_washing

label SPE_washing:
    scene spe23
    $ renpy.pause(0.5, hard=True)
    scene spe31
    $ inv_call_SPE = "SPE_washing"
    $ step_SPE = "SPE_washing1"
    call screen inventory

label SPE_washing1:
    scene spe32
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong. Try again."
            jump SPE_washing1
        "1 mL/minute":
            $ step_num_SPE = 5 # washg fromic, next wash w/methanol
            jump SPE_washing2

label SPE_washing2:
    scene spe33
    $ inv_call_SPE = "SPE_washing2"
    $ step_SPE = "SPE_washing3" #methanol
    call screen inventory

label SPE_washing3:
    scene spe34
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_washing3
        "1 mL/minute":
            $ step_num_SPE = 6 # 5% ammonium hydroxide ELUTION
            jump SPE_elution

label SPE_elution:
    scene spe33
    $ renpy.pause(0.5, hard=True)
    scene spe41
    $ inv_call_SPE = "SPE_elution"
    $ step_SPE = "SPE_elution1"
    call screen inventory

label SPE_elution1:
    scene spe42
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_elution1
        "1 mL/minute":
            $ step_num_SPE = 7
            jump SPE_elution2

label SPE_elution2:
    scene spe43
    "What temperature should the mixture be dried at?"
    menu:
        "37 Celsius":
            scene spe44
            "You've obtained the prepared sample."
            if(has_SPE_sample1 and current_SPE_drug == "sample1"):
                $ evidence.add_to_inventory(evids["Prepared Sample 1"])
            elif(has_SPE_sample2 and current_SPE_drug == "sample2"):
                $ evidence.add_to_inventory(evids["Prepared Sample 2"])
            elif(has_SPE_sample3 and current_SPE_drug == "sample3"):
                $ evidence.add_to_inventory(evids["Prepared Sample 3"])

            $ spe_check_completion()

            # reset counter
            $ step_num_SPE = 1
            $ current_SPE_drug = ""
            hide screen spe_spo

            if choice_SPE == "COMPLETED":
                show screen back_button_screen('materials_lab') onlayer over_screens
                jump materials_lab
            else:
                jump solid_phase_extraction

# toolbox stuffs for SPE
label use5Amm:
    if location == "solid_phase_extraction":
        if(inv_call_SPE == "SPE_dilute_question"):
            "Wrong!"
            jump expression inv_call_SPE
        else:
            if(step_num_SPE != 6):
                "Wrong compound!"
                jump expression inv_call_SPE

            "How much will you add?"
            menu:
                "1 mL":
                    jump expression step_SPE
                "2 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE
                "5 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE

label use01Formic:
    if location == "solid_phase_extraction":
        if(inv_call_SPE == "SPE_dilute_question"):
            "Wrong!"
            jump expression inv_call_SPE
        else:
            if(step_num_SPE != 4):
                "Wrong compound!"
                jump expression inv_call_SPE

            "How much will you add?"
            menu:
                "1 mL":
                    jump expression step_SPE
                "2 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE
                "5 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE

label useMethanol:
    if location == "solid_phase_extraction":
        if(inv_call_SPE == "SPE_dilute_question"):
            "Wrong!"
            jump expression inv_call_SPE
        else:
            if(step_num_SPE != 1 and step_num_SPE != 5):
                "Wrong compound!"
                jump expression inv_call_SPE

            "How much will you add?"
            menu:
                "1 mL":
                    jump expression step_SPE
                "2 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE
                "5 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE
                # can add other options here

label useStep3: # 1% formic acid 
    if location == "solid_phase_extraction":
        if(inv_call_SPE == "SPE_dilute_question"):
            show nina normal1
            "Good! Now we'll start."
            hide nina normal1
            jump expression step_SPE
        else:
            if(step_num_SPE != 2):
                "Wrong compound!"
                jump expression inv_call_SPE

            "How much will you add?"
            menu:
                "1 mL":
                    jump expression step_SPE
                "2 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE
                "5 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE

label useWater: # use water
    if location == "solid_phase_extraction":
        if(inv_call_SPE == "SPE_dilute_question"):
            "Wrong!"
            jump expression inv_call_SPE
        else:
            if(step_num_SPE != 2):
                "Wrong compound!"
                jump expression inv_call_SPE

            "How much will you add?"
            menu:
                "1 mL":
                    jump expression step_SPE
                "2 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE
                "5 mL":
                    "Wrong amount."
                    jump expression inv_call_SPE

label useSample1:
    if location == "solid_phase_extraction":
        if(step_num_SPE == 3 and current_SPE_drug == "sample1"):
            $ has_SPE_sample1 = True
            $ evidence.delete_from_inventory(evids["Sample 1"])
            jump expression step_SPE
        else:
            "Wrong compound!"
            jump expression inv_call_SPE

label useSample2:
    if location == "solid_phase_extraction":
        if(step_num_SPE == 3 and current_SPE_drug == "sample2"):
            $ has_SPE_sample2 = True
            $ evidence.delete_from_inventory(evids["Sample 2"])
            jump expression step_SPE
        else:
            "Wrong compound!"
            jump expression inv_call_SPE

label useSample3:
    if location == "solid_phase_extraction":
        if(step_num_SPE == 3 and current_SPE_drug == "sample3"):
            $ has_SPE_sample3 = True
            $ evidence.delete_from_inventory(evids["Sample 3"])
            jump expression step_SPE
        else:
            "Wrong compound!"
            jump expression inv_call_SPE