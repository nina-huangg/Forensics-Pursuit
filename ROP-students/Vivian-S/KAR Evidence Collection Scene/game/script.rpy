### The script of the game goes in this file.

# ----------------------------- Nina's Code ----------------------------- 

# variable that describes whether current user is in the center (of all five possible positions)
default middle = True
# which direction currently looking at 
default front_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default curr_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default hallway_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default stove_directions = {'up': False, 'down': False, 'left': False, 'right': False}
# whether toolbox is currently displayed
default toolbox_show = False
# first time exploring toolbox?
default first_time_toolbox = True
# which tool is currently enabled (shown on screen)
default tools = { "tape" : False, "bag": False, "powder": False, "marker": False, "scalebar": False, "light": True, "lifting_tape": False}
# finished evidence collection?
default finish_collection = False
# finish tutorial
default finish_tutorial = False
# define config.mouse = { }
# define config.mouse['pressed_default'] = [ ( "mouse-click.png", 0, 0) ]
# define config.mouse['button'] = [ ( "mouse-click.png", 0, 0) ]
define config.mouse = { }
define config.mouse['default'] = [ ( "five.png", 0, 0) ]
define config.mouse['pressed_default'] = [ ( "grab.png", 0, 0) ]
define config.mouse['button'] = [ ( "grab.png", 0, 0) ]
# ----------------------------- My Code ----------------------------- 


style draw_ui:
    spacing 2

init python:

    # KEY MAPPINGS -------------------------

    config.keymap['dismiss'].append('K_UP')
    config.keymap['dismiss'].append('K_DOWN')
    config.keymap['dismiss'].append('K_LEFT')
    config.keymap['dismiss'].append('K_RIGHT')

    default_colour = '#ffc157'
    freehand_canvas = FreehandCanvas(default_colour, 400, 1100) # size of canvas

    freehand_canvas.line_width = 30

## Drawing screen ###############################################################

screen freehand_draw():

    vbox:
        hbox:
            vbox:
                style "draw_ui"
            frame:
                background "door_closeup_clear"
                padding (700, 0)
                xsize 400
                ysize 400

                add freehand_canvas
         
        hbox:
            style "draw_ui"
            xpos 1200
            ypos 100
            imagebutton:
                idle "clear-idle"
                hover "clear-hover"
                action Function(freehand_canvas.clear)
        
        hbox:
            style "draw_ui"
            xpos 1200
            ypos 300
            imagebutton:
                idle "done-idle"
                hover "done-hover"
                action Jump("timer")


# DEFINITIONS -------------------------

image string_tape_left = "string_tape_left.png"
define s = Character("Supervisor")

# LABELS -------------------------




### The game starts here.
label start:
    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = ["lantern", "tape"] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Evidence marker", "Evidence bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag", "Pvs kit"] # holds names for inspect pop-up text 
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

    $all_evidence_markers = []
    call screen opening_screen

# REQUIRED FOR INVENTORY -----------------------------------------:

# sets up environment items for first scene
label setupScene1:

    # environment items to interact with in this scene - remember to put exact file name
    $environment_items = ["lantern"]

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

            # door vines = dotted tape, don't need rn
            # if item == "door-vines":
            #     environment_sprites[-1].width = 2500 / 2
            #     environment_sprites[-1].height = 696 / 2
            #     environment_sprites[-1].x = 2000
            #     environment_sprites[-1].y = 550
            # if item == "tape":
            #     environment_sprites[-1].width = 101 / 2
            #     environment_sprites[-1].height = 55 / 2
            #     environment_sprites[-1].x = 1020
            #     environment_sprites[-1].y = 430
            if item == "lantern":
                environment_sprites[-1].width = 300 / 2
                environment_sprites[-1].height = 231 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 500

    # scene scene-1-bg at half_size - sets background image, don't need rn
    call screen scene1

