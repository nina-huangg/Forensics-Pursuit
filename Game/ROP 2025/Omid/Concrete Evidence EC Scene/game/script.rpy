define s = Character('Steve')
image scene1_selected = "images/scene1_selected.png"
image scene2_selected = "images/scene2_selected.png"
image scene3_selected = "images/scene3_selected.png"
image scene1 = "images/scene1.png"
image scene2 = "images/scene2.png"
image scene3 = "images/scene3.png"
image scene3_knife = "images/scene3_knife.png"
image scene3_knife_selected = "images/scene3_knife_selected.png"
image scene2_knife = "images/scene2_knife.png"
image scene2_knife_selected = "images/scene2_knife_selected.png"


init python:
    config.mouse = {
        "default": [("images/cursor.png", 0, 0)],
        "swab": [("images/cursor_swab.png", 0, 0)],
        "hungarian_red": [("images/cursor_hungarian_red.png", 0, 0)]
    }
    global default_mouse
    default_mouse = "default"

    scene1_collected_count = 0
    scene1_total_evidence = 2 + 1
    scene2_collected_count = 0
    scene2_total_evidence = 5 + 1
    scene3_collected_count = 0
    scene3_total_evidence = 4 + 1
    # Track FARO scan completion
    faro_scanned_scene1 = False
    faro_scanned_scene2 = False
    faro_scanned_scene3 = False
    # Track current scene for FARO scan menu logic
    current_scene = None

transform zoom_out:
    size (config.screen_width, config.screen_height)
    fit "fill"
transform zoom_in:
    zoom 1.15
transform bottom_right:
    xalign 1.0
    yalign 1.0
    zoom 0.85
transform invis:
    alpha 0.01
transform half_size:
    zoom 0.5

label start:
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
    $inventory_item_names = ["Tape on acetate", "Tapeglo in bag", "Tape photo", "Duct tape tapeglo", "Distilled water", "Tape in tweezers", "Duct tape", "Tapeglo", 
    "Fingerprint on card", "Backing card","Scalebar", "Lifting tape", "Jar photo", "Lid in tweezers", "Camel brush", "Lid with soot", "Lid", "Camphor smoke", "Lighter", 
    "Tweezers", "Gloves box", "Evidence bag", "Jar in bag", "Tape in bag", "Pvs in bag",
    "Bloody kitchen knife"
    
    
    ] # holds names for inspect pop-up text 
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
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    # $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_size = (100, 100)
    # $toolbox_slot_padding = 125 / 2 # sets padding size between toolbox slots
    $toolbox_slot_padding = 69
    $toolbox_first_slot_x = 110 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 175 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (100, 100) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 69 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 406 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 445 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    # $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    $all_pieces = 0

    ########## INVENTORY DONE ##########


    #### INVNETORY ENV VARIABLES ####
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
            if item == "clean_swab":
                environment_sprites[-1].type = "pop_item"
                environment_sprites[-1].width = 300 / 2
                environment_sprites[-1].height = 231 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 500

        # adding items to inventory/evidence box and toolbox

        # addToInventory(["evidence_bag"])
        addToToolbox(["clean_swab"])
        addToToolbox(["hungarian_red"])
        addToToolbox(["faro3d"])
        # addToToolboxPop(["clean_swab"])
        ### END OF INVENTORY ENV VARIABLES ####
    jump begin


label begin:
    hide screen revisit_walkthrough_button
    hide screen scene1_selection
    hide screen scene2_selection
    hide screen scene3_selection
    hide screen evidence_counter_screen
    hide screen evidence_counter_screen_scene2
    hide screen evidence_counter_screen_scene3
    hide screen toolbox
    hide screen inventory
    hide screen inv_buttons
    hide screen close_inv
    hide screen full_inventory

    scene opening at zoom_in
    show steve at bottom_right

    s "Glad you’re here. Here’s the breakdown: Two individuals. Male, 19, and Female, 25. Both with serious knife wounds, but alive, and both claim the other struck first." 
    s "CCTV is useless. The lens was dirty, and a support beam blocked the angle. We’ve got two knives, bloodied clothes, and multiple blood trails. No eyewitnesses."

    s "Let's walk through the scene."
    hide steve
    scene scene1 at zoom_out
    show steve at bottom_right
    s "Here's the initial scene of attack. Let's call this scene 1. Looks like there's a pool of blood and some drag marks."
    hide steve
    scene scene2 at zoom_out
    show scene2_knife at zoom_out
    show steve at bottom_right
    s "To the left is scene 2. More blood, and one of the potential weapons, a knife."
    s "There's a lot of blood here. You'll probably have to use multiple swabs for this."
    hide steve
    scene scene3 at zoom_out
    show scene3_knife at zoom_out
    show steve at bottom_right
    s "And further left, scene 3. A bloody handprint on the wall, drag marks, and another knife."
    s "Now it's your turn. Get to it. Oh- and one more thing: Don't forget that hungarian red destroys DNA."

    jump overview

