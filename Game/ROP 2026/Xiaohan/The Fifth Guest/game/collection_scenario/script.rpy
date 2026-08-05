init python:
    import json

    # Define custom mouse cursors
    config.mouse = {
        'default': [ ('images/cursors/cursor.png', 0, 0) ],
        'camera': [ ('images/cursors/camera.png', 24, 24) ],
        'swab_pack': [ ('images/cursors/swab_pack.png', 24, 24) ],
        'scalebar': [ ('images/cursors/scalebar.png', 24, 24) ],
        'black_granular_powder': [ ('images/cursors/cursor-black-granular-powder.png', 16, 16) ],
        'gray_granular_powder': [ ('images/cursors/cursor-gray-granular-powder.png', 16, 16) ],
        'gray_magnetic_powder': [ ('images/cursors/cursor-gray-magnetic-powder.png', 16, 16) ],
        'roller': [ ('images/cursors/cursor-roller.png', 16, 16) ],
        'fingerprint_tape': [ ('images/cursors/cursor-fingerprint-tape.png', 16, 16) ],
        'macro_lens': [ ('images/cursors/cursor-macro-lens.png', 16, 16) ],
        'pencil_crayon': [ ('images/cursors/cursor-red-crayon.png', 16, 16) ],
        'camera_flashlight': [ ('images/cursors/cursor-camera-flashlight.png', 16, 16) ],
        'tripod': [ ('images/cursors/cursor-tripod.png', 16, 16) ],
        'backing_card': [ ('images/cursors/cursor-backing-card.png', 16, 16) ],
        'tube': [ ('images/cursors/cursor-tube.png', 16, 16) ],
        'gel_lifter': [ ('images/cursors/gel-lifter.png', 16, 16) ],
        'methanol': [ ('images/cursors/cursor-methanol.png', 16, 16) ],
        'phenolphthalein': [ ('images/cursors/cursor-phenolphthalein.png', 16, 16) ],
        'hydrogen_peroxide': [ ('images/cursors/cursor-hydrogen-peroxide.png', 16, 16) ],
        'hungarian_red': [ ('images/cursors/cursor-hungarian-red.png', 16, 16) ],
        'distilled_water': [ ('images/cursors/cursor-distilled-water.png', 16, 16) ],
        'micropipette': [ ('images/cursors/micropipette.png', 10, 10) ],
    }

    tools = load_items("jsons/toolbox.json")
    # Add all toolbox items from the toolbox JSON
    for tool in tools.values():
        toolbox.add_to_inventory(tool)

    evids = load_items("jsons/evidence.json")


define n = Character(name=("Nina"), image="nina")
define d = Character(
    "",
    what_color="#F5F5F5"
)

default player_name = "Player"
default first_study_visit = True
default scalebar_placed = False

image hallway-bg = Transform("images/Scenes/hallway-bg.png", xysize=(config.screen_width, config.screen_height))
image study-bg = "images/Scenes/study-bg.png"
image door_view-bg = ConditionSwitch(
    "evids.get('Gel-Lifted Shoeprint') in evidence._inventory", "images/Scenes/door-view-shoeprint-removed-bg.png",
    "True", "images/Scenes/door-view-bg.png"
)
image lamp-bg = "images/Scenes/lamp-bg.png"
image fingerprint-zoom-bg = "fingerprint_dynamic_bg"
image blood-pool-bg = "images/Scenes/blood-pool-bg.png"

image fingerprint_dynamic_bg = ConditionSwitch(
    "not fingerprint_powder and not fingerprint_circled", "images/Scenes/fingerprint-zoom-bg.png",
    "not fingerprint_powder and fingerprint_circled", "images/Scenes/fingerprint-circled.png",
    "fingerprint_powder == 'black' and not fingerprint_circled", "images/Scenes/fingerprint-black-powered-bg.png",
    "fingerprint_powder == 'black' and fingerprint_circled", "images/Scenes/fingerprint-black-powered-circled-bg.png",
    "fingerprint_powder == 'white' and not fingerprint_circled", "images/Scenes/fingerprint-white-powered-bg.png",
    "fingerprint_powder == 'white' and fingerprint_circled", "images/Scenes/fingerprint-white-powered-circled-bg.png",
    "fingerprint_powder == 'hungarian_red' and not fingerprint_circled", "images/Scenes/fingerprint-zoom-bg.png",
    "fingerprint_powder == 'hungarian_red' and fingerprint_circled", "images/Scenes/fingerprint-circled.png",
    "True", "images/Scenes/fingerprint-zoom-bg.png",
)

