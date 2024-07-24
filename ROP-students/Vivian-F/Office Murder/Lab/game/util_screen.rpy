
screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [SetVariable('process_fumehood', False), SetVariable('process_afis', False), Jump(location), Hide('afis_screen')]

# Tools      
transform tools_small():
    zoom 0.2

screen toolbox_button_screen:
    hbox:
        xpos 0.02 yalign 0.38
        imagebutton:
            idle "toolbox" at Transform(zoom=0.4)
            hover "toolbox_hover"

            hovered Notify("Toolbox")
            unhovered Notify('')

            action [ToggleVariable("show_toolbox"), Function(set_cursor, '')]
    
    showif show_toolbox:
        # (add?) ruler
        hbox:
            xpos 0.9 ypos 0.05
            imagebutton:
                idle "gun_blue" at tools_small
                hovered Notify("Gun Blue")
                unhovered Notify('')
                action Function(set_tool, 'gun_blue')
        hbox:
            xpos 0.9 ypos 0.2
            imagebutton:
                idle "water_idle" at tools_small
                hovered Notify("Distilled Water")
                unhovered Notify('')
                action Function(set_tool, 'water')
        hbox:
            xpos 0.9 ypos 0.35
            imagebutton:
                idle "bottle" at tools_small
                hovered Notify("Clean Bottle")
                unhovered Notify('')
                action Function(set_tool, 'bottle')
        hbox:
            xpos 0.9 ypos 0.5
            imagebutton:
                idle "ninhydrin" at tools_small
                hovered Notify("Ninhydrin")
                unhovered Notify('')
                action Function(set_tool, 'ninhydrin')
        hbox:
            xpos 0.9 ypos 0.65
            imagebutton:
                idle "bag_idle" at tools_small
                hovered Notify("Evidence Bag")
                unhovered Notify('')
                action Function(set_tool, 'bag')
        hbox:
            xpos 0.9 ypos 0.78
            imagebutton:
                idle "tape_idle" at tools_small
                hovered Notify("Evidence Tape")
                unhovered Notify('')
                action Function(set_tool, 'tape')


# Casefile
transform case_evidence:
    zoom 0.2

screen case_files_screen():
    hbox:
        xpos 0.005 yalign 0.12
        imagebutton:
            idle "casefile_idle" at Transform(zoom=0.45)
            hover "casefile_hover"

            hovered Notify("Case Files")
            unhovered Notify('')

            action ToggleVariable('show_case_files')
    
    showif show_case_files:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xalign 0.5 ypos 0.1
            text("Case Files")
        
        hbox:
            xpos 0.25 ypos 0.20
            imagebutton:
                idle "casefile_bullet" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'bullet'), 
                SetVariable("bool_show_case", True), Show("show_case", name='Bullet Casing', _layer="over_screens")]
        hbox:
            xpos 0.55 ypos 0.20
            imagebutton:
                idle "casefile_cheque" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'cheque'),
                SetVariable("bool_show_case", True), Show("show_case", name='Cheque', _layer="over_screens")]
        hbox:
            xpos 0.25 ypos 0.50
            imagebutton:
                idle "casefile_deskfoot" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'deskfoot'),
                SetVariable("bool_show_case", True), Show("show_case", name='KNAAP Footprint', _layer="over_screens")]
        hbox:
            xpos 0.55 ypos 0.50
            imagebutton:
                idle "casefile_blood" at case_evidence
                action [ToggleVariable('show_case_files'), Function(set_case_file_dict, 'blood'),
                SetVariable("bool_show_case", True), Show("show_case", name='Bloody Carpet', _layer="over_screens")]

# Options for physical/digital/report casefile type_case 
# Each set current_casefile[type_case] to True and make case_type_selected = type_case
# then deselect bool_show_case before leaving this screen
# set bool_show_case_evidence to True in prep of new screen
# then show new screen show_case_evidence given current process to be sensitive to
screen show_case(name):
    showif bool_show_case:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xalign 0.5 ypos 0.1
            text(name)
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', False), SetVariable('show_case_files', True)]
        hbox:
            xpos 0.20 ypos 0.20
            imagebutton:
                idle "casefile_evidence" at Transform(zoom=0.4)
                hover "casefile_evidence_hover"

                action [Function(set_current_casefile, 'evidence'), SetVariable("bool_show_case", False),
                SetVariable('bool_show_case_evidence', True), Show("show_case_evidence", _layer="over_screens")]
        hbox:
            xpos 0.22 ypos 0.47
            text("{size=-5}Physical Evidence{/size}")
    
        hbox:
            xpos 0.37 ypos 0.15
            imagebutton:
                idle "casefile_digi_evidence" at Transform(zoom=0.5)
                hover "casefile_digi_evidence_hover"

                action [Function(set_current_casefile, 'digi_evidence'), SetVariable("bool_show_case", False),
                SetVariable('bool_show_case_digi', True), Show('show_case_digi_evidence', _layer="over_screens")]
        hbox:
            xpos 0.42 ypos 0.47
            text("{size=-5}Digital Evidence{/size}")

        hbox:
            xpos 0.58 ypos 0.18
            imagebutton:
                idle "casefile_report" at Transform(zoom=0.5)
                hover "casefile_report_hover"

                action [Function(set_current_casefile, 'report'), SetVariable("bool_show_case", False),
                SetVariable('bool_show_case_report', True), Show('show_case_report', _layer="over_screens")]
        
        hbox:
            xpos 0.65 ypos 0.47
            text("{size=-5}Reports{/size}")

transform evidence_small():
    zoom 0.2

