screen scene_office():
    image "office_bg"
    
    showif not case_file_evidence_show and not camera_photo_show:
        imagemap:
            idle "office_bg"
            hover "office_bg"

            hotspot(0,460,420,420) action [Jump("show_deskfoot")] mouse "magnify"
            hotspot(500,280,820,320) action [Jump("show_blood")] mouse "magnify"
            hotspot(520,720,330,250) action[ Jump("show_bullet")] mouse "magnify"
            hotspot(1530,740,350,260) action [Jump("show_cheque")] mouse "magnify"

screen end():
    image "office_bg"
    hbox:
        xpos 0.2 ypos 0.85
        textbutton('You have collected all evidences on site, click here to proceed to lab'):
            style "custom_button"
            action [Jump("end")]


screen screen_finished_processing(evidence):
    hbox:
        xpos 0.15 ypos 0.85
        textbutton('Add to evidence bin'):
            style "custom_button"
            action [SetVariable('on_main_screen', True), Hide('screen_finished_processing', _layer='over_screens'),
            Hide('case_files_screen', _layer='over_screens'), Hide('camera_screen', _layer='over_camera'), 
            Hide('toolbox_screen', _layer='over_screens'), Function(finished_process, evidence), 
            Jump('office_start'), Function(set_cursor, '')]


screen scene_deskfoot():
    default empty_ziplock = False
    default ziplock_stone = False
    default ziplock_water = False
    default ziplock_mixed = False
    default poured = False
    default onemin = False
    default hour = False
    default solid = False
    default lift = False
    default tagged = False
    default done = False
    default photo = False

    default wrong_dusted = False
    default under_dusted = False
    default proceeded_under = False
    default good_dusted = False
    default over_dusted = False
    default cleared_dust = False

    if 'deskfoot' not in processed:  
        imagemap:
            idle "deskfoot_zoom"
            hover "deskfoot_zoom"
            hotspot(130,100,1230,880) action [SetLocalVariable('under_dusted', True)] sensitive tools['magnetic_black']
            hotspot(130,100,1230,880) action [SetLocalVariable('wrong_dusted', True), Function(set_cursor, '')] sensitive tools['magnetic_white']
        
        showif wrong_dusted:
            image 'deskfoot_zoom'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Using white magnetic powder against dental stone would not show clear result!\n(click to go back)'):
                    style 'custom_button'
                    action SetLocalVariable('wrong_dusted', False)
        showif under_dusted:
            imagemap:
                idle "deskfoot_dust_under"
                hover "deskfoot_dust_under"
                hotspot(130,100,1230,880) action [SetLocalVariable('good_dusted', True)] sensitive tools['magnetic_black']
                hotspot(130,100,1230,880) action [SetLocalVariable('proceeded_under', True), Function(set_cursor, '')] sensitive tools['applicator']
        showif proceeded_under:
            image 'deskfoot_dust_under'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('That was not enough powder to show clear result! (click to dust more)'):
                    style 'custom_button'
                    action [SetLocalVariable('good_dusted', True), SetLocalVariable('proceeded_under', False)]
        showif good_dusted:
            imagemap:
                idle "deskfoot_dust_good"
                hover "deskfoot_dust_good"
                hotspot(130,100,1230,880) action [SetLocalVariable('over_dusted', True), Function(set_cursor, '')] sensitive tools['magnetic_black']
                hotspot(130,100,1230,880) action [SetLocalVariable('cleared_dust', True)] sensitive tools['applicator'] 
        showif over_dusted:
            image 'deskfoot_dust_over'
            hbox:
                xpos 0.1 ypos 0.85
                textbutton('That is too much magnetic powder! (click to go back)'):
                    style 'custom_button'
                    action SetLocalVariable('over_dusted', False)
        showif cleared_dust:
            imagemap:
                idle "deskfoot_dust_clear"
                hover "deskfoot_dust_clear"
                hotspot(130,100,1230,880) action [SetLocalVariable('empty_ziplock', True)] sensitive tools['ziplock']
        showif empty_ziplock:
            imagemap:
                idle "deskfoot_ziplock"
                hover "deskfoot_ziplock"
                hotspot(130,100,1230,880) action [SetLocalVariable('ziplock_stone', True)] sensitive tools['stone']
        showif ziplock_stone:
            imagemap:
                idle "deskfoot_stone"
                hover "deskfoot_stone"
                hotspot(130,100,1230,880) action [SetLocalVariable('ziplock_water', True), Function(set_cursor, '')] sensitive tools['water']     
        showif ziplock_water:
            image 'deskfoot_water'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Mix together'):
                    style 'custom_button'
                    action SetLocalVariable('ziplock_mixed', True)
        showif ziplock_mixed:
            image 'deskfoot_mix'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Pour mix on footprint'):
                    style 'custom_button'
                    action SetLocalVariable('poured', True)
        showif poured:
            image 'deskfoot_poured'
            hbox:
                xalign 0.5 ypos 0.1
                text "Wait for the cast to cure"
            hbox:
                xpos 0.15 ypos 0.2
                textbutton('1 minute'):
                    style 'custom_button'
                    action SetLocalVariable('onemin', True)
            hbox:
                xpos 0.15 ypos 0.3
                textbutton('30 minutes'):
                    style 'custom_button'
                    action SetLocalVariable('solid', True)
            hbox:
                xpos 0.15 ypos 0.4
                textbutton('3 hours'):
                    style 'custom_button'
                    action SetLocalVariable('hour', True)          
        showif onemin:
            image 'deskfoot_poured'
            hbox:
                xpos 0.15 ypos 0.5
                textbutton('The cast has not cured! wait longer!\n(click to jump another 30 minutes)'):
                    style 'custom_button'
                    action SetLocalVariable('solid', True)
        showif hour:
            image 'deskfoot_solid'
            hbox:
                xpos 0.15 ypos 0.5
                textbutton('It solidified a long time ago... but ok\n(click to proceed)'):
                    style 'custom_button'
                    action SetLocalVariable('solid', True)
        showif solid:
            image 'deskfoot_solid'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Lift the cast up'):
                    style 'custom_button'
                    action SetLocalVariable('lift', True)
        showif lift:
            imagemap:
                idle "deskfoot_lift"
                hover "deskfoot_lift"
                hotspot(130,100,1230,880) action [SetLocalVariable('tagged', True)] sensitive tools['ruler']
        showif tagged:
            image 'deskfoot_tagged'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action Jump("take_deskfoot")
    
    else:
        image 'deskfoot_gone'
        

