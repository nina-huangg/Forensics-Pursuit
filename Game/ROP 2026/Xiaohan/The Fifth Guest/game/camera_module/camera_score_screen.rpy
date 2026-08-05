## Camera Module - Score Display Screen
## Modal overlay — no label jumps, no scene changes

screen photo_score_display(score_data):
    tag camera_overlay
    modal True
    zorder 100

    $ _cc = camera_config
    $ _font = _cc.font if _cc else "DejaVuSans.ttf"
    $ _loc_name = score_data.get("location_name", "Unknown")
    $ _grade = score_data.get("grade", "F")
    $ _overall = score_data.get("overall_feedback", score_data.get("error", "No feedback available."))
    $ _comp = score_data.get("composition", {}).get("feedback", "")
    $ _exp = score_data.get("exposure", {}).get("feedback", "")
    $ _sharp = score_data.get("sharpness", {}).get("feedback", "")
    $ _complete = score_data.get("completeness", {}).get("feedback", "")
    $ _tips = score_data.get("tips", "")
    $ _total = score_data.get("total", 0)
    $ _has_error = bool(score_data.get("error"))
    $ _acceptance = score_data.get("acceptance_note", "")
    $ _requires_retake = bool(score_data.get("requires_retake"))

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
            text "Retake" size 20 color "#FFFFFF" xalign 0.5 font _font

        # Continue button
        vbox:
            spacing 5
            imagebutton:
                idle Transform("back_button.png", zoom=0.4)
                hover Transform("back_button_hover.png", zoom=0.4)
                action Function(camera_close_score)
            text ("Keep Album Only" if _requires_retake else "Continue") size 18 color "#FFFFFF" xalign 0.5 font _font

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

            text "Photo Analysis & Feedback" size 42 color "#000000" xalign 0.5 bold True font _font

            hbox:
                spacing 15
                xalign 0.5

                text "Location: [_loc_name]" size 24 color "#333333" font _font

                if _grade in ["A+", "A", "A-"]:
                    $ grade_color = "#00AA00"
                    $ grade_bg = "#E8F5E9"
                elif _grade in ["B+", "B", "B-"]:
                    $ grade_color = "#0066CC"
                    $ grade_bg = "#E3F2FD"
                elif _grade in ["C+", "C", "C-"]:
                    $ grade_color = "#FF8800"
                    $ grade_bg = "#FFF3E0"
                else:
                    $ grade_color = "#CC0000"
                    $ grade_bg = "#FFEBEE"

                frame:
                    background grade_bg
                    padding (12, 6)
                    text "Grade: [_grade]" size 22 color grade_color bold True font _font

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
                    text "Overall Assessment:" size 22 color "#000000" bold True font _font
                    text "[_overall]" size 19 color "#333333" line_spacing 3

            null height 8

            if not _has_error:
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
                            text "Composition & Framing" size 21 color "#1976D2" bold True font _font
                            text "[_comp]" size 18 color "#424242" line_spacing 3

                    frame:
                        xsize 1170
                        background "#FAFAFA"
                        padding (18, 14)
                        vbox:
                            spacing 6
                            text "Exposure Settings" size 21 color "#1976D2" bold True font _font
                            text "[_exp]" size 18 color "#424242" line_spacing 3

                    frame:
                        xsize 1170
                        background "#FAFAFA"
                        padding (18, 14)
                        vbox:
                            spacing 6
                            text "Focus & Sharpness" size 21 color "#1976D2" bold True font _font
                            text "[_sharp]" size 18 color "#424242" line_spacing 3

                    frame:
                        xsize 1170
                        background "#FAFAFA"
                        padding (18, 14)
                        vbox:
                            spacing 6
                            text "Documentation Requirements" size 21 color "#1976D2" bold True font _font
                            text "[_complete]" size 18 color "#424242" line_spacing 3

            if (not _has_error) and _total < 90 and _tips:
                null height 8
                frame:
                    xsize 1170
                    background "#FFF9E6"
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text "Professional Tip" size 21 color "#F57C00" bold True font _font
                        text "[_tips]" size 18 color "#5D4037"

            if _acceptance:
                null height 8
                frame:
                    xsize 1170
                    background ("#FFEBEE" if _requires_retake else "#E8F5E9")
                    padding (18, 14)
                    vbox:
                        spacing 6
                        text ("Evidence Not Accepted" if _requires_retake else "Evidence Ready") size 21 color ("#CC0000" if _requires_retake else "#2E7D32") bold True font _font
                        text "[_acceptance]" size 18 color "#333333"

            null height 8
            text "Press SPACE to continue  |  Press ESC to retake" size 16 color "#999999" xalign 0.5 font _font

    key "K_SPACE" action Function(camera_close_score)
    key "K_ESCAPE" action Function(camera_retake)