screen revisit_walkthrough_button:
    textbutton "Revisit Walkthrough":
        xpos 0.19
        ypos 0.2
        xanchor 0.5
        action [Jump("begin")]

screen scene1_selection:
    imagebutton:
        idle At("scene1_selected", invis)
        hover "scene1_selected"
        focus_mask True
        action Jump("scene1_action")
        hovered Show("evidence_counter_screen")
        unhovered Hide("evidence_counter_screen")

screen scene2_selection:
    imagebutton:
        idle At("scene2_selected", invis)
        hover "scene2_selected"
        focus_mask True
        action Jump("scene2_action")
        hovered Show("evidence_counter_screen_scene2")
        unhovered Hide("evidence_counter_screen_scene2")

screen scene3_selection:
    imagebutton:
        idle At("scene3_selected", invis)
        hover "scene3_selected"
        focus_mask True
        action Jump("scene3_action")
        hovered Show("evidence_counter_screen_scene3")
        unhovered Hide("evidence_counter_screen_scene3")

label overview:
    $ default_mouse = "default"

    if scene1_collected_count == scene1_total_evidence and scene2_collected_count == scene2_total_evidence and scene3_collected_count == scene3_total_evidence:
        hide screen scene1_selection
        hide screen scene2_selection
        hide screen scene3_selection
        hide screen revisit_walkthrough_button
        window show
        show steve at bottom_right
        s "Congratulations! You've collected all the evidence from the crime scene."
        s "Let's head back to the lab to analyze what you've found."
        s "(This means close this game and start the lab scene)"
        hide steve
        pause

    hide screen toolbox
    hide screen inventory
    hide screen inv_buttons
    hide screen close_inv
    show screen full_inventory
    window hide
    show overview
    show screen scene1_selection
    show screen scene2_selection
    show screen scene3_selection
    show screen revisit_walkthrough_button
    pause
    jump overview


screen evidence_counter_screen:
    text "Evidence collected: [scene1_collected_count] / [scene1_total_evidence]" xpos 1260 ypos 105 xanchor 0.5 yanchor 0.5

screen evidence_counter_screen_scene2:
    text "Evidence collected: [scene2_collected_count] / [scene2_total_evidence]" xpos 410 ypos 480 xanchor 0.5 yanchor 0.5

screen evidence_counter_screen_scene3:
    text "Evidence collected: [scene3_collected_count] / [scene3_total_evidence]" xpos 1260 ypos 615 xanchor 0.5 yanchor 0.5

screen scene1:
    add "scene1" at zoom_out

    if default_mouse == "swab":
        # blood swab 1
        if "blood_swab_1_scene1" not in inventory_items:
            imagebutton:
                idle Null(711, 169)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(711, 169))
                xpos 14
                ypos 636
                action Jump("swab_blood_1_scene1")
        
        # blood swab 2
        if "blood_swab_2_scene1" not in inventory_items:
            imagebutton:
                idle Null(407, 249)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(467, 249))
                xpos 758
                ypos 482
                action Jump("swab_blood_2_scene1")

    textbutton "Return to Overview":
        xpos 0.5
        ypos 0.1
        xanchor 0.5
        yanchor 0.5
        background Frame("#0008", 10, 10)  # semi-transparent black with padding
        action Jump("overview")

screen scene2:
    add "scene2" at zoom_out

    if default_mouse == "swab":
        # blood swab 1
        if "blood_swab_1_scene2" not in inventory_items:
            imagebutton:
                idle Null(492, 326)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(532, 386))
                xpos 614
                ypos 401
                action Jump("swab_blood_1_scene2")
        
        # blood swab 2
        if "blood_swab_2_scene2" not in inventory_items:
            imagebutton:
                idle Null(573, 556)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(623, 556))
                xpos 7
                ypos 600
                action Jump("swab_blood_2_scene2")

        # blood swab 3
        if "blood_swab_3_scene2" not in inventory_items:
            imagebutton:
                idle Null(911, 386)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(911, 386))
                xpos 1089
                ypos 714
                action Jump("swab_blood_3_scene2")
    
    if default_mouse == "hungarian_red":
        # Footprints and drag marks area for hungarian red
        if "footprints_hungarian_red_scene2" not in inventory_items:
            imagebutton:
                idle Null(573, 556)
                hover Transform(Frame(Solid("#ff000030"), 5, 5), size=(623, 556))
                xpos 7
                ypos 600
                action Jump("hungarian_red_footprints_scene2")

    # Knife interaction
    if "bloody_default_knife" not in inventory_items:
        imagebutton at zoom_out:
            idle "scene2_knife"
            hover "scene2_knife_selected"
            action Return("knife_clicked")  # Return a value for knife interaction
            focus_mask True
    
    textbutton "Return to Overview":
        xpos 0.5
        ypos 0.1
        xanchor 0.5
        yanchor 0.5
        background Frame("#0008", 10, 10)  # semi-transparent black with padding
        action Jump("overview")

