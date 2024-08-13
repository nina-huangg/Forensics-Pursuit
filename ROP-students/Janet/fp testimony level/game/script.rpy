default show_evidence = False

default q_a_bank = []
default score = 0
define main_character = Character("[povname]")
define j = Character("Judge Whiskers")
define y = Character("You")
default correct = False
default correct_answer = ''
default choice = ''

label check_answer:
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False

init python:
    def check_answer(correct_answer, choice):
        global score
        if correct_answer == choice:
            score += 1

    def load_q_a():
        global q_a_bank
        q_a_bank.append({
            'question': "What evidence did you collect at the crime scene?",
            'choice_1': "Footprint in snow, Fingerprint on car handle, Crowbar, Paint Chip, Glass",
            'choice_2': "Footprint in mud, Paint Chip",
            'choice_3': "Crowbar, Paint Chip, Glass",
            'choice_4': "Footprint on car handle, fingerprint in snow, paint chip, fragment of crowbar",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "What pieces of evidence did you analyze in the lab?",
            'choice_1': "Footprint, Fingerprint on Crowbar",
            'choice_2': "Paint Chip, Footprint",
            'choice_3': "Paint Chip, Fingerprint on Crowbar",
            'choice_4': "NMR Magnet, Microfluidic Chip",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What microscopy technique did you use to analyze the paint chip?",
            'choice_1': "Gas Chromatography triple quadrupole mass spectrometry with a stereomicroscope attached",
            'choice_2': "Confocal Microscopy",
            'choice_3': "Stereo Microscopy",
            'choice_4': "Polarized Light Microscopy",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What technique did you use to lift the fingerprint from the crowbar?",
            'choice_1': "Ninhydrin",
            'choice_2': "CA Fuming",
            'choice_3': "Iodine Fuming",
            'choice_4': "Mass Spectrometry lifting",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What did you fill the two compartments with within the CA fuming chamber?",
            'choice_1': "Sulfuric Acid and Water",
            'choice_2': "Fentanyl and Trifluralin",
            'choice_3': "SuperGlue and Water",
            'choice_4': "Zinc Oxide and Water",
            'answer': 'choice_3'
        })
        ###
        q_a_bank.append({
            'question': "What solution could you have used after CA fuming to enhance the fingerprint?",
            'choice_1': "Ninhydrin",
            'choice_2': "Rhodamine 6G",
            'choice_3': "Silver Nitrate",
            'choice_4': "Ardrox",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What was the percent score on the AFIS database?",
            'choice_1': "92.2%",
            'choice_2': "94.2%",
            'choice_3': "62.2%",
            'choice_4': "80%",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Can you say, with absolute certainty, that your results are accurate?",
            'choice_1': "Yes, because science is always accurate and everything is a match.",
            'choice_2': "No, because there are alternative truths.",
            'choice_3': "No, because science is always probabilistic in nature and there are no parameters for defining absolute certainty.",
            'choice_4': "Yes, because I have years of experience working as a forensic practitioner.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What tentative classification of the car did you apply, upon your paint chip analysis??",
            'choice_1': "1988 Ford Windstar",
            'choice_2': "2018 Honda Civvy",
            'choice_3': "2001 Volkswagen Beetle",
            'choice_4': "1998 Ford Windstar",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why didn’t you use Ninhydrin to detect the fingerprint on the Crowbar?",
            'choice_1': "Ninhydrin is good for porous surfaces. The crowbar is a non-porous surface as it is metal.",
            'choice_2': "Ninhydrin is good for non-porous surfaces. The crowbar is a porous surface as it is metal.",
            'choice_3': "Ninhydrin could have dissolved the crowbar",
            'choice_4': "Ninydrine reacts with only primary amines. Ninhydrine aims to react with ammonia, which is a tertiary amine.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Could you have misidentified the layers of the paint chip?",
            'choice_1': "Yes, it is a possibility as paint chip analysis can be slightly subjective, and science is probabilistic in nature.",
            'choice_2': "No, my analysis was perfect!",
            'choice_3': "Yes, because the paint chip’s layers are difficult to see using the stereo microscopy method.",
            'choice_4': "No, because each layer was very clear.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Was the suspect drunk at the time of the crime?",
            'choice_1': "Yes, the crowbar usage indicates the suspect was under the influence of alcohol.",
            'choice_2': "No, as we shoud assume the suspect was not drunk if we have no evidence for it.",
            'choice_3': "I am unable to determine whether the suspect was drunk at the time of the crime based on the evidence I analyzed in the lab.",
            'choice_4': "Yes, based on my analysis in the lab involving blood testing.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "How fast was the suspect driving after they fled the scene?",
            'choice_1': "I assume they were going well over the speed limit as it was a residential neighbourhood.",
            'choice_2': "That information is outside of my area of expertise as I cannot determine that with the evidence I collected at the crime scene and the evidence I analyzed at the lab.",
            'choice_3': "The suspect must have been travelling at a high speed as they crashed, and a paint chip was found and collected.",
            'choice_4': "The owner report by observation that the suspect was going around a hundred an hour.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Would you let your work be affected by any potential bias towards the victim?",
            'choice_1': "No, as I am a professional and I have been trained by best practices guidelines to mitigate biases.",
            'choice_2': "Yes, but only because the evidence I discovered highly indicates that the suspect is guilty.",
            'choice_3': "No, because I am perfect and I am not affected by bias at all.",
            'choice_4': "No, but if bias happens subconsciously there's nothing I can do to try to be unbiased.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "What if the suspect was randomly touching all the neighbourhood cars, and that's how you have the fingerprint?",
            'choice_1': "As this is highly unlikely, we should assume this is not the case.",
            'choice_2': "Um seriously? No, that’s so ridiculous.",
            'choice_3': "Yes they could have but I highly doubt the suspect did this as it does not make logical sense.",
            'choice_4': "Theoretically, yes the suspect could have done this.",
            'answer': 'choice_1'
        })

    def reset_answers():
        global score 
        score = 0