screen scene_deskfoot_tobag():
    default bagged = False
    imagemap:
        idle "deskfoot_tagged"
        hover "deskfoot_tagged"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True), Show('screen_finished_processing', evidence='deskfoot',_layer='over_screens')] sensitive tools['bag']
    showif bagged:
        image 'deskfoot_bagged'


screen scene_blood():
    default under_sprayed = False
    default proceed_under_sprayed = False
    default good_sprayed = False
    default over_sprayed = False
    default proceed_good_sprayed = False
    default appeared = False
    default cut = False
    default rulered = False

    if 'blood' not in processed:
        imagemap:
            idle "office_bg"
            hover "office_bg"
            hotspot(500,280,820,320) action [SetLocalVariable('under_sprayed', True)] sensitive tools['hungarian_red']
        
        showif under_sprayed:
            imagemap:
                idle "blood_spray_under"
                hover "blood_spray_under"
                hotspot(500,280,820,320) action [SetLocalVariable('good_sprayed', True)] sensitive tools['hungarian_red']
                hbox:
                    xpos 0.25 ypos 0.85
                    textbutton('Click if you think this is enough dye'):
                        style 'custom_button'
                        action [SetLocalVariable('proceed_under_sprayed', True), Function(set_cursor, '')]
        showif proceed_under_sprayed:
            image 'blood_spray_under'
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('That was not enough! (click here to spray more)'):
                    style 'custom_button'
                    action [SetLocalVariable('good_sprayed', True), Function(set_cursor, '')]       
        showif good_sprayed:
            imagemap:
                idle "blood_spray_good"
                hover "blood_spray_good"
                hotspot(500,280,820,320) action [SetLocalVariable('over_sprayed', True)] sensitive tools['hungarian_red']
                hbox:
                    xpos 0.25 ypos 0.85
                    textbutton('Click if you think this is enough dye'):
                        style 'custom_button'
                        action [SetLocalVariable('proceed_good_sprayed', True), Function(set_cursor, '')]       
        showif over_sprayed:
            image 'blood_spray_over'
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('That is too much, the bllod stains would not be visible!\n(click to go back to last dye level)'):
                    style 'custom_button'
                    action [SetLocalVariable('proceed_good_sprayed', True), Function(set_cursor, '')]        
        showif proceed_good_sprayed:
            image 'blood_spray_good'
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('Wait a few minutes for latent blood to appear'):
                    style 'custom_button'
                    action [SetLocalVariable('appeared', True), Function(set_cursor, '')]        
        showif appeared:
            imagemap:
                idle 'blood_appear'
                hover 'blood_appear'
                hotspot(500,280,820,320) action [SetLocalVariable('cut', True)] sensitive tools['knife']        
        showif cut:
            imagemap:
                idle 'blood_cut'
                hover 'blood_cut'
                hotspot(500,280,820,320) action [SetLocalVariable('rulered', True)] sensitive tools['ruler']        
        showif rulered:
            image 'blood_ruler'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action Jump("take_blood")
    
    else:
        image 'blood_gone'


