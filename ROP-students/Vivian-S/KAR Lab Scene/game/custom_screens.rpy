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

screen new_afis_screen:
    imagebutton:
        xalign 0.3 yalign 0.16
        idle "import_idle"
        hover "import_hover"
        action Show("import_image")
    imagebutton:
        xalign 0.7 yalign 0.16
        idle "search_idle"
        hover "search_hover"
        action Jump("processing_fingerprint")

screen import_image:
    imagebutton:
        xalign 0.23 yalign 0.73
        idle "import_lid_idle"
        hover "import_lid_hover"
        action Show("lid_image")

screen lid_image:
    image "jar_fingerprint":
        xalign 0.25 yalign 0.6

screen tapeglo_afis:
    python:
        renpy.hide("next_image")
    imagebutton:
        xalign 0.3 yalign 0.16
        idle "import_idle"
        hover "import_hover"
        action Show("import_tapeglo")
    imagebutton:
        xalign 0.7 yalign 0.16
        idle "search_idle"
        hover "search_hover"
        action Jump("processing_fingerprint2")

screen import_tapeglo:
    imagebutton:
        xalign 0.23 yalign 0.73
        idle "import_lid_idle"
        hover "import_lid_hover"
        action Show("tapeglo_image")

screen tapeglo_image:
    image "tapeglo_fingerprint":
        xalign 0.25 yalign 0.6

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
                Function(set_cursor, ''),
                Jump("processing_fingerprint")]
    
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

    hbox:
        xpos 0.15 yalign 0.5
        imagebutton:
            idle "wet_lab_idle"
            hover "wet_lab_hover"
            hovered Notify("Wet Lab")
            unhovered Notify('')
            action Jump('wet_lab')
    hbox:
        xpos 0.4 yalign 0.5
        imagebutton:
            idle "fingerprint_development_idle"
            hover "fingerprint_development_hover"
            hovered Notify("Wet Lab")
            unhovered Notify('')
            action NullAction()
    
    hbox:
        xpos 0.62 yalign 0.5
        imagebutton:
            idle "analytical_instruments_idle"
            hover "analytical_instruments_hover"
            hovered Notify("Analytical Instruments")
            unhovered Notify('')
            action Jump('analytical_instruments')

screen wet_lab_screen:
    image "fumehood"
    frame:
        xpos 0.23 ypos 0.70
        hbox:
            spacing 3
            text "Welcome to the wet lab! Let’s first review the evidence we have collected! \n\n >> hit space to continue"
    key "K_SPACE" action Jump("analyze_evidence")

screen analyze_evidence_screen:
    image "fumehood"
    image "black_bg"
    hbox:
        xpos 0.34 ypos 0.2
        spacing 3
        text "{size=+20}{b}Here's what we collected!"
    hbox:
        xpos 0.37 ypos 0.29
        spacing 3
        text "Click on the item you want to analyze!"
    hbox:
        xpos 0.3 ypos 0.7
        spacing 3
        text "{b}Mason Jar Lid"
    hbox:
        xpos 0.6 ypos 0.7
        spacing 3
        text "{b}Duct Tape"
    imagebutton:
        xpos 0.27 ypos 0.4
        idle "lid-idle"
        hover "lid-hover"
        action Jump("mason_jar")
    imagebutton:
        xpos 0.6 ypos 0.4
        idle "duct_tape-idle"
        hover "duct_tape-hover"
        action Jump("duct_tape")

screen mason_jar_screen:
    image "fumehood "
    image "black_bg"
    
    image "lid-idle":
        xpos 0.39 ypos 0.4
    hbox:
        xpos 0.44 ypos 0.7
        spacing 3
        text "{b}Mason Jar Lid"
    hbox:
        xpos 0.27 ypos 0.25
        spacing 3
        text "Hmm... it looks like this jar could have some fingerprints on it."
    hbox:
        xpos 0.2 ypos 0.3
        spacing 3
        text "Which technique is the best fit for analyzing fingerprints on a smooth surface?"
    hbox:
        xpos 0.4 ypos 0.35
        spacing 3
        text ">> hit space to continue"
    key "K_SPACE" action Jump("which_technique")