screen scene3:
    
    add "scene3" at zoom_out
    
    if default_mouse == "swab":
        # Handprint area
        if "handprint_blood_swab_scene3" not in inventory_items:
            imagebutton:
                idle Null(95, 239)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(95, 239))  # Force same size as idle
                xpos 950
                ypos 250
                action Jump("swab_blood_hand_scene3")
        
        # Footprints and drag marks area
        if "drag_mark_blood_swab_scene3" not in inventory_items:
            imagebutton:
                idle Null(900, 268)
                hover Transform(Frame(Solid("#ffffff30"), 5, 5), size=(900, 268))  # Force same size as idle
                xpos 940
                ypos 775
                action Jump("swab_blood_drag_scene3")

    if default_mouse == "hungarian_red":
        # Footprints and drag marks area for hungarian red
        if "drag_mark_hungarian_red_scene3" not in inventory_items:
            imagebutton:
                idle Null(900, 268)
                hover Transform(Frame(Solid("#ff000030"), 5, 5), size=(900, 268))  # Red tint for hungarian red
                xpos 940
                ypos 775
                action Jump("hungarian_red_drag_marks_scene3")
    
    # Knife interaction
    if "bloody_kitchen_knife" not in inventory_items:
        imagebutton at zoom_out:
            idle "scene3_knife"
            hover "scene3_knife_selected"
            action Return("knife_clicked")  # Return a value for knife interaction
            focus_mask True
    
    textbutton "Return to Overview":
        xpos 0.5
        ypos 0.1
        xanchor 0.5
        yanchor 0.5
        background Frame("#0008", 10, 10)  # semi-transparent black with padding
        action Jump("overview")


label swab_blood_hand_scene3:
    $ addToInventory(["handprint_blood_swab_scene3"])
    $ scene3_collected_count += 1
    $ default_mouse = "default"
    "You swabbed the bloody handprint on the wall."
    "The sample could contain DNA and blood type information from the perpetrator."
    call screen scene3

label swab_blood_drag_scene3:
    $ addToInventory(["drag_mark_blood_swab_scene3"])
    $ scene3_collected_count += 1
    $ default_mouse = "default"
    "You collected blood samples from the drag marks and footprints."
    "These samples might help determine the sequence of events and identify the individuals involved."
    call screen scene3

label hungarian_red_drag_marks_scene3:
    if "drag_mark_hungarian_red_scene3" in inventory_items:
        $ default_mouse = "default"
        s "You've already used Hungarian Red here."
        call screen scene3
    elif "drag_mark_blood_swab_scene3" in inventory_items:
        $ addToInventory(["drag_mark_hungarian_red_scene3"])
        $ scene3_collected_count += 1
        $ default_mouse = "default"
        "You used Hungarian Red on the drag marks."
        "The area glows, revealing more details about the struggle."
        call screen scene3
    else:
        s "You need to collect the blood sample first before using Hungarian Red."
        $ default_mouse = "default"
        call screen scene3

label hungarian_red_footprints_scene2:
    if "footprints_hungarian_red_scene2" in inventory_items:
        $ default_mouse = "default"
        s "You've already used Hungarian Red here."
        call screen scene2
    elif "blood_swab_2_scene2" in inventory_items:
        $ addToInventory(["footprints_hungarian_red_scene2"])
        $ scene2_collected_count += 1
        $ default_mouse = "default"
        "You used Hungarian Red on the footprints."
        "The area glows, revealing more details about the struggle."
        call screen scene2
    else:
        s "You need to collect the blood sample first before using Hungarian Red."
        $ default_mouse = "default"
        call screen scene2

label swab_blood_1_scene1:
    $ addToInventory(["blood_swab_1_scene1"])
    $ scene1_collected_count += 1
    $ default_mouse = "default"
    "You collected a blood sample."
    call screen scene1