# Physical Evidence
screen show_case_evidence():
    showif bool_show_case_evidence:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("bool_show_case_evidence", False)]
        hbox:
            xalign 0.5 ypos 0.1
            text(case_type_selected)

        if case_file_dict['bullet']:
            showif not evidence_complete_process['gun_blue']:
                hbox:
                    xpos 0.55 ypos 0.3
                    textbutton('Process bullet casing'):
                        style "custom_button"
                        action [Function(set_cursor, 'tweezer_bullet'), SetVariable('current_evidence', bullet), SetVariable("bool_show_case_evidence", False)]
                        sensitive process_fumehood
                hbox:
                    xalign 0.3 yalign 0.3
                    imagebutton:
                        idle "casefile_bullet" at evidence_small
            else:
                hbox:
                    xpos 0.55 ypos 0.3
                    textbutton('Bullet casing processed'):
                        style "custom_button"
                        action NullAction()
                hbox:
                    xalign 0.3 yalign 0.3
                    imagebutton:
                        idle "bullet_print" at evidence_small
        
        if case_file_dict['cheque']:
            showif not evidence_complete_process['ninhydrin']:
                hbox:
                    xpos 0.55 ypos 0.3
                    textbutton('Process cheque'):
                        style "custom_button"
                        action [Function(set_cursor, 'cheque_mouse'), SetVariable('current_evidence', cheque), SetVariable("bool_show_case_evidence", False)]
                        sensitive process_fumehood
                hbox:
                    xalign 0.3 yalign 0.3
                    imagebutton:
                        idle "casefile_cheque" at evidence_small
            else:
                hbox:
                    xpos 0.55 ypos 0.3
                    textbutton('Cheque processed'):
                        style "custom_button"
                        action NullAction()
                hbox:
                    xalign 0.3 yalign 0.3
                    imagebutton:
                        idle "cheque_print" at evidence_small
        
        if case_file_dict['deskfoot']:
            hbox:
                xpos 0.5 ypos 0.3
                textbutton('Footprint processed (KNAAP)'):
                    style "custom_button"
                    action NullAction()
            hbox:
                xalign 0.3 yalign 0.3
                imagebutton:
                    idle "casefile_deskfoot" at evidence_small

        if case_file_dict['blood']:
            hbox:
                xpos 0.5 ypos 0.3
                textbutton('Bloody carpet processed\n(Hungarian Red)'):
                    style "custom_button"
                    action NullAction()
            hbox:
                xalign 0.3 yalign 0.3
                imagebutton:
                    idle "casefile_blood" at evidence_small

# Digital Evidence        
screen show_case_digi_evidence():
    showif bool_show_case_digi:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("bool_show_case_digi", False)]
        hbox:
            xalign 0.5 ypos 0.1
            text(case_type_selected)
        
        if case_file_dict['bullet']:
            showif evidence_complete_process['gun_blue']:
                showif not evidence_complete_process['bullet_AFIS']:
                    hbox:
                        xpos 0.55 ypos 0.3
                        textbutton('Process fingerprint'):
                            style "custom_button"
                            action [Function(set_cursor, 'bullet_fingerprint'), SetVariable('current_evidence', bullet), SetVariable('bool_show_case_digi', False)]
                            sensitive process_afis
                else:
                    hbox:
                        xpos 0.55 ypos 0.3
                        textbutton('Fingerprint processed'):
                            style "custom_button"
                            action NullAction() sensitive False
                hbox:
                    xalign 0.28 yalign 0.3
                    imagebutton:
                        idle "bullet_print" at evidence_small
        
        if case_file_dict['cheque']:
            showif evidence_complete_process['ninhydrin']:
                showif not evidence_complete_process['cheque_AFIS']:
                    hbox:
                        xpos 0.55 ypos 0.3
                        textbutton('Process fingerprint'):
                            style "custom_button"
                            action [Function(set_cursor, 'cheque_print'), SetVariable('current_evidence', deskfoot), SetVariable('bool_show_case_digi', False)]
                            sensitive process_afis
                else:
                    hbox:
                        xpos 0.55 ypos 0.3
                        textbutton('Fingerprint processed'):
                            style "custom_button"
                            action NullAction() sensitive False
                hbox:
                    xalign 0.28 yalign 0.3
                    imagebutton:
                        idle "cheque_print" at evidence_small

        if case_file_dict['deskfoot']:
            showif not evidence_complete_process['deskfoot_AFIS']:
                hbox:
                    xpos 0.55 ypos 0.3
                    textbutton('Process footprint'):
                        style "custom_button"
                        action [Function(set_cursor, 'casefile_deskfoot'), SetVariable('current_evidence', blood), SetVariable('bool_show_case_digi', False)]
                        sensitive process_afis
            else:
                hbox:
                    xpos 0.55 ypos 0.3
                    textbutton('Footprint processed'):
                        style "custom_button"
                        action NullAction() sensitive False
            hbox:
                xalign 0.28 yalign 0.3
                imagebutton:
                    idle "casefile_deskfoot" at evidence_small
        
        if case_file_dict['blood']:
            hbox:
                xpos 0.55 ypos 0.3
                textbutton('No visible print to process'):
                    style "custom_button"
                    action NullAction() sensitive False
            hbox:
                xalign 0.28 yalign 0.3
                imagebutton:
                    idle "casefile_blood" at evidence_small



screen show_case_report():
    showif bool_show_case_report:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("bool_show_case_report", False)]
        hbox:
            xalign 0.5 ypos 0.1
            text(case_type_selected)