screen duct_tape_screen:
    image "fumehood "
    image "black_bg"
    image "duct_tape-idle":
        xpos 0.45 ypos 0.44
    hbox:
        xpos 0.46 ypos 0.7
        spacing 3
        text "{b}Duct Tape"
    hbox:
        xpos 0.23 ypos 0.25
        spacing 3
        text "This piece of duct tape might have some fingerprints on the adhesive side."
    hbox:
        xpos 0.22  ypos 0.3
        spacing 3
        text "Which technique is the best fit for analyzing fingerprints on a sticky surface?"
    hbox:
        xpos 0.4 ypos 0.35
        spacing 3
        text ">> hit space to continue"
    key "K_SPACE" action Jump("which_technique2")

screen gloved:
    image "gloved_hands":
        xpos 0.18 ypos 0.5
    frame:
        xpos 0.25 ypos 0.70
        hbox:
            spacing 3
            text "Great job! Now that we have our gloves on we can get started. \n\n >> hit space to continue"
    key "K_SPACE" action Jump("setupCamphor2")

screen gloved1:
    image "gloved_hands":
        xpos 0.18 ypos 0.5
    frame:
        xpos 0.25 ypos 0.70
        hbox:
            spacing 3
            text "Great job! Now that we have our gloves on we can get started. \n\n >> hit space to continue"
    key "K_SPACE" action Jump("setupTapeglo2") 

screen extinguisher_screen:
    imagebutton:
        xalign 0.5
        yalign 0.3
        idle "extinguish_button_idle"
        hover "extinguish_button_hover"
        action Jump("extinguished")

screen camera_screen:
    image "camera_lens"
    imagebutton:
        xalign 0.5
        yalign 0.91
        idle "camera_button_idle"
        hover "camera_button_hover"
        action Jump("take_picture")

screen scalebar_screen:
    imagebutton:
        xalign 0.6
        yalign 0.6
        # ground "scalebar_idle_test"
        idle "scalebar_idle"
        hover "scalebar_hover"
        action Jump("add_scalebar")

screen add_scalebar:
    image "scalebar":
        xalign 0.6 yalign 0.6
    # python:
    #     characterSay(who = "", what = "Nice job! Now, we need to add some tape.")
    imagebutton:
        xalign 0.5
        yalign 0.48
        # ground "scalebar_idle_test"
        idle "lifting_tape_idle"
        hover "lifting_tape_hover"
        action Jump("add_lifting_tape")
    
screen add_lifting_tape:
    image "lifting_tape":
        xalign 0.5
        yalign 0.48
    imagebutton:
        xalign 0.5
        yalign 0.48
        # ground "scalebar_idle_test"
        idle "lifting_tape_idle"
        hover "lifting_tape_hover"
        action Jump("remove_tape")

screen backing_card_screen:
    imagebutton:
        xalign 0.5
        yalign 0.9
        idle "backing_card_idle"
        hover "backing_card_hover"
        action Jump("collect_backing_card")

screen package_screen:
    imagebutton:
        xalign 0.5
        yalign 0.5
        idle "evidence_bags_idle"
        hover "evidence_bags_hover"
        action Jump("packaged")

#-------------

screen remove_tape:
    imagebutton:
        xpos 0.3
        ypos 0.65
        idle "tray3"
        hover "tray3"
        action Jump("tape_removed")

screen spray_water:
    imagebutton:
        xpos 0.3
        ypos 0.65
        idle "tray_no_tape"
        hover "tray_no_tape"
        action Jump("water_sprayed")

screen spray_water2:
    imagebutton:
        xpos 0.6
        ypos 0.5
        idle "distilled_water_idle"
        hover "distilled_water_hover"
        action Jump("water_sprayed2")

screen spray_water3:
    imagebutton:
        xpos 0.6
        ypos 0.5
        idle "distilled_water_idle"
        hover "distilled_water_hover"
        action Jump("water_sprayed3")

