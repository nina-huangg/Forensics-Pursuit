"""
Note: for all scenarios to return back to no-tool and default cursor,
    function set_tool is called on last supposedly effective tool to toggle availability
    straight up calling set_cursor bugs out and affects all cursor change.
Exception case in screen toolbox for toggling 'marker' -- comment included there
"""


# Start/Finish
# Main Screen
screen scene_office():
    image "office_bg"   # default background

    # All imagemaps should show when casefile and camera are both not open
    # This avoid hoverin or clicking changes happen when looking throuh file/camera
    
    # Before markers are set, tool can be marker, allow hotspot to place
    if tools['marker']:
        showif not case_file_evidence_show and not camera_photo_show:
            imagemap:
                idle "office_bg"
                hover "office_bg"

                hotspot(0,460,420,420) action [SetDict(evidence_marker_set,'deskfoot', True)] sensitive tools['marker']
                hotspot(500,280,820,320) action [SetDict(evidence_marker_set,'blood', True)] sensitive tools['marker']
                hotspot(520,720,330,250) action [SetDict(evidence_marker_set,'bullet', True)] sensitive tools['marker']
                hotspot(1530,740,350,260) action [SetDict(evidence_marker_set,'cheque', True)] sensitive tools['marker']

    # When tool not marker but markers not all placed
    # Show magnify hovering but clicking has no actions so markers are forced
    elif not all(evidence_marker_set[evidence] for evidence in evidence_marker_set):
        showif not case_file_evidence_show and not camera_photo_show:
            imagemap:
                idle "office_bg"
                hover "office_bg"

                hotspot(0,460,420,420) action NullAction() mouse "magnify"
                hotspot(500,280,820,320) action NullAction() mouse "magnify"
                hotspot(520,720,330,250) action NullAction() mouse "magnify"
                hotspot(1530,740,350,260) action NullAction() mouse "magnify"
    
    # When all markers placed, hover with magnify and clicking jumps to detail scene
    else:
        showif not case_file_evidence_show and not camera_photo_show:
            imagemap:
                idle "office_bg"
                hover "office_bg"

                hotspot(0,460,420,420) action [Jump("show_deskfoot")] mouse "magnify"
                hotspot(500,280,820,320) action [Jump("show_blood")] mouse "magnify"
                hotspot(520,720,330,250) action [Jump("show_bullet")] mouse "magnify"
                hotspot(1530,740,350,260) action [Jump("show_cheque")] mouse "magnify"
    
    # Place images of post-evidence collection (evidence not in place)
    # Note: office_deskfoot/blood has pixel overlap, blood must appear after
    if 'deskfoot' in processed: 
        hbox:
            pos(0, 0)
            image "office_deskfoot"
    
    if 'blood' in processed: 
        hbox:
            pos(427, 0)
            image "office_blood"
    
    if 'bullet' in processed: 
        hbox:
            pos(523, 905)
            image "office_bullet"
    
    if 'cheque' in processed: 
        hbox:
            pos(1303, 0)
            image "office_cheque"

    # Place evidence markers on top of all previous images layers
    if evidence_marker_set['deskfoot']:
        hbox:
            pos(128, 496)
            image "marker_deskfoot" at Transform(zoom=0.9)
    if evidence_marker_set['blood']:
        hbox:
            pos(1022, 373)
            image "marker_blood" at Transform(zoom=0.9)
    if evidence_marker_set['bullet']:
        hbox:
            pos(535, 749)
            image "marker_bullet" at Transform(zoom=0.5)
    if evidence_marker_set['cheque']:
        hbox:
            pos(1775, 815)
            image "marker_cheque" at Transform(zoom=0.9)
    
    # # When all evidence collected and prompt to proceed to lab
    if all(evidence in processed for evidence in should_be_examined):
        # can add line here to auto-pop casefile to show evidence
        hbox:
            xpos 0.2 ypos 0.85
            textbutton('You have collected all evidences on site, click here to proceed to lab'):
                style "custom_button"
                action [Jump("end")]


# Post evidence bag 
# Back to main screen, hide current and collapse pop screens, 
# add photo and evidence image to camera and evidence bin (casefile),
# jump back to office scene and restart cursor
screen screen_finished_processing(evidence):
    hbox:
        xpos 0.15 ypos 0.85
        textbutton('Add to evidence bin'):
            style "custom_button"
            action [SetVariable('on_main_screen', True), 
            Hide('screen_finished_processing', _layer='over_screens'),
            Hide('case_files_screen', _layer='over_screens'), 
            Hide('camera_screen', _layer='over_camera'), 
            Hide('toolbox_screen', _layer='over_screens'),
            Function(add_photo, evidence), Function(finished_process, evidence), 
            Jump('office_start'), Function(set_cursor, '')]
        # do not change order to these!



