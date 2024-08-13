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
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "afis_software_idle"
            hover "afis_software_hover"
            action Jump('afis')
    hbox:
        xpos 0.325 yalign 0.25
        imagebutton:
            idle "dna_software_idle"
            hover "dna_software_hover"
            action Jump('dna')

screen afis_screen:
    # default afis_bg = "software_interface"
    # default interface_import = False
    # default interface_imported = False
    # default interface_search = False
    image afis_bg

    hbox:
        xpos 0.15 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleVariable('show_case_files'),
                Function(set_cursor, '')
                # SetLocalVariable('interface_imported', False),
                # SetLocalVariable('interface_search', False),
                # SetLocalVariable('afis_bg', 'software_interface'),
                # ToggleLocalVariable('interface_import')
            ]
                
    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Prev'):
            style "afis_button"
            action [
                ToggleVariable('interface_search'),
                Function(set_image_idx, 'afis', 'prev'),
                Function(set_cursor, '')]
    
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Next'):
            style "afis_button"
            action [
                ToggleVariable('interface_search'),
                Function(set_image_idx, 'afis', 'next'),
                Function(set_cursor, '')]
    hbox:
        xpos 0.75 ypos 0.145
        textbutton('Compare'):
            style "afis_button"
            action [
                ToggleVariable('interface_search'),
                Function(compare_evidence, current_evidence),
                Function(set_cursor, '')]
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            hotspot (282,241,680,756) action [
                SetVariable('interface_import', False), 
                SetVariable('interface_imported', True),
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    hbox:
        xpos 0.55 ypos 0.3
        image afis_images[afis_image_idx]

screen dna_screen:
    image afis_bg

    hbox:
        xpos 0.15 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleVariable('show_case_files'),
                Function(set_cursor, '')
            ]
                
    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Prev'):
            style "afis_button"
            action [
                ToggleVariable('interface_search'),
                Function(set_image_idx, 'dna', 'prev'),
                Function(set_cursor, '')]
    
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Next'):
            style "afis_button"
            action [
                ToggleVariable('interface_search'),
                Function(set_image_idx, 'dna', 'next'),
                Function(set_cursor, '')]
    hbox:
        xpos 0.75 ypos 0.145
        textbutton('Compare'):
            style "afis_button"
            action [
                ToggleVariable('interface_search'),
                Function(compare_evidence, current_evidence),
                Function(set_cursor, '')]
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            hotspot (282,241,680,756) action [
                SetVariable('interface_import', False), 
                SetVariable('interface_imported', True),
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    hbox:
        xpos 0.5 ypos 0.3
        image dna_images[dna_image_idx]

    

    
#################################### MATERIALS ####################################
screen materials_lab_screen:
    image "materials_lab"

    hbox:
        xpos 0.15 yalign 0.5
        imagebutton:
            idle "wet_lab_idle" at Transform(zoom=0.8)
            hover "wet_lab_hover"
            hovered Notify("Wet Lab")
            unhovered Notify('')
            action Jump('wet_lab')
    hbox:
        xpos 0.325 yalign 0.5
        imagebutton:
            idle "fingerprint_development_idle" at Transform(zoom=0.8)
            hover "fingerprint_development_hover"
            hovered Notify("Fingerprint development")
            unhovered Notify('')
            action Jump('fingerprint_development')
    
    hbox:
        xpos 0.48 yalign 0.5
        imagebutton:
            idle "analytical_instruments_idle" at Transform(zoom=0.8)
            hover "analytical_instruments_hover"
            hovered Notify("Analytical Instruments")
            unhovered Notify('')
            action Jump('analytical_instruments')
    hbox:
        xpos 0.65 yalign 0.5
        imagebutton:
            idle "bio_lab_idle" at Transform(zoom=0.8)
            hover "bio_lab_hover"
            hovered Notify("Bio Lab")
            unhovered Notify('')
            action Jump('bio_lab')



screen analytical_instruments_screen:
    image "lab_bench"
    hbox:
        xpos 0.35 yalign 0.5
        imagebutton:
            idle "headspace_gc_idle"
            hover "headspace_gc_hover"
            hovered Notify("Headspace GC instrument")
            unhovered Notify('')
            action Jump('headspace_gc')

screen fingerprint_development_screen:
    image "materials_lab"

    hbox:
        xpos 0.2 yalign 0.5
        imagebutton:
            idle "ca_fuming_idle"
            hover "ca_fuming_hover"
            hovered Notify("Cyanoacrylate Fuming")
            unhovered Notify('')
            action Jump('fingerprint_ca_fuming')
    
    hbox:
        xpos 0.5 yalign 0.5
        imagebutton:
            idle "lab_bench_idle"
            hover "lab_bench_hover"
            hovered Notify("Lab Bench (Dusting)")
            unhovered Notify('')
            action Jump('fingerprint_lab_bench')
        


##### Lab Bench #####

screen add_bottle_screen():
    hbox:
        xalign 0.5 yalign 0.38
        image "bottle" at Transform(zoom=0.275)

screen bottle_uv_light_screen():
    imagemap:
        xalign 0.5 yalign 0.38
        idle "bottle" at Transform(zoom=0.275)
        hover "bottle_uv_light"
        hotspot (300,1000,1000,1000) action Return("")

screen add_bottle_with_outline_screen():
    hbox:
        xalign 0.5 yalign 0.38
        image "bottle_fingerprint_outline" at Transform(zoom=0.275)

screen bottle_duster_screen():
    imagemap:
        xalign 0.5 yalign 0.38
        idle "bottle_fingerprint_outline" at Transform(zoom=0.275)
        hover "bottle_duster_hover"
        hotspot (300,1000,1000,1000) action Return("")

screen add_bottle_duster():
    hbox:
        xalign 0.5 yalign 0.38
        image "bottle_duster" at Transform(zoom=0.275)

screen bottle_scalebar_screen():
    imagemap:
        xalign 0.5 yalign 0.38
        idle "bottle_duster" at Transform(zoom=0.275)
        hover "bottle_scalebar_hover"
        hotspot (300,1000,1000,1000) action Return("")

screen add_bottle_scalebar():
    hbox:
        xalign 0.5 yalign 0.38
        image "bottle_scalebar" at Transform(zoom=0.275)

screen bottle_lifting_tape_screen():
    imagemap:
        xalign 0.5 yalign 0.38
        idle "bottle_scalebar" at Transform(zoom=0.275)
        hover "bottle_lifting_tape_hover"
        hotspot (300,1000,1000,1000) action Return("")
    
screen add_bottle_lifting_tape():
    hbox:
        xalign 0.5 yalign 0.38
        image "fingerprint_lifted_idle" at Transform(zoom=0.275)

screen bottle_backing_card_screen():
    draggroup:
        drag:
            align(0.3, 0.5)
            drag_raise True
            drag_name "tape"
            draggable True
            droppable False
            dragged dragged_func
            image "/images/bottle/fingerprint_lifted_idle.png" at Transform(zoom=0.3)
        drag:
            align(0.7, 0.43)
            drag_name "backing_card"
            draggable False 
            droppable True
            dragged dragged_func
            image "/images/toolbox/backing_card_idle.png" at Transform(zoom=0.3)

screen bottle_backing_card_complete_screen():
    imagebutton:
        xalign 0.5 yalign 0.1
        idle "fingerprint_lifted_complete" at Transform(zoom=0.4)
        action Return("")

screen open_cyanosafe_screen():
    imagemap:
        idle "cyanosafe_far_closed" 
        hover "cyanosafe_far_closed_hover"
        hotspot(610, 400, 685, 515) action Jump("vase_ca_opened")

screen cyanosafe_enter_chamber_screen():
    imagemap:
        idle "cyanosafe_far_open"
        hover "cyanosafe_far_open_hover"
        hotspot(610, 400, 685, 515) action Jump("vase_select")

screen cyanosafe_add_vase_screen():
    imagemap:
        idle "cyanosafe_hanger_idle"
        hover "cyanosafe_hanger_hover"
        hotspot (325, 120, 1275, 200) action [Return("")]

screen vase_ca_glue_screen():
    imagemap:
        idle "cyanosafe_with_vase"
        hover "cyanosafe_fluids_hover"
        hotspot (500, 800, 500, 350) action Return("")
        hotspot (1000, 800, 500, 300) action Show("vase_ca_wrong_supplement")

screen vase_glue_added_screen():
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "Glue has been added."
            textbutton "Okay" action [Hide("vase_glue_added_screen"), Function(set_cursor, '')]
        
screen vase_ca_wrong_supplement():
    zorder 10
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "Try put it in the other supplment location"
            textbutton "Okay" action [Hide("vase_ca_wrong_supplement"), Function(set_cursor, '')]

screen vase_ca_water_screen():
    imagemap:
        idle "cyanosafe_water_idle"
        hover "cyanosafe_water_hover"
        hotspot (1000, 800, 500, 300) action Return("")

screen vase_water_added_screen():
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "Water has been added."
            textbutton "Okay" action [Hide("vase_water_added_screen"), Function(set_cursor, ''), Return("")]

screen vase_close_chamber_screen():
    imagemap:
        idle "cyanosafe_close_chamber_idle"
        hover "cyanosafe_close_chamber_hover"
        hotspot (1200, 350, 450, 620) action Return("")

screen get_vase_from_chamber():
    imagemap:
        idle "cyanosafe_close_chamber_idle"
        hover "cyanosafe_get_vase"
        hotspot (850, 350, 450, 300) action Return("")

screen vase_ca_complete():
    zorder 10
    hbox:
        xalign 0.5 yalign 0.4
        image "vase_processed" at Transform(zoom=1)
    frame:
        xalign 0.5
        yalign 0.85
        vbox:
            text "The fumed vase has been put into your inventory. \nYou may leave this lab."
            textbutton "Okay" action [Hide("vase_fingerprint_lifted"), Function(set_cursor, ''), Return("")]


screen bottle_pipette():
    imagebutton:
        xalign 0.3 yalign 0.38
        idle "bottle_idle" at Transform(zoom=0.2)
        hover "bottle_hover"
        action [
            If(default_mouse == "pipette", Jump("test"), NullAction()), 
        ]

    imagebutton:
        xalign 0.6 yalign 0.35
        idle "jar_idle" at Transform(zoom=0.2)
        hover "jar_hover"
        action [
            If(default_mouse == "pipette_full", Jump("bottle_headspace_jar_full"), NullAction())
        ]

screen bottle_headspace_jar_complete():
    hbox:
        xalign 0.5 yalign 0.38
        image "jar_full_with_lid" at Transform(zoom=0.275)

screen bottle_headspace_start_screen():
    hbox:
        xalign 0.5 yalign 0.38
        image "bottle" at Transform(zoom=0.275)



screen put_jar_in_gc():
    imagemap:
        idle "gc_instrument_idle" 
        hover "gc_instrument_hover"
        hotspot(300, 300, 500, 500) action [Show("run_gc_instrument_button"), Function(set_cursor, None)]

screen run_gc_instrument_button():
    image "gc_instrument_added_vial"
    frame:
        xalign 0.35
        yalign 0.6
        vbox:
            text "Click to 'Run' Gas Chromatography Spectometer"
            textbutton "Run" action [Hide("run_gc_instrument_button"), Jump('run_gc_questions')]
        
screen gc_spectrograph_result_screen():
    frame:
        xalign 0.5
        yalign 0.8
        vbox:
            text "The results show that the bottle does contain Diphenhydramine."
            textbutton "Okay" action [Hide("gc_spectrograph_result_screen"), 
            Function(set_cursor, ''), Jump("gc_complete")]



screen vase_wet_lab_screen():
    imagebutton:
        xalign 0.5 yalign 0.87
        idle "vase_wet_lab_idle" at Transform(zoom=0.15)
        hover "vase_wet_lab_hover"
        action [
            If(default_mouse == "spray", Jump("vase_wet_lab_sprayed"), NullAction())
        ]

screen vase_sprayed_screen():
    hbox:
        xalign 0.5 yalign 0.87
        image "vase_wet_lab_sprayed" at Transform(zoom=0.15) 

screen vase_wet_lab_light_screen():
    imagemap:
        idle "fumehood_light_idle"
        hover "fumehood_light_hover"
        hotspot(100, 150, 300, 300) action Jump("vase_wet_lab_light")

screen vase_light_fingerprint():
    hbox:
        xalign 0.5 yalign 0.87
        image "vase_light_fingerprint" at Transform(zoom=0.15) 

screen vase_wet_lab_scale:
    zorder 50
    imagemap:
        xalign 0.5 yalign 0.87
        idle "vase_light_fingerprint" at Transform(zoom=0.15)
        hover "vase_scale_hover1"
        hotspot(0, 0, 2048, 2048) action [
            If(default_mouse == "scalebar", Return(""), NullAction())]
    
screen vase_scale_hover_screen():
    hbox:
        xalign 0.5 yalign 0.87
        image "vase_scale_added" at Transform(zoom=0.15) 

screen vase_picture_taken():
    frame:
        xalign 0.5
        yalign 0.85
        vbox:
            text "Picture of fingerprint has been taken and put into your inventory."
            textbutton "Okay" action [Hide("vase_picture_taken"), Function(set_cursor, ''), Return("")]

screen drop_box_screen():
    imagebutton:
        xalign 0.48 yalign 0.4
        idle "drop_box_idle" at Transform(zoom=0.25)
        hover "drop_box_hover"
        action [
            If(default_mouse == "swab_from_vase", Return("swab_from_vase"), NullAction()),
            If(default_mouse == "swab_from_wall", Return("swab_from_wall"), NullAction())
        ]

screen try_something_else():
    frame:
        xalign 0.5
        yalign 0.85
        vbox:
            text "Try something else"
            textbutton "Okay" action [Hide("try_something_else"), Function(set_cursor, ''), Return("")]

screen swab_vase_screen():
    zorder 10
    imagemap:
        xalign 0.5 yalign 0.4
        idle "vase_swab_idle" at Transform(zoom=0.275)
        hover "vase_swab_hover"
        hotspot(500, 300, 700, 1200) action [Return("")]
    
screen vase_after_swabbed():
    imagebutton:
        xalign 0.5 yalign 0.4
        idle "vase_after_swab_idle" at Transform(zoom=0.275)
        hover "vase_after_swab_hover"
        action [Return(""), Function(set_cursor, "vase")]

