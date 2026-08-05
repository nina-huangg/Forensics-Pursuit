init python:
    import json

    tools = load_items("jsons/toolbox.json")

    evids = load_items("jsons/evidence.json")
    evidences = set()

    #for evid in evids.values():
    #    evidence.add_to_inventory(evid)
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

    player_kastle_meyer_order = []

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

    swab = False
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
            else:
                "Alright. Now we need to do our presumptive test."
                $ toolbox.add_to_inventory(tools["Tube"])
                jump right_wall
        "Dry":
            if analyzing["small splatter"]:
                "Don't you think we should wet the swab? This blood's already dried out."
                jump swab_use_label
            else:
                "Alright. Now we need to do our presumptive test."
                $ toolbox.add_to_inventory(tools["Tube"])
                jump big_splatter

label e_use_label:
    "Adding a drop of ethanol."
    $ player_kastle_meyer_order.append("e")
    if analyzing["big splatter"]:
        jump big_splatter
    if analyzing["small splatter"]:
        jump right_wall

label r_use_label:
    "Adding a drop of reagent."
    $ player_kastle_meyer_order.append("r")
    if analyzing["big splatter"]:
        jump big_splatter
    if analyzing["small splatter"]:
        jump right_wall

label h_use_label:
    "Adding a drop of hydrogen peroxide."
    $ player_kastle_meyer_order.append("h")
    if analyzing["big splatter"]:
        jump big_splatter
    if analyzing["small splatter"]:
        jump right_wall

label kastle_meyer_fail:
    "You destroyed the evidence by putting the wrong chemical. Take another swab."
    $ player_kastle_meyer_order = []
    if analyzing["big splatter"]:
        jump big_splatter
    if analyzing["small splatter"]:
        jump right_wall

label kastle_meyer_success:
    "Great. Now you can send it to the lab."
    $ player_kastle_meyer_order = []
    if analyzing["big splatter"]:
        $ meyered["big splatter"] = True
        jump big_splatter
    if analyzing["small splatter"]:
        $ meyered["small splatter"] = True
        jump right_wall

label uv_use_label:
    if analyzing["handprint"]:
        call screen dark_overlay_with_mouse
    else:
        call screen dark_overlay_with_mouse2

label bar_use_label:
    if identified["fingerprint"]:
        "Alright, I'll just put the scalebar here..."
        $ scalebar = True
    else:
        "Don't you think you should enhance that fingerprint first?"
    jump right_wall

label hungarian_use_label:
    "I'll just spray a few drops..."
    $ identified["fingerprint"] = True 
    jump right_wall

label tape_use_label:
    if scalebar:
        "Alright, let's lift it off with the tape. Carefully now..."
        scene right wall tape
        pause 1.0
        scene right wal lifted
        $ tape = True
    else:
        "Shouldn't you use the scalebar first?"
    jump right_wall

label powder_use_label:
    if analyzing["handprint"]:
        $ identified["handprint"] = True
        scene left wall mag
        "New photo taken for evidence."
        "I should lift it with the gel now I think."
    jump left_wall

label lifter_use_label:
    if identified["handprint"]:
        "Perfect."
    else:
        "I don't think I should use that right now."
    jump left_wall

label card_use_label:
    if analyzing["handprint"]:
        "That's a big print, but I got it all on the card, thankfully."
        jump left_wall
    else:
        "Got the print."
        jump right_wall

