# default show_evidence = False
# default inventory_item_names = ["KNAAP Footprint", "Cheque Fingerprint", "Bullet Casing Fingerprint", "Blood Carpet"] # holds names for inspect pop-up text 

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
            'question': "Which area were you responsible to collect evidence from at the scene?",
            'choice_1': "Bedroom",
            'choice_2': "Kitchen",
            'choice_3': "Washroom",
            'choice_4': "Walk-in closet",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What evidence had you collected from the scene?",
            'choice_1': "A bloodied swab",
            'choice_2': "Two blood swabs",
            'choice_3': "Bone fragments",
            'choice_4': "A suspected blood swab",
            'answer': 'choice_4'
        })
        q_a_bank.append({
            'question': "Where did you collect this swab?",
            'choice_1': "From an unknown stain on the shower wall.",
            'choice_2': "From an unknown stain in the sink basin.",
            'choice_3': "From an unknown stain under the toilet seat cover.",
            'choice_4': "From an unknown stain in the shower tub.",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "How did you confirm the stain was blood at the scene?",
            'choice_1': "I used a rapid DNA test kit.",
            'choice_2': "I used a presumptive blood test kit.",
            'choice_3': "I had not confirmed the stain was blood at the scene.",
            'choice_4': "I had conducted a sense test; it was red and smelled of iron.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What made you suspect the stain was blood?",
            'choice_1': "An unknown stain had not fluoresced under an IR alternate light source.",
            'choice_2': "An unknown stain at the scene had fluoresced under a UV alternate light source.",
            'choice_3': "An unknown stain at the scene had not fluoresced under a UV alternate light source.",
            'choice_4': "An unknown stain at the scene had fluoresced under a 510 alternate light source.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What technique did you use to check if the stain was likely blood?",
            'choice_1': "I used a Hemastix presumptive blood test on the stain. It had turned yellow, which indicates a positive result.",
            'choice_2': "I used a Luminol presumptive blood test on the stain. It glowed yellow, indicating a high likelihood that it could be blood.",
            'choice_3': "I used a Hemastix presumptive blood test on the stain. It had turned dark green, which indicates a positive result.",
            'choice_4': "I used a phenolphthalein presumptive blood test on the stain. It turned dark green, indicating a high likelihood that it could be blood.",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "In the lab, did you confirm an identification from the blood swab?",
            'choice_1': "Yes, I had confirmed a DNA profile match.",
            'choice_2': "No, but I had found a DNA profile with high consistency to the tested sample.",
            'choice_3': "No, I had not found a DNA profile with high consistency to the tested sample.",
            'choice_4': "No, I had not conducted a DNA test with the blood swab.",
            'answer': 'choice_2'
        })
        q_a_bank.append({
            'question': "How many potential bone fragments did you analyze?",
            'choice_1': "Six",
            'choice_2': "Five",
            'choice_3': "Three",
            'choice_4': "Seven",
            'answer': 'choice_1'
        })
        q_a_bank.append({
            'question': "How many were determined to be actual bone?",
            'choice_1': "Four",
            'choice_2': "Two",
            'choice_3': "Three",
            'choice_4': "All of them",
            'answer': 'choice_3'
        })
        q_a_bank.append({
            'question': "What techniques did you use to determine that number?",
            'choice_1': "Radiography and microscopy",
            'choice_2': "Radiography and odontology",
            'choice_3': "Odontology and microscopy",
            'choice_4': "Microscopy and odontolosis",
            'answer': 'choice_1'
        })
        
        q_a_bank.append({
            'question': "Final question. Are you, [name], 100 precent certain in the accuracy of your results from all your analyses?",
            'choice_1': "No, but it’s not like you know any better.",
            'choice_2': "Yes, because my techniques are trusted to be 100 precent accurate.",
            'choice_3': "No, but after several years of experience, my intuition is extremely refined.",
            'choice_4': "No, because science is theory-based and often works within probabilities, so there can never be an absolute certainty.",
            'answer': 'choice_4'
        })
   
        
    def reset_answers():
        global score 
        global user_answers
        score = 0
        user_answers = []

label start:
    # $slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for inventory
    # $slot_padding = 120 / 2
    # $distance_slot = slot_size[0] + slot_padding
    # $first_slot_x = 105 # inventory and toolbox
    # $first_slot_y = 300 # inventory and toolbox
    # $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    # $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    
    # # inventory
    # $inventory_SM = SpriteManager(event = inventoryEvents) # sprite manager that manages inventory items; triggers function inventoryUpdate 
    # $inventory_sprites = [] # holds all inventory sprite objects
    # $inventory_items = [] # holds inventory items
    # $inventory_db_enabled = False # determines whether down arrow on inventory hotbar is enabled or not
    # $inventory_ub_enabled = False # determines whether up arrow on inventory hotbar is enabled or not

    # # toolbox:
    # $toolbox_SM = SpriteManager(event = toolboxEvents)
    # $toolbox_sprites = []
    # $toolbox_items = []
    # $toolbox_db_enabled = False
    # $toolbox_ub_enabled = False

    # # toolbox popup:
    # $toolboxpop_SM = SpriteManager(event = toolboxPopupEvents)
    # $toolboxpop_sprites = []
    # $toolboxpop_items = []
    # $toolboxpop_db_enabled = False
    # $toolboxpop_ub_enabled = False

    # python:
    #     addToInventory(["knaap_footprint", "cheque_fingerprint", "bullet_casing_fingerprint", "blood_carpet"])

label enter:
    scene courtroom_bg
    python:
        # maybe: pixel_width: If not None, the input is limited to being this many pixels wide, in the font used by the input to display text.
        name = renpy.input("Please enter your first and last name")
        name = name.strip()
        if not name:
            name = "John Doe"
    # show screen full_inventory
    "[name], welcome to the courtroom!"
    "In this scene, you will give a testimony with regards to the evidence you've analyzed."
    # show screen arrow_screen
    # "Remember, you can click on the evidence button to remind you of your analysis results."
    # hide screen arrow_screen
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