screen scene_blood_tobag():
    default bagged = False
    imagemap:
        idle 'blood_ruler'
        hover 'blood_ruler'
        hotspot(232,195,1035,580) action [SetLocalVariable('bagged', True), Show('screen_finished_processing', evidence='blood',_layer='over_screens')] sensitive tools['bag']        
    showif bagged:
        image 'blood_bagged'


screen scene_bullet():
    if 'bullet' not in processed:
        image 'bullet_zoom'
        hbox:
            xpos 0.15 ypos 0.85
            textbutton('Take Photo'):
                style 'custom_button'
                action Jump("take_bullet")
    else:
        image 'bullet_gone'


screen scene_bullet_tobag():
    default bagged = False
    imagemap:
        idle "bullet_zoom"
        hover "bullet_zoom"
        hotspot(530,180,900,670) action [SetLocalVariable('bagged', True), Show('screen_finished_processing', evidence='bullet',_layer='over_screens')] sensitive tools['bag']
    showif bagged:
        image 'bullet_bagged'
    

screen scene_cheque():
    if 'cheque' not in processed:
        image 'cheque_zoom'
        hbox:
            xpos 0.15 ypos 0.85
            textbutton('Take Photo'):
                style 'custom_button'
                action Jump("take_cheque")
    else:
        image 'cheque_gone'


screen scene_cheque_tobag():
    default bagged = False
    imagemap:
        idle "cheque_zoom"
        hover "cheque_zoom"
        hotspot(870,140,530,390) action [SetLocalVariable('bagged', True), Show('screen_finished_processing', evidence='cheque',_layer='over_screens')] sensitive tools['bag']
    showif bagged:
        image 'cheque_bagged'
    
    


# back button
screen back_button_screen(location, curr_screen):
    hbox:
        xalign 0.035 yalign 0.96
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Function(set_cursor, ''), Hide('screen_finished_processing', _layer='over_screens'), 
            SetVariable('on_main_screen', True), Jump(location), Hide(curr_screen),]

# toolbox
transform tools_small():
    zoom 0.2

