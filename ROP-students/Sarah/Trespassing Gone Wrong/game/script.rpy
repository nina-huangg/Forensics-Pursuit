# The script of the game goes in this file.

default modal_value = False

# Is toolbox currently on the screen
default showing_toolbox = False

# Is the toolbox currently open
default toolbox_open = False

# List of tools in tool box
default tools = { "tape" : False, "bag" : False, "powder" : False, "marker" : True, "scalebar" : False, "light" : False, "lifting_tape" : False, "fixative" : False, "dental_stone_powder" : False, "water" : False, "spatula" : False, "timer" : False, "box" : False}

# Is the player currently outside
default outside = True

# Is the player at the door
default at_door = False

# For footprint process
# Is the footprint selected
default selected_footprint = False
# Have footprints been marked with evidence marker
default footprints_marked = False
# Has dental stone powder been used
default powder_placed = False
# Has water been added to dental stone powder
default placed_water = False
# Has footprint been casted
default casted = False
# Has cast dried
default cast_dried = False
# Has cast been removed
default cast_removed = False

# For fingerprint process
# Has a fingerprint been selected
default selected_fingerprint = False
default fingerprint_dusted = False
default fingerprint_scaled = False

# The game starts here.

label start:

    # Starting background (outside the abandoned house)

    scene abandoned_house_idle

    # Debrief the player on the scenario

    "You have just arrived at the scene of a possible homicide. \n \n Press space to continue."

    "Last night, a neighbour reported seeing a person entering the abandoned house. \n \n Press space to continue." 
    
    "This neighbour has reported this many times over the past five years but, whenever inspected, nobody was found and the house was deemed secure. \n \n Press space to continue."

    "This time when police were investigating the possible tresspassing issue, they discovered the door to the house was unlocked. \n \n Press space to continue."

    "Inside the abandoned house they discovered human skeletal remains, a gun and some used syringes. \n \n Press space to continue."

    "Your job is to collect all the forensic evidence available to help solve this homicide. \n \n Press space to continue."

    scene abandoned_house_idle

    label screen_selection:

        if outside:
            if fingerprint_scaled:
                scene scaled_fingerprint
            elif fingerprint_dusted:
                scene dusted_fingerprint
            elif selected_fingerprint:
                scene door_close_up_idle
            elif at_door:
                show screen front_door
            elif cast_removed:
                scene closed_box_idle
            elif casted:
                scene casted_footprint
            elif placed_water:
                scene mixed_idle
            elif powder_placed:
                scene with_powder_idle
            elif selected_footprint:
                scene footprint_idle
            elif footprints_marked:
                show screen explore_outside_marked
            else: 
                show screen explore_outside
            
        call screen toolbox
        
    label evidence_markers:
        show screen toolbox
        call screen mark_footprints

    label placed_marker:
        scene abandoned_house_marked_idle

        if footprints_marked:
            $ footprints_marked = False
        else:
            $ footprints_marked = True
        jump screen_selection

    label fixative:
        $ toolbox_show = False
        scene footprint_idle
        hide screen toolbox
        hide screen expand_tools
        call screen apply_fixative

    label applied_fixative:
        hide apply_fixative
        show screen toolbox
        show screen expand_tools
        scene footprint_idle
        jump screen_selection

    label dental_stone_powder:
        $ toolbox_show = False
        scene empty_bag_idle
        hide screen toolbox
        hide screen expand_tools
        call screen powder_in_bag

    label placed_powder:
        $ powder_placed = True
        hide powder_in_bag
        show screen toolbox
        show screen expand_tools
        scene with_powder_idle 
        jump screen_selection

    label water:
        $ toolbox_show = False
        scene with_powder_idle
        hide screen toolbox
        hide screen expand_tools
        call screen add_water

    label placed_water:
        $ placed_water = True
        hide add_water 
        show screen toolbox
        show screen expand_tools
        scene mixed_idle
        jump screen_selection

    label spatula:
        $ toolbox_show = False
        scene mixed_idle
        hide screen toolbox
        hide screen expand_tools
        call screen cast_footprint

    label casted:
        $ casted = True
        hide cast_footprint
        show screen toolbox
        show screen expand_tools
        scene casted_footprint
        jump screen_selection

    label timer:
        scene casted_footprint
        show screen toolbox
        show screen expand_tools
        "Waiting to dry . . ."
        $ cast_dried = True
        jump screen_selection

    label open_box:
        scene casted_footprint
        call screen remove_cast

    label removed_cast:
        $ cast_removed = True
        hide remove_cast
        show screen toolbox
        show screen expand_tools
        scene footprint_idle
        jump screen_selection

    label tamper_tape:
        $ default_mouse = 'tape'
        $ toolbox_show = False
        if selected_footprint:
            scene closed_box_idle
            show screen toolbox
            show screen expand_tools
            call screen tape_box
        else: 
            scene door_close_up_dark_idle
            hide screen toolbox
            hide screen expand_tools
            show screen tamper_evident_tape(False)
            call screen tamper_evident_tape(True)

    label finished_cast:
        hide tape_box
        show screen toolbox
        show screen expand_tools
        scene taped_box_idle
        $ renpy.pause(0.7)

        # Set all variables related to the footprints to False since the process is done
        $ selected_footprint = False
        $ footprints_marked = False
        $ powder_placed = False
        $ placed_water = False
        $ casted = False
        $ cast_dried = False
        $ cast_removed = False    

        $ tools["fixative"] = False
        $ tools["dental_stone_powder"] = False
        $ tools["water"] = False
        $ tools["spatula"] = False
        $ tools["timer"] = False
        $ tools["box"] = False
        $ tools["tape"] = False

        jump screen_selection

    label uv_light:
        $ toolbox_show = False
        hide screen toolbox
        hide screen expand_tools
        scene door_close_up_dark_idle

        call screen uv_light_door

    label found_fingerprint:
        hide screen uv_light_door
        show screen toolbox
        show screen expand_tools
        jump screen_selection

    label magnetic_powder:
        $ toolbox_show = False
        hide screen toolbox
        hide screen expand_tools
        scene door_close_up_idle

        call screen dust_door

    label dusted:
        hide screen dust_door
        scene dusted_fingerprint
        $ fingerprint_dusted = True
        show screen toolbox
        show screen expand_tools

        jump screen_selection

    label scalebar:
        $ toolbox_show = False
        hide screen toolbox
        hide screen expand_tools
        scene dusted_fingerprint

        call screen scale_print

    label scaled:
        hide screen scale_print
        $ fingerprint_scaled = True
        scene scaled_fingerprint
        show screen toolbox
        show screen expand_tools

        jump screen_selection

    label lifting_tape:
        $ toolbox_show = False
        hide screen toolbox
        hide screen expand_tools
        scene scaled_fingerprint

        call screen lift_fingerprint

    label taped:
        hide screen lift_fingerprint
        scene taped_fingerprint

        call screen add_backing('lift')

    label drag_tape:
        $ default_mouse = 'tape_print_scalebar'
        call screen add_backing('drag')

    label stick_backing:
        $ default_mouse = ''
        show screen add_backing('stick')
        call screen add_backing('complete_front')

    label finish_lifting_tape:
        scene door_close_up_idle
        hide screen add_backing

        show screen toolbox
        show screen expand_tools

        $ fingerprint_scaled = False
        $ fingerprint_dusted = False

        jump screen_selection

    label evidence_bags:
        $ default_mouse = 'evidence_bags'
        $ toolbox_show = False
        scene door_close_up_idle
        hide screen toolbox
        hide screen expand_tools
        scene door_close_up_idle
        show screen current_evidence('insensitive')
        call screen current_evidence('show')

    label drag_card_into_bag:
        $ default_mouse = 'tape_print_scalebar'
        call screen current_evidence('drag')

    label put_card_into_bag:
        $ default_mouse = ''
        call screen current_evidence('put_in')
    
    label evidence_bags_finished:
        $ default_mouse = ''
        scene door_close_up_idle
        hide screen current_evidence
        show screen toolbox
        show screen expand_tools
        jump screen_selection

    label finished_fingerprint:
        scene door_close_up_idle
        $ renpy.pause(0.7)
        scene front_door_idle

        $ selected_fingerprint = False
        $ fingerprint_dusted = False
        $ fingerprint_scaled = False

        $ tools["light"] = False
        $ tools["powder"] = False
        $ tools["scalebar"] = False
        $ tools["tape"] = False
        $ tools["bag"] = False
        $ tools["lifting_tape"] = False

        jump screen_selection


    label tool_expand:
        show screen toolbox

        if toolbox_open:
            hide screen expand_tools
            $ toolbox_open = False
            jump screen_selection
        else:
            $ toolbox_open = True
            $ toolbox_show = True
            show screen expand_tools
            jump screen_selection

    label selected_footprints:

        if footprints_marked:
            hide screen explore_outside_marked
            hide screen explore_outside
        else:
            hide screen explore_outside

        $ selected_footprint = True

        $ tools["fixative"] = True
        $ tools["dental_stone_powder"] = True
        $ tools["water"] = True
        $ tools["spatula"] = True
        $ tools["timer"] = True
        $ tools["box"] = True
        $ tools["tape"] = True

        scene footprint_idle
        call screen toolbox

    label selected_door:
        hide screen explore_outside

        scene front_door_idle

        $ at_door = True

        jump screen_selection

    label door_handle:
        hide screen front_door
        scene door_close_up_idle

        $ selected_fingerprint = True

        $ tools["light"] = True
        $ tools["powder"] = True
        $ tools["scalebar"] = True
        $ tools["tape"] = True
        $ tools["bag"] = True
        $ tools["lifting_tape"] = True

        jump screen_selection

    label inside:

