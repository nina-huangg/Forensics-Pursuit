## Camera Module - Score Display Screen
## Modal overlay — no label jumps, no scene changes

screen photo_score_display(score_data):
    tag camera_overlay
    modal True
    zorder 100

    $ _cc = camera_config

    add Solid("#000000CC")

    # Action buttons on right side
    vbox:
        xalign 0.95
        yalign 0.5
        spacing 25

        # Retake button
        vbox:
            spacing 5
            imagebutton:
                idle Transform("back_button.png", zoom=0.4)
                hover Transform("back_button_hover.png", zoom=0.4)
                action Function(camera_retake)
            text "Retake" size 20 color "#FFFFFF" xalign 0.5 font _cc.font

        # Continue button
        vbox:
            spacing 5
            imagebutton:
                idle Transform("back_button.png", zoom=0.4)
                hover Transform("back_button_hover.png", zoom=0.4)
                action Function(camera_close_score)
            text "Continue" size 20 color "#FFFFFF" xalign 0.5 font _cc.font

    # Main score card
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1250
        ysize 1000
        background "#FFFFFF"
        padding (40, 30)

        vbox:
            spacing 12
            xalign 0.5

            text "Photo Analysis & Feedback" size 42 color "#000000" xalign 0.5 bold True font _cc.font

            hbox:
                spacing 15
                xalign 0.5

                text "Location: [score_data['location_name']]" size 24 color "#333333" font _cc.font

                if score_data["grade"] in ["A+", "A", "A-"]:
                    $ grade_color = "#00AA00"
                    $ grade_bg = "#E8F5E9"
                elif score_data["grade"] in ["B+", "B", "B-"]:
                    $ grade_color = "#0066CC"
                    $ grade_bg = "#E3F2FD"
                elif score_data["grade"] in ["C+", "C", "C-"]:
                    $ grade_color = "#FF8800"
                    $ grade_bg = "#FFF3E0"
                else:
                    $ grade_color = "#CC0000"
                    $ grade_bg = "#FFEBEE"

                frame:
                    background grade_bg
                    padding (12, 6)
                    text "Grade: [score_data['grade']]" size 22 color grade_color bold True font _cc.font

            null height 3
            frame:
                xsize 1170
                ysize 2
                background "#DDDDDD"
            null height 3

            frame:
                xsize 1170
                background "#F5F5F5"
                padding (20, 15)
                vbox:
                    spacing 6
                    text "Overall Assessment:" size 22 color "#000000" bold True font _cc.font
                    text "[score_data['overall_feedback']]" size 19 color "#333333" line_spacing 3

            null height 8

            vbox:
                spacing 12
                xalign 0.5
                xsize 1170

                frame:
                    xsize 1170
                    background "#FAFAFA"
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text "Composition & Framing" size 21 color "#1976D2" bold True font _cc.font
                        text "[score_data['composition']['feedback']]" size 18 color "#424242" line_spacing 3

                frame:
                    xsize 1170
                    background "#FAFAFA"
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text "Exposure Settings" size 21 color "#1976D2" bold True font _cc.font
                        text "[score_data['exposure']['feedback']]" size 18 color "#424242" line_spacing 3

                frame:
                    xsize 1170
                    background "#FAFAFA"
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text "Focus & Sharpness" size 21 color "#1976D2" bold True font _cc.font
                        text "[score_data['sharpness']['feedback']]" size 18 color "#424242" line_spacing 3

                frame:
                    xsize 1170
                    background "#FAFAFA"
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text "Documentation Requirements" size 21 color "#1976D2" bold True font _cc.font
                        text "[score_data['completeness']['feedback']]" size 18 color "#424242" line_spacing 3

            if score_data["total"] < 90 and score_data.get("tips", ""):
                null height 8
                frame:
                    xsize 1170
                    background "#FFF9E6"
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text "Professional Tip" size 21 color "#F57C00" bold True font _cc.font
                        text "[score_data['tips']]" size 18 color "#5D4037"

            null height 8
            text "Press SPACE to continue  |  Press ESC to retake" size 16 color "#999999" xalign 0.5 font _cc.font

    key "K_SPACE" action Function(camera_close_score)
    key "K_ESCAPE" action Function(camera_retake)
