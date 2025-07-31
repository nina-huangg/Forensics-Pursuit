# initial screen
screen lab_hallway_screen:
    image "lab_hallway_dim"
    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            # hovered Notify("Data Analysis Lab")
            # unhovered Notify('')
            action Jump('data_analysis_lab')
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            # hovered Notify("Materials Lab")
            # unhovered Notify('')
            action Jump('materials_lab')

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "afis_software_idle"
            hover "afis_software_hover"
            action Jump("computer")

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
                ToggleVariable('show_case_files'),
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

    

    
#################################### MATERIALS ####################################
screen materials_lab_screen:
    image "materials_lab"

    # hbox:
    #     xpos 0.15 yalign 0.5
    #     imagebutton:
    #         idle "wet_lab_idle"
    #         hover "wet_lab_hover"
    #         hovered Notify("Wet Lab")
    #         unhovered Notify('')
    #         action Jump('wet_lab')
    # hbox:
    #     xpos 0.26 yalign 0.5
    #     imagebutton:
    #         auto "oven_%s" at Transform(zoom=0.7)
    #         # hovered Notify("Dry Oven")
    #         # unhovered Notify('')
    #         action [SetVariable("location", "oven"), Jump("oven")]
    # text "Dry Oven" xpos 0.31 ypos 0.66
    
    # hbox:
    #     xpos 0.52 yalign 0.5
    #     imagebutton:
    #         auto "fumehood_%s" at Transform(zoom=0.95)
    #         # hovered Notify("Fumehood")
    #         # unhovered Notify('')
    #         action [SetVariable("location", "fumehood"), Jump("fumehood")]
    # text "Fumehood" xpos 0.59 ypos 0.67

    hbox:
        xpos 0.52 yalign 0.5
        imagebutton:
            idle "materials_lab/ICP_idle.png"
            hover "materials_lab/ICP_hover.png"
            action [SetVariable("location", "ICP"), Jump("icp_analysis")]
    text "ICP" xpos 0.59 ypos 0.67

    # Grinder&Scale_idle.png

    hbox:
        xpos 0.20 yalign 0.32
        imagebutton:
            idle "Grinder&Scale_idle.png"
            hover "Grinder&Scale_hover.png"
            action [SetVariable("location", "grinder"), Jump("grinder")]
    text "Grinder & Scale" xpos 0.24 ypos 0.67

screen wet_lab_screen:
    image "fumehood"

screen analytical_instruments_screen:
    image "lab_bench"


# images\materials_lab\scale_and_grinder_hover.png
screen grinder:
    imagemap:
        idle "materials_lab/scale_and_grinder_idle.png"
        hover "materials_lab/scale_and_grinder_hover.png"
        hotspot (607, 717, 267, 224) action [SetVariable("location", "grinder")]
        hotspot (1038, 474, 424, 491) action [SetVariable("location", "grinder")]

screen grindering:
    zorder 1
    imagemap:
        idle "materials_lab/grinder_idle.png"
        hover "materials_lab/grinder_idle.png"
        hotspot (607, 717, 267, 224) action [SetVariable("location", "grindering")]
        hotspot (1038, 474, 424, 491) action [SetVariable("location", "grindering")]

screen digestion:
    zorder 1
    imagemap:
        idle "materials_lab/digestion_idle.png"
        hover "materials_lab/digestion_idle.png"
        # 你可以根据需要添加热点区域
        # hotspot (x, y, width, height) action [SetVariable("location", "digestion")]

