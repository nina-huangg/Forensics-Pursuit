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
            'question': "Why were the dented vase and alcohol bottle bagged instead of being examined on the scene?",
            'choice_1': "To preserve the alcohol in the bottle from evaporating into the environment",
            'choice_2': "To prevent contamination of the evidence and ensure further examination is done in a controlled environment",
            'choice_3': "To remove bulky items from the crime scene to allow investigators to focus on more critical areas with minimal distraction",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Why was an Alternate Light Source (ALS) used to detect the pool of blood and not Luminol?",
            'choice_1': "ALS is a non-destructive and non-invasive method of detection and ensures DNA integrity which can be altered or destroyed after Luminol",
            'choice_2': "ALS is more specific than Luminol and does not produce false positives",
            'choice_3': "ALS is more cost-effective as Luminol is more expensive",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "How does blood react under ALS for it to be detected?",
            'choice_1': "Blood fluoresces under ALS and appears bright",
            'choice_2': "Blood absorbs the ALS and appears dark",
            'choice_3': "Blood changes color under ALS and turns black",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Why is it critical to perform a presumptive test on the blood splatter on the wall, and any biological sample in general, before collecting a sample for DNA analysis?",
            'choice_1': "To determine the blood type of the sample for a preliminary report",
            'choice_2': "To enhance the visual appearance of the blood sample, making it easier to photograph for court records",
            'choice_3': "To confirm the presence of blood and ensure the sample is not a contaminant",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Why is it important to close the curtains and darken the room when using ALS?",
            'choice_1': "To protect the ALS flashlights from potential damage caused by natural light",
            'choice_2': "To limit false positive reactions that can be caused with the interference of natural light",
            'choice_3': "To provide a clearer visualization of the reactions from substances, which may be diluted by natural light",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Was the vase processed for DNA sample collection first or fingerprint enhancement, and why?",
            'choice_1': "DNA sample collection; Ensures biological evidence was not degraded or compromised by fingerprint enhancement chemicals",
            'choice_2': "Fingerprint enhancement; Ensures fingerprint was not damaged  by DNA swabs and presumptive tests, ensuring they were still visible",
            'choice_3': "One of the two processes were chosen randomly",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why was cyanoacrylate fuming (CA) used to develop and visualize the fingerprint on the vase rather than a traditional powder?",
            'choice_1': "Traditional powders can damage the vase’s surface due to its antique material",
            'choice_2': "CA fuming is more effective for non-porous surfaces like metal blades since traditional powders may not adhere well, which allows for better visualization of fingerprints",
            'choice_3': "CA fuming provides a more detailed and enhanced prints than traditional powders due to the superglue used",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Why was an orange filter used when photographing the fingerprint on the vase?",
            'choice_1': "To protect the fingerprint from UV light while photographing",
            'choice_2': "To enhance the visibility of the fingerprint by adding more background brightness",
            'choice_3': "To block out unnecessary wavelengths of light and only capture those that enhance the fingerprint",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What were the findings from the DNA analysis performed on the swab taken from the vase?",
            'choice_1': "The DNA profile generated was consistent with the profile of the victim",
            'choice_2': "The DNA profile generated was consistent with the profile of the victim’s friend",
            'choice_3': "The DNA profile generated was consistent with the profiles of both the victim and his friend",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "What were the findings from the DNA analysis performed on the swab taken from the blood stain on the wall?",
            'choice_1': "The DNA profile generated was consistent with the profile of an unknown individual, who was later found to be the victim’s son",
            'choice_2': "The DNA profile generated was consistent with the profile of the victim",
            'choice_3': "The DNA profile generated was consistent with the profiles of the victim’s friend",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What were the findings from the Drug Test performed on the blood sample from the vase and wall?",
            'choice_1': "Both blood samples contained alcohol and Diphenhydramine, which is a poiso",
            'choice_2': "Both blood samples only contained alcohol",
            'choice_3': "Both blood samples did not contain any drugs",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why was white fingerprint powder used to develop the fingerprints on the alcohol bottle?",
            'choice_1': "Traditional black powder was not available ",
            'choice_2': "White powder is less likely to damage the alcohol bottle’s surface",
            'choice_3': "White powder provides better contrast on dark surfaces",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What were the findings of the fingerprints enhanced from the vase and the alcohol bottle?",
            'choice_1': "Both fingerprints were consistent with each other and belonged to the victim",
            'choice_2': "Both fingerprints were inconsistent with each other, with the print from the bottle being consistent with the victim and the print from the vase being consistent with the victim’s friend",
            'choice_3': "Both fingerprints were inconsistent with each other, with the print from the bottle being consistent with the victim’s son and the print from the vase being consistent with the victim’s friend",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Why was the alcohol bottle sent for Headspace Gas-Chromatography",
            'choice_1': "To identify the type of alcohol in the bottle ",
            'choice_2': "To check for the presence of any contaminants or other substances ",
            'choice_3': "To determine the alcohol content in the bottle ",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What were the findings from the Heasdpsace Gas-Chromatography performed on the alcohol sample from the bottle?",
            'choice_1': "The alcohol sample only contained alcohol",
            'choice_2': "The alcohol sample contained alcohol and Diphenhydramine, which is a poison",
            'choice_3': "The results were inconclusive",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "Was any insight received about the victim?",
            'choice_1': "The victim suffered a blunt force trauma to the head, which caused an injury, while poison was found in the body, being the main cause of death",
            'choice_2': "The victim suffered a blunt force trauma to the head, which was the main cause of death",
            'choice_3': "The victim had a history of consuming alcohol",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "Why is it significant that the alcohol bottle was not full and was opened when found at the crime scene?",
            'choice_1': "It suggests the bottle was tampered with before the victim’s death",
            'choice_2': "It suggests that the victim’s friend was also drinking from the bottle",
            'choice_3': "It suggests that the victim had consumed alcohol from that bottle before his death",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "Based on the findings, who can be seen as the primary suspect, and ultimately be charged?",
            'choice_1': "The victim’s friend",
            'choice_2': "The victim’s son",
            'choice_3': "An unknown individual",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What key evidence supports your theory of the prime suspect? ",
            'choice_1': "The fingerprints on the vase were consistent with the victim’s friend",
            'choice_2': "The fingerprints on the alcohol bottle were consistent with the victim’s son, and Diphenhydramine, a poison, was found in the alcohol ",
            'choice_3': "There is not enough evidence that points towards a specific individual",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "What is the main finding about the pathology report that also supports your theory?",
            'choice_1': "The victim died from an alcohol overdose",
            'choice_2': "The victim died from blunt force trauma on the head due to the vase, with the poison being a secondary factor",
            'choice_3': "The victim died from poisoning, with the head injury being a secondary factor",
            'answer': 'choice_3'
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

label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    #$environment_items = ["lid"]

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        addToInventory(["bottle_fingerprint", "vase_fingerprint", "dna_vase", "dna_wall"])

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