label setupScene2:
    # environment items to interact with
    $environment_items = ["right_hand", "duct_tape"]


    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image

            if item == "right_hand":
                environment_sprites[-1].width = 999 / 2
                environment_sprites[-1].height = 621 / 2
                environment_sprites[-1].x = 598
                environment_sprites[-1].y = 3000
            elif item == "duct_tape":
                environment_sprites[-1].width = 376 / 2
                environment_sprites[-1].height = 540 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 500

    # scene scene-1-bg at half_size # change as necessary
    call screen scene1

label removeGun:
    hide gun_cap_up
    jump setupScene3


label gun_with_cartridges_label:
    # environment items to interact with
    $environment_items = ["tip_holes"]

    transform gun_pos:
        xalign 1.0 yalign 0.45

    show gun_with_cartridges_hand at gun_pos

    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image

            if item == "tip_holes":
                environment_sprites[-1].width = 144 
                environment_sprites[-1].height = 148
                environment_sprites[-1].x = 860
                environment_sprites[-1].y = 180

    # scene scene-1-bg at half_size # change as necessary'
    call screen scene1

label setupScene3:
    
    # jump impression
    hide gun_cap_up

    # environment items to interact with
    $environment_items = ["right_hand"]

    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image

            if item == "right_hand":
                environment_sprites[-1].width = 1998 / 2
                environment_sprites[-1].height = 1242 / 2
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 100

    # scene scene-1-bg at half_size # change as necessary
    call screen scene1

label setupScene4:
    # environment items to interact with
    $environment_items = ["gun_lid"]

    transform gun_pos:
        xalign 1.0 yalign 0.45

    show hand_with_gun1 at gun_pos

    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image

            if item == "gun_lid":
                environment_sprites[-1].width = 400 / 2
                environment_sprites[-1].height = 586 / 2
                environment_sprites[-1].x = 1120
                environment_sprites[-1].y = 350

    # scene scene-1-bg at half_size # change as necessary'
    call screen scene1


label setupScene5:
    # environment items to interact with
    $environment_items = ["cart_holes"]

    hide hand_with_gun1

    transform gun_pos:
        xalign 1.0 yalign 0.45

    show gun_cap_up at gun_pos

    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image
            if item == "cart_holes":
                environment_sprites[-1].width = 412
                environment_sprites[-1].height = 228
                environment_sprites[-1].x = 1150
                environment_sprites[-1].y = 460

    # scene scene-1-bg at half_size # change as necessary
    call screen scene1


transform half_size:
    zoom 0.5
    
# starting screen 
label enter_splash_screen:
    scene entering_splash_screen
    with Dissolve(.8)
    call screen splash_screen

label kar_title:
    play music "mystery.mp3"
    scene title_card
    with Dissolve(2.5)
    call screen kar_title_screen

# debrief
label robarts_exterior:
    stop music fadeout 1.0
    scene robarts_exterior
    "Hey there! You must be the new FIA in training."
    "My name is Steve, I'll be assisting you with collecting evidence for this case."
    "To give you an overview, female student went missing a couple days ago and was last seen at Robarts Library, specifically in the Robarts Commons."
    "Witnesses close to the student were asked to come in for questioning and sources close to the student claim the student was staying late studying for a chemistry exam and never returned home nor showed up for their exam."
    "The team already secured the area and identified the location where the victim was kidnapped."
    "Let's go inside and take a look."
    # show supervisor
    # s "You're late."
    # s "You're lucky I haven't fired you."
    # s "Anyways, a female student went missing a couple days ago and was last seen at Robarts Library, specifically in the Robarts Commons."
    # s "Witnesses close to the student were asked to come in for questioning and sources close to the student claim the student was staying late studying for a chemistry exam and never returned home nor showed up for their exam."
    # s "Our team already secured the area and identified the location where the victim was kidnapped."
    # s "Let's go inside and take a look."
    # s "Our forensics team also retrieved some critical information about the student that you might want to look at."
    # s "Here, take a look."
    jump study_room1
    # scene folder
    # call screen file_folder()

