"""
This file contains all labels and functions related to evidence collection,
presumptive drug testing, fingerprint collection, firearm collection,
and evidence packaging.
"""

# =========================
# FINGERPRINT COLLECTION
# =========================

label fingerprint:
    if analyzed["firearm fingerprint"]:
        scene fingerprint_backing
        n "You've already collected this fingerprint."
        jump scene_room
    $ analyzing["firearm fingerprint"] = True
    scene firearm_fingerprint
    call screen inventory

label fingerprint_dusted:
    scene firearm_fingerprint_dusted
    "New photo added to evidence."
    call screen inventory

label fingerprint_taped:
    scene firearm_fingerprint_taped
    call screen inventory

label fingerprint_backing:
    scene firearm_fingerprint_backing
    call screen inventory

# =========================
# FIREARM COLLECTION
# =========================

label firearm:
    if analyzed["firearm"]:
        n "The firearm has already been collected."
        jump scene_room
    $ analyzing["firearm"] = True
    scene firearm
    "New photo added to evidence."
    n "We should package this firearm for transport to the lab."
    call screen inventory

# =========================
# COCAINE TEST
# =========================

label cocaine_test:
    if analyzed["cocaine presumptive"]:
        n "You've already completed this test."
        jump scene_room
    $ analyzing["cocaine presumptive"] = True
    scene cocaine_sample
    n "Use the Scott Reagent on the sample."
    call screen inventory

label cocaine_positive:
    scene cocaine_positive
    $ cocaine_scott_test_done = True
    n "The reagent produced the expected color change."
    call screen inventory

# =========================
# MDMA TEST
# =========================

label mdma_test:
    if analyzed["mdma presumptive"]:
        n "You've already completed this test."
        jump scene_room
    $ analyzing["mdma presumptive"] = True
    scene mdma_sample
    n "Use the Marquis Reagent on the sample."
    call screen inventory

label mdma_positive:
    scene mdma_positive
    $ mdma_marquis_test_done = True
    n "The reagent produced the expected color change."
    call screen inventory

# =========================
# METH TEST
# =========================

label meth_test:
    if analyzed["meth presumptive"]:
        n "You've already completed this test."
        jump scene_room
    $ analyzing["meth presumptive"] = True
    scene meth_sample
    n "Use the Marquis Reagent on the sample."
    call screen inventory

label meth_positive:
    scene meth_positive
    $ meth_marquis_test_done = True
    n "The reagent produced the expected color change."
    call screen inventory

# =========================
# PACKAGING
# =========================

label packaging:
    scene packaging_table
    call screen inventory

label packaging_complete:
    if analyzing["firearm fingerprint"]:
        "The fingerprint has been packaged."
        $ analyzing["firearm fingerprint"] = False
        $ analyzed["firearm fingerprint"] = True
        $ evidence.add_to_inventory(evids["Fingerprint"])
    elif analyzing["firearm"]:
        "The firearm has been packaged."
        $ analyzing["firearm"] = False
        $ analyzed["firearm"] = True
        $ evidence.add_to_inventory(evids["Firearm"])
    elif analyzing["cocaine presumptive"]:
        "The cocaine sample has been packaged."
        $ analyzing["cocaine presumptive"] = False
        $ analyzed["cocaine presumptive"] = True
        $ analyzed["cocaine packaged"] = True
        $ evidence.add_to_inventory(evids["Cocaine"])
    elif analyzing["mdma presumptive"]:
        "The MDMA sample has been packaged."
        $ analyzing["mdma presumptive"] = False
        $ analyzed["mdma presumptive"] = True
        $ analyzed["mdma packaged"] = True
        $ evidence.add_to_inventory(evids["MDMA"])
    elif analyzing["meth presumptive"]:
        "The methamphetamine sample has been packaged."
        $ analyzing["meth presumptive"] = False
        $ analyzed["meth presumptive"] = True
        $ analyzed["meth packaged"] = True
        $ evidence.add_to_inventory(evids["Meth"])
    jump scene_room