screen study_observe_label():
    $ splatter_photo = evids.get("Photo of Blood Splatter")
    $ splatter_collected = splatter_photo in evidence._inventory if splatter_photo else False

    $ lamp_photo = evids.get("Photo of Lamp (Far)")
    $ lamp_far_collected = lamp_photo in evidence._inventory if lamp_photo else False

    $ floor_swab = evids.get("Swab with Blood (Floor)")
    $ floor_tube = evids.get("Tube with Swab (Floor)")
    $ floor_blood_collected = (floor_swab in evidence._inventory if floor_swab else False) or (floor_tube in evidence._inventory if floor_tube else False)

    imagemap:
        ground "images/Scenes/study-bg.png"
        # TEMPORARILY DISABLED: right-side route to the door/shoeprint scene.
        # hotspot (1522, 121, 396, 935) action [Hide("study_observe_label"), Jump("study_door")] tooltip "Move this way?"

        if not splatter_collected:
            hotspot (577, 575, 274, 237) action Function(click_blood_splatter_direct) tooltip "inspect"
        else:
            hotspot (577, 575, 274, 237) action NullAction() tooltip "Blood Splatter (Photographed)"

        if active_tool == "camera":
            hotspot (884, 322, 200, 266) action Function(click_lamp_far_direct) tooltip "Photograph lamp (overall)"
        else:
            hotspot (884, 322, 200, 266) action [Hide("study_observe_label"), Jump("study_lamp")] tooltip "inspect"

        if not floor_blood_collected:
            # Floor blood on the overview is the same sample as the blood pool.
            hotspot (631, 589, 222, 223) action [Hide("study_observe_label"), Jump("study_blood_pool")] tooltip "inspect"
        else:
            hotspot (631, 589, 222, 223) action NullAction() tooltip "Blood Sample (Floor pool collected)"

        hotspot (363, 816, 336, 261) action [Hide("study_observe_label"), Jump("study_blood_pool")] tooltip "inspect"
        hotspot (604, 602, 243, 220) action [Hide("study_observe_label"), Jump("study_blood_pool")] tooltip "inspect"

        $ tooltip = GetTooltip()
        if tooltip:
            frame:
                background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
                padding gui.notify_frame_borders.padding
                xalign 0.5
                ypos 50
                text "[tooltip]" style "notify_text"


screen game_mode_selection():
    tag menu
    modal True

    # Keep the mode selection visually connected to the title screen.
    add gui.main_menu_background
    add Solid("#081018b8")

    vbox:
        xalign 0.5
        ypos 105
        spacing 16

        text "What would you like to play?":
            xalign 0.5
            size 58
            color "#ffffff"
            bold True
            outlines [(3, "#000000aa", 0, 2)]

        text "Choose where you want to begin the investigation.":
            xalign 0.5
            size 27
            color "#d8e3ea"
            outlines [(2, "#000000aa", 0, 1)]

    hbox:
        xalign 0.5
        yalign 0.62
        spacing 75

        button:
            xysize (650, 390)
            padding (45, 40)
            background Solid("#172c3ed9")
            hover_background Solid("#245273ee")
            action Return("evidence")

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 30

                text "EVIDENCE COLLECTION":
                    xalign 0.5
                    text_align 0.5
                    size 42
                    color "#ffffff"
                    bold True

                text "Begin at the crime scene.\nDocument, collect, and package the evidence before continuing to the lab.":
                    xalign 0.5
                    text_align 0.5
                    size 25
                    color "#dceaf2"
                    line_spacing 8

                text "START AT THE CRIME SCENE":
                    xalign 0.5
                    size 23
                    color "#8fd3ff"
                    bold True

        button:
            xysize (650, 390)
            padding (45, 40)
            background Solid("#30243ed9")
            hover_background Solid("#60447bee")
            action Return("lab")

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 30

                text "LAB SCENE":
                    xalign 0.5
                    text_align 0.5
                    size 42
                    color "#ffffff"
                    bold True

                text "Skip evidence collection.\nStart with two blood swabs and a fingerprint photograph already loaded into AFIS.":
                    xalign 0.5
                    text_align 0.5
                    size 25
                    color "#eee4f5"
                    line_spacing 8

                text "GO DIRECTLY TO THE LAB":
                    xalign 0.5
                    size 23
                    color "#d2a8ff"
                    bold True


