screen screen_finished_processing(process):
    hbox:
        xpos 0.25 ypos 0.8
        textbutton('Store in physical evidences'):
            style "custom_button"
            action [Hide('screen_finished_processing', _layer='over_screens'),
            Hide('physical_screen', _layer='over_screens'), 
            Hide('digital_screen', _layer='over_screens'), 
            Hide('toolbox_button_screen', _layer='over_screens'), 
            Hide('backtrack', _layer='over_screens'),
            Hide('back_button_screen', _layer='over_screens'),
            Function(set_state_to_processed, process), 
            SetVariable('current_process', ''), 
            SetVariable('current_evidence', no_evidence),
            SetVariable('process_fumehood', False), 
            SetVariable('process_afis', False),
            Jump('hallway'), Function(set_cursor, '')]
        # do not change order to these!

transform fumehood_zoom:
    zoom 0.12

screen hallway_screen():
    image "lab_hallway_dim"
    showif not (show_physical or show_digital):
        hbox:
            xpos 0.20 yalign 0.5
            imagebutton:
                idle "data_analysis_lab_idle"
                hover "data_analysis_lab_hover"   
                action Jump("data_analysis_lab")
        hbox:
            xpos 0.55 yalign 0.48
            imagebutton:
                idle "materials_lab_idle"
                hover "materials_lab_hover"
                action Jump("materials_lab")
    
        showif evidence_complete_process['gun_blue'] and cheque.afis_processed and deskfoot.afis_processed:
            hbox:
                xpos 0.2 ypos 0.8
                textbutton('All 4 pieces of evidences have completed processing, click to proceed to courtroom'):
                    style "custom_button"
                    action [Jump("end")]
    

# Data Lab -- AFIS
screen data_analysis_lab_screen:
    image "afis_interface"
    showif not (show_physical or show_digital):
        hbox:
            xpos 0.25 yalign 0.25
            imagebutton:
                idle "afis_software_idle"
                hover "afis_software_hover"
                action [SetVariable('process_afis', True), Show('afis_screen')]
    
screen afis_screen:
    default afis_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    
    image afis_bg
    showif not (show_physical or show_digital):
        hbox:
            xpos 0.35 ypos 0.145
            textbutton('Import'):
                style "afis_button"
                action [
                    ToggleLocalVariable('interface_import'),
                    SetLocalVariable('interface_imported', False),
                    SetLocalVariable('interface_search', False),
                    SetLocalVariable('afis_bg', 'software_interface'),
                    SetVariable('importing', True),
                    Function(set_cursor, ''),
                    Hide('toolbox'),
                    SetVariable('show_digital', True),
                    Show('inventory'),
                    Show('digital_screen')]
        hbox:
            xpos 0.55 ypos 0.145
            textbutton('Search'):
                sensitive not interface_search
                style "afis_button"
                action [
                    ToggleLocalVariable('interface_search'),
                    SetLocalVariable('afis_bg', 'software_search'),
                    Function(set_cursor, ''), Function(add_afis, current_evidence)]
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            hotspot (282,241,680,756) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                Function(set_cursor, '')] sensitive current_cursor != ''    
            
    # Note: line under does not work when placed into showif, hence the separate if statement
    if current_evidence != no_evidence:
        showif interface_imported:
            hbox:
                xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
                image current_evidence.afis_details['image']
    showif interface_search:
        if afis_search:
            for i in range(len(afis_search)):
                hbox:
                    xpos afis_search_coordinates['xpos'] ypos afis_search_coordinates['ypos']+(i*0.04)
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['compare']+"{/color}")
                hbox:
                    xpos afis_search_coordinates['score_xpos'] ypos afis_search_coordinates['ypos']+(i*0.04)
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['score']+"{/color}")        
        else:
            hbox:
                xpos 0.57 yalign 0.85
                hbox:
                    text("{color=#000000}No match found in records.{/color}")


screen materials_lab_screen:
    image "materials_lab"
    showif not (show_physical or show_digital):
        hbox:
            xpos 0.36 yalign 0.5
            imagebutton:
                idle "fumehood_idle"
                hover "fumehood_hover"
                action [Jump('fumehood_lab')]
        hbox:
            xpos 0.15 yalign 0.5
            imagebutton:
                idle "cyanoacrylate_chamber_idle"
                action NullAction()
        hbox:
            xpos 0.58 yalign 0.5
            imagebutton:
                idle "analytical_instruments_idle"
                action NullAction()

# Idle screen while in fumehood but player has not chosen an evidence 
# (if without, others screens will jump to each other)
screen fumehood_idle:
    image "fumehood_bg"