screen toolbox_screen():
   
    hbox:
        xpos 0.015 ypos 0.09
        imagebutton:
            idle 'toolbox' at Transform(zoom=0.35) 
            hover "toolbox_hover"

            hovered Notify("Toolbox")
            unhovered Notify('')

            action [Function(set_cursor, ''), ToggleVariable('toolbox_show'), ToggleScreen("case_files_screen", _layer="over_screens"), ToggleScreen("camera_screen", _layer="over_camera")]

    showif toolbox_show:
        # left_side
        hbox:
            xpos 0.03 ypos 0.26
            imagebutton:
                insensitive "evidence_bags" at tools_small
                idle "evidence_bags"
                hover "evidence_bags_hover"

                hovered Notify("evidence bags")
                unhovered Notify('')

                action[Function(set_tool, 'bag')]
                mouse "glove"
        
        hbox:
            xpos 0.03 ypos 0.41
            imagebutton:
                insensitive "ruler_idle" at tools_small
                idle "ruler_idle" 
                hover "ruler_idle"

                hovered Notify("ruler")
                unhovered Notify('')

                action[Function(set_tool, 'ruler')]
                mouse "glove"
              
        hbox:
            xpos 0.03 ypos 0.53
            imagebutton:
                insensitive "knife_idle" at tools_small
                idle "knife_idle"
                hover "knife_idle"

                hovered Notify("exacto knife")
                unhovered Notify('')

                action[Function(set_tool, 'knife')]
                mouse "glove"

        hbox:
            xpos 0.03 ypos 0.66
            imagebutton:
                insensitive "hungarian_red_idle" at tools_small
                idle "hungarian_red_idle" 
                hover "hungarian_red_idle"

                hovered Notify("hungarian red dye")
                unhovered Notify('')

                action[Function(set_tool, 'hungarian_red')]
                mouse "glove"
        
        # right side
        hbox:
            xpos 0.9 ypos 0.07
            imagebutton:
                insensitive "applicator_idle" at Transform(zoom=0.15)
                idle "applicator_idle" 
                hover "applicator_idle"

                hovered Notify("magnetic powder applicator")
                unhovered Notify('')

                action[Function(set_tool, 'applicator')]
                mouse "glove"

        hbox:
            xpos 0.89 ypos 0.2
            imagebutton:   
                insensitive "magnetic_black_idle" at tools_small
                idle "magnetic_black_idle"
                hover "magnetic_black_idle"

                hovered Notify("black magnetic powder")
                unhovered Notify('')

                action[Function(set_tool, 'magnetic_black')]
                mouse "glove"
                
        hbox:
            xpos 0.89 ypos 0.36
            imagebutton:   
                insensitive "magnetic_white_idle" at tools_small
                idle "magnetic_white_idle"
                hover "magnetic_white_idle"

                hovered Notify("white magnetic powder")
                unhovered Notify('')

                action[Function(set_tool, 'magnetic_white')]
                mouse "glove"
        
        hbox:
            xpos 0.89 ypos 0.52
            imagebutton:
                insensitive "ziplock_idle" at tools_small
                idle "ziplock_idle"
                hover "ziplock_idle"

                hovered Notify("empty zip lock bag")
                unhovered Notify('')

                action[Function(set_tool, 'ziplock')] 
                mouse "glove"

        hbox:
            xpos 0.89 ypos 0.68
            imagebutton:
                insensitive "stone_idle" at tools_small
                idle "stone_idle"
                hover "stone_idle"

                hovered Notify("dental stone powder")
                unhovered Notify('')

                action[Function(set_tool, 'stone')]
                mouse "glove"

        hbox:
            xpos 0.9 ypos 0.84
            imagebutton:
                insensitive "water_idle" at tools_small
                idle "water_idle"
                hover "water_idle"

                hovered Notify("distilled water")
                unhovered Notify('')

                action[Function(set_tool, 'water')]
                mouse "glove"


# casefile evidences
transform casefile_small():
    zoom 0.2

# case files screen
screen case_files_screen():
    hbox:
        xpos 0.02 yalign 0.265
        imagebutton:
            idle "casefile_bin_idle" at Transform(zoom=0.22)
            hover "casefile_bin_hover"

            hovered Notify("Evidence Bin")
            unhovered Notify('')

            action [ToggleVariable('case_file_evidence_show'), SetVariable('camera_photo_show', False)]
    
    showif case_file_evidence_show:
        default title = 'Evidence Collected'
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xalign 0.5 ypos 0.1
            text title
        
        showif 'deskfoot' in processed:
            hbox:
                xpos 0.25 ypos 0.5
                image 'casefile_deskfoot' at casefile_small
        showif 'blood' in processed:
            hbox:
                xpos 0.55 ypos 0.2
                image 'casefile_blood' at casefile_small
        showif 'bullet' in processed:
            hbox:
                xpos 0.25 ypos 0.2
                image 'casefile_bullet' at casefile_small
        showif 'cheque' in processed:
            hbox:
                xpos 0.55 ypos 0.5
                image 'casefile_cheque' at casefile_small

# camera screen
# Change position and zoom
screen camera_screen():
    hbox:
        xpos 0.015 yalign 0.38
        imagebutton:
            idle "camera_idle" at Transform(zoom=0.45)
            hover "camera_hover"

            hovered Notify("Camera")
            unhovered Notify('')

            action [ToggleVariable('camera_photo_show'), SetVariable('case_file_evidence_show', False)]
    
    showif camera_photo_show:
        default title = 'Photos Taken'
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xalign 0.5 ypos 0.1
            text title
        
        showif 'deskfoot' in processed:
            hbox:
                xpos 0.25 ypos 0.5
                image 'camera_deskfoot' at casefile_small
        showif 'blood' in processed:
            hbox:
                xpos 0.55 ypos 0.2
                image 'camera_blood' at casefile_small
        showif 'bullet' in processed:
            hbox:
                xpos 0.25 ypos 0.2
                image 'camera_bullet' at casefile_small
        showif 'cheque' in processed:
            hbox:
                xpos 0.55 ypos 0.5
                image 'camera_cheque' at casefile_small