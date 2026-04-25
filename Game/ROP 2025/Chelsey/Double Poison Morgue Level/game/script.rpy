# Characters 

define n = Character(name=("Nina"), image="nina")

define l = Character(name=("Vivienne"), image="vivienne")

# this adds an invisible icon to the corner, it's just so that the textbox icon shows up
image vivienne normal = "images/sprites/viv.png"

define d = Character("")

default default_mouse = "default"

default location = "external"
default global_label = "external"
default global_tool = "external"

# # game specifics
transform clipboard_slide_in:
    xalign 1.2   
    yalign 0.0
    alpha 0.0
    ease 0.25 xalign 0.5 alpha 1.0   # slide + fade in


init python:
    config.mouse = {
        "default": [("images/cursors/cursor.png", 10, 10)],
        "formalin": [("images/Toolbox Items/toolbox-formalin.png", 150, 0)],
        "tube": [("images/Toolbox Items/toolbox-heparin tube.png", 0, 0)],
        "syringe": [("images/Toolbox Items/toolbox-syringe.png", 150, 0)], 
        "scalpel": [("images/Toolbox Items/toolbox-scalpel.png", 150, 0)],
        "rib cutter": [("images/Toolbox Items/toolbox-rib_cutter.png", 150, 0)],
        "falcon tube": [("images/Toolbox Items/toolbox-falcon_tube.png", 150, 0)],
        "bone saw": [("images/Toolbox Items/toolbox-bone_saw.png", 150, 0)],
        "weight": [("images/Toolbox Items/toolbox-weight.png", 150, 0)]
        }


label start:
    $ score = 0

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
    $inventory_item_names = ["Heart blood", "Femoral blood", "Urine", "Images", "Camera", "Rib cutter", "Scalpel", "Syringe", "Falcon tube", "Weight", "Formalin"] # holds names for inspect pop-up text (Chelsey comment: i did not make this inventory system but the popup labels only work when you add them to this array ;-;)
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 110 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 175 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Forceps", "Bone saw", "Camera", "Clamps", "Rib cutter", "Scalpel", "Syringe", "Falcon tube", "Weight", "Formalin", "Photos"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_size = (100, 100)
    $toolbox_slot_padding = 125 / 2 # sets padding size between toolbox slots
    $toolbox_slot_padding = 69
    $toolbox_first_slot_x = 110 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 175 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    $toolboxpop_item_names = [] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (100, 100) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 69 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 406 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 445 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    $all_pieces = 0

    #################################### SET-UP SCENE LABEL #############################################

    # sets up environment items for first scene
    label setupScene1:

        # environment items to interact with in this scene - remember to put exact file name
        $environment_items = ["lid"]

        # python code block
        python:
            # iterate through environment items list
            for item in environment_items:
                idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
                hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
                t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
                environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
                environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
                environment_sprites[-1].idle_image = idle_image # sets idle image
                environment_sprites[-1].hover_image = hover_image # sets hover image


                # SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ------------------------------
            
                # for each item, make sure to set width/height to width and height of actual image
                if item == "lid":
                    environment_sprites[-1].width = 300 / 2
                    environment_sprites[-1].height = 231 / 2
                    environment_sprites[-1].x = 1000
                    environment_sprites[-1].y = 500

            # adding items to inventory/evidence box and toolbox

            addToInventory(["images"])

            addToToolboxPop(["camera", "rib_cutter", "scalpel", "weight"])
            addToToolbox(["camera", "rib_cutter", "scalpel", "syringe", "falcon_tube", 'weight', "formalin"])

            # Initialize camera module
            camera_config = CameraConfig()
            camera_config.font = "ConcertOne-Regular.ttf"

            camera_config.register_location("tattoo", "Tattoo")

            camera_state = CameraState()

        
    #################################### TRANSFORM #############################################

    # make sure to add this add the bottom of the setup labels to ensure that images are properly sized
    transform half_size:
        zoom 0.5


##################################################################################################
########################################## INTRODUCTION ##########################################

scene morgue

pause 0.5

d "Welcome to the morgue!"

d "Here comes Nina..."

show nina_normal with moveinbottom

