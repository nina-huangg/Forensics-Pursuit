# initial screen
screen lab_hallway_screen:
    image "lab_hallway_dim"
    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            hovered Notify("Data Analysis Lab")
            unhovered Notify('')
            action Jump('data_analysis_lab')
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            hovered Notify("Materials Lab")
            unhovered Notify('')
            action Jump('materials_lab')

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "afis_software_idle"
            hover "afis_software_hover"
            action Jump('afis')

screen afis_screen:
    default afis_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    image afis_bg

    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleLocalVariable('interface_import'),
                Show("inventory"), Hide("toolbox"),
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
                Function(calculate_afis, current_evidence),
                Function(set_cursor, '')]
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            
            ## add in sensitive when clicked on evidence 


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

    

    
#################################### MATERIALS ####################################
screen materials_lab_screen:
    image "materials_lab"

    hbox:
        xpos 0.15 yalign 0.5
        imagebutton:
            idle "fumehood_idle" at Transform(zoom=0.8)
            hover "fumehood_hover"
            hovered Notify("Fume Hood")
            unhovered Notify('')
            action Jump('fumehood')
    hbox:
        #xpos 0.4 yalign 0.5
        xpos 0.32 yalign 0.5
        imagebutton:
            idle "fingerprint_development_idle" at Transform(zoom=0.8)
            hover "fingerprint_development_hover"
            hovered Notify("Fingerprint Development")
            unhovered Notify('')
            action NullAction()
    
    hbox:
        #xpos 0.4 yalign 0.5
        xpos 0.48 yalign 0.53
        imagebutton:
            idle "lab_bench_idle" at Transform(zoom=0.8)
            hover "lab_bench_hover"
            hovered Notify("Lab Bench")
            unhovered Notify('')
            action NullAction()
    
    hbox:
        xpos 0.62 yalign 0.5
        imagebutton:
            idle "analytical_instruments_idle"
            hover "analytical_instruments_hover"
            hovered Notify("Analytical Instruments")
            unhovered Notify('')
            action Jump('analytical_instruments')

screen fumehood_screen:
    image "fumehood"

screen analytical_instruments_screen:
    image "lab_bench"