
################################################################################
## In-game screens
################################################################################

# Drag and drop screen
screen drag_and_drop(drag_name, drag_image, drop_name, drop_image):
    draggroup:
        drag:
            drag_name drag_name
            draggable True
            droppable False

            dragged item_dragged_package
            dragging item_dragging_package

            xpos 400
            ypos 250

            add drag_image
        drag:
            drag_name drop_name
            draggable False
            droppable True

            xpos 900
            ypos 250

            add drop_image

# ---------------------------------------------------------------------------
# Generic drug processing screen
# ---------------------------------------------------------------------------

screen drug_processing_screen(drop_image, drop_xpos, drop_ypos):
    draggroup:
        if selected_tool is not None:
            drag:
                drag_name selected_tool
                draggable True
                droppable False
                dragging item_dragging_package
                dragged  generic_drop
                xpos 0.75 ypos 0.35
                child Transform(selected_tool, zoom=1.5)
        drag:
            drag_name drop_image
            draggable False
            droppable True
            xalign 0.5 yalign 0.5
            child Transform(drop_image, zoom=2)

screen drug_collection_screen():
    modal True
    imagebutton:
        idle "casefile_evidence_idle"
        hover "casefile_evidence_hover"
        at Transform(zoom=2)
        xalign 0.5
        yalign 0.5
        action [
            SetVariable("collect_step_flag", True),
            Return()
        ]
        
screen placed_marker_display(marker_image):
    add marker_image at Transform(xpos=0.2, ypos=0.1)

screen investigation_buttons():
    # get the order of the evidence markers
    $ _order = evidence_visited_order
    $ sample1_num       = (_order.index("sample1")  + 1) if "sample1"   in _order else None
    $ sample2_num       = (_order.index("sample2")  + 1) if "sample2"   in _order else None
    $ sample3_num       = (_order.index("sample3")  + 1) if "sample3"   in _order else None
    $ firearm_num       = (_order.index("firearm")  + 1) if "firearm"   in _order else None
    $ cash_num          = (_order.index("cash")     + 1) if "cash"      in _order else None

    if not evidence_found["sample1_processed"] and not evidence_found["sample1_packaged"]:
        imagebutton:
            xpos 0.43 ypos 0.67
            idle  ("sample1_idle" if not evidence_found["sample1_presumptive"] else "cocaine_blue")
            hover ("sample1_hover" if not evidence_found["sample1_presumptive"] else "cocaine_blue")
            mouse "hover"
            hovered   Notify("Suspected drugs")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "sample1"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if sample1_num is not None:
            add ("marker_" + str(sample1_num)) at Transform(xpos=0.43, ypos=0.67)
    elif evidence_found["sample1_packaged"]:
        if sample1_num is not None:
            add ("marker_" + str(sample1_num)) at Transform(xpos=0.43, ypos=0.67)
    
    if not evidence_found["sample2_processed"] and not evidence_found["sample2_packaged"]:
        imagebutton:
            xpos 0.32 ypos 0.54
            idle  ("sample2_idle" if not evidence_found["sample2_presumptive"] else "cocaine_blue")
            hover ("sample2_hover" if not evidence_found["sample2_presumptive"] else "cocaine_blue")
            mouse "hover"
            hovered   Notify("Suspected drugs")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "sample2"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if sample2_num is not None:
            add ("marker_" + str(sample2_num)) at Transform(xpos=0.32, ypos=0.54)
    elif evidence_found["sample2_packaged"]:
        add ("marker_" + str(sample2_num)) at Transform(xpos=0.32, ypos=0.54)

    if not evidence_found["sample3_processed"] and not evidence_found["sample3_packaged"]:
        imagebutton:
            xpos 0.66 ypos 0.52
            idle  ("sample3_idle" if not evidence_found["sample3_presumptive"] else "cocaine_blue")
            hover ("sample3_hover" if not evidence_found["sample3_presumptive"] else "cocaine_blue")
            mouse "hover"
            hovered   Notify("Suspected drugs")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "sample3"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if sample3_num is not None:
            add ("marker_" + str(sample3_num)) at Transform(xpos=0.66, ypos=0.52)
    elif evidence_found["sample3_packaged"]:
        add ("marker_" + str(sample3_num)) at Transform(xpos=0.66, ypos=0.52)
    
    if not evidence_found["firearm_processed"] and not evidence_found["firearm_packaged"]:
        imagebutton:
            xpos 0.30 ypos 0.21
            idle  "firearm_idle"
            hover "firearm_hover"
            mouse "hover"
            hovered   Notify("Firearm")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "firearm"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if firearm_num is not None:
            add ("marker_" + str(firearm_num)) at Transform(xpos=0.30, ypos=0.21)
    elif evidence_found["firearm_packaged"]:
        add ("marker_" + str(firearm_num)) at Transform(xpos=0.30, ypos=0.21)

    if not evidence_found["cash_processed"] and not evidence_found["cash_packaged"]:
        imagebutton:
            xpos 0.16 ypos 0.57
            idle  "cash_idle"
            hover "cash_hover"
            mouse "hover"
            hovered   Notify("Piles of cash")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "cash"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if cash_num is not None:
            add ("marker_" + str(cash_num)) at Transform(xpos=0.16, ypos=0.57)
    elif evidence_found["cash_packaged"]:
        add ("marker_" + str(cash_num)) at Transform(xpos=0.16, ypos=0.57)

    if (evidence_found["sample1_packaged"]
        and evidence_found["sample2_packaged"]
        and evidence_found["sample3_packaged"]
        and evidence_found["firearm_packaged"]
        and evidence_found["cash_packaged"]):
        textbutton "Finish Investigation":
            xpos 0.75 ypos 0.9
            style "hud_button"
            background "#030364"
            hover_background "#b5b5ff"
            action Jump("investigation_complete")

