default show_evidence = False

default q_a_bank = []
default score = 0
define s = "Supervisor"
define d = "Defense"
define j = "Judge"

transform t_judge:
    zoom 1.7
    xanchor 0.5
    yanchor 0.5
    xpos 0.5
    ypos 0.55

init python:
    from typing import List


    def check_answer(correct_answer, choice):
        global score
        if correct_answer == choice:
            score += 1
    
    def say_responses(responses: List[str]) -> None:
        for p in range(len(responses)):
            renpy.say(None, responses[p])

    def load_q_a():
        global q_a_bank
        # q_1
        q_a_bank.append({
            'question': "You identified a small pool of blood at the crime scene. How did you determine that the sample was indeed blood, considering several typed of liquids were present at the party?",
            'choice_1': "By running a Kastle-Meyer test",
            "choice_1_responses": ["The kastle-meyer test is a presumptive test for blood that turns pink in the presence of hemoglobin."],
            'choice_2': "By using luminol",
            "choice_2_responses": ["While Luminol does glow blue in the presence of blood, the Kastle-Meyer test is more specific to blood. However, Luminol is great for detecting trace amount of blood!"],
            'choice_3': "By performing a pH test",
            "choice_3_responses": ["A pH test cannot differentiate blood from other substances. A kastle-meyer test is the correct option!"],
            "choice_4": "Usually, red liquids at a scene of a murder are blood.",
            "choice_4_responses": ["While this can be an easy assumption to make, there are many liquids that can look like blood (most notably, ketchup!). The correct option is a Kastle-Meyer test."],
            'answer': 'choice_1'
        })

        # q_2
        q_a_bank.append({
            'question': "How did you determine the source of this blood, and what were the conclusions drawn from this?",
            'choice_1': "The Kastle-Meyer Test is also able to determine the source of the blood. The blood was from Alex Deere, who was injured at the scene",
            "choice_1_responses": [],
            'choice_2': "We performed DNA analysis on the blood sample, which matched the DNA of Alex Deere",
            "choice_2_responses": [],
            'choice_3': "The blood was identified through a simple blood type test, showing it was from an unknown person.",
            "choice_3_responses": [],
            "choice_4": "The blood pattern analysis indicated it was from the assailant during a physical struggle with the victim.",
            "choice_4_responses": [],
            'answer': 'choice_2'
        })

        # q_3
        q_a_bank.append({
            'question': "What process did you use to identify the fingerprint found on the label of the alcohol bottle, and what did this result yield?",
            'choice_1': "I used the DFO method to enhance the fingerprint. The print was then run through AFIS and was consistent to Doorag Deelar, linking him to the crime scene.",
            "choice_1_responses": [],
            'choice_2': "I dusted the bottle with fingerprint powder. The results were photographed and they matched the fingerprints of Mr. Doorag Dealer.",
            "choice_2_responses": [],
            'choice_3': "I used the DFO method to enhance the fingerprint, but the print was too smudged to be useful, so we couldn't identify the individual.",
            "choice_3_responses": [],
            "choice_4": "The fingerprint was lifted using cyanoacrylate fuming. When the print was enhanced and photographed, we determined that it was consistent with an unknown individual.",
            "choice_4_responses": [],
            'answer': "choice_1"
        })

        # q_4
        q_a_bank.append({
            'question': "During your investigation, you chose to use the DFO process on the alcohol bottle label. How does it work, and why was DFO the preferred method over other fingerprint development techniques?",
            'choice_1': "it reacts with amino acids in the fingerprint residue, making prints visible under specific lighting, particularly on porous surfaces like paper.",
            "choice_1_responses": [],
            'choice_2': "it works well on all surfaces, especially glass and metal.",
            "choice_2_responses": [],
            'choice_3': "it reacts with oils in fingerprints, making them visible to the naked eye.",
            "choice_3_responses": [],
            "choice_4": "it provides instant results without the need for additional equipment.",
            "choice_4_responses": [],
            'answer': "choice_1"
        })

        # q_5
        q_a_bank.append({
            'question': "During your investigation, a smudged handprint was found on the door at the crime scene. Why was this handprint not utilized as a key piece of evidence?",
            'choice_1': "The handprint was too small to belong to any adult and was deemed irrelevant.",
            "choice_1_responses": [],
            'choice_2': "The handprint was not used because it was determined to belong to the victim.",
            "choice_2_responses": [],
            'choice_3': "The handprint was too smudged to provide sufficient ridge detail, making it impossible to identify the individual.",
            "choice_3_responses": [],
            "choice_4": "The handprint was ignored because it was found in a low-traffic area of the crime scene.",
            "choice_4_responses": [],
            'answer': "choice_3"
        })

        # q_6
        q_a_bank.append({
            'question': "While collecting the blood sample at the crime scene, what precautions did you take to ensure that the DNA evidence was not contaminated?",
            'choice_1': "We avoided contamination by collecting the sample with bare hands to avoid introducing foreign substances from gloves.",
            "choice_1_responses": [],
            'choice_2': "The sample was collected after the area was wiped clean to ensure only the freshest sample was taken.",
            "choice_2_responses": [],
            'choice_3': "The sample was collected immediately to prevent exposure to the elements. This ensured that the sample had the greatest integrity.",
            "choice_3_responses": [],
            "choice_4": "We used sterile gloves and tools, collected the sample in a sterile container, and ensured the area was free of any potential contaminants before collection.",
            "choice_4_responses": [],
            'answer': "choice_4"
        })

        # q_7
        q_a_bank.append({
            'question': "When collecting the bloody footprint at the scene, what steps did you take to preserve the evidence for further analysis?",
            'choice_1': "We collected the footprint by pouring dental stone over it to create a 2D cast of the impression. This ensures that the detail is not lost as the blood degrades.",
            "choice_1_responses": [],
            'choice_2': "After enhancing the footprint with hungarian red, It was collected and preserved by covering it with plastic wrap to protect it from contamination.",
            "choice_2_responses": [],
            'choice_3': "After enhancing the footprint with hungarian red, we photographed the footprint, carefully lifted it using a gel lifter, and stored it in a protected environment to prevent any degradation.",
            "choice_3_responses": [],
            "choice_4": "In order to preserve the integrity of the footprint, the entire area of flooring was lifted from the scene and taken to the lab for analysis. This ensured any photos taken had the best lighting section.",
            "choice_4_responses": [],
            'answer': "choice_3"
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
    $inventory_item_names = ["Fingerprint", "Handprint", "Gin", "Splatter", "Footprint"] # holds names for inspect pop-up text 
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
        addToInventory(["fingerprint", "handprint", "gin", "splatter", "footprint"])

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
    scene lobby
    show ema glasses as character
    $ preferences.text_cps = 50
    s "Hey! Welcome to the final step of your journey!"
    show ema normal as character
    s "You've done great so far, but this is your final test — the courtroom." 
    s "All the evidence you’ve gathered, the clues you’ve pieced together, it’s time to present your case."
    show ema serious as character
    s "Just a heads-up: the defense attorney you’re up against is no pushover. {w=0.25}They’re sharp, relentless, and will do everything in their power to poke holes in your case."
    s "So, stay sharp, think on your feet, and remember everything you’ve uncovered during your investigation."
    show ema shocked as character
    "???" "Did I hear someone mention my name?{w=1}{nw}"
    window hide
    show kristoph smile as character
    with Dissolve(1.5)
    pause 2
    show ema annoyed as character
    s "Um...{w=0.25} technically speaking I didn't say your name."
    show kristoph smile as character
    d "...{w=0.25}So you're the new officer they hired."
    show ema annoyed as character
    s "Did I just get ignored...?"
    show kristoph smile as character
    d "It's a pleasure to meet you. I look forward to seeing you in there."
    d "Don't stress yourself out too much. This will be a quick case to resolve."
    show kristoph confident as character
    d "It'll be over before you know it."
    show ema serious as character
    s "{fast}For you, that is!{fast}"
    show ema annoyed as character
    s "Ugh!{w=0.1} That guy is so full of it!"
    s "Let's put him in his place!"
    "Attention. The case of the People v. Doorag Deelar will be in session in approximately 5 minutes."
    "All those participating should report to Courtroom #15 immediately."
    show ema serious as character
    s "That's you."
    show ema normal as character
    s "Good luck. The truth is on your side — let's hope you can prove it."
    scene judge bench
    show judge normal as character at t_judge
    j "Let us begin."
    j "Do you,{w=0.25} swear that you will,{w=0.25} according to the best of your skill and knowledge"
    j "truly and faithfully and without partiality to any of the parties to this proceeding"
    j "take the evidence of every witness examined under this commission"
    menu:
        j "and cause the evidence to be transcribed and forwarded to the Court?"
        "I do.":
            jump start_questions
        "I do not.":
            jump ask_again
            
label ask_again:
    show judge stern as character at t_judge
    j "...You do understand that a refusal to testify means you will be held under contempt of court, correct?"
    menu:
        j "Are you sure about your answer?"
        "Yes.":
            jump quick_end
        "No.":
            "I'm sorry, Your Honour. I wasn't in the right headspace."
            "I'm just a bit nervous. It's my first time testifying in court."
            show judge ponder as character at t_judge
            j "Right, your supervisor informed me that this is your first time on the witness stand."
            show judge normal as character at t_judge
            j "I'll look the other way today, but do your best not to make such a mistake in future proceedings."
            "I understand, Your Honour."
            jump start_questions

label start_questions:
    scene judge bench
    show judge normal as character at t_judge
    python:
        for q_a in q_a_bank:
            global responses
            renpy.call_screen("question_screen", q_a=q_a)
            # say_responses(responses = q_a[responses])

        if score > 4:
            renpy.jump("good_ending")
        else:
            renpy.jump("bad_ending")

label good_ending:
    scene judge bench
    show judge normal as character at t_judge
    j "I believe I've heard quite enough."
    j "Mr. Doorag Deelar, you have, without a shadow of doubt, murdered the victim, Davis Dayid."
    show judge stern as character at t_judge
    j "I see no reason to continue further."
    j "You will be charged with second degree murder."
    j "This court is adjourned."
    scene lobby
    with Dissolve(1.5)
    show ema normal as character
    s "You did it! I knew I could count on you!"
    s "Are you sure you're not already a pro at this?"
    show kristoph glasses as character
    with Dissolve(1.0)
    d "..."
    show ema glasses as character
    s "Ha, what do you have to say to that?"
    show kristoph smile as character
    d "I'll say... {w=0.5}that was a stroke of beginner's luck."
    d "It seems I took this new recruit too lightly."
    show kristoph confident as character
    d "I do look forward to crushing you in the battlefield next time."
    hide kristoph confident
    show ema annoyed as character
    s "Um... overdramatic much? What a sore loser."
    show ema glasses as character
    s "Well - forget about him! This calls for celebration! Drinks are on me!"
    show ema normal as character
    s "We'll toast to your commendable performance today!"
    s "I can't wait to see what you bring to the future."
    jump end

label bad_ending:
    scene judge bench
    show judge normal as character at t_judge
    j "I believe I've heard quite enough."
    j "There remains some doubt as to whether the defendant has murdered Davis Dayid."
    show judge stern as character at t_judge
    j "However, Mr. Doorag Deelar, there is sufficient evidence that shows that you assaulted Alex Deere - and you will be charged for that."
    j "That is all. Court is adjourned."
    scene lobby
    with Dissolve(1.5)
    show ema serious as character
    s "It's unfortunate that he was only charged for assault... after all, we both know he murdered Davis."
    show ema normal as character
    s "But for your first time - I'm proud of you! You held up well against the defense."
    show kristoph smile as character
    with Dissolve(1.5)
    d "Indeed... it is quite unfortunate that I could not clear my client of all charges."
    show ema annoyed as character
    s "No one asked..."
    show kristoph smile as character
    d "You lasted longer than I had expected. You put up a good fight."
    d "Although, it's only natural that this was the only outcome."
    d "Perhaps I will see you again in the courtroom."
    d "Good day."
    show ema annoyed as character
    s "This guy is insufferable!"
    s "Next time, we'll show him!"
    show ema normal as character
    s "But for now, give yourself a pat on the back. You did a great job!"
    s "Go get some rest. I'll see you next time!"
    jump end

label end:
    call screen score_screen
    if _return == 'retry':
        jump start_questions

label quick_end:
    j "I'm afraid we simply cannot continue then."
    j "You will be put under direct civil contempt of court for disrupting proceedings."
    j "Court is adjourned."
    scene lobby
    "5 minutes later..."
    show kristoph confident as character
    d "Hah! How laughable."
    show ema serious as character
    s "What the heck was that?!"
    s "Have you lost your mind?!"
    s "This is ridiculous... You're fired!"
    return

# make sure to add this add the bottom of the setup labels to ensure that images are properly sized
transform half_size:
    zoom 0.5

return
