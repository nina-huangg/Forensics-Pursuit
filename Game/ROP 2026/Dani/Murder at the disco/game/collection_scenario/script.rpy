init python:
    import json

    tools = load_items("jsons/toolbox.json")

    evids = load_items("jsons/evidence.json")
    evidences = set()

    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False

    valid_kastle_meyer_orders = [
        ["e", "r", "h"],
        ["e", "r", "r", "h"],
        ["e", "r", "h", "h"],
        ["e", "r", "r", "h", "h"],
        ["e", "e", "r", "h"],
        ["e", "e", "r", "r", "h"],
        ["e", "e", "r", "h", "h"],
        ["e", "e", "r", "r", "h", "h"]
    ]

    # FIX: scoped per area instead of one shared list, so an abandoned test
    # on one sample can't bleed into the other.
    player_kastle_meyer_order = {
        "big splatter": [],
        "small splatter": []
    }

    encountered = {
        "big splatter": False,
        "small splatter": False,
        "handprint": False,
        "fingerprint": False
    }

    analyzing = {
        "big splatter": False,
        "small splatter": False,
        "handprint": False,
        "fingerprint": False
    }

    identified = {
        "big splatter": False,
        "small splatter": False,
        "handprint": False,
        "fingerprint": False
    }

    # FIX: these now actually gate the steps that follow them.
    swabbed = {
        "big splatter": False,
        "small splatter": False
    }

    uv_found = {
        "handprint": False
    }

    lifted = {
        "handprint": False,
        "fingerprint": False
    }

    carded = {
        "handprint": False,
        "fingerprint": False
    }

    scalebar = False
    tape = False

    tube = {
        "big splatter": False,
        "small splatter": False
    }

    cased = {
        "big splatter": False,
        "small splatter": False,
        "handprint": False,
        "fingerprint": False
    }

    analyzed = {
        "big splatter": False,
        "small splatter": False,
        "handprint": False,
        "fingerprint": False
    }

    meyered = {
        "big splatter": False,
        "small splatter": False
    }

    def check_kastle_meyer(current_order):
        for valid_order in valid_kastle_meyer_orders:
            if current_order == valid_order:
                return "complete"
            if current_order == valid_order[:len(current_order)]:
                return "progress"
        return "fail"

define n = Character(name=("Nina"), image="nina")


label start:
    scene storyboard
    show nina normal1 at left
    n "Hello detective. I'm detective Nina. It's a sad case today. A case of murder."
    n "After what must've been an argument between a trio of partygoers, one Joseph Talywn was stabbed in the throat."
    show nina thinknote1 at left
    n "All items on the scene have been sent off to the lab. You've got to help me analyze the scene."
    n "You should keep in mind that thanks to the two suspectst that we apprehended, we know that they only put their hands on the upper areas of the walls."
    n "Good luck. I'm here to guide you but I trust you know what to do."
    jump game

label game:
    hide nina normal1
    hide nina thinknote1
    if analyzed["big splatter"] and analyzed["small splatter"] and analyzed["handprint"] and analyzed["fingerprint"]:
        show nina normal1
        n "Well, that's all the evidence of the case. Thanks for all your help, detective. I'll see you in the lab."
        return
    show screen inventory
    call screen storyboard

label swab_use_label:
    menu:
        "Would you like to use a wet or dry swab?"
        "Wet":
            if analyzing["big splatter"]:
                "I don't think wetting the swab is necessary, the blood's still wet."
                jump swab_use_label
            elif analyzing["small splatter"]:
                "Alright. Now we need to do our presumptive test."
                $ swabbed["small splatter"] = True
                jump right_wall
            else:
                jump game
        "Dry":
            if analyzing["small splatter"]:
                "Don't you think we should wet the swab? This blood's already dried out."
                jump swab_use_label
            elif analyzing["big splatter"]:
                "Alright. Now we need to do our presumptive test."
                $ swabbed["big splatter"] = True
                jump big_splatter
            else:
                jump game

label e_use_label:
    if analyzing["big splatter"] and swabbed["big splatter"] and not meyered["big splatter"]:
        "Adding a drop of ethanol."
        $ player_kastle_meyer_order["big splatter"].append("e")
        jump big_splatter
    elif analyzing["small splatter"] and swabbed["small splatter"] and not meyered["small splatter"]:
        "Adding a drop of ethanol."
        $ player_kastle_meyer_order["small splatter"].append("e")
        jump right_wall
    elif analyzing["big splatter"] or analyzing["small splatter"]:
        "I should swab the sample before testing it."
        jump game
    else:
        jump game