n normal1 "Hey there! I'm Nina."

n normal1 "I'll start with the first step in a medicolegal autopsy: examining the case's History, Scene & Circumstances."

########################################## CASE HISTORY ##########################################

n normal2 "The decedent was found on the 10th floor of Robarts Library, inside an enclosed study room."

n normal2 "The body was discovered in a seated position, collapsed forward onto the desk. There were no signs of forced entry or disturbance within the room."

n normal3 "A partially consumed cup of coffee was located on the desk."

n normal1 "A pill bottle was recovered at the scene in the decedent's backpack and on their desk."

n normal2 "Witness statements indicate the individual had reported progressive fatigue and recent unexplained hair thinning over the preceding weeks."

n normal1 "The evidence raises concern for a possible toxic exposure, so we will need to conduct which ancillary test..."

########################################## QUIZ 1: ANCILLARY TEST ##########################################

label quiz1:
    menu:
        "Toxicology analysis":
            $ score += 1
            n normal2 "Correct. Toxicology is essential in suspected poisoning."
            jump toxicology_correct

        "Ballistics examination":
            n normal2 "Incorrect. There is no evidence of firearm involvement in this case."

        "Sexual assault examination":
            n normal2 "Incorrect. There are no indicators suggesting sexual violence."

        "Forensic entomology":
            n normal2 "Incorrect. The body was discovered shortly after death; insect activity is not relevant."

        "Forensic odontology":
            n normal2 "Incorrect. Dental identification is unnecessary as the decedent's identity is already confirmed."

label toxicology_retry:
    n normal1 "Please try again."
    jump quiz1

label toxicology_correct:

########################################## TRANSITION TO VIVIENNE ##########################################

n normal3 "After the case history examination, the next step in the process is to conduct an external examination."

show nina_normal at right

show vivienne at left with moveinleft

n normal2 "You'll be assisting Dr. Luk today for the rest of your examinations."

hide nina_normal

hide vivienne

########################################## CLOTHING EXAMINATION ##########################################

label clothing_exam_start:

    scene body_with_clothing

    l normal "Hi there, let's begin with the external examination."

    l normal "Start by checking for any items or belongings in the pockets."

    call screen clothing_body

    scene pill_closeup with fade

    l normal "We retrieved some pills from the pockets."

    l normal "These will be packaged and added to your inventory."

    scene body_with_clothing

    l normal "You now have access to the Post Mortem Report sheet in the top right corner."

    l normal "You can use it to review notes and track progress."

    l normal "Please record the items you found in the pockets."

    show screen viv_tip_clipboard

    call screen clipboard_icon

    hide screen viv_tip_clipboard

    l normal "The clipboard will be available for you throughout the procedure."

    show screen clipboard_icon

    l normal "After recording the clothing worn and pocket contents, we need to undress and wash the decedent."

########################################## EXTERNAL EXAMINATION & PHOTOGRAPHY ##########################################

label external_exam_start:

    scene body_base with fade

    l normal "Start by examining the body for any injuries and taking photos of them using the camera in your inventory."

    hide screen clipboard_icon

    show screen full_inventory

    call screen injuries_body

label finished_photography:

    show screen viv_screen

    scene body_base

    $ hide_all_inventory()

    if len(photos_taken_locations) > 0:
        l normal "You documented [len(photos_taken_locations)] area(s). Good work!"

    l normal "You can examine your photos in your evidence folder."

    $ location = "postphoto"

    l "Next, record the identifications and injuries that you discovered on the victim."

    show screen viv_tip_clipboard

    call screen clipboard_icon

    hide screen viv_tip_clipboard

    hide screen clipboard_icon

########################################## QUIZ 2: FLUID SAMPLES ##########################################

    $ location = "internal"
    $ store.current_photo_location = "internal"

    l normal "Before we start the internal examination, confirm the fluid samples that we need to collect from the decedent:"

