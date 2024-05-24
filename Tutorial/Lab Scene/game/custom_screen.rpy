screen hallway_screen(active):
    image "lab_hallway_dim"

    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_lab_button_idle"
            hover "data_lab_button_hover"

            hovered Notify("Data Analysis Lab")
            unhovered Notify('')
            if not evidence_complete_process['backing_card'] and not cyanoacrylate_in_progress:
                action Jump("wrong_action")
            elif (not evidence_complete_process['backing_card']):
                action [Jump("data_analysis_lab"), SetVariable('wrong_action', False)] sensitive active
            else:
                action [Jump('process_firearm_fingerprint'), SetVariable('wrong_action', False)]sensitive active

    hbox:
        xpos 0.234 yalign 0.628
        hbox:
            text("{size=-6}Data Analysis Lab{/size}")
        
    hbox:
        xpos 0.63 yalign 0.5
        imagebutton:
            idle "materials_lab_button_idle"
            hover "materials_lab_button_hover"

            hovered Notify("Materials Lab")
            unhovered Notify('')

            action Jump("materials_lab") sensitive active

    hbox:
        xpos 0.68 yalign 0.628
        hbox:
            text("{size=-6}Materials Lab{/size}")


screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at checkmark_small
            hover "back_button_hover"
            action Jump(location)

screen data_analysis_lab_screen:
    default show_analysis = False
    imagemap:
        idle "afis_workstation_idle"
        hover "afis_workstation_hover"
        insensitive "afis_workstation_idle"
        hotspot (473,207,975,513) action [Function(set_state_to_processed, current_evidence), Function(set_cursor, ''), Return()] sensitive current_cursor =='backing_card' or current_cursor=='firearm_fingerprint'
    

transform checkmark_small():
    zoom 0.2

transform evidence_small():
    zoom 0.4

screen evidence_button_screen(process):
    hbox:
        xpos 0.015 yalign 0.15
        imagebutton:
            idle "evidence_button_idle" at evidence_small
            hover "evidence_button_hover"

            hovered Notify("Evidence")
            unhovered Notify('')

            action ToggleVariable('show_evidence')
    

    showif show_evidence:
        default current = {'firearm': False, 'firearm_fingerprint': False, 'backing_card': False}
        hbox:
            xalign 0.1 yalign 0.3
            image "inventory"
        hbox:
            xpos 0.29 ypos 0.1
            text("Evidence Storage")
        hbox:
            xpos 0.69 ypos 0.1
            text("Details")

        #showif not cyanoacrylate_finish:
        hbox:
            xpos 0.16 ypos 0.23
            imagebutton:
                idle "evidence_gun" at evidence_gun_small
                hover "evidence_gun"

                action [ToggleDict(current, 'firearm'), SetDict(current,'backing_card', False), SetDict(current,'firearm_fingerprint', False), Function(set_evidence_select, 'firearm')]
        hbox:
            xpos 0.31 ypos 0.23
            imagebutton:
                idle "evidence_backing_card" at evidence_gun_small
                hover "evidence_backing_card"

                action [ToggleDict(current, 'backing_card'), SetDict(current,'firearm', False),SetDict(current,'firearm_fingerprint', False), Function(set_evidence_select, 'backing_card')]
        # showif cyanoacrylate_finish:
        #     hbox:
        #         xpos 0.43 ypos 0.19
        #         imagebutton:
        #             idle "evidence_gun_fingerprint" at Transform(zoom=0.9)
        #             hover "evidence_gun_fingerprint"

        #             action [ToggleDict(current, 'firearm_fingerprint'), SetDict(current,'backing_card', False),SetDict(current,'firearm', False), Function(set_evidence_select, 'firearm_fingerprint')]
    
        showif current['firearm']:
            showif not evidence_complete_process['firearm']:
                hbox:
                    xpos 0.62 ypos 0.55
                    textbutton('Process firearm'):
                        style "custom_button"
                        action [Function(set_cursor, 'evidence_gun'), Function(set_current_evidence, 'firearm'), ToggleVariable('show_evidence')]
                        sensitive process in evidence_process_tool['firearm']
            else:
                hbox:
                    xpos 0.62 ypos 0.55
                    textbutton('Firearm processed'):
                        style "custom_button"
                        action NullAction() sensitive False

            hbox:
                xpos 0.61 ypos 0.25
                text("-firearm\n-collected on kitchen\nfloor")         
    
        showif current['backing_card']:
            showif not evidence_complete_process['backing_card']:
                hbox:
                    xpos 0.62 ypos 0.55
                    textbutton('Process fingerprint'):
                        style "custom_button"
                        action [Function(set_cursor, 'backing_card'), Function(set_current_evidence, 'backing_card'), ToggleVariable('show_evidence')]
                        sensitive process in evidence_process_tool['backing_card'] 
            else:
                hbox:
                    xpos 0.62 ypos 0.55
                    textbutton('Fingerprint processed'):
                        style "custom_button"
                        action NullAction() sensitive False

            hbox:
                xpos 0.61 ypos 0.25
                text("-fingerprint\n-collected on kitchen\nstove")
    
        # showif current['firearm_fingerprint']:
        #     showif not evidence_complete_process['firearm_fingerprint']:
        #         hbox:
        #             xpos 0.62 ypos 0.55
        #             textbutton('Process fingerprint'):
        #                 style "custom_button"
        #                 action [Function(set_cursor, 'firearm_fingerprint'), Function(set_current_evidence, 'firearm_fingerprint'), ToggleVariable('show_evidence')]
        #                 sensitive process in evidence_process_tool['firearm_fingerprint'] 
        #     else:
        #         hbox:
        #             xpos 0.62 ypos 0.55
        #             textbutton('Fingerprint processed'):
        #                 style "custom_button"
        #                 action NullAction() sensitive False
        #     hbox:
        #         xpos 0.61 ypos 0.25
        #         text("-fingerprints from\nfirearm")