# Evidence Collection
# Waxy footprint on desk: magnetic powder (mistake) - dust (mistake) - mix cast (mistake) 
#                           - cast (mitake) - lift - tag - photo - bag
screen scene_deskfoot():
    # Define local variables to track stage of processing
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
    # dusting variables
    default wrong_dusted = False
    default under_dusted = False
    default proceeded_under = False
    default good_dusted = False
    default over_dusted = False
    default cleared_dust = False
    default no_dust = False

    # Start processed if not done: first magnetic powder (2 choice)
    if 'deskfoot' not in processed:  
        imagemap:
            idle "deskfoot_zoom"
            hover "deskfoot_zoom"
            hotspot(130,100,1230,880) action [SetLocalVariable('under_dusted', True)] sensitive tools['magnetic_black']
            hotspot(130,100,1230,880) action [SetLocalVariable('wrong_dusted', True), Function(set_cursor, '')] sensitive tools['magnetic_white']
        # magnetic_white (mistake) sends back to above by setting variable False
        showif wrong_dusted:
            image 'deskfoot_zoom'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Using white magnetic powder against dental stone would not show clear result!\n(click to go back)'):
                    style 'custom_button'
                    action SetLocalVariable('wrong_dusted', False)
        # Once powdered is not enough: good_dusted if powder more
        # proceed_under if proceed to dust or mix cast
        showif under_dusted:
            imagemap:
                idle "deskfoot_dust_under"
                hover "deskfoot_dust_under"
                hotspot(130,100,1230,880) action [SetLocalVariable('good_dusted', True)] sensitive tools['magnetic_black']
                hotspot(130,100,1230,880) action [SetLocalVariable('proceeded_under', True), Function(set_cursor, '')] sensitive tools['brush']
                hotspot(130,100,1230,880) action [SetLocalVariable('proceeded_under', True), Function(set_cursor, '')] sensitive tools['ziplock']
        # Proceeded with once powder (mistake) and forward to good_dusted
        showif proceeded_under:
            image 'deskfoot_dust_under'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('That was not enough powder to show clear result! (click to dust more)'):
                    style 'custom_button'
                    action [SetLocalVariable('good_dusted', True), SetLocalVariable('proceeded_under', False)]
        # With enough powder (twice powder or from proceeded_under)
        # More powder is over_dusted, brushing excess is correctly clearly_dusted
        # Skip dusting to mix cast is no_dust
        showif good_dusted:
            imagemap:
                idle "deskfoot_dust_good"
                hover "deskfoot_dust_good"
                hotspot(130,100,1230,880) action [SetLocalVariable('over_dusted', True), Function(set_cursor, '')] sensitive tools['magnetic_black']
                hotspot(130,100,1230,880) action [SetLocalVariable('cleared_dust', True)] sensitive tools['brush']
                hotspot(130,100,1230,880) action [SetLocalVariable('no_dust', True)] sensitive tools['ziplock']
        # Over/No dusting (mistake) sends back to good_dusted by False local
        showif over_dusted:
            image 'deskfoot_dust_over'
            hbox:
                xpos 0.1 ypos 0.85
                textbutton('That is too much magnetic powder! (click to go back)'):
                    style 'custom_button'
                    action SetLocalVariable('over_dusted', False)
        showif no_dust:
            image 'deskfoot_dust_good'
            hbox:
                xpos 0.1 ypos 0.85
                textbutton('You must dust off excess powder before casting it! (click to go back)'):
                    style 'custom_button'
                    action SetLocalVariable('no_dust', False)
        # Correctly dusting allows to proceed to mixing cast mixture
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
            image 'good_water'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Mix together'):
                    style 'custom_button'
                    action SetLocalVariable('ziplock_mixed', True)
        showif ziplock_mixed:
            image 'good_mix'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Pour mix on footprint'):
                    style 'custom_button'
                    action SetLocalVariable('poured', True)
        # Poured cast allow menu choice for wait time
        # 1 min is under (mistake), 3 hrs is over but not mistake
        # both jumps forward to correctly waited 30 min (solid)
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
                hotspot(130,100,1230,880) action [Function(set_tool, 'ruler'), SetLocalVariable('tagged', True)] sensitive tools['ruler']
                # set_tool toggles to unselect ruler tool before take photo button 
        # Once tagged with ruler and tag, display button to take photo and send to label take_deskfoot
        showif tagged:
            image 'deskfoot_tagged'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action [Jump("take_deskfoot")]
    
    # If already processed, show empty desk
    else:
        image 'deskfoot_gone'
        
