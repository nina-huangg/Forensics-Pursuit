# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

#The current screen var is referred to within the inventory function which has init of -5
init python:
    import json

    tools = load_items("toolbox.json") #Gets dictionary representing all tools contained in toolbox.json
    for tool in tools: #Loops through all keys and displays tool to inventory
        toolbox.add_to_inventory(tools[tool])

    toolbox.delete_from_inventory(tools["Tape"])
    toolbox.delete_from_inventory(tools["Backing Card"])
    
    evies = load_items("evidence.json")

    #This is the invenory that will hold mistakes as the player makes them.
    mistake_inventory = Inventory()
    mistakes = load_items("mistakes.json")

    #Line below is for testing
    #for mistake in mistakes: mistake_inventory.add_to_inventory(mistakes[mistake])


define config.mouse_displayable = MouseDisplayable(
    "images/default_cursor.png", 0, 0
    ).add(
        "clean swab","images/Toolbox Items/clean_swab.png", 150, 138
        ).add(
            "red swab","images/Toolbox Items/red_swab.png", 150, 138
            ).add(
                "pink swab","images/Toolbox Items/pink_swab.png", 150, 138
                )

#-1 contaminated gloves, 0 no gloves, 1 clean gloves
define s = Character(name=("Nina"), image="nina")


label start:
    $mistake_inventory.reset_inventory()
    $evidence.reset_inventory()

    scene outside_crime_scene
    show nina normal1
    "May 16, 2026 12:17 PM. 13 Reaper's End."
    show nina talk
    s "Officer, glad you could make it"
    s "Behind me is the Peaceful Rest Senior Retirement Community."
    show nina thinknote1
    s "From what I've heard it's the best place in the city for people looking to boot their parents out of the house."
    s "At least..."
    s "...Under normal circumstances."
    show nina talk
    s "Police recieved a call around 10 this morning reporting the sudden death of a patient, Mary Sullivan, aged 75."
    s "Staff claim she was in good health during her morning check up and had no underlying health conditions."
    show nina thinknote1
    s "Mary was paid a visit by her daughter, Jane Sullivan, at around 9."
    s "Typically such a visit would be supervised."
    s "However, a facility emergency led to an hour long gap from the time Jane entered the facility, left the premises, and when Mary was found deceased."
    show nina talk
    s "The deceased has been transferred to the morgue and the initial state of the room has been preserved."
    s "That's about all the details I have for you right now, Officer."
    s "I'm sure you don't need me to tell you what to do with the scene."
    show nina normal1
    s "Good luck, Officer. We're counting on you to help us solve this case."
    
    scene bg bedroom 

    show screen open_inv

    show screen environment_tester

    call screen main

label review_mistakes:
    python:
        #This is likely an abominable way of handling the mistake presentation but it gets the job done for now.             
        
        #Use what is in evidence inventory for check on missing items
        #else: mistake_inventory.add_to_inventory(mistakes["Missing Evidence"])
        
        if scenes["angel_head"].get_state("examined"):
            if not scenes["angel_head"].get_state("scene_photographed"): mistake_inventory.add_to_inventory(mistakes["No Photo Scene"])
            if scenes["angel_head"].get_state("enhanced"): 
                if not scenes["angel_head"].get_state("enhanced_photographed"): mistake_inventory.add_to_inventory(mistakes["No Developed Fingerprint Photograph"])
            else: mistake_inventory.add_to_inventory(mistakes["Incomplete Fingerprint Development"])

        for i in range(3 - len(evidence._inventory)):
            mistake_inventory.add_to_inventory(mistakes["Missing Evidence"])


    hide screen inventory

    scene outside_crime_scene
    show nina normal1 at right
    s "All finished officer?"
    s "Lets see how you did!"
    show screen mistake_screen

    if len(mistake_inventory._inventory) == 0:
        s "Oh..."
        s "My..."
        s "Goodness..."

        $renpy.play("victory.mp3")

        s "You investigated the crime scene perfectly!"
        s "I always knew you could do it without ever making a single mistake."
        s "Feel free to try the crime scene investigation again or move on to the lab."

        
        call screen restart_game

    s "Click on the info buttons for the displayed items to learn about specific mistakes you made within the level."
    s "When you are ready to try again, press the arrow button to return to the main menu and restart."
    call screen mistake_screen


    
        