label tube_use_label:
    "Putting the swab in a tube..."
    if analyzing["big splatter"]:
        $ tube["big splatter"] = True
        jump big_splatter
    if analyzing["small splatter"]:
        $ tube["small splatter"] = True
        jump right_wall

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
                    if analyzing["big splatter"]:
                        $ cased["big splatter"] = True
                        jump big_splatter
                    if analyzing["small splatter"]:
                        $ cased["small splatter"] = True
                        $ analyzing["small splatter"] = False
                        jump right_wall
                    if analyzing["fingerprint"]:
                        $ analyzing["fingerprint"] = False
                        jump right_wall
        else:
            "Aren't you forgetting to put that swab in a tube?"
            jump big_splatter
    if analyzing["small splatter"]:
        if tube["small splatter"] == True:
            "Nice. You've put it in the bag."
            menu:
                "Send off to the lab?"
                "Yes":
                    "Someone forgot the tamper tape."
                    jump bag_use_label
                "No":
                    "Guess we should use the tamper tape then."
                    if analyzing["big splatter"]:
                        $ cased["big splatter"] = True
                        jump big_splatter
                    if analyzing["small splatter"]:
                        $ cased["small splatter"] = True
                        $ analyzing["small splatter"] = False
                        jump right_wall
                    if analyzing["fingerprint"]:
                        $ analyzing["fingerprint"] = False
                        jump right_wall
        else:
            "Aren't you forgetting to put that swab in a tube?"
            jump right_wall
    else:
            "Nice. You've put it in the bag."
            menu:
                "Send off to the lab?"
                "Yes":
                    "Someone forgot the tamper tape."
                    jump bag_use_label
                "No":
                    "Guess we should use the tamper tape then."
                    if analyzing["handprint"]:
                        jump left_wall
                    if analyzing["big splatter"]:
                        $ cased["big splatter"] = True
                        jump big_splatter
                    if analyzing["small splatter"]:
                        $ cased["small splatter"] = True
                        $ analyzing["small splatter"] = False
                        jump right_wall
                    if analyzing["fingerprint"]:
                        $ analyzing["fingerprint"] = False
                        jump right_wall

label tamper_use_label:
    "Perfect! Now we can send it to the lab."
    if analyzing["handprint"]:
        $ toolbox.delete_from_inventory(tools["UV Light"])
        $ toolbox.delete_from_inventory(tools["Magnetic Powder"])
        $ toolbox.delete_from_inventory(tools["Gel Lifter"])
        $ toolbox.delete_from_inventory(tools["Backing Card"])
        $ toolbox.delete_from_inventory(tools["Evidence Bag"])
        $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
        $ analyzing["handprint"] = False
        $ analyzed["handprint"] = True
        $ evidence.add_to_inventory(evids["Handprint"])
    if analyzing["big splatter"]:
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
    if analyzing["small splatter"] and analyzing["fingerprint"] == False:
        $ toolbox.delete_from_inventory(tools["Swab Pack"])
        $ toolbox.delete_from_inventory(tools["Tube"])
        $ toolbox.delete_from_inventory(tools["Ethanol"])
        $ toolbox.delete_from_inventory(tools["Reagent"])
        $ toolbox.delete_from_inventory(tools["Hydrogen Peroxide"])
        $ analyzed["small splatter"] = True
        $ evidence.add_to_inventory(evids["Splatter 2"])
        $ evidences.add("sp")
        jump right_wall
    if analyzing["small splatter"] == False and analyzing["fingerprint"]:
        $ toolbox.delete_from_inventory(tools["Hungarian Red"])
        $ toolbox.delete_from_inventory(tools["Tape"])
        $ toolbox.delete_from_inventory(tools["Scalebar"])
        $ toolbox.delete_from_inventory(tools["Backing Card"])
        $ toolbox.delete_from_inventory(tools["Evidence Bag"])
        $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
        $ analyzed["fingerprint"] = True
        $ evidence.add_to_inventory(evids["Fingerprint 1"])
        $ evidences.add("f")
        jump right_wall
    if analyzing["small splatter"] and analyzing["fingerprint"]:
        $ toolbox.delete_from_inventory(tools["Hungarian Red"])
        $ toolbox.delete_from_inventory(tools["Tape"])
        $ toolbox.delete_from_inventory(tools["Scalebar"])
        $ toolbox.delete_from_inventory(tools["Backing Card"])
        $ toolbox.delete_from_inventory(tools["Evidence Bag"])
        $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])
        if "f" in evidences:
            $ evidence.add_to_inventory(evids["Splatter 2"])
        else:
            $ evidence.add_to_inventory(evids["Fingerprint"])
        $ analyzing["fingerprint"] = False
        $ analyzed["small splatter"] = True
        $ analyzed["fingerprint"] = True
    jump game

label handprint:
    "That's a pretty gnarly handprint."
    call screen inventory

label sample:
    show nina normal1
    n "Great job!"
    show nina talk
    n "There are more detailed instructions on how to use the inventory in inventory.rpy, so make sure to check that out!"
    n "Now, back to the overall structure of the game!"
    show nina thinknote1
    n "Once the player has finished collecting all their evidence, we should move on to the lab level for analysis."
    n "This won't be covered until later on though. For now, give yourselves a pat on the back!"