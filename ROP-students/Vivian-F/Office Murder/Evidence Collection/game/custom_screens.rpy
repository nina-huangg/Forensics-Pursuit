"""
Note: for all scenarios to return back to no-tool and default cursor,
    function set_tool is called on last supposedly effective tool to toggle availability
    straight up calling set_cursor bugs out and affects all cursor change.
Exception case in screen toolbox for toggling 'marker' -- comment included there
"""


# # Start/Finish
# # Putting gloves:currently commented out until found grey/non-colored hands
# screen gloves():
#     imagebutton:
#         xalign 0.5
#         yalign 0.5
#         idle "gloves_box_idle"
#         hover "gloves_box_hover"
#         action Jump("gloves2")

# Main Screen
screen scene_office():
    default missing = False
    default curr_num = ''
    image "office_bg"   # default background

    # All imagemaps should show when casefile and camera are both not open
    # This avoid hoverin or clicking changes happen when looking throuh file/camera
    
    showif not case_file_show and not camera_photo_show:
        # Before markers are set, tool can be marker, allow hotspot to place
        if tools['marker']:
            # Store current marker number (check if bigger numbers already taken for an evidence)
            if num_deskfoot == 'numthree' or num_blood == 'numthree' or num_bullet == 'numthree' or num_cheque == 'numthree':
                $ curr_num = 'numfour'
            elif num_deskfoot == 'numtwo' or num_blood == 'numtwo' or num_bullet == 'numtwo' or num_cheque == 'numtwo':
                $ curr_num = 'numthree'
            elif num_deskfoot == 'numone' or num_blood == 'numone' or num_bullet == 'numone' or num_cheque == 'numone':
                $ curr_num = 'numtwo'
            else:
                $ curr_num = 'numone'
            
            imagemap:
                idle "office_bg"
                hover "office_bg_hover"
                # When marker not already placed for an evidence, create hotspot to add marker and set number
                if evidence_marker_set['deskfoot'] == False:
                    hotspot(10,520,450,430) action [SetDict(evidence_marker_set,'deskfoot', True), SetVariable('num_deskfoot', curr_num)] sensitive tools['marker']
                if evidence_marker_set['blood'] == False:
                    hotspot(590,280,490,320) action [SetDict(evidence_marker_set,'blood', True), SetVariable('num_blood', curr_num)] sensitive tools['marker']
                if evidence_marker_set['bullet'] == False:
                    hotspot(580,830,240,190) action [SetDict(evidence_marker_set,'bullet', True), SetVariable('num_bullet', curr_num)] sensitive tools['marker']
                if evidence_marker_set['cheque'] == False:
                    hotspot(1450,650,380,300) action [SetDict(evidence_marker_set,'cheque', True), SetVariable('num_cheque', curr_num)] sensitive tools['marker']
            
            showif all(evidence_marker_set[evidence] for evidence in evidence_marker_set):
                hbox:
                    xpos 0.35 ypos 0.1        
                    text "Unselect the marker tool to proceed\nafter placing all markers"

        # When tool not marker but markers not all placed
        # Show magnify hovering but clicking has no actions so markers are forced
        elif not all(evidence_marker_set[evidence] for evidence in evidence_marker_set):
            imagemap:
                idle "office_bg"
                hover "office_bg_hover"

                hotspot(220,520,240,430) action [SetLocalVariable('missing', True)] mouse "exclamation"
                hotspot(590,280,490,320) action [SetLocalVariable('missing', True)] mouse "exclamation"
                hotspot(580,830,240,190) action [SetLocalVariable('missing', True)] mouse "exclamation"
                hotspot(1450,650,380,300) action [SetLocalVariable('missing', True)] mouse "exclamation"
            # Show hint if trying to proceed (clicking into the evidence locations (exclamation marks)
            showif missing:
                hbox:
                    xpos 0.35 ypos 0.1        
                    text "You have not yet marked all evidence \nlocations! Do so before analyzing them"
                $ missing = False
        
        # When all markers placed, hover with magnify and clicking jumps to detail scene
        else:
            imagemap:
                idle "office_bg"
                hover "office_bg_hover"

                hotspot(220,520,240,430) action [Jump("show_deskfoot")] mouse "magnify"
                hotspot(590,280,490,320) action [Jump("show_blood")] mouse "magnify"
                hotspot(580,830,240,190) action [Jump("show_bullet")] mouse "magnify"
                hotspot(1450,650,380,300) action [Jump("show_cheque")] mouse "magnify"
        
    # Place images of post-evidence collection (evidence not in place)
    # Note: office_deskfoot/blood has pixel overlap, blood must appear after
    if 'deskfoot' in processed: 
        hbox:
            pos(0, 0)
            image "office_deskfoot"
    if 'blood' in processed: 
        hbox:
            pos(533, 251)
            image "office_blood" at Transform(zoom=0.395)
    if 'bullet' in processed: 
        hbox:
            pos(519, 911)
            image "office_bullet"
    if 'cheque' in processed: 
        hbox:
            pos(1303, 0)
            image "office_cheque"

    # Place evidence markers and numbers on top of all previous images layers
    if evidence_marker_set['deskfoot']:
        hbox:
            pos(260, 350)
            image "marker_blank" at Transform(zoom=0.9)
        hbox:
            pos(275, 370)
            image '[num_deskfoot]' at Transform(zoom=0.6)
    if evidence_marker_set['blood']:
        hbox:
            pos(1070, 360)
            image "marker_blank" at Transform(zoom=0.7)
        hbox:
            pos(1083, 371)
            image '[num_blood]' at Transform(zoom=0.5)
    if evidence_marker_set['bullet']:
        hbox:
            pos(790, 840)
            image "marker_blank" at Transform(zoom=0.7)
        hbox:
            pos(803, 855)
            image '[num_bullet]' at Transform(zoom=0.5)
    if evidence_marker_set['cheque']:
        hbox:
            pos(1775, 815)
            image "marker_blank" at Transform(zoom=0.7)
        hbox:
            pos(1786, 831)
            image '[num_cheque]' at Transform(zoom=0.5)
        
    # # When all evidence collected and prompt to proceed to lab
    if all(evidence in processed for evidence in should_be_examined):
        hbox:
            xpos 0.2 ypos 0.6
            textbutton('All 4 pieces of evidence have been collected, click to proceed to lab'):
                style "custom_button"
                action [Jump("end")]


