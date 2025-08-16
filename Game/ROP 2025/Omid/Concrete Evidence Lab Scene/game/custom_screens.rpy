# initial screen
screen lab_hallway_screen:
    image "lab_hallway_dim"
    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            hovered Notify("Data Analysis Lab")
            unhovered Notify('')
            action Jump('data_analysis_lab')
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            hovered Notify("Materials Lab")
            unhovered Notify('')
            action Jump('materials_lab')

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    # hbox:
    #     xpos 0.25 yalign 0.25
    #     imagebutton:
    #         idle "afis_software_idle"
    #         hover "afis_software_hover"
    #         hovered Notify("AFIS Software")
    #         unhovered Notify('')
    #         action Jump('afis')
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "dna_software_idle"
            hover "dna_software_hover"
            hovered Notify("CODIS DNA Analysis Software")
            unhovered Notify('')
            action Jump('dna_analysis')
    
    hbox:
        xpos 0.35 yalign 0.25
        imagebutton:
            idle "images/data_analysis_lab/faro/faro_software_idle.png"
            hover "images/data_analysis_lab/faro/faro_software_hover.png"
            hovered Notify("FARO Scene Documentation Software")
            unhovered Notify('')
            action Jump('faro_analysis')

screen afis_screen:
    default afis_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    image afis_bg

    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleLocalVariable('interface_import'),
                Show("inventory"), Hide("toolbox"),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('interface_search', False),
                SetLocalVariable('afis_bg', 'software_interface'),
                Function(set_cursor, '')]
    
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Search'):
            sensitive not interface_search
            style "afis_button"
            action [
                ToggleLocalVariable('interface_search'),
                SetLocalVariable('afis_bg', 'software_search'),
                Function(calculate_afis, current_evidence),
                Function(set_cursor, '')]
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            
            ## add in sensitive when clicked on evidence 


            hotspot (282,241,680,756) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    showif interface_search:
        if afis_search:
            for i in range(len(afis_search)):
                hbox:
                    xpos afis_search_coordinates[i]['xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].name+"{/color}")
                hbox:
                    xpos afis_search_coordinates[i]['score_xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['score']+"{/color}")
            
        else:
            hbox:
                xpos 0.57 yalign 0.85
                hbox:
                    text("{color=#000000}No match found in records.{/color}")

screen dna_analysis_screen:
    default dna_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default selected_warrant = ""
    default selected_evidence_id = ""
    default dna_selection_mode = False
    image dna_bg

    # Warrant samples section (right side)
    vbox:
        xpos 0.62 ypos 0.206
        text "{color=#ffffff}Warrant Samples{/color}" size 22
        
    hbox:
        xpos 0.49 ypos 0.225
        spacing -20
        textbutton "Male Suspect":
            style "afis_button"
            action [SetLocalVariable('selected_warrant', 'male')]
        
        textbutton "Female Suspect":
            style "afis_button"
            action [SetLocalVariable('selected_warrant', 'female')]
    
    # Display warrant sample DNA profile image
    if selected_warrant != "":
        vbox:
            xpos 0.55 ypos 0.28
            text "{color=#000000}DNA Profile:{/color}" size 16
            if selected_warrant == "male":
                add "images/data_analysis_lab/male_dna_profile.jpg" at Transform(zoom=0.475)
            elif selected_warrant == "female":
                add "images/data_analysis_lab/female_dna_profile.jpg" at Transform(zoom=0.462)

    # Import evidence section (left side) - now shows DNA selection buttons
    hbox:
        xpos 0.15 ypos 0.145
        textbutton('Import Evidence'):
            style "afis_button"
            sensitive dna_samples_added  # Only available after PCR
            action [
                ToggleLocalVariable('dna_selection_mode'),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('selected_evidence_id', ""),
                SetVariable('dna_comparison_result', '')]
    
    # Compare button
    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Compare'):
            sensitive interface_imported and selected_warrant != "" and selected_evidence_id != ""
            style "afis_button"
            action [
                Function(compare_dna_profiles, selected_evidence_id, selected_warrant),
                Show("dna_result_popup"),
                If(check_analysis_completion(), Jump('analysis_complete'), NullAction())]
    
    # Discard Evidence button
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Discard Evidence'):
            sensitive interface_imported and selected_evidence_id != "" and get_dna_sample_type(selected_evidence_id) == "mixed_dna_profile"
            style "afis_button_wide"
            action [
                Function(discard_mixed_sample, selected_evidence_id),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('selected_evidence_id', ""),
                SetVariable('dna_comparison_result', 'Mixed sample excluded from analysis.'),
                Show("dna_result_popup"),
                If(check_analysis_completion(), Jump('analysis_complete'), NullAction())]

    # DNA Selection Mode - show available DNA samples
    if dna_selection_mode and dna_samples_added:
        vbox:
            xpos 0.155 ypos 0.235
            spacing 10
            text "{color=#000000}Select DNA Sample:{/color}" size 18
            
            for sample in dna_samples_available:
                if dna_samples_status[sample["id"]] == "available":
                    hbox:
                        textbutton sample["name"]:
                            style "afis_button"
                            action [
                                SetLocalVariable('selected_evidence_id', sample["id"]),
                                SetLocalVariable('interface_imported', True),
                                SetLocalVariable('dna_selection_mode', False)]
                elif dna_samples_status[sample["id"]] == "identified_male":
                    hbox:
                        textbutton sample["name"] + " (Male Identified)":
                            style "afis_button_wide"
                            text_color "#00ff00"
                            sensitive False
                            action NullAction()
                elif dna_samples_status[sample["id"]] == "identified_female":
                    hbox:
                        textbutton sample["name"] + " (Female Identified)":
                            style "afis_button_wide"
                            text_color "#00ff00" 
                            sensitive False
                            action NullAction()
                elif dna_samples_status[sample["id"]] == "discarded":
                    hbox:
                        textbutton sample["name"] + " (Discarded)":
                            style "afis_button_wide"
                            text_color "#ff0000"
                            sensitive False
                            action NullAction()
            
            hbox:
                textbutton "Cancel":
                    style "afis_button"
                    action [SetLocalVariable('dna_selection_mode', False)]
    
    elif dna_selection_mode and not dna_samples_added:
        vbox:
            xpos 0.15 ypos 0.235
            text "{color=#ff0000}Complete PCR process first to obtain DNA samples{/color}" size 16
            hbox:
                textbutton "Cancel":
                    style "afis_button"
                    action [SetLocalVariable('dna_selection_mode', False)]

    # Show selected evidence information
    if interface_imported and selected_evidence_id != "":
        vbox:
            xpos 0.16 ypos 0.235
            text "{color=#000000}Evidence DNA Profile:{/color}" size 16
            text "{color=#000000}Loaded: [get_dna_display_name(selected_evidence_id)]{/color}" size 14
            
            # Show appropriate DNA profile image
            $ sample_type = get_dna_sample_type(selected_evidence_id)
            if sample_type == "male_dna_profile":
                add "images/data_analysis_lab/male_dna_profile.jpg" at Transform(zoom=0.475)
            elif sample_type == "female_dna_profile":
                add "images/data_analysis_lab/female_dna_profile.jpg" at Transform(zoom=0.462)
            elif sample_type == "mixed_dna_profile":
                add "images/data_analysis_lab/mixed_dna_profile.jpg" at Transform(zoom=0.475)

screen faro_analysis_screen:
    # FARO Scene Documentation Software with 3D analysis capabilities
    default faro_bg = "software_interface"
    default selected_scene = ""
    default scene_analyzed = {"scene1": False, "scene2": False, "scene3": False}

    # Always show the software interface background
    image faro_bg
    
    # Show scene images as centered overlays when selected
    if selected_scene != "" and not scene_analyzed[selected_scene]:
        # Show pre-analysis image centered on top
        add "images/data_analysis_lab/faro/[selected_scene]_pre_analysis.png" at Transform(xalign=0.5025, yalign=0.5205, xzoom=1.18, yzoom=1.082)
    elif selected_scene != "" and scene_analyzed[selected_scene]:
        # Show analyzed image centered on top
        add "images/data_analysis_lab/faro/[selected_scene]_analyzed.png" at Transform(xalign=0.5025, yalign=0.5205, xzoom=1.18, yzoom=1.082)
    
    # Scene selection buttons (top row)
    hbox:
        xpos 0.15 ypos 0.145
        xsize 750
        spacing 0
        
        textbutton "Scene 1":
            style "afis_button"
            action [SetLocalVariable('selected_scene', 'scene1')]
        
        textbutton "Scene 2":
            style "afis_button"
            action [SetLocalVariable('selected_scene', 'scene2')]
        
        textbutton "Scene 3":
            style "afis_button"
            action [SetLocalVariable('selected_scene', 'scene3')]
        
        if selected_scene == "scene1" and not scene_analyzed["scene1"]:
            $ temp_dict = scene_analyzed.copy()
            $ temp_dict["scene1"] = True
            textbutton "Analyze":
                style "afis_button"
                action [
                    SetLocalVariable('scene_analyzed', temp_dict),
                    SetVariable('scene1_analyzed', True),
                    If(check_analysis_completion(), Jump('analysis_complete'), NullAction())
                ]
        elif selected_scene == "scene2" and not scene_analyzed["scene2"]:
            $ temp_dict = scene_analyzed.copy()
            $ temp_dict["scene2"] = True
            textbutton "Analyze":
                style "afis_button"
                action [
                    SetLocalVariable('scene_analyzed', temp_dict),
                    SetVariable('scene2_analyzed', True),
                    If(check_analysis_completion(), Jump('analysis_complete'), NullAction())
                ]
        elif selected_scene == "scene3" and not scene_analyzed["scene3"]:
            $ temp_dict = scene_analyzed.copy()
            $ temp_dict["scene3"] = True
            textbutton "Analyze":
                style "afis_button"
                action [
                    SetLocalVariable('scene_analyzed', temp_dict),
                    SetVariable('scene3_analyzed', True),
                    If(check_analysis_completion(), Jump('analysis_complete'), NullAction())
                ]
        else:
            textbutton "Analyze":
                style "afis_button"
                sensitive False
                action NullAction()
        
        textbutton "Return":
            style "afis_button"
            action [SetLocalVariable('selected_scene', '')]
    
    # Show scene info when selected
    if selected_scene != "":
        vbox:
            xpos 0.15 ypos 0.31
            spacing 10
            if scene_analyzed[selected_scene]:
                text "{color=#ffffff}Scene [selected_scene.upper()]: ANALYZED{/color}" size 18
                text "{color=#ffffff}Blood spatter analysis complete{/color}" size 14
                text "{color=#ffffff}Trajectory vectors calculated{/color}" size 14
                text "{color=#ffffff}Point of origin determined{/color}" size 14
            else:
                text "{color=#ffffff}Scene [selected_scene.upper()]: READY FOR ANALYSIS{/color}" size 18
                text "{color=#ffffff}3D laser scan data loaded{/color}" size 14
                text "{color=#ffffff}Click 'Analyze Scene' to process{/color}" size 14
    else:
        # Main interface info
        vbox:
            xalign 0.25 yalign 0.35
            spacing 20
            text "{color=#000000}FARO Scene Documentation Software{/color}" size 24 xalign 0.5
            text "{color=#000000}3D Laser Scanning and Point Cloud Analysis{/color}" size 18 xalign 0.5
            text "{color=#000000}Select a scene to begin analysis{/color}" size 16 xalign 0.5

screen materials_lab_screen:
    image "materials_lab"

    # hbox:
    #     xpos 0.15 yalign 0.5
    #     imagebutton:
    #         idle "fumehood_idle" at Transform(zoom=0.8)
    #         hover "fumehood_hover"
    #         hovered Notify("Fume Hood")
    #         unhovered Notify('')
    #         action Jump('fumehood')
    # hbox:
    #     #xpos 0.4 yalign 0.5
    #     xpos 0.32 yalign 0.5
    #     imagebutton:
    #         idle "fingerprint_development_idle" at Transform(zoom=0.8)
    #         hover "fingerprint_development_hover"
    #         hovered Notify("Fingerprint Development")
    #         unhovered Notify('')
    #         action NullAction()
    
    # hbox:
    #     #xpos 0.4 yalign 0.5
    #     xpos 0.48 yalign 0.53
    #     imagebutton:
    #         idle "lab_bench_idle" at Transform(zoom=0.8)
    #         hover "lab_bench_hover"
    #         hovered Notify("Lab Bench")
    #         unhovered Notify('')
    #         action NullAction()
    
    hbox:
        xpos 0.62 yalign 0.5
        imagebutton:
            idle "analytical_instruments_idle"
            hover "analytical_instruments_hover"
            hovered Notify("Analytical Instruments")
            unhovered Notify('')
            action Jump('analytical_instruments')

screen fumehood_screen:
    image "fumehood"

screen analytical_instruments_screen:
    image "lab_bench"
    imagebutton:
        idle "pcr_machine"
        hover "pcr_machine"
        at pcr_machine_transform
        hovered Notify("PCR Machine")
        unhovered Notify('')
        action Jump('pcr_machine')

transform pcr_machine_transform:
    zoom 0.2
    xpos 0.2225
    ypos 0.29

screen pcr_machine_screen:
    # DNA extraction and PCR amplification process with lab assistant guidance
    image "empty_lab_bench"
    
    # Show PCR machine state
    if pcr_state == "empty":
        image "empty_pcr" at pcr_display_transform
    elif pcr_state == "filled":
        image "filled_pcr" at pcr_display_transform
    
    # Track mistakes for final summary
    # pcr_mistakes is a list that accumulates errors
    
    # Lab assistant dialogue and questions
    if pcr_step == 0:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: We need to extract and amplify DNA from this blood swab sample."
            text "First, we'll prepare the sample. What volumes do we need?"
            text "We need: 200µl whole blood, QIAGEN Protease, and Buffer AL."
            
            # Randomize button order
            $ step0_buttons = [
                ("20µl Protease, 200µl Buffer AL", [SetVariable("pcr_step", 1), SetVariable("pcr_state", "filled")]),
                ("50µl Protease, 100µl Buffer AL", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Incorrect protease/buffer volumes. The proper amounts are 20µl Protease and 200µl Buffer AL.")])
            ]
            $ import random
            $ random.shuffle(step0_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step0_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 1:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Good! Now we mix by vortexing and incubate."
            text "What temperature should we use for incubation?"
            
            # Randomize button order
            $ step1_buttons = [
                ("37°C for 15 minutes", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Incorrect incubation temperature. We need 56°C for 10 minutes to properly lyse the cells.")]),
                ("56°C for 10 minutes", [SetVariable("pcr_step", 2)]),
                ("95°C for 5 minutes", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "That's the PCR denaturation temperature, not for sample incubation. We need 56°C for 10 minutes.")])
            ]
            $ random.shuffle(step1_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step1_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 2:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: After incubation and spinning down, we add ethanol."
            text "What concentration of ethanol should we use?"
            
            # Randomize button order
            $ step2_buttons = [
                ("70% ethanol", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "70% ethanol is too dilute. We need 96-100% ethanol for proper DNA precipitation.")]),
                ("96-100% ethanol", [SetVariable("pcr_step", 3)]),
                ("50% ethanol", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "50% ethanol concentration is far too low. We need 96-100% ethanol.")])
            ]
            $ random.shuffle(step2_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step2_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 3:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Now we apply the mixture to the QIAamp spin column."
            text "The DNA binds to the filter. Next, we wash with Buffer AW1."
            text "How much Buffer AW1 should we add?"
            
            # Randomize button order
            $ step3_buttons = [
                ("200µl Buffer AW1", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Insufficient buffer volume. We need 500µl Buffer AW1 for proper washing.")]),
                ("500µl Buffer AW1", [SetVariable("pcr_step", 4)]),
                ("1000µl Buffer AW1", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Excessive buffer volume could damage the column. We need exactly 500µl Buffer AW1.")])
            ]
            $ random.shuffle(step3_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step3_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 4:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: After washing with AW1, we use Buffer AW2."
            text "How long should we centrifuge with AW2?"
            
            # Randomize button order
            $ step4_buttons = [
                ("1 minute", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Insufficient centrifugation time. Buffer AW2 requires 3 minutes for complete salt removal.")]),
                ("3 minutes", [SetVariable("pcr_step", 5)]),
                ("10 minutes", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Excessive centrifugation time could damage the DNA. 3 minutes is optimal.")])
            ]
            $ random.shuffle(step4_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step4_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 5:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Finally, we elute the DNA with Buffer AE."
            text "How much DNA should we use for a 50µl PCR reaction?"
            
            # Randomize button order
            $ step5_buttons = [
                ("5µl extracted DNA", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Too much DNA will inhibit the PCR reaction. Use only 1µl for a 50µl reaction.")]),
                ("1µl extracted DNA", [SetVariable("pcr_step", 6)]),
                ("10µl extracted DNA", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Excessive DNA amount will completely inhibit PCR. Use only 1µl.")])
            ]
            $ random.shuffle(step5_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step5_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 6:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Perfect! The PCR amplification is complete."
            text "Now we need to compare this DNA profile to a reference sample."
            text "What should we compare it against?"
            
            # Randomize button order
            $ step6_buttons = [
                ("Random database profiles", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Incorrect comparison method. We need a specific suspect sample obtained legally.")]),
                ("Blood from accused via warrant", [SetVariable("pcr_step", 7)]),
                ("Any available samples", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "No proper legal authorization. We need blood from the accused obtained via proper warrant.")])
            ]
            $ random.shuffle(step6_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step6_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 7:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Excellent work! You completed the DNA extraction"
            text "and PCR amplification process perfectly."
            
            textbutton "Complete Analysis":
                style "back_button"
                xalign 0.5
                action [SetVariable("pcr_step", 8)]
    
    elif pcr_step == 8:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Okay, now let me get through the rest of the swabs."
            text "Great! But we have three profiles... I thought there were only two people involved?"
            text "Anyway, they've been added to your evidence toolbox for analysis."
            
            textbutton "Continue":
                style "back_button"
                xalign 0.5
                action [SetVariable("pcr_step", 0), SetVariable("pcr_state", "empty"),
                        Function(add_dna_samples), Jump('analytical_instruments')]
    
    elif pcr_step == -1:  # Error state
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: [pcr_error]"
            text "In forensic analysis, precision is critical. Any deviation from"
            text "the proper protocol could compromise the evidence in court."
            text "We need to start over with a fresh sample."
            
            hbox:
                xalign 0.5
                spacing 20
                textbutton "Start Over":
                    style "back_button"
                    action [SetVariable("pcr_step", 0), SetVariable("pcr_state", "empty"),
                            SetVariable("pcr_error", "")]
                textbutton "Return to Lab":
                    style "back_button"
                    action [SetVariable("pcr_step", 0), SetVariable("pcr_state", "empty"),
                            SetVariable("pcr_error", ""), Jump('analytical_instruments')]

screen analysis_complete_screen:
    # Congratulations screen similar to the first lab hallway screen
    image "lab_hallway_dim"
    
    # Main congratulations message
    vbox:
        xalign 0.5 yalign 0.4
        spacing 30
        
        text "{color=#ffffff}CONGRATULATIONS!{/color}" size 48 xalign 0.5
        text "{color=#ffffff}All the data has been successfully processed.{/color}" size 24 xalign 0.5
        text "{color=#ffffff}Time to prepare a report for court!{/color}" size 24 xalign 0.5
        
        # Summary of completed tasks
        vbox:
            xalign 0.5
            spacing 15
            if scene1_analyzed:
                text "{color=#00ff00}✓ Scene 1 trajectory analyzed{/color}" size 18 xalign 0.5
            if scene2_analyzed:
                text "{color=#00ff00}✓ Scene 2 trajectory analyzed{/color}" size 18 xalign 0.5
            if scene3_analyzed:
                text "{color=#00ff00}✓ Scene 3 trajectory analyzed{/color}" size 18 xalign 0.5
            if male_dna_identified:
                text "{color=#00ff00}✓ Male DNA profile identified{/color}" size 18 xalign 0.5
            if female_dna_identified:
                text "{color=#00ff00}✓ Female DNA profile identified{/color}" size 18 xalign 0.5
            if mixed_dna_discarded:
                text "{color=#00ff00}✓ Mixed DNA sample discarded{/color}" size 18 xalign 0.5
    
    # End game button
    hbox:
        xalign 0.5 yalign 0.8
        textbutton "End Simulation":
            style "back_button"
            action [Return()]

screen dna_result_popup:
    # Semi-transparent background overlay
    add "#000000aa"
    
    # Main popup box
    frame:
        xalign 0.5 yalign 0.5
        xsize 800
        ysize 400
        background Frame("gui/frame.png", 12, 12)
        
        vbox:
            xalign 0.5 yalign 0.5
            spacing 30
            
            # Title
            text "DNA Analysis Complete" size 32 xalign 0.5 color "#ffffff"
            
            # Result text
            text "[dna_comparison_result]" size 24 xalign 0.5 color "#ffffff" text_align 0.5
            
            # Close button
            textbutton "Continue":
                style "afis_button"
                xalign 0.5
                action [Hide("dna_result_popup")]

transform pcr_display_transform:
    zoom 0.35
    xpos 0.32
    ypos 0.2