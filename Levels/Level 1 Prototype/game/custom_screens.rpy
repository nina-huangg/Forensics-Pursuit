
screen scene_office():
    
    image "office_bg"
   
    if uv_light:
        imagemap:
            idle "office_bg_dim"
            hover "office_bg_dim_hover"

            hotspot(370,855,286,196) action [Jump("show_office_footprints")] 
            hotspot(851,744,160,109) action [Jump("show_office_screwdriver")] 
            hotspot(812,402,304,166) action[ Jump("show_office_exam")] 
            hotspot(1121,118,448,309) action Jump('show_office_computer')
            hotspot(556,0,224,651) action NullAction()

            #hotspot(773, 97, 607, 480) action [Jump("show_office_window")] 
            #hotspot(309,122,347,209) action [Hide("scene_window"), Jump("show_office_books_cabinet")] 
            #hotspot(1401,188,220,239) action [Hide("scene_window"),Jump("show_office_books_bookshelves")] 
            
    elif tools['marker']:
            imagemap:
                idle "office_bg"
                hover "office_bg_hover"

                hotspot(370,855,286,196) action [SetDict(evidence_marker_set,'footprints', True)] sensitive tools['marker']
                hotspot(851,744,160,109) action [SetDict(evidence_marker_set,'screwdriver', True)] sensitive tools['marker']
                hotspot(812,402,304,166) action [SetDict(evidence_marker_set,'exam', True)] sensitive tools['marker']
                hotspot(1121,118,448,309) action [SetDict(evidence_marker_set,'computer', True)] sensitive tools['marker']
                hotspot(556,0,224,651) action [SetDict(evidence_marker_set,'window', True)] sensitive tools['marker']
                # hotspot(773, 97, 607, 480) action [SetDict(evidence_marker_set,'window', True)] sensitive tools['marker']
                # hotspot(309,122,347,209) action NullAction()
                # hotspot(1401,188,220,239) action NullAction()
    
    else:
        imagemap:
            idle "office_bg"
            hover "office_bg_hover"

            hotspot(370,855,286,196) action [Jump("show_office_footprints")] 
            hotspot(851,744,160,109) action [Jump("show_office_screwdriver")]
            hotspot(812,402,304,166) action[ Jump("show_office_exam")] 
            hotspot(1121,118,448,309) action Jump('show_office_computer')
            hotspot(556,0,224,651) action NullAction()

            # hotspot(773, 97, 607, 480) action [Jump("show_office_window")] 
            # hotspot(309,122,347,209) action NullAction()
            # hotspot(1401,188,220,239) action NullAction()

    if evidence_marker_set['footprints']:
        hbox:
            pos(438, 859)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['screwdriver']:
        hbox:
            pos(847, 720)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['exam']:
        hbox:
            pos(890, 410)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['computer']:
        hbox:
            pos(1265, 330)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['window']:
        hbox:
            pos(620, 635)
            image "marker" at Transform(zoom=0.2)

screen keyboard_screen():

    key "K_RIGHT" action [Function(keyboard_switch, 'right')]
    key "K_LEFT" action [Function(keyboard_switch, 'left')]

    image scenes[keyboard_scene_counter]

screen scene_footprints():
    default process = False
    default peel = False
    default stick = False

    if uv_light and 'footprints' not in processed:
        imagemap:
            idle "office_footprints_dim"
            hover "office_footprints_dim_hover"

            hotspot(577,144,654,753) action NullAction()
    elif 'footprints' not in processed:
        imagemap:
            idle "office_footprints"
            hover "office_footprints_lift_hover" 

            hotspot(577,144,654,753) action [SetLocalVariable('process', True)] sensitive tools['gel_lift']
        showif process:
            imagemap:
                idle "lift1"
                hover "lift1_hover" 

                hotspot(412,0,941,1043) action [SetLocalVariable('peel', True), Function(set_cursor, 'gel_lifted')] sensitive tools['gel_lift']
        showif peel:
            imagemap:
                idle "lift6"
                hover "lift6_hover" 

                hotspot(412,0,941,1043) action [SetLocalVariable('stick', True), Function(set_cursor, ''),Show('screen_finished_processing',evidence='footprints', _layer='over_screens')] sensitive tools['gel_lift']
        showif stick:
            image "lift7"
    else:
        image 'lift7'
        hbox:
            xpos 0.65 ypos 0.90
            textbutton('Processing Finished'):
                style 'custom_button'
                action NullAction() sensitive False

screen screen_finished_processing(evidence):
    hbox:
        xpos 0.65 ypos 0.90
        textbutton('Add to case files'):
            style "custom_button"
            action [Function(set_scene_enable, False), Function(photo_append, evidence),SetVariable('on_main_screen', True),Hide('screen_finished_processing', _layer='over_screens'), Function(finished_process, evidence), Show('scene_office')]



screen scene_screwdriver():
    default dusted = False
    default taped = False
    default bagged = False

    if uv_light and 'screwdriver' not in processed:
        imagemap:
            idle "screwdriver_dim"
            hover "screwdriver_dim_hover"

            hotspot(395,61,974,1007) action NullAction()
    elif 'screwdriver' not in processed:
        imagemap:
            idle "screwdriver"
            hover "screwdriver_fingerprint"

            hotspot(960,300,175,120) action SetLocalVariable('dusted', True) sensitive tools['powder']
    
        showif dusted:
            imagemap:
                idle 'screwdriver_dusted'
                hover 'screwdriver_dusted'

                hotspot(1147,227,1190,214) action SetLocalVariable('taped', True) sensitive tools['scalebar']
        showif taped:
            imagemap:
                idle 'screwdriver_taped'
                hover 'screwdriver_taped'

                hotspot(646,188,809,443) action [SetLocalVariable('bagged', True),Function(set_cursor, ''),Show('screen_finished_processing', evidence='screwdriver',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'screwdriver_packed'
    else:
        image 'screwdriver_empty_bg'

screen scene_exam():
    default packed = False
    if uv_light and 'exam' not in processed:
        imagemap:
            idle "exam_dim"
            hover "exam_dim_hover"

            hotspot(395,61,974,1007) action NullAction()
    elif 'exam' not in processed:
        imagemap:
            idle "exam"
            hover "exam"

            hotspot(395,61,974,1007) action [SetLocalVariable('packed', True),Function(set_cursor, ''),Show('screen_finished_processing', evidence='exam',_layer='over_screens')] sensitive tools['bag']
        showif packed:
            image 'exam_packed'
    else:
        image 'exam_empty'

screen scene_computer():
    default dusted = False
    default scalebar = False
    default taped = False
    default lift = False
    default done = False
    default bagged = False

    if uv_light and 'computer' not in processed:
        imagemap:
            idle "computer_zoomout_dim"
            hover "computer_zoomout_dim_hover"

            hotspot(760,120,867,634) action NullAction()
    elif 'computer' not in processed:
        imagemap:
            idle "computer_zoomout"
            hover "computer_zoomout_fingerprint"

            hotspot(760,120,855,634) action SetLocalVariable('dusted', True) sensitive tools['powder']
        showif dusted:
            imagemap:
                idle "computer_dusted"
                hover "computer_dusted"

                hotspot(258,93,650,970) action SetLocalVariable('scalebar', True) sensitive tools['scalebar']
        showif scalebar:
            imagemap:
                idle "computer_tape"
                hover "computer_tape"

                hotspot(244,93,1400,900) action [SetLocalVariable('lift', True), Function(set_cursor, 'computer_lifted')] sensitive tools['lifting_tape']
        showif lift:
            imagemap:
                idle "computer_backing_dim"
                hover "computer_backing"

                hotspot(180,439,1000,500) action [SetLocalVariable('done', True), Function(set_cursor, '')]
        showif done:
            imagemap:
                idle "computer_complete"
                hover "computer_complete_hover"

                hotspot(550,285,812,550) action [SetLocalVariable('bagged', True), Function(set_cursor, ''), Show('screen_finished_processing', evidence='computer',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'computer_evidence_bag'
    
    else:
        image 'computer_zoomout'

screen scene_window():
    default button_text = 'View outside'
    default window_image = 'office_window'
    image window_image
    hbox:
        xalign 0.5 ypos 50
        textbutton button_text:
                style "custom_button"
                if button_text == 'View outside':
                    action [SetLocalVariable('button_text', 'View inside'), SetLocalVariable('window_image', 'office_window_outside')]
                else:
                    action [SetLocalVariable('button_text', 'View outside'), SetLocalVariable('window_image', 'office_window')]



screen scene_books_cabinet():
    default open_book = False
    image "office_books_cabinet"

screen scene_books_bookshelves():
    if uv_light:
        imagemap:
            idle "office_books_bookshelves_dim"
            hover "office_books_bookshelves"

            hotspot(514,119,1021,567) action NullAction()
            hotspot(519,719,1021,360) action NullAction()
    else:
        image "office_books_bookshelves"

screen scene_cabinet():
    image "office_cabinet_open"

screen screen_examine_ignore(item):
    default examine = False
    default ignore = False

    hbox:
        xpos 0.65 ypos 0.04
        textbutton('Examine'):
            style "custom_button"
            action [ToggleLocalVariable('examine'),  SetLocalVariable('ignore', False)]
    hbox:
        xpos 0.75 ypos 0.04
        textbutton('Ignore'):
            style "custom_button"
            action [ToggleLocalVariable("ignore"), SetLocalVariable('examine', False)]

    if should_be_examined[item]:
        showif examine:
            frame:
                xalign 0.5 yalign 0.3
                text "Great!"
            frame:
                xalign 0.5 yalign 0.4
                text "Place an evidence marker on this item when you return to the main screen."
        showif ignore:
            frame:
                xalign 0.5 yalign 0.3
                text "Are you sure you want to ignore this item?"

    else:
        showif examine:
            frame:
                xalign 0.5 yalign 0.3
                text "Mmmh... Think again about why you want to examine this item."

        showif ignore:
            frame:
                xalign 0.5 yalign 0.3
                text "Yup! This is the right call here."
            frame:
                xalign 0.5 yalign 0.4
                text "This is because..."

# back button
screen back_button_screen(location, curr_screen):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Hide('screen_examine_ignore', _layer='over_screens'), Function(set_cursor, ''),Function(set_scene_enable, False),SetVariable('on_main_screen', True),Show(location), Hide(curr_screen),]

# toolbox
transform tools_extra_small():
    zoom 0.06

screen toolbox_screen():
   
    hbox:
        xpos 0.015 ypos 0.09
        imagebutton:
            idle 'toolbox' at Transform(zoom=0.45) 
            hover "toolbox_hover"
            selected 'toolbox_open'

            hovered Notify("Toolbox")
            unhovered Notify('')

            action [Function(set_cursor, ''), ToggleVariable('toolbox_show'), ToggleScreen("case_files_screen", _layer="over_screens")]

    
    showif toolbox_show and on_main_screen:
        hbox:
                xpos 0.89 ypos 0
                imagebutton:
                    insensitive "uv_light_idle" at tools_extra_small
                    idle "uv_light_idle" 
                    hover "uv_light_hover"

                    hovered Notify("flashlight")
                    unhovered Notify('')

                    action[Function(set_tool, 'light')]
                    sensitive scene_enable['light']
        hbox:
            xpos 0.892 ypos 0.20
            imagebutton:
                insensitive "evidence_markers" at tools_extra_small
                idle "evidence_markers"
                hover "evidence_markers_hover"

                hovered Notify("evidence markers")
                unhovered Notify('')

                action [SensitiveIf(on_main_screen),Function(set_tool, 'marker')]

    showif toolbox_show and not on_main_screen:
        hbox:
            xpos 0.888 ypos 0.365
            imagebutton:
                insensitive "scalebar_idle" at tools_extra_small
                idle "scalebar_idle"
                hover "scalebar_hover"

                hovered Notify("scale bar")
                unhovered Notify('')

                action[Function(set_tool, 'scalebar')]
                sensitive scene_enable['scalebar']

        hbox:
            xpos 0.890 ypos 0.53
            imagebutton:
                insensitive "lifting_backing_idle" at tools_extra_small
                idle "lifting_backing_idle"
                hover "lifting_backing_hover"

                hovered Notify("fingerprint lifting tape")
                unhovered Notify('')

                action[Function(set_tool, 'lifting_tape')]
                sensitive scene_enable['lifting_tape']

        # hbox:
        #     xpos 0.004 ypos 0.3
        #     imagebutton:
        #         insensitive "evident_tape_idle" at tools_extra_small
        #         idle "evident_tape_idle"
        #         hover "evident_tape_hover"

        #         hovered Notify("evident tape")
        #         unhovered Notify('')

        #         action[Function(set_tool, 'tape')]
        #         sensitive scene_enable['tape']

        hbox:
            xpos 0.032 ypos 0.3
            imagebutton:
                insensitive "evidence_bags" at Transform(zoom=0.25)
                idle "evidence_bags"
                hover "evidence_bags_hover"

                hovered Notify("evidence bags")
                unhovered Notify('')

                action[Function(set_tool, 'bag')]
                sensitive scene_enable['bag']

        hbox:
            xpos 0.895 ypos 0.20
            imagebutton:   
                insensitive "magnetic_powder" at tools_extra_small
                idle "magnetic_powder"
                hover "hover_magnetic_powder"

                hovered Notify("granular powder")
                unhovered Notify('')

                action[Function(set_tool, 'powder')]
                sensitive scene_enable['powder']
                

        hbox:
            xpos 0.89 ypos 0
            imagebutton:
                insensitive "uv_light_idle" at tools_extra_small
                idle "uv_light_idle" 
                hover "uv_light_hover"

                hovered Notify("flashlight")
                unhovered Notify('')

                action[Function(set_tool, 'light')]
                sensitive scene_enable['light']
        hbox:
            xpos 0.895 ypos 0.76
            imagebutton:
                insensitive "gel_lift" at Transform(zoom=0.8)
                idle "gel_lift" 
                hover "gel_lift_hover"

                hovered Notify("gel lift")
                unhovered Notify('')

                action[Function(set_tool, 'gel_lift')]
                sensitive scene_enable['gel_lift']



screen scene_evidence_markers_place():
    image "office_bg"
    imagemap:
        
        idle "office_bg"
        hover "office_bg"

        hotspot(334,807,140,168) action [Jump("show_office_footprints")] sensitive uv_light
        hotspot(1140, 605, 124, 27) action [Jump("show_office_screwdriver")] sensitive uv_light
        hotspot(773, 97, 607, 480) action [Jump("show_office_window")] sensitive uv_light
        hotspot(395,186,140,108) action Jump("show_office_books_cabinet") sensitive uv_light
        hotspot(1442,311,146,78) action Jump("show_office_books_cabinet") sensitive uv_light
        hotspot(295,422,130,114) action Jump("show_office_cabinet") sensitive uv_light

# case files screen
screen case_files_screen():
    hbox:
        xpos 0.008 yalign 0.32
        imagebutton:
            idle "case_file_idle" at Transform(zoom=0.45)
            hover "case_file_hover"

            hovered Notify("Evidence")
            unhovered Notify('')

            action ToggleVariable('case_file_evidence_show')
    
    showif case_file_evidence_show:
        # default current = {'screwdriver': False, 'footprints': False, 'window': False}
        default show_evidence = False
        default casefile_main = True
        default show_photos = False
        default title = 'Evidence Collected'
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_inventory"
        hbox:
            xalign 0.5 ypos 0.1
            text title
        
        showif casefile_main:

            hbox:
                xpos 0.20 ypos 0.20
                imagebutton:
                    idle "casefile_evidence" at Transform(zoom=0.5)
                    hover "casefile_evidence_hover"
                    action [SetScreenVariable(title, 'Physical Evidence'),SetLocalVariable('casefile_main', False), SetLocalVariable('show_evidence', True)]
            hbox:
                xpos 0.23 ypos 0.53
                text("Evidence Collected")
            
            hbox:
                xpos 0.53 ypos 0.23
                imagebutton:
                    idle "casefile_photos"
                    hover "casefile_photos_hover"
                    action [SetScreenVariable(title, 'Photos'),SetLocalVariable('casefile_main', False), SetLocalVariable('show_photos', True)]
            hbox:
                xpos 0.55 ypos 0.53
                text("Evidence Photos")

        showif not casefile_main:
            hbox:
                xpos 0.175 ypos 0.1
                textbutton('Back'):
                    style "back_button" 
                    action [SetLocalVariable('show_evidence', False), SetLocalVariable('show_photos', False), Function(photo_switch, 'reset'),SetLocalVariable('casefile_main', True)]
        
        showif show_evidence:
            showif 'screwdriver' in processed:
                hbox:
                    xpos 0.20 ypos 0.30
                    image 'casefile_screwdriver'
            showif 'exam' in processed:
                hbox:
                    xpos 0.38 ypos 0.26
                    image 'casefile_exam' at Transform(zoom=0.5)
            showif 'computer' in processed:
                hbox:
                    xpos 0.52 ypos 0.25
                    image 'casefile_computer' at Transform(zoom=0.8)
        
        showif show_photos:
            hbox:
                xpos 0.8 ypos 0.4
                imagebutton:
                    idle 'casefile_photos_next' at Transform(zoom=0.3)
                    hover 'casefile_photos_next_hover'

                    action [Function(photo_switch, 'next')]
            hbox:
                xpos 0.17 ypos 0.4
                imagebutton:
                    idle 'casefile_photos_prev'at Transform(zoom=0.3)
                    hover 'casefile_photos_prev_hover'
                    
                    action [Function(photo_switch, 'prev')]
            hbox:
                xalign 0.5 yalign 0.48
                image evidence_photos[evidence_photos_counter] at Transform(zoom=0.17)

            



        # showif evidence_marker_set['footprints']:
        #     hbox:
        #         xpos 0.15 ypos 0.20
        #         imagebutton:
        #             idle "case_file_footprints"
        #             hover "case_file_footprints"

        #             action NullAction()
        #     hbox:
        #         xpos 0.24 ypos 0.535
        #         text("{color=#000000}Footprints{/color}")
        
        # showif evidence_marker_set['screwdriver']:
        #     hbox:
        #         xpos 0.35 ypos 0.20
        #         imagebutton:
        #             idle "case_file_screwdriver"
        #             hover "case_file_screwdriver"

        #             action NullAction()
        #     hbox:
        #         xpos 0.43 ypos 0.535
        #         text("{color=#000000}Screwdriver{/color}")
        
        # showif evidence_marker_set['window']:
        #     hbox:
        #         xpos 0.55 ypos 0.20
        #         imagebutton:
        #             idle "case_file_window"
        #             hover "case_file_window"

        #             action NullAction()
        #     hbox:
        #         xpos 0.65 ypos 0.535
        #         text("{color=#000000}Window{/color}")