# After photo taken (flashed), send here from label take_deskfoot
# Final step to bag and screen_finished_processing
screen scene_deskfoot_tobag():
    default bagged = False
    imagemap:
        idle "deskfoot_tagged"
        hover "deskfoot_tagged"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True), Function(set_tool, 'bag'),
            Show('screen_finished_processing', evidence='deskfoot',_layer='over_screens')] sensitive tools['bag']
        # set_tool toggles to unselect bag tool before return to main screen 
    showif bagged:
        image 'deskfoot_bagged'
        


# Latnet blood on floor: Hungarian Red spray (mistake) - cut - ruler - photo - bag
screen scene_blood():
    # Define local variables to track stage of processing
    default under_sprayed = False
    default proceed_under_sprayed = False
    default good_sprayed = False
    default over_sprayed = False
    default proceed_good_sprayed = False
    default appeared = False
    default cut = False
    default rulered = False

    # Start processed if not done: first hungarian red dye spray
    if 'blood' not in processed:
        imagemap:
            idle "office_bg"
            hover "office_bg"
            hotspot(500,280,820,320) action [SetLocalVariable('under_sprayed', True)] sensitive tools['hungarian_red']
        # Spray once is not enough, good if spray again, proceed_under if clicked enough
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
        # One layer click enough (mistake) send automatically to good_sprayed
        showif proceed_under_sprayed:
            image 'blood_spray_under'
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('That was not enough! (click here to spray more)'):
                    style 'custom_button'
                    action [SetLocalVariable('good_sprayed', True), Function(set_cursor, '')]       
        # Enough spray (twice or from under), can go over or press enough to proceed_good
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
        # Over jumps forward to proceed_good_sprayed
        showif over_sprayed:
            image 'blood_spray_over'
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('That is too much, the bllod stains would not be visible!\n(click to proceede with last dye level)'):
                    style 'custom_button'
                    action [SetLocalVariable('proceed_good_sprayed', True), Function(set_cursor, '')]        
        # Hungarian red dye reveals latent blood maybe within few seconds even 
        # so no muistake point here for how long to wait
        showif proceed_good_sprayed:
            image 'blood_spray_good'
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('Take a pause for latent blood to appear'):
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
                hotspot(500,280,820,320) action [Function(set_tool, 'ruler'), SetLocalVariable('rulered', True)] sensitive tools['ruler']  
                # set_tool toggles to unselect ruler tool before take photo button       
        # After place ruler, take photo with evidence marker in scene -- jump to label take_blood 
        showif rulered:
            image 'blood_ruler'
            hbox:
                xpos 0.15 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action [Jump("take_blood")]
    
    # When already processed, show scene with carpet cut out -- shows flooring
    else:
        image 'blood_gone'

# After photo, here from label take_blood -- bag carpet and screen_finished_processing
screen scene_blood_tobag():
    default bagged = False
    imagemap:
        idle 'blood_ruler'
        hover 'blood_ruler'
        hotspot(232,195,1035,580) action [SetLocalVariable('bagged', True), Function(set_tool, 'bag'),
            Show('screen_finished_processing', evidence='blood',_layer='over_screens')] sensitive tools['bag'] 
        # set_tool toggles to unselect bag tool before return to main screen 
    showif bagged:
        image 'blood_bagged'


# Bullet cartridge: photo by jump to label take_bullet -- bag
screen scene_bullet():
    if 'bullet' not in processed:
        image 'bullet_zoom'
        hbox:
            xpos 0.15 ypos 0.85
            textbutton('Take Photo'):
                style 'custom_button'
                action Jump("take_bullet")
    else:
        image 'bullet_gone' # bullet taken out of scene after processed

# After photo, here from label take_bullet -- bag and screen_finished_processing
screen scene_bullet_tobag():
    default bagged = False
    imagemap:
        idle "bullet_zoom"
        hover "bullet_zoom"
        hotspot(530,180,900,670) action [SetLocalVariable('bagged', True), Function(set_tool, 'bag'),
            Show('screen_finished_processing', evidence='bullet',_layer='over_screens')] sensitive tools['bag']
        # set_tool toggles to unselect bag tool before return to main screen 
    showif bagged:
        image 'bullet_bagged'
    

