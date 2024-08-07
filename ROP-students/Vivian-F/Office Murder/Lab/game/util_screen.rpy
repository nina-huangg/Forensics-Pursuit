
# To jump to label (currenly only to hallway and fumehood_lab)
screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [SetVariable('process_fumehood', False), SetVariable('process_afis', False), SetVariable('importing', False), Hide('afis_screen'), Jump(location)]
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
    

# current_casefile, set_current_casefile, casefile_title, type_case, case_type_selected, bool_show_case
# screen show_case
# Align things

transform evidence_small():
    zoom 0.2

# Digital Evidence        
screen digital_screen():
    showif show_digital:
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.5 ypos 0.2
            text("Physical Evidence")
        hbox:
            xpos 0.25 ypos 0.2
            textbutton('Close'):
                style "back_button" 
                action [SetVariable("show_digital", False)]
        
        # Bullet only shows after fumehood process, and no print to afis
        showif evidence_complete_process['gun_blue']:
            hbox:
                xpos 0.31 ypos 0.6
                image "bullet_print" at evidence_small
            hbox:
                xpos 0.29 ypos 0.82
                text 'No complete print to process'
        
        # Cheque show after fumehood and can compare in afis
        showif evidence_complete_process['ninhydrin']:
            hbox:
                xpos 0.61 ypos 0.3
                image "cheque_print" at evidence_small
            # Before afis compared, show needing comparison and allow button if in afis scene
            showif not cheque.afis_processed:
                showif importing:
                    hbox:
                        xpos 0.61 ypos 0.52
                        textbutton('Process fingerprint'):
                            style "custom_button"
                            action [SetVariable('importing', False), Function(set_cursor, 'cheque_fingerprint'), SetVariable('current_evidence', cheque), SetVariable('show_digital', False)]
                else:
                    hbox:
                        xpos 0.58 ypos 0.52
                        text 'Requires comparison analysis' color "#1f1da7"
            # After afis searched, show text to reflect
            else:
                hbox:
                    xpos 0.61 ypos 0.52
                    text 'Fingerprint searched' 

        # Deskfoot default shows, can compare in afis
        showif not deskfoot.afis_processed:
            hbox:
                xpos 0.3 ypos 0.3
                image "casefile_deskfoot" at evidence_small
            showif importing:
                hbox:
                    xpos 0.32 ypos 0.52
                    textbutton('Process footprint'):
                        style "custom_button"
                        action [SetVariable('importing', False), Function(set_cursor, 'deskfoot_footprint'), SetVariable('current_evidence', deskfoot), SetVariable('show_digital', False)]
            else:    
                hbox:
                    xpos 0.27 ypos 0.52
                    text 'Requires comparison analysis' color "#1f1da7"    
        else:
            hbox:
                xpos 0.3 ypos 0.3
                image "casefile_deskfoot" at evidence_small
            hbox:
                xpos 0.32 ypos 0.52
                text 'Footprint searched'

        # Carpet default shows, cannot be processed in afis  
        hbox:
            xpos 0.6 ypos 0.6
            image "casefile_blood" at evidence_small
        hbox:
            xpos 0.59 ypos 0.82
            text 'No visible print to process'


# Physical Evidence -- need position adjust according to digital
screen physical_screen():
    showif show_physical:
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.5 ypos 0.2
            text("Physical Evidence")
        hbox:
            xpos 0.25 ypos 0.2
            textbutton('Close'):
                style "back_button" 
                action [SetVariable('show_physical', False)]
        
        # Bullet without gun blue - image same as eivdence collection
        #   Then if in fumehood scene, allow process button, if not just text         
        showif not evidence_complete_process['gun_blue']:
            hbox:
                xpos 0.3 ypos 0.6
                image "casefile_bullet" at evidence_small
            showif process_fumehood:
                hbox:
                    xpos 0.3 ypos 0.82
                    textbutton('Process bullet casing'):
                        style "custom_button"
                        action [SetVariable('current_evidence', bullet), SetVariable("show_physical", False), Hide('fumehood_idle'), Jump('process_prompt')]
            else:
                hbox:
                    xpos 0.27 ypos 0.82
                    text 'Requires further processing' color "#1f1da7"
        # Bullet after gun blue - image from photo
        else:
            hbox:
                xpos 0.3 ypos 0.6
                image "casefile_bullet_processed" at evidence_small
            hbox:
                xpos 0.3 ypos 0.82
                text 'Bullet casing processed'

        # Cheque - same format as bullet
        showif not evidence_complete_process['ninhydrin']:
            hbox:
                xpos 0.6 ypos 0.3
                image "casefile_cheque" at evidence_small
            showif process_fumehood:
                hbox:
                    xpos 0.61 ypos 0.52
                    textbutton('Process cheque'):
                        style "custom_button"
                        action [SetVariable('current_evidence', cheque), SetVariable("show_physical", False), Hide('fumehood_idle'), Jump('process_prompt')]
            else:
                hbox:
                    xpos 0.58 ypos 0.52
                    text 'Requires further processing' color "#1f1da7"                               
        else:
            hbox:
                xpos 0.61 ypos 0.3
                image "casefile_cheque_processed" at evidence_small 
            hbox:
                xpos 0.62 ypos 0.52
                text 'Cheque processed'

        # Footprint on desk 
        hbox:
            xpos 0.3 ypos 0.3
            image "casefile_deskfoot" at evidence_small
        hbox:
            xpos 0.28 ypos 0.52
            text 'Footprint processed (KNAAP)'
        
        # Carpet
        hbox:
            xpos 0.6 ypos 0.6
            image "casefile_blood" at evidence_small
        hbox:
            xpos 0.59 ypos 0.82
            text 'Bloody carpet processed\n(Hungarian Red)'