# Show evidence that is selected placed on the fumehood table surface
# Unselect first tool that is used and show evidence process screen
screen fumehood_screen():
    default camphor = False
    default magnetic = False
    
    image "fumehood_bg"
    showif not (show_physical or show_digital):
        showif current_evidence == bullet:
            imagemap:
                idle "bullet_placed"
                hover "bullet_placed_hover"
                hotspot(1000,540,700,440) action [Function(set_tool, 'bottle'), Jump('bullet_prep')] sensitive tools['bottle']
        showif current_evidence == cheque:
            image 'cheque_placed'
            frame:
                style_group 'choice'
                xalign 0.5 ypos 0.3
                hbox:
                    text "Which method should we use to develop this evidence?" color "#000000"
            hbox:
                xpos 0.15 ypos 0.4
                textbutton('Camphor smoke'):
                    style 'custom_button'
                    action SetLocalVariable('camphor', True)
            hbox:
                xpos 0.15 ypos 0.5
                textbutton('Magnetic powder'):
                    style 'custom_button'
                    action SetLocalVariable('magnetic', True) 
            hbox:
                xpos 0.15 ypos 0.6
                textbutton('Ninhydrin'):
                    style 'custom_button'
                    action Jump('cheque_prep')          
            showif camphor:
                image 'cheque_placed'
                hbox:
                    xpos 0.15 ypos 0.5
                    textbutton('That is not quite right! Camphor will not work on porous surfaces like paper.\n(click to try again)'):
                        style 'custom_button'
                        action [SetLocalVariable('camphor', False)]
            showif magnetic:
                image 'cheque_placed'
                hbox:
                    xpos 0.15 ypos 0.5
                    textbutton('Nope! Try again! Magnetic powder will not work on porous surfaces like paper.\n(click to try again)'):
                        style 'custom_button'
                        action SetLocalVariable('magnetic', False)    

            
screen gun_blue_screen:
    # Note: will not reach here if process already done
    default water_poured = False

    imagemap:
        idle "bottle_placed_zoom"
        hover "bottle_placed_zoom_hover"
        hotspot(500,360,900,610) action [SetLocalVariable('water_poured', True)] sensitive tools['water']
    showif water_poured:
        imagemap:
            idle "bottle_water"
            hover "bottle_water_hover"
            hotspot(570,400,450,540) action [Show('gun_blue_ten')] sensitive tools['gun_blue']

screen gun_blue_ten:
    imagemap:
        idle "gb_ten"
        hover "gb_ten_hover"
        hotspot(570,400,450,540) action [Show('gun_blue_fifty')] sensitive tools['gun_blue']
    hbox:
        xalign 0.5 ypos 0.8
        textbutton('This makes a 10:90 Gun Blue to water ratio solution.\nClick to proceed if you think this is what you need.'):
            style 'custom_button'
            action [Jump('proceed_ten')]
    
screen gun_blue_fifty:
    imagemap:
        idle "gb_fifty"
        hover "gb_fifty_hover"
        hotspot(570,400,450,540) action [Function(set_cursor, 'gun_blue'), Jump('gun_blue_ninty')] sensitive tools['gun_blue']
    hbox:
        xalign 0.5 ypos 0.8
        textbutton('This makes a 50:50 Gun Blue to water ratio solution.\nClick to proceed if you think this is what you need.'):
            style 'custom_button'
            action [Function(set_cursor, 'gun_blue'), Jump('proceed_fifty')]

screen bullet_dip():
    default bullet_picked = False
    default dipped_gb = False
    default threes = False
    default onemin = False

    image "bottle_gb"
    imagebutton:
        xpos 450 ypos 650
        idle "bullet_photo_mouse" at Transform(zoom=2)   
        action [Function(set_cursor, 'tweezer_bullet'), SetLocalVariable('bullet_picked', True)]
        mouse "tweezer"
    showif bullet_picked:
        imagemap:
            idle "bottle_gb"
            hover "bottle_gb_hover"
            hotspot(570,400,450,540) action [Function(set_cursor, ''), Jump('dip_timer')]

screen bullet_water():
    default lift_gb = False
    default dipped_water = False
    
    imagemap:
        idle "bullet_dip_gb"
        hover "bullet_dip_gb_hover"
        hotspot(570,400,450,540) action [SetLocalVariable('lift_gb', True)]
    showif lift_gb:
        imagemap:
            idle "bullet_lift_gb"
            hover "bullet_lift_gb_hover"
            hotspot(910,400,440,540) action [SetLocalVariable('dipped_water', True)]
    showif dipped_water:
        imagemap:
            idle "bullet_dip_water"
            hover "bullet_dip_water_hover"
            hotspot(910,400,440,540) action [Function(set_cursor, ''), Jump('bullet_to_photo')]