label r_use_label:
    if analyzing["big splatter"] and swabbed["big splatter"] and not meyered["big splatter"]:
        "Adding a drop of reagent."
        $ player_kastle_meyer_order["big splatter"].append("r")
        jump big_splatter
    elif analyzing["small splatter"] and swabbed["small splatter"] and not meyered["small splatter"]:
        "Adding a drop of reagent."
        $ player_kastle_meyer_order["small splatter"].append("r")
        jump right_wall
    elif analyzing["big splatter"] or analyzing["small splatter"]:
        "I should swab the sample before testing it."
        jump game
    else:
        jump game

label h_use_label:
    if analyzing["big splatter"] and swabbed["big splatter"] and not meyered["big splatter"]:
        "Adding a drop of hydrogen peroxide."
        $ player_kastle_meyer_order["big splatter"].append("h")
        jump big_splatter
    elif analyzing["small splatter"] and swabbed["small splatter"] and not meyered["small splatter"]:
        "Adding a drop of hydrogen peroxide."
        $ player_kastle_meyer_order["small splatter"].append("h")
        jump right_wall
    elif analyzing["big splatter"] or analyzing["small splatter"]:
        "I should swab the sample before testing it."
        jump game
    else:
        jump game

label kastle_meyer_fail:
    "You destroyed the evidence by putting the wrong chemical. Take another swab."
    if analyzing["big splatter"]:
        $ player_kastle_meyer_order["big splatter"] = []
        $ swabbed["big splatter"] = False
        jump big_splatter
    elif analyzing["small splatter"]:
        $ player_kastle_meyer_order["small splatter"] = []
        $ swabbed["small splatter"] = False
        jump right_wall
    else:
        jump game

label kastle_meyer_success:
    "Great. Now you can send it to the lab."
    if analyzing["big splatter"]:
        $ player_kastle_meyer_order["big splatter"] = []
        $ meyered["big splatter"] = True
        $ identified["big splatter"] = True
        jump big_splatter
    elif analyzing["small splatter"]:
        $ player_kastle_meyer_order["small splatter"] = []
        $ meyered["small splatter"] = True
        $ identified["small splatter"] = True
        jump right_wall
    else:
        jump game

label uv_use_label:
    if analyzing["handprint"]:
        call screen dark_overlay_with_mouse
    else:
        "There's nothing here to search with the UV light right now."
        jump game

label bar_use_label:
    if identified["fingerprint"]:
        "Alright, I'll just put the scalebar here..."
        $ scalebar = True
    else:
        "Don't you think you should enhance that fingerprint first?"
    jump right_wall

label hungarian_use_label:
    if analyzing["fingerprint"]:
        "I'll just spray a few drops..."
        $ identified["fingerprint"] = True
    else:
        "There's nothing here that needs that yet."
    jump right_wall

label tape_use_label:
    if scalebar:
        "Alright, let's lift it off with the tape. Carefully now..."
        scene right wall tape
        pause 1.0
        scene right wall lifted
        $ tape = True
        $ lifted["fingerprint"] = True
    else:
        "Shouldn't you use the scalebar first?"
    jump right_wall

label powder_use_label:
    if analyzing["handprint"] and uv_found["handprint"]:
        $ identified["handprint"] = True
        scene left wall mag
        "New photo taken for evidence."
        "I should lift it with the gel now I think."
    elif analyzing["handprint"]:
        "I should search this wall with the UV light first."
    jump left_wall

label lifter_use_label:
    if identified["handprint"]:
        "Perfect."
        $ lifted["handprint"] = True
    else:
        "I don't think I should use that right now."
    jump left_wall

label card_use_label:
    if analyzing["handprint"]:
        if lifted["handprint"]:
            "That's a big print, but I got it all on the card, thankfully."
            $ carded["handprint"] = True
        else:
            "I should lift the print with the gel first."
        jump left_wall
    else:
        if lifted["fingerprint"]:
            "Got the print."
            $ carded["fingerprint"] = True
        else:
            "I should lift the print with the tape first."
        jump right_wall

label tube_use_label:
    if analyzing["big splatter"] and meyered["big splatter"]:
        "Putting the swab in a tube..."
        $ tube["big splatter"] = True
        jump big_splatter
    elif analyzing["small splatter"] and meyered["small splatter"]:
        "Putting the swab in a tube..."
        $ tube["small splatter"] = True
        jump right_wall
    elif analyzing["big splatter"] or analyzing["small splatter"]:
        "I should finish the presumptive test on the swab first."
        jump game
    else:
        jump game

