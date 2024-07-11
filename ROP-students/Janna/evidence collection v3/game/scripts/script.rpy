# TODO: gin bottle processing scene - need to go back to crime scene house and rearrange table to look less crowded and take pictures without the bottles for game logic
# TODO: intro and outro text
# TODO: insert evidence and evidence photos in evidence bag
# TODO: get Vivian's inventory code up
# TODO: need to add the evidence markers!!!

init python:
    config.mouse = {
        "default": [("cursor.png", 0, 0)],
        "magnifying": [("default cursor.png", 0, 0)],
        "hover": [("hover cursor.png", 0, 0)],
        "dropper": [("dropper.png", 0, 49)],
        "ethanol": [("dropper filled.png", 0, 49)],
        "reagent": [("dropper filled.png", 0, 49)],
        "hydrogen": [("dropper filled.png", 0, 49)]
    }
    
    tools = {
        "uv light": False,
        "magnetic powder": False,
        "scalebar": False,
        "tape": False,
        "backing": False,
        "packaging": False,
        "tube": False,
        "bag": False,
        "tamper evident tape": False,
        "swab": False
    }

    # TODO: remember to set analyzing back to False when complete
    analyzing = {
        "handprint": False,
        "fingerprint": False,
        "bottle": False,
        "splatter": False,
        "footprint": False,
        "gin": False

    }

    # TODO: need to find a way to return to the front corridor from a piece of evidence and need to create a message for when player tries to analyze already analyzed evidence
    analyzed = {
        "handprint": False,
        "fingerprint": False,
        "bottle": False,
        "splatter": False,
        "splatter presumptive": False,
        "splatter packaged": False,
        "footprint": False,
        "footprint packaged": False,
        "footprint presumptive": False,
        "footprint enhanced": False,
        "gin": False
    }

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

    def item_dragged(drags, drop):
        if not drop:
            return

        store.dragged = drags[0].drag_name
        store.dropped = drop.drag_name

        # Hide all draggable screens
        renpy.hide_screen("sample_to_tube")
        renpy.hide_screen("fingerprint_to_bag")
        renpy.hide_screen("handprint_to_bag")
        renpy.hide_screen("tape_to_bag")

        return True

label start:
    $ default_mouse = "default"
    scene front corridor
    "Eventually, there'll be a scene briefing here."
    "But for now, go and investigate the scene!"

label corridor:
    $ default_mouse = "magnifying"
    if analyzed["gin"]:
        scene no gin
    else:
        scene front corridor
    show screen ui
    if analyzed["fingerprint"] and analyzed["handprint"] and analyzed["splatter"] and analyzed["footprint"]:
        "Well done. You've found all the evidence."
        "We'll put some outro code here that segues into the lab portion later!"
        return
    call screen front_corridor

label handprint_desc:
    show screen casefile_physical
    "This is the handprint we gathered from the door. It is slightly degraded."
    jump corridor

label fingerprint_desc:
    show screen casefile_physical
    "This is the fingerprint we gathered from the light switch next to the door knob."
    jump corridor

label gin_desc:
    show screen casefile_physical
    "This is the gin bottle we recovered from the table."
    jump corridor

label sample_splatter_desc:
    show screen casefile_physical
    if analyzed["splatter presumptive"]:
        "This is blood gathered from the splatter beside the table."
    else:
        "This is the red substance gathered from the splatter beside the table. It is unknown what this substance is at the moment."
    jump corridor

label sample_footprint_desc:
    show screen casefile_physical
    if analyzed["footprint presumptive"]:
        "This is blood gathered from the footprint."
    else:
        "This is the red substance gathered from the footprint. It is unknown what this substance is at the moment."
    jump corridor


    