# Post evidence bag 
# Back to main screen, hide current and collapse pop screens, 
# add photo and evidence image to camera and evidence bin (casefile),
# jump back to office scene and restart cursor
screen screen_finished_processing(evidence):
    hbox:
        xpos 0.2 ypos 0.85
        textbutton('Add to evidence bin'):
            style "custom_button"
            action [SetVariable('on_main_screen', True), 
            Hide('screen_finished_processing', _layer='over_screens'),
            Hide('case_files_screen', _layer='over_screens'), 
            Hide('camera_screen', _layer='over_camera'), 
            Hide('toolbox_screen', _layer='over_screens'),
            Function(finished_process, evidence), 
            Jump('office_start'), Function(set_cursor, '')]
        # do not change order to these!



# Evidence Collection
# Waxy footprint on desk: magnetic powder (mistake) - dust (mistake) - mix cast (mistake) 
#                           - cast (mitake) - lift - tag - photo - bag
screen scene_deskfoot():
    # Define local variables to track stage of processing -- here only dusting
    default wrong_dusted = False
    default under_dusted = False
    default proceeded_under = False
    default good_dusted = False
    default over_dusted = False
    default no_dust = False

    # Start processed if not done: first magnetic powder (2 choice)
    if 'deskfoot' not in processed:  
        imagemap:
            idle "deskfoot_zoom"
            hotspot(130,100,1230,880) action [SetLocalVariable('under_dusted', True)] sensitive tools['magnetic_black']
            hotspot(130,100,1230,880) action [SetLocalVariable('wrong_dusted', True), Function(set_cursor, '')] sensitive tools['magnetic_white']
        # magnetic_white (mistake) sends back to above by setting variable False
        showif wrong_dusted:
            image 'deskfoot_zoom'
            hbox:
                xpos 0.2 ypos 0.8
                textbutton('Using white magnetic powder against dental stone would not show clear result!\n(click to go back)'):
                    style 'custom_button'
                    action [SetLocalVariable('wrong_dusted', False)]
        # Once powdered is not enough: good_dusted if powder more
        # proceed_under if proceed to dust or mix cast, reset tool to re-choose manetic_black
        showif under_dusted:
            imagemap:
                idle "deskfoot_dust_under"
                hotspot(130,100,1230,880) action [SetLocalVariable('good_dusted', True)] sensitive tools['magnetic_black']
                hotspot(130,100,1230,880) action [SetLocalVariable('proceeded_under', True), Function(set_tool, 'brush')] sensitive tools['brush']
                hotspot(130,100,1230,880) action [SetLocalVariable('proceeded_under', True), Function(set_tool, 'ziplock')] sensitive tools['ziplock']
        # Proceeded with once powder (mistake) and forward to good_dusted after powder once more
        showif proceeded_under:
            imagemap:
                idle 'deskfoot_dust_under'
                hbox:
                    xpos 0.2 ypos 0.83
                    text 'That was not enough powder to show clear result!\n(you need to dust more)'
                hotspot(130,100,1230,800) action [SetLocalVariable('good_dusted', True), SetLocalVariable('proceeded_under', False)] sensitive tools['magnetic_black']
        # With enough powder (twice powder or from proceeded_under)
        # More powder is over_dusted, skip dusting to mix cast is no_dust, both reset tool in prep for button press
        showif good_dusted:
            imagemap:
                idle "deskfoot_dust_good"
                hotspot(130,100,1230,880) action [SetLocalVariable('over_dusted', True), Function(set_tool, 'magnetic_black')] sensitive tools['magnetic_black']
                hotspot(130,100,1230,880) action [SetLocalVariable('no_dust', True), Function(set_tool, 'ziplock')] sensitive tools['ziplock']
                # Correctly dusting allows to proceed to mixing cast mixture
                hotspot(130,100,1230,880) action [Jump("deskfoot_dusted")] sensitive tools['brush']
        # Over/No dusting (mistake) sends back to good_dusted by False local
        showif over_dusted:
            image 'deskfoot_dust_over'
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('That is too much magnetic powder! (click to go back)'):
                    style 'custom_button'
                    action [SetLocalVariable('over_dusted', False)]
        showif no_dust:
            image 'deskfoot_dust_good'
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('You must dust off excess powder before casting it! (click to go back)'):
                    style 'custom_button'
                    action [SetLocalVariable('no_dust', False)]
    
    # If already processed, show empty desk
    else:
        image 'deskfoot_gone'