transform evidence_gun_small():
    zoom 0.25
transform evidence_gun_detail_small():
    zoom 0.4


screen materials_lab_screen:
    hbox:
        xpos 0.35 ypos 0.42
        imagebutton:
            idle "cyano_idle" at cyano_small
            hover "cyano_hover"

            hovered Notify("Fingerprint Development")
            unhovered Notify('')

            action Jump('cyano_machine')
    
    hbox:
        xpos 0.65 ypos 0.77
        hbox:
            text("{size=-7}Analytical Instruments{/size}")
    
    hbox:
        xpos 0.10 ypos 0.34
        imagebutton:
            idle "fumehood_idle" at fumehood_small
            hover "fumehood_hover"

            hovered Notify("Wet Lab")
            unhovered Notify('')

            action Jump('wet_lab')
    
    hbox:
        xpos 0.24 ypos 0.77
        hbox:
            text("{size=-6}Wet Lab{/size}")
    
    hbox:
        xpos 0.60 ypos 0.43
        imagebutton:
            idle "ftir_idle" at cyano_small
            hover "ftir_hover"

            hovered Notify("Analytical Instruments")
            unhovered Notify('')

            action Jump('analytical_instruments')
    
    hbox:
        xpos 0.42 ypos 0.77
        hbox:
            text("{size=-7}Fingerprint Development{/size}")

    # hbox:
    #     xalign 0.97 yalign 0.93
    #     imagebutton:
    #         idle "back_button" at checkmark_small
    #         hover "back_button_hover"
    #         action Jump("hallway")

transform cyano_small():
    zoom 0.1

transform fumehood_small():
    zoom 0.125

transform ftir_small():
    zoom 0.02

screen cyano_screen():
    imagemap:
        idle "fingerprint_development_bg"
        hover "cyano_open"
        hotspot (663,434,732,483) action Return()

screen cyano_process_screen():
    default metal_dish_filled = False
    default water_dish_filled = False
    imagemap:
        idle 'cyano_inside'
        hover "cyano_inside_hover"
        insensitive 'cyano_inside'
        hotspot(494, 187, 873, 123) action [SetVariable('hang_evidence', True), Function(set_cursor, ''), Return()] sensitive current_cursor=='evidence_gun'

    showif hang_evidence:
        imagemap:
            idle 'cyano_hang_evidence'
            hover 'cyano_hang_evidence_hover'
            insensitive 'cyano_hang_evidence'
            hotspot(606, 724, 270, 125) action [SetLocalVariable('metal_dish_filled', True), Function(set_cursor, '')] sensitive current_cursor=='superglue'
            hotspot(1067, 731, 260, 136) action [SetLocalVariable('water_dish_filled', True), Function(set_cursor, '')] sensitive current_cursor=='water'

    showif metal_dish_filled:
        hbox:
            xalign 0.38 yalign 0.8
            image("check") at Transform (zoom=0.8)
    
    showif water_dish_filled:
        hbox:
            xalign 0.64 yalign 0.8
            image("check") at Transform (zoom=0.8)
                
    showif metal_dish_filled and water_dish_filled:
        # frame:
        #     xalign 0.82 yalign 0.5
        #     textbutton('CLOSE CHAMBER') at Transform(zoom=1.2):
        #         action [Function(set_cursor, ''), Return()]


        hbox:
            xalign 0.82 yalign 0.5
            textbutton "CLOSE CHAMBER":
                style "custom_button"
                action [Function(set_cursor, ''), Return()]



screen cyano_start_screen():
    hbox:
            xalign 0.48 yalign 0.25
            #textbutton('START PROCESS') at Transform (zoom=1.2):
            textbutton "START PROCESS":
                style "custom_button"
                action [Function(set_state_to_processed, current_evidence), Return()]

screen cyano_in_progress_screen():
    image('cyano_in_process_dim')
    hbox:
        image("small_notification")
    hbox:
            xalign 0.49 yalign 0.37
            text('Fuming in progress...') at Transform (zoom=1.3)

    
screen wet_lab_screen:
    hbox:
        xalign 0.95 yalign 0.93
        imagebutton:
            idle "checkmark" at checkmark_small
            hover "checkmark_hover"
            action Jump("materials_lab_tools")
    
screen analytical_instruments_screen:
    hbox:
        xalign 0.95 yalign 0.93
        imagebutton:
            action NullAction()

screen instruments_button_screen:
    hbox:
        #xpos 0.01 yalign 0.40
        xpos 0.008 yalign 0.65
        imagebutton:
            idle "instruments_button_idle" at evidence_small
            hover "instruments_button_hover"

            hovered Notify("Instruments")
            unhovered Notify('')

            action ToggleVariable('show_instruments')

    showif show_instruments:
        hbox:
            xalign 0.1 yalign 0.3
            image "instruments_inventory" 
        hbox:
            xpos 0.20 ypos 0.1
            text("Instruments")
        hbox:
            xpos 0.55 ypos 0.1
            text("Description")
        # hbox:
        #     xpos 0.16 ypos 0.1
        #     imagebutton: 
        #         idle "inventory_previous"
        #         hover "inventory_previous_hover"
        #         action Function(previous_page)
        # hbox:
        #     xpos 0.50 ypos 0.5
        #     text("num is: %d" % current_inventory_page)
        # hbox:
        #     xpos 0.31 ypos 0.1
        #     imagebutton: 
        #         idle "inventory_next"
        #         hover "inventory_next_hover"
        #         action Function(next_page)
        
        showif current_inventory_page == 1:
            hbox:
                xpos 0.16 ypos 0.20
                imagebutton:
                    idle "ftir_inventory_idle" at evidence_gun_small
                    hover "ftir_inventory_hover"

                    hovered Notify("FTIR")
                    unhovered Notify('')

                    action [ToggleDict(instruments, 'FTIR'), Function(set_instruments_false, 'FTIR')]
            hbox:
                xpos 0.16 ypos 0.48
                imagebutton:
                    idle "altftir_inventory_idle" at evidence_gun_small
                    hover "altftir_inventory_hover"

                    hovered Notify("altFTIR")
                    unhovered Notify('')

                    action [ToggleDict(instruments, 'altFTIR'), Function(set_instruments_false, 'altFTIR')]
            
            showif instruments['FTIR']:
                hbox:
                    xpos 0.40 ypos 0.17
                    image('ftir_inventory_idle') at inventory_instruments_small
                hbox:
                    xpos 0.65 ypos 0.25
                    text('{size=-6}Classes:\n\n-Spectroscopy\n-Organic analysis\n-Inorganic analysis{/size}')
                hbox:
                    xpos 0.39 ypos 0.53
                    text("{size=-6}Function: uses infrared light to identify functional groups\n\nLimitations: -Sample must be purified prior to analysis\n\
                    -Accepts both solid, liquid, and dissolved samples\n\nOperation time: 2-5 minutes{/size}")
            showif instruments['altFTIR']:
                hbox:
                    xpos 0.41 ypos 0.15
                    image('altftir_inventory_idle') at evidence_gun_small

        showif current_inventory_page == 2:
            hbox:
                xpos 0.17 ypos 0.20
                imagebutton:
                    idle "gcms_inventory_idle" at evidence_gun_small
                    hover "gcms_inventory_hover"

                    hovered Notify("GCMS")
                    unhovered Notify('')

                    action [ToggleDict(instruments, 'GCMS'), Function(set_instruments_false, 'GCMS')]
            hbox:
                xpos 0.25 ypos 0.60
                textbutton('MS'):
                    action [ToggleDict(instruments, 'MS'), Function(set_instruments_false, 'MS')]

            showif instruments['GCMS']:
                hbox:
                    xpos 0.41 ypos 0.16
                    image('gcms_inventory_idle') at inventory_instruments_small
                hbox:
                    xpos 0.65 ypos 0.25
                    text('{size=-6}Classes:\n\n-Seperation Science\n-Organic analysis{/size}')
                hbox:
                    xpos 0.39 ypos 0.53
                    text("{size=-10}Functions:\n -A separation technique where a column is packed with\nmaterial (stationary phase) which retains a volatilized compound \nwhile \
a gas (mobile phase) is used to carry the compound through \nto a detector\n-The time it takes for each compound to reach the detector is \ncharacteristic of the compound and is known as the retention times\n\n\
{/size}")
            showif instruments['MS']:
                hbox:
                    xpos 0.65 ypos 0.25
                    text('{size=-6}Classes:\n\n-Organice\n-Inorganic analysis{/size}')
                hbox:
                    xpos 0.39 ypos 0.50
                    text("{size=-10}Functions:\n-Uses electricity to fragment molecules in predictable patterns for\n identification\
-Fragments are characterized based on a mass-to-charge\n ratio (m/z)\n-Useful for determining the identity of unknown compounds\n\nLimitations:\n-Sample must be purified prior to analysis\
\n-Accepts samples dissolved in aqeuous solvent{/size}")
            
        showif current_inventory_page == 3:
            hbox:
                xpos 0.16 ypos 0.20
                textbutton('HPLS-MS')
            hbox:
                xpos 0.16 ypos 0.48
                textbutton('ICP-MS')
        showif current_inventory_page == 4:
            hbox:
                xpos 0.16 ypos 0.20
                textbutton('SEM-EDX')


