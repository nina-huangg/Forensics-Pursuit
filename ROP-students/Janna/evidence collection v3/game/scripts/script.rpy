# TODO: get Vivian's inventory code up
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
        "gel lifter": False,
        "tape": False,
        "backing": False,
        "packaging": False,
        "tube": False,
        "bag": False,
        "tamper evident tape": False,
        "swab": False
    }

    analyzing = {
        "handprint": False,
        "fingerprint": False,
        "splatter": False,
        "footprint": False,
        "gin": False

    }

    analyzed = {
        "handprint": False,
        "fingerprint": False,
        "splatter": False,
        "splatter presumptive": False,
        "splatter packaged": False,
        "footprint": False,
        "footprint packaged": False,
        "footprint presumptive": False,
        "footprint enhanced": False,
        "gin": False
    }

    encountered = {
        "door": False,
        "handprint": False,
        "fingerprint": False,
        "gin": False,
        "splatter": False,
        "footprint": False,
        "footprint enhanced": False 
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
    
    def close_menu():
        if renpy.get_screen("casefile_physical"):
            renpy.hide_screen("casefile_physical")
        elif renpy.get_screen("casefile_photos"):
            renpy.hide_screen("casefile_photos")
        elif renpy.get_screen("casefile"):
            renpy.hide_screen("casefile")
        else:
            renpy.show_screen("casefile")

define s = Character("Supervisor")

label start:
    $ default_mouse = "default"
    scene front corridor
    "{color=#30b002}July 13, 2024 8:17 AM. 1219 Address Road.{/color}"
    show ema normal
    s "Officer, glad to see you."
    show ema serious
    s "It’s been a long, long morning. We were called in pretty early- around 10am."
    s "The victim was found in this very living room."
    s "Witnesses say there was possibly a small gathering here last night. Neighbours reported shouting, but dismissed it as just general party behaviour-"
    s "-until this morning when the victim's friend came over to check in on him and found him dead in the living room."
    show ema normal
    s "Let me give you a quick rundown of what we know so far."
    s "The victim, Davis Dayid, was a 20-year-old student at the University of Rotonro, Simisaugus."
    show ema holding glasses
    s "According to the friend who found him, Davis was hosting a small get-together with a few close friends."
    show ema serious
    s "We've interviewed a few neighbours, and they reported hearing loud voices and shouting around 1am."
    s "Unfortunately, they didn't think much of it at the time, assuming it was just typical party noise."
    s "It wasn't until Davis' friend came by this morning to check on him that anyone realized something was terribly wrong."
    s "The body has been moved to the morgue, but the room itself remains untouched."
    s "I need you to be thorough."
    s "Look for any relevant evidence, collect fingerprints, and keep an eye out for possible weapons."
    s " Fair warning, there’s quite a bit of blood on this scene. I trust you know the drill by now."
    show ema normal
    s "Remember, time is of the essence. We need to gather all the evidence we can before it gets contaminated or lost."
    s "You can check your collected evidence at anytime through the casefile on the top left corner"
    show ema holding glasses
    s "Good luck, Officer. We're counting on you to help us solve this case."

    
label corridor:
    $ default_mouse = "magnifying"
    if analyzed["gin"]:
        scene no gin
    else:
        scene front corridor
    show screen ui
    if analyzed["fingerprint"] and analyzed["handprint"] and analyzed["splatter"] and analyzed["footprint"] and analyzed["gin"]:
        hide screen ui
        # For some reason only 1 displays, will fix later
        # show marker 4 at Transform(xpos=0.63, ypos=0.74, zoom=0.3)
        # show marker 2 at Transform(xpos=0.32, ypos=0.83, zoom=0.33)
        # show marker 1 at Transform(xpos=0.54, ypos=0.77, zoom= 0.32)
        show ema holding glasses
        s "Well done. It looks like you've processed quite a lot of evidence!"
        show ema normal
        s "Tomorrow you can head into the lab to analyze them."
        show ema holding glasses
        s "But for now, give yourself a pat on the back and rest well. Tomorrow's going to be a busy day!"
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


    