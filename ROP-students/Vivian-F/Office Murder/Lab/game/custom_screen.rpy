screen screen_finished_processing(evidence):
    hbox:
        xpos 0.25 ypos 0.8
        textbutton('Store in case file'):
            style "custom_button"
            action [Hide('screen_finished_processing', _layer='over_screens'),
            Hide('case_files_screen', _layer='over_screens'), 
            Hide('toolbox_button_screen', _layer='over_screens'), 
            Hide('back_button_screen', _layer='over_screens'),
            Function(set_state_to_processed, current_process), 
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
    showif not (show_case_files or bool_show_case or bool_show_case_evidence or bool_show_case_digi or bool_show_case_report):
        hbox:
            xpos 0.20 yalign 0.5
            imagebutton:
                idle "data_analysis_lab_idle"
                hover "data_analysis_lab_hover"
                hovered Notify("Data Analysis Lab")
                unhovered Notify('')     
                action Jump("data_analysis_lab")
        hbox:
            xpos 0.55 yalign 0.48
            imagebutton:
                idle "materials_lab_idle"
                hover "materials_lab_hover"
                hovered Notify("Materials Lab")
                unhovered Notify('')
                action Jump("materials_lab")

# Data Lab -- AFIS
screen data_analysis_lab_screen:
    image "afis_interface"
    showif not (show_case_files or bool_show_case or bool_show_case_evidence or bool_show_case_digi or bool_show_case_report):
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
    showif not (show_case_files or bool_show_case or bool_show_case_evidence or bool_show_case_digi or bool_show_case_report):
        hbox:
            xpos 0.35 ypos 0.145
            textbutton('Import'):
                style "afis_button"
                action [
                    ToggleLocalVariable('interface_import'),
                    ToggleVariable('show_case_files'),
                    SetLocalVariable('interface_imported', False),
                    SetLocalVariable('interface_search', False),
                    SetLocalVariable('afis_bg', 'software_interface'),
                    Function(set_cursor, '')]
        hbox:
            xpos 0.55 ypos 0.145
            textbutton('Search'):
                sensitive not interface_search
                style "afis_button"
                action [
                    ToggleLocalVariable('interface_search'),
                    SetLocalVariable('afis_bg', 'software_search'),
                    Function(set_cursor, '')]
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            hotspot (282,241,680,756) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                Function(set_cursor, ''),
                Function(add_afis, current_evidence)]
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
                        text("{color=#000000}"+afis_search[i].name+"{/color}")
                hbox:
                    xpos afis_search_coordinates['score_xpos'] ypos afis_search_coordinates['ypos']+(i*0.04)
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['score']+"{/color}")        
        else:
            hbox:
                xpos 0.57 yalign 0.85
                hbox:
                    text("{color=#000000}No match found in records.{/color}")





screen gloves():
    imagebutton:
        xalign 0.5
        yalign 0.5
        idle "gloves_box_idle"
        hover "gloves_box_hover"
        action Jump("fumehood_pick")

screen materials_lab_screen:
    image "materials_lab"
    showif not (show_case_files or bool_show_case or bool_show_case_evidence or bool_show_case_digi or bool_show_case_report):
        hbox:
            xpos 0.15 yalign 0.5
            imagebutton:
                idle "wet_lab_idle"
                hover "wet_lab_hover"
                hovered Notify("Fumehood")
                unhovered Notify('')
                action [Jump('fumehood_lab')]
        hbox:
            xpos 0.4 yalign 0.5
            imagebutton:
                idle "fingerprint_development_idle"
                hover "fingerprint_development_hover"
                hovered Notify("Cyanoacrylate Chamber")
                unhovered Notify('')
                action NullAction()
        
        hbox:
            xpos 0.62 yalign 0.5
            imagebutton:
                idle "analytical_instruments_idle"
                hover "analytical_instruments_hover"
                hovered Notify("Analytical Instruments")
                unhovered Notify('')
                action NullAction()

screen fumehood_screen():
    image "fumehood_bg"
    showif not (show_case_files or bool_show_case or bool_show_case_evidence or bool_show_case_digi or bool_show_case_report):
        imagemap:
            xpos 0.0 ypos 0.0
            idle "fumehood_bg"
            hotspot(130,100,1230,880) action [SetVariable('current_process', 'gun_blue'), Function(set_cursor, ''), Show('gun_blue_screen')] sensitive current_evidence == bullet
            hotspot(130,100,1230,880) action [SetVariable('current_process', 'ninhydrin'), Function(set_cursor, ''), Show('ninhydrin_screen')] sensitive current_evidence == cheque
    

