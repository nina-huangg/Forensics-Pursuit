init python:
    """
    Below is a sample snippet of code that loads items from the toolbox and evidence json files. This adds one single tool to the toolbox and adds all evidence items into the evidence inventory, but you can modify this as needed.
    """
    import json

    tools = load_items("jsons/toolbox.json")
    toolbox.add_to_inventory(tools["Backing Card"])

    evids = load_items("jsons/evidence.json")

    for evid in evids.values():
        evidence.add_to_inventory(evid)


define n = Character(name=("Nina"), image="nina")


label start:
    scene front corridor
    call screen inventory
    

label sample:
    show nina normal1
    "You clicked on the backing card."
    "The function use_backing_card in inventory_functions.rpy jumps to this label."
    "The game will end now."
    return


label sample_2:
    show nina normal2
    n "Wow, a scalebar! I'm removing it now!"
    $ toolbox.delete_from_inventory(tools["Scalebar"])
    call screen inventory