label ext_exam_quiz:
    menu:
        "Blood sample and urine sample":
            $ score += 1
            l normal "Correct. Peripheral blood and urine are needed for the toxicology analysis."
            jump ext_exam_quiz_correct

        "Blood sample only":
            l normal "Not quite. Blood is needed for toxicology, but collecting it alone is insufficient."
            jump ext_exam_quiz_retry

        "Urine sample and vitreous humor":
            l normal "Not quite. While vitreous humor can assist with certain analyses, it does not replace peripheral blood in standard toxicology testing."
            jump ext_exam_quiz_retry

label ext_exam_quiz_retry:
    l normal "Please try again."
    jump ext_exam_quiz

label ext_exam_quiz_correct:

########################################## QUIZ 3: BLOOD SAMPLE LOCATIONS ##########################################

    l normal "Next, we need to take blood samples from which two areas?"

label blood_samp_quiz:
    menu:
        "From pooled blood at the scene":
            l normal "Incorrect. Scene blood may be contaminated and is unsuitable for proper toxicological sampling."
            jump blood_samp_quiz_retry

        "Heart and femoral area.":
            l normal "Correct."
            jump blood_samp_quiz_correct

        "From superficial arm veins only":
            l normal "Incorrect. Peripheral venous blood alone may be unreliable; both central and femoral samples are typically required."
            jump blood_samp_quiz_retry

label blood_samp_quiz_retry:
    l normal "Please try again."
    jump blood_samp_quiz

label blood_samp_quiz_correct:

    $ location = "internal"

########################################## INTERNAL EXAMINATION ##########################################

label internal_exam_start:

    scene internal_examination_base with fade

    l normal "We are ready to start the internal dissection."

    l normal "Please pass me the appropriate tools for each step."

    ## -- Y-Incision --

    l normal "First, we need to do a Y-incision."

    show screen full_inventory

    call screen viv_check("scalpel_given", "scalpel")

label scalpel_given:
    $ default_mouse = "default"
    l normal "Correct."

    scene internal_examination_y with fade
    pause 1
    scene internal_examination_ribs with fade

    ## -- Rib Removal --

    l normal "Next, we need to remove the ribs."

    show screen full_inventory

    call screen viv_check("rib_cutters_given", "rib cutter")

label rib_cutters_given:
    $ default_mouse = "default"
    l normal "Correct."

    scene internal_examination_organs with fade

########################################## MODIFIED GHON TECHNIQUE ##########################################

label ghon_start:

    l normal "Now that the Y-incision is completed, we will be using the Modified Ghon technique to remove the decedent's organs in three blocks."

    l normal "First is the Neck Block. Second is the Thoracic Block. The third is the Abdominal Block."

    ## -- Neck Block --

    l normal "Pass me the scalpel to dissect the neck block from the floor of the mouth downward."

    show screen full_inventory

    call screen viv_check("neck_block_removed", "scalpel")

label neck_block_removed:

    scene neck_remove1 with fade
    pause 1
    scene neck_remove2 with fade
    pause 1
    scene neck_remove3 with fade

    l normal "The neck organs have now been individually dissected."

label weighed_neck:

    ## -- Thoracic Block --

    scene internal_examination_organs with fade

    l normal "Let's remove the chest block next. Pass me the scalpel again."

    l normal "This is also where we will collect the heart blood."

    show screen full_inventory

    call screen viv_check("chest_block_removed", "scalpel")

label chest_block_removed:

    scene internal_examination_chest with fade

    ## -- Heart Blood Collection --

    l normal "Now, we need to collect blood from the heart."

    scene heart1 with fade
    pause 1

    l normal "We need to cut the pericardial sac to reach the blood. Pass me a scalpel for this."

    show screen full_inventory

    call screen viv_check("heart_cut", "scalpel")

label heart_cut:

    scene heart2 with fade

    l normal "Next, pass me the syringe."

    show screen full_inventory

    call screen viv_check("heart_blood_collection", "syringe")

label heart_blood_collection:

    scene heart3
    pause 0.7
    scene heart4
    pause 0.7
    scene heart5

    l normal "To store the blood, pass me a falcon tube."

    show screen full_inventory

    call screen viv_check("heart_blood_store", "falcon tube")