label bag_use_label:
    if analyzing["big splatter"]:
        if tube["big splatter"] == True:
            "Nice. You've put it in the bag."
            menu:
                "Send off to the lab?"
                "Yes":
                    "Someone forgot the tamper tape."
                    jump bag_use_label
                "No":
                    "Guess we should use the tamper tape then."
                    $ cased["big splatter"] = True
                    jump big_splatter
        else:
            "Aren't you forgetting to put that swab in a tube?"
            jump big_splatter
    elif analyzing["small splatter"]:
        if tube["small splatter"] == True:
            "Nice. You've put it in the bag."
            menu:
                "Send off to the lab?"
                "Yes":
                    "Someone forgot the tamper tape."
                    jump bag_use_label
                "No":
                    "Guess we should use the tamper tape then."
                    $ cased["small splatter"] = True
                    jump right_wall
        else:
            "Aren't you forgetting to put that swab in a tube?"
            jump right_wall
    elif analyzing["handprint"]:
        if carded["handprint"]:
            "Nice. You've put it in the bag."
            menu:
                "Send off to the lab?"
                "Yes":
                    "Someone forgot the tamper tape."
                    jump bag_use_label
                "No":
                    "Guess we should use the tamper tape then."
                    $ cased["handprint"] = True
                    jump left_wall
        else:
            "We should get this print onto a backing card before we bag it."
            jump left_wall
    elif analyzing["fingerprint"]:
        if carded["fingerprint"]:
            "Nice. You've put it in the bag."
            menu:
                "Send off to the lab?"
                "Yes":
                    "Someone forgot the tamper tape."
                    jump bag_use_label
                "No":
                    "Guess we should use the tamper tape then."
                    $ cased["fingerprint"] = True
                    jump right_wall
        else:
            "We should get this print onto a backing card before we bag it."
            jump right_wall
    else:
        jump game

label tamper_use_label:
    if analyzing["handprint"]:
        if cased["handprint"]:
            "Perfect! Now we can send it to the lab."
            $ toolbox.delete_from_inventory(tools["UV Light"])
            $ toolbox.delete_from_inventory(tools["Magnetic Powder"])
            $ toolbox.delete_from_inventory(tools["Gel Lifter"])
            $ toolbox.delete_from_inventory(tools["Backing Card"])
            $ toolbox.delete_from_inventory(tools["Evidence Bag"])
            $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
            $ analyzing["handprint"] = False
            $ analyzed["handprint"] = True
            $ evidence.add_to_inventory(evids["Handprint"])
        else:
            "We need to bag this before we can seal it."
        jump game

    elif analyzing["big splatter"]:
        if cased["big splatter"]:
            "Perfect! Now we can send it to the lab."
            $ toolbox.delete_from_inventory(tools["Swab Pack"])
            $ toolbox.delete_from_inventory(tools["Tube"])
            $ toolbox.delete_from_inventory(tools["Ethanol"])
            $ toolbox.delete_from_inventory(tools["Reagent"])
            $ toolbox.delete_from_inventory(tools["Hydrogen Peroxide"])
            $ toolbox.delete_from_inventory(tools["Evidence Bag"])
            $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
            $ analyzing["big splatter"] = False
            $ analyzed["big splatter"] = True
            $ evidence.add_to_inventory(evids["Splatter"])
        else:
            "We need to bag this before we can seal it."
        jump game

    elif analyzing["small splatter"]:
        if cased["small splatter"]:
            "Perfect! Now we can send it to the lab."
            $ toolbox.delete_from_inventory(tools["Swab Pack"])
            $ toolbox.delete_from_inventory(tools["Tube"])
            $ toolbox.delete_from_inventory(tools["Ethanol"])
            $ toolbox.delete_from_inventory(tools["Reagent"])
            $ toolbox.delete_from_inventory(tools["Hydrogen Peroxide"])
            $ analyzed["small splatter"] = True
            $ evidence.add_to_inventory(evids["Splatter 2"])
            $ evidences.add("sp")
        else:
            "We need to bag this before we can seal it."
        jump right_wall

    elif analyzing["fingerprint"]:
        if cased["fingerprint"]:
            "Perfect! Now we can send it to the lab."
            $ toolbox.delete_from_inventory(tools["Hungarian Red"])
            $ toolbox.delete_from_inventory(tools["Tape"])
            $ toolbox.delete_from_inventory(tools["Scalebar"])
            $ toolbox.delete_from_inventory(tools["Backing Card"])
            $ toolbox.delete_from_inventory(tools["Evidence Bag"])
            $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
            $ analyzed["fingerprint"] = True
            $ analyzing["fingerprint"] = False
            $ evidence.add_to_inventory(evids["Fingerprint 1"])
            $ evidences.add("f")
        else:
            "We need to bag this before we can seal it."
        jump game

    else:
        jump game

label handprint:
    # FIX: this used to fall through into `label sample` because it had no
    # jump/return at the end.
    $ uv_found["handprint"] = True
    "That's a pretty gnarly handprint."
    jump left_wall

label sample:
    show nina normal1
    n "Great job!"
    show nina talk
    n "There are more detailed instructions on how to use the inventory in inventory.rpy, so make sure to check that out!"
    n "Now, back to the overall structure of the game!"
    show nina thinknote1
    n "Once the player has finished collecting all their evidence, we should move on to the lab level for analysis."
    n "This won't be covered until later on though. For now, give yourselves a pat on the back!"