screen gun_blue_screen:
    # Note: will not reach here if process already done
    # Ratio mistake tbi
    default bottle_placed = False
    default water_poured = False
    default gb_poured = False
    default bullet_picked = False
    default dipped_gb = False
    default lift_gb = False
    default dipped_water = False
    default lift_water = False
    default to_photo = False
    default macro = False

    imagemap:
        idle "bullet_placed"
        hover "bullet_placed_hover"
        hotspot(130,100,1230,880) action [SetLocalVariable('bottle_placed', True)] sensitive tools['bottle']
    showif bottle_placed:
        imagemap:
            idle "bottle_placed_zoom"
            hover "bottle_placed_zoom_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('water_poured', True)] sensitive tools['water']
    showif water_poured:
        imagemap:
            idle "bottle_water"
            hover "bottle_water_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('gb_poured', True), Function(set_tool, 'gun_blue')] sensitive tools['gun_blue']
    showif gb_poured:
        image "bottle_gb"
        imagebutton:
            xpos 300 ypos 450
            idle "bullet_photo_mouse" at Transform(zoom=8)
            hovered Notify("Pick up bullet with tweezer")
            unhovered Notify('')     
            action [Function(set_cursor, 'tweezer_bullet'), SetLocalVariable('bullet_picked', True)]
    showif bullet_picked:
        imagemap:
            idle "bottle_gb"
            hover "bottle_gb_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('dipped_gb', True)]
    showif dipped_gb:
        imagemap:
            idle "bullet_dip_gb"
            hover "bullet_dip_gb_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('lift_gb', True)]
    showif lift_gb:
        imagemap:
            idle "bullet_lift_gb"
            hover "bullet_lift_gb_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('dipped_water', True)]
    showif dipped_water:
        imagemap:
            idle "bullet_dip_water"
            hover "bullet_dip_water_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('lift_water', True), Function(set_cursor, '')]
    showif lift_water:
        image "bullet_lift_water"
        hbox:
            xpos 0.25 ypos 0.8
            textbutton('Set up for photo (white background, evidence clipped\nto stand with ruler on side)'):
                style 'custom_button'
                action [SetLocalVariable('to_photo', True)]
    showif to_photo:
        image 'bullet_ruler'
        hbox:
            xpos 0.25 ypos 0.8
            textbutton('Change camera to macro lens to better photograph the print'):
                style 'custom_button'
                action [SetLocalVariable('macro', True)]
    showif macro:
        image 'bullet_ruler'
        image 'bullet_print' at Transform(zoom=0.5, xalign=0.5, yalign=0.45)
        hbox:
            xpos 0.25 ypos 0.8
            textbutton('Take photo (this will be your digital evidence)'):
                style 'custom_button'
                action [Hide('gun_blue_screen'), Jump('take_bullet')]

screen gun_blue_tobag:
    default bagged = False
    default taped = False
    imagemap:
        idle "bullet_ruler"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "bin_bagged"
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='bullet',_layer='over_screens')] sensitive tools['tape']
    showif taped:
        image 'bin_taped'


screen ninhydrin_screen:
    # Note: will not reach here if process already done
    default poured = False
    default to_dip = False
    default dipped = False
    default lift = False
    default choice = False
    default dry = False
    default humidified = False
    default at_cabinet = False
    default opened = False
    default placed = False
    default setting = False
    default wait = False
    default takeout = False
    default to_photo = False

    imagemap:
        idle "cheque_placed"
        hover "cheque_placed_hover"
        hotspot(130,100,1230,880) action [SetLocalVariable('poured', True), Function(set_tool, 'ninhydrin')] sensitive tools['ninhydrin']
    showif poured:
        imagemap:
            idle "cheque_ninhydrin"
            hover "cheque_ninhydrin_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('to_dip', True), Function(set_cursor, 'cheque_mouse')]
    showif to_dip:
        imagemap:
            idle "cheque_pickup"
            hover "cheque_pickup_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('dipped', True), Function(set_cursor, '')]
    showif dipped:
        imagemap:
            idle "cheque_dipped"
            hover "cheque_dipped_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('lift', True), Function(set_cursor, 'tray_cheque')]
    showif lift:
        image "cheque_pickup"
        imagebutton:
            xpos 1100 ypos 70
            idle "cabinet" at Transform(zoom=0.5)
            hovered Notify("Proceed to the heated cabinets")
            unhovered Notify('')     
            action [SetLocalVariable('choice', True), Function(set_cursor, '')]
    showif choice:
        image 'cheque_pickup'
        hbox:
            xpos 1100 ypos 70
            image "cabinet" at Transform(zoom=0.5)
        hbox:
            xpos 0.15 ypos 0.6
            textbutton('Dry'):
                style 'custom_button'
                action SetLocalVariable('dry', True)
        hbox:
            xpos 0.15 ypos 0.7
            textbutton('Humidified'):
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
            hotspot(130,100,1230,880) action [SetLocalVariable('opened', True), Function(set_cursor, 'tray_cheque')]
    showif opened:
        imagemap:
            idle "cabinet_open"
            hover "cabinet_open_hover"
            hotspot(130,100,1230,880) action [SetLocalVariable('placed', True), Function(set_cursor, '')]
    showif placed:
        image 'cabinet_placed'
        hbox:
            xpos 0.2 ypos 0.75
            textbutton('Set temperature to 80 degrees celcius with 65%\ relative humidity'):
                style 'custom_button'
                action [SetLocalVariable('setting', True)]
    showif setting:
        image 'cabinet_humidified'
        hbox:
            xpos 0.2 ypos 0.75
            textbutton('Wait for 5 minutes'):
                style 'custom_button'
                action [SetLocalVariable('wait', True)]
    showif wait:
        image 'cabinet_done'
        hbox:
            xpos 0.2 ypos 0.75
            textbutton('Set up exhibit behind white background for photograph'):
                style 'custom_button'
                action [SetLocalVariable('takeout', True)]
    showif takeout:
        image 'ninhydrin_take_photo'
        hbox:
            xpos 0.2 ypos 0.8
            textbutton('Take Photo'):
                style 'custom_button'
                action [Hide('ninhydrin_screen'), Jump("take_cheque")]
    
screen ninhydrin_tobag:
    default bagged = False
    default taped = False
    imagemap:
        idle "ninhydrin_tophoto"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "bin_bagged"
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='cheque',_layer='over_screens')] sensitive tools['tape']
    showif taped:
        image 'bin_taped'
