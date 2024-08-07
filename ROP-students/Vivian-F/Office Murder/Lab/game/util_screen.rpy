
# To jump to label (currenly only to hallway and fumehood_lab)
screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [SetVariable('process_fumehood', False), SetVariable('process_afis', False), Hide('afis_screen'), Jump(location)]
            sensitive current_cursor == ''

# Rollback to last step (last screen or label) -- cannot use if disable rollback
screen backtrack():
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action Rollback()
            sensitive current_cursor == ''
    

# Casefile
transform case_evidence:
    zoom 0.2

screen case_files_screen():
    showif show_case_files:
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.5 ypos 0.2
            text("Case Files")
        hbox:
            xpos 0.25 ypos 0.2
            textbutton('Close'):
                style "back_button" 
                action [SetVariable('show_case_files', False)]
        
        hbox:
            xpos 0.3 ypos 0.62
            imagebutton:
                idle "casefile_bullet" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'bullet'), 
                SetVariable("bool_show_case", True), Show("show_case", name='Bullet Casing', _layer="over_screens")]
        hbox:
            xpos 0.6 ypos 0.34
            imagebutton:
                idle "casefile_cheque" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'cheque'),
                SetVariable("bool_show_case", True), Show("show_case", name='Cheque', _layer="over_screens")]
        hbox:
            xpos 0.3 ypos 0.34
            imagebutton:
                idle "casefile_deskfoot" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'deskfoot'),
                SetVariable("bool_show_case", True), Show("show_case", name='KNAAP Footprint', _layer="over_screens")]
        hbox:
            xpos 0.6 ypos 0.62
            imagebutton:
                idle "casefile_blood" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'blood'),
                SetVariable("bool_show_case", True), Show("show_case", name='Bloody Carpet', _layer="over_screens")]


# Options for physical/digital casefile type_case 
# Each set current_casefile[type_case] to True and make case_type_selected = type_case
# then deselect bool_show_case before leaving this screen
# set show_physical to True in prep of new screen
# then show new screen show_case_evidence given current process to be sensitive to
screen show_case(name):
    showif bool_show_case:
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.46 ypos 0.2
            text(name)
        hbox:
            xpos 0.3 ypos 0.2
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', False), SetVariable('show_case_files', True)]
        hbox:
            xpos 0.3 ypos 0.35
            imagebutton:
                idle "casefile_evidence" at Transform(zoom=0.4)
                hover "casefile_evidence_hover"
                action [Function(set_current_casefile, 'evidence'), SetVariable("bool_show_case", False),
                SetVariable('show_physical', True), Show("show_case_evidence", _layer="over_screens")]
        hbox:
            xpos 0.32 ypos 0.65
            text("{size=-5}Physical Evidence{/size}")
    
        hbox:
            xpos 0.5 ypos 0.32
            imagebutton:
                idle "casefile_digi_evidence" at Transform(zoom=0.5)
                hover "casefile_digi_evidence_hover"
                action [Function(set_current_casefile, 'digi_evidence'), SetVariable("bool_show_case", False),
                SetVariable('show_digital', True), Show('show_case_digi_evidence', _layer="over_screens")]
        hbox:
            xpos 0.55 ypos 0.65
            text("{size=-5}Digital Evidence{/size}")


transform evidence_small():
    zoom 0.2