screen scene_back_arrow(current_screen, destination):
    zorder 90

    imagebutton:
        idle "ui/left_arrow.png"
        hover "ui/left_arrow_hover.png"
        xalign 0.96
        yalign 0.94
        action [Hide(current_screen), Jump(destination)]
        tooltip "Go back"


label start:
    call screen game_mode_selection

    if _return == "lab":
        jump standalone_lab_start
    else:
        jump evidence_collection_start


label evidence_collection_start:
    $ initialize_collection_route()

    scene hallway-bg
    with fade

    d "Address: 41 Columbia Street, Delhi, ON N4B 4M6"

    $ player_name = renpy.input("Enter your name")
    $ player_name = player_name.strip()
    if not player_name:
        $ player_name = "Player"

    show nina normal1
    n "Hi [player_name], I'm Nina, your supervisor for today."
    n "Let's begin by collecting and documenting the evidence in the study."

    jump study_bg


label standalone_lab_start:
    $ initialize_standalone_lab_route()
    jump lab_transition_loading

label study_bg:
    scene study-bg
    with fade

    if first_study_visit:
        $ first_study_visit = False
        "You step into the study. The body has been removed, leaving only a chalk outline and evidence markers on the floor."

    show screen study_observe_label
    show screen open_inv
    show screen leave_lab_button_screen

    window hide
    $ renpy.pause(9999, hard=True)


# TEMPORARILY DISABLED: right-side door and shoeprint scene.
# label study_door:
#     scene door_view-bg
#     with fade
#     "You move closer to the door."
#
#     show screen door_observe_label
#     show screen open_inv
#     show screen leave_lab_button_screen
#     window hide
#     $ renpy.pause(9999, hard=True)
#
#
# screen door_observe_label():
#     # Hotkey to leave the location
#     key "l" action [Hide("door_observe_label"), Jump("study_bg")]
#     key "L" action [Hide("door_observe_label"), Jump("study_bg")]
#
#     $ photo_normal = evids.get("Photo of Shoeprint")
#     $ photo_scale = evids.get("Photo of Shoeprint with Scalebar")
#     $ gel_lift = evids.get("Gel-Lifted Shoeprint")
#     $ lifted = gel_lift in evidence._inventory if gel_lift else False
#     $ photographed = (photo_normal in evidence._inventory if photo_normal else False) and (photo_scale in evidence._inventory if photo_scale else False)
#
#     textbutton "Leave Location":
#         xpos 20
#         ypos 20
#         text_size 24
#         background "#c0392b"
#         hover_background "#e74c3c"
#         padding (15, 8)
#         action [Hide("door_observe_label"), Jump("study_bg")]
#         tooltip "Leave Location (Hotkey: L)"
#
#     imagemap:
#         if lifted:
#             ground "images/Scenes/door-view-shoeprint-removed-bg.png"
#         else:
#             ground "images/Scenes/door-view-bg.png"
#
#         if lifted:
#             hotspot (800, 800, 320, 200) action NullAction() tooltip "Shoeprint (Lifted)"
#         elif photographed:
#             # Hotspot showing it is already photographed
#             hotspot (800, 800, 320, 200) action NullAction() tooltip "Shoeprint (Photographed)"
#         else:
#             if scalebar_placed:
#                 # Hotspot on the floor where the shoeprint is located (placeholder)
#                 hotspot (800, 800, 320, 200) action Function(click_shoeprint_direct_or_scalebar) tooltip "Inspect shoeprint (Scalebar placed)"
#             else:
#                 # Hotspot on the floor where the shoeprint is located (placeholder)
#                 hotspot (800, 800, 320, 200) action Function(click_shoeprint_direct_or_scalebar) tooltip "Inspect the floor"
#
#         $ tooltip = GetTooltip()
#         if tooltip:
#             frame:
#                 background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
#                 padding gui.notify_frame_borders.padding
#                 xalign 0.5
#                 ypos 50
#                 text "[tooltip]" style "notify_text"
#
#     if scalebar_placed:
#         add "toolbox-scalebar" xpos 760 ypos 860 zoom 0.5
#
#     use scene_back_arrow("door_observe_label", "study_bg")
#
#

label study_lamp:
    scene lamp-bg
    with fade
    "You move closer to the lamp."

    show screen lamp_observe_label
    show screen open_inv
    show screen leave_lab_button_screen
    window hide
    $ renpy.pause(9999, hard=True)


screen lamp_observe_label():
    # Hotkey to leave the location
    key "l" action [Hide("lamp_observe_label"), Jump("study_bg")]
    key "L" action [Hide("lamp_observe_label"), Jump("study_bg")]

    $ lamp_blood_swab = evids.get("Swab with Blood (Lamp)")
    $ lamp_blood_tube = evids.get("Tube with Swab (Lamp)")
    $ lamp_blood_collected = (lamp_blood_swab in evidence._inventory if lamp_blood_swab else False) or (lamp_blood_tube in evidence._inventory if lamp_blood_tube else False)

    $ lamp_photo_item = evids.get("Photo of Lamp")
    $ lamp_photo_collected = lamp_photo_item in evidence._inventory if lamp_photo_item else False

    textbutton "Leave Location":
        xpos 20
        ypos 20
        text_size 24
        background "#c0392b"
        hover_background "#e74c3c"
        padding (15, 8)
        action [Hide("lamp_observe_label"), Jump("study_bg")]
        tooltip "Go Back (Hotkey: L)"

    imagemap:
        ground "images/Scenes/lamp-bg.png"

        # Hotspot for the bloody fingerprint
        hotspot (980, 741, 231, 242) action [Hide("lamp_observe_label"), Jump("study_fingerprint_zoom")] tooltip "inspect"

        # Hotspot for taking photo of the lamp
        if not lamp_photo_collected:
            if active_tool == "camera":
                hotspot (841, 139, 534, 432) action Function(click_lamp_direct) tooltip "inspect"
            else:
                hotspot (841, 139, 534, 432) action NullAction() tooltip "inspect"
        else:
            hotspot (841, 139, 534, 432) action NullAction() tooltip "Photo of Lamp collected"

        # Hotspot for blood sample on the lamp-bg page
        if not lamp_blood_collected:
            if active_tool in ("swab_pack", "methanol", "phenolphthalein", "hydrogen_peroxide") or active_tool is None:
                hotspot (884, 75, 425, 387) action Function(click_lamp_blood_direct) tooltip "inspect"
            else:
                hotspot (884, 75, 425, 387) action NullAction() tooltip "inspect"
        else:
            hotspot (884, 75, 425, 387) action NullAction() tooltip "Blood Sample (Lamp collected)"

        $ tooltip = GetTooltip()
        if tooltip:
            frame:
                background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
                padding gui.notify_frame_borders.padding
                xalign 0.5
                ypos 50
                text "[tooltip]" style "notify_text"

    use scene_back_arrow("lamp_observe_label", "study_bg")


label study_fingerprint_zoom:
    scene fingerprint-zoom-bg
    with fade
    "You zoom in on the bloody fingerprint on the lamp."

    show screen fingerprint_zoom_label
    show screen open_inv
    show screen leave_lab_button_screen
    window hide
    $ renpy.pause(9999, hard=True)

label study_blood_pool:
    scene blood-pool-bg
    with fade
    "You move closer to the blood."

    show screen blood_pool_observe_label
    show screen open_inv
    show screen leave_lab_button_screen
    window hide
    $ renpy.pause(9999, hard=True)

