
screen back_button_screen(location):
    hbox:
        xalign 0.965 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.25)
            hover "back_button_hover"
            action [Jump(location)]


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
                        idle "/case_files/" + file + "_idle.png" at Transform(zoom=0.35)

                        hovered Notify(file)
                        unhovered Notify('')

                        action NullAction()
                hbox:
                    xalign i*0.15 + 0.24 ypos 0.40
                    text (file)
            else:
                hbox:
                    xpos i * 0.15 + 0.20 ypos 0.50
                    imagebutton:
                        idle "/case_files/" + file + "_idle" at Transform(zoom=0.35)

                        hovered Notify(file)
                        unhovered Notify('')

                        action NullAction()
                hbox:
                    xalign i*0.15 + 0.24 ypos 0.60
                    text (file)

        
        # hbox:
        #     xpos 0.20 ypos 0.20
        #     imagebutton:
        #         idle "bottle-idle" at Transform (zoom=0.4)

        #         action [ToggleVariable('show_case_files'),SetVariable('current_evidence', bottle),Function(set_cursor, 'bottle-idle'), Jump("fingerprint_start")]
 
        # hbox:
        #     xalign 0.24 ypos 0.41
        #     text("{color=#ffffff}Alcohol Bottle{/color}")
        
        # hbox:
        #     xpos 0.40 ypos 0.20
        #     imagebutton:
        #         idle "vase-idle" at Transform (zoom=0.4)

        #         action [ToggleVariable('show_case_files'),SetVariable('current_evidence', vase),Function(set_cursor, 'vase-idle'), Jump("fingerprint_start")]
 
        # hbox:
        #     xalign 0.44 ypos 0.41
        #     text("{color=#ffffff}Vase{/color}")
        
        # hbox:
        #     xpos 0.60 ypos 0.22
        #     imagebutton:
        #         idle "swab" at Transform (zoom=0.1)

        #         action [ToggleVariable('show_case_files'),SetVariable('current_evidence', swab),Function(set_cursor, 'swab'), Jump("fingerprint_start")]
 
        # hbox:
        #     xalign 0.64 ypos 0.41
        #     text("{color=#ffffff}Swab{/color}")

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


screen tool_unavailable_screen():
    zorder 10
    vbox:
        xalign 0.5
        yalign 0.8
        frame:
            text "Try selecting a different tool first." + str(steps["wall"]) 

        frame:
            xalign 0.5
            yalign 0.9
            textbutton "OK" action [Hide("tool_unavailable_screen"), Function(set_cursor, '')]

screen photo_unavailable_screen():
    zorder 10
    vbox:
        xalign 0.5
        yalign 0.8
        frame:
            text "No need for photos right now."

        frame:
            xalign 0.5
            yalign 0.9
            textbutton "OK" action [Hide("photo_unavailable_screen"), Function(set_cursor, '')]