screen bullet_set_photo():
    default macroed = False
    
    image 'bullet_ruler'
    hbox:
        xpos 0.25 ypos 0.8
        textbutton('Change camera to macro lens to better photograph the print'):
            style 'custom_button'
            action [SetLocalVariable('macroed', True)]
    showif macroed:
        image 'bullet_take_photo'
        hbox:
            xpos 0.25 ypos 0.8
            textbutton('Take photo (this will be your digital evidence)'):
                style 'custom_button'
                action [Jump('take_bullet')]

screen gun_blue_tobag:
    default bagged = False
    default taped = False
    imagemap:
        idle "bullet_ruler"
        hover "bullet_ruler_hover"
        hotspot(400,100,1000,880) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "bin_bagged"
            hover "bin_bagged_hover"
            hotspot(400,100,1000,880) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', process='gun_blue', _layer='over_screens')] sensitive tools['tape']
    showif taped:
        image 'bin_taped'


screen ninhydrin_screen:
    # Note: will not reach here if process already done
    default nin = False
    default to_dip = False
    default dipped = False

    imagemap:
        idle "cheque_placed"
        hover "cheque_placed_hover"
        hotspot(320,510,770,490) action [SetLocalVariable('nin', True), Function(set_tool, 'ninhydrin')] sensitive tools['ninhydrin']
    showif nin:
        imagemap:
            idle "cheque_ninhydrin"
            hover "cheque_ninhydrin_hover"
            hotspot(1020,560,630,390) action [SetLocalVariable('to_dip', True), Function(set_cursor, 'cheque_mouse')]
    showif to_dip:
        imagemap:
            idle "cheque_pickup"
            hover "cheque_pickup_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('dipped', True), Function(set_cursor, '')]
    showif dipped:
        imagemap:
            idle "cheque_dipped"
            hover "cheque_dipped_hover"
            hotspot(320,510,770,490) action [Jump('cheque_to_cabinet')]
    
screen ninhydrin_cabinets:
    default choice = False
    default dry = False
    default humidified = False
    default at_cabinet = False
    default opened = False
    default placed = False
    
    image "cheque_pickup"
    imagebutton:
        xpos 1100 ypos 70
        idle "cabinet" at Transform(zoom=0.5)  
        action [SetLocalVariable('choice', True), Function(set_cursor, '')]
    showif choice:
        image 'cheque_pickup'
        hbox:
            xpos 1100 ypos 70
            image "cabinet" at Transform(zoom=0.5)
        hbox:
            xpos 0.2 ypos 0.65
            textbutton('Dry heating cabinet'):
                style 'custom_button'
                action SetLocalVariable('dry', True)
        hbox:
            xpos 0.2 ypos 0.75
            textbutton('Humidified heating cabinet'):
                style 'custom_button'
                action SetLocalVariable('humidified', True)
    showif dry:
        image 'cheque_pickup'
        hbox:
            xpos 0.2 ypos 0.7
            textbutton('That is incorrect, you should place paper evidence in\na humidified heated cabinet to evaporate exccess liquid\n(click to proceed)'):
                style 'custom_button'
                action [SetLocalVariable('at_cabinet', True)]
    showif humidified:
        image 'cheque_pickup'
        hbox:
            xpos 0.2 ypos 0.75
            textbutton('That is correct (click to walk to the cabinet)'):
                style 'custom_button'
                action [SetLocalVariable('at_cabinet', True)]
    showif at_cabinet:
        imagemap:
            idle "cabinet_humidified"
            hover "cabinet_humidified_hover"
            hotspot(350,10,1120,850) action [SetLocalVariable('opened', True), Function(set_cursor, 'tray_cheque')]
    showif opened:
        imagemap:
            idle "cabinet_open"
            hover "cabinet_open_hover"
            hotspot(660,360,760,380) action [SetLocalVariable('placed', True), Function(set_cursor, '')]
    showif placed:
        image 'cabinet_placed'
        hbox:
            xpos 0.2 ypos 0.75
            textbutton('Set temperature to 80 degrees celcius with 65% relative humidity'):
                style 'custom_button'
                action [Hide('ninhydrin_cabinets'), Jump('cabinet_timer')]

screen ninhydrin_set_photo:
    image 'ninhydrin_take_photo'
    hbox:
        xpos 0.2 ypos 0.8
        textbutton('Take Photo'):
            style 'custom_button'
            action [Jump("take_cheque")]
    
screen ninhydrin_tobag:
    default bagged = False
    default taped = False
    imagemap:
        idle "ninhydrin_tophoto"
        hover "ninhydrin_tophoto_hover"
        hotspot(400,400,1200,580) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "bin_bagged"
            hover "bin_bagged_hover"
            hotspot(400,100,1000,880) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', process='ninhydrin', _layer='over_screens')] sensitive tools['tape']
    showif taped:
        image 'bin_taped'
