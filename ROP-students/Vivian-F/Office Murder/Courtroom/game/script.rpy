default show_evidence = False
default inventory_item_names = ["KNAAP Footprint", "Cheque Fingerprint", "Bullet Casing Fingerprint", "Blood Carpet"] # holds names for inspect pop-up text 

default q_a_bank = []
default score = 0
default name = ''
default user_answers = []

init python:
    def check_answer(correct_answer, choice):
        global score
        if correct_answer == choice:
            score += 1
        user_answers.append(choice)

    def load_q_a():
        global q_a_bank
        q_a_bank.append({
            'question': "Can you tell the court why you are here? What are you testifying for today?",
            'choice_1': "I am here to speak about the opinions I cultivated regarding the case.",
            'choice_2': "I am here to explain what happened in this case based on all the evidence collected.",
            'choice_3': "I am here to speak about the evidence collection and processing in this case and offer my opinions where relevant in the limits of my expertise.",
            'choice_4': "I am here to speak about the evidence collection and processing in this case.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What is evidence?",
            'choice_1': "Evidence is an item of some sort relating to a case or investigation with the possibility of advancing the case or investigation.",
            'choice_2': "Evidence is an item of some sort that advances the case or investigation.",
            'choice_3': "Something the suspect left behind.",
            'choice_4': "Blood, knives, DNA, bullets.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "How did you process the scene to collect evidence? What was the order of events there?",
            'choice_1': "Our team secured the path of contamination, numbered found evidence with markers, photographed everything, and certain exhibits were collected to bring to the lab and others were processed there, which were photographed and collected after development.",
            'choice_2': "My fellow officer collected some evidence and photographed it and then I numbered the rest of the evidence and processed it.",
            'choice_3': "Our team secured the path of contamination, numbered found evidence with markers, then certain exhibits were collected to bring to the lab and others were processed there.",
            'choice_4': "The team walked through and numbered found evidence with markers, photographed everything, and certain exhibits were collected to bring to the lab and others were processed there, which were photographed and collected after development.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "And does that follow correct procedure standards for forensic identification officers?",
            'choice_1': "No, we could have improved. Nothing is absolute or for certain.",
            'choice_2': "Yes, we bagged all evidences in tamper proof sealed bags and all evidence were numbered in photos with scales present. Also, the path of contamination was adhered to and the scene was preserved in pristine condition with minimal alteration.",
            'choice_3': "Yes, we bagged all evidence and all evidence were numbered in photos with scales present. Also, the path of contamination was adhered to and the scene was preserved in pristine condition with minimal alteration.",
            'choice_4': "",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What evidence did you collect for lab processing and what did you do at the scene?",
            'choice_1': "We collected the bullet cartridge and cheque to process at the lab and processed the bloody footprint as well as the waxy/greasy footprint at the scene.",
            'choice_2': "We collected a bullet and some blood to process at the lab and processed the bloody footprint as well as the waxy/greasy footprint at the scene.",
            'choice_3': "We brought back everything to do at the lab.",
            'choice_4': "We collected the bullet cartridge and cheque to process at the lab and processed the waxy/greasy footprint at the scene.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why did you process the waxy footprint at the scene? Why not just bring the desk to the lab, a controlled and safe environment?",
            'choice_1': "It was in the best interest of evidence preservation to do the dental stone process at the scene for the waxy footprint after dusting it. If we brought back the desk to our lab we would have risked damaging the latent evidence before being able to lift it.",
            'choice_2': "We were rushing and just decided to do it there.",
            'choice_3': "We did not do it there we brought the desk to the lab to do it.",
            'choice_4': "That’s just what you do. That’s protocol.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "What happened to your bloody footprint impression evidence? It looks like a mess after processing at the scene.",
            'choice_1': "We do not know what happened there.",
            'choice_2': "We spilled fruit punch on it.",
            'choice_3': "We took photos of the original faint bloody footprint, then attempted to increase contrast with Hungarian Red dye, however, it sunk into the carpet and failed. No evidence was lost due to the original photo. No other processing was done so the attempt is not detrimental.",
            'choice_4': "We have our photos of the faint bloody footprint we originally saw. We tried processing it further and it did not work so we lost that evidence. Please disregard it Jury.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "If you brought that carpet to the lab would you have different results?",
            'choice_1': "Yes, if we cut and processed the carpet with the Hungarian red at the lab it would have yielded us results.",
            'choice_2': "No, the same thing would have happened at the lab, it would still sink into the carpet. The vital evidence is still captured by photo.",
            'choice_3': "Yes, we could have used other dyes at the lab and washed them out to try again.",
            'choice_4': "No, the same thing would have happened at the lab, it would still sink into the carpet. The difference is maybe we could have undone it if we did it at the lab in that controlled setting.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "So when you were in the lab how did you process the bullet cartridge? What method did you use?",
            'choice_1': "Gun Blue",
            'choice_2': "fingerprint powder",
            'choice_3': "dental stone",
            'choice_4': "ninhydrin",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "And how did you process the cheque?",
            'choice_1': "We used Gun Blue",
            'choice_2': "We used fingerprinting powder",
            'choice_3': "We used Camphor Smoke",
            'choice_4': "We used Ninhydrin",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "Why did you use Ninhydrin to obtain prints on the cheque?",
            'choice_1': "Ninhydrin is an efficient way of making latent prints on porous substances like paper visible.",
            'choice_2': "We did not use Ninydrin.",
            'choice_3': "Ninhydrin is an efficient way of making latent prints on non-porous substances like paper visible.",
            'choice_4': "It produces a pretty purple colour.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "But are there not other ways? Why not use DFO or another chemcial?",
            'choice_1': "Good point, maybe we should have used DFO",
            'choice_2': "Ninhydrin is always best development tool for this cheque with writing and light colour on it’s front side because Ninhydrin enhances latent prints into a dark purple colour (Rhumanns purple), offering the greatest contrast with the light background.",
            'choice_3': "Ninhydrin was the best development tool for this cheque that has writing and light colour on it’s front side because Ninhydrin enhances latent prints into a dark red colour (Rhumanns red), offering the greatest contrast with the light background.",
            'choice_4': "Ninhydrin was the best development tool for this cheque that has writing and light colour on it’s front side because Ninhydrin enhances latent prints into a dark purple colour (Rhumanns purple), offering the greatest contrast with the light background.",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "Okay I see. Let’s move back to the bullet cartidge. Why use Gun blue for it?",
            'choice_1': "Gun Blue is an efficient way to enhance and preserve latent fingerprint impressions on metals, such as those that bullet cartridges are made of because it is an acid that oxidizes the metal inversely around the ridges of the print. ",
            'choice_2': "Gun Blue is the best way to get fingerprints on all metals, big or small, always go with Gun Blue.",
            'choice_3': "Gun Blue is an efficient way to enhance and preserve latent fingerprint impressions on porous substrates, such as the metal that the bullet cartridge is made of because it is an acid that oxidizes the metal inversely around the ridges of the print.",
            'choice_4': "Gun Blue is an efficient way to enhance and preserve latent fingerprint impressions on both porous and non-porous substrates, such as the bullet cartridge medal because it is an acid that oxidizes the metal inversely around the ridges of the print.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "I see that you got a partial print on the bullet and used the cheque prints for digital comparison analysis. Why did you only get a partial print?",
            'choice_1': "It happens, not all prints left behind are perfectly clear and legible. The print on our bullet cartridge from the Ninhydrin development was our strongest print, hence uploaded to the comparison software rather than the incomplete print that yielded from the cheque.",
            'choice_2': "It happens, not all prints left behind are perfectly clear and legible. The print on our cheque from the Ninhydrin development was our strongest print, hence we uploaded it to the comparison software, rather than the incomplete print that yielded from the cartridge.",
            'choice_3': "There must have been a mistake with the Gun Blue process.",
            'choice_4': "The evidence could have been tampered with and therefore someone could have ruined the print.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Okay. Alright then. And did you get a match in your digital processing of the fingerprint you developed with Ninhydrin then?",
            'choice_1': "Yes we got a match on our fingerprint comparison software.",
            'choice_2': "No we did not get a match on our fingerprint comparison software.",
            'choice_3': "We compared the developed prints on a software that found consistencies with other prints in the database, which generates a likelihood of origin based on consistency. We cannot say for certain that we found a match from our developed fingerprints to a person. ",
            'choice_4': "We compared the developed prints on a software that found matches with other prints in the database, which generates a likelihood of origin based on consistency. We can now for certain say that we found a match from our developed fingerprints to a person.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "But you have reported from your digital analysis that there is a likely source to the fingerprints you found. How is this not a match? Explain.",
            'choice_1': "We can only report an answer of probability based on consistency between our developed fingerprint and the one in the database. We can simply have a high degree of confidence in our results based on the parameters of the analysis, but no absolute matches. ",
            'choice_2': "No we can say we found a match, we just aren’t completely sure in this case.",
            'choice_3': "Science is not probabilistic in nature and there are absolutes in theory. We simply have a low degree of confidence in our results based on the parameters of the analysis.",
            'choice_4': "We cannot say it is a match because someone else could have that print. What if he has a twin? Maybe it’s his evil twin’s print.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Alright can you tell us then who is the likely origin of your developed fingerprints from the scene based on the consistencies from comparison?",
            'choice_1': "No, we don’t have any likely origin sources for the prints.",
            'choice_2': "Yes, the likely origin for the fingerprints that we are confident in based on our comparison software is Mr. X.",
            'choice_3': "Yes, the match is Mr. X.",
            'choice_4': "",
            'answer': 'choice_2'
        })
        # Note the placeholder name for suspect is Mr. X
        
    def reset_answers():
        global score 
        global user_answers
        score = 0
        user_answers = []