screen paper_towel:
    imagebutton:
        xpos 0.3
        ypos 0.2
        idle "paper_towel_idle"
        hover "paper_towel_hover"
        action Jump("air_dry")

# define a screen for overlay
screen dark_overlay_with_mouse():
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())
    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)
    key "K_SPACE" action Jump("photograph_tape")

screen camera_screen2:
    image "camera_lens"
    imagebutton:
        xalign 0.5
        yalign 0.91
        idle "camera_button_idle"
        hover "camera_button_hover"
        action Jump("take_picture2")

screen acetate:
    imagebutton:
        xalign 0.5
        yalign 0.5
        idle "acetate_idle"
        hover "acetate_hover"
        action Jump("collect_acetate")

screen collect_acetate_screen:
    imagebutton:
        xalign 0.5
        yalign 0.5
        idle "tape_on_acetate_idle"
        hover "tape_on_acetate_hover"
        action Jump("pack_tape")

screen package_screen2:
    imagebutton:
        xalign 0.5
        yalign 0.5
        idle "evidence_bags_idle"
        hover "evidence_bags_hover"
        action Jump("packaged2")
# screen dust_lid_screen:
#     #--------- ADDING ENVIRONMENT ITEMS ---------
    
   

# screen dust_lid_screen:
#     imagebutton:
#         xalign 0.48
#         yalign 0.7
#         idle "piece2_idle"
#         hover "piece2_hover"
#         action Jump("extinguished")
#     imagebutton:
#         xalign 0.5
#         yalign 0.5
#         idle "piece1_idle"
#         hover "piece1_hover"
#         action Jump("extinguished")
#     imagebutton:
#         xalign 0.45
#         yalign 0.3
#         idle "piece3_idle"
#         hover "piece3_hover"
#         action Jump("extinguished")
#     imagebutton:
#         xalign 0.6
#         yalign 0.4
#         idle "piece4_idle"
#         hover "piece4_hover"
#         action Jump("extinguished")


# screen dust_lid_screen:
#     # --------- ADDING ENVIRONMENT ITEMS ---------
#     $environment_items = ["piece1", "piece2", "piece3", "piece4"]

#     python:
#         for item in environment_items: # iterate through environment items list
#             idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
#             hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
#             t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
#             environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
#             environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
#             environment_sprites[-1].idle_image = idle_image # sets idle image
#             environment_sprites[-1].hover_image = hover_image # sets hover image

#             # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
#             # NOTE: for each item, make sure to set width/height to width and height of actual image
#             if item == "piece1":
#                 environment_sprites[-1].width = 551
#                 environment_sprites[-1].height = 506
#                 environment_sprites[-1].x = 700
#                 environment_sprites[-1].y = 200
#             elif item == "piece2":
#                 environment_sprites[-1].width = 576
#                 environment_sprites[-1].height = 461
#                 environment_sprites[-1].x = 680
#                 environment_sprites[-1].y = 400
#             elif item == "piece3":
#                 environment_sprites[-1].width = 397
#                 environment_sprites[-1].height = 323
#                 environment_sprites[-1].x = 700
#                 environment_sprites[-1].y = 200
#             elif item == "piece4":
#                 environment_sprites[-1].width = 371
#                 environment_sprites[-1].height = 451
#                 environment_sprites[-1].x = 900
#                 environment_sprites[-1].y = 200
#         renpy.call_screen("scene1")
# screen dust_lid_screen:
#     image "black_bg"
#     frame:
#         xpos 0.25 ypos 0.70
#         hbox:
#             spacing 3
#             text "Hmm, there seems to be a bit of soot on the lid. Maybe we should use something to get rid of it? \n\n >> hit space to continu"
#     key "K_SPACE" action Jump("dust_lid")

# screen camphor_smoke_screen3:
#     key "K_SPACE" action Jump("setupCamphor")

# screen camphor_smoke_screen4:
    
#     key "K_SPACE" action Jump("setupCamphor")

screen black_bg:
    image "black_bg"

screen analytical_instruments_screen:
    image "lab_bench"