# Here after guidance on KNAAP, to be done:  mix - cast - lift - tag - photo - bag 
screen scene_deskfoot_tomix():  
    # Mixing
    default empty_ziplock = False
    default ziplock_stone = False
    default under_water = False
    default under_mix = False
    default under_add_water = False
    default good_water = False
    default good_mix = False
    default over_water = False
    default over_add_stone = False
    # Others
    default poured = False
    default onemin = False
    default hour = False
    default solid = False
    default lift = False
    default rulered = False
    default tagged = False
    default done = False
    default photo = False

    imagemap:
        idle "deskfoot_dust_clear"
        hover "deskfoot_ziplock_hover"
        hotspot(550,100,810,880) action [SetLocalVariable('empty_ziplock', True)] sensitive tools['ziplock']
    showif empty_ziplock:
        imagemap:
            idle "deskfoot_ziplock"
            hotspot(130,100,1230,880) action [SetLocalVariable('ziplock_stone', True)] sensitive tools['stone']
    showif ziplock_stone:
        imagemap:
            idle "deskfoot_stone"
            hotspot(130,100,1230,880) action [SetLocalVariable('under_water', True)] sensitive tools['water']     
    showif under_water:
        imagemap:
            idle "deskfoot_under_water"
            hotspot(130,100,1230,880) action [SetLocalVariable('good_water', True)] sensitive tools['water']     
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('Click to mix: current ratio will result in a dry mixture'):
                    style 'custom_button'
                    action [SetLocalVariable('under_mix', True)]
    showif under_mix:
        imagemap:
            idle "deskfoot_under_mix"
            hbox:
                xpos 0.15 ypos 0.84
                text 'A dry mixture is not what you want!\n(You should add more water)'
            hotspot(130,100,1230,800) action [SetLocalVariable('under_add_water', True), Function(set_tool, 'water')] sensitive tools['water']
            # Reset tool from water in prep of button press
    showif under_add_water:
        imagemap:
            idle "deskfoot_under_add_water"
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('Click to mix to a pancake batter consistency'):
                    style 'custom_button'
                    action [SetLocalVariable('good_mix', True)]
    # Mix here is good, if more water, reset tool from water to re-choose for stone
    showif good_water:
        imagemap:
            idle "deskfoot_good_water"
            hotspot(130,100,1230,880) action [SetLocalVariable('over_water', True), Function(set_tool, 'water')] sensitive tools['water']     
            hbox:
                xpos 0.25 ypos 0.85
                textbutton('Click to mix: current ratio will result in a pancake batter consistency'):
                    style 'custom_button'
                    action [SetLocalVariable('good_mix', True), Function(set_cursor, '')]
    showif over_water:
        imagemap:
            idle "deskfoot_over_water"
            hbox:
                xpos 0.2 ypos 0.84
                text 'That results in a watery mixture, that is not what you want!\n(You should add more dental stone powder)'
            hotspot(130,100,1230,800) action [SetLocalVariable('over_add_stone', True), Function(set_tool, 'stone')] sensitive tools['stone']
            # Re-set tool from stone in prep for simple button-clicking
    showif over_add_stone:
        imagemap:
            idle "deskfoot_over_add_stone"
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('Click to mix to a pancake batter consistency'):
                    style 'custom_button'
                    action [SetLocalVariable('good_mix', True), Function(set_cursor, '')]
    showif good_mix:
        imagemap:
            idle "deskfoot_good_mix"
            hbox:
                xpos 0.25 ypos 0.8
                textbutton('A pancake batter consistency is exactly what you wanted!\nClick to pour mix on footprint'):
                    style 'custom_button'
                    action [SetLocalVariable('poured', True), Function(set_cursor, '')]
    # Poured cast allow menu choice for wait time
    # 1 min is under (mistake), 3 hrs is over but not mistake
    # both jumps forward to correctly waited 30 min (solid)
    showif poured:
        image 'deskfoot_poured'
        hbox:
            xalign 0.55 ypos 0.3
            text "Wait for the cast to cure"
        hbox:
            xpos 0.25 ypos 0.4
            textbutton('1 minute'):
                style 'custom_button'
                action SetLocalVariable('onemin', True)
        hbox:
            xpos 0.25 ypos 0.5
            textbutton('30 minutes'):
                style 'custom_button'
                action SetLocalVariable('solid', True)
        hbox:
            xpos 0.25 ypos 0.6
            textbutton('3 hours'):
                style 'custom_button'
                action SetLocalVariable('hour', True)          
    showif onemin:
        image 'deskfoot_poured'
        hbox:
            xpos 0.25 ypos 0.5
            textbutton('The cast has not cured! wait longer!\n(click to jump another 30 minutes)'):
                style 'custom_button'
                action [SetLocalVariable('solid', True)]
    showif hour:
        image 'deskfoot_solid'
        hbox:
            xpos 0.25 ypos 0.5
            textbutton('It solidified already in 30 minutes... but ok\n(click to proceed)'):
                style 'custom_button'
                action SetLocalVariable('solid', True)
    showif solid:
        image 'deskfoot_solid'
        hbox:
            xpos 0.25 ypos 0.85
            textbutton('Lift the cast up and properly mark and bag it'):
                style 'custom_button'
                action SetLocalVariable('lift', True)
    showif lift:
        imagemap:
            idle "deskfoot_lift"
            hotspot(130,10,1230,970) action [SetLocalVariable('rulered', True)] sensitive tools['ruler']
            hotspot(130,10,1230,970) action [SetLocalVariable('tagged', True)] sensitive tools['tag']
    showif rulered and not tagged:
        imagemap:
            idle 'deskfoot_ruler'
            hotspot(130,10,1230,970) action [Function(set_tool, 'tag'), SetLocalVariable('tagged', True)] sensitive tools['tag']  
            # set_tool toggles to unselect tag tool before take photo button 
    showif tagged and not rulered:
        imagemap:
            idle 'deskfoot_tag_only'
            hotspot(130,10,1230,970) action [Function(set_tool, 'ruler'), SetLocalVariable('rulered', True)] sensitive tools['ruler']  
            # set_tool toggles to unselect ruler tool before take photo button 
    # Once tagged with ruler and tag, display button to take photo and send to label take_deskfoot
    showif rulered and tagged:
            image 'deskfoot_tagged'
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action [Function(add_photo, 'deskfoot'), Jump("take_deskfoot")]
        