screen colour_chart(chart_image):
    modal False
    add chart_image at Transform(zoom=1.2, xalign=0.3, yalign=0.2)

screen reagent_result(item):
    modal False
    $ _reagent = current_reagent.get(item)
    if _reagent == "marquis":
        add "sample1_tube" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)
    elif _reagent == "scott":
        add "cocaine_blue_pink" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)

# lab start
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

############################## DATA ANALYSIS LAB CODE HERE ##############################
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

    
#################################### MATERIALS LAB CODE HERE ####################################
screen materials_lab_screen:
    image "materials_lab"

    hbox:
        xpos 0.26 yalign 0.1
        imagebutton:
            idle "gcms_idle"
            hover "gcms_hover"
            action [SetVariable("location", "gcms"), Jump("gcms")]
    text "GC-MS" xpos 0.33 ypos 0.43

    hbox:
        xpos 0.52 yalign 0.1
        imagebutton:
            idle "ca_chamber_idle"
            hover "ca_chamber_hover"
            action [SetVariable("location", "ca_chamber"), Jump("ca_chamber")]    
    text "Cyanoacrylate Chamber" xpos 0.52 ypos 0.43

    hbox:
        xpos 0.26 yalign 0.7
        imagebutton:
            idle "solid_phase_extraction_idle"
            hover "solid_phase_extraction_hover"
            action [SetVariable("location", "solid_phase_extraction"), Jump("solid_phase_extraction")]
    text "Solid Phase Extraction" xpos 0.29 ypos 0.8

    hbox:
        xpos 0.53 yalign 0.7
        imagebutton:
            idle "analytical_balance_idle"
            hover "analytical_balance_hover"
            action [SetVariable("location", "analytical_balance"), Jump("analytical_balance")]
    text "Analytical Balance" xpos 0.52 ypos 0.8

