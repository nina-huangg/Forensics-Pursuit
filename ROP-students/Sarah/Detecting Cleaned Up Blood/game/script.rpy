# The script of the game goes in this file.

# mouse cursors
define config.mouse_displayable = MouseDisplayable("mouse_cursor", 0, 0).add("inspect", "magnifying_glass_cursor", 0, 0).add("important", "exclamation_point_cursor", 0, 0).add("uv", "uv_light_resized", 0, 0).add("swab", "swab_cursor", 0, 0).add("pipette", "pipette_cursor", 0, 0).add("spray", "spray_cursor", 0, 0)

# variables for the toolbox
define toolbox_open = False
define toolbox_show = False
define tools = { "ALS_lights" : True, "cotton_swab" : False, "distilled_water" : False, "ethanol" : False, "phenolphthalein" : False, "hydrogen_peroxide" : False, "spray_bottle" : False, "bluestar_packet" : False, "uv_flashlight" : False, "black_granular_powder" : False, "white_granular_powder" : False, "scalebar" : False, "lifting_tape_and_backing" : False, "evidence_bag" : True, "sealing_tape" : True, "evidence_markers" : True}

# variables for the flashlights
define selecting_als_flashlights = False
define using_uva = False
define using_415nm = False
define using_uv = False

# variables for the player's current location/scene
define in_kitchen = True
define at_stove = False
define looking_down = False
define viewing_dish_towel = False
define viewing_floor = False

# variables to keep track of placed evidence markers on stove
define fingerprint_marked = False
define knife_marked = False

# variables to keep track of placed evidence markers in kitchen
define blood_marked = False
define dish_towel_marked = False

# variables to keep track of what evidence has been collected
define collected_knife = False
define collected_dish_towel = False

# variables for blood on the floor
define discovered_blood_pool = False

# variables for blood 
define currently_swabbing = False
define wet_swab = False
define ethanol_selected = False
define ethanol_applied = False
define phenolphthalein_selected = False
define phenolphthalein_applied = False
define hydrogen_peroxide_selected = False
define hydrogen_peroxide_applied = False
define correct_kastle_meyer_procedure = False

# variables for luminol
define spray_bottle_selected = False
define selected_water = False
define selected_luminol_packet = False
define number_of_sprays = 0
define spraying_luminol = False
define luminol_ready = False

# variables for collecting the fingerprint
define selecting_powder = False

# The game starts here.

