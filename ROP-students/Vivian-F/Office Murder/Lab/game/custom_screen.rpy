screen screen_finished_processing(evidence):
    hbox:
        xpos 0.15 ypos 0.85
        textbutton('Store in case file'):
            style "custom_button"
            action [Hide('screen_finished_processing', _layer='over_screens'),
            Hide('case_files_screen', _layer='over_screens'), 
            Hide('toolbox_button_screen', _layer='over_screens'), 
            Hide('back_button_screen', _layer='over_screens'),
            Function(set_state_to_processed, current_evidence), 
            Function(set_current_evidence, ''),
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
                idle "data_lab_button_idle"
                hover "data_lab_button_hover"
                hovered Notify("Data Analysis Lab")
                unhovered Notify('')     
                action Jump("data_analysis_lab")
        hbox:
            xpos 0.234 yalign 0.628
            hbox:
                text("{size=-6}Data Analysis Lab{/size}")
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
                action Jump('afis')    
    # imagemap:
    #     idle "afis_workstation_idle"
    #     hover "afis_workstation_hover"
    #     hotspot (473,207,975,513) action [Function(set_state_to_processed, current_evidence), Function(set_cursor, ''), 
    #     Return()] sensitive current_cursor =='bullet' or current_cursor=='cheque' or current_cursor=='deskfoot' or current_cursor=='blood'
 
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
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    showif interface_search:
        if afis_search:
            for i in range(len(afis_search)):
                hbox:
                    xpos afis_search_coordinates[i]['xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].name+"{/color}")
                hbox:
                    xpos afis_search_coordinates[i]['score_xpos'] ypos afis_search_coordinates[i]['ypos']
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
            hotspot(130,100,1230,880) action [Show('gun_blue_screen')] sensitive 'current_evidence' == bullet
            hotspot(130,100,1230,880) action [Show('ninhydrin_screen')] sensitive 'current_evidence' == cheque
    

screen gun_blue_screen:
    # Note: will not reach here if process already done
    # Ratio mistake tbi
    default bottle_placed = False
    # default gb_poured = False
    # default water_under = False
    # default water_good = False
    # default water_over = False
    default dipped = False
    # default dipped_gb = False
    # default dipped_water = False
    ## default bin_clipped = False
    ## default rulered = False
    default set_up = False

    imagemap:
        idle "fumehood_bg"
        hotspot(130,100,1230,880) action [SetLocalVariable('bottle', True), Function(set_tool, 'bottle')] sensitive tools['bottle']
    showif bottle_placed:
        image "gb_bottle"
        hbox:
            xpos 0.25 ypos 0.8
            textbutton('Gun Blue process'):
                style 'custom_button'
                action [SetLocalVariable('dipped', True)]
    showif dipped:
        image "gb_done"
        hbox:
            xpos 0.25 ypos 0.8
            textbutton('Set up for photo (white background with ruler next to evidence)'):
                style 'custom_button'
                action [SetLocalVariable('set_up', True)]
    showif set_up:
        image 'bullet_print_photo'
        hbox:
            xpos 0.15 ypos 0.85
            textbutton('Take Photo'):
                style 'custom_button'
                action [Jump("take_bullet")]
    
screen gun_blue_tobag:
    default bagged = False
    default taped = False
    imagemap:
        idle "bullet_print_photo"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "bin_bagged"
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='bullet',_layer='over_screens')] sensitive tools['tape']
            # Overwrite current evidence before return to main screen 
    showif taped:
        image 'bin_taped'


screen ninhydrin_screen:
    # Note: will not reach here if process already done
    # default tray_placed = False
    # default picked = False
    # default sprayed = False
    # default kettle_placed = False
    default dried = False
    ## default bin_placed = False
    ## default rulered = False
    default set_up = False

    # imagemap:
    #     idle "fumehood_bg"
    #     hotspot(130,100,1230,880) action [SetLocalVariable('tray_placed', True)] sensitive tools['tray']
    
    # showif dried:
    image "ninhydrin_done"
    hbox:
        xpos 0.25 ypos 0.8
        textbutton('Set up for photo (white background with ruler next to evidence)'):
            style 'custom_button'
            action [SetLocalVariable('set_up', True), Function(set_cursor, '')]
    showif set_up:
        image 'cheque_print_photo'
        hbox:
            xpos 0.15 ypos 0.85
            textbutton('Take Photo'):
                style 'custom_button'
                action [Jump("take_cheque")]
    
screen ninhydrin_tobag:
    default bagged = False
    default taped = False
    imagemap:
        idle "cheque_print_photo"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "bin_bagged"
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='cheque',_layer='over_screens')] sensitive tools['tape']
            # Overwrite current evidence before return to main screen 
    showif taped:
        image 'bin_taped'


screen show_consistency():
    image("consistency_result_afis")
    hbox:
        xalign 0.51 yalign 0.42
        text"80% consistency found\nbetween the fingerprints!"