# Cheque: photo by jump to label take_cheque -- bag
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

# After photo, here from label take_cheque -- bag and screen_finished_processing
screen scene_cheque_tobag():
    default bagged = False
    imagemap:
        idle "cheque_zoom"
        hover "cheque_zoom"
        hotspot(870,140,530,390) action [SetLocalVariable('bagged', True), Function(set_tool, 'bag'),
            Show('screen_finished_processing', evidence='cheque',_layer='over_screens')] sensitive tools['bag']
        # set_tool toggles to unselect bag tool before return to main screen 
    showif bagged:
        image 'cheque_bagged'
    
    

# Back Button (only used for returning to main screen for now in script)
screen back_button_screen(location, curr_screen):
    hbox:
        xalign 0.035 yalign 0.96
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Function(set_cursor, ''),
                    Hide('screen_finished_processing', _layer='over_screens'), 
                    SetVariable('on_main_screen', True), Jump(location), Hide(curr_screen)]


# Toolbox
transform tools_small():
    zoom 0.17

screen toolbox_screen():
    default mag_powder_ypos = 0
    # Toolbox icon (always show)
    hbox:
        xpos 0.015 ypos 0.09
        imagebutton:
            idle 'toolbox' at Transform(zoom=0.35) 
            hover "toolbox_hover"

            hovered Notify("Toolbox")
            unhovered Notify('')

            action [Function(set_cursor, ''), ToggleVariable('toolbox_show'), 
                    ToggleScreen("case_files_screen", _layer="over_screens"), ToggleScreen("camera_screen", _layer="over_camera")]
    # Toolbox contents
    showif toolbox_show:
        hbox:
            xalign 0.0 yalign 0.3
            image "toolbox_bg" at Transform(zoom=0.55, alpha=0.9)
        # hbox:
        #     xalign 0.5 yalign 0.003
        #     text title
        # Tools will display in gallery (show one at a time and press arrow to change)
        # Left arrow
        hbox:   
            xpos 0.038 ypos 0.24
            imagebutton:
                idle 'tools_prev'at Transform(zoom=0.2)
                hover 'tools_prev_hover'
                
                action [Function(tools_switch, 'prev')]
        # Right arrow
        hbox:   
            xpos 0.038 ypos 0.815
            imagebutton:
                idle 'tools_next' at Transform(zoom=0.2)
                hover 'tools_next_hover' 

                action [Function(tools_switch, 'next')]
            
        # When not all markers are placed, only tool avaiable is marker
        if not all(evidence_marker_set[evidence] for evidence in evidence_marker_set):
            hbox:
                xpos 0.017 ypos 0.275
                imagebutton:
                    insensitive "evidence_markers" at Transform(zoom=0.04) 
                    idle "evidence_markers"
                    hover "evidence_markers_hover"

                    hovered Notify("evidence markers")
                    unhovered Notify('')

                    action [Function(set_tool, 'marker')]
                    mouse "marker"
    
        # Disable marker after placing last marker (all placed but tool marker)
        elif tools['marker']:        
            # Don't use set_tool here: keeps glitching the cursor to marker when starting
            $ set_cursor('')
            $ tools['marker'] = False        
        
        # Normal analyzation after markers placed, show all tools to use top bar
        # Cursor changes to gloves when hover over tools' icon
        # Tool + cursor changes to tool selected after clicked icon (set_tool)
        elif not on_main_screen:
            if tools_name_list[tools_counter] == 'applicator':
                $ (mag_powder_ypos) = 0.285
            elif tools_name_list[tools_counter + 1] == 'applicator':
                $ (mag_powder_ypos) = 0.43
            elif tools_name_list[tools_counter + 2] == 'applicator':
                $ (mag_powder_ypos) = 0.57
            elif tools_name_list[tools_counter + 3] == 'applicator':
                $ (mag_powder_ypos) = 0.7
            else:
                $ (mag_powder_ypos) = 0

            hbox:
                xpos 0.018 ypos 0.285
                imagebutton:
                    insensitive tools_image_list[tools_counter] at tools_small
                    idle tools_image_list[tools_counter] 
                    hover tools_image_list[tools_counter]

                    hovered Notify(tools_name_list[tools_counter])
                    unhovered Notify('')

                    action[Function(set_tool, tools_name_list[tools_counter])]
                    mouse "glove"

            hbox:
                xpos 0.018 ypos 0.43
                imagebutton:
                    insensitive tools_image_list[tools_counter + 1] at tools_small
                    idle tools_image_list[tools_counter + 1] 
                    hover tools_image_list[tools_counter + 1]

                    hovered Notify(tools_name_list[tools_counter + 1])
                    unhovered Notify('')

                    action[Function(set_tool, tools_name_list[tools_counter + 1])]
                    mouse "glove"
            hbox:
                xpos 0.018 ypos 0.57
                imagebutton:
                    insensitive tools_image_list[tools_counter + 2] at tools_small
                    idle tools_image_list[tools_counter + 2] 
                    hover tools_image_list[tools_counter + 2]

                    hovered Notify(tools_name_list[tools_counter + 2])
                    unhovered Notify('')

                    action[Function(set_tool, tools_name_list[tools_counter + 2])]
                    mouse "glove"

            hbox:
                xpos 0.018 ypos 0.7
                imagebutton:
                    insensitive tools_image_list[tools_counter + 3] at tools_small
                    idle tools_image_list[tools_counter + 3] 
                    hover tools_image_list[tools_counter + 3]

                    hovered Notify(tools_name_list[tools_counter + 3])
                    unhovered Notify('')

                    action[Function(set_tool, tools_name_list[tools_counter + 3])]
                    mouse "glove"
            
            showif tools["applicator"]:
                hbox:
                    xpos 0.0885 ypos (mag_powder_ypos - 0.024)
                    image "toolbox_snd_bg" at Transform(zoom=0.55, alpha=0.9)
                hbox:
                    xpos 0.095 ypos (mag_powder_ypos)
                    imagebutton:
                        insensitive "magnetic_black_idle" at tools_small
                        idle "magnetic_black_idle" 
                        hover "magnetic_black_idle"

                        hovered Notify("black magnetic powder")
                        unhovered Notify('')

                        action[Function(set_tool, "magnetic_black")]
                        mouse "glove"

                hbox:
                    xpos 0.095 ypos (mag_powder_ypos + 0.14)
                    imagebutton:
                        insensitive "magnetic_white_idle" at tools_small
                        idle "magnetic_white_idle" 
                        hover "magnetic_white_idle"

                        hovered Notify("white magnetic powder")
                        unhovered Notify('')

                        action[Function(set_tool, "magnetic_white")]
                        mouse "glove"



