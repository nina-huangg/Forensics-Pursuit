# The script of the game goes in this file.

# mouse cursors
define config.mouse_displayable = MouseDisplayable("mouse_cursor", 0, 0).add("inspect", "magnifying_glass_cursor", 0, 0).add("important", "exclamation_point_cursor", 0, 0).add("swab", "swab_cursor", 0, 0).add("pipette", "pipette_cursor", 0, 0).add("spray", "spray_cursor", 0, 0).add("uva", "uva_cursor", 0, 0).add("415nm", "415nm_cursor", 0, 0).add("450nm", "450nm_cursor", 0, 0).add("530nm", "530nm_cursor", 0,0).add("powder", "dusting_powder_cursor", 0, 0).add("bag", "evidence_bag_cursor", 0, 0).add("marker", "evidence_marker_cursor", 0, 0).add("tape", "evident_tape_cursor", 0, 0).add("lifting_tape", "lifting_tape_cursor", 0, 0).add("scalebar", "scalebar_cursor", 0, 0).add("water", "water_cursor", 0, 0).add("lifted_print", "lifted_fingerprint_cursor", 0, 0).add("luminol", "luminol_packet_cursor", 0, 0).add("forensic_tube", "forensic_tube_cursor", 0, 0)

# variables for viewing evidence
define viewing_evidence = False
define current_page = 1
define total_pages = 11
define viewing_pictures = False

# variables for the toolbox
define toolbox_open = False
define toolbox_show = False

# variables for the flashlights
define selecting_als_flashlights = False
define using_uva = False
define using_415nm = False
define using_450nm = False
define using_530nm = False
define using_uv = False

# variables for the player's current location/scene
define in_kitchen = True
define at_stove = False
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
define collected_fingerprint = False
define collected_swab = False

define put_knife_in_tube = False
define knife_tube_sealed = False
define put_knife_in_bag = False
define put_towel_in_bag = False
define knife_not_ready_to_bag = False

# variables for blood on the floor
define discovered_blood_pool = False

# variables for blood 
define currently_swabbing = False
define wet_swab = False
define swabbing_floor = False
define swabbed_floor = False
define ethanol_selected = False
define ethanol_applied = False
define phenolphthalein_selected = False
define phenolphthalein_applied = False
define hydrogen_peroxide_selected = False
define hydrogen_peroxide_applied = False
define correct_kastle_meyer_procedure = False
define bag_selected = False
define properly_swabbed_blood = False
define captured_luminol = False
define holding_swab = False
define selected_water = False
define conducted_kastle_meyer_test = False

define put_swab_in_tube = False
define put_swab_in_bag = False

define display_clean_swab = False
define display_positive_swab = False
define display_swabbing_options = False

define delivered_kastle_meyer_message = False
define warning_swab_message = False

# variables for luminol
define spray_bottle_selected = False
define selected_water = False
define only_water = False
define selected_luminol_packet = False
define number_of_sprays = 0
define luminol_ready = False
define added_water_to_bottle = False
define added_packet_to_bottle = False

# variables for collecting the fingerprint
define selecting_powder = False
define black_powder_selected = False
define scalebar_selected = False
define lifting_tape_selected = False
define currently_collecting_fingerprint = False
define picking_up = True
define backing_card_placed = False

define discovered_fingerprint = False
define dusted_fingerprint = False
define scaled_fingerprint = False
define taped_fingerprint = False
define put_print_on_card = False
define put_print_in_bag = False

# variables for forensic tool selection
define marker_selected = False
define tamper_tape_selected = False
define forensic_tube_selected = False

# The game starts here.

