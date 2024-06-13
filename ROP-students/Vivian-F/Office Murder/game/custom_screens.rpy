# change hotspots (2 each)------------------------------------------------------------------------------------------
screen scene_office():
    
    if 'blood' not in processed:
        image "office_bg"
    else:
        image "office_cut"
   
    if tools['marker']:
            imagemap:
                idle "office_bg"
                hover "office_bg_hover"

                hotspot(50,609,360,260) action [SetDict(evidence_marker_set,'deskfoot', True)] sensitive tools['marker']
                hotspot(560,349,580,390) action [SetDict(evidence_marker_set,'blood', True)] sensitive tools['marker']
                hotspot(560,949,40,100) action [SetDict(evidence_marker_set,'bullet', True)] sensitive tools['marker']
                hotspot(1560,773,200,120) action [SetDict(evidence_marker_set,'cheque', True)] sensitive tools['marker']

    # Once markers set, hover over to see magnifying glass for mouse indicating possible search (no image change)            
    else:
        imagemap:
            idle "office_bg"
            hover "office_bg"

            hotspot(50,609,360,260) action [Function(set_cursor, 'magnify'), Jump("show_deskfoot")] 
            hotspot(560,349,580,390) action [Jump("show_blood"), Function(set_cursor, 'magnify')]
            hotspot(560,949,40,100) action[ Jump("show_bullet"), Function(set_cursor, 'magnify')] 
            hotspot(1560,773,200,120) action [Jump("show_cheque"), Function(set_cursor, 'magnify')] 

    if evidence_marker_set['deskfoot']:
        hbox:
            pos(86, 470)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['blood']:
        hbox:
            pos(490, 330)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['bullet']:
        hbox:
            pos(747, 923)
            image "marker" at Transform(zoom=0.2)
    if evidence_marker_set['cheque']:
        hbox:
            pos(1535, 949)
            image "marker" at Transform(zoom=0.2)


screen screen_finished_processing(evidence):
    hbox:
        xpos 0.65 ypos 0.90
        textbutton('Add to case files'):
            style "custom_button"
            action [SetVariable('on_main_screen', True),Function(set_cursor, ''),Hide('screen_finished_processing', _layer='over_screens'), Function(finished_process, evidence), Show('scene_office')]