# Casefile Evidences
transform casefile_small():
    zoom 0.2

screen case_files_screen():
    # Evidence bin icon (always show)
    hbox:
        xpos 0.02 yalign 0.265
        imagebutton:
            idle "casefile_bin_idle" at Transform(zoom=0.22)
            hover "casefile_bin_hover"

            hovered Notify("Evidence Bin")
            unhovered Notify('')

            action [ToggleVariable('case_file_evidence_show'), SetVariable('camera_photo_show', False)]
    # Evidence bin contents
    showif case_file_evidence_show:
        default title = 'Evidence Collected'
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xalign 0.5 ypos 0.1
            text title
        
        # Only display evidence once processed (collected)
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


# Camera Screen
screen camera_screen():
    # Camera icon (always show)
    hbox:
        xpos 0.015 yalign 0.38
        imagebutton:
            idle "camera_idle" at Transform(zoom=0.45)
            hover "camera_hover"

            hovered Notify("Camera")
            unhovered Notify('')

            action [ToggleVariable('camera_photo_show'), SetVariable('case_file_evidence_show', False)]
    # Camera contents
    showif camera_photo_show:
        default title = 'Photos Taken'
        hbox:
            xalign 0.1 yalign 0.3
            image "casefile_bg"
        hbox:
            xalign 0.5 ypos 0.1
            text title
        # Photos of collected evidence will display in gallery 
        # (show one at a time and press arrow to change -- same as Nina Level 1 prototype)
        hbox:   # Left arrow
                xpos 0.8 ypos 0.4
                imagebutton:
                    idle 'casefile_photos_next' at Transform(zoom=0.3)
                    hover 'casefile_photos_next_hover'

                    action [Function(photo_switch, 'next')]
        hbox:   # Right arrow
            xpos 0.17 ypos 0.4
            imagebutton:
                idle 'casefile_photos_prev'at Transform(zoom=0.3)
                hover 'casefile_photos_prev_hover'
                
                action [Function(photo_switch, 'prev')]
        
        # When there are photos, display one at counter index
        if len(evidence_photos) != 0:
            hbox:
                xalign 0.5 yalign 0.4
                image evidence_photos[evidence_photos_counter] at Transform(zoom=0.55)
        # Display when no photos taken yet
        else:
            hbox:
                xalign 0.5 ypos 0.42
                text "no photos taken yet"