label start:

    scene front

    "You've just arrived at the crime scene. During a welfare check for an individual who is now missing, blood was found on a dish cloth."

    "Your job is to collect the dish cloth and look for additional evidence to solve this disappearance. Enter the house and investigate the scene."

    call screen outside_house

    scene kitchen_idle

    label select_screen:
        if viewing_floor:
            scene floor_idle
            if not currently_swabbing:
                show screen kitchen_floor
        elif viewing_dish_towel:
            jump select_dish_towel_view
        elif at_stove:
            jump select_stove_view
        elif in_kitchen:
            if collected_knife and collected_dish_towel:
                jump select_kitchen_view_all_collected
            elif collected_knife:
                jump select_kitchen_view_knife_collected
            elif collected_dish_towel:
                jump select_kitchen_view_dish_towel_collected
            else:
                jump select_kitchen_view_nothing_collected

            show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        if toolbox_open:
            if viewing_floor:
                show screen expand_floor_tools
            elif viewing_dish_towel:
                show screen_expand_dish_towel_tools
            elif at_stove:
                show screen expand_stove_tools
            elif in_kitchen:
                show screen expand_kitchen_tools
        else:
            show screen collected_evidence_icon
        call screen toolbox

    label select_kitchen_view_all_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene all_all
                elif knife_marked:
                    scene all_blood_towel_knife
                elif fingerprint_collected:
                    scene all_blood_towel_fingerprint
                else:
                    scene all_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene all_blood_fingerprint_knife
                elif knife_marked:
                    scene all_blood_knife
                elif collected_fingerprint:
                    scene all_blood_fingerprint
                else:
                    scene all_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene all_towel_fingerprint_knife
                elif knife_marked:
                    scene all_towel_knife
                elif collected_fingerprint:
                    scene all_towel_fingerprint
                else:
                    scene all_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene all_fingerprint_knife
                elif knife_marked:
                    scene all_knife
                elif collected_fingerprint:
                    scene all_fingerprint
                else:
                    scene all_none
            
        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        if toolbox_open:
            show screen expand_kitchen_tools
        else:
            show screen collected_evidence_icon
        call screen toolbox

    label select_kitchen_view_knife_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene knife_all
                elif knife_marked:
                    scene knife_blood_towel_knife
                elif fingerprint_marked:
                    scene knife_blood_towel_fingerprint
                else:
                    scene knife_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene knife_blood_fingerprint_knife
                elif knife_marked:
                    scene knife_blood_knife
                elif fingerprint_marked:
                    scene knife_blood_fingerprint
                else:
                    scene knife_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene knife_towel_fingerprint_knife
                elif knife_marked:
                    scene knife_towel_knife
                elif fingerprint_marked:
                    scene knife_towel_fingerprint
                else:
                    scene knife_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene knife_fingerprint_knife
                elif knife_marked:
                    scene knife_knife
                elif fingerprint_marked:
                    scene knife_fingerprint
                else:
                    scene knife_none

        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        if toolbox_open:
            show screen expand_kitchen_tools
        else:
            show screen collected_evidence_icon
        call screen toolbox

    label select_kitchen_view_dish_towel_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene towel_all
                elif knife_marked:
                    scene towel_blood_towel_knife
                elif fingerprint_marked:
                    scene towel_blood_towel_fingerprint
                else:
                    scene towel_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene towel_blood_fingerprint_knife
                elif knife_marked:
                    scene towel_blood_knife
                elif fingerprint_marked:
                    scene towel_blood_fingerprint
                else:
                    scene towel_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene towel_towel_fingerprint_knife
                elif knife_marked:
                    scene towel_towel_knife
                elif fingerprint_marked:
                    scene towel_towel_fingerprint
                else:
                    scene towel_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene towel_fingerprint_knife
                elif knife_marked:
                    scene towel_knife
                elif fingerprint_marked:
                    scene towel_fingerprint
                else:
                    scene towel_none

        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        if toolbox_open:
            show screen expand_kitchen_tools
        else:
            show screen collected_evidence_icon
        call screen toolbox

    label select_kitchen_view_nothing_collected:
        if blood_marked:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene none_all
                elif knife_marked:
                    scene none_blood_towel_knife
                elif fingerprint_marked:
                    scene none_blood_towel_fingerprint
                else:
                    scene none_blood_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene none_blood_fingerprint_knife
                elif knife_marked:
                    scene none_blood_knife
                elif fingerprint_marked:
                    scene none_blood_fingerprint
                else:
                    scene none_blood
        else:
            if dish_towel_marked:
                if knife_marked and fingerprint_marked:
                    scene none_towel_fingerprint_knife
                elif knife_marked:
                    scene none_towel_knife
                elif fingerprint_marked:
                    scene none_towel_fingerprint
                else:
                    scene none_towel
            else:
                if knife_marked and fingerprint_marked:
                    scene none_fingerprint_knife
                elif knife_marked:
                    scene none_knife
                elif fingerprint_marked:
                    scene none_fingerprint
                else:
                    scene none_none

        show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
        if toolbox_open:
            show screen expand_kitchen_tools
        else:
            show screen collected_evidence_icon
        call screen toolbox

    label select_stove_view:
        if collected_fingerprint:
            if collected_knife:
                hide screen knife_screen
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker_knife_dusty
                elif fingerprint_marked:
                    scene stove_fingerprint_knife_dusty
                elif knife_marked:
                    scene stove_marker_knife_dusty
                else:
                    scene stove_knife_dusty
            else:
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker_dusty
                elif fingerprint_marked:
                    scene stove_fingerprint_dusty
                elif knife_marked:
                    scene stove_marker_dusty
                else:
                    scene stove_none_dusty
        else:
            if collected_knife:
                hide screen knife_screen
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker_knife
                elif fingerprint_marked:
                    scene stove_fingerprint_knife
                elif knife_marked:
                    scene stove_marker_knife
                else:
                    scene stove_knife
            else:
                if fingerprint_marked and knife_marked:
                    scene stove_fingerprint_marker
                elif fingerprint_marked:
                    scene stove_fingerprint
                elif knife_marked:
                    scene stove_marker
                else:
                    scene stove_none
        if knife_tube_sealed:
            show taped_tube_idle:
                xpos 0.42
                ypos 0.1
        elif put_knife_in_tube:
            show filled_tube_idle:
                xpos 0.42
                ypos 0.1
        if toolbox_open:
            show screen expand_stove_tools
        else:
            show screen collected_evidence_icon
        show screen stove_buttons
        call screen toolbox

    label select_dish_towel_view:
        if dish_towel_marked and collected_dish_towel:
            scene dish_towel_marker
        elif dish_towel_marked:
            scene dish_towel_all
        elif collected_dish_towel:
            scene dish_towel_none
        else:
            scene dish_towel_towel
        if toolbox_open:
            show screen expand_dish_towel_tools
        else:
            show screen collected_evidence_icon
        show screen dish_towel
        call screen toolbox

    label tool_expand:
        show screen toolbox
        if not viewing_evidence:
            if toolbox_open:
                if viewing_floor:
                    hide screen expand_floor_tools
                elif viewing_dish_towel:
                    hide screen expand_dish_towel_tools
                elif at_stove:
                    hide screen expand_stove_tools
                else:
                    hide screen expand_kitchen_tools

                $ toolbox_open = False
                $ toolbox_show = False
                show screen collected_evidence_icon
                call screen toolbox
            else:
                hide screen collected_evidence_icon
                $ toolbox_open = True
                $ toolbox_show = True
                if viewing_floor:
                    show screen expand_floor_tools
                elif viewing_dish_towel:
                    show screen expand_dish_towel_tools
                elif at_stove:
                    show screen expand_stove_tools
                else:
                    show screen expand_kitchen_tools

                call screen toolbox

    label display_evidence:
        if viewing_evidence:
            $ viewing_evidence = False
            hide casefile_inventory
            hide screen show_evidence_bags
            jump select_screen
        else:
            hide screen kitchen_screen
            hide screen display_image
            hide screen present_evidence
            $ current_page = 1
            $ viewing_pictures = False
            $ viewing_evidence = True
            show casefile_inventory:
                ypos 0.05
            show screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab)
            show screen toolbox
            call screen collected_evidence_icon

    label dish_towel_message:
        show screen collected_evidence_icon
        call screen dish_towel_evidence_message
        show screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab)
        show screen toolbox
        call screen collected_evidence_icon

    label knife_message:
        show screen collected_evidence_icon
        call screen knife_evidence_message
        show screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab)
        show screen toolbox
        call screen collected_evidence_icon

    label swab_message:
        show screen collected_evidence_icon
        call screen swab_evidence_message
        show screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab)
        show screen toolbox
        call screen collected_evidence_icon

    label fingerprint_message:
        show screen collected_evidence_icon
        call screen fingerprint_evidence_message
        show screen show_evidence_bags(collected_dish_towel, collected_knife, collected_fingerprint, collected_swab)
        show screen toolbox
        call screen collected_evidence_icon

    label display_images:
        if viewing_pictures:
            $ viewing_pictures = False
            $ current_page = 1
            hide casefile_inventory
            hide screen display_image
            hide screen present_evidence
            jump select_screen
        else:
            hide screen kitchen_screen
            hide screen show_evidence_bags
            $ vewiing_evidence = False
            $ viewing_pictures = True
            show casefile_inventory:
                ypos 0.05
            show screen display_image(current_page, discovered_blood_pool, dish_towel_marked, knife_marked, collected_fingerprint, captured_luminol)
            show screen present_evidence(current_page)
            show screen toolbox
            call screen collected_evidence_icon

    label next_page:
        hide screen display_image
        $ current_page = current_page + 1
        show screen display_image(current_page, discovered_blood_pool, dish_towel_marked, knife_marked, collected_fingerprint, captured_luminol)
        show screen present_evidence(current_page)
        call screen collected_evidence_icon 

    label back_page:
        hide screen display_image
        $ current_page = current_page - 1
        show screen display_image(current_page, discovered_blood_pool, dish_towel_marked, knife_marked, collected_fingerprint, captured_luminol)
        show screen present_evidence(current_page)
        call screen collected_evidence_icon

    label select_light:
        show screen toolbox

        if selecting_als_flashlights:
            $ selecting_als_flashlights = False
            hide screen select_ALS
            hide als_frame
            show screen kitchen_screen(discovered_blood_pool, collected_dish_towel)
            call screen toolbox
        else:
            show als_frame:
                xpos 0.41
                ypos 0.19
            hide screen kitchen_screen
            $ selecting_als_flashlights = True
            call screen select_ALS

    label selected_530nm:
        $ selecting_als_flashlights = False

        if using_530nm:
            $ using_530nm = False
            $ default_mouse = "default"
            hide filter_530nm
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_530nm = True
            $ default_mouse = "530nm"
            hide screen toolbox
            hide screen expand_kitchen_tools
            show filter_530nm
            show screen dark_overlay_with_mouse
            call screen kitchen_530nm

    label selected_450nm:
        $ selecting_als_flashlights = False

        if using_450nm:
            $ using_450nm = False
            $ default_mouse = "default"
            hide filter_450nm
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_450nm = True
            $ default_mouse = "450nm"
            hide screen toolbox
            hide screen expand_kitchen_tools
            show filter_450nm
            show screen dark_overlay_with_mouse
            call screen kitchen_450nm

    label selected_415nm:
        $ selecting_als_flashlights = False

        if using_415nm:
            $ using_415nm = False
            $ default_mouse = "default"
            hide blood_spot
            hide filter_415nm
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_415nm = True
            $ default_mouse = "415nm"
            hide screen toolbox
            hide screen expand_kitchen_tools
            show blood_spot
            show filter_415nm
            show screen dark_overlay_with_mouse
            call screen kitchen_415nm

    label selected_uva:
        $ selecting_als_flashlights = False

        if using_uva:
            $ using_uva = False
            $ default_mouse = "default"
            hide blood_spot
            hide uva_filter
            hide screen dark_overlay_with_mouse
            jump select_screen
        else:
            $ using_uva = True 
            $ default_mouse = "uva"
            hide screen toolbox
            hide screen expand_kitchen_tools
            show blood_spot
            show uva_filter
            show screen dark_overlay_with_mouse
            call screen uva_kitchen

    label discovered_floor_blood:
        $ discovered_blood_pool = True
        $ blood_marked = True
        call screen discovered_blood_with_flashlight
        if using_uva:
            call screen uva_kitchen
        elif using_415nm:
            call screen kitchen_415nm

    label stove:
        hide screen kitchen_screen
        hide screen expand_kitchen_tools
        $ at_stove = True

        jump select_screen

    label dish_towel:
        hide screen kitchen_screen
        hide screen expand_kitchen_tools
        if toolbox_open:
            show screen expand_dish_towel_tools
        $ viewing_dish_towel = True
        jump select_dish_towel_view

    label back:
        hide casefile_inventory
        hide screen show_evidence_bags
        hide screen display_image
        hide screen present_evidence
        $ viewing_evidence = False
        $ viewing_pictures = False
        if viewing_floor:
            $ viewing_floor = False
            hide screen kitchen_floor
            hide screen expand_floor_tools
        elif viewing_dish_towel:
            $ viewing_dish_towel = False
            hide screen dish_towel
            hide screen expand_dish_towel_tools
        elif at_stove:
            $ at_stove = False
            hide screen kitchen_stove
            hide screen stove_buttons
            hide screen collected_knife
            hide screen place_marker_stove
            hide screen expand_stove_tools
        
        jump select_screen

    label place_evidence_marker:
        if marker_selected:
            $ default_mouse = "default"
            $ marker_selected = False
            hide screen place_marker_dish_towel
            hide screen place_marker_stove
            hide screen place_marker_kitchen
            jump select_screen
        else:
            $ default_mouse = "marker"
            $ marker_selected = True
            if viewing_dish_towel:
                if not collected_dish_towel and not dish_towel_marked:
                    show screen expand_dish_towel_tools
                    show screen place_marker_dish_towel
                    call screen toolbox
            elif at_stove:
                if not collected_knife and not knife_marked:
                    show screen expand_stove_tools
                    show screen place_marker_stove
                    call screen toolbox
            elif in_kitchen:
                if not collected_dish_towel and not dish_towel_marked:
                    hide screen kitchen_screen
                    show screen expand_kitchen_tools
                    show screen place_marker_kitchen
                    call screen toolbox
            else:
                $ default_mouse = "default"
                $ marker_selected = False
                show screen toolbox
                call screen nothing_to_mark
                jump select_screen

    label placed_marker_dish_towel:
        hide screen place_marker_dish_towel
        hide screen place_marker_kitchen
        $ default_mouse = "default"
        $ marker_selected = False
        $ dish_towel_marked = True
        jump select_screen

    label placed_fingerprint:
        $ fingerprint_marked = True
        jump select_screen

    label placed_knife:
        hide screen place_marker_stove
        $ default_mouse = "default"
        $ marker_selected = False
        $ knife_marked = True
        jump select_screen

    label uv_light:
        if currently_collecting_fingerprint:
                show screen toolbox
                call screen in_fingerprinting_procedure
                show screen expand_stove_tools
                call screen toolbox
        if using_uv:
            $ using_uv = False
            $ default_mouse = "default"
            hide screen dark_stove
            hide screen dark_overlay_with_mouse
            hide uv_fingerprint
            hide uv_fingerprint_collected
            show screen stove_buttons
            show screen expand_stove_tools
            call screen toolbox
        else:
            $ using_uv = True
            $ default_mouse = "uva"
            hide screen stove_buttons
            hide screen toolbox
            hide screen expand_stove_tools
            if collected_fingerprint:
                show uv_fingerprint_collected
            else:
                show uv_fingerprint
            show screen dark_overlay_with_mouse
            if not collected_fingerprint:
                show screen dark_stove

            show screen expand_stove_tools
            call screen toolbox

    label found_fingerprint:
        $ default_mouse = "default"
        show screen toolbox
        call screen discovered_fingerprint_message
        hide screen dark_stove
        hide screen dark_overlay_with_mouse
        hide uv_fingerprint
        $ discovered_fingerprint = True
        $ using_uv = False
        $ fingerprint_marked = True
        jump select_screen

    label select_black_powder:
        if not collected_fingerprint and discovered_fingerprint:
            if dusted_fingerprint:
                show screen toolbox
                call screen already_dusted
                show screen expand_stove_tools
                call screen toolbox
            if black_powder_selected:
                $ default_mouse = "default"
                $ black_powder_selected = False
                hide screen dust_fingerprint
            else:
                $ default_mouse = "powder"
                $ black_powder_selected = True
                show screen dust_fingerprint

            show screen expand_stove_tools
            call screen toolbox
        else:
            show screen toolbox
            call screen discover_fingerprint_first
            show screen expand_stove_tools
            call screen toolbox

    label dusted_fingerprint:
        $ default_mouse = "default"
        $ black_powder_selected = False
        $ dusted_fingerprint = True
        hide screen stove_buttons
        $ currently_collecting_fingerprint = True
        scene dusted_fingerprint
        hide screen dust_fingerprint
        show screen expand_stove_tools
        call screen toolbox

    label selected_scalebar:
        if not collected_fingerprint and dusted_fingerprint:
            if scaled_fingerprint:
                show screen toolbox
                call screen already_scaled
                show screen expand_stove_tools
                call screen toolbox
            if scalebar_selected:
                $ default_mouse = "default"
                $ scalebar_selected = False
                hide screen scalebar_screen
            else:
                $ default_mouse = "scalebar"
                $ scalebar_selected = True
                show screen scalebar_screen
        show screen expand_stove_tools
        call screen toolbox

    label placed_scalebar:
        $ default_mouse = "default"
        $ scaled_fingerprint = True
        scene dusted_fingerprint_scaled
        $ scalebar_selected = False
        hide screen scalebar_screen
        show screen expand_stove_tools
        call screen toolbox

    label selected_lifting_tape:
        if not collected_fingerprint and scaled_fingerprint:
            if taped_fingerprint:
                show screen toolbox
                call screen already_taped
                show screen expand_stove_tools
                call screen toolbox
            if lifting_tape_selected:
                $ default_mouse = "default"
                $ lifting_tape_selected = False
                hide screen taping_screen
                show screen expand_stove_tools
                call screen toolbox
            else:
                $ default_mouse = "lifting_tape"
                $ lifting_tape_selected = True
                show screen taping_screen
                show screen expand_stove_tools
                call screen toolbox
        show screen expand_stove_tools
        call screen toolbox
    
    label placed_tape:
        $ default_mouse = "default"
        $ lifitng_tape_selected = False
        $ picking_up = False
        $ taped_fingerprint = True
        hide screen taping_screen
        scene dusted_fingerprint_scaled_taped
        show screen picking_up_tape
        show screen expand_stove_tools
        call screen toolbox

    label lifted_tape:
        $ default_mouse = "lifted_print"
        hide screen picking_up_tape
        if backing_card_placed:
            scene fingerprint_removed_backing_card
            show screen placed_fingerprint
        else:
            scene fingerprint_removed
            $ picking_up = True
        show screen expand_stove_tools
        call screen toolbox

    label selected_backing_card:
        if not collected_fingerprint and taped_fingerprint:
            if put_print_on_card:
                    show screen toolbox
                    call screen already_put_on_card
                    show screen expand_stove_tools
                    call screen toolbox
            if picking_up:
                jump finished_placing_fingerprint
            else:
                $ backing_card_placed = True
                scene empty_backing_card
                show screen picking_up_tape
                show screen expand_stove_tools
                call screen toolbox
        show screen expand_stove_tools
        call screen toolbox

    label finished_placing_fingerprint:
        $ default_mouse = "default"
        $ backing_card_placed = True
        hide screen placed_fingerprint
        scene filled_backing_card
        show screen expand_stove_tools
        $ put_print_on_card = True
        call screen toolbox

    label evidence_bags:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if bag_selected:
            $ bag_selected = False
            $ default_mouse = "default"
            hide screen packed_fingerprint
            hide screen packing_swab
            hide screen collecting_dish_towel
            hide screen collected_knife
            jump select_screen
        else:
            $ bag_selected = True
            $ default_mouse = "bag"
            if currently_collecting_fingerprint and put_print_on_card and not collected_fingerprint:
                show screen packed_fingerprint
                show screen expand_stove_tools
                call screen toolbox
            elif viewing_floor:
                if put_swab_in_tube and not collected_swab:
                    show screen packing_swab(bag_selected)
                show screen expand_floor_tools
                call screen toolbox
            elif viewing_dish_towel:
                show screen collecting_dish_towel
                show screen expand_dish_towel_tools
                call screen toolbox
            elif at_stove:
                if knife_tube_sealed:
                    hide taped_tube_idle
                    show screen collect_knife_tube
                show screen expand_stove_tools
                call screen toolbox

    label selected_forensic_tube:
        if forensic_tube_selected:
            $ forensic_tube_selected = False
            $ default_mouse = "default"
            show screen expand_stove_tools
            call screen toolbox
        else:
            $ forensic_tube_selected = True
            $ default_mouse = "forensic_tube"
            show screen collected_knife
            show screen expand_stove_tools
            call screen toolbox

    label knife_put_in_tube:
        if knife_marked and fingerprint_marked:
            scene stove_fingerprint_marker_knife
        elif knife_marked:
            scene stove_marker_knife
        elif fingerprint_marked:
            scene stove_fingerprint_knife
        else:
            scene stove_knife
        $ forensic_tube_selected = False
        $ default_mouse = "default"
        hide screen collected_knife
        $ knife_not_ready_to_bag = True
        $ put_knife_in_tube = True
        $ collected_knife = True
        show filled_tube_idle:
            xpos 0.42
            ypos 0.1
        show screen expand_stove_tools
        call screen toolbox

    label sealed_knife_tube:
        hide filled_tube_idle
        hide screen tube_with_knife
        $ tamper_tape_selected = False
        $ default_mouse = "default"
        $ knife_not_ready_to_bag = False
        $ knife_tube_sealed = True
        show taped_tube_idle:
            xpos 0.42
            ypos 0.1
        show screen expand_stove_tools
        call screen toolbox

    label seal_evidence_bag:
        $ default_mouse = "default"
        $ tamper_tape_selected = False
        hide screen collected_evidence
        show screen toolbox
        show sealed_evidence_bag:
            xpos 0.4
            ypos 0.07
        $ renpy.pause(0.7)
        if currently_collecting_fingerprint:
            $ currently_collecting_fingerprint = False
            $ collected_fingerprint = True
            show screen toolbox
            call screen fingerprint_has_been_collected
        if put_towel_in_bag:
            $ put_towel_in_bag = False
            $ collected_dish_towel = True
            show screen toolbox
            call screen dish_towel_has_been_collected
        if put_knife_in_bag:
            $ put_knife_in_bag = False
            $ collected_knife = True
            $ knife_tube_sealed = False
            $ put_knife_in_tube = False
            show screen toolbox
            call screen knife_has_been_collected
        if put_swab_in_bag:
            $ put_swab_in_bag = False
            $ put_swab_in_tube = False
            $ collected_swab = True
            show screen toolbox
            call screen swab_has_been_collected
        jump select_screen

    label collect_towel:
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen stove_buttons
        hide screen collecting_dish_towel
        $ put_towel_in_bag = True
        if dish_towel_marked:
            scene dish_towel_marker
        else:
            scene dish_towel_none
        show screen collected_evidence
        show screen expand_dish_towel_tools
        call screen toolbox

    label collect_knife:
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen collect_knife_tube
        $ put_knife_in_bag = True
        show screen collected_evidence
        show screen expand_stove_tools
        call screen toolbox

    label packaged_swab:
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen packing_swab
        $ put_swab_in_bag = True
        show screen collected_evidence
        show screen expand_floor_tools
        call screen toolbox

    label pack_fingerprint:
        $ bag_selected = False
        $ default_mouse = "default"
        hide screen packed_fingerprint
        $ put_print_in_bag = True
        scene fingerprint_removed
        show screen collected_evidence
        show screen expand_stove_tools
        call screen toolbox

    label tamper_tape:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if tamper_tape_selected:
            $ tamper_tape_selected = False
            $ default_mouse = "default"
            hide screen collected_evidence
            jump select_screen
        else:
            $ tamper_tape_selected = True
            $ default_mouse = "tape"
            if viewing_floor:
                if put_swab_in_bag:
                    show screen collected_evidence
                show screen expand_floor_tools
            elif viewing_dish_towel:
                if put_towel_in_bag:
                    show screen collected_evidence
                show screen expand_dish_towel_tools
            elif currently_collecting_fingerprint and not collected_fingerprint:
                if put_print_in_bag:
                    show screen collected_evidence
                show screen expand_stove_tools
            elif at_stove:
                if put_knife_in_bag:
                    hide screen collect_knife_tube
                    show screen collected_evidence
                elif knife_not_ready_to_bag and put_knife_in_tube:
                    hide filled_tube_idle
                    show screen tube_with_knife
                show screen expand_stove_tools
            call screen toolbox

    label floor:
        hide screen kitchen_screen
        scene floor_idle
        $ viewing_floor = True
        hide screen expand_kitchen_tools
        jump select_screen

    label selected_swab:
        if put_swab_in_bag:
            show screen expand_floor_tools
            show screen toolbox
            call screen already_collected_swab
            show screen expand_floor_tools
            call screen toolbox
        if currently_swabbing:
            $ default_mouse = "default"
            $ currently_swabbing = False
            $ swabbing_floor = False
            hide screen swabbing
            show screen kitchen_floor
        else:
            $ currently_swabbing = True
            $ display_clean_swab = True
            hide screen kitchen_floor
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            show screen expand_floor_tools
            call screen toolbox
            
        jump select_screen

    label wet:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if selected_water:
            $ selected_water = False
            $ default_mouse = "default"
            hide screen swabbing
        else:
            $ selected_water = True
            $ default_mouse = "water"
            if currently_swabbing:
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            
        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label collect_swab:
        if holding_swab:
            if not ethanol_applied and not phenolphthalein_applied and not hydrogen_peroxide_applied and properly_swabbed_blood:
                $ properly_swabbed_blood = True
            else:
                $ properly_swabbed_blood = False
            if not properly_swabbed_blood and not warning_swab_message:
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                show screen expand_floor_tools
                show screen toolbox
                call screen incorrect_swab_warning
                $ warning_swab_message = True
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                show screen expand_floor_tools
                call screen toolbox
            if not conducted_kastle_meyer_test:
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                show screen expand_floor_tools
                show screen toolbox
                call screen no_kastle_meyer_test
                show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
                show screen expand_floor_tools
                call screen toolbox
            $ default_mouse = "default"
            $ display_clean_swab = False
            $ display_positive_swab = False
            $ display_swabing_options = False
            $ put_swab_in_tube = True
            $ holding_swab = False
            $ warning_swab_message = False
            hide screen swabbing
            show screen expand_floor_tools
            $ bag_selected = False
            $ delivered_kastle_meyer_message = False
            $ currently_swabbing = False
            show screen packing_swab(bag_selected)
        else:
            show screen expand_floor_tools
        call screen toolbox

    label more_guidance:
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        show screen toolbox
        call screen explain_more
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label throw_out_swab:
        if holding_swab:
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
            $ display_clean_swab = False
            $ display_posiitve_swab = False
            $ display_swabbing_options = False
            $ swabbed_floor = False
            $ holding_swab = False
            $ delivered_kastle_meyer_message = False
            $ warning_swab_message = False
            hide screen swabbing
            jump select_screen
        else:
            show screen expand_floor_tools
            call screen toolbox

    label swabbed_floor:
        $ default_mouse = "default"
        $ swabbing_floor = False
        $ swabbed_floor = True
        $ display_clean_swab = True
        $ display_swabbing_options = True
        $ holding_swab = False
        if wet_swab:
            $ properly_swabbed_blood = True
        show screen toolbox
        call screen swabbed_floor_message
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label place_swab:
        $ default_mouse = "default"
        $ holding_swab = False
        if correct_kastle_meyer_procedure and ethanol_applied and phenolphthalein_applied and hydrogen_peroxide_applied and wet_swab:
            $ display_positive_swab = True 
        else:
            $ display_clean_swab = True
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label pick_up_swab:
        if selected_water:
            $ wet_swab = True
            $ default_mouse = "default"
            $ selected_water = False
        elif ethanol_selected:
            $ ethanol_applied = True
            if phenolphthalein_applied or hydrogen_peroxide_applied or not wet_swab or not swabbed_floor:
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
                $ display_positive_swab = True
                $ conducted_kastle_meyer_test = True
            $ hydrogen_peroxide_selected = False
            $ default_mouse = "default"
        else :
            if not swabbed_floor:
                $ swabbing_floor = True
            else:
                $ swabbing_floor = False

            $ display_clean_swab = False
            $ display_positive_swab = False
            $ default_mouse = "swab"
            $ holding_swab = True
        
        if ethanol_applied and phenolphthalein_applied and hydrogen_peroxide_applied and not correct_kastle_meyer_procedure and not delivered_kastle_meyer_message:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            show screen expand_floor_tools
            show screen toolbox
            $ delivered_kastle_meyer_message = True
            $ conducted_kastle_meyer_test = True
            call screen incorrect_kastle_meyer_procedure

        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label not_sure:
        show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        show screen toolbox
        call screen give_direction
        show screen expand_floor_tools
        call screen toolbox

    label ethanol:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if ethanol_selected:
            $ default_mouse = "default"
            $ ethanol_selected = False
        else:
            $ default_mouse = "pipette"
            $ ethanol_selected = True

        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label phenolphthalein:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if phenolphthalein_selected:
            $ default_mouse = "default"
            $ phenolphthalein_selected = False
        else:
            $ default_mouse = "pipette"
            $ phenolphthalein_selected = True

        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label hydrogen_peroxide:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if hydrogen_peroxide_selected:
            $ default_mouse = "default"
            $ hydrogen_peroxide_selected = False
        else:
            $ default_mouse = "pipette"
            $ hydrogen_peroxide_selected = True

        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
        show screen expand_floor_tools
        call screen toolbox

    label spray_bottle:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if put_swab_in_tube or put_swab_in_bag:
            show screen toolbox
            call screen finish_collecting
            show screen expand_floor_tools
            call screen toolbox
        if not collected_swab:
            show screen toolbox
            call screen collect_swab_first
            show screen expand_floor_tools
            call screen toolbox
        if currently_swabbing:
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            show screen expand_floor_tools
            show screen toolbox
            call screen cannot_use_now
            show screen swabbing(swabbing_floor, display_clean_swab, display_positive_swab)
            show screen expand_floor_tools
            call screen toolbox
        if spray_bottle_selected:
            $ spray_bottle_selected = False
            hide screen luminol
        else:
            $ spray_bottle_selected = True
            show screen luminol(only_water, luminol_ready)
            show screen expand_floor_tools
            call screen toolbox

        jump select_screen

    label luminol_packet:
        if holding_swab:
            show screen toolbox
            call screen currently_holding_swab
            show screen expand_floor_tools
            call screen toolbox
        if selected_luminol_packet:
            $ selected_luminol_packet = False
            $ default_mouse = "default"
        else:
            $ selected_luminol_packet = True
            $ default_mouse = "luminol"
        
        show screen expand_floor_tools
        call screen toolbox

    label selected_bottle:
        if selected_water:
            $ selected_water = False
            $ default_mouse = "default"
            $ only_water = True
            $ added_water_to_bottle = True
            if added_water_to_bottle and added_packet_to_bottle:
                $ luminol_ready = True
            show screen luminol(only_water, luminol_ready)
        elif selected_luminol_packet:
            $ default_mouse = "default"
            $ only_water = False
            $ added_packet_to_bottle = True
            $ selected_luminol_packet = False
            if added_water_to_bottle and added_packet_to_bottle:
                $ luminol_ready = True
            show screen luminol(only_water, luminol_ready)
        elif luminol_ready:
            hide screen luminol
            $ default_mouse = "spray"
            scene dark_floor
            show screen spraying_luminol
        
        show screen expand_floor_tools
        call screen toolbox

    label spray_luminol:
        $ number_of_sprays = number_of_sprays + 1

        if number_of_sprays == 3:
            $ default_mouse = "default"
            hide screen spraying_luminol
            hide screen kitchen_floor
            hide screen expand_floor_tools
            scene luminol_floor
            call screen capture_luminol
        else: 
            scene dark_floor
            show screen spraying_luminol
            show screen expand_floor_tools
            call screen toolbox

    label took_picture:
        $ captured_luminol = True
        $ number_of_sprays = 0
        $ only_water = False
        $ luminol_ready = False
        $ spray_bottle_selected = False
            
        jump select_screen