screen ca_chamber_screen():
    $ bg_image = (
        "ca_chamber_closed" if (ca_chamber_done or ca_chamber_state in ("closed", "loaded"))
        else "ca_chamber_firearm" if ca_chamber_firearm_placed
        else "ca_chamber_empty"
    )
    add bg_image at Transform(xalign=0.5, yalign=0.5, rotate=90, zoom=1.4)

    if not ca_chamber_done:
        if ca_chamber_state == "empty":
            draggroup:
                if selected_tool is not None:
                    drag:
                        drag_name selected_tool
                        draggable True
                        droppable False
                        dragging item_dragging_package
                        dragged  ca_chamber_drop
                        xpos 0.65 ypos 0.60
                        child Transform(selected_tool, zoom=1.5)
                drag:
                    drag_name "ca_chamber_dropzone"
                    draggable False
                    droppable True
                    xalign 0.5 yalign 0.5
                    child Transform(Solid("#00000000"), size=(300, 300))

            textbutton "Close Chamber":
                xalign 0.5 ypos 0.85
                xsize 400 ysize 90
                text_size 42
                text_color "#ffffff"
                text_align 0.5
                background "#012a4a"
                hover_background "#0466c8"
                insensitive_background "#3a3a3a"
                sensitive (ca_chamber_water_added and ca_chamber_glue_added and ca_chamber_firearm_placed)
                action Function(close_ca_chamber)

        elif ca_chamber_state == "closed":
            textbutton "Set Temperature & Time":
                xalign 0.5 ypos 0.85
                xsize 480 ysize 90
                text_size 42
                text_color "#ffffff"
                text_align 0.5
                background "#012a4a"
                hover_background "#0466c8"
                action Jump("ca_chamber_load_dialogue")

screen ca_chamber_checklist():
    add "images/materials_lab/ca_chamber/ca_fuming_checklist/ca_fuming_checklist_%d.png" % ca_chamber_step:
        xalign 0.999999
        yalign 0.3
        
screen ca_chamber_amount_check():
    modal True
    if ca_pending_mcq == "water":
        frame:
            xalign 0.5 yalign 0.5
            padding (30, 30)
            vbox:
                spacing 15
                text "How much distilled water will you add?" size 36
                textbutton "50 mL"  action Function(check_ca_amount, "water", 50)
                textbutton "100 mL" action Function(check_ca_amount, "water", 100)
                textbutton "300 mL" action Function(check_ca_amount, "water", 300)
    elif ca_pending_mcq == "glue":
        frame:
            xalign 0.5 yalign 0.5
            padding (30, 30)
            vbox:
                spacing 15
                text "How many drops of superglue will you add?" size 36
                textbutton "2 drops"   action Function(check_ca_amount, "glue", 2)
                textbutton "5 drops"  action Function(check_ca_amount, "glue", 5)
                textbutton "10 drops" action Function(check_ca_amount, "glue", 10)

