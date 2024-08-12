
screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Jump(location), Hide('afis_screen')]

screen checkmark_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "checkmark" at Transform(zoom=0.2)
            hover "checkmark_hover"
            action [Jump(location), Hide('checkmark_button_screen')]
            
### CASE FILES
screen case_files_screen(case_files):
    hbox:
        xpos 0.017 yalign 0.12
        imagebutton:
            idle "case_file_idle" at Transform(zoom=0.35)
            hover "case_file_hover"

            hovered Notify("Case files")
            unhovered Notify('')

            action [ToggleVariable('show_case_files'), Function(set_cursor, '')]
    
    showif show_case_files:
        # default current = {'firearm': False, 'stovetop': False}
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xalign 0.5 ypos 0.1
            text("Case Files")
        
        for i, file in enumerate(case_files):
            if i < 4:
                hbox:
                    xpos i * 0.15 + 0.20 ypos 0.20
                    imagebutton:
                        idle "/case_files/" + file + ".png" at Transform(zoom=0.35)

                        hovered Notify(file)
                        unhovered Notify('')

                        action [ToggleVariable('show_case_files'), Function(check_valid_evidence, file, current_lab)]
                hbox:
                    xalign i*0.15 + 0.24 ypos 0.40
                    text (file) size 15
            else:
                hbox:
                    xpos (i % 4) * 0.15 + 0.20 ypos 0.50
                    imagebutton:
                        idle "/case_files/" + file + ".png" at Transform(zoom=0.35)

                        hovered Notify(file)
                        unhovered Notify('')

                        action [ToggleVariable('show_case_files'), Function(check_valid_evidence, file, current_lab)]
                hbox:
                    xalign (i % 4) * 0.15 + 0.24 ypos 0.70
                    text (file) size 15


screen toolbox_button_screen(tools):
    zorder 10
    hbox:
        xpos 0.017 yalign 0.3
        imagebutton:
            idle 'toolbox_button_idle' at Transform(zoom=0.25) 
            hover "toolbox_button_hover"

            hovered Notify("Toolbox")
            unhovered Notify('')

            action [Function(set_cursor, ''), ToggleVariable('show_toolbox')]

    showif show_toolbox:
        for i, tool in enumerate(tools[1:]):
            if i < 5:
                hbox:
                    xpos 0.90
                    ypos i * 0.16 + 0.05
                    imagebutton:
                        idle "/toolbox/" + tool + "_idle.png" at Transform(zoom=0.07)
                        hover "/toolbox/" + tool + "_hover.png"
                        hovered Notify(tool)
                        unhovered Notify('')
                        if tools[0] == 'default':
                            action [Show("photo_unavailable_screen")]
                        elif steps[tools[0]] >= len(tools):
                            action Show("tool_unavailable_screen")
                        else:
                            action [Function(set_cursor, tool), If(tool == tools[steps[tools[0]]], Jump(tools[0]+"_"+tool), 
                            Show("tool_unavailable_screen"))]

            else:
                hbox:
                    xpos 0.0225
                    ypos (i - 5) * 0.16 + 0.45
                    imagebutton:
                        idle "/toolbox/" + tool + "_idle.png" at Transform(zoom=0.07)
                        hover "/toolbox/" + tool + "_hover.png"
                        hovered Notify(tool)
                        unhovered Notify('')
                        if tools[0] == 'default':
                            action [Show("photo_unavailable_screen")]
                        elif steps[tools[0]] >= len(tools):
                            action Show("tool_unavailable_screen")
                        else:
                            action [Function(set_cursor, tool), If(tool == tools[steps[tools[0]]], Jump(tools[0]+"_"+tool), 
                            Show("tool_unavailable_screen"))]


screen invalid_evidence_screen():
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "This evidence does not need to be processed at the lab you are currently in." 
            textbutton "Okay" action [Hide("invalid_evidence_screen"), Function(set_cursor, '')]

screen processed_evidence_screen():
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "You have already processed this evidence." 
            textbutton "Okay" action [Hide("processed_evidence_screen"), Function(set_cursor, '')]

screen tool_unavailable_screen():
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "Try selecting a different tool."
            textbutton "Okay" action [Hide("tool_unavailable_screen"), Function(set_cursor, '')]

screen photo_unavailable_screen():
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "No need for photos right now."
            textbutton "Okay" action [Hide("photo_unavailable_screen"), Function(set_cursor, '')]

screen incorrect_time_message():
    zorder 50
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "Hmm . . . that doesn't seem like the correct time. Try again."
            textbutton "Okay":
                action Return(True) 

screen dna_score_screen(score):
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "The DNA profiles are [score]% consistent."
            textbutton "Okay" action [Hide("dna_score_screen"), Function(set_cursor, '')]


screen fingerprint_score_screen(score):
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "The fingerprints are [score]% consistent."
            textbutton "Okay" action [Hide("fingerprint_score_screen"), Function(set_cursor, '')]


screen error_score_screen():
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "ERROR: type mismatch"
            textbutton "Okay" action [Hide("error_score_screen"), Function(set_cursor, '')]

screen text_screen(dialouge):
    frame:
        xalign 0.5
        yalign 0.85
        vbox:
            text dialouge
            textbutton "Okay" action [Hide("text_screen"), Function(set_cursor, ''), Return("")]

screen correct_screen(dialouge):
    frame:
        xalign 0.5
        yalign 0.85
        vbox:
            text dialouge
            textbutton "Okay" action [Hide("correct_screen"), Function(set_cursor, '')]
