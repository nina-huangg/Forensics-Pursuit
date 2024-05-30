
screen scene_store():
    
    image "store_bg"
   
    if tools['marker']:
            imagemap:
                idle "store_bg"
                hover "store_bg_hover"

                hotspot(1050,700,900,400) action [SetDict(evidence_marker_set,'tabletop', True)] sensitive tools['marker']
                hotspot(120,500,280,150) action [SetDict(evidence_marker_set,'jewel', True)] sensitive tools['marker']
                hotspot(0,900,550,200) action [SetDict(evidence_marker_set,'inside_footprints', True)] sensitive tools['marker']
                
    else:
        imagemap:
            idle "store_bg"
            hover "store_bg_hover"

            hotspot(1050,700,900,400) action [Jump("show_tabletop")] 
            hotspot(120,500,280,150) action [Jump("show_jewel")]
            hotspot(0,900,550,200) action[ Jump("show_inside_footprints")] 
            hotspot(930,0,400,250) action [Jump("show_storefront")] 

    if evidence_marker_set['tabletop']:
        hbox:
            pos(1200, 850)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['jewel']:
        hbox:
            pos(400, 530)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['inside_footprints']:
        hbox:
            pos(120, 950)
            image "marker" at Transform(zoom=0.2)

screen scene_inside_footprints():
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

                hotspot(412,0,941,1043) action [SetLocalVariable('stick', True), Function(set_cursor, ''),Show('screen_finished_processing',evidence='inside_footprints', _layer='over_screens')] sensitive tools['gel_lift']
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
            action [SetVariable('on_main_screen', True),Hide('screen_finished_processing', _layer='over_screens'), Function(finished_process, evidence), Show('scene_store')]



screen scene_tabletop():
    default dusted = False
    default scalebar = False
    default taped = False
    default lift = False
    default done = False
    default bagged = False

    if uv_light and 'tabletop' not in processed:
        imagemap:
            idle "tabletop_dim"
            hover "tabletop_dim_hover"

            hotspot(1300,720,600,634) action NullAction()
    elif 'tabletop' not in processed:
        imagemap:
            idle "tabletop"
            hover "tabletop_hover"

            hotspot(1200,720,600,634) action SetLocalVariable('dusted', True) sensitive tools['powder']
        showif dusted:
            imagemap:
                idle "tabletop_dusted"
                hover "tabletop_dusted"

                hotspot(1200,720,1400,900) action SetLocalVariable('scalebar', True) sensitive tools['scalebar']
        showif scalebar:
            imagemap:
                idle "tabletop_scalebar"
                hover "tabletop_scalebar"

                hotspot(1200,720,1400,900) action [SetLocalVariable('lift', True), Function(set_cursor, 'fingerprint_lifted')] sensitive tools['lifting_tape']
        showif lift:
            imagemap:
                idle "tabletop_backing"
                hover "tabletop_backing"

                hotspot(450,450,1000,500) action [SetLocalVariable('done', True), Function(set_cursor, '')]
        showif done:
            imagemap:
                idle "tabletop_complete"
                hover "tabletop_complete_hover"

                hotspot(400,450,1000,500) action [SetLocalVariable('bagged', True), Function(set_cursor, ''), Show('screen_finished_processing', evidence='tabletop',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'tabletop_evidence_bag'
    
    else:
        image 'tabletop'

# to be completed (switch screwdriver to jewel)
screen scene_jewel():
    default dusted = False
    default taped = False
    default bagged = False

    if uv_light and 'jewel' not in processed:
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

                hotspot(646,188,809,443) action [SetLocalVariable('bagged', True),Function(set_cursor, ''),Show('screen_finished_processing', evidence='jewel',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'screwdriver_packed'
    else:
        image 'screwdriver_empty_bg'



# back button
screen back_button_screen(location, curr_screen):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Function(set_cursor, ''),Function(set_scene_enable, False),SetVariable('on_main_screen', True),Show(location), Hide(curr_screen),]

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

        hbox:
            xpos 0.004 ypos 0.3
            imagebutton:
                insensitive "evident_tape_idle" at tools_extra_small
                idle "evident_tape_idle"
                hover "evident_tape_hover"

                hovered Notify("evident tape")
                unhovered Notify('')

                action[Function(set_tool, 'tape')]
                sensitive scene_enable['tape']

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
    image "store_bg"
    imagemap:
        
        idle "store_bg"
        hover "store_bg"

        hotspot(1050,700,900,400) action [Jump("show_tabletop")] sensitive uv_light
        hotspot(120,500,280,150) action [Jump("show_jewel")] sensitive uv_light
        hotspot(0,900,550,200) action [Jump("show_inside_footprints")] sensitive uv_light
        hotspot(930,0,400,250) action [Jump("show_storefront")] 


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

        showif not casefile_main:
            hbox:
                xpos 0.175 ypos 0.1
                textbutton('Back'):
                    style "back_button" 
                    action [SetLocalVariable('show_evidence', False),SetLocalVariable('casefile_main', True)]
        
        showif show_evidence:
            showif 'tabletop' in processed:
                hbox:
                    xpos 0.15 ypos 0.20
                    image 'casefile_tabletop' at Transform(zoom=1.2)
            showif 'jewel' in processed:
                hbox:
                    xpos 0.38 ypos 0.26
                    image 'casefile_jewel' at Transform(zoom=0.5)
            showif 'inside_footprints' in processed:
                hbox:
                    xpos 0.45 ypos 0.20
                    image 'case_file_footprints'