transform inventory_instruments_small():
    zoom 0.3
        

screen instrument_dropdown_screen():

    # This frame can be a very complex layout, if required.
    frame:
        align (.9, .05)
        padding (20, 20)

        has vbox

        # This is the button that is clicked to enable the dropdown,
        textbutton "Category: [category]":

            # This action captures the focus rectangle, and in doing so,
            # displays the dropdown.
            action CaptureFocus("diff_drop")

        # textbutton "Done":
        #     action Return()

    # All sorts of other screen elements could be here, but the nearrect needs
    # be at the top level, and the last thing show, apart from its child.

    # Only if the focus has been captured, display the dropdown.
    # You could also use showif instead of basic if
    if GetFocusRect("diff_drop"):

        # If the player clicks outside the frame, dismiss the dropdown.
        # The ClearFocus action dismisses this dropdown.
        dismiss action ClearFocus("diff_drop")

        # This positions the displayable near (usually under) the button above.
        nearrect:
            focus "diff_drop"

            # Finally, this frame contains the choices in the dropdown, with
            # each using ClearFocus to dismiss the dropdown.
            frame:
                modal True

                has vbox

                textbutton "Inorganic Analysis" action [ SetVariable("category", "Inorganic Analysis"), ClearFocus("diff_drop") ]
                textbutton "Organic Analysis" action [ SetVariable("category", "Organic Analysis"), ClearFocus("diff_drop") ]
                textbutton "Spectroscopy" action [ SetVariable("category", "Spectroscopy"), ClearFocus("diff_drop") ]
                textbutton "Separation Science" action [ SetVariable("category", "Separation Science"), ClearFocus("diff_drop") ]
                textbutton "Elemental Analysis" action [ SetVariable("category", "Elemental Analysis"), ClearFocus("diff_drop") ]
    
    showif category=='Organic Analysis':
        hbox:
            xpos 0.18 ypos 0.48
            image('gcms_inventory_idle') at analytical_instruments_small
        text('GCMS') xpos 0.30 ypos 0.87
        hbox:
            xpos 0.55 ypos 0.53
            image('ftir_inventory_idle') at analytical_instruments_small
        text('FTIR') xpos 0.67 ypos 0.87
    showif category=='Inorganic Analysis':
        hbox:
            xalign 0.5 ypos 0.54
            image('ftir_inventory_idle') at analytical_instruments_small
        text('FTIR') xalign 0.5 ypos 0.89
    showif category=='Separation Science':
        hbox:
            xalign 0.5 ypos 0.48
            image('gcms_inventory_idle') at analytical_instruments_small
        text('GCMS') xalign 0.5 ypos 0.89


