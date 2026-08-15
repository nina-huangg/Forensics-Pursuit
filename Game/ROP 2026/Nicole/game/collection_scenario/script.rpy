init python:
    import json

    global pressed

    config.rollback_enabled = False # disables rollback

    def hide_all_inventory():
        renpy.hide_screen("inventory")
        renpy.hide_screen("open_inv")

    def delete_all_toolbox():
        toolbox.delete_from_inventory(tools["gloves"])
        toolbox.delete_from_inventory(tools["Backing Card"])
        toolbox.delete_from_inventory(tools["Scalebar"])
        toolbox.delete_from_inventory(tools["Magnetic Powder"])
        toolbox.delete_from_inventory(tools["Tape"])
        toolbox.delete_from_inventory(tools["Evidence Bag"])
        toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
        toolbox.delete_from_inventory(tools["100% Methanol"])
        toolbox.delete_from_inventory(tools["Water"])
        toolbox.delete_from_inventory(tools["1% Formic acid"])
        toolbox.delete_from_inventory(tools["0.1% Formic acid"])
        toolbox.delete_from_inventory(tools["Methanol and 5% Ammonium Hydroxide"])

    def check_all_bagged():
        for item in can_bag:
            if(bagged_objs[item] == False and collected_objs[item] == True):
                return False
        return True

    def check_all_scalebar():
        for item in can_scale:
            if(scalebard[item] == False):
                return False
        return True

    tools = load_items("jsons/toolbox.json")
    evids = load_items("jsons/evidence.json")

    # FUNCTION FOR DRAG AND DROP
    def put_in_bag(drags, drop):
        if drop:
            return True
        else: 
            return

define n = Character(name=("Nina"), image="nina")

########### HOSPITAL VARS ##########
default got_testimony = {"parents": False, "friends": False}
default want_collection_scenario = False
default parent_count = {"1": 0, "2": 0, "3": 0}
default friend_count = {"1": 0, "2": 0, "3": 0}
default parent_1 = ""
default parent_2 = ""
default parent_3 = ""
default friend_1 = ""
default friend_2 = ""
default friend_3 = ""
########### HOUSE VARS ##########
default got_intro = False
default button_yes = False
default backbuttonenable = True
default bagging = False
default current_bag_item = ""
default click_object = ""
default last_area = ""
default last_action = "" # also for use in the lab section
default put_gloves = False
default need_tape = False
# for fingerprinting
default fingerprint_toback = ""
default can_fingerprint = ["weedbag", "pilltop", "grape"] #, "pill"
default fingerprint1_stuff = ["pilltop", "grape"] #, "pill"
default fingerprint2_stuff = ["weedbag"]
default dusted = {"weedbag": False, "pill": False, "pilltop": False, "grape": False}
default uvd = {"weedbag": False, "pill": False, "pilltop": False, "grape": False}
default scalebard = {"weedbag": False, "pill": False, "pilltop": False, "grape": False}
default taped = {"weedbag": False, "pill": False, "pilltop": False, "grape": False}
default backed = {"weedbag": False, "pill": False, "pilltop": False, "grape": False}
default num_evidence = 0
default sf = False
default can_scale = ["weedbag", "pilltop", "grape"]
# for bagged evidence
default collected_objs = {"weedbag": False, "weedbag_print": False, "pill": False, "pill_print": False, "grape": False, "grape_print": False}
default bagged_objs = {"weedbag": False, "weedbag_print": False, "pill": False, "pill_print": False, "grape": False, "grape_print": False}
default can_bag = ["weedbag", "weedbag_print","pill", "pill_print", "grape", "grape_print"]
default pill_status = 0 # even default, odd top
########### LAB VARS ##########
default in_lab = False
default can_add_to_tox = ["print1", "pill", "photos", "hospital_report"] #FOR LATER COURTROOM
default added_to_tox = {"print1": False, "pill": False, "photos": False, "hospital_report": False} #UNUSED
default has_tox = False
# SPE
default spe_difficulty = 0 # 0 = full checklist, 1 = half checklist, 2 = low checklist
default has_SPE_pre = False
default has_SPE_post = False
default added_SPE_post = False
default added_SPE_pre = False
default step_SPE = ""
default step_num_SPE = 1 # see ipad notes for specifics, relates to which step to do, related to the spe_spo
default inv_call_SPE = ""
default choice_SPE = ""
default askq = True
default tookpre = False
default tookpost = False
default selected_blood = ""
# LC-MS
default placed_in_lcms = ""
default completed_lcms = {"pre": False, "post": False}
default first_lcms = False
default peak = ""
default peaked = {"fent": False, "caf": False, "thc": False}
# AFIS/CSI PIX
default processed_prints = {"print_1": False, "print_2": False, "print_3": False}