# After photo taken (flashed), send here from label take_deskfoot
# Final step to bag, tape, and screen_finished_processing
screen scene_deskfoot_tobag():
    default bagged = False
    default taped = False
    imagemap:
        idle "deskfoot_tagged"
        hotspot(130,100,1230,880) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle "deskfoot_bagged"
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='deskfoot',_layer='over_screens')] sensitive tools['tape']
            # set_tool toggles to unselect tape tool before return to main screen 
    showif taped:
        image 'deskfoot_taped'
        

transform blood_markers(): 
    zoom 2.1
transform blood_nums(): 
    zoom 1.8

# Latnet blood on floor: Hungarian Red spray (mistake) - cut - ruler - photo - bag
screen scene_blood():
    # Define local variables to track stage of processing
    default rulered = False

    # Start processed if not done: first hungarian red dye spray
    if 'blood' not in processed:
        imagemap:
            idle "blood_zoom"
            hotspot(232,195,1035,580) action [Function(set_tool, 'ruler'), SetLocalVariable('rulered', True)] sensitive tools['ruler']
            hbox:
                xpos 0.781 ypos 0.276
                image "marker_blank" at blood_markers
            hbox:
                xpos 0.791 ypos 0.286
                image '[num_blood]' at blood_nums
        # After place ruler, take photo with evidence marker in scene -- jump to label take_blood 
        showif rulered:
            image 'blood_ruler'
            hbox:
                xpos 0.781 ypos 0.276
                image "marker_blank" at blood_markers
            hbox:
                xpos 0.791 ypos 0.286
                image '[num_blood]' at blood_nums
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action [Function(add_photo, 'blood'), Jump("take_blood")]
    # When already processed, show scene with carpet cut out -- shows flooring
    else:
        image 'blood_gone'
        hbox:
            xpos 0.781 ypos 0.276
            image "marker_blank" at blood_markers
        hbox:
            xpos 0.791 ypos 0.286
            image '[num_blood]' at blood_nums
    
screen scene_blood_tospray():
    imagemap:
        idle "blood_ruler"
        hbox:
            xpos 0.781 ypos 0.276
            image "marker_blank" at blood_markers
        hbox:
            xpos 0.791 ypos 0.286
            image '[num_blood]' at blood_nums
        hotspot(232,195,1035,580) action [Function(set_tool, 'hungarian_red'), SetLocalVariable('sprayed', True), Jump('blood_tocut')] sensitive tools['hungarian_red']

screen scene_blood_tocut():
    default cut = False
    imagemap:
        idle "blood_sprayed"
        hover "blood_cut_hover"
        hbox:
            xpos 0.781 ypos 0.276
            image "marker_blank" at blood_markers
        hbox:
            xpos 0.791 ypos 0.286
            image '[num_blood]' at blood_nums
        hotspot(232,195,1135,680) action [Function(set_tool, 'knife'), SetLocalVariable('cut', True)] sensitive tools['knife']
    showif cut:
        imagemap:
            idle "blood_cut"
            hbox:
                xpos 0.781 ypos 0.276
                image "marker_blank" at blood_markers
            hbox:
                xpos 0.791 ypos 0.286
                image '[num_blood]' at blood_nums
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action [Function(add_photo, 'blood_sprayed'), Jump("take_blood_sprayed")]

# After photo, here from label take_blood -- bag carpet, tape, and screen_finished_processing
screen scene_blood_tobag():
    default bagged = False
    default taped = False
    imagemap:
        idle "blood_cut"
        hbox:
            xpos 0.781 ypos 0.276
            image "marker_blank" at blood_markers
        hbox:
            xpos 0.791 ypos 0.286
            image '[num_blood]' at blood_nums
        hotspot(232,195,1035,580) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle 'blood_bagged'
            hbox:
                xpos 0.781 ypos 0.276
                image "marker_blank" at blood_markers
            hbox:
                xpos 0.791 ypos 0.286
                image '[num_blood]' at blood_nums
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='blood',_layer='over_screens')] sensitive tools['tape'] 
            # set_tool toggles to unselect tape tool before return to main screen 
    showif taped:
        image 'blood_taped'
        hbox:
            xpos 0.781 ypos 0.276
            image "marker_blank" at blood_markers
        hbox:
            xpos 0.791 ypos 0.286
            image '[num_blood]' at blood_nums


transform bullet_markers(): 
    zoom 4.03
transform bullet_nums(): 
    zoom 3.3

