screen hallway():
    imagebutton:
        idle "laboratory_idle.jpg"
        hover "laboratory_hover.jpg"
        if wall_done == False or floor_done == False:
            action Jump("laboratory")
        xpos 600
        ypos 450
    
    text "Blood Analysis":
            xpos 630
            ypos 470
            color "#fff"
            size 24

#        idle "monitor idle.png"
#        hover "monitor hover.png"
#        action Jump("monitor")
#        xpos 1000
#        ypos 450
    
#    text "Blood Analysis":
#            xpos 1030
#            ypos 470
#            color "#fff"
#            size 24

screen lab():
    imagebutton:
        idle "heat.png"
        hover "heath.png"
        if step == 2:
            action Jump("heat")
        xpos 500
        ypos 700
    
    text "heating box":
            xpos 530
            ypos 900
            color "#fff"
            size 24

    imagebutton:
        idle "vortex.png"
        hover "vortexh.png"
        if step == 4:
            action Jump("vortex")
        xpos 1100
        ypos 650
    
    text "vortex":
            xpos 1120
            ypos 900
            color "#fff"
            size 24

    imagebutton:
        idle "centrifuge.png"
        hover "centrifugeh.png"
        if step == 5:
            action Jump("centrifuge")
        xpos 765
        ypos 680
    
    text "centrifuge":
            xpos 830
            ypos 900
            color "#fff"
            size 24
    if freezing == False:
        imagebutton:
            idle "freezer.png"
            hover "freezerh.png"
            if step == 8:
                action Jump("freezer")
            xpos 1400
            ypos 500
        
        text "freezer":
                xpos 1450
                ypos 900
                color "#fff"
                size 24


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

    

screen dark_overlay_with_mouse():
    # This is the screen used after pressing the flashlight when analyzing
    # the scissors.
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "left wall idle"
        hover "left wall hover"

        # Handprint
        hotspot (1292, 260, 265, 461) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), SetDict(tools, "gel lifter", True), ToggleScreen("dark_overlay_with_mouse"), Jump("handprint")]

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

screen dark_overlay_with_mouse2():
    # This is the screen used after pressing the flashlight when analyzing
    # the book.
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())

    imagemap:
        idle "baginside idle"
        hover "baginside"

        # Handprint
        hotspot (334, 192, 740, 670) action [SetDict(tools, "uv light", False), SetDict(tools, "magnetic powder", True), ToggleScreen("dark_overlay_with_mouse2"), Jump("fingerprints2")]

    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

screen toolbox_print():
    # This is the toolbox used for the fingerprint and the handprint.
    zorder 1
    hbox:
        xpos 0.89 ypos 0.084
        imagebutton:
            sensitive tools["uv light"]
            auto "uv_light_%s.png" at Transform(zoom=0.06)
            hovered Notify("flashlight")
            action [SetDict(tools, "uv light", False), Show("dark_overlay_with_mouse")]
    
    hbox:
        xpos 0.88 ypos 0.27
        imagebutton:
            sensitive tools["magnetic powder"]
            auto "magnetic_powder_%s.png" at Transform(zoom=0.06)
            hovered Notify("magnetic powder")
            action [SetDict(tools, "magnetic powder", False), If(analyzing["handprint"], [SetDict(tools, "gel lifter", True), Jump("handprint_dusted")], [SetDict(tools, "scalebar", True), Jump("fingerprint_dusted")])]
    
    hbox:
        xpos 0.885 ypos 0.5
        imagebutton:
            sensitive tools["scalebar"]
            auto "scalebar_%s.png" at Transform(zoom=0.6)
            hovered Notify("scalebar")
            action [SetDict(tools, "scalebar", False), SetDict(tools, "tape", True), If(analyzing["handprint"], Jump("handprint_scalebar"), Jump("fingerprint_scalebar"))]
        
    hbox:
        xpos 0.88 ypos 0.65
        imagebutton:
            sensitive tools["tape"]
            auto "tape_%s.png" at Transform(zoom=1)
            hovered Notify("tape")
            action [SetDict(tools, "tape", False), SetDict(tools, "backing", True), If(analyzing["handprint"], Jump("handprint_taped"), Jump("fingerprint_taped"))]
    
    hbox:
        xpos 0.885 ypos 0.8
        imagebutton:
            sensitive tools["backing"]
            auto "backing_card_%s.png" at Transform(zoom=0.6)
            hovered Notify("backing card")
            action [SetDict(tools, "backing", False), SetDict(tools, "packaging", True), If(analyzing["handprint"], Jump("handprint_backing"), Jump("fingerprint_backing"))]
    
    hbox:
        xpos 0 ypos 0.13
        imagebutton:
            sensitive tools["packaging"]
            auto "casefile_evidence_%s.png" at Transform(zoom=0.3)
            hovered Notify("packaging")
            action [SetDict(tools, "packaging", False), SetDict(tools, "tube", True), Jump("packaging")]
    
    hbox:
        xpos 0 ypos 0.34
        imagebutton:
            sensitive tools["gel lifter"]
            auto "gel_lifter_%s.png" at Transform(zoom=0.35)
            hovered Notify("gel lifter")
            action [SetDict(tools, "gel lifter", False), SetDict(tools, "packaging", True), Jump("handprint_gel")]