# SCREENS -----------------------------------------------------------------
screen spe_spo: # the checklist
    if(step_num_SPE == 1 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full1.png":
            xalign 0.999999
    elif(step_num_SPE == 1 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half1.png":
            xalign 0.999999
    elif(step_num_SPE <= 2 and spe_difficulty == 2):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_low1.png":
            xalign 0.999999
    elif(step_num_SPE == 2 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full2.png":
            xalign 0.999999
    elif(step_num_SPE == 2 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half2.png":
            xalign 0.999999
    elif(step_num_SPE <= 3 and spe_difficulty == 2):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_low2.png":
            xalign 0.999999
    elif(step_num_SPE == 3 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full3.png":
            xalign 0.999999
    elif(step_num_SPE == 3 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half3.png":
            xalign 0.999999
    elif(step_num_SPE <= 5 and spe_difficulty == 2):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_low3.png":
            xalign 0.999999
    elif(step_num_SPE == 4 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full4.png":
            xalign 0.999999
    elif(step_num_SPE == 4 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half4.png":
            xalign 0.999999
    elif(step_num_SPE <= 6 and spe_difficulty == 2):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_low4.png":
            xalign 0.999999
    elif(step_num_SPE == 5 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full5.png":
            xalign 0.999999
    elif(step_num_SPE == 5 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half5.png":
            xalign 0.999999
    elif(step_num_SPE <= 7 and spe_difficulty == 2):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_low5.png":
            xalign 0.999999
    elif(step_num_SPE == 6 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full6.png":
            xalign 0.999999
    elif(step_num_SPE == 6 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half6.png":
            xalign 0.999999
    elif(step_num_SPE == 7 and spe_difficulty == 0):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_full7.png":
            xalign 0.999999
    elif(step_num_SPE == 7 and spe_difficulty == 1):
        add "images/Lab/Solid-phase extraction/spe_checklist/spe_checklist_half7.png":
            xalign 0.999999

screen lab_hallway:
    imagebutton:
        auto "images/Lab/hallway_assets/materials_lab_%s.png"
        xalign 0.75
        yalign 0.5
        action Jump("materials")
    imagebutton:
        auto "images/Lab/hallway_assets/data_analysis_lab_%s.png"
        xalign 0.25
        yalign 0.5
        action Jump("data_analysis")

screen material_lab: 
    imagebutton:
        auto "images/Lab/VacuumManifold_%s.png"
        xalign 0.75
        yalign 0.5
        action Jump("solid_phase_extraction")
    imagebutton:
        auto "images/Lab/LCMS_%s.png"
        xalign 0.25
        yalign 0.5
        action Jump("lc_ms")
    imagebutton:
        auto "images/Environment Items/back_button_%s.png"
        xalign 0.99
        yalign 0.1
        action Jump("lab_nonina")

screen data_analysis_lab:
    imagebutton:
        auto "images/data_analysis_lab/afis_software_%s.png"
        xalign 0.30
        yalign 0.25
        action Jump("afis")
    imagebutton:
        auto "images/Environment Items/back_button_%s.png"
        xalign 0.99
        yalign 0.1
        action Jump("lab_nonina")

screen lcms_machine:
    imagebutton:
        auto "images/Lab/LC-MS/lcms_%s.png"
        xalign 0.58
        yalign 0.5
        action Jump("lab_prepare_lcms")
    imagebutton:
        auto "images/Environment Items/back_button_%s.png"
        xalign 0.99
        yalign 0.1
        action Jump("materials")

screen lcms_chromatogram:
    # the ? buttons
    if(not peaked["caf"]):
        imagebutton: # caffeine
            auto "images/Lab/LC-MS/lcms_question_%s.png"
            xalign 0.34
            yalign 0.45
            action Jump("lcms_peak_caf")
    if(not peaked["fent"]):
        imagebutton: # fentanyl
            auto "images/Lab/LC-MS/lcms_question_%s.png"
            xalign 0.46
            yalign 0.36
            action Jump("lcms_peak_fent")
    if(not peaked["thc"]):
        imagebutton: # thc
            auto "images/Lab/LC-MS/lcms_question_%s.png"
            xalign 0.6
            yalign 0.59
            action Jump("lcms_peak_thc")

screen lcms_post_pers:
    text "Post-mortem sample Chromatogram":
        xalign 0.5
        yalign 0.25
        size 40
        color "#000000ff"
    text "Sample":
        xalign 0.165
        yalign 0.13
        size 20
        color "#000000ff"

screen lcms_pre_pers:
    text "Pre-mortem sample Chromatogram":
        xalign 0.5
        yalign 0.25
        size 40
        color "#000000ff"
    text "Sample":
        xalign 0.165
        yalign 0.13
        size 20
        color "#000000ff"

screen lcms_fent:
    text "4.2 FENT":
        xalign 0.46
        yalign 0.36
        size 25
        color "#000000ff"

screen lcms_caf:
    text "1.8 CAF":
        xalign 0.34
        yalign 0.45
        size 25
        color "#000000ff"

screen lcms_thc:
    text "7.5 THC":
        xalign 0.6
        yalign 0.59
        size 25
        color "#000000ff"

screen kitchenInteractables():
    zorder -1
    imagebutton:
        auto "images/Environment Items/trash-%s.png"
        xalign 0
        yalign 0.999999999
        action Jump("trashbin")
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/counter-%s.png"
        xalign 0.999999999
        yalign 0.999999999
        action Jump("countertop")
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/counterleft-%s.png"
        xalign 0.13
        yalign 0.5
        action Jump("countertopleft")
        sensitive button_yes

screen trashInteractables():
    if collected_objs["weedbag"] == False:
        imagebutton:
            auto "images/Environment Items/weedbag-%s.png"
            xalign 0.5
            yalign 0.3
            action Jump("weedbagaction")
            sensitive button_yes

screen topInteractables():
    imagebutton:
        auto "images/Environment Items/brownies-%s.png"
        xalign 0.999
        yalign 0.7
        action Jump("countertop")
        sensitive False # change to button_yes
    imagebutton:
        auto "images/Environment Items/juice-%s.png"
        xalign 0.3
        yalign 0
        action Jump("grapeaction")
        sensitive button_yes

screen topleftInteractables():
    if collected_objs["pill"] == False:
        imagebutton:
            auto "images/Environment Items/pill-%s.png"
            xalign 0.4
            yalign 0.4
            action Jump("pillaction")
            sensitive button_yes

screen backButton():
    if last_area != "" and backbuttonenable == True and sf == False:
        imagebutton:
            auto "images/Environment Items/back_button_%s.png"
            xalign 0.99
            yalign 0.1
            if last_area == "countertop":
                action Jump("countertop")
            elif last_area == "kitchen":
                action Jump("house")
            elif last_area == "trash":
                action Jump("trashbin")
            elif last_area == "houseoutside":
                action Jump("houseoutside")
            elif last_area == "countertopleft":
                action Jump("countertopleft")
            sensitive button_yes

screen grapecollect():
    zorder -1
    if collected_objs["grape"] == False:
        textbutton "Collect item?":
            style_prefix "textB"
            text_idle_color "#ffffffff"
            text_hover_color "#35ffe4ff"
            background "#696969ff"
            xalign 0.85
            yalign 0.85
            action Jump("grapecollected")
            sensitive button_yes
screen weedbagcollect():
    zorder -1
    if collected_objs["weedbag"] == False and backbuttonenable == True:
        textbutton "Collect item?":
            style_prefix "textB"
            text_idle_color "#ffffffff"
            text_hover_color "#35ffe4ff"
            background "#696969ff"
            xalign 0.85
            yalign 0.85
            action Jump("weedbagcollected")
            sensitive button_yes
screen pillcollect():
    zorder -1
    if collected_objs["pill"] == False and backbuttonenable == True:
        # button to turn the pill bottle
        imagebutton:
            auto "images/Environment Items/turn-%s.png"
            xalign 0.65
            yalign 0.3
            action Jump("pillturned")
            sensitive button_yes
        textbutton "Collect item?":
            style_prefix "textB"
            text_idle_color "#ffffffff"
            text_hover_color "#35ffe4ff"
            background "#696969ff"
            xalign 0.85
            yalign 0.85
            action Jump("pillcollected")
            sensitive button_yes

screen hospitaloutsideInteractables():
    zorder -1
    imagebutton:
        auto "images/Environment Items/turn-%s.png"
        xalign 0.9
        yalign 0.2
        action Jump("insidehospital")
        at Transform(zoom=1.2)

# drag screens
screen tape_drag_screen():
    zorder -1
    draggroup:
        drag:
            drag_name "evidence_bag"
            draggable False
            droppable True
            dropped put_in_bag
            xpos 1000 ypos 100
            child "images/evidence/openbag.png"
        drag:
            drag_name "evidence_tape"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            child "images/Environment Items/tet.png"

screen item_deposit_screen():
    zorder -1
    draggroup:
        drag:
            drag_name "bag_drop"
            droppable True
            draggable False
            dropped put_in_bag
            xpos 1000 ypos 100
            child "images/evidence/openbag.png"
        drag:
            drag_name "item_drag"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            if("finger" in current_bag_item):
                child "images/Environment Items/backing fingerprint.png"
            elif(current_bag_item == "grape"):
                child "images/Environment Items/grape_idle.png"
            elif(current_bag_item == "weedbag"):
                child "images/Environment Items/weedbag-idle.png"
            elif(current_bag_item == "pill"):
                child "images/Environment Items/pill-idle.png"

screen finger_drag():
    zorder -1
    draggroup:
        drag:
            drag_name "backing_drop"
            droppable True
            draggable False
            dropped put_in_bag
            xpos 1000 ypos 100
            child "images/Environment Items/backing_card.png"
        drag:
            drag_name "item_drag"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            if("finger2 NS" == fingerprint_toback):
                child "images/Environment Items/finger2NS.png"
            elif("finger2 S" == fingerprint_toback):
                child "images/Environment Items/finger2S.png"
            elif("finger1 NS" == fingerprint_toback or "finger3 NS" == fingerprint_toback):
                child "images/Environment Items/finger1NS.png"
            elif("finger1 S" == fingerprint_toback or "finger3 S" == fingerprint_toback):
                child "images/Environment Items/finger1S.png"

screen write_drag():
    zorder -1
    draggroup:
        drag:
            drag_name "backing_drop"
            droppable True
            draggable False
            dropped put_in_bag
            xpos 1000 ypos 100
            if("finger2 NS" == fingerprint_toback):
                child "images/Environment Items/finger2_noscale.png"
            elif("finger2 S" == fingerprint_toback):
                child "images/Environment Items/finger2_scale.png"
            elif("finger1 NS" == fingerprint_toback or "finger3 NS" == fingerprint_toback):
                child "images/Environment Items/finger1_noscale.png"
            elif("finger1 S" == fingerprint_toback or "finger3 S" == fingerprint_toback):
                child "images/Environment Items/finger1_scale.png"
        drag:
            drag_name "item_drag"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            child "images/Environment Items/R.png"

# LABELS ------------------------------------------------------------------------
# HOSPITAL SECTION -------------------------------------------------------------------------------------------------------------
#
#
# -------------------------------------------------------------------------------------------------------------
label start:
    # trigger warning and select difficulty
    scene black
    "Trigger warning: the game talks about overdosing and suicide."
    "Please be advised."
    "Select your difficulty (applicable only in the lab section):"
    menu:
        "Easy (given detailed steps)":
            $ spe_difficulty = 0
        "Medium (given less detailed steps)":
            $ spe_difficulty = 1
        "Hard (given brief steps)":
            $ spe_difficulty = 2

    #start the game
    scene hospitaloutside with fade
    # brief on the scenario + testimona
    show nina normal1
    n "You might be wondering why I've brought you to the hospital."
    n "Well, there's a new coroner case."
    n "A few hours ago, a 25 year old male collapsed during a house party. He died an hour ago here at the hospital."
    show nina thinknote1
    n "Hospital staff has confirmed that the man died from overdosing on Fentanyl."
    n "However, we've been called in because his parents are adamant about his death being some sort of malicious plot."
    n "According to the parents, their son was a happy man and would never commit suicide..."
    show nina talk
    n "The staff has already given me 2 blood samples, one taken pre-mortem, the other post-mortem."
    n "In addition I have the man's hospital report and photos from the scene taken by the first responders, so you won't need to take any photos for yourself."
    n "I'll give them to you at the lab."
    n "Right now, I need you to go inside and get testimony statements from the parents and the other party go-er."
    n "Once you're done, meet me out here for the next steps."
    hide nina talk
    call screen hospitaloutsideInteractables
label insidehospital:
    scene hospital
    "Whose testimony do you want to get?"
    menu:
        "Parents" if got_testimony["parents"] != True:
            jump parents_testimony
        "Friend" if got_testimony["friends"] != True:
            jump friends_testimony
        "Return to Nina":
            #if got_testimony["friends"] and got_testimony["parents"]:
            jump return_to_nina

label parents_testimony:
    show parents
    "What do you want to ask?"
    menu:
        "[parent_1] About your son...":
            jump MDson
        "[parent_2] About what happened at the party...":
            jump MDparty
        "[parent_3] About Alastor Brahe's medical history...":
            jump MDmedhist
        "Thank them for their time and give out condolences." if (parent_count["1"] >= 1 and parent_count["2"] >= 1 and parent_count["3"] >= 1):
            hide parents
            "Parents testimony has been added to your inventory."
            $ evidence.add_to_inventory(evids["Parents Testimony"])
            $ got_testimony["parents"] = True
            jump insidehospital
label MDson:
    "Mrs Brahe: *sniff* Alastor was always such a happy child... Giggling over everything he found funny..."
    "Mrs Brahe: I don't understand how this could've happened! *sobsob*"
    "Mr Brahe: Alastor had his entire life in front of him. There's no way he would've overdosed on purpose!"
    "Mr Brahe: I don't know care about what the medical personnel here are saying, he wouldn't have killed himself!!!"
    "Mr Brahe: Someone must have done something to him at the party!"
    $ parent_count["1"] += 1
    $ parent_1 = "*DONE*"
    jump parents_testimony
label MDparty:
    "Mrs Brahe: *sobsob* He wanted to celebrate with his friends about getting into a masters program... All I know is that he invited a few people..."
    "Mr Brahe: We don't know exactly what happened at the party, I think you're better off asking someone who was there."
    $ parent_count["2"] += 1
    $ parent_2 = "*DONE*"
    jump parents_testimony
label MDmedhist:
    "Mrs Brahe: *sniff* He had kidney cancer as a child but the chemo worked! But he's suffered from chronic pain since..."
    "Mrs Brahe: He's taken all sorts of pain medications for it, but none of them worked very well..."
    "Mrs Brahe: I know that his medication was changed recently because he told me it was working really well."
    "Mrs Brahe: He also asked us to help him manage his doses."
    "Mr Brahe: We've been careful! Both of us are certain he's been taking his medication on time, EVERY time."
    "Mr Brahe: In fact, he should have 2 pills left in the medication bottle!"
    "Mr Brahe: And if you're wondering about mental illness, he's has no history of it. No depression, nothing."
    "Mr Brahe: So it doesn't make sense for him to have overdosed!"
    $ parent_count["3"] += 1
    $ parent_3 = "*DONE*"
    jump parents_testimony

label friends_testimony:
    show friend
    "What do you want to ask?"
    menu:
        "[friend_1] About their friend...":
            jump Ffriend
        "[friend_2] About what happened at the party...":
            jump Fparty
        "[friend_3] About Alastor Brahe's medical history...":
            jump Fmedhist
        "Thank them for their time and give out condolences." if (friend_count["1"] >= 1 and friend_count["2"] >= 1 and friend_count["3"] >= 1):
            hide friend
            "Friend testimony has been added to your inventory."
            $ evidence.add_to_inventory(evids["Friend Testimony"])
            $ got_testimony["friends"] = True
            jump insidehospital
label Ffriend:
    "Friend: Alastor was a good friend... I just can't believe this is happening, he was just fine at the party!"
    $ friend_count["1"] += 1
    $ friend_1 = "*DONE*"
    jump friends_testimony
label Fparty:
    "Friend: Besides him collapsing all of a sudden, he acted normally."
    "Friend: We were all drinking and having fun, and like usual Alastor only drank mocktails, we were joking around and baking..."
    "Friend: ... Listen, everyone brought something for the party, juices, alcohol, and someone even brought weed."
    "Friend: We all decided to bake some brownies with it, but I know it wasn't enough to cause Alastor to collapse. We didn't even put the whole bag in!"
    $ friend_count["2"] += 1
    $ friend_2 = "*DONE*"
    jump friends_testimony
label Fmedhist:
    "Friend: I don't know too much about his medical history... He prefered to keep that private."
    "Friend: But he has mentioned in the past about not being able to drink because of some medication he was on."
    $ friend_count["3"] += 1
    $ friend_3 = "*DONE*"
    jump friends_testimony

label return_to_nina: 
    scene hospitaloutside
    show nina normal1
    n "Back already?"
    n "Well, now that you've gotten the testimonies, we should go to the lab and analyse the blood samples to double check for anything out of the ordinary."
    show nina thinknote1
    n "Normally, we wouldn't go back to the scene of the incident since there's no evidence of malicious intent..."
    n "But if you'd like to go and look around the party for possible causes of the man's death, I won't stop you."
    show nina talk
    n "Remember to follow protocol and bag everything up properly."
    n "Note that you won't be able to head there if you decide to go to the lab first."
    show nina normal1
    n "So, do you want to head straight to the lab? Or do you want to check out the house party first?"
    menu:
        "Head to the house party":
            $ want_collection_scenario = True
            jump houseoutside
        "Head to the lab":
            $ want_collection_scenario = False
            hide nina normal1
            jump lab
    return
# CODE BELOW IS FOR THE COURTROOM ------------------------------------------------------------------------------------------
# 
#
# -------------------------------------------------------------------------------------------------------------
label courtroom: # not really but this is the get score thing
    scene black
    n normal1 "Here's a review of what you did wrong/could do next time."
    n normal2 "In the Evidence Collection scenario..."
    if(want_collection_scenario):
        $ forgot = 0
        python:
            for item in can_bag:
                if(collected_objs[item] == False):
                    forgot += 1
        if (forgot > 0):
            n normal2 "You didn't collect [forgot] item(s)"
        if not check_all_scalebar():
            n normal1 "You didn't place the scalebar on every fingerprint you examined."
        if not put_gloves:
            n normal1 "You didn't put gloves on before you examined the house party scene."
    else:
        n normal1 "You didn't do anything since you skipped it."
        n normal2 "In doing so, you missed 6 pieces of evidence."
        n talk "Some of which, might've helped you in determining a better explanation for a possible cause of death."
        n talk "Anyway..."
    n normal1 "In the Lab section you..."
    python:
        count = 0
        for fingerprint in processed_prints.keys():
            if(not processed_prints[fingerprint]):
                count += 1
    if(count >0):
        n normal1 "You didn't process [count] fingerprint(s) because you either didn't collect them at the house party."
        n normal2 "Or forgot to do so at the lab."

    n normal1 "That's everything you missed!"
    n normal2 "In the courtroom, you'll be given every piece of evidence you collected and missed. So you can practice."
    n normal1 "If you didn't collect/do everything correctly, play this again!"
    return

# CODE BELOW IS FOR THE LAB ------------------------------------------------------------------------------------------
# 
#
# -------------------------------------------------------------------------------------------------------------
label lab: #initialize this section
    scene lab_hallway_idle
    show nina normal1
    n "Now that we're here in the lab, here's the hospital report."
    $ evidence.add_to_inventory(evids["Hospital Report"])
    n "And here are the photos from the scene."
    $ evidence.add_to_inventory(evids["House Party Photos"])
    hide nina normal1
    scene lab_hallway_dim
    $ in_lab = True
    #removing previous toolbox items
    $ delete_all_toolbox()
    jump lab_nonina

label lab_nonina:
    scene lab_hallway_dim
    $ last_action = "lab_nonina"
    if(has_tox):
        scene lab_hallway_idle
        show nina normal1
        n "Ready to head to the courtroom?"
        menu:
            "Yes":
                jump courtroom
            "No":
                hide nina normal1
                scene lab_hallway_dim
                call screen lab_hallway
    else:
        #show screen inventory
        call screen lab_hallway

label materials:
    hide screen inventory
    scene materials_lab
    $ delete_all_toolbox()
    call screen material_lab # choose either LC-MS or vaccuum manifold

label data_analysis:
    hide screen inventory
    scene afis_interface
    if(not bagged_objs["weedbag_print"] and not bagged_objs["pill_print"] and not bagged_objs["grape_print"]):
        n normal1 "You don't have any fingerprint to import..."
        jump lab_nonina
    elif (processed_prints["print_1"] and processed_prints["print_2"] and processed_prints["print_3"]): #if processed all them prints...
        n normal1 "You've done everything here."
        jump lab_nonina
    else:
        call screen data_analysis_lab # fingerprinting only (button)

# LC-MS CODE (includes tox report and 'additional comments') --------------------------------------------------
label lc_ms:
    scene lcms_background
    if(has_SPE_pre or has_SPE_post):
        call screen lcms_machine
    else:
        n normal1 "You don't have anything to put in the machine..."
        jump materials

label lab_prepare_lcms: # place in samples and then check computer
    "Place your sample into the machine."
    $ last_action = "lab_prepare_lcms"
    call screen inventory

label tox_report:
    scene materials_lab
    $ has_tox = True
    show nina normal1
    n "Here's the tox report from the blood samples."
    $ evidence.add_to_inventory(evids["Toxicology Report"])
    $ last_action = "tox_report2"
    jump useToxReport
label tox_report2:
    show nina talk
    n "Feel free to finish up any unfinished work."
    n "I'll be here in the hallway when you're ready to leave."
    hide nina talk
    jump materials

label lcms_peak_caf:
    call ask_peak from _call_ask_peak
    if peak == "caf":
        n normal1 "Yup, that's Caffeine!"
        show screen lcms_caf
        $ peaked["caf"] = True
        if(peaked["caf"] and peaked["fent"] and peaked["thc"]):
            $ completed_lcms[placed_in_lcms] = True
            if(completed_lcms["pre"] and completed_lcms["post"]):
                $has_SPE_pre = False
                $has_SPE_post = False
                n normal1 "Now let's get the tox report."
                hide screen lcms_post_pers
                hide screen lcms_pre_pers
                hide screen lcms_fent
                hide screen lcms_caf
                hide screen lcms_thc
                jump tox_report
            n normal2 "You'll need to analyse the other blood sample to finish the tox report."
            $peak = ""
            $placed_in_lcms = ""
            $peaked["caf"] = False
            $peaked["fent"] = False
            $peaked["thc"] = False
            hide screen lcms_post_pers
            hide screen lcms_pre_pers
            hide screen lcms_fent
            hide screen lcms_caf
            hide screen lcms_thc
            jump materials
        else:
            call screen lcms_chromatogram
    else:
        n think "That doesn't seem to be correct."
        jump lcms_peak_caf

label lcms_peak_fent:
    call ask_peak from _call_ask_peak_1
    if peak == "fent":
        n normal1 "Correct! That's the peak for Fentanyl"
        show screen lcms_fent
        $ peaked["fent"] = True
        if(peaked["caf"] and peaked["fent"] and peaked["thc"]):
            $ completed_lcms[placed_in_lcms] = True
            if(completed_lcms["pre"] and completed_lcms["post"]):
                $has_SPE_pre = False
                $has_SPE_post = False
                n normal1 "Now let's get the tox report."
                hide screen lcms_post_pers
                hide screen lcms_pre_pers
                hide screen lcms_fent
                hide screen lcms_caf
                hide screen lcms_thc
                jump tox_report
            n normal2 "You'll need to analyse the other blood sample to finish the tox report."
            $peak = ""
            $placed_in_lcms = ""
            $peaked["caf"] = False
            $peaked["fent"] = False
            $peaked["thc"] = False
            hide screen lcms_post_pers
            hide screen lcms_pre_pers
            hide screen lcms_fent
            hide screen lcms_caf
            hide screen lcms_thc
            jump materials
        else:
            call screen lcms_chromatogram
    else:
        n think "That doesn't seem to be correct."
        jump lcms_peak_fent

label lcms_peak_thc:
    call ask_peak from _call_ask_peak_2
    if peak == "thc":
        n normal1 "That's the peak for THC."
        show screen lcms_thc
        $ peaked["thc"] = True
        if(peaked["caf"] and peaked["fent"] and peaked["thc"]):
            $ completed_lcms[placed_in_lcms] = True
            if(completed_lcms["pre"] and completed_lcms["post"]):
                n normal1 "Now let's get the tox report."
                hide screen lcms_post_pers
                hide screen lcms_pre_pers
                hide screen lcms_fent
                hide screen lcms_caf
                hide screen lcms_thc
                $has_SPE_pre = False
                $has_SPE_post = False
                jump tox_report
            n normal2 "You'll need to analyse the other blood sample to finish the tox report."
            hide screen lcms_post_pers
            hide screen lcms_pre_pers
            hide screen lcms_fent
            hide screen lcms_caf
            hide screen lcms_thc
            $peak = ""
            $placed_in_lcms = ""
            $peaked["caf"] = False
            $peaked["fent"] = False
            $peaked["thc"] = False
            jump materials
        else:
            call screen lcms_chromatogram
    else:
        n think "That doesn't seem to be correct."
        jump lcms_peak_thc

label ask_peak:
    n think "What RRT belongs here?"
    menu:
        "CAF":
            $peak = "caf"
            return
        "FENT":
            $peak = "fent"
            return
        "THC":
            $peak = "thc"
            return

# lcms specific inventory functions -----
label usePpostBS:
    if last_action == "lab_prepare_lcms": #allow player to put in sample
        $ evidence.delete_from_inventory(evids["Prepared post blood sample"])
        $ placed_in_lcms = "post"
        jump usedPreparedBloodSample
    jump expression last_action

label usePpreBS:
    if last_action == "lab_prepare_lcms": #allow player to put in sample
        $ evidence.delete_from_inventory(evids["Prepared pre blood sample"])
        $ placed_in_lcms = "pre"
        jump usedPreparedBloodSample
    jump expression last_action

label usedPreparedBloodSample:
    if(not first_lcms):
        n normal1 "Let's boot up the computer while we wait for the sample to finish."
        n normal1 "Once the results are out, you'll need to identify the peaks with their corresponding relative retention time (RRT)."
        $ first_lcms = True
    scene lcms_interface
    $ renpy.pause(0.8)
    scene lcms_solo
    if(placed_in_lcms == "post"):
        show screen lcms_post_pers
        show lcms_chroma_post:
            xalign 0.5
            yalign 0.5
    elif(placed_in_lcms =="pre"):
        show screen lcms_pre_pers
        show lcms_chroma_pre:
            xalign 0.5
            yalign 0.5
    call screen lcms_chromatogram

# FINGERPRINT ANALYSIS --------------------------------------------------
label afis:
    scene afis_plain_with_bar
    $ last_action = "afis"
    call screen afis

# SOLID PHASE EXTRACTION CODE ---------------------------------------------------------------------------------------------------
# there are 5 steps for blood, 1. dilute the mixture, 2. condition the cartridge, 
# 3. load it with the sample, 4. wash the cartridge, 5. elution (obtain the extracted compound)
label solid_phase_extraction:
    # check if already done
    if added_SPE_post and added_SPE_pre:
        n normal1 "There's nothing else to do here."
        jump materials
    # adding correct toolbox items
    $ toolbox.add_to_inventory(tools["100% Methanol"])
    $ toolbox.add_to_inventory(tools["Water"])
    $ toolbox.add_to_inventory(tools["1% Formic acid"])
    $ toolbox.add_to_inventory(tools["0.1% Formic acid"])
    $ toolbox.add_to_inventory(tools["Methanol and 5% Ammonium Hydroxide"])
    #PRE-TREATMENT
    scene lab_counter_bk
    if(spe_difficulty == 0):
        show spe_dilute_1:
            xalign 0.999
            yalign 0.0
    elif(spe_difficulty == 2):
        show spe_dilute_2:
            xalign 0.999
            yalign 0.0
    else: 
        show spe_dilute_3:
            xalign 0.999
            yalign 0.0
    show beaker_empty:
        xalign 0.5
        yalign 0.5
    n normal1 "Before you do anything, you'll need to pre-treat your sample and dilute it 1:1 with an acidic buffer."
    n think "Which blood sample do you want to dilute?"
    menu:
        "Post-mortem blood sample" if not has_SPE_post:
            $ selected_blood = "post"
            show beaker_blood:
                xalign 0.5
                yalign 0.5
        "Pre-mortem blood sample" if not has_SPE_pre:
            $ selected_blood = "pre"
            show beaker_blood:
                xalign 0.5
                yalign 0.5
    jump SPE_dilute_question
label SPE_dilute_question:
    $ inv_call_SPE = "SPE_dilute_question"
    $ step_SPE = "SPE_condition"
    $ last_action = "SPE_dilute_question"
    "What will you use to dilute the blood sample?"
    call screen inventory
    return
label SPE_condition:
    if(not tookpre and selected_blood == "pre"):
        $ evidence.add_to_inventory(evids["Pre blood sample"])
        $ tookpre = True
    elif(not tookpost and selected_blood == "post"):
        $ evidence.add_to_inventory(evids["Post blood sample"])
        $ tookpost = True
    scene spe11
    show screen spe_spo
    $ inv_call_SPE = "SPE_condition"
    $ last_action = "SPE_condition"
    $ step_SPE = "SPE_condition1"
    call screen inventory
label SPE_condition1:
    scene spe12
    $ step_num_SPE = 2 # catridge has been reinsed with methanol waiting for 2
    if(askq):
        "Vacuum update to what flow rate?"
        $askq=False
    menu:
        "5 mL/minute":
            $askq=True
            jump SPE_condition2
        "1 mL/minute":
            "Wrong."
            jump SPE_condition1
label SPE_condition2:
    $ inv_call_SPE = "SPE_condition2"
    $ last_action = "SPE_condition2"
    $ step_SPE = "SPE_condition3" #1% formic acid or water
    scene spe13
    call screen inventory
label SPE_condition3:
    scene spe14
    $ step_num_SPE = 3 # catridge has been reinsed with formic or water waiting for loading
    if(askq):
        "Vacuum update to what flow rate?"
        $askq=False
    menu:
        "5 mL/minute":
            scene spe13
            $askq=True
            jump SPE_loading
        "1 mL/minute":
            "Wrong."
            jump SPE_condition3

label SPE_loading:
    $ renpy.pause(0.5, hard=True)
    scene spe21
    $ inv_call_SPE = "SPE_loading"
    $ last_action = "SPE_loading"
    $ step_SPE = "SPE_loading1"
    call screen inventory
label SPE_loading1:
    scene spe22
    $ step_num_SPE = 4 # blood in, next wash w/formic
    if(askq):
        "Vacuum update to what flow rate?"
        $askq=False
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_loading1
        "1 mL/minute":
            scene spe23
            $askq=True
            jump SPE_washing

label SPE_washing:
    $ renpy.pause(0.5, hard=True)
    scene spe31
    $ inv_call_SPE = "SPE_washing"
    $ last_action = "SPE_washing"
    $ step_SPE = "SPE_washing1"
    call screen inventory
label SPE_washing1:
    scene spe32
    $ step_num_SPE = 5 # washg fromic, next wash w/methanol
    if(askq):
        "Vacuum update to what flow rate?"
        $askq=False
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_washing1
        "1 mL/minute":
            $askq=True
            jump SPE_washing2
label SPE_washing2:
    scene spe33
    $ inv_call_SPE = "SPE_washing2"
    $ last_action = "SPE_washing2"
    $ step_SPE = "SPE_washing3" #methanol
    call screen inventory
label SPE_washing3:
    scene spe34
    $ step_num_SPE = 6 # 5% ammonium hydroxide ELUTION
    if(askq):
        "Vacuum update to what flow rate?"
        $askq=False
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_washing3
        "1 mL/minute":
            scene spe33
            $askq=True
            jump SPE_elution

label SPE_elution:
    $ renpy.pause(0.5, hard=True)
    scene spe41
    $ inv_call_SPE = "SPE_elution"
    $ last_action = "SPE_elution"
    $ step_SPE = "SPE_elution1"
    call screen inventory
label SPE_elution1:
    $ step_num_SPE = 7
    scene spe42
    if(askq):
        "Vacuum update to what flow rate?"
        $askq=False
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_elution1
        "1 mL/minute":
            $askq=True
            jump SPE_elution2
label SPE_elution2:
    scene spe43
    "What temperature should the mixture be dried at?"
    # can add the timer, so like, do fingerprinting analysis while the mixture dries
    menu:
        "37 Celsius": # this is the correct temperature, ummmm may change this
            scene spe44
            "You've obtained the prepared sample."
            if((not added_SPE_post) and has_SPE_post):
                $ evidence.add_to_inventory(evids["Prepared post blood sample"])
                $ added_SPE_post = True
            elif((not added_SPE_pre) and has_SPE_pre):
                $ evidence.add_to_inventory(evids["Prepared pre blood sample"])
                $ added_SPE_pre = True
            elif(has_SPE_post and has_SPE_pre):
                $ choice_SPE = "COMPLETED"
            # reset counter
            hide screen spe_spo
            $ step_num_SPE = 1
            jump materials
        # can add other choices here

# toolbox stuffs for SPE
label use5Amm:
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
    if(inv_call_SPE == "SPE_dilute_question"):
        n normal1 "Good! Now we'll start."
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
label usePost:
    
    if(step_num_SPE == 3):
        $ has_SPE_post = True
        $ evidence.delete_from_inventory(evids["Post blood sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE
label usePre:
    if(step_num_SPE == 3):
        $ has_SPE_pre = True
        $ evidence.delete_from_inventory(evids["Pre blood sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE

# CODE BELOW IS THE COLLECTION SCENARIO  ---------------------------------------------------------------------------
#
#
# -------------------------------------------------------------------------------------------------------------
label houseoutside:
    scene houseoutside
    hide screen inventory
    $ last_area = ""
    if(got_intro == False):
        show nina normal1
        n "Feel free to peruse the area and bag anything you find suspicious or potentially helpful."
        n "Once you're done return here and we'll head to the lab for analysis."
        hide nina normal1
        $ got_intro = True
    else:
        show nina normal1
        n "Ready to leave?"
        menu:
            "Yes, let's go to the labs":
                if check_all_bagged():
                    hide nina normal1
                    jump lab
                else:
                    n "Go back inside and make sure everything has been properly bagged."
                    n "I have a feeling you've forgotten something."
                    hide nina normal1
                    jump house
            "No, I'll look around some more":
                n "Alright, take your time."
                hide nina normal1
                jump house

label house:
    hide screen inventory
    $ delete_all_toolbox()
    $ last_action = "house"
    $toolbox.add_to_inventory(tools["gloves"])
    $toolbox.add_to_inventory(tools["Evidence Bag"])
    $toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    show screen inventory
    if collected_objs["pill"] and collected_objs["grape"]:
        scene bk_kitchen_nopillgrape
    elif collected_objs["pill"]:
        scene bk_kitchen_nopill
    elif collected_objs["grape"]:
        scene bk_kitchen_nogrape
    else: 
        scene kitchen
    $ last_area = "houseoutside"
    show screen kitchenInteractables
    $ button_yes = True
    show screen backButton
    call screen kitchenInteractables

label trashbin:
    $ delete_all_toolbox()
    $toolbox.add_to_inventory(tools["Evidence Bag"])
    $toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    $toolbox.add_to_inventory(tools["Backing Card"])
    $toolbox.add_to_inventory(tools["Scalebar"])
    $toolbox.add_to_inventory(tools["Magnetic Powder"])
    $toolbox.add_to_inventory(tools["Tape"])
    hide screen inventory
    hide screen weedbagcollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene trashinside
    $ button_yes = True
    call screen trashInteractables

label countertop:
    $ delete_all_toolbox()
    $toolbox.add_to_inventory(tools["Evidence Bag"])
    $toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    $toolbox.add_to_inventory(tools["Backing Card"])
    $toolbox.add_to_inventory(tools["Scalebar"])
    $toolbox.add_to_inventory(tools["Magnetic Powder"])
    $toolbox.add_to_inventory(tools["Tape"])
    hide screen inventory
    hide screen grapecollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene countertop
    $ button_yes = True
    call screen topInteractables

label countertopleft:
    $ delete_all_toolbox()
    $toolbox.add_to_inventory(tools["Evidence Bag"])
    $toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    $toolbox.add_to_inventory(tools["Backing Card"])
    $toolbox.add_to_inventory(tools["Scalebar"])
    $toolbox.add_to_inventory(tools["Magnetic Powder"])
    $toolbox.add_to_inventory(tools["Tape"])
    hide screen inventory
    hide screen pillcollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene countertopleft
    $ button_yes = True
    call screen topleftInteractables

# OBJECT ACTIONS -------------------------------------------
label grapeaction:
    $ button_yes = True
    $ last_area = "countertop"
    scene black
    $ click_object = "grape"
    if collected_objs["grape"] == False:
        show grape_idle:
            xalign 0.5
            yalign 0.5
        show screen grapecollect
        if dusted.get(click_object) == True:
            show fingerprint1_black:
                zoom 0.1
                xalign 0.47
                yalign 0.43
                alpha 1
        elif uvd.get(click_object) == False:
            show fingerprint1_idle:
                zoom 0.1
                xalign 0.47
                yalign 0.43
                alpha 0.7
        elif uvd.get(click_object) == True:
            show fingerprint1_white:
                zoom 0.1
                xalign 0.47
                yalign 0.43
        if scalebard.get(click_object) == True:
            show scale:
                zoom 0.14
                xalign 0.5
                yalign 0.42
                anchor (0.5, 0.5)
                rotate 80
        if taped.get(click_object) == True:
            show tapepiece:
                zoom 0.1
                xalign 0.5
                yalign 0.42
        if backed.get(click_object) == True:
            hide tapepiece
            hide scale
            hide fingerprint1_black
    $ last_action = "grapeaction"
    call screen inventory
label grapecollected:
    "Are you sure you would like to collect this? Doing so prevents you from doing any in field tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory (NOT BAGGED)":
            $ collected_objs["grape"] = True
            "The grapefruit juice bottle has been added to your inventory."
            $ evidence.add_to_inventory(evids["Grape"])
            $ num_evidence += 1
            jump expression last_action
        "No":
            jump expression last_action

label weedbagaction:
    $ button_yes = True
    $ last_area = "trash"
    scene black 
    $ click_object = "weedbag"
    if collected_objs["weedbag"] == False:
        show weedbag-idle:
            xalign 0.5
            yalign 0.5
        show screen weedbagcollect
        if dusted.get(click_object) == True:
            show fingerprint2_black:
                zoom 0.2
                xalign 0.4
                yalign 0.4
                alpha 1
        elif uvd.get(click_object) == False:
            show fingerprint2_idle:
                zoom 0.2
                xalign 0.4
                yalign 0.4
                alpha 0.7
        elif uvd.get(click_object) == True:
            show fingerprint2_white:
                zoom 0.2
                xalign 0.4
                yalign 0.4
        if scalebard.get(click_object) == True:
            show scale:
                zoom 0.3
                xalign 0.465
                yalign 0.4
                anchor (0.5, 0.5)
                rotate 280
        if taped.get(click_object) == True:
            show tapepiece:
                zoom 0.2
                xalign 0.4
                yalign 0.4
        if backed.get(click_object) == True:
            hide tapepiece
            hide scale
            hide fingerprint2_black
    $ last_action = "weedbagaction"
    call screen inventory
label weedbagcollected:
    "Are you sure you would like to collect this? Doing so prevents you from doing any in field tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory (NOT BAGGED)":
            $ collected_objs["weedbag"] = True
            "Evidence has been added to your inventory."
            $ evidence.add_to_inventory(evids["Plastic bag"])
            $ num_evidence += 1
            jump expression last_action
        "No":
            jump expression last_action

label pillaction:
    hide screen inventory
    $ button_yes = True
    $ last_area = "countertopleft"
    scene black 
    if collected_objs["pill"] == False:
        show screen pillcollect
        # if status is even, show the side view/default of the pill bottle
        if(pill_status % 2 == 0):
            $ click_object = "pill"
            show pill-idle:
                xalign 0.5
                yalign 0.5
        if (pill_status%2 == 1):
            $ click_object = "pilltop"
            show pill-top:
                xalign 0.5
                yalign 0.5
            if dusted.get(click_object) == True:
                show fingerprint1_black:
                    zoom 0.1
                    xalign 0.5
                    yalign 0.5
                    alpha 0.75
            elif uvd.get(click_object) == False:
                show fingerprint1_idle:
                    zoom 0.1
                    xalign 0.5
                    yalign 0.5
                    alpha 0.3
            elif uvd.get(click_object) == True:
                show fingerprint1_white:
                    zoom 0.1
                    xalign 0.5
                    yalign 0.5
            if scalebard.get(click_object) == True:
                show scale:
                    zoom 0.16
                    xalign 0.465
                    yalign 0.5
                    anchor (0.5, 0.5)
                    rotate 280
            if taped.get(click_object) == True:
                show tapepiece:
                    zoom 0.1
                    xalign 0.5
                    yalign 0.5
            if backed.get(click_object) == True:
                hide tapepiece
                hide scale
                hide fingerprint1_black
    $ last_action = "pillaction"
    call screen inventory
label pillcollected:
    "Are you sure you would like to collect this? Doing so prevents you from doing any in field tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory (NOT BAGGED)":
            $ collected_objs["pill"] = True
            "Evidence has been added to your inventory."
            $ evidence.add_to_inventory(evids["Pill bottle"])
            $ num_evidence += 1
            jump expression last_action
        "No":
            jump expression last_action
label pillturned:
    $ pill_status += 1
    jump expression last_action

# EVIDENCE STUFF ACTIONS -------------------------------------
# FINGERPRINTS _____
label canMagneticPowder:
    if bagging == False:
        if (click_object in can_fingerprint):
            jump useMagneticPowder
        else:
            "There are no fingerprints here."
            jump expression last_action
    elif bagging == True:
        if(need_tape):
            "You can't use this here."
        else:
            "Please select a piece of evidence"
        jump askWhatToBag

label useMagneticPowder:
    if click_object in fingerprint1_stuff:
        hide fingerprint1_idle
        hide fingerprint1_white
    else: #weedbag
        hide fingerprint2_idle
        hide fingerprint2_white
    if dusted.get(click_object) == True:
        "You've already dusted the fingerprints on this object."
    $ dusted[click_object] = True
    jump expression last_action

label useUVLight: # OPTIONAL, cant use after dusted
    if bagging == False:
        if dusted.get(click_object) == True:
            "You've already dusted the fingerprints on this object."
            jump expression last_action
        else:
            if click_object in fingerprint1_stuff:
                $ uvd[click_object] = True
                hide fingerprint1_idle
                jump expression last_action
            elif click_object in fingerprint2_stuff:
                $ uvd[click_object] = True
                hide fingerprint2_idle
                jump expression last_action
    elif bagging == True:
        if(need_tape):
            "You can't use this here."
        else:
            "Please select a piece of evidence"
        jump askWhatToBag

label useScaleBar: # (not required to bag evidence)
    if bagging == False:
        if (click_object in can_fingerprint):
            if scalebard[click_object] == True or dusted[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif taped[click_object] == True:
                "You can't use a scale bar."
                jump expression last_action
            elif dusted[click_object] == True:
                $ scalebard[click_object] = True
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        if(need_tape):
            "You can't use this here."
        else:
            "Please select a piece of evidence"
        jump askWhatToBag

label useTape: 
    if bagging == False:
        if (click_object in can_fingerprint):
            if taped[click_object] == True or dusted[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif dusted[click_object] == True: # change this to scaled[click_object] == True for scalebar to be required
                $ taped[click_object] = True
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        if(need_tape):
            "You can't use this here."
        else:
            "Please select a piece of evidence"
        jump askWhatToBag

label useBackingcard:
    if bagging == False:
        if (click_object in can_fingerprint):
            if backed[click_object] == True or taped[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif taped[click_object] == True:
                $ backed[click_object] = True
                if click_object == "weedbag":
                    if scalebard[click_object] == True:
                        $ fingerprint_toback = "finger2 S"
                        call sophisticatedFinger from _call_sophisticatedFinger
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 2 S"])
                    else:
                        $ fingerprint_toback = "finger2 NS"
                        call sophisticatedFinger from _call_sophisticatedFinger_1
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 2 NS"])
                    $  collected_objs["weedbag_print"] = True
                elif click_object == "pilltop":
                    if scalebard[click_object] == True:
                        $ fingerprint_toback = "finger1 S"
                        call sophisticatedFinger from _call_sophisticatedFinger_2
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 1 S"])
                    else:
                        $ fingerprint_toback = "finger1 NS"
                        call sophisticatedFinger from _call_sophisticatedFinger_3
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 1 NS"])
                    $ collected_objs["pill_print"] = True
                elif click_object == "grape":
                    if scalebard[click_object] == True:
                        $ fingerprint_toback = "finger3 S"
                        call sophisticatedFinger from _call_sophisticatedFinger_4
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 3 S"])
                    else:
                        $ fingerprint_toback = "finger3 NS"
                        call sophisticatedFinger from _call_sophisticatedFinger_5
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 3 NS"])
                    $ collected_objs["grape_print"] = True
                elif click_object == "pill":
                    "More than half of the print is missing from the tape."
                    "It seems like the textured surface interfered with the sample. This can't be used as evidence now."
                    $ num_evidence -= 1
                $ num_evidence += 1
                $ sf = False
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        if(need_tape):
            "You can't use this here."
        else:
            "Please select a piece of evidence"
        jump askWhatToBag

label sophisticatedFinger:
    $ sf = True
    scene dragndrop
    hide screen weedbagcollect
    hide screen pillcollect
    hide screen grapecollect
    call screen finger_drag
    if("finger2 NS" == fingerprint_toback):
        show finger2_noscale:
            xpos 1000 
            ypos 100
    elif("finger2 S" == fingerprint_toback):
        show finger2_scale:
            xpos 1000 
            ypos 100
    elif("finger1 NS" == fingerprint_toback):
        show finger1_noscale:
            xpos 1000 
            ypos 100
    elif("finger1 S" == fingerprint_toback):
        show finger1_scale:
            xpos 1000 
            ypos 100
    elif("finger3 NS" == fingerprint_toback):
        show finger1_noscale:
            xpos 1000 
            ypos 100
    elif("finger3 S" == fingerprint_toback):
        show finger1_scale:
            xpos 1000 
            ypos 100
    call screen write_drag
    return

# END OF FINGERPRINTS _____
# EVIDENCE BAG ___________________
label askWhatToBag:
    scene dragndrop
    hide screen weedbagcollect
    hide screen pillcollect
    hide screen grapecollect
    if num_evidence != 0:
        $ bagging = True
        $ backbuttonenable = False
        show openbag:
            xpos 1000 
            ypos 100
        if(not need_tape):
            "Please select the evidence you would like to bag from your inventory."
        call screen inventory
    else:
        "There's nothing in your inventory to bag. Collect it first."
        if(last_action == ''):
            jump house
        else: 
            jump expression last_action
label useTamperTape:
    if current_bag_item != "":
        if current_bag_item == "fingerprint1":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Fingerprint 1"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            $ need_tape = False
            jump expression last_action
        elif current_bag_item == "fingerprint2":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Fingerprint 2"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            $ need_tape = False
            jump expression last_action
        elif current_bag_item == "fingerprint3":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Fingerprint 3"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            $ need_tape = False
            jump expression last_action
        elif current_bag_item == "grape":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Grape"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            $ need_tape = False
            jump expression last_action
        elif current_bag_item == "weedbag":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Plastic bag"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            $ need_tape = False
            jump expression last_action
        elif current_bag_item == "pill":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Pill bottle"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            $ need_tape = False
            jump expression last_action
    else:
        "Please put evidence in an evidence bag first."
        if(last_action == ''):
            jump house
        else: 
            jump expression last_action
label remove_item:
    hide screen item_deposit_screen
    jump expression last_action

# ACTIONS for evidence in the inventory, what it do :) -------------------------------------------------
# does not include all actions for the lab section

label bagItem1: # fingerprint on the PILL BOTTLE
    if in_lab: #should not be reachable
        if last_action == "afis" and pressed == "import":
            $ imported_print = "print_1"
            $ processed_prints[imported_print] = True
            $ renpy.jump("import_print")
    else: #collection scenario
        if bagging == True and current_bag_item == "":
            $ current_bag_item = "fingerprint1"
            $ need_tape = True
            call screen item_deposit_screen
            if(scalebard["pilltop"] == True):
                $ evidence.delete_from_inventory(evids["Fingerprint 1 S"])
            else:
                $ evidence.delete_from_inventory(evids["Fingerprint 1 NS"])
            $ bagged_objs["pill_print"] = True
            call screen inventory
        elif current_bag_item != "":
            "You've already put something in the evidence bag!"
            call screen inventory
        else:
            "You need an evidence bag!"
            jump expression last_action
label bagFinger1:
    if in_lab:
        if last_action == "afis" and pressed == "import":
            $ imported_print = "print_1"
            $ processed_prints[imported_print] = True
            $ renpy.jump("import_print")
    else: #collection scenario
        jump expression last_action

label bagItem2: # fingerprint on the WEEDBAG
    if in_lab: #shouldnt be reachable
        if last_action == "afis" and pressed == "import":
            $ imported_print = "print_3"
            $ processed_prints[imported_print] = True
            $ renpy.jump("import_print")
    else: #collection scenario
        if bagging == True and current_bag_item == "":
            $ current_bag_item = "fingerprint2"
            $ need_tape = True
            call screen item_deposit_screen
            if(scalebard["weedbag"] == True):
                $ evidence.delete_from_inventory(evids["Fingerprint 2 S"])
            else:
                $ evidence.delete_from_inventory(evids["Fingerprint 2 NS"])
            $ bagged_objs["weedbag_print"] = True
            call screen inventory
        elif current_bag_item != "":
            "You've already put something in the evidence bag!"
            call screen inventory
        else:
            "You need an evidence bag!"
            jump expression last_action
label bagFinger2:
    if in_lab:
        if last_action == "afis" and pressed == "import":
            $ imported_print = "print_3"
            $ processed_prints[imported_print] = True
            $ renpy.jump("import_print")
    else: #collection scenario
        jump expression last_action

label bagItem3: # fingerprint on the GRAPEFRUIT JUICE BOTTLE
    if in_lab: #should not be reachable
        if last_action == "afis" and pressed == "import":
            $ imported_print = "print_2"
            $ processed_prints[imported_print] = True
            $ renpy.jump("import_print")
    else: #collection scenario
        if bagging == True and current_bag_item == "":
            $ current_bag_item = "fingerprint3"
            $ need_tape = True
            call screen item_deposit_screen
            if(scalebard["grape"] == True):
                $ evidence.delete_from_inventory(evids["Fingerprint 3 S"])
            else:
                $ evidence.delete_from_inventory(evids["Fingerprint 3 NS"])
            $ bagged_objs["grape_print"] = True
            call screen inventory
        elif current_bag_item != "":
            "You've already put something in the evidence bag!"
            call screen inventory
        else:
            "You need an evidence bag!"
            jump expression last_action
label bagFinger3:
    if in_lab:
        if last_action == "afis" and pressed == "import":
            $ imported_print = "print_2"
            $ processed_prints[imported_print] = True
            $ renpy.jump("import_print")
    else: #collection scenario
        jump expression last_action

label bagItem4: # grape
    if in_lab:
        jump expression last_action
    else: #collection scenario
        if bagging == True and current_bag_item == "":
            $ current_bag_item = "grape"
            $ need_tape = True
            call screen item_deposit_screen
            $ evidence.delete_from_inventory(evids["Grape"])
            $ bagged_objs["grape"] = True
            call screen inventory
        elif current_bag_item != "":
            "You've already put something in the evidence bag!"
            call screen inventory
        else:
            "You need an evidence bag!"
            jump expression last_action

label bagItem5: #for the weedbag
    if in_lab:
        "There's nothing else to do with this item."
        jump expression last_action
    else: #collection scenario
        if bagging == True and current_bag_item == "":
            $ current_bag_item = "weedbag"
            $ need_tape = True
            call screen item_deposit_screen
            $ evidence.delete_from_inventory(evids["Plastic bag"])
            $ bagged_objs["weedbag"] = True
            call screen inventory
        elif current_bag_item != "":
            "You've already put something in the evidence bag!"
            call screen inventory
        else:
            "You need an evidence bag!"
            jump expression last_action

label bagItem6: #pill bottle
    if in_lab:
        "There's nothing else to do with this item." 
        jump expression last_action
    else: #collection scenario
        if bagging == True and current_bag_item == "":
            $ current_bag_item = "pill"
            $ need_tape = True
            call screen item_deposit_screen
            $ evidence.delete_from_inventory(evids["Pill bottle"])
            $ bagged_objs["pill"] = True
            call screen inventory
        elif current_bag_item != "":
            "You've already put something in the evidence bag!"
            call screen inventory
        else:
            "You need an evidence bag!"
            jump expression last_action
label baggedPill:
    if in_lab:
        "A prescription bottle for Fentanyl containing 2 pills."
    jump expression last_action

label useGlove:
    if not put_gloves:
        "You've put gloves on."
        $ put_gloves = True
        jump house
    else:
        "You already have gloves on!"
        jump house

# report section + screens
label useHospitalReport:
    show hospital_report_full:
        xalign 0.5
        yalign 0.5
        zoom 0.6
    call screen report_return
label useToxReport:
    show tox_report_full:
        xalign 0.5
        yalign 0.5
        zoom 0.6
    call screen report_return

screen report_return:
    $ renpy.hide("hospital_report_full")
    $ renpy.hide("tox_report_full")
    imagebutton:
        auto "images/Environment Items/back_button_%s.png"
        xalign 0.99
        yalign 0.1
        action Jump(last_action)