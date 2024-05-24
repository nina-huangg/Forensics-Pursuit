screen arrow_screen():
    image "courtroom_dark_bg"
    hbox:
        xpos 0.10 yalign 0.15
        image("arrow") at Transform (zoom=0.08)
            
screen evidence_button_screen():
    hbox:
        xpos 0.015 yalign 0.15
        imagebutton:
            idle "evidence_button_idle" at Transform (zoom=0.4)
            hover "evidence_button_hover"

            hovered Notify("Evidence")
            unhovered Notify('')

            action [ToggleVariable('show_evidence'), Hide("arrow_screen")]
    
    showif show_evidence:
        default current = {'evidence_gun_fingerprint': False, 'backing_card': False}
        hbox:
            xalign 0.1 yalign 0.3
            image "inventory"
        hbox:
            xpos 0.32 ypos 0.1
            text("Evidence")
        hbox:
            xpos 0.69 ypos 0.1
            text("Details")

        hbox:
            xpos 0.17 ypos 0.20
            imagebutton:
                idle "evidence_gun_fingerprint" at Transform(zoom=2)
                hover "evidence_gun_fingerprint"

                action [ToggleDict(current, 'evidence_gun_fingerprint'), SetDict(current,'backing_card', False)]
        hbox:
            xpos 0.31 ypos 0.23
            imagebutton:
                idle "evidence_backing_card" at Transform(zoom=0.25)
                hover "evidence_backing_card"

                action [ToggleDict(current, 'backing_card'), SetDict(current,'evidence_gun_fingerprint', False)]

        showif current['evidence_gun_fingerprint']:
            hbox:
                xpos 0.65 ypos 0.55
                textbutton('Use evidence'):
                    style "custom_button"
                    action NullAction()
    
            # else:
            #     frame:
            #         xpos 0.61 ypos 0.55
            #         textbutton('Firearm processed'):
            #             style "custom_button"
            #             action NullAction()
            hbox:
                xpos 0.61 ypos 0.20
                text("-firearm\n-collected on kitchen\nfloor\n-similarity report to stove\ntop fingerprint = 80%")         
    
        showif current['backing_card']:
            hbox:
                xpos 0.65 ypos 0.55
                textbutton('Use evidence'):
                    style "custom_button"
                    action NullAction()
    
        
        #     showif not evidence_complete_process['backing_card']:
        #         hbox:
        #             xpos 0.61 ypos 0.55
        #             textbutton('Process this fingerprint'):
        #                 style "custom_button"
        #                 action [Function(set_cursor, 'backing_card'), Function(set_current_evidence, 'backing_card'), ToggleVariable('show_evidence')]
        #                 sensitive process in evidence_process_tool['backing_card'] 
        #     else:
        #         hbox:
        #             xpos 0.61 ypos 0.55
        #             textbutton('Fingerprint processed'):
        #                 style "custom_button"
        #                 action NullAction() sensitive False
        #             #text('{color=#b3b3b3}Fingerprint processed{/color}')

        #     frame:
        #         xpos 0.62 ypos 0.63
        #         textbutton('See a larger image'):
        #             action NullAction()
            hbox:
                xpos 0.61 ypos 0.20
                text("-fingerprint\n-collected on kitchen\nstove\n-similarity report to\nfirearm fingerprint = 80%")
    
        # showif current['pills']:
        #     hbox:
        #         xpos 0.68 ypos 0.55
        #         image "evidence_pills" at evidence_gun_detail_small
        #     hbox:
        #         xpos 0.61 ypos 0.25
        #         text("-unknown pills\n-collected from oven")

screen score_screen():
    image("courtroom_dark_bg")
    hbox:
        image("score")
    hbox:
        xalign 0.48 yalign 0.3
        text("Number of correct answers:")
    hbox:
        xalign 0.48 yalign 0.38
        text("{size=+12}[total_score]{/size}")
    
    hbox:
        xalign 0.48 yalign 0.48
        text("Number of times consulted notes:")
    hbox:
        xalign 0.48 yalign 0.55
        text("{size=+12}0{/size}")

screen question_screen():
    frame:
        xalign 0.48 yalign 0.3
        text("What method did you use to develop fingerprints on the firearm and why?")