label start:

    scene kitchen_idle

    label select_screen:

        if viewing_floor:
            show screen kitchen_floor
        elif viewing_dish_towel:
            if collected_dish_towel:
                scene dish_towel_collected
            else:
                scene dish_towel_uncollected
            show screen dish_towel
        elif looking_down:
            show screen stove_looking_down
        elif at_stove:
            if knife_marked:
                if collected_knife:
                        if fingerprint_marked:
                            scene stove_both_collected
                        scene stove_2_collected
                elif fingerprint_marked:
                    scene stove_both_uncollected
                else:
                    scene stove_2_uncollected
            elif fingerprint_marked:
                if collected_knife:
                    scene stove_1_collected
                else:
                    scene stove_1_uncollected
            else:
                if collected_knife:
                    scene stove_collected
                else:
                    scene stove_uncollected
            show screen stove_buttons
        elif in_kitchen:
            if blood_marked and dish_towel_marked:
                scene kitchen_both
            elif blood_marked:
                scene kitchen_4
            elif dish_towel_marked:
                scene kitchen_3
            else:
                scene kitchen_none

            show screen kitchen_screen(discovered_blood_pool)

        call screen toolbox

    label tool_expand:
        show screen toolbox

        if toolbox_open:
            if viewing_floor:
                hide screen expand_floor_tools
            elif at_stove:
                hide screen expand_stove_tools
            else:
                hide screen expand_kitchen_tools

            $ toolbox_open = False
            $ toolbox_show = False
            call screen toolbox
        else:
            $ toolbox_open = True
            $ toolbox_show = True
            if viewing_floor:
                show screen expand_floor_tools
            elif at_stove:
                show screen expand_stove_tools
            else:
                show screen expand_kitchen_tools

            call screen toolbox

    label select_light:
        show screen toolbox

        if selecting_als_flashlights:
            $ selecting_als_flashlights = False
            hide screen select_ALS
            show screen kitchen_screen
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
                show screen kitchen_screen(discovered_blood_pool)
                call screen toolbox
        else:
            $ using_415nm = True
            if in_kitchen:
                call screen kitchen_415nm

    label selected_uva:
        $ selecting_als_flashlights = False

        if using_uva:
            $ using_uva = False
            jump select_screen
        else:
            $ using_uva = True 
            if in_kitchen:
                call screen uva_kitchen

    label discovered_floor_blood:
        $ discovered_blood_pool = True
        $ blood_marked = True
        if using_uva:
            call screen uva_kitchen
        elif using_415nm:
            call screen kitchen_415nm

    label stove:
        hide screen kitchen_screen
        hide screen expand_kitchen_tools
        $ at_stove = True

        $ tools["ALS_lights"] = False
        $ tools["uv_flashlight"] = True

        jump select_screen

    label dish_towel:
        hide screen stove_looking_down
        $ viewing_dish_towel = True
        jump select_screen

    label back:
        if viewing_floor:
            $ viewing_floor = False
            hide screen kitchen_floor
            hide screen expand_floor_tools

            $ tools["cotton_swab"] = False
            $ tools["distilled_water"] = False
            $ tools["ethanol"] = False
            $ tools["phenolphthalein"] = False
            $ tools["hydrogen_peroxide"] = False
            $ tools["spray_bottle"] = False
            $ tools["bluestar_packet"] = False
            $ tools["evidence_marker"] = True
            $ tools["ALS_lights"] = True

        elif viewing_dish_towel:
            $ viewing_dish_towel = False
            hide screen dish_towel
        elif at_stove:
            $ at_stove = False
            $ tools["uv_flaslight"] = False
            $ tools["ALS_lights"] = True
            hide screen kitchen_stove
            hide screen stove_buttons
            hide screen expand_stove_tools
        
        jump select_screen

    label look_down:
        $ looking_down = True
        $ tools["uv_flashlight"] = False
        jump select_screen
    
    label look_up:
        $ looking_down = False
        $ tools["uv_flashlight"] = True
        hide screen stove_looking_down
        jump select_screen

    label place_evidence_marker:
        if at_stove:
            show screen toolbox
            call screen place_marker_stove
        elif in_kitchen:
            show screen toolbox
            call screen place_marker_kitchen

    label placed_marker_dish_towel:
        $ dish_towel_marked = True
        jump select_screen

    label placed_fingerprint:
        $ fingerprint_marked = True
        jump select_screen

    label placed_knife:
        $ knife_marked = True
        jump select_screen

    label uv_light:
        if using_uv:
            $ using_uv = False
            $ default_mouse = "default"
            hide screen dark_stove
            hide dark_overlay
            show screen stove_buttons
            show screen expand_stove_tools
            call screen toolbox
        else:
            $ using_uv = True
            $ default_mouse = "uv"
            hide screen stove_buttons
            hide screen toolbox
            hide screen expand_stove_tools
            show dark_overlay
            show screen dark_stove
            show screen expand_stove_tools
            call screen toolbox

    label found_fingerprint:
        $ default_mouse = "default"
        hide screen dark_stove
        $ using_uv = False
        $ fingerprint_marked = True
        jump select_screen

    label select_powder:
        show screen toolbox

        if selecting_powder:
            $ selecting_powder = False
            hide screen select_powder
            show screen stove_buttons
            call screen toolbox
        else:
            $ selecting_powder = True
            hide screen stove_buttons
            call screen select_powder

    label evidence_bags:
        if viewing_dish_towel:
            show screen collected_dish_towel
            show screen expand_stove_tools
            call screen toolbox
        elif at_stove:
            show screen collected_knife
            show screen expand_stove_tools
            call screen toolbox

    label collect_towel:
        hide screen stove_buttons
        hide screen collected_dish_towel
        $ collected_dish_towel = True
        scene dish_towel_collected_bag
        show screen expand_stove_tools
        call screen toolbox

    label sealed_towel_bag:
        hide screen seal_dish_towel
        scene dish_towel_collected_sealed
        $ renpy.pause(0.7)
        jump select_screen

    label collect_knife:
        hide screen collected_knife
        $ collected_knife = True
        if knife_marked:
            if fingerprint_marked:
                scene stove_both_collected
            else:
                scene stove_2_collected
        elif fingerprint_marked:
            scene stove_1_collected
        else:
            scene stove_collected

        show evidence_bag
        show screen expand_stove_tools
        call screen toolbox

    label sealed_knife_bag:
        hide screen sealed_knife
        hide evidence_bag
        show sealed_evidence_bag
        $ renpy.pause(0.7)
        jump select_screen

    label tamper_tape:
        if viewing_dish_towel:
            show screen seal_dish_towel
            show screen expand_stove_tools
            call screen toolbox
        elif at_stove:
            show screen sealed_knife
            show screen expand_stove_tools
            call screen toolbox

    label floor:
        hide screen kitchen_screen
        scene floor_idle
        $ viewing_floor = True
        hide screen expand_kitchen_tools

        $ tools["ALS_lights"] = False
        $ tools["evidence_markers"] = False
        $ tools["cotton_swab"] = True
        $ tools["distilled_water"] = True
        $ tools["ethanol"] = True
        $ tools["phenolphthalein"] = True
        $ tools["hydrogen_peroxide"] = True
        $ tools["spray_bottle"] = True
        $ tools["bluestar_packet"] = True

        jump select_screen

    label selected_swab:
        if currently_swabbing:
            $ default_mouse = "default"
            $ currently_swabbing = False
            hide screen swab_procedure
            hide screen swab_floor
        else:
            $ default_mouse = "swab"
            $ currently_swabbing = True
            show screen swab_procedure
            show screen swab_floor
            show screen expand_floor_tools

        show screen expand_floor_tools
        call screen toolbox

    label wet:
        if currently_swabbing:
            $ wet_swab = True
            show screen expand_floor_tools
            call screen toolbox
        else:
            $ selected_water = True
            show screen expand_floor_tools
            call screen toolbox

    label collect_swab:
        hide screen swab_procedure

    label throw_out_swab:
        $ default_mouse = "default"
        $ currently_swabbing = False
        $ wet_swab = False
        $ ethanol_selected = False
        $ ethanol_applied = False
        $ phenolphthalein_selected = False
        $ phenolphthalein_applied = False
        $ hydrogen_peroxide_selected = False
        $ hydrogen_peroxide_applied = False
        $ correct_kastle_meyer_procedure = False
        jump select_screen

    label swabbed_floor:
        $ default_mouse = "default"
        hide screen swab_floor
        show screen swab_procedure
        show screen clean_swab
        show screen expand_floor_tools
        call screen toolbox

    label pick_up_swab:
        if ethanol_selected:
            $ ethanol_applied = True
            if phenolphthalein_applied or hydrogen_peroxide_applied or not wet_swab:
                $ correct_kastle_meyer_procedure = False
            else:
                $ correct_kastle_meyer_procedure = True
            $ ethanol_selected = False
            $ default_mouse = "default"
        elif phenolphthalein_selected:
            $ phenolphthalein_applied = True
            if not ethanol_applied or hydrogen_peroxide_applied:
                $ correct_kastle_meyer_procedure = False
            $ phenolphthalein_selected = False
            $ default_mouse = "default"
        elif hydrogen_peroxide_selected:
            $ hydrogen_peroxide_applied = True
            if ethanol_applied and phenolphthalein_applied and correct_kastle_meyer_procedure:
                $ hydrogen_peroxide_selected = False
                $ default_mouse = "default"
                jump display_positive_result
            $ hydrogen_peroxide_selected = False
            $ default_mouse = "default"
        else :
            hide screen clean_swab
            hide screen positive_swab
            $ default_mouse = "swab"
        
        call screen toolbox

    label display_positive_result:
        hide screen clean_swab
        hide screen expand_floor_tools
        hide screen swab_procedure
        show screen swab_procedure
        show screen expand_floor_tools
        call screen positive_swab
        call screen toolbox

    label ethanol:
        if ethanol_selected:
            $ default_mouse = "default"
            $ ethanol_selected = False
        else:
            $ default_mouse = "pipette"
            $ ethanol_selected = True

        show screen expand_floor_tools
        call screen toolbox

    label phenolphthalein:
        if phenolphthalein_selected:
            $ default_mouse = "default"
            $ phenolphthalein_selected = False
        else:
            $ default_mouse = "pipette"
            $ phenolphthalein_selected = True

        show screen expand_floor_tools
        call screen toolbox

    label hydrogen_peroxide:
        if hydrogen_peroxide_selected:
            $ default_mouse = "default"
            $ hydrogen_peroxide_selected = False
        else:
            $ default_mouse = "pipette"
            $ hydrogen_peroxide_selected = True

        show screen expand_floor_tools
        call screen toolbox

    label spray_bottle:
        if spray_bottle_selected:
            $ spray_bottle_selected = False
            hide screen empty_bottle
        else:
            $ spray_bottle_selected = True
            show screen empty_bottle

        show screen expand_floor_tools
        call screen toolbox

    label luminol_packet:
        if selected_luminol_packet:
            $ selected_luminol_packet = False
        else:
            $ selected_luminol_packet = True
        
        show screen expand_floor_tools
        call screen toolbox

    label selected_bottle:
        if selected_water:
            hide screen empty_bottle
            $ selected_water = False
            show screen water_bottle
        elif selected_luminol_packet:
            hide screen water_bottle
            $ luminol_ready = True
            $ selected_luminol_packet = False
            call screen luminol_bottle
        elif luminol_ready:
            hide screen luminol_bottle
            $ default_mouse = "spray"
            show screen dark_floor
        
        show screen expand_floor_tools
        call screen toolbox

    label spray_luminol:
        $ number_of_sprays = number_of_sprays + 1

        if number_of_sprays == 3:
            $ default_mouse = "default"
            hide screen dark_floor
            hide screen kitchen_floor
            hide screen expand_floor_tools
            scene luminol_floor
            $ renpy.pause(5)
            jump select_screen
        else: 
            show screen dark_floor
            show screen expand_floor_tools
            call screen toolbox



        