label heart_blood_store:

    scene heart6 with fade
    pause 0.7
    scene heart7
    pause 0.7
    scene heart8

    l normal "Now we will label and seal the sample."

    scene heart9
    pause 0.7
    scene heart10
    pause 0.7
    scene heart11 with fade

    l normal "This will be added to your inventory."

    $ addToInventory(["heart_blood"])

    ## -- Abdominal Block --

    scene internal_examination_chest with fade

    l normal "Let's continue with the Abdominal Block."

    l normal "Before we remove all the organs, we need to remove the large and small intestine to reach the bladder for urine sampling."

    l normal "Pass me a scalpel."

    show screen full_inventory

    call screen viv_check("intestine_removed", "scalpel")

label intestine_removed:

    scene intestine_removed with fade

    ## -- Urine Collection --

    l normal "Next, we need a syringe for the urine."

    show screen full_inventory

    call screen viv_check("urine_collect", "syringe")

label urine_collect:

    scene urine1
    pause 0.7
    scene urine2
    pause 0.7
    scene urine3
    pause 0.7

    l normal "Please pass me a falcon tube."

    show screen full_inventory

    call screen viv_check("urine_store", "falcon tube")

label urine_store:

    scene urine4 with fade
    pause 0.7
    scene urine5
    pause 0.7
    scene urine6
    pause 0.7
    scene urine7

    l normal "Now we will label and seal the sample."

    scene urine8
    pause 0.7
    scene urine9 with fade

    l normal "This will be added to your inventory."

    $ addToInventory(["urine"])

    scene intestine_removed with fade

    l normal "Next, let's remove the rest of the abdominal block."

    l normal "Please pass me a scalpel."

    show screen full_inventory

    call screen viv_check("all_organs_removed", "scalpel")

label all_organs_removed:

    ## -- Femoral Blood Collection --

    scene internal_examination_empty with fade

    l normal "Next, we will be collecting the femoral blood which is accessible now."

    l normal "Pass me the syringe to take the blood sample."

    show screen full_inventory

    call screen viv_check("syringe_femoral", "syringe")

label syringe_femoral:

    pause 0.3
    scene femur1 with fade
    pause 0.5
    scene femur2
    pause 0.5
    scene femur3
    pause 1

    l normal "Next, pass me a 15ml falcon tube."

    show screen full_inventory

    call screen viv_check("tube_femoral", "falcon tube")

label tube_femoral:

    pause 0.3
    scene femur4 with fade
    pause 0.5
    scene femur5
    pause 0.5
    scene femur6
    pause 1
    scene femur7

    l normal "Finally, we will label and seal the bottle."

    scene femur8
    pause 0.7
    scene femur9
    pause 0.7

    l normal "The bottle will be added to your evidence inventory."

    $ addToInventory(["femoral_blood"])

########################################## ORGAN WEIGHING & SAMPLING ##########################################

label weighing:

    scene internal_examination_empty

    l normal "Finally, we will be weighing and sampling the heart, lung, liver, and kidneys."

    scene tray_organs with fade

    l normal "First, please bring over the weight."

    show screen full_inventory

    call screen viv_check("sampling", "weight")

    l normal "Great! All organs have been weighed."

label sampling:

    ## -- Tissue Sampling --

    l normal "Next, pass me the correct tool for taking small samples of the organ tissue."

    show screen full_inventory

    call screen viv_check("sample_organs", "scalpel")

label sample_organs:
    $ default_mouse = "default"
    scene tray_samples with fade

    l normal "Now that we have all the samples, select the correct container."

    call screen container_choice

label sampling_complete:

    l normal "Correct."

    scene organ_bottle1 with fade

    l normal "Next, pass me formalin, which is used for preservation purposes."

    show screen full_inventory

    call screen viv_check("jar_label", "formalin")

label jar_label:

    l normal "Lastly, we need to label the jar."

    scene organ_bottle2 with fade
    pause 1
    scene organ_bottle3
    pause 2

########################################## CONCLUSION ##########################################

    scene internal_examination_empty

    l normal "Great work! These samples will be sent to the lab where you will conduct further tests."

    hide screen viv_screen

    scene morgue

    show nina_normal with moveinbottom

    n normal1 "Great job! We will see you in the labs!"

    $ MainMenu(confirm=False)()