screen spe_spo(): # the solid phase extraction checklist
    if(step_num_SPE == 1 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full1.png":
            xalign 0.999999
    elif(step_num_SPE == 1 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half1.png":
            xalign 0.999999
    elif(step_num_SPE <= 2 and spe_difficulty == 2):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_low1.png":
            xalign 0.999999
    elif(step_num_SPE == 2 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full2.png":
            xalign 0.999999
    elif(step_num_SPE == 2 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half2.png":
            xalign 0.999999
    elif(step_num_SPE <= 3 and spe_difficulty == 2):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_low2.png":
            xalign 0.999999
    elif(step_num_SPE == 3 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full3.png":
            xalign 0.999999
    elif(step_num_SPE == 3 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half3.png":
            xalign 0.999999
    elif(step_num_SPE <= 5 and spe_difficulty == 2):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_low3.png":
            xalign 0.999999
    elif(step_num_SPE == 4 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full4.png":
            xalign 0.999999
    elif(step_num_SPE == 4 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half4.png":
            xalign 0.999999
    elif(step_num_SPE <= 6 and spe_difficulty == 2):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_low4.png":
            xalign 0.999999
    elif(step_num_SPE == 5 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full5.png":
            xalign 0.999999
    elif(step_num_SPE == 5 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half5.png":
            xalign 0.999999
    elif(step_num_SPE <= 7 and spe_difficulty == 2):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_low5.png":
            xalign 0.999999
    elif(step_num_SPE == 6 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full6.png":
            xalign 0.999999
    elif(step_num_SPE == 6 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half6.png":
            xalign 0.999999
    elif(step_num_SPE == 7 and spe_difficulty == 0):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_full7.png":
            xalign 0.999999
    elif(step_num_SPE == 7 and spe_difficulty == 1):
        add "images/materials_lab/spe/spe_checklist/spe_checklist_half7.png":
            xalign 0.999999

screen lab_notebook():
    modal True
    add Solid("#000c")
    frame:
        align (0.5, 0.5)
        xsize 700
        ysize 500
        background "#f1eff4"
        padding (30, 30)

        vbox:
            spacing 15
            text "{b}Lab Notebook{/b}" size 40 color "#012a4a"
            text "Sample Weights:" size 30 color "#474646"
            for drug, weights in drug_weights.items():
                $ net = weights["net"]
                $ gross = weights["gross"]
                $ _label = _SAMPLE_DISPLAY_NAME[drug]
                text (f"Presumed Drug {_label}: " + (f"{net} g" if net is not None else "not yet weighed")) size 24 color "#474646"
                text (f"Presumed Drug {_label} Bag: " + (f"{gross} g" if gross is not None else "not yet weighed")) size 24 color "#474646"

        textbutton "✕":
            xalign 0.95 yalign 0.05
            action Hide("lab_notebook")
            
screen analytical_balance_screen():
    add "analytical_balance_zero" at Transform(xalign=0.5, yalign=0.5)

    if balance_state == "result":
        $ _result_img = "analytical_balance_%s_%s" % (balance_result_type, balance_result_drug)
        add _result_img at Transform(xalign=0.5, yalign=0.5)

        textbutton "Remove Sample":
            xalign 0.5 ypos 0.85
            xsize 400 ysize 90
            text_size 42
            text_color "#ffffff"
            text_align 0.5
            background "#012a4a"
            hover_background "#0466c8"
            action Function(clear_balance)

    else:
        if not all(weighed_net.values()) or weighboat_state == "loaded":
            draggroup:
                if selected_tool == "spatula_idle":
                    drag:
                        drag_name selected_tool
                        draggable True
                        droppable False
                        dragging item_dragging_package
                        dragged  sample_bag_drop
                        xpos 0.85 ypos 0.65
                        child Transform(selected_tool, zoom=1.2)
                elif selected_tool == "spatula_powder":
                    drag:
                        drag_name selected_tool
                        draggable True
                        droppable False
                        dragging item_dragging_package
                        dragged  weighboat_drop
                        xpos 0.85 ypos 0.65
                        child Transform(selected_tool, zoom=1.2)

                for _drug in ["sample1", "sample2", "sample3"]:
                    if not weighed_net[_drug]:
                        $ _tx = {"sample1": 0.15, "sample2": 0.25, "sample3": 0.35}[_drug]
                        drag:
                            drag_name (_drug + "_idle")
                            draggable False
                            droppable True
                            xpos _tx ypos 0.75
                            child Transform((_drug + "_idle"), zoom=1.2)

                if weighboat_state == "empty":
                    drag:
                        drag_name "weighboat_dropzone"
                        draggable False
                        droppable True
                        xpos 0.5 ypos 0.75
                        child Transform("weighboat_idle", zoom=1.2)

        if weighboat_state == "loaded":
            draggroup:
                drag:
                    drag_name "weighboat_loaded"
                    draggable True
                    droppable False
                    dragging item_dragging_package
                    dragged  analytical_balance_drop
                    xpos 0.5 ypos 0.75
                    child Transform("weighboat_loaded", zoom=1.2)
                drag:
                    drag_name "analytical_balance_dropzone"
                    draggable False
                    droppable True
                    xalign 0.5 yalign 0.35
                    child Transform(Solid("#00000000"), size=(300, 300))

        draggroup:
            if selected_tool in ("inventory-sample1", "inventory-sample2", "inventory-sample3"):
                drag:
                    drag_name selected_tool
                    draggable True
                    droppable False
                    dragging item_dragging_package
                    dragged  analytical_balance_drop
                    xpos 0.75 ypos 0.55
                    child Transform(selected_tool, zoom=1.2)
            drag:
                drag_name "analytical_balance_dropzone"
                draggable False
                droppable True
                xalign 0.5 yalign 0.35
                child Transform(Solid("#00000000"), size=(300, 300))

screen gcms_checklist():
    add "images/materials_lab/gcms/gcms_checklist/gcms_checklist_%d.png" % gcms_step:
        xalign 0.999999
        yalign 0.3

screen gcms_screen():
    $ bg = "gc_autosampler_background" if gcms_step in (3, 4) else "gcms_background"
    add bg at Transform(xalign=0.5, yalign=0.5)

    if gcms_step == 3:
        draggroup:
            if selected_tool is not None:
                drag:
                    drag_name selected_tool
                    draggable True
                    droppable False
                    dragging item_dragging_package
                    dragged  gcms_autosampler_drop
                    xpos 0.65 ypos 0.60
                    child Transform(selected_tool, zoom=1.5)
            drag:
                drag_name "gcms_autosampler_dropzone"
                draggable False
                droppable True
                xalign 0.5 yalign 0.5
                child Transform(Solid("#00000000"), size=(300, 300))

    elif gcms_step == 4:
        textbutton "Start Run":
            xalign 0.5 ypos 0.85
            xsize 400 ysize 90
            text_size 42
            text_color "#ffffff"
            text_align 0.5
            background "#012a4a"
            hover_background "#0466c8"
            action Jump("gcms_set_time")

    elif gcms_step == 8:
        textbutton "Open Comparison Interface":
            xalign 0.5 ypos 0.85
            xsize 480 ysize 90
            text_size 42
            text_color "#ffffff"
            text_align 0.5
            background "#012a4a"
            hover_background "#0466c8"
            action Jump("gcms_compare_interface")

screen gcms_compare_screen():
    $ ref_charts  = {"cocaine": "cocaine_gcms_charts", "mdma": "mdma_gcms_charts", "meth": "meth_gcms_charts"}
    $ ref_keys    = ["cocaine", "mdma", "meth"]
    $ evidence_chart  = "evidence_%s_gcms_charts" % gcms_current_drug
    $ reference_chart = ref_charts[ref_keys[gcms_ref_index]]

    add "gcms_interface"
    add evidence_chart  at Transform(xalign=0.5, ypos=0.25, zoom=0.83)
    add reference_chart at Transform(xalign=0.5, ypos=0.45, zoom=0.83)

    imagebutton:
        auto "afis_button_%s" at Transform(xpos=0.30, ypos=0.85)
        action Jump("gcms_compare_prev")
    text "Prev" xpos 0.34 ypos 0.88 size 50

    imagebutton:
        auto "afis_button_%s" at Transform(xpos=0.45, ypos=0.85)
        action Jump("gcms_compare_next")
    text "Next" xpos 0.49 ypos 0.88 size 50

    imagebutton:
        auto "afis_button_%s" at Transform(xpos=0.60, ypos=0.85)
        action Jump("gcms_identify")
    text "Identify" xpos 0.62 ypos 0.88 size 50

screen gcms_open_autosampler():
    add "gcms_background" at Transform(xalign=0.5, yalign=0.5)
    textbutton "Go to GC Autosampler":
            xalign 0.5 ypos 0.85
            xsize 480 ysize 90
            text_size 42
            text_color "#ffffff"
            text_align 0.5
            background "#012a4a"
            hover_background "#0466c8"
            action Jump("gcms_load_autosampler")