label swab_blood_2_scene1:
    $ addToInventory(["blood_swab_2_scene1"])
    $ scene1_collected_count += 1
    $ default_mouse = "default"
    "You collected another blood sample."
    call screen scene1

label swab_blood_1_scene2:
    $ addToInventory(["blood_swab_1_scene2"]) # pool
    $ scene2_collected_count += 1
    $ default_mouse = "default"
    "You collected a blood sample."
    call screen scene2

label swab_blood_2_scene2:
    $ addToInventory(["blood_swab_2_scene2"]) # footsteps
    $ scene2_collected_count += 1
    $ default_mouse = "default"
    "You collected another blood sample."
    call screen scene2

label swab_blood_3_scene2:
    $ addToInventory(["blood_swab_3_scene2"]) # drag marks
    $ scene2_collected_count += 1
    $ default_mouse = "default"
    "You collected a third blood sample."
    call screen scene2



label scene1_action:
    $ current_scene = "scene1"
    show screen full_inventory
    hide screen scene1_selection
    hide screen scene2_selection
    hide screen scene3_selection
    
    call screen scene1
    $ current_scene = None
    jump overview

label scene2_action:
    $ current_scene = "scene2"
    show screen full_inventory
    hide screen scene1_selection
    hide screen scene2_selection
    hide screen scene3_selection
    $ result = renpy.call_screen("scene2")
    
    if result == "knife_clicked":
        jump knife_choice_menu_scene2
    $ current_scene = None
    jump overview

label scene3_action:
    $ current_scene = "scene3"
    show screen full_inventory
    hide screen scene1_selection
    hide screen scene2_selection
    hide screen scene3_selection
    $ result = renpy.call_screen("scene3")
    
    if result == "knife_clicked":
        jump knife_choice_menu
    $ current_scene = None
    jump overview

label clean_swab:
    $ default_mouse = "images/Toolbox Items/tooltip-clean_swab.png"

label hungarian_red:
    $ default_mouse = "hungarian_red"

label knife_choice_menu:
    $ scene3_collected_count += 1
    "You found a bloody kitchen knife. How should you collect it?"
    menu:
        "Place it in a bag":
            jump knife_in_bag
        "Place it in a box":
            jump knife_in_box

    call screen scene3

label knife_in_box:
    $ addToInventory(["bloody_kitchen_knife"])
    "You carefully placed the bloody kitchen knife in a box."
    "Good choice! Using a box helps preserve the evidence properly."
    "The knife has been added to your inventory."
    call screen scene3

label knife_in_bag:
    $ addToInventory(["bloody_kitchen_knife"])
    "You placed the bloody knife in a bag."
    "This was the wrong choice! You should have used a box to preserve the evidence properly."
    "The knife has been added to your inventory, but you may have compromised the evidence."
    call screen scene3

label knife_choice_menu_scene2:
    $ scene2_collected_count += 1
    "You found a bloody knife. How should you collect it?"
    menu:
        "Place it in a bag":
            jump knife_in_bag_scene2
        "Place it in a box":
            jump knife_in_box_scene2

label knife_in_bag_scene2:
    $ addToInventory(["bloody_default_knife"])
    "You placed the bloody knife in a bag."
    "This was the wrong choice! You should have used a box to preserve the evidence properly."
    "The knife has been added to your inventory, but you may have compromised the evidence."
    call screen scene2

label knife_in_box_scene2:
    $ addToInventory(["bloody_default_knife"])
    "You carefully placed the bloody knife in a box."
    "Good choice! Using a box helps preserve the evidence properly."
    "The knife has been added to your inventory."
    call screen scene2

init python:
    def scan_scene(scene_name):
        global faro_scanned_scene1, faro_scanned_scene2, faro_scanned_scene3
        global scene1_collected_count, scene2_collected_count, scene3_collected_count
        if scene_name == "scene1" and not faro_scanned_scene1:
            faro_scanned_scene1 = True
            scene1_collected_count += 1
            renpy.hide_screen("faro3d_scan")
            renpy.notify("Scene 1 scanned with FARO 3D")
        elif scene_name == "scene2" and not faro_scanned_scene2:
            faro_scanned_scene2 = True
            scene2_collected_count += 1
            renpy.hide_screen("faro3d_scan")
            renpy.notify("Scene 2 scanned with FARO 3D")
        elif scene_name == "scene3" and not faro_scanned_scene3:
            faro_scanned_scene3 = True
            scene3_collected_count += 1
            renpy.hide_screen("faro3d_scan")
            renpy.notify("Scene 3 scanned with FARO 3D")
        else:
            renpy.hide_screen("faro3d_scan")