transform analytical_instruments_small():
    zoom 0.4


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

screen caution_screen():
    default show_dismiss = False
    default show_arrow = True
    showif show_arrow:
        hbox:
            xpos 0.83 ypos 0.06 
            image("arrow") at Transform(zoom=0.06)
    hbox:
        xpos 0.88 ypos 0.01
        imagebutton:
            idle "caution_button_idle" at Transform (zoom=0.4)
            hover "caution_button_hover"

            hovered Notify("Notification")
            unhovered Notify('')
                    
            action [ToggleLocalVariable('show_dismiss'), SetLocalVariable("show_arrow", False)]

    showif show_dismiss:
        #image("afis_workstation_dim")
        hbox:
            image("notification")
        hbox:
            xalign 0.3 yalign 0.38
            image("caution_button_idle") at Transform(zoom=0.3)
        hbox:
            xalign 0.54 yalign 0.4
            text "The latent fingerprint has finished\nprocessing in the materials lab!"



screen button_style_example():
    frame:
        xalign 0.5 ypos 50

        has vbox

        textbutton "Click me.":
            style "custom_button"
            action Notify("You clicked the button.")

        textbutton "Or me.":
            style "custom_button"
            action Notify("You clicked the other button.")

screen cyano_finish_screen():
    imagemap:
        idle "cyano_hang_evidence" 
        hover "cyano_hang_evidence_gun_hover"
        hotspot(638, 109, 560, 390) action [Function(set_cursor, 'camera_fingerprint'), SetVariable('cyanoacrylate_picture', True), Return()] sensitive current_cursor=='camera'

screen show_match():
    image("match_result_afis")
    hbox:
        xalign 0.51 yalign 0.42
        text"80% match found\nbetween the fingerprints!"
    # hbox:
    #     xalign 0.37 yalign 0.6
    #     text"{size=-6}stove top fingerprint{/size}"
    # hbox:
    #     xalign 0.64 yalign 0.6
    #     text"{size=-6}firearm fingerprint{/size}"

screen wrong_action_screen():
    hbox:
        xalign 0.51 yalign 0.50
        text"Oops... you're not supposed to be here yet!"

screen case_files_screen():
    hbox:
        xpos 0.005 yalign 0.12
        imagebutton:
            idle "case_file_idle" at Transform(zoom=0.45)
            hover "case_file_hover"

            hovered Notify("Case files")
            unhovered Notify('')

            action ToggleVariable('show_case_files')
    

    showif show_case_files:
        default current = {'firearm': False, 'stovetop': False}
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xalign 0.5 ypos 0.1
            text("Case Files")
        
        hbox:
            xpos 0.12 ypos 0.20
            imagebutton:
                idle "firearm" at Transform (zoom=0.4)
                hover "firearm_hover"

                action [ToggleVariable('show_case_files'), SetDict(case_file_dict,'firearm', True),SetDict(case_file_dict,'stovetop', False), 
                SetVariable("bool_show_case", True), Show("show_case", name='Firearm', _layer="over_screens")]
 
        hbox:
            xalign 0.24 ypos 0.49
            text("{color=#000000}Firearm{/color}")
        
        hbox:
            xpos 0.31 ypos 0.20
            imagebutton:
                idle "stovetop" at Transform (zoom=0.4)
                hover "stovetop_hover"

                action [ToggleVariable('show_case_files'), SetDict(case_file_dict,'stovetop', True),SetDict(case_file_dict,'firearm', False),
                SetVariable("bool_show_case", True), Show("show_case", name='Stovetop Fingerprint', _layer="over_screens")]
        hbox:
            xalign 0.44 ypos 0.5
            text("{color=#000000}{size=-11}Stovetop Fingerprint{/size}{/color}")


