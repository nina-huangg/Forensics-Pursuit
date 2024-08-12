default show_evidence = False

default q_a_bank = []
default score = 0

init python:
    def check_answer(correct_answer, choice):
        global score
        if correct_answer == choice:
            score += 1

    def load_q_a():
        global q_a_bank
        q_a_bank.append({
            'question': 'Can you tell the court why you are here? What are you testifying for today?',
            'choice_1': 'I came here for the plot >:)',
            'choice_2': 'I came here today because my boss told me to.',
            'choice_3': 'I am here to speak about the evidence collection and processing in this case and offer my opinions where relevant in the limits of my expertise',
            # 'choice_4': 'I feel bad for the victim.',
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': 'Okay, now, how did you process the scene to collect evidence?',
            'choice_1': 'The team numbered found evidence with markers, photographed them, brought them to the lab, then evidence processed on scene was photographed and collected after development.',
            'choice_2': 'My fellow officer collected some evidence and photographed it and then I numbered the rest of the evidence and processed it.',
            'choice_3': 'The team walked through and numbered found evidence with markers, onward certain exhibits were collected to bring to the lab and others were processed there.',
            # 'choice_4': 'The team walked through and numbered found evidence with markers, next everything was photographed, onward certain exhibits were collected to bring to the lab and others were processed there, then evidence processed on scene was photographed and collected after development.',
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "And does that follow correct procedure standards for forensic identification officers?",
            'choice_1': "No.",
            'choice_2': "Yes, we bagged all evidence that was collected in tamper proof sealed bags and all evidence was numbered in photos with scales present.",
            'choice_3': "Um, yeah? I don’t know.",
            'answer': "choice_2"
        })
        q_a_bank.append({
            'question': "Why did you collect the impression evidence from the Polyvinylsiloxane on the door at the scene instead of at the lab?",
            'choice_1': "Good point, maybe we should have brought the entire door to the lab and done it there instead.",
            'choice_2': "Google just said to do it there so I just did that.",
            # 'choice_3': "It looked like a fun thing to do.",
            'choice_3': "In order to maintain the evidence of the damage done to the door accurately the team made the decision to process it with Polyvinylsiloxane at the scene.",
            
            # 'choice_3': "In order to maintain the evidence of the damage done to the door accurately the team made the decision to process it with Polyvinylsiloxane at the scene. The integrity of the marks left on the door may have been comprimised in the process of removing and transporting it to the lab. Polyvinylsiloxane is a fast acting, non-toxic, non-invasive, and non-damaging product. It was in the best interest of accurate evidence preservation to take the mould of the door damage with the polyvinylsiloxane at the scene.",
            # 'choice_5': "We did it at the scene to be as quick as possible.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Why did you collect a jar lid and a piece of tape? I don’t see any blood on it in your evidence collection photos?",
            'choice_1': "It looked important so I collected it.",
            'choice_2': "Not all evidence is visible to the naked eye like spilled dried blood. We collected certain items like the lid and tape for further processing at the lab to reveal latent fingerprint impressions after development.",
            'choice_3': "Shiny and sticky!",
            # 'choice_4': "We collected it because we knew we could find latent evidence on there.",
            'answer': "choice_2"
        })
        q_a_bank.append({
            'question': "And how did you process the lid at the lab?",
            'choice_1': "We used Tapeglo. That chemical revealed a latent fingerprint impression on the lid.",
            # 'choice_2': "We used black granular fingerprint dusting. That revealed a latent fingerprint impression on the lid.",
            'choice_2': "We used Camphor powder for dusting. The chemical powder revealed a latent fingerprint impression on the lid.",
            'choice_3': "We used Camphor smoke. The soot revealed a latent fingerprint impression on the lid.",
            'answer': "choice_3"
        })
        q_a_bank.append({
            'question': "Why did you use that method?",
            'choice_1': "I googled it.",
            'choice_2': "This is an efficient way of enhancing fingerprints on non-porous substrates like a metal jar lid.",
            'choice_3': "This is an efficient way of enhancing fingerprints on porous substrates like a metal jar lid.",
            # 'choice_4': "This is an interesting way of enhancing fingerprints on substrates like a metal jar lid.",
            'answer': "choice_3"
        })
        q_a_bank.append({
            'question': "And how did you develop the tape evidence?",
            'choice_1': "Tapeglo",
            'choice_2': "Camphor smoke",
            'choice_3': "Granular dusting",
            # 'choice_4': "Polyvinylsiloxane",
            'answer': "choice_1"
        })
        q_a_bank.append({
            'question': "Why did you use that method?",
            'choice_1': "It was a cool colour.",
            'choice_2': "I googled it.",
            # 'choice_3': "Tapeglo is an efficient way of enhancing fingerprint impression evidence on the non-adhesive side of tape.",
            'choice_3': "Tapeglo is an efficient way of enhancing fingerprint impression evidence on the adhesive side of tape.",
            # 'choice_5': "Tapeglo is an efficient way of enhancing fingerprint impression evidence on anything.",
            'answer': "choice_3"
        })
        q_a_bank.append({
            'question': "Is there not any other way to develop fingerprint impression evidence on tape? Why use Tapeglo?",
            'choice_1': "No there is no other way.",
            'choice_2': "Yes there are other ways, such as sticky side powder. However, we felt that in this case the Tapeglo followed by an alternative light source is the best way to create optimal contrast and visibility.",
            # 'choice_3': "Yes, there are other ways, but the Tapeglo is always the best to use on tape.",
            'choice_3': "Yes there are other ways, but I was told to do it with Tapeglo and I do not believe in peer review so I do what I am told without thought to it.",
            # 'choice_5': "Yes there are other ways. Maybe we should have used sticky side powder but we did not.",
            'answer': "choice_2"
        })
        q_a_bank.append({
            'question': "Alright then. And did you get a match in your digital processing of the fingerprints you developed?",
            'choice_1': "Yes we got a match on our fingerprint comparison software.",
            'choice_2': "No we did not get a match on our fingerprint comparison software.",
            'choice_3': "We compared the developed fingerprints on a software that allowed us to find consistencies with other fingerprints in the database. From that we have a likelihood of origin based on consistency. We cannot for certain say that we have found a match from our developed fingerprints to a person.",
            # 'choice_4': "We compared the developed fingerprints on a software that allowed us to find matches with other fingerprints in the database. From that we have a likelihood of origin based on consistency. We can now for certain say that we have found a match from our developed fingerprints to a person.",
            'answer': "choice_3" 
        })
        q_a_bank.append({
            'question': "I’m confused. You have reported from your digital analysis that there is a likely source to the fingerprints you found. How is this not a match?",
            'choice_1': "We cannot say anything is for certain. There are no absolutes because science is probabilistic in nature.",
            'choice_2': "No we can say we found a match, we just aren’t completely sure in this case.",
            'choice_3': "We cannot say it is a match because.. um.... I don’t know.",
            # 'choice_4': "We just can’t say it’s a match.",
            # 'choice_5': "We cannot say it is a match because someone else could have that print. What if he has a twin? Maybe it’s his evil twin’s print.",
            'answer': "choice_1" 
        })
        q_a_bank.append({
            'question': "So can you tell us then who is the likely origin of your developed fingerprints from the scene based on the consistencies found in your comparison software?",
            'choice_1': "No, we don’t have any likely origin sources for the prints.",
            'choice_2': "Yes, the likely origin for the fingerprints that we are confident in based on our comparison software is Mr. X.",
            'choice_3': "Yes, the match is Mr. X.",
            'answer': "choice_2" 
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
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Pvs", "Lid", "Duct tape", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag", "Pvs kit"] # holds names for inspect pop-up text 
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

    # $player_name = ""
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    show screen full_inventory onlayer over_screens 

label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    #$environment_items = ["lid"]

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        addToInventory(["lid", "duct_tape", "pvs"])

        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            # if item == "lid":
            #     environment_sprites[-1].width = 300 / 2
            #     environment_sprites[-1].height = 231 / 2
            #     environment_sprites[-1].x = 1000
            #     environment_sprites[-1].y = 500
        
    # scene scene-1-bg at half_size - sets background image
    show screen scene1

label enter_courtroom:
    scene courtroom_bg
    with Dissolve(0.8)
    "Welcome to the courtroom!"
    "In this scene, you will give a testimony with regards to the evidence you've analyzed."
    show screen arrow_screen
    "Remember, you can click on the evidence button to remind you of your analysis results."
    hide screen arrow_screen
    "Let's get started!"

label state_name:

    python:
        name = renpy.input("First, please state your name for the record: ")

label p:
    pass

menu:
    "Do you [name] swear that the evidence you shall give the Court within trial shall be the truth, the whole truth and nothing but the truth?"
    "Yes":
        jump started
    "No":
        jump disqualified

label started:
    "Okay let's get started then."
    window hide
    jump start_questions

label disqualified:
    "You are disqualified as a witness. All witnesses must be sworn in to tell the truth during testimony." 
    "Fact: Lying or being untruthful by omission under oath is called Perjury."
    "Perjury is a serious crime and an indictable offence with a potential prison sentence of up to 14 years according to section 131.1 subsection 3 of the Criminal Code of Canada."
    "You can try again now!"
    jump p


label start_questions:
    python:
        for q_a in q_a_bank:
            renpy.call_screen("question_screen", q_a=q_a)

label end:
    call screen score_screen
    if _return == 'retry':
        jump start_questions

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

return
