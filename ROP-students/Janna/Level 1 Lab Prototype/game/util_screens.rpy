
screen back_button_screen(old_location):
    zorder 1
    hbox:
        xalign 0.01 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [SetVariable("imported_print", ""), SetVariable("print_imported", False), Hide('afis_screen'), Hide("casefile_physical"), SetVariable("location", old_location), Jump(old_location)]

### CASE FILES
screen case_files_screen():
    hbox:
        xpos 0.005 yalign 0.12
        imagebutton:
            idle "case_file_idle" at Transform(zoom=3)
            hover "case_file_hover"

            hovered Notify("Case files")
            unhovered Notify('')

            action [ToggleVariable('show_case_files'), Function(set_cursor, '')]
    
    showif show_case_files:
        default current = {'firearm': False, 'stovetop': False}
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xalign 0.5 ypos 0.1
            text("Case Files")
        
        hbox:
            xpos 0.20 ypos 0.20
            imagebutton:
                idle "evidence_computer_fingerprint" at Transform (zoom=0.4)

                action [ToggleVariable('show_case_files'),SetVariable('current_evidence', laptop_fingerprint),Function(set_cursor, 'laptop_fingerprint')]
 
        hbox:
            xalign 0.24 ypos 0.41
            text("{color=#ffffff}Laptop Fingerprint{/color}")
        
        hbox:
            xpos 0.40 ypos 0.20
            imagebutton:
                idle "evidence_screwdriver" 

                action [ToggleVariable('show_case_files'),SetVariable('current_evidence', screwdriver),Function(set_cursor, 'screwdriver')]
 
        hbox:
            xalign 0.44 ypos 0.41
            text("{color=#ffffff}Screwdriver{/color}")



#### toolbox
screen toolbox_button_screen:
    hbox:
        xpos 0.006 yalign 0.38
        imagebutton:
            idle "toolbox_button_idle" at Transform (zoom=0.3)
            hover "toolbox_button_hover"

            hovered Notify("Toolbox")
            unhovered Notify('')

            action [ToggleVariable("show_toolbox"), Function(set_cursor, '')]
    showif show_toolbox:
            hbox:
                xpos 0.91 ypos 0.12
                imagebutton:
                    idle "superglue_idle" at Transform (zoom=0.18)
                    hover "superglue_hover"

                    hovered Notify("Superglue")
                    unhovered Notify('')
                    
                    action Function(set_cursor, 'superglue')
            hbox:
                xpos 0.90 ypos 0.32
                imagebutton:
                    idle "water_idle" at Transform (zoom=0.22)
                    hover "water_hover"

                    hovered Notify("Water")
                    unhovered Notify('')

                    action Function(set_cursor, 'water')
            hbox:
                xpos 0.91 ypos 0.53
                imagebutton:
                    idle "lifting_tape_idle" at Transform (zoom=0.16)
                    hover "lifting_tape_hover"

                    hovered Notify("Lifting Tape")
                    unhovered Notify('')

                    action Function(set_cursor, 'lifting_tape')
            
            hbox:
                xpos 0.895 ypos 0.72
                imagebutton:
                    idle "camera_idle" at Transform (zoom=0.33)
                    hover "camera_hover"

                    hovered Notify("Camera")
                    unhovered Notify('')

                    action Function(set_cursor, 'camera')