# INSIDE STUDY ROOM -------------------------

label study_room1:
    scene outside_study
    call screen outside_study1

label gloves1:
    show hands
    call screen gloves

label gloves2:
    python:
        # adds tape and ziploc bag to inventory
        addToInventory(["evidence_bag"])
        addToToolbox(["pvs_kit"])
        addToToolbox(["evidence_marker"])
        addToToolboxPop(["empty_gun"])
        addToToolboxPop(["cartridges"])
        addToToolboxPop(["tip"])
    hide hands
    show gloved_hands
    pause 
    "Great job, now click the doorknob to head inside!"
    hide gloved_hands
    call screen outside_study2

label study_room3:
    show screen hint_screen1("HINT: ")
    python:
        renpy.show_screen("toolbox")
    scene inside_study
    show screen study_room3_inventory
    "Look around and see if you can spot any traces of evidence."
    "Place down evidence markers on areas that may have evidence."
    
    # HINT: Use your cursor and mouse over the area.

    # environment items to interact with
    $environment_items = ["marker1", "marker2", "marker3"]

    # track = TrackCursor("inside_study.png", 70)

    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image
            if item == "marker1":
                environment_sprites[-1].width = 193
                environment_sprites[-1].height = 298
                environment_sprites[-1].x = 200
                environment_sprites[-1].y =780
            elif item == "marker2":
                environment_sprites[-1].width = 506
                environment_sprites[-1].height = 314
                environment_sprites[-1].x = 350
                environment_sprites[-1].y = 550
            elif item == "marker3":
                environment_sprites[-1].width = 163
                environment_sprites[-1].height = 437
                environment_sprites[-1].x = 1100
                environment_sprites[-1].y = 380

    # scene scene-1-bg at half_size # change as necessary
    call screen scene1


label inside_study1_screen:
    call screen inside_study1

label under_table:
    scene underneath_table
    show screen back_button1
    python:
        renpy.hide_screen("marker1")
        renpy.hide_screen("marker2")
        renpy.hide_screen("marker3")
    jump setupScene1

label chair:
    scene chair_closeup
    show screen back_button1
    python:
        renpy.hide_screen("marker1")
        renpy.hide_screen("marker2")
        renpy.hide_screen("marker3")
    jump setupScene2

label scratches:
    scene door_closeup_clear
    show screen back_button1
    python:
        renpy.hide_screen("marker1")
        renpy.hide_screen("marker2")
        renpy.hide_screen("marker3")
    "Hmm, some scratches on the door. What technique should be used to collect this piece of evidence?"
    scene door_closeup
    # hide expression my_drawing 

menu:
    "Polyvinylsiloxane": 
        jump choices1_a
    "Dental Stone":
        jump choices2_a

label choices1_a:
    "Correct!"
    jump setupScene3  

label choices2_a:
    "That's not quite right. Try again!"
    jump scratches
    
label gun_front:
    jump setupScene4
    call screen hand_with_gun
    

label gun_side:
    jump setupScene5

label impression:
    hide gun_with_cartridges_hand
    call screen freehand_draw
    # $my_drawing = draw_logic.Draw.main(background = "door_closeup_clear.png", start_color = "#ffc157", start_width = 50)


image timer:
    "timer1.png"
    0.5
    "timer2.png"
    0.5
    "timer3.png"
    0.5
    "timer4.png"
    0.5
    "timer5.png"
    0.5
    "timer6.png"
    0.5
    "timer7.png"
    0.5
    "timer8.png"
    0.5
    "timer9.png"
    0.5
    "timer10.png"
    # repeat

label timer:
    scene door_closeup_clear
    show screen impression_dry

    transform timer_pos:
        xalign 0.8 yalign 0.45

    show timer at timer_pos
    pause
    