screen show_case(name):
    showif bool_show_case:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
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
                idle "casefile_evidence" at Transform (zoom=0.4)
                hover "casefile_evidence_hover"

                action [Function(set_current_casefile, 'evidence'), SetVariable("bool_show_case", False),
                SetVariable('bool_show_case_evidence', True), Show("show_case_evidence", process=current_process, _layer="over_screens")]
        hbox:
            xpos 0.22 ypos 0.47
            text("{size=-5}Physical Evidence{/size}")
    
        hbox:
            xpos 0.37 ypos 0.15
            imagebutton:
                idle "casefile_digi_evidence" at Transform (zoom=0.5)
                hover "casefile_digi_evidence_hover"

                action [Function(set_current_casefile, 'digi_evidence'), ToggleVariable("bool_show_case"),
                SetVariable('bool_show_case_digi', True), Show('show_case_digi_evidence', process=current_process, _layer="over_screens")]
        hbox:
            xpos 0.42 ypos 0.47
            text("{size=-5}Digital Evidence{/size}")

        hbox:
            xpos 0.58 ypos 0.18
            imagebutton:
                idle "casefile_report" at Transform (zoom=0.5)
                hover "casefile_report_hover"

                action [Function(set_current_casefile, 'report'), ToggleVariable("bool_show_case"),
                SetVariable('bool_show_case_report', True), Show('show_case_report', process=current_process, _layer="over_screens")]
        
        hbox:
            xpos 0.65 ypos 0.47
            text("{size=-5}Reports{/size}")
    
    # showif not bool_show_case:
    #     hbox:
    #         xalign 0.1 yalign 0.3
    #         image "casefile_inventory"
    #     hbox:
    #         xalign 0.5 ypos 0.1
    #         text(case_type_selected)
    #     if current_casefile['evidence']:
    #         if case_file_dict['firearm']:
    #             showif not evidence_complete_process['firearm']:
    #                 hbox:
    #                     xpos 0.62 ypos 0.3
    #                     textbutton('Process firearm'):
    #                         style "custom_button"
    #                         action [Function(set_cursor, 'evidence_gun'), Function(set_current_evidence, 'firearm'), ToggleVariable('show_evidence')]
    #                         #sensitive process in evidence_process_tool['firearm']
    #             else:
    #                 hbox:
    #                     xpos 0.62 ypos 0.55
    #                     textbutton('Firearm processed'):
    #                         style "custom_button"
    #                         action NullAction() sensitive False
    #             hbox:
    #                 xalign 0.3 yalign 0.3
    #                 imagebutton:
    #                     idle "firearm_evidence" at Transform(zoom=0.08)

    #         if case_file_dict['stovetop']:
    #             showif not evidence_complete_process['backing_card']:
    #                 hbox:
    #                     xpos 0.60 ypos 0.3
    #                     textbutton('Process fingerprint'):
    #                         style "custom_button"
    #                         action [Function(set_cursor, 'backing_card'), Function(set_current_evidence, 'backing_card'), ToggleVariable('show_evidence')]
    #                     #sensitive process in evidence_process_tool['firearm']
    #             else:
    #                 hbox:
    #                     xpos 0.62 ypos 0.55
    #                     textbutton('Fingerprint processed'):
    #                         style "custom_button"
    #                         action NullAction() sensitive False
    #             hbox:
    #                 xalign 0.28 yalign 0.3
    #                 imagebutton:
    #                     idle "evidence_backing_card" at Transform(zoom=0.5)

screen show_case_evidence(process):
    showif bool_show_case_evidence:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("bool_show_case_evidence", False)]
        hbox:
            xalign 0.5 ypos 0.1
            text(case_type_selected)

        if case_file_dict['firearm']:
            showif not evidence_complete_process['firearm']:
                hbox:
                    xpos 0.62 ypos 0.3
                    textbutton('Process firearm'):
                        style "custom_button"
                        action [Function(set_cursor, 'evidence_gun'), Function(set_current_evidence, 'firearm'), SetVariable("bool_show_case_evidence", False)]
                        sensitive process in evidence_process_tool['firearm']
            else:
                hbox:
                    xpos 0.62 ypos 0.3
                    textbutton('Firearm processed'):
                        style "custom_button"
                        action NullAction() sensitive False
            hbox:
                xalign 0.3 yalign 0.3
                imagebutton:
                    idle "firearm_evidence" at Transform(zoom=0.08)