# Bullet cartridge: photo by jump to label take_bullet -- bag
screen scene_bullet():
    default rulered = False
    if 'bullet' not in processed:
        imagemap:
            idle "bullet_zoom"
            hbox:
                xpos 0.616 ypos 0.145
                image "marker_blank" at bullet_markers
            hbox:
                xpos 0.64 ypos 0.18
                image '[num_bullet]' at bullet_nums
            hotspot(300,200,700,700) action [SetLocalVariable('rulered', True), Function(set_tool, 'ruler')] sensitive tools['ruler']
        showif rulered:
            image 'bullet_ruler'
            hbox:
                xpos 0.616 ypos 0.145
                image "marker_blank" at bullet_markers
            hbox:
                xpos 0.64 ypos 0.18
                image '[num_bullet]' at bullet_nums
            hbox:
                xpos 0.2 ypos 0.85
                textbutton('Take Photo'):
                    style 'custom_button'
                    action [Function(add_photo, 'bullet'), Jump("take_bullet")]
    else:
        image 'bullet_gone' # bullet taken out of scene after processed
        hbox:
            xpos 0.616 ypos 0.145
            image "marker_blank" at bullet_markers
        hbox:
                xpos 0.64 ypos 0.18
                image '[num_bullet]' at bullet_nums

# After photo, here from label take_bullet -- bag and screen_finished_processing
screen scene_bullet_tobag():
    default bagged = False
    default taped = False
    imagemap:
        idle "bullet_ruler"
        hbox:
            xpos 0.616 ypos 0.145
            image "marker_blank" at bullet_markers
        hbox:
                xpos 0.64 ypos 0.18
                image '[num_bullet]' at bullet_nums
        hotspot(240,380,600,400) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle 'bullet_bagged'
            hbox:
                xpos 0.616 ypos 0.145
                image "marker_blank" at bullet_markers
            hbox:
                xpos 0.64 ypos 0.18
                image '[num_bullet]' at bullet_nums
            hotspot(410,190,550,710) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='bullet',_layer='over_screens')] sensitive tools['tape'] 
            # set_tool toggles to unselect tape tool before return to main screen 
    showif taped:
        image 'bullet_taped'
        hbox:
            xpos 0.616 ypos 0.145
            image "marker_blank" at bullet_markers
        hbox:
            xpos 0.64 ypos 0.18
            image '[num_bullet]' at bullet_nums


transform cheque_markers(): 
    zoom 2.9
transform cheque_nums(): 
    zoom 2.5

# Cheque: photo by jump to label take_cheque -- bag
screen scene_cheque():
    if 'cheque' not in processed:
        image 'cheque_zoom'
        hbox:
            xpos 0.75 ypos 0.45
            image "marker_blank" at cheque_markers
        hbox:
            xpos 0.762 ypos 0.47
            image '[num_cheque]' at cheque_nums
        hbox:
            xpos 0.2 ypos 0.85
            textbutton('Take Photo'):
                style 'custom_button'
                action [Function(add_photo, 'cheque'), Jump("take_cheque")]
    else:
        image 'cheque_gone'
        hbox:
            xpos 0.75 ypos 0.45
            image "marker_blank" at cheque_markers
        hbox:
            xpos 0.762 ypos 0.47
            image '[num_cheque]' at cheque_nums

# After photo, here from label take_cheque -- bag, tape, and screen_finished_processing
screen scene_cheque_tobag():
    default bagged = False
    default taped = False
    imagemap:
        idle "cheque_zoom"
        hbox:
            xpos 0.75 ypos 0.45
            image "marker_blank" at cheque_markers
        hbox:
            xpos 0.762 ypos 0.47
            image '[num_cheque]' at cheque_nums
        hotspot(540,290,860,560) action [SetLocalVariable('bagged', True)] sensitive tools['bag']
    showif bagged:
        imagemap:
            idle 'cheque_bagged'
            hbox:
                xpos 0.75 ypos 0.45
                image "marker_blank" at cheque_markers
            hbox:
                xpos 0.762 ypos 0.47
                image '[num_cheque]' at cheque_nums
            hotspot(710,210,510,680) action [SetLocalVariable('taped', True), Function(set_tool, 'tape'),
                Show('screen_finished_processing', evidence='cheque',_layer='over_screens')] sensitive tools['tape'] 
            # set_tool toggles to unselect tape tool before return to main screen 
    showif taped:
        image 'cheque_taped'
        hbox:
            xpos 0.75 ypos 0.45
            image "marker_blank" at cheque_markers
        hbox:
            xpos 0.762 ypos 0.47
            image '[num_cheque]' at cheque_nums