screen blood_pool_observe_label():
    key "l" action [Hide("blood_pool_observe_label"), Jump("study_bg")]
    key "L" action [Hide("blood_pool_observe_label"), Jump("study_bg")]

    $ pool_blood_swab = evids.get("Swab with Blood (Floor)")
    $ pool_blood_tube = evids.get("Tube with Swab (Floor)")
    $ pool_blood_collected = (pool_blood_swab in evidence._inventory if pool_blood_swab else False) or (pool_blood_tube in evidence._inventory if pool_blood_tube else False)

    $ pool_photo = evids.get("Photo of Blood Pool")
    $ pool_photo_collected = pool_photo in evidence._inventory if pool_photo else False

    textbutton "Leave Location":
        xpos 20
        ypos 20
        text_size 24
        background "#c0392b"
        hover_background "#e74c3c"
        padding (15, 8)
        action [Hide("blood_pool_observe_label"), Jump("study_bg")]
        tooltip "Go Back (Hotkey: L)"

    imagemap:
        ground "images/Scenes/blood-pool-bg.png"

        # Blood collection hotspots
        if not pool_blood_collected:
            if active_tool == "camera" and not pool_photo_collected:
                hotspot (431, 550, 901, 523) action Function(click_pool_photo_direct) tooltip "inspect"
                hotspot (973, 204, 521, 413) action Function(click_pool_photo_direct) tooltip "inspect"
            elif active_tool in ("swab_pack", "methanol", "phenolphthalein", "hydrogen_peroxide") or active_tool is None:
                hotspot (431, 550, 901, 523) action Function(click_pool_blood_direct) tooltip "inspect"
                hotspot (973, 204, 521, 413) action Function(click_pool_blood_direct) tooltip "inspect"
            else:
                hotspot (431, 550, 901, 523) action NullAction() tooltip "inspect"
                hotspot (973, 204, 521, 413) action NullAction() tooltip "inspect"
        else:
            if active_tool == "camera" and not pool_photo_collected:
                hotspot (431, 550, 901, 523) action Function(click_pool_photo_direct) tooltip "inspect"
                hotspot (973, 204, 521, 413) action Function(click_pool_photo_direct) tooltip "inspect"
            elif pool_photo_collected:
                hotspot (431, 550, 901, 523) action NullAction() tooltip "Blood Pool (Photographed)"
                hotspot (973, 204, 521, 413) action NullAction() tooltip "Blood Pool (Photographed)"
            else:
                hotspot (431, 550, 901, 523) action NullAction() tooltip "Blood Sample (Pool collected)"
                hotspot (973, 204, 521, 413) action NullAction() tooltip "Blood Sample (Pool collected)"

        $ tooltip = GetTooltip()
        if tooltip:
            frame:
                background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
                padding gui.notify_frame_borders.padding
                xalign 0.5
                ypos 50
                text "[tooltip]" style "notify_text"

    use scene_back_arrow("blood_pool_observe_label", "study_bg")

screen fingerprint_zoom_label():
    # Transparent button for fingerprint hotspot (1253, 415, 190, 222)
    imagebutton:
        xpos 1253
        ypos 415
        xysize (190, 222)
        idle Solid("#0000")
        hover Solid("#fff1") # subtle hover highlight
        action Function(click_fingerprint_hotspot)
        tooltip "Fingerprint"

    # Camera attachment checklist before photographing
    frame:
        xpos 40
        ypos 40
        background "#17354add"
        padding (16, 12)
        vbox:
            spacing 4
            text "Camera setup" size 18 color "#7ec8e3" bold True
            if fingerprint_camera_equip_lens:
                text "Macro Lens: Ready" size 16 color "#2ecc71"
            else:
                text "Macro Lens: Needed" size 16 color "#e74c3c"
            if fingerprint_camera_equip_flashlight:
                text "Flashlight: Ready" size 16 color "#2ecc71"
            else:
                text "Flashlight: Needed" size 16 color "#e74c3c"
            if fingerprint_camera_equip_tripod:
                text "Tripod: Ready" size 16 color "#2ecc71"
            else:
                text "Tripod: Needed" size 16 color "#e74c3c"
    # Hotkey to leave the location
    key "l" action [Hide("fingerprint_zoom_label"), Jump("study_lamp")]
    key "L" action [Hide("fingerprint_zoom_label"), Jump("study_lamp")]

    # Render placed scalebar
    if fingerprint_scalebar_placed:
        add "images/Toolbox Items/toolbox-scalebar.png" xpos 1210 ypos 480 zoom 0.45
        text "[fingerprint_scalebar_label]" xpos 1224 ypos 456 size 16 color "#fff"

    $ tooltip = GetTooltip()
    if tooltip:
        frame:
            background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
            padding gui.notify_frame_borders.padding
            xalign 0.5
            ypos 50
            text "[tooltip]" style "notify_text"

    use scene_back_arrow("fingerprint_zoom_label", "study_lamp")