label start:
    $ load_q_a()
    scene enter_courtroom_screen
    with Dissolve(1.5)

    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = True # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Screwdriver", "Laptop Fingerprint", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag", "Pvs kit"] # holds names for inspect pop-up text 
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 105 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 300 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_padding = 120 / 2 # sets padding size between toolbox slots
    $toolbox_first_slot_x = 105 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 300 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 120 / 2 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    show screen full_inventory onlayer over_screens 

label enter_courtroom:
    scene judge_normal
    with Dissolve(0.8)
    j "Welcome student. I'm Judge Whiskers, and this is Kitten Court."
    y "(Why the heck is everything in this world cat themed?)"
    j "In this scene, you will give a testimony with regards to the evidence you've analyzed."
    show screen arrow_screen
    j "Remember, you can click on the evidence button to remind you of your analysis results."
    hide screen arrow_screen
    scene judge_happy
    j "Let's get started!"
    scene judge_normal
    $ povname = renpy.input("Please state your full name for the court.", length = 32)
    j "Thank you [povname]."
    jump start_questions

label start_questions:
    j "What evidence did you collect at the crime scene?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[0])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_sweat
        j "Hmmm okay, thank you."
    
    scene judge_normal
    j "What pieces of evidence did you analyze in the lab?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[1])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_sweat
        j "Hmmm see, thank you."

    scene judge_normal
    j "What microscopy technique did you use to analyze the paint chip?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[2])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_sweat
        j "Hmmm okay, thank you."
    
    scene judge_normal
    j "What technique did you use to lift the fingerprint from the crowbar?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[3])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Thank you, good."
    else:
        scene judge_sweat
        j "Hmmm okay, thank you."
    
    scene judge_normal
    j "What did you fill the two compartments with within the CA fuming chamber?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[4])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_sweat
        j "Hmmm okay, thank you."
    ###
    scene judge_normal
    j "What solution did you use after CA fuming to enhance the fingerprint?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[5])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_sweat
        j "Hmmm okay, thank you."
    
    scene judge_normal
    j "What was the percent score on the AFIS database?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[6])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_sweat
        j "Hmmm okay, thank you."

    scene judge_normal
    j "Can you say, with absolute 100 percent certainty, that your results are accurate?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[7])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_woozy
        j "Alright then..."
    
    scene judge_normal
    j "What tentative classification of the car did you apply, upon your paint chip analysis?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[8])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_woozy
        j "Alright then..."
    
    scene judge_normal
    j "Why didn’t you use Ninhydrin to detect the fingerprint on the Crowbar?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[9])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_woozy
        j "Alright then..."

    scene judge_normal
    j "Could you have misidentified the layers of the paint chip?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[10])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_bruh
        j "Hmmm... okay..."

    scene judge_normal
    j "Was the suspect drunk at the time of the crime?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[11])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_woozy
        j "Alright then..."
    
    scene judge_normal
    j "How fast was the suspect driving after they fled the scene?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[12])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_woozy
        j "Okay..."
    
    scene judge_normal
    j "Has your car ever been stolen before?"
menu:
    "Yes":
        jump bias
    "No":
        jump questions_cont

label bias:
    scene judge_normal
    j "So would you let your work be affected by any potential bias towards the victim?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[13])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_woozy
        j "Alright then..."

label questions_cont:
    scene judge_normal
    j "Could the suspect have theoretically just have been going around the neighbourhood touching car door handles? What if that is how you obtained that fingerprint?"
    python:
        renpy.call_screen("question_screen", q_a=q_a_bank[14])
    if correct_answer == choice:
        $ score = score + 1
        $ correct = True
    else:
        $ correct = False
    if correct:
        scene judge_happy
        j "Great, thank you."
    else:
        scene judge_bruh
        j "Okay..."

    # python:
    #     for q_a in q_a_bank:
    #         renpy.call_screen("question_screen", q_a=q_a)

label end:

    call screen score_screen
    if _return == 'retry':
        jump start_questions

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

return