screen show_case_digi_evidence(process):
    showif bool_show_case_digi:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("bool_show_case_digi", False)]
        hbox:
            xalign 0.5 ypos 0.1
            text(case_type_selected)
        
        if case_file_dict['stovetop']:
            showif not evidence_complete_process['backing_card']:
                hbox:
                    xpos 0.60 ypos 0.3
                    textbutton('Process fingerprint'):
                        style "custom_button"
                        action [Function(set_cursor, 'backing_card'), Function(set_current_evidence, 'backing_card'), SetVariable('bool_show_case_digi', False)]
                        sensitive process in evidence_process_tool['backing_card']
            else:
                hbox:
                    xpos 0.62 ypos 0.3
                    textbutton('Fingerprint processed'):
                        style "custom_button"
                        action NullAction() sensitive False
            hbox:
                xalign 0.28 yalign 0.3
                imagebutton:
                    idle "evidence_backing_card" at Transform(zoom=0.5)

        if case_file_dict['firearm']:
            # showif cyanoacrylate_picture:
        #     hbox:
        #         xpos 0.17 ypos 0.19
        #         imagebutton:
        #             idle "evidence_gun_fingerprint" at Transform(zoom=0.9)
        #             hover "evidence_gun_fingerprint"

        #             action [ToggleDict(current, 'firearm_fingerprint'), SetDict(current,'backing_card', False),SetDict(current,'firearm', False), Function(set_evidence_select, 'firearm_fingerprint')]
            showif cyanoacrylate_picture:
        
                showif not evidence_complete_process['firearm_fingerprint']:
                    hbox:
                        xpos 0.60 ypos 0.3
                        textbutton('Process fingerprint'):
                            style "custom_button"
                            action [Function(set_cursor, 'firearm_fingerprint'), Function(set_current_evidence, 'firearm_fingerprint'), SetVariable('bool_show_case_digi', False)]
                            sensitive process in evidence_process_tool['firearm_fingerprint']
                else:
                    hbox:
                        xpos 0.62 ypos 0.3
                        textbutton('Fingerprint processed'):
                            style "custom_button"
                            action NullAction() sensitive False
                hbox:
                    xalign 0.28 yalign 0.3
                    imagebutton:
                        idle "firearm_fingerprint" at Transform(zoom=0.08)


screen show_case_report(process):
    showif bool_show_case_report:
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xpos 0.175 ypos 0.1
            textbutton('Back'):
                style "back_button" 
                action [SetVariable('bool_show_case', True), SetVariable("bool_show_case_report", False)]
        hbox:
            xalign 0.5 ypos 0.1
            text(case_type_selected)




# showif current['firearm_fingerprint']:
        #     showif not evidence_complete_process['firearm_fingerprint']:
        #         hbox:
        #             xpos 0.62 ypos 0.55
        #             textbutton('Process fingerprint'):
        #                 style "custom_button"
        #                 action [Function(set_cursor, 'firearm_fingerprint'), Function(set_current_evidence, 'firearm_fingerprint'), ToggleVariable('show_evidence')]
        #                 sensitive process in evidence_process_tool['firearm_fingerprint'] 
        #     else:
        #         hbox:
        #             xpos 0.62 ypos 0.55
        #             textbutton('Fingerprint processed'):
        #                 style "custom_button"
        #                 action NullAction() sensitive False
        #     hbox:
        #         xpos 0.61 ypos 0.25
        #         text("-fingerprints from\nfirearm")





            

        # showif cyanoacrylate_picture:
        #     hbox:
        #         xpos 0.17 ypos 0.19
        #         imagebutton:
        #             idle "evidence_gun_fingerprint" at Transform(zoom=0.9)
        #             hover "evidence_gun_fingerprint"

        #             action [ToggleDict(current, 'firearm_fingerprint'), SetDict(current,'backing_card', False),SetDict(current,'firearm', False), Function(set_evidence_select, 'firearm_fingerprint')]

        # showif current['firearm_fingerprint']:
        #     showif not evidence_complete_process['firearm_fingerprint']:
        #         hbox:
        #             xpos 0.62 ypos 0.55
        #             textbutton('Process fingerprint'):
        #                 style "custom_button"
        #                 action [Function(set_cursor, 'firearm_fingerprint'), Function(set_current_evidence, 'firearm_fingerprint'), ToggleVariable('show_case_files')]
        #                 sensitive process in evidence_process_tool['firearm_fingerprint'] 
        #     else:
        #         hbox:
        #             xpos 0.62 ypos 0.55
        #             textbutton('Fingerprint processed'):
        #                 style "custom_button"
        #                 action NullAction() sensitive False
        #     hbox:
        #         xpos 0.61 ypos 0.25
        #         text("-fingerprints from\nfirearm")