label collect_impression:
    hide screen impression_dry
    python:
        addToInventory(["pvs_in_bag"])
        renpy.show_screen("inspectItem", ["pvs_in_bag"])
    
    pause


# NOT USED RN ------------------------------------------------------------------------------------------------

# end debrief, go inside library - not used rn
label inside_library:
    scene robarts_exterior
    show supervisor
    s "Hopefully that information should be sufficient to identify the location of the crime."
    s "Let's head inside."
    scene task1
    pause
    hide string_tape_left
    scene main_lib_interior
    call screen task_1()

# tape - not used rn
label tape:
    call screen tape()
    # remember to use tape.mp3

label instructions_key_arrows:
    #show screen move_on
    hide screen instructions_text_screen
    "Great job! Now let's head back!"
    #hide screen move_on
    call screen instructions_key_screen()

# label jump_directions:
#     hide screen opening
#     if middle:
#         if front_directions['up']:
#             $ curr_directions['up'] = True
#             scene front_up
#             show screen opening('looking up')
#         elif front_directions['down']:
#             $ curr_directions['down'] = True
#             scene front_down
#             show screen opening('looking down')
#             show screen toolbox
#         elif front_directions['right']:
#             $ curr_directions['right'] = True
#             scene right
#             show screen opening('looking to the right')
#         elif front_directions['left']:
#             $ curr_directions['left'] = True
#             scene left
#             show screen opening('looking to the left')
#         $ middle = False
#         call screen instructions_key_screen()

#     else:
#         scene robarts_outside_2
#         show screen opening('back in center')
#         python:
#             middle = True
#             for c_d in front_directions:
#                 front_directions[c_d] = False
#             for c_d in curr_directions:
#                 curr_directions[c_d] = False
#         call screen instructions_move_on_screen
#         call screen instructions_key_screen()

label keep_exploring:
    call screen instructions_key_screen()

# TAPE + NAVIGATION ---------------------
label interior_scene2:
    scene interior_2
    show screen taped_left
    jump setupScene1

label interior_scene3:
    scene right_1
    call screen interior_scene3a

label r2:
    scene right_2
    call screen interior_scene3b

label r3:
    scene right_3
    call screen interior_scene3c

label r4:
    scene right_4
    pause

# label setupScene2:
#     # show screen tape_left
#     show string_tape_left:
#         xalign 0.3
#         yalign 0.5
    #xpos 200 ypos 550 at half_size

screen taped_left:
    zorder 1
    # image "taped_left.png" xpos 0 ypos 0.8 at half_size
    imagebutton auto "UI/inventory-icon-%s.png" action If(renpy.get_screen("inventory") == None, true= Show("inventory"), false= Hide("inventory")) xpos 0.03 ypos 0.5 at half_size
# NINA'S CODE ---------------------

### entering scene 
label enter_scene:
    hide screen opening
    #show screen move_on
    "Great job! Let's continue securing the area!"
    pause
    #hide screen move_on
    scene main_lib_interior
    call screen task_1()
    


# label  tutorial_finished:
#     $ default_mouse = ''
#     $ tools['bag'] = False
#     scene footprints_closeup
#     hide screen current_evidence
#     show screen toolbox
#     show screen expand_tools
#     #show screen move_on
#     if not finish_tutorial:
#         show screen evidence_marker_stove
#         "With the evidence collected, we can now remove our evidence marker.\n\n\n>>hit space to continue"
#         $ finish_tutorial = True
#     hide screen evidence_marker_stove
#     "Congratulations! You have now finished evidence collection for this stage.\n\n\n>>hit space to continue"
#     $ finish_collection = True
#     call screen evidence_to_lab

# label enter_lab:
#     hide screen stove_center
#     hide screen move_on_lab
#     hide screen toolbox
#     hide screen expand_tools
#     #hide screen move_on
#     scene entering_lab_screen
#     with Dissolve(.8)
#     call screen temporary_pause


#     return