label start:
    $slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for inventory
    $slot_padding = 120 / 2
    $distance_slot = slot_size[0] + slot_padding
    $first_slot_x = 105 # inventory and toolbox
    $first_slot_y = 300 # inventory and toolbox
    $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    
    # inventory
    $inventory_SM = SpriteManager(event = inventoryEvents) # sprite manager that manages inventory items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all inventory sprite objects
    $inventory_items = [] # holds inventory items
    $inventory_db_enabled = False # determines whether down arrow on inventory hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether up arrow on inventory hotbar is enabled or not

    # toolbox:
    $toolbox_SM = SpriteManager(event = toolboxEvents)
    $toolbox_sprites = []
    $toolbox_items = []
    $toolbox_db_enabled = False
    $toolbox_ub_enabled = False

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(event = toolboxPopupEvents)
    $toolboxpop_sprites = []
    $toolboxpop_items = []
    $toolboxpop_db_enabled = False
    $toolboxpop_ub_enabled = False

    python:
        addToInventory(["knaap_footprint", "cheque_fingerprint", "bullet_casing_fingerprint", "blood_carpet"])

label enter:
    scene courtroom_bg
    python:
        # maybe: pixel_width: If not None, the input is limited to being this many pixels wide, in the font used by the input to display text.
        name = renpy.input("Please enter your first and last name")
        name = name.strip()
        if not name:
            name = "John Doe"
    show screen full_inventory
    "[name], welcome to the courtroom!"
    "In this scene, you will give a testimony with regards to the evidence you've analyzed."
    show screen arrow_screen
    "Remember, you can click on the evidence button to remind you of your analysis results."
    hide screen arrow_screen
    "Let's get started!"
    window hide # hides dialogue box
    
    call screen swear

label start_questions:
    scene courtroom_bg
    "Alright, let’s begin then."
    $ load_q_a()
    python:
        for q_a in q_a_bank:
            renpy.call_screen("question_screen", q_a=q_a)

label end:
    call screen score_screen
    if _return == 'retry':
        call screen swear

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

return