# Physical Evidence
screen show_case_evidence():
    showif show_physical:
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.3 ypos 0.2
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("show_physical", False)]
        hbox:
            xpos 0.46 ypos 0.2
            text(case_type_selected)

        if case_file_dict['bullet']:
            showif not evidence_complete_process['gun_blue']:
                showif process_fumehood:
                    hbox:
                        xpos 0.55 ypos 0.5
                        textbutton('Process bullet casing'):
                            style "custom_button"
                            action [SetVariable('current_evidence', bullet), SetVariable("show_physical", False), Hide('fumehood_idle'), Jump('process_prompt')]
                else:
                    hbox:
                        xpos 0.55 ypos 0.5
                        text 'Requires further processing' color "#1f1da7"
                hbox:
                    xalign 0.4 yalign 0.5
                    image "casefile_bullet" at evidence_small
            else:
                hbox:
                    xpos 0.55 ypos 0.5
                    text 'Bullet casing processed'
                hbox:
                    xalign 0.4 yalign 0.5
                    image "casefile_bullet_processed" at evidence_small
        
        if case_file_dict['cheque']:
            showif not evidence_complete_process['ninhydrin']:
                showif process_fumehood:
                    hbox:
                        xpos 0.55 ypos 0.5
                        textbutton('Process cheque'):
                            style "custom_button"
                            action [SetVariable('current_evidence', cheque), SetVariable("show_physical", False), Hide('fumehood_idle'), Jump('process_prompt')]
                else:
                    hbox:
                        xpos 0.55 ypos 0.5
                        text 'Requires further processing' color "#1f1da7"                           
                hbox:
                    xalign 0.4 yalign 0.5
                    image "casefile_cheque" at evidence_small
            else:
                hbox:
                    xpos 0.55 ypos 0.5
                    text 'Cheque processed'
                hbox:
                    xalign 0.4 yalign 0.5
                    image "casefile_cheque_processed" at evidence_small
        
        if case_file_dict['deskfoot']:
            hbox:
                xpos 0.54 ypos 0.5
                text 'Footprint processed (KNAAP)'
            hbox:
                xalign 0.4 yalign 0.5
                image "casefile_deskfoot" at evidence_small

        if case_file_dict['blood']:
            hbox:
                xpos 0.55 ypos 0.5
                text 'Bloody carpet processed\n(Hungarian Red)'
            hbox:
                xalign 0.4 yalign 0.5
                image "casefile_blood" at evidence_small

# Digital Evidence        
screen show_case_digi_evidence():
    showif show_digital:
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.3 ypos 0.2
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("show_digital", False)]
        hbox:
            xpos 0.46 ypos 0.2
            text(case_type_selected)
        
        if case_file_dict['bullet']:
            showif evidence_complete_process['gun_blue']:
                hbox:
                    xpos 0.55 ypos 0.5
                    text 'No visible complete print to process'
                hbox:
                    xalign 0.4 yalign 0.5
                    image "bullet_print" at evidence_small
        
        if case_file_dict['cheque']:
            showif evidence_complete_process['ninhydrin']:
                showif not cheque.afis_processed:
                    showif process_afis:
                        hbox:
                            xpos 0.55 ypos 0.5
                            textbutton('Process fingerprint'):
                                style "custom_button"
                                action [Function(set_cursor, 'cheque_fingerprint'), SetVariable('current_evidence', cheque), SetVariable('show_digital', False)]
                    else:
                        hbox:
                            xpos 0.55 ypos 0.5
                            text 'Requires comparison analysis' color "#1f1da7"
                else:
                    hbox:
                        xpos 0.55 ypos 0.5
                        text 'Fingerprint searched'
                hbox:
                    xalign 0.4 yalign 0.5
                    image "cheque_print" at evidence_small

        if case_file_dict['deskfoot']:
            showif not deskfoot.afis_processed:
                hbox:
                    xalign 0.4 yalign 0.5
                    image "casefile_deskfoot" at evidence_small
                showif process_afis:
                    hbox:
                        xpos 0.55 ypos 0.5
                        textbutton('Process footprint'):
                            style "custom_button"
                            action [Function(set_cursor, 'deskfoot_footprint'), SetVariable('current_evidence', deskfoot), SetVariable('show_digital', False)]
                else:    
                    hbox:
                        xpos 0.55 ypos 0.5
                        text 'Requires comparison analysis' color "#1f1da7"    
            else:
                hbox:
                    xpos 0.55 ypos 0.5
                    text 'Footprint searched'
                hbox:
                    xalign 0.4 yalign 0.5
                    image "casefile_deskfoot" at evidence_small
        
        if case_file_dict['blood']:
            hbox:
                xpos 0.55 ypos 0.5
                text 'No visible print to process'
            hbox:
                xalign 0.4 yalign 0.5
                image "casefile_blood" at evidence_small


