# The script of the game goes in this file.

# mouse cursors
define config.mouse_displayable = MouseDisplayable("mouse_cursor", 0, 0).add("inspect", "magnifying_glass_cursor", 0, 0)

# variables for the toolbox
define toolbox_open = False
define toolbox_show = False
define tools = {"ALS_lights": True, "cotton_swab": False, "distilled_water": False, "ethanol": False, "phenolphthalein": False, 
    "hydrogen_peroxide": False, "bluestar_packet": False, "uv_flashlight": False, "black_granular_powder": False, "white_granular_powder": False, 
    "scalebar": False, "lifting_tape_and_backing": False, "evidence_bag": False, "sealing_tape": False, "evidence_markers": False, "crime_scene_tape": False}

# variables for the als flashlights
define selecting_als_flashlights = False
define using_uva = False
define using_415nm = False

# variables for the player's current location/scene
define in_kitchen = True
define at_stove = False
define at_oven = False
define viewing_dish_towel = False
define at_wall = False
define viewing_floor = False

# variables for blood on the floor
define discovered_blood_pool = False

#variables for blood on the wall
define discovered_blood_spatter = False

# The game starts here.

label start:

    scene kitchen_idle

    label select_screen:

        if at_wall:
            show screen kitchen_wall
        elif viewing_floor:
            show screen kitchen_floor
        elif viewing_dish_towel:
            show screen dish_towel
        elif at_oven:
            show screen oven_screen
        elif at_stove:
            show screen kitchen_stove
        elif in_kitchen:
            show screen kitchen_screen(discovered_blood_pool, discovered_blood_spatter)
        call screen toolbox

    label tool_expand:
        show screen toolbox

        if toolbox_open:
            hide screen expand_tools
            $ toolbox_open = False
            $ toolbox_show = False
            call screen toolbox
            jump select_screen
        else:
            $ toolbox_open = True
            $ toolbox_show = True
            show screen expand_tools
            jump select_screen

    label select_light:
        show screen toolbox

        if selecting_als_flashlights:
            $ selecting_als_flashlights = False
            hide screen select_ALS
            call screen toolbox
        else:
            hide screen kitchen_screen
            $ selecting_als_flashlights = True
            call screen select_ALS

    label selected_415nm:
        $ selecting_als_flashlights = False

        if using_415nm:
            $ using_415nm = False
            if in_kitchen:
                show screen kitchen_screen(discovered_blood_pool, discovered_blood_spatter)
                call screen toolbox
        else:
            $ using_415nm = True
            if in_kitchen:
                call screen kitchen_415nm

    label selected_uva:
        $ selecting_als_flashlights = False

        if using_uva:
            $ using_uva = False
            if in_kitchen:
                show screen toolbox
                call screen kitchen_screen(discovered_blood_pool, discovered_blood_spatter)
        else:
            $ using_uva = True 
            if in_kitchen:
                call screen uva_kitchen

    label discovered_floor_blood:
        $ discovered_blood_pool = True
        if using_uva:
            call screen uva_kitchen
        elif using_415nm:
            call screen kitchen_415nm

    label discovered_wall_spatter:
        $ discovered_blood_spatter = True
        if using_uva:
            call screen uva_kitchen
        elif using_415nm:
            call screen kitchen_415nm

    label stove:
        hide screen kitchen_screen
        $ at_stove = True
        jump select_screen

    label oven:
        hide screen kitchen_stove
        $ at_oven = True
        jump select_screen

    label dish_towel:
        hide screen kitchen_stove
        $ viewing_dish_towel = True
        jump select_screen

    label floor:
        hide screen kitchen_stove
        $ viewing_floor = True
        jump select_screen

    label wall:
        hide screen kitchen_stove
        $ at_wall = True
        jump select_screen

    label back:
        if at_wall:
            $ at_wall = False
            hide screen kitchen_wall
        elif viewing_floor:
            $ viewing_floor = False
            hide screen kitchen_floor
        elif viewing_dish_towel:
            $ viewing_dish_towel = False
            hide screen dish_towel
        elif at_oven:
            $ at_oven = False
            hide screen oven_screen
        elif at_stove:
            $ at_stove = False
            hide screen kitchen_stove
        
        jump select_screen