screen toolbox_blood():
    # This is the toolbox used for the bloody footprint and the splatter.
    # It contains the swab and the hungarian red reagent.
    zorder 1
    hbox:
        xpos 0.13 ypos 0.03
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action [If(analyzing["splatter"], SetDict(analyzing, "splatter", False), SetDict(analyzing, "footprint", False)), Jump("corridor")]
    hbox:
        xpos 0.77 ypos 0.11
        imagebutton:
            sensitive tools["swab"]
            hovered Notify("swab")
            auto "swab_pack_%s.png" at Transform(zoom=0.8)
            action If(analyzing["footprint"], Jump("footprint_swab"), Jump("splatter_swab"))

screen toolbox_presumptive():
    # This is the toolbox used for the presumptive test.
    zorder 1
    hbox:
        xpos 0.88 ypos 0.02
        imagebutton:
            auto "ethanol_%s.png"
            hovered Notify("ethanol")
            action [SetVariable("default_mouse", "ethanol"), ToggleScreen("toolbox_presumptive")] mouse "dropper"
    
    hbox:
        xpos 0.885 ypos 0.26
        imagebutton:
            auto "reagent_%s.png"
            hovered Notify("reagent")
            action [SetVariable("default_mouse", "reagent"), ToggleScreen("toolbox_presumptive")] mouse "dropper"

    hbox:
        xpos 0.885 ypos 0.5
        imagebutton:
            auto "hydrogen_peroxide_%s.png"
            hovered Notify("hydrogen peroxide")
            action [SetVariable("default_mouse", "hydrogen"), ToggleScreen("toolbox_presumptive")] mouse "dropper"

    hbox:
        xpos 0.898 ypos 0.75
        imagebutton:
            auto "trash_%s"
            hovered Notify("trash")

            action Jump("trash")

screen toolbox_packaging():
    # This is the toolbox used for packaging the evidence.
    zorder 1
    hbox:
        xpos 0.89 ypos 0.13
        imagebutton:
            sensitive tools["tube"]
            hovered Notify("tube")
            auto "tube_%s" at Transform(zoom=0.8)
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", True), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_0"))]
    hbox:
        xpos 0.885 ypos 0.32
        imagebutton:
            sensitive tools["bag"]
            auto "evidence_bag_%s" at Transform(zoom=0.9)
            hovered Notify("evidence bag")
            action [SetDict(tools, "tube", False), SetDict(tools, "bag", False), SetDict(tools, "tamper evident tape", True), If(analyzing["fingerprint"] or analyzing["handprint"] or analyzing["gin"], Jump("packaging_1")), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_1"))]
    
    hbox:
        xpos 0.885 ypos 0.51
        imagebutton:
            sensitive tools["tamper evident tape"]
            hovered Notify("tamper evident tape")
            auto "tamper_evident_tape_%s.png" at Transform(zoom=0.9)
            action [SetDict(tools, "tamper evident tape", False), If(analyzing["splatter"] or analyzing["footprint"], Jump("splatter_packaging_2"), Jump("packaging_2"))]


    