screen scene_deskfoot():
    default dusted = False
    default empty_bucket = False
    default bucket_stone = False
    default bucket_water = False
    default bucket_mixed = False
    default poured = False
    default solid = False
    default lift = False
    default tagged = False
    default done = False
    default bagged = False

    # if uv_light and 'deskfoot' not in processed:
    #     imagemap:
    #         idle "deskfoot_dim"
    #         hover "deskfoot_dim_hover"

    #         hotspot(1300,720,600,634) action NullAction()
    if 'deskfoot' not in processed:
        imagemap:
            idle "deskfoot_zoom"
            hover "deskfoot_zoom"

            hotspot(233,187,1265,750) action [SetLocalVariable('dusted', True), Function(set_cursor, 'bucket')] sensitive tools['magnetic']
        showif dusted:
            imagemap:
                idle "deskfoot_dusted"
                hover "deskfoot_dusted"

                hotspot(233,187,1265,750) action [SetLocalVariable('empty_bucket', True), Function(set_cursor, 'bucket')] sensitive tools['bucket']
        showif empty_bucket:
            imagemap:
                idle "deskfoot_bucket"
                hover "deskfoot_bucket"

                hotspot(233,187,1265,750) action [SetLocalVariable('bucket_stone', True), Function(set_cursor, 'stone')] sensitive tools['stone']
        showif bucket_stone:
            imagemap:
                idle "deskfoot_stone"
                hover "deskfoot_stone"

                hotspot(233,187,1265,750) action [SetLocalVariable('bucket_water', True), Function(set_cursor, 'water')] sensitive tools['water']
        showif bucket_water:
            image 'deskfoot_water'
            hbox:
                xpos 0.65 ypos 0.90
                textbutton('Mix together'):
                    style 'custom_button'
                    action [SetLocalVariable('bucket_mixed', True), Function(set_cursor, '')] sensitive False
        showif bucket_mixed:
            image 'deskfoot_mix'
            hbox:
                xpos 0.65 ypos 0.90
                textbutton('Pour mix on footprint'):
                    style 'custom_button'
                    action SetLocalVariable('poured', True) sensitive False
        showif poured:
            image 'deskfoot_poured'
            hbox:
                xpos 0.65 ypos 0.90
                textbutton('Wait for cast to cure'):
                    style 'custom_button'
                    action SetLocalVariable('solid', True) sensitive False
        showif solid:
            image 'deskfoot_solid'
            hbox:
                xpos 0.65 ypos 0.90
                textbutton('Lift the cast up'):
                    style 'custom_button'
                    action SetLocalVariable('lift', True) sensitive False
        showif lift:
            imagemap:
                idle "deskfoot_lift"
                hover "deskfoot_lift"

                hotspot(233,187,1265,750) action [SetLocalVariable('tagged', True), Function(set_cursor, 'ruler_tag')] sensitive tools['ruler_tag']
        showif tagged:
            imagemap:
                idle "deskfoot_tagged"
                hover "deskfoot_tagged"

                hotspot(233,187,1265,750) action [SetLocalVariable('bagged', True), Function(set_cursor, 'bag'), Show('screen_finished_processing', evidence='deskfoot',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'deskfoot_evidence_bag'
    
    else:
        image 'deskfoot_gone'


screen scene_blood():
    default sprayed = False
    default appeared = False
    default cut = False
    default bagged = False

    
    if 'blood' not in processed:
        imagemap:
            idle "office_bg"
            hover "office_bg"

            hotspot(560,349,580,390) action [SetLocalVariable('sprayed', True), Function(set_cursor, 'hungarian_red')] sensitive tools['hungarian_red']
        showif sprayed:
            image 'blood_sprayed'
            hbox:
                xpos 0.65 ypos 0.90
                textbutton('Wait for latent blood to appear'):
                    style 'custom_button'
                    action SetLocalVariable('appeared', True) sensitive False
        showif appeared:
            imagemap:
                idle 'blood_appear'
                hover 'blood_appear'

                hotspot(560,349,580,390) action [SetLocalVariable('cut', True), Function(set_cursor, 'knife')] sensitive tools['knife']
        showif cut:
            imagemap:
                idle 'blood_cut'
                hover 'blood_cut'

                hotspot(560,349,580,390) action [SetLocalVariable('bagged', True), Function(set_cursor, 'bag'), Show('screen_finished_processing', evidence='blood',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'blood_packed'
    else:
        image 'office_cut'


screen scene_bullet():
    default bagged = False

    if 'bullet' not in processed:
        imagemap:
            idle "bullet_zoom"
            hover "bullet_zoom"

            hotspot(233,187,1265,750) action [SetLocalVariable('bagged', True), Function(set_cursor, 'bag'), Show('screen_finished_processing', evidence='bullet',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'bullet_packed'
    else:
        image 'bullet_gone'


screen scene_cheque():
    default bagged = False

    if 'cheque' not in processed:
        imagemap:
            idle "cheque_zoom"
            hover "cheque_zoom"

            hotspot(233,187,1265,750) action [SetLocalVariable('bagged', True), Function(set_cursor, 'bag'), Show('screen_finished_processing', evidence='cheque',_layer='over_screens')] sensitive tools['bag']
        showif bagged:
            image 'cheque_packed'
    else:
        image 'cheque_gone'


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
            xpos 0.03 ypos 0.5
            imagebutton:
                insensitive "bucket_idle" at Transform(zoom=0.25)
                idle "bucket_idle"
                hover "bucket_idle"

                hovered Notify("empty zip lock bag")
                unhovered Notify('')

                action[Function(set_tool, 'bucket')] sensitive scene_enable['bucket']

        hbox:
            xpos 0.890 ypos 0.5
            imagebutton:
                insensitive "stone_idle" at Transform(zoom=0.25)
                idle "stone_idle"
                hover "stone_idle"

                hovered Notify("dental stone powder")
                unhovered Notify('')

                action[Function(set_tool, 'stone')]
                sensitive scene_enable['stone']

        hbox:
            xpos 0.03 ypos 0.8
            imagebutton:
                insensitive "water_idle" at Transform(zoom=0.25)
                idle "water_idle"
                hover "water_idle"

                hovered Notify("distilled water")
                unhovered Notify('')

                action[Function(set_tool, 'water')]
                sensitive scene_enable['water']

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
            xpos 0.03 ypos 0.65
            imagebutton:
                insensitive "knife_idle" at Transform(zoom=0.25)
                idle "knife_idle"
                hover "knife_idle"

                hovered Notify("knife")
                unhovered Notify('')

                action[Function(set_tool, 'knife')]
                sensitive scene_enable['knife']

        hbox:
            xpos 0.895 ypos 0.20
            imagebutton:   
                insensitive "magnetic_powder" at tools_extra_small
                idle "magnetic_powder"
                hover "hover_magnetic_powder"

                hovered Notify("granular powder")
                unhovered Notify('')

                action[Function(set_tool, 'magnetic')]
                sensitive scene_enable['magnetic']
                

        hbox:
            xpos 0.89 ypos 0
            imagebutton:
                insensitive "ruler_tag_idle" at tools_extra_small
                idle "ruler_tag_idle" 
                hover "ruler_tag_idle"

                hovered Notify("ruler and tag")
                unhovered Notify('')

                action[Function(set_tool, 'ruler_tag')]
                sensitive scene_enable['ruler_tag']
        hbox:
            xpos 0.895 ypos 0.7
            imagebutton:
                insensitive "hungarian_red_idle" at Transform(zoom=0.25)
                idle "hungarian_red_idle" 
                hover "hungarian_red_idle"

                hovered Notify("hungarian red")
                unhovered Notify('')

                action[Function(set_tool, 'hungarian_red')]
                sensitive scene_enable['hungarian_red']


# change hotspot----------------------------------------------------------------------------------------------
screen scene_evidence_markers_place():
    image "office_bg"
    imagemap:
        
        idle "office_bg"
        hover "office_bg"

        hotspot(1050,700,900,400) action [Jump("show_deskfoot")] sensitive uv_light
        hotspot(120,500,280,150) action [Jump("show_blood")]
        hotspot(0,900,550,200) action [Jump("show_bullet")]
        hotspot(930,0,400,250) action [Jump("show_cheque")] 


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
            showif 'deskfoot' in processed:
                hbox:
                    xpos 0.15 ypos 0.20
                    image 'casefile_deskfoot' at Transform(zoom=1.2)
            showif 'blood' in processed:
                hbox:
                    xpos 0.38 ypos 0.26
                    image 'casefile_blood' at Transform(zoom=0.5)
            showif 'bullet' in processed:
                hbox:
                    xpos 0.45 ypos 0.20
                    image 'casefile_bullet'
            showif 'cheque' in processed:
                hbox:
                    xpos 0.60 ypos 0.20
                    image 'casefile_cheque'