# ICP Periodic Table Screen
screen icp_periodic_table():
    zorder 1
    imagemap:
        idle "materials_lab/ICP_periodic_idle.png"
        hover "materials_lab/ICP_periodic_hover.png"
        
        # Group 1 - Alkali Metals
        hotspot (324, 197, 66, 70) action Function(toggle_element, "H")     # Hydrogen
        hotspot (323, 269, 67, 66) action Function(toggle_element, "Li")    # Lithium
        hotspot (323, 337, 69, 70) action Function(toggle_element, "Na")    # Sodium
        hotspot (323, 408, 68, 67) action Function(toggle_element, "K")     # Potassium
        hotspot (324, 475, 68, 74) action Function(toggle_element, "Rb")    # Rubidium
        hotspot (323, 548, 69, 69) action Function(toggle_element, "Cs")    # Cesium
        hotspot (323, 619, 69, 69) action Function(toggle_element, "Fr")    # Francium

        # Group 2 - Alkaline Earth Metals
        hotspot (392, 267, 70, 69) action Function(toggle_element, "Be")    # Beryllium
        hotspot (392, 337, 70, 69) action Function(toggle_element, "Mg")    # Magnesium
        hotspot (392, 408, 70, 69) action Function(toggle_element, "Ca")    # Calcium
        hotspot (392, 475, 70, 69) action Function(toggle_element, "Sr")    # Strontium
        hotspot (392, 548, 70, 69) action Function(toggle_element, "Ba")    # Barium
        hotspot (392, 619, 70, 69) action Function(toggle_element, "Ra")    # Radium

        # Transition Metals (Row 4)
        hotspot (462, 406, 71, 71) action Function(toggle_element, "Sc")   # Scandium
        hotspot (534, 408, 67, 69) action Function(toggle_element, "Ti")   # Titanium
        hotspot (603, 407, 70, 69) action Function(toggle_element, "V")    # Vanadium
        hotspot (673, 407, 70, 69) action Function(toggle_element, "Cr")   # Chromium
        hotspot (743, 407, 70, 69) action Function(toggle_element, "Mn")   # Manganese
        hotspot (813, 407, 70, 69) action Function(toggle_element, "Fe")   # Iron
        hotspot (883, 407, 70, 69) action Function(toggle_element, "Co")   # Cobalt
        hotspot (953, 407, 70, 69) action Function(toggle_element, "Ni")   # Nickel
        hotspot (1023, 407, 70, 69) action Function(toggle_element, "Cu")   # Copper
        hotspot (1093, 407, 70, 69) action Function(toggle_element, "Zn")   # Zinc

        # Groups 13‑18 – period 3  (row aligned to y = 337)
        hotspot (1162, 337, 69, 68) action Function(toggle_element, "Al")   # Aluminum
        hotspot (1232, 336, 70, 71) action Function(toggle_element, "Si")   # Silicon
        hotspot (1302, 335, 70, 71) action Function(toggle_element, "P")    # Phosphorus
        hotspot (1372, 335, 70, 71) action Function(toggle_element, "S")    # Sulfur
        hotspot (1442, 335, 70, 71) action Function(toggle_element, "Cl")   # Chlorine
        hotspot (1512, 335, 70, 71) action Function(toggle_element, "Ar")   # Argon

        # Post-transition metals and metalloids (Row 4)
        hotspot (1162, 406, 70, 70) action Function(toggle_element, "Ga")   # Gallium
        hotspot (1232, 406, 70, 70) action Function(toggle_element, "Ge")   # Germanium
        hotspot (1302, 406, 70, 70) action Function(toggle_element, "As")   # Arsenic
        hotspot (1372, 406, 70, 70) action Function(toggle_element, "Se")   # Selenium
        hotspot (1442, 406, 70, 70) action Function(toggle_element, "Br")   # Bromine
        hotspot (1512, 406, 70, 70) action Function(toggle_element, "Kr")   # Krypton

        # # Heavy metals (Row 5)
        # hotspot (450, 340, 40, 40) action Function(toggle_element, "Ag")   # Silver
        # hotspot (490, 340, 40, 40) action Function(toggle_element, "Cd")   # Cadmium
        # hotspot (530, 340, 40, 40) action Function(toggle_element, "In")   # Indium
        # hotspot (570, 340, 40, 40) action Function(toggle_element, "Sn")   # Tin
        # hotspot (610, 340, 40, 40) action Function(toggle_element, "Sb")   # Antimony
        
        # # Heavy metals (Row 6)
        # hotspot (450, 380, 40, 40) action Function(toggle_element, "Au")   # Gold
        # hotspot (490, 380, 40, 40) action Function(toggle_element, "Hg")   # Mercury
        # hotspot (530, 380, 40, 40) action Function(toggle_element, "Tl")   # Thallium
        # hotspot (570, 380, 40, 40) action Function(toggle_element, "Pb")   # Lead
        # hotspot (610, 380, 40, 40) action Function(toggle_element, "Bi")   # Bismuth
        
        # # More transition metals (Row 5)
        # hotspot (130, 340, 40, 40) action Function(toggle_element, "Y")    # Yttrium
        # hotspot (170, 340, 40, 40) action Function(toggle_element, "Zr")   # Zirconium
        # hotspot (210, 340, 40, 40) action Function(toggle_element, "Nb")   # Niobium
        # hotspot (250, 340, 40, 40) action Function(toggle_element, "Mo")   # Molybdenum
        # hotspot (290, 340, 40, 40) action Function(toggle_element, "Tc")   # Technetium
        # hotspot (330, 340, 40, 40) action Function(toggle_element, "Ru")   # Ruthenium
        # hotspot (370, 340, 40, 40) action Function(toggle_element, "Rh")   # Rhodium
        # hotspot (410, 340, 40, 40) action Function(toggle_element, "Pd")   # Palladium
        
        # # More transition metals (Row 6)
        # hotspot (130, 380, 40, 40) action Function(toggle_element, "La")   # Lanthanum  
        # hotspot (170, 380, 40, 40) action Function(toggle_element, "Hf")   # Hafnium
        # hotspot (210, 380, 40, 40) action Function(toggle_element, "Ta")   # Tantalum
        # hotspot (250, 380, 40, 40) action Function(toggle_element, "W")    # Tungsten
        # hotspot (290, 380, 40, 40) action Function(toggle_element, "Re")   # Rhenium
        # hotspot (330, 380, 40, 40) action Function(toggle_element, "Os")   # Osmium
        # hotspot (370, 380, 40, 40) action Function(toggle_element, "Ir")   # Iridium
        # hotspot (410, 380, 40, 40) action Function(toggle_element, "Pt")   # Platinum
    
    # Display selected elements
    text "Selected Elements: [', '.join(selected_elements)]" xpos 50 ypos 50 size 20 color "#FFFFFF"
    
    # Display selection message with auto-clear timer
    if element_selection_message:
        text element_selection_message xpos 50 ypos 80 size 18 color "#FFFF00"
        timer 2.0 action Function(clear_element_message)
    
    # Analysis button
    if len(selected_elements) > 0:
        textbutton "Start ICP Analysis" action Jump("icp_results") xpos 50 ypos 120