screen camera_setup_screen():
    # DEPRECATED: Replaced by the overlay camera module (camera_preview_ui).
    # Kept only as a harmless stub so old saves/scripts do not crash.
    modal True
    add Solid("#000b")

    frame:
        align (0.5, 0.5)
        background Frame("gui/frame.png", 10, 10)
        padding (30, 30)

        vbox:
            spacing 20
            align (0.5, 0.5)
            text "Camera Setup (legacy)" size 26 xalign 0.5
            text "Opening the forensic camera viewfinder…" size 18 xalign 0.5
            textbutton "Continue" action [Hide("camera_setup_screen"), Function(open_crime_scene_camera, "fingerprint")] xalign 0.5
            textbutton "Cancel" action Hide("camera_setup_screen") xalign 0.5


screen backing_card_form_screen():
    modal True
    add Solid("#000d")
    
    frame:
        align (0.5, 0.5)
        background Frame("gui/frame.png", 10, 10)
        padding (30, 30)
        xsize 600
        
        vbox:
            spacing 20
            
            text "Select the correct backing card information:" size 22 xalign 0.5 color "#fff"
            
            vbox:
                spacing 10
                xfill True
                
                textbutton "Case 2026-10A, Date: Today, Location: Study Lamp" action [Function(submit_backing_card, True)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
                    
                textbutton "Case 2026-10A, Date: Today, Location: Front Door" action [Function(submit_backing_card, False)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
                    
                textbutton "Case 9999-99X, Date: Today, Location: Study Lamp" action [Function(submit_backing_card, False)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
                    
            textbutton "Cancel" action Hide("backing_card_form_screen") xalign 0.5 yoffset 10


screen scalebar_label_screen():
    modal True
    add Solid("#000d")
    
    frame:
        align (0.5, 0.5)
        background Frame("gui/frame.png", 10, 10)
        padding (30, 30)
        xsize 500
        
        vbox:
            spacing 20
            
            text "Select the correct scalebar label for a fingerprint:" size 22 xalign 0.5 color "#fff"
            
            vbox:
                spacing 10
                xfill True
                
                textbutton "Scale 1cm" action [SetVariable("fingerprint_scalebar_label", "Scale 1cm"), Function(submit_scalebar_label, True)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
                
                textbutton "Scale 10cm" action [SetVariable("fingerprint_scalebar_label", "Scale 10cm"), Function(submit_scalebar_label, False)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
                
                textbutton "Fingerprint Size" action [SetVariable("fingerprint_scalebar_label", "Fingerprint Size"), Function(submit_scalebar_label, False)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
                
                textbutton "No Label" action [SetVariable("fingerprint_scalebar_label", "No Label"), Function(submit_scalebar_label, False)]:
                    xfill True
                    padding (12, 10)
                    background "#2c3e50"
                    hover_background "#34495e"
            
            textbutton "Cancel" action Hide("scalebar_label_screen") xalign 0.5


screen leave_lab_button_screen():
    # Above study imagemaps / open_inv so it stays visible after Nina's "No".
    zorder 250
    if store.show_leave_button:
        textbutton "Move to Lab" action Jump("lab_scene"):
            xalign 0.95
            yalign 0.05
            text_size 24
            background "#c0392b"
            hover_background "#e74c3c"
            padding (15, 8)


label nina_lab_transition_dialogue:
    hide screen deferred_lab_transition
    hide screen evidence_collected_notice
    hide screen fingerprint_zoom_label
    hide screen lamp_observe_label
    hide screen door_observe_label
    hide screen blood_pool_observe_label
    hide screen study_observe_label
    hide screen inventory
    hide screen open_inv
    hide screen camera_preview_ui
    hide screen photo_score_display
    hide screen photo_album
    hide screen photo_viewer
    hide screen camera_setup_screen
    hide screen blood_test_screen
    hide screen camera_hint_overlay

    if fingerprint_collected and fingerprint_method == "powder":
        $ evidence_wrong_moves += 1
        $ evidence_score = max(0, evidence_score - 10)

    $ collection_grade = collection_letter_grade()
    $ _mistakes = evidence_wrong_moves

    show nina normal1
    n "Great work, [player_name]! You've collected [len(evidence._inventory)] evidence items."

    if _mistakes == 0:
        n "I didn't catch any procedural mistakes during collection. Your overall rating is [collection_grade]."
    elif _mistakes == 1:
        n "I noted 1 procedural mistake during collection. Your overall rating is [collection_grade]."
    else:
        n "I noted [_mistakes] procedural mistakes during collection. Your overall rating is [collection_grade]."

    if fingerprint_collected and fingerprint_method == "powder":
        n "One thing to flag: you used granular powder to develop the print on the lamp. That's a metal surface, so Hungarian Red dye followed by distilled water would have been the better method — I've logged that as one of the mistakes."

    n "Would you like to head to the lab to process them now?"

    menu:
        "Yes, let's go to the lab.":
            jump lab_scene
        "No, I want to keep looking around.":
            n "Alright, let me know when you're ready. You can click the 'Move to Lab' button at the top right of the screen at any time."
            $ store.show_leave_button = True
            show screen leave_lab_button_screen
            jump study_bg


label lab_scene:
    hide screen leave_lab_button_screen
    hide screen fingerprint_zoom_label
    hide screen lamp_observe_label
    hide screen door_observe_label
    hide screen blood_pool_observe_label
    hide screen study_observe_label
    hide screen inventory
    hide screen open_inv
    hide screen camera_preview_ui
    hide screen photo_score_display
    hide screen photo_album
    hide screen photo_viewer
    hide screen camera_setup_screen
    hide screen blood_test_screen
    hide screen camera_hint_overlay

    if game_route == "collection":
        $ transfer_issues = collection_lab_transfer_issues()

        if transfer_issues["has_issues"]:
            scene hallway-bg
            show nina talk at right

            n "Before we leave, let's check that the physical evidence is ready for transport."

            if transfer_issues["missing"]:
                n "We still have not collected: [transfer_issues['missing_text']]."

            if transfer_issues["unbagged"]:
                n "These items are still loose and need to be packaged: [transfer_issues['unbagged_text']]."

            if transfer_issues["unsealed"]:
                n "These evidence bags were not sealed: [transfer_issues['unsealed_text']]."

            n "Photographs can transfer electronically, but loose or unsealed physical evidence cannot go to the lab."

            menu:
                "Go back to the crime scene":
                    n "Good choice. Finish collecting and packaging the evidence, then use the Move to Lab button when you're ready."
                    hide nina
                    $ store.show_leave_button = True
                    show screen leave_lab_button_screen
                    jump study_bg
                "Continue to the lab anyway":
                    n "Alright, but any missing, loose, or unsealed evidence will not be available for analysis."
                    hide nina

    $ prepare_collected_evidence_for_lab()

    scene hallway-bg
    show nina normal1

    n "Let's take the evidence you collected to the laboratory, [player_name]."
    jump lab_transition_loading

label nina_swab_warning:
    show nina normal1
    n "Wait, [player_name], don't do that!"
    n "Packing a wet swab directly in the bag will contaminate the evidence. You must place it in a tube first!"
    return

label nina_backing_card_wrong:
    show nina normal1
    n "Wait, make sure the case number and location are correct on the backing card. If the chain of custody is broken, it won't hold up in court!"
    return

label nina_fingerprint_swab_warning:
    show nina normal1
    n "Wait, [player_name], don't do that!"
    n "Using a swab on the fingerprint will destroy the ridge details and contaminate the print. We want to collect the fingerprint itself, not destroy it!"
    return

label nina_magnetic_powder_warning:
    show nina normal1
    n "Wait, [player_name]! That's magnetic powder."
    n "This is a metal lamp.You should only use magnetic powder on non-metallic surfaces. Using it on the fingerprint will ruin the evidence!"
    return

label nina_fingerprint_camera_setup_warning(missing_part="Macro Lens"):
    show nina talk at right
    n "Hold on, [player_name]. Before you photograph this fingerprint, set up the camera properly."
    n "You still need to attach the [missing_part] from your toolbox."
    n "Attach the Macro Lens, Camera Flashlight, and Tripod first — then equip the Camera and try again."
    hide nina
    return

label nina_blood_test_order_warning:
    # Kept for old saves; incorrect order is now accepted silently.
    return

label nina_blood_test_required_warning:
    show nina talk at right
    n "Not yet, [player_name]. Run a presumptive blood test on this stain first."
    n "There are three test solutions in your toolbox — apply them to the stain, then collect a clean swab once you see a reaction."
    hide nina
    return