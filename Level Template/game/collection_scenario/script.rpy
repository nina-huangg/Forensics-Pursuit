init python:
    import json

    tools = load_items("jsons/toolbox.json")
    toolbox.add_to_inventory(tools["Backing Card"])
    # toolbox.add_to_inventory(tools["Scalebar"])

    evids = load_items("jsons/evidence.json")

    for evid in evids.values():
        evidence.add_to_inventory(evid)


define n = Character(name=("Nina"), image="nina")


label start:
    scene front corridor
    show nina normal1
    n "This is a template project that you can use to create your levels!"
    n "My name is Nina and I'm usually in the evidence collection level."
    n "This level is where you collect evidence to be later analyzed in the lab."
    show nina talk
    n "All code related to this level should be placed under the collection_scenario folder."
    n "You can have as many subdirectories as you'd like underneath it!"
    show nina normal1
    n "There will be three levels in your game: the evidence collection level, the lab level, and the courtroom level."
    n "There's one directory for each level."
    n "All levels use an inventory system which will be shown on the left-hand side."
    show nina thinknote1
    n "Try playing around with it!"
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
    return