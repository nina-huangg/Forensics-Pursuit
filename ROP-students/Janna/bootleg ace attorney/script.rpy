define config.mouse = {
    "default": [("default cursor.png", 0, 0)],
    "hover": [("hover cursor.png", 0, 0)],
    "move": [("person.png", 0, 0)]
}

default tools = {
    # Tools for footprint lifting
    "electrostatic dust print lifter": False,
    "conductive film": False,
    "lint roller": False,
    "uv light": False,
    "dust": False,
    "scalebar": False,
    "backing card": False,
    "bag": False,
    "tape": False
}

default investigated = {
    "footprint": False,
    "fingerprint": False,
    "blood": False
}

define e = Character("Ema")

# Examining blood ---------------------------------------------------------------------------------------------
label start:
    scene car side
    show ema holding glasses
    e "Hi there! Thanks for coming in today!"
    show ema normal
    e "We've got a whole lot of work to do."
    show ema serious
    e "Let me give you a briefing of the scene so far."
    e "Recently, the body of a young girl was found in a nearby river."
    "I see. So how come we're at a car rental?"
    show ema normal
    e "Today we'll be focusing on a secondary scene."
    e "It was discovered that the culprit used this car on the day of the murder."
    "Secondary scene?"
    e "Basically a scene where evidence related to the crime can be recovered."
    e "Although this isn't the exact scene of the murder, I'm sure we can uncover some clues about the perp's identity through this car."
    show ema holding glasses
    e "So let's get to work!"
    e "Hover around objects with your magnifying glass to investigate."
    e "If you see anything interesting, click on it!"

label car_side:
    call screen car_side

label car_back_unopened:
    call screen car_back_unopened

label car_inside:
    call screen opening_screen

label car_back_opened:
    scene car back opened
    if investigated["blood"]:
        e "We've covered everything here already."
        call screen car_back_unopened
    show ema normal
    "There doesn't seem to be anything here."
    show ema holding glasses
    e "That's what you think. But this bottle of luminol might say otherwise!"
    "Luminol?"
    show ema normal
    e "Oh! Is this your first time hearing about luminol?"
    e "It's not too difficult to use."
    show ema holding glasses
    e "You just need to put on these special glasses and then spray this everywhere!"
    show ema normal
    e "If you see anything glowy, then that means you've found blood."
    "I see... I'll give it a try!"
    call screen luminol

label blood_found:
    show ema serious
    "There's a pool of blood here!"
    e "The culprit must have tried to clean it up."
    e "But no matter how hard they try, they'll always leave traces of blood!"
    show ema normal
    e "So, is there anything you can deduce from this blood?"
    "I'm guessing... the body must have been stored here since it's been pooling."
    "This car was probably used to transport the body to the river."
    show ema holding glasses
    e "Ding ding! That's probably true!"
    e "Nice work so far!"
    hide screen car_back_opened
    $ investigated["blood"] = True
    
    if investigated["footprint"] and investigated["fingerprint"] and investigated["blood"]:
        jump end

    call screen car_back_unopened

# Examining footprint ---------------------------------------------------------------------------------------
label enter_splash_screen:
    if investigated["footprint"]:
        scene footprint acquired
        "I already examined this footprint."
        hide screen footprint_acquired
        call screen opening_screen
    else:
        hide screen opening_screen
        scene footprint untouched
        e "Ooh, there's a footprint! Nice catch!"
        e "Let's get to collecting!"
        $ tools["conductive film"] = True
        "First, I need to place the conductive film on the print."
        "(I just need to remember to click on the tool I want to use.)"
        call screen footprint_tools

label conductive_film:
    $ tools["conductive film"] = False
    $ tools["electrostatic dust print lifter"] = True
    scene footprint covered
    "Now, I need to adjust the electrostatic dust print lifter."
    call screen footprint_tools
    
label electrostatic: 
    $ tools["electrostatic dust print lifter"] = False
    $ tools["lint roller"] = True
    scene footprint flattened
    "Lastly, I need to flatten any air bubbles..."
    call screen footprint_tools

label lint_roller:
    scene footprint acquired
    "I did it!"
    e "Nice work!"
    $ tools["lint roller"] = False
    $ investigated["footprint"] = True
    
    if investigated["footprint"] and investigated["fingerprint"] and investigated["blood"]:
        jump end

    call screen opening_screen

# Examining fingerprint --------------------------------------------------------------------------------------
label another_label:
    if investigated["fingerprint"]:
        scene wheel backing
        "I already examined this fingerprint."
        call screen opening_screen
    scene wheel
    "Let's see if I can dig up some prints!"
    $ tools["uv light"] = True
    call screen expand_tools

label uv_light:
    call screen wheel_flashlight

label dust:
    scene wheel flashlight print
    e "Nice work! You found one!"
    e "Well I'm sure you don't need any help with this one."
    e "After all, you've dusted hundreds of prints!"
    "Right..."
    "(I just need to click on the tool I want to use.)"
    $ tools["uv light"] = False
    $ tools["dust"] = True
    show screen expand_tools
    call screen wheel_print_found

label scalebar:
    scene wheel print dusted
    e "What a clear print!"
    "(Okay, now onto the next step!)"
    $ tools["dust"] = False
    $ tools["scalebar"] = True
    scene wheel zoomed in
    call screen expand_tools

label backing:
    show screen wheel_zoomed_scalebar
    e "Amazing!"
    "(Now, I just need to do one last thing.)"
    $ tools ["scalebar"] = False
    $ tools["backing card"] = True
    call screen expand_tools

label backing_2:
    hide screen wheel_zoomed_scalebar
    scene wheel backing
    e "Great job!"
    $ investigated["fingerprint"] = True
    hide screen expand_tools
    
    if investigated["footprint"] and investigated["fingerprint"] and investigated["blood"]:
        jump end

    call screen opening_screen

label end:
    scene car side
    show ema normal
    e "It looks like we've examined everything there is to offer!"
    show ema holding glasses
    e "Good work, rookie!"
    "Thanks!"
    "So what do we do now?"
    show ema normal
    e "It's getting pretty late now, so we should call it a day."
    e "After all, we don't want to overdo it."
    show ema holding glasses
    e "The future of this case depends on us!"
    show ema normal
    e "Tomorrow we can analyze this evidence in the lab and see where it goes from there."
    e "Thanks for all your help!"
    return

# Unused labels ------------------------------------------------------------------------------------------------
label bag:
    "Time to package this."
    $ tools["backing card"] = False
    $ tools["bag"] = True
    call screen expand_tools

label tape:
    "Now, we just need to tape it."
    $ tools["bag"] = False
    $ tools["tape"] = True
    call screen expand_tools

label fingerprint_complete:
    scene wheel print dusted
    $ tools["tape"] = False
    "Done!"
    $ investigated["fingerprint"] = True
    hide screen expand_tools
    call screen opening_screen