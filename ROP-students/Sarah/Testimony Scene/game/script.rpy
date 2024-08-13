default show_evidence = False

default q_a_bank = []
default question_explanations = []
default score = 0
default current_question_reviewing = 1
define current_question = 1
define track_questions = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False, 11: False, 12: False, 13: False, 14: False, 15: False, 16: False, 17: False, 18: False, 19: False}

init python:
    def check_answer(correct_answer, choice):
        global score
        global track_questions
        global current_question
        if correct_answer == choice:
            score += 1
            track_questions[current_question] = True
        else:
            track_questions[current_question] = False
        current_question = current_question + 1

    def load_q_a():
        global q_a_bank
        q_a_bank.append({
            'question': "Why were the dish towel and knife bagged instead of being examined on the scene?",
            'choice_1': "To preserve the bloody fingerprint.",
            'choice_2': "To prevent contamination of the evidence and ensure further examination is done in a controlled environment.",
            'choice_3': "To ensure the integrity of the DNA on the dishcloth.",
            'choice_4': "To prioritize the collection of accessible evidence.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Why was the knife placed in an extra plastic container while being collected?",
            'choice_1': "For easier transportation of evidence.",
            'choice_2': "To ensure it is professionally preserved for court matters.",
            'choice_3': "To ensure the safety of forensic personnel and prevent cross-contamination with other evidence material.",
            'choice_4': "The extra plastic container is a step that is optional and was done as a personal choice.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Why was an Alternate Light Source (ALS) used to discover fingerprints instead of using fingerprint powder over the suspected areas?",
            'choice_1': "To identify latent fingerprints and powder the known region only and avoid unnecessary processing.",
            'choice_2': "To avoid wasting police and forensic resources and time.",
            'choice_3': "To preserve the integrity of the fingerprint using this non-invasive method.",
            'choice_4': "To avoid the risk of damaging areas or delicate surfaces with fingerprint powder.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why was black powder used to develop the latent fingerprint?",
            'choice_1': "Because it was the only option available.",
            'choice_2': "Because it is the least expensive method.",
            'choice_3': "Because it contrasted with the white background of the stove.",
            'choice_4': "Because it chemically reacted with the fingerprint to enhance it further.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Why was ALS used to detect the pool of blood and not Luminol?",
            'choice_1': "ALS is a non-destructive and non-invasive method of detection and ensures DNA integrity which can be altered or destroyed after Luminol.",
            'choice_2': "ALS is faster than Luminol as it takes less time for the blood to be detected without a chemical reaction.",
            'choice_3': "ALS is more specific than Luminol and does not produce false positives.",
            'choice_4': "ALS is more cost-effictive as Luminol is more expensive",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "How does blood react under ALS for it to be detected?",
            'choice_1': "Blood fluoresces under ALS and appears bright.",
            'choice_2': "Blood absorbs the ALS and appears dark.",
            'choice_3': "Blood changes colour under ALS and turns white.",
            'choice_4': "Blood chemically reacts under ALS and turns blue.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Why is it critical to perform a presumptive test on the pool of blood before collecting a sample?",
            'choice_1': "To determine the blood type of the sample for a preliminary report.",
            'choice_2': "To sterilize the pool of blood and prevent any contamination or alteration.",
            'choice_3': "To enhance the visual appearance of the blood sample, making it easier to photograph for court records.",
            'choice_4': "To confirm the presence of blood and ensure the sample is not contaminated.",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "Why was a picture taken of the pool of blood after treating it with luminol?",
            'choice_1': "To capture the luminescence produced due to the chemical reaction.",
            'choice_2': "To ensure all steps and procedures being carried out on the pool of blood are documented for the court.",
            'choice_3': "To produce a high-contrast image of the pool of blood for better examination and comparison to its original state.",
            'choice_4': "To verify the presence of blood since the presumptive test is not enough.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why is it important to take a picture of the evidence with and without markers?",
            'choice_1': "To ensure evidence is correctly documented for chain-of-custody purposes.",
            'choice_2': "To ensure there is an image without any interference to be used for digital image enhancement purposes.",
            'choice_3': "To provide a clear image of things in their original and unaltered state.",
            'choice_4': "To ensure two types of images are taken of the evidence for a wider variety for evidence collection.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Was the knife processed for DNA sample collection first or fingerprint enhancement, and why?",
            'choice_1': "DNA sample collection; ensures biological evidence was not degraded or compromised by fingerprint enhancement chemicals.",
            'choice_2': "Fingerprint enhancement; ensures fingerprint was not degraded or compromised by DNA swabs and presumptive tests.",
            'choice_3': "The order of processing does not matter as it has no consequence on the result.",
            'choice_4': "I chose based on convenience.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why was cyanoacrylate fuming (CA) used to develop and visualize the fingerprint on the knife rather than traditional powder?",
            'choice_1': "CA fuming is faster and more cost-effective than using traditional powders.",
            'choice_2': "CA fuming enhances the contrast of fingerprints on metallic surfaces such as the knife's blade and provides a better visualization of the print.",
            'choice_3': "CA fuming is the standard procedure for knives and other weapons in a crime scene.",
            'choice_4': "CA fuming is more effective for non-porous surfaces like metal blades since traditional powders may not adhere well, which allows for better visualization of fingerprints.",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "Why was an orange filter used when photographing the fingerprint on the knife blade?",
            'choice_1': "To block out unnecessary wavelengths of light and only capture those that enhance the fingerprint.",
            'choice_2': "To protect the camera lens from getting damaged by the ALS.",
            'choice_3': "To add more brightness to the fingerprint's background while taking pictures.",
            'choice_4': "To produce a contrast between the fingerprint and the background.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "What were the findings from the DNA analysis performed on the swab taken from the knife blade?",
            'choice_1': "The DNA profile generated was consistent with the profile of Jenny Adams, the wife.",
            'choice_2': "The DNA profile generated was consistent with the profile of the victim, Kurt Adams, the husband.",
            'choice_3': "The DNA profile generated was consistent with the profiles of both Jenny and Kurt Adams.",
            'choice_4': "The DNA profile generates was consistent with the profiles of both Kurt Adams and an unknown individual named Lucy.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What does it mean to have a mixed DNA profile?",
            'choice_1': "A mixed DNA profile indicates that the profiles have been exchanged with the original source with a profile from another case.",
            'choice_2': "A mixed DNA profile indicates that the profile identified in this case is the same profile from a cold case.",
            'choice_3': "A mixed DNA profile indicates that chemicals and different elements have been found in the DNA profile.",
            'choice_4': "A mixed DNA profile indicates that more than one source has genetically contributed to the profile.",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "Why couldn't a fingerprint be developed from the dish towel?",
            'choice_1': "The dish towel was heavily stained with blood which smudged the fingerprint.",
            'choice_2': "The dish towel is a porous substrate and hence fingerprints can not be developed from it due to their high absorbance of moisture and other substances.",
            'choice_3': "The required materials were not present to process the fingerprint as they are very rare and expensive.",
            'choice_4': "The fingerprint on the dish towel was irrelevant to the case, and hence was not processed to preserve resources.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What were the findings from the DNA analysis performed on the swab taken from the dish towel?",
            'choice_1': "No DNA profile was generated as there was an insufficient amount of DNA.",
            'choice_2': "The DNA profile generated was consisitent with the profiles of both the victim and the suspect.",
            'choice_3': "The DNA profile generated was consistent with an unknown individual named Lucy.",
            'choice_4': "The DNA profile geerated was consistent with the profile of Jenny Adams, the wife.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "What were the findings from the DNA analysis performed on the swab taken from the floor?",
            'choice_1': "No DNA profile could be generated as there was an insufficient amount of DNA.",
            'choice_2': "The DNA profile generated was consistent with the profile of Jenny Adams, the wife.",
            'choice_3': "The DNA profile generated was consistent with an unknown individual named Lucy from the DNA database.",
            'choice_4': "The DNA profile generated was consistent with the profile of the victim, Kurt Adams, the husband.",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "What were the findings of the fingerprint enhanced from the knife blade and the stove?",
            'choice_1': "Both fingerprints were consistent with Jenny Adams, the wife's, fingerprint.",
            'choice_2': "Both fingerprints were consistent with Kurt Adams, the husband's fingerprint.",
            'choice_3': "The fingerprint on the knife blade was consistent with Jenny Adams, the wife's fingerprint, while the fingerprint on the stove was consistent with Kurt Adams, the husband's fingerprint.",
            'choice_4': "The fingerprint on the knife belonged to another officer on the scene who had handled this evidence prior to collection.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Based on the evidence and findings, who is more likely to be the prime suspect?",
            'choice_1': "Kurt Adams, the husband.",
            'choice_2': "Jenny Adams, the wife.",
            'choice_3': "Neither, the perpetrator left no trace",
            'choice_4': "I cannot say with certainty who the prime suspect is.",
            'answer': 'choice_4'
        })

    def load_explanations():
        global question_explanations
        question_explanations.append("Question 1:\n A controlled environment is suggested for further examination to ensure evidence contamination chances are very low.")
        question_explanations.append("Question 2:\n Evidence like knives are sharp and hence a safety hazard. So they should be contained in a separate container that is able to preserve it in a safe manner and lower chances of cross contamination with other evidence on scene")
        question_explanations.append("Question 3:\n It's best to avoid unnecessary processing, so using an ALS first can prevent that.")
        question_explanations.append("Question 4:\n You should always use powder that contrasts in colour.")
        question_explanations.append("Question 5:\n Luminol can affect the integrity of the DNA, while ALS does not.")
        question_explanations.append("Question 6:\n Blood does not fluoresce— rather it absorbs the light coming from the ALS and hence appears darker. It can luminesce with the help of substances like Luminol and BlueStar.")
        question_explanations.append("Question 7:\n Presumptive tests are usually used to confirm the presence of blood. Forensic services are usually very backlogged and will not test a biological sample without a presumptive test. This is not only to save time and resources, but also to add another piece of evidence to the log for court purposes, and fulfills the screening of evidence on scene.")
        question_explanations.append("Question 8:\n You should always capture the luminescence produced by the luminol.")
        question_explanations.append("Question 9:\n The original and non-tampered state of the crime scene is always important to capture in the case of cross-questioning from defence counsel in court. It is important to ensure nothing is being hidden from the court and transparency is being maintained at all times.")
        question_explanations.append("Question 10:\n DNA samples should always be collected first before any other analysis.")
        question_explanations.append("Question 11:\n Cyanoacrylate fuming (CA) is more effective for non-porus surfaces such as the metal knife blade since powder may not adhere well to the knife.")
        question_explanations.append("Question 12:\n When ALS is used to enhance fingerprints, an orange filter is used to block the waves of light that are unnecessary and are reflected back from the evidence piece, and hence only the rays that are targeted on the piece are captured.")
        question_explanations.append("Question 13:\n Check the DNA analysis performed on the sample from the knife blade.")
        question_explanations.append("Question 14:\n A mixed DNA profile is when there is more than one source that has genetically contributed to the profile.")
        question_explanations.append("Question 15:\n The dish towel absorbed the blood, therefore a fingerprint could not be developed from it.")
        question_explanations.append("Question 16:\n Check the DNA analysis performed, the sample from the dish towel could not generate a complete profile.")
        question_explanations.append("Question 17:\n Check the DNA analysis performed on the sample from the floor.")
        question_explanations.append("Question 18:\n Check the fingerprint analysis that was performed.")
        question_explanations.append("Question 19:\n As an expert witness, one can only speak to the evidence and its results, and can not say or determine with certainty who is guilty in the case. An expert witness should only testify within their realm of expertise, which does not include deciding who the culprit is.")

        

    def reset_answers():
        global score 
        score = 0

label start:
    $ load_q_a()
    $ load_explanations()
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
    $inventory_item_names = ["Dish Towel", "Fingerprint From Stove", "Knife with Basic Yellow", "Photo of Fingerprint Scaled With 450nm", 
    "Photo of Hemastix Next to Knife", "Photo of Hemastix Next to Towel", "Table of Findings", "AFIS Results"] # holds names for inspect pop-up text 
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

label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    #$environment_items = ["lid"]

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        addToInventory(["dish_towel", "fingerprint_from_stove", "knife_with_basic_yellow", 
        "photo_of_fingerprint_scaled_with_450nm", "photo_of_hemastix_next_to_knife", 
        "photo_of_hemastix_next_to_towel", "table_of_findings", "afis_results"])

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

label start_questions:

    python:
        player_name = renpy.input("Please state your full name.")

    label swear_player_in:
        menu:
            "Do you, [player_name], swear that the evidence you shall give the court within trial shall be the truth, the whole truth and nothing but the truth?"
            "Yes":
                jump ask_questions
            "No":
                call screen disqualified 
                jump swear_player_in

    label ask_questions:
        $ current_question = 1
        python:
            for q_a in q_a_bank:
                renpy.call_screen("question_screen", q_a=q_a)

label end:
    call screen score_screen
    $ current_question_reviewing = 1
    python:
        for explanation in question_explanations:
            if not track_questions[current_question_reviewing]:
                renpy.call_screen("explain_question", current_question_reviewing=current_question_reviewing)
            current_question_reviewing = current_question_reviewing + 1

    call screen retry

    if _return == 'retry':
        jump start_questions

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

return
