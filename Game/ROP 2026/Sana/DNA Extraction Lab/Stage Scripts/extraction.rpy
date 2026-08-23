init python:
    import json

    tools = load_items("toolbox.json") #Gets dictionary representing all tools contained in toolbox.json
    #samples = load_items("evidence.json")
    for tool in tools: #Loops through all keys and displays tool to inventory
        toolbox.add_to_inventory(tools[tool])
    
    toolbox.delete_from_inventory("PBS")
    
    
    evidence.reset_inventory()
    
    total_tubes = 0
    
    #Horrendously inellgant but I have spent a day and a half bashing my head against a wall. 
    last_used_item = None

    #When working with multiple 2ml tubes (e.g. tubes for sample and centrifuge balance), this variable tracks which one is currently being manipulated
    curr_sample = None

    #Holds the Tube_2ml we're transferring OUT of, while the player is choosing a destination tube. None when not transferring.
    transfer_source = None

    #Tracks which part of the tube is being transferred: "solution", "spin_column", or None when not transferring.
    transfer_mode = None
    """
    #Function(s) for adjusting current sample
    def discard_sample(sample):
        global curr_sample
        item = evidence.get_item(sample.label)
        if item is not None:
            evidence.delete_from_inventory(item)
        if curr_sample is sample:
            curr_sample = None
    """


define s = Character(name=("Nina"), image="nina")

label start:
    $evidence.reset_inventory()
    $evidence.add_to_inventory(Instance_Item(
        "Collected Sample", 
        image_name="balance_tube_idle", 
        usable=True, 
        action=use_sample, 
        description="2ml tube containing blood swab taken from crime scene for DNA extraction",
        instance=Tube_2ml("Collected Sample", mass_DNA=200, volume_solvent=400, decay_rate=1)))
    
    scene lab_hallway_idle
    show nina normal1
    s "Welcome to the lab."
    s "Today, we will focus on the extraction of DNA from the blood sample you collected."

    #This is the central variable that the extraction stage revolves around
    $curr_sample = evidence.get_item("Collected Sample").instance
    scene bio_station
    show screen extraction_lab 
    s "In front of you are all the instruments needed for the extraction process."
    show screen test
    s "I've taken the liberty of cutting the swab and placing it in 400 microliters of PBS"
    show screen sample_info
    s "What you are seeing on the screen now is what I like to call the sample control panel"
    s "Below the text displaying the label of the tube are buttons that allow you to transfer the contents of the tube or discard the tube entirely."
    s "On the far right you will notice a bar. It represents the concentration of DNA within the tube. It does not include DNA that is bound to a spin column."
    s "Keep an eye on how this bar changes throughout the extraction process!"
    show screen inventory

    s "All the tools needed for the extraction process are in your inventory."
    s "Using any given reagent automatically adds the amount called for within the lab procedure."
    s "You can swap between your sample tubes by interacting with them in the evidence tab."
    s "Good luck with the extraction, and remember: theres no one to stop you from making mistakes!"
    show nina write1 zorder -1000
    call screen inventory


label end:
    scene lab_hallway_idle
    show nina normal1

    s "All finished?"
    s "Give me a second to analyze what you extracted so I can tell you how you did"

    hide nina normal1

    "..."

    show nina normal1

    if curr_sample._decay_rate != 0:
        s "You did not properly neutralize the DNases. Make sure that you use protease and that you incubate it to optimize protein digestion!"

    if not curr_sample.proteins_washed:
        s "It seems that you did not properly remove protein impurities. Make sure that you use AW1 and centrifuge."
    
    if curr_sample.has_chaotropic_salts:
        s "There is still significant amounts of chaotropic salts attached to the DNA. Don't forget to wash them of with AW2 next time!"
    
    if curr_sample._mass_DNA != 0:
        s "You must lyse the blood cells if you want acess to the DNA. Other wise, everything else you do is useless!"
    elif curr_sample._mass_DNA_bound != 0:
        s "You've mostly done an amazing job collecting the DNA; however, you need to pull it off the spin column using buffer AE before we can use it!"
    elif curr_sample._mass_DNA_free < 100:
        s "Your DNA conentration is significantly lower than expected. Make sure you are not diluting by adding too many buffers."
        s "If thats not the case, make sure you proprely adhere the DNA to the spin column by uniformly mixing ethanol into the collected tube!"
    
    s "This was a good try. Keep practicin the extraction procedure and you will master it in no time!"
    
   
screen test():
    key "l" action Function(lambda: renpy.notify(f"{last_used_item}"))
    key "c" action Function(lambda: renpy.notify(f"{vars(curr_sample)}"))


screen extraction_lab():
    imagemap:
        #ground "bg bedroom_idle.png"
        idle "bio_station"
        hover "bio_station_hover"

        hotspot (742, 399, 224, 203) action Function(use_centrifuge)
        hotspot (996, 336, 329, 297) action Function(use_vortex_and_mini_centrifuge)
        hotspot (1357, 516, 199, 166) action Function(use_incubater)


screen incubator():
    imagebutton:
        idle "centrifuge_button_idle"
        hover "centrifuge_button_hover"
        action Function(use_incubater)

screen centrifuge():
    imagebutton:
        idle "centrifuge_button_idle"
        hover "centrifuge_button_hover"
        action Function(use_centrifuge)


screen vortex_and_mini_centrifuge():
    imagebutton:
        idle "centrifuge_button_idle"
        hover "centrifuge_button_hover"
        action Function(use_vortex_and_mini_centrifuge)



    




    
    

         
        