# Casefile Evidences
transform casefile_small():
    zoom 0.2

screen case_files_screen():
    # Contents
    showif case_file_show:
        default title = 'Evidence Collected'
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.46 ypos 0.2
            text title
        hbox:
            xpos 0.25 ypos 0.2
            textbutton('Close'):
                style "back_button" 
                action [SetVariable('case_file_show', False)]
        
        
        if all(evidence not in processed for evidence in should_be_examined):
            hbox:
                xpos 0.44 ypos 0.5
                text "no evidence collected yet"
        
        # Only display evidence once processed (collected)
        showif 'deskfoot' in processed:
            hbox:
                xpos 0.3 ypos 0.62
                image 'casefile_deskfoot' at casefile_small
        showif 'blood' in processed:
            hbox:
                xpos 0.6 ypos 0.34
                image 'casefile_blood' at casefile_small
        showif 'bullet' in processed:
            hbox:
                xpos 0.3 ypos 0.34
                image 'casefile_bullet' at casefile_small
        showif 'cheque' in processed:
            hbox:
                xpos 0.6 ypos 0.62
                image 'casefile_cheque' at casefile_small
        
        

# Camera Screen
transform camera_photo():
    zoom 0.52

screen camera_screen():
    # Camera contents
    showif camera_photo_show:
        default title = 'Photos Taken'
        hbox:
            xpos 0.05 ypos 0.08
            image "casefile_inventory"
        hbox:
            xpos 0.49 ypos 0.2
            text title
        hbox:
            xpos 0.25 ypos 0.2
            textbutton('Close'):
                style "back_button" 
                action [SetVariable('camera_photo_show', False)]
        # Photos of collected evidence will display in gallery 
        # (show one at a time and press arrow to change -- same as Nina Level 1 prototype)
        hbox:   # Left arrow
            xpos 0.22 ypos 0.47         
            imagebutton:
                idle 'inventory-arrow-left-enabled-idle' at Transform(zoom=0.7)
                hover If(photo_counter - 1 > 0, true= 'inventory-arrow-left-enabled-hover')

                action [Function(photo_switch, 'next')]
        hbox:   # Right arrow
            xpos 0.82 ypos 0.47
            imagebutton:
                idle 'inventory-arrow-right-enabled-idle' at Transform(zoom=0.7)
                hover If(photo_counter + 1 < len(photoed), true= 'inventory-arrow-right-enabled-hover')
                
                action [Function(photo_switch, 'prev')]
        
        # When there are photos, display one at counter index 
        # account for image name by storing in photo_name
        # Must code for hbox under each if, muliple if then hbox only shows one
        if len(photoed) != 0:
            default photo_name = ''
            if photoed[photo_counter] == 'deskfoot':
                $ photo_name = 'camera_deskfoot'
                hbox:
                    xalign 0.6 yalign 0.57
                    image '[photo_name]' at camera_photo
            if photoed[photo_counter] == 'blood':
                $ photo_name = 'blood_' + num_blood
                hbox:
                    xalign 0.6 yalign 0.57
                    image '[photo_name]' at camera_photo
            if photoed[photo_counter] == 'blood_sprayed':
                $ photo_name = 'blood_sprayed_' + num_blood
                hbox:
                    xalign 0.6 yalign 0.57
                    image '[photo_name]' at camera_photo
            if photoed[photo_counter] == 'bullet':
                $ photo_name = 'bullet_' + num_bullet
                hbox:
                    xalign 0.6 yalign 0.57
                    image '[photo_name]' at camera_photo
            if photoed[photo_counter] == 'cheque':
                $ photo_name = 'cheque_' + num_cheque
                hbox:
                    xalign 0.6 yalign 0.57
                    image '[photo_name]' at camera_photo
        # Display when no photos taken yet
        else:
            hbox:
                xpos 0.46 ypos 0.5
                text "no photos taken yet"



# Back Button (only used for returning to main screen for now in script)
screen back_button_screen(location, curr_screen):
    hbox:
        xpos 0.93 ypos 0.88
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Function(set_cursor, ''),
                    Hide('screen_finished_processing', _layer='over_screens'), 
                    SetVariable('on_main_screen', True), Jump(location), Hide(curr_screen)]
