# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define o = Character(_("Officer Meow"))

# The game starts here.

label start:
    scene officer_meow
    play audio "meow.mp3" volume 0.5
    o "Good meowning student. You know who I am, let's get started."
    default curr_screen = "car_f"
    default evidence_collected = 1
    default scenes_visited = False
    default inside_visited = False
    default garage_pic_collected = False
    default coldprint_collected = False
    default fingerprint_collected = False
    default glass_collected = False
    default coldprint_correct_order = True
    default fingerprint_correct_order = True
    default glass_correct_order = True
    default invalid_print = False
    default powder_colour = "white"
    jump map_scene

label map_scene:
    scene map_bg_full
    if scenes_visited == False:
        o "Any time you see text at the bottom of the screen like this, it signifies a dialogue box. Press SPACE whenever you see it to continue forwards!"
        o "Here is a map of the crime scene. You can click on the elements to visit a single scene. There are 3 in total."
        o "Be careful where you click, because the order you visit the scenes in will influence your outcome!"
        o "Alright, where would you like to check first?"
        $ scenes_visited = True
    else:
        o "Where do you want to check next?"
    scene map_bg
    call screen display_map

screen display_map:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.5
        idle "garage.png"
        hover "garage_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("garage")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.53
        ypos 0.52
        idle "car_exterior.png"
        hover "car_exterior_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("car_f")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.53
        ypos 0.52
        idle "car_interior.png"
        hover "car_interior_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("inside")]

label box_scene:
    show evidence_box:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
    show box_inside
    call screen inner_box

screen inner_box:
    if garage_pic_collected:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.29
            ypos 0.45
            idle "box_photo.png"
            hover "box_photo_hover.png"
            action Play("sound", "map_location_click.mp3")
    if coldprint_collected:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.47
            ypos 0.45
            idle "box_cp.png"
            hover "box_cp_hover.png"
            action Play("sound", "map_location_click.mp3")
    if fingerprint_collected:
        if powder_colour == "white":
            imagebutton:
                xanchor 0.5
                yanchor 0.5
                xpos 0.67
                ypos 0.46
                idle "box_bcard.png"
                hover "box_bcard_hover.png"
                action Play("sound", "map_location_click.mp3")
        elif powder_colour == "black":
            imagebutton:
                xanchor 0.5
                yanchor 0.5
                xpos 0.67
                ypos 0.46
                idle "box_wcard.png"
                hover "box_wcard_hover.png"
                action Play("sound", "map_location_click.mp3")
    if glass_collected:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.47
            ypos 0.58
            idle "box_lowerbag.png"
            hover "box_glass_hover.png"
            action Play("sound", "map_location_click.mp3")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.79
        ypos 0.235
        idle "x.png"
        hover "x_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("x_button")]

label x_button:
    hide evidence_box
    hide box_inside
    if curr_screen == "garage_scene":
        jump garage_scene_cont
    elif curr_screen == "car_f":
        jump car_f
    elif curr_screen == "car_r":
        jump car_r
    elif curr_screen == "inside":
        jump inside
    elif curr_screen == "car_b":
        jump car_b
    elif curr_screen == "car_l":
        jump car_l

label garage:
    scene garage_scene
    $ curr_screen = "garage_scene"
    if garage_pic_collected == False:
        "Hmm, are those tool marks on that garage? Better grab a picture of that."
    else:
        "Looks like we're done with this area."
label garage_scene_cont:
    call screen toolmarks

screen toolmarks:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
        idle "evidence_box.png"
        hover "evidence_box_hover.png"
        action [Play("sound", "cardboard_box.mp3"), Jump("box_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.35
        idle "map_icon.png"
        hover "map_icon_hover.png"
        action [Play("sound", "map_furl.mp3"), Jump("map_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.85
        ypos 0.85
        idle "camera.png"
        hover "camera_hover.png"
        action Jump("take_picture_garage")

label take_picture_garage:
    if garage_pic_collected == False:
        $ garage_pic_collected = True
        $ flash = Fade(.25, 0, .75, color="#fff")
        play sound "camera.mp3"
        scene garage_picture
        with flash
        $ evidence_collected = evidence_collected + 1
        "Evidence collected."
        if evidence_collected == 5:
            jump end
    else:
        play sound "map_location_click.mp3"
        "Looks like we're done with this area."
    call screen toolmarks

label car_f:
    scene bg car_front
    $ curr_screen = "car_f"
    call screen car_f_options

screen car_f_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
        idle "evidence_box.png"
        hover "evidence_box_hover.png"
        action [Play("sound", "cardboard_box.mp3"), Jump("box_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.35
        idle "map_icon.png"
        hover "map_icon_hover.png"
        action [Play("sound", "map_furl.mp3"), Jump("map_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_l")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_r")]

label car_r:
    $ curr_screen = "car_r"
    if inside_visited == False:
        scene bg car_right
    else:
        scene bg car_rightb
        "Hey, my footprints got mixed with the suspect's by accident..."
    call screen car_r_options

screen car_r_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
        idle "evidence_box.png"
        hover "evidence_box_hover.png"
        action [Play("sound", "cardboard_box.mp3"), Jump("box_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.35
        idle "map_icon.png"
        hover "map_icon_hover.png"
        action [Play("sound", "map_furl.mp3"), Jump("map_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_f")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_b")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.4
        ypos 0.445
        idle "car_hover_hide.png"
        hover "car_hover_show.png"
        action [Play("sound", "evidence_click.mp3"), Jump("door_handle")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.19
        ypos 0.82
        idle "fp_right_hover_hide.png"
        hover "fp_right_hover_show.png"
        action [Play("sound", "evidence_click.mp3"), Jump("cold_print")]

label door_handle:
    scene fingerprint1
    if fingerprint_collected == False:
        "Let's check the door handle for evidence."
        default checked_mag_glass = False
        default marked_h = False
        default powdered_fp = False
        default scaled = False
        default taped_h = False
        default carded_h = False
        show toolbox:
            xpos 0.0
            ypos 0.02
    else:
        "I think we have all we need from this area."
        jump car_r
    call screen handle_examine

screen handle_examine:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.38
        idle "evidence_markers.png"
        hover "evidence_markers_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_mark_h")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.6
        idle "card.png"
        hover "card_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_card")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.15
        idle "mag_glass.png"
        hover "mag_glass_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_mag_glass")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.35
        idle "backing_tape.png"
        hover "backing_tape_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_backing_tape")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.58
        idle "fingerprint_powder.png"
        hover "fingerprint_powder_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_powder_h")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.81
        idle "scalebar.png"
        hover "scale_bar_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_scale_bar")]

label toggle_mag_glass:
    if checked_mag_glass == True:
        "Hmm, seems like you already did this part."
        $ fingerprint_correct_order = False
    else:
        $ checked_mag_glass = True
        scene fingerprint2
        show toolbox:
            xpos 0.0
            ypos 0.02
        "A fingerprint!"
        scene fingerprint1
        show toolbox:
            xpos 0.0
            ypos 0.02
    call screen handle_examine

label toggle_mark_h:
    if marked_h == True:
        "Hmm, seems like you already did this part."
    elif checked_mag_glass == False:
        "This doesn't seem like the correct order."
        $ fingerprint_correct_order = False
    else:
        $ marked_h = True
        scene fingerprint3
        show toolbox:
            xpos 0.0
            ypos 0.02
    call screen handle_examine

label toggle_powder_h:
    if powdered_fp == True:
        "Hmm, seems like you already did this part."
    elif marked_h == False:
        "This doesn't seem like the correct order."
        $ fingerprint_correct_order = False
    else:
        $ powdered_fp = True
        "Which colour powder should I use?"
        jump powder_choose
    call screen handle_examine

label powder_choose:
menu:
    "White":
        jump powder_white
    "Black":
        $ powder_colour = "black"
        jump powder_black

label powder_white:
    play sound "fp_powder.mp3"
    scene fingerprint4
    show toolbox:
        xpos 0.0
        ypos 0.02
    call screen handle_examine

label powder_black:
    play sound "fp_powder.mp3"
    show toolbox:
        xpos 0.0
        ypos 0.02
    call screen handle_examine

label toggle_scale_bar:
    if scaled == True:
        "Hmm, seems like you already did this part."
        $ fingerprint_correct_order = False
    elif powdered_fp == False:
        "This doesn't seem like the correct order."
        $ fingerprint_correct_order = False
    else:
        $ scaled = True
        if powder_colour == "white":
            scene fingerprint5
        else:
            scene fingerprint5b
        show toolbox:
            xpos 0.0
            ypos 0.02
    call screen handle_examine

label toggle_backing_tape:
    if taped_h == True:
        "Hmm, seems like you already did this part."
        $ fingerprint_correct_order = False
    elif scaled == False:
        "This doesn't seem like the correct order."
        $ fingerprint_correct_order = False
    else:
        $ taped_h = True
        if powder_colour == "white":
            scene fingerprint6
        else:
            scene fingerprint6b
        show toolbox:
            xpos 0.0
            ypos 0.02
    call screen handle_examine

label toggle_card:
    if carded_h == True:
        "Hmm, seems like you already did this part."
        $ fingerprint_correct_order = False
    elif taped_h == False:
        "This doesn't seem like the correct order."
        $ fingerprint_correct_order = False
    else:
        $ carded_h = True
        $ fingerprint_collected = True
        if powder_colour == "white":
            scene fingerprint7
        else:
            scene fingerprint7b
        show toolbox:
            xpos 0.0
            ypos 0.02
        if powder_colour == "white":
            play sound "success.mp3" volume 0.2
            "Good work, evidence collected."
        else:
            "Looks like that fingerprint got cut off..."
        $ evidence_collected = evidence_collected + 1
        if evidence_collected == 5:
            jump end
        jump car_r
    call screen handle_examine

label cold_print:
    scene footprint0
    if coldprint_collected == False:
        "You found a footprint in the snow!"
        default marked_cp = False
        default powdered_cp = False
        default bucketed_cp = False
        default news_cp = False
        default snowed_cp = False
        default bagged_cp = False
        default labeled_cp = False
        default snowtime = False
        show toolbox:
            xpos 0.0
            ypos 0.02
        if inside_visited == True:
            $ invalid_print = True
    else:
        "I think we already have everything we need from this area."
        jump car_r
    call screen cold_print_collection

screen cold_print_collection:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.34
        idle "evidence_markers.png"
        hover "evidence_markers_hover.png"
        action Jump("toggle_mark_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.6
        idle "bags.png"
        hover "bags_hover.png"
        action Jump("toggle_bag_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.8
        idle "evidence_tape.png"
        hover "evidence_tape_hover.png"
        action Jump("toggle_tape_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.15
        idle "powder.png"
        hover "powder_hover.png"
        action Jump("toggle_powder_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.38
        idle "bucket.png"
        hover "bucket_hover.png"
        action Jump("toggle_bucket_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.65
        idle "newspaper.png"
        hover "newspaper_hover.png"
        action Jump("toggle_news_cp")

label toggle_mark_cp:
    if marked_cp == False:
        play sound "coldprint.mp3"
        scene footprint1
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ marked_cp = True
    else:
        play sound "map_location_click.mp3"
        "Hmm, seems like you already did this part."
        $ coldprint_correct_order = False
    if snowtime == False:
        call screen cold_print_collection
    else:
        call screen snow_cp

label toggle_powder_cp:
    if marked_cp == True and powdered_cp == False:
        play sound "powder.mp3"
        scene footprint2
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ powdered_cp = True
    elif marked_cp == False:
        play sound "map_location_click.mp3"
        "This doesn't seem like the correct order."
        $ coldprint_correct_order = False
    else:
        play sound "map_location_click.mp3"
        "Hmm, seems like you already did this part."
        $ coldprint_correct_order = False
    if snowtime == False:
        call screen cold_print_collection
    else:
        call screen snow_cp

label toggle_bucket_cp:
    if powdered_cp == True and bucketed_cp == False:
        scene footprint3
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ bucketed_cp = True
        play sound "mixing.mp3" volume 2
        "Mixing for 60 seconds..."
        scene footprint4
        show toolbox:
            xpos 0.0
            ypos 0.02
        stop sound
        play sound "pouring.mp3"
        "Pouring mixture..."
        stop sound
        scene footprint5
        show toolbox:
            xpos 0.0
            ypos 0.02
    elif powdered_cp == False:
        play sound "map_location_click.mp3"
        "This doesn't seem like the correct order."
        $ coldprint_correct_order = False
    else:
        play sound "map_location_click.mp3"
        "Hmm, seems like you already did this part."
        $ coldprint_correct_order = False
    if snowtime == False:
        call screen cold_print_collection
    else:
        call screen snow_cp

label toggle_news_cp:
    if bucketed_cp == True and news_cp == False:
        play sound "coldprint.mp3"
        scene footprint6
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ news_cp = True
        $ snowtime = True
    elif bucketed_cp == False:
        play sound "map_location_click.mp3"
        "This doesn't seem like the correct order."
        $ coldprint_correct_order = False
    else:
        play sound "map_location_click.mp3"
        "Hmm, seems like you already did this part."
        $ coldprint_correct_order = False
    if snowtime == False:
        call screen cold_print_collection
    else:
        call screen snow_cp

screen snow_cp:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.34
        idle "evidence_markers.png"
        hover "evidence_markers_hover.png"
        action Jump("toggle_mark_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.6
        idle "bags.png"
        hover "bags_hover.png"
        action Jump("toggle_bag_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.8
        idle "evidence_tape.png"
        hover "evidence_tape_hover.png"
        action Jump("toggle_tape_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.15
        idle "powder.png"
        hover "powder_hover.png"
        action Jump("toggle_powder_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.38
        idle "bucket.png"
        hover "bucket_hover.png"
        action Jump("toggle_bucket_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.65
        idle "newspaper.png"
        hover "newspaper_hover.png"
        action Jump("toggle_news_cp")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.48
        ypos 0.5
        idle "footprint_6.png"
        hover "footprint_6_hover.png"
        action Jump("toggle_snow_cp")

label toggle_snow_cp:
    scene footprint7
    show toolbox:
        xpos 0.0
        ypos 0.02
    $ snowed_cp = True
    play sound "coldprint.mp3"
    "Waiting 10 mins for footprint to harden..."
    hide screen snow_cp
    $ snowtime = False
    scene footprint8
    play sound "coldprint.mp3"
    show toolbox:
        xpos 0.0
        ypos 0.02
    "Awesome! I should bag and collect that."
    show arrow_left_hover:
        xpos 0.12
        ypos 0.55
    call screen cold_print_collection

label toggle_bag_cp:
    play sound "map_location_click.mp3"
    if snowed_cp == True and bagged_cp == False:
        scene footprint91
        show toolbox:
            xpos 0.0
            ypos 0.02
        show print_bag:
            xpos 0.4
            ypos 0.25
        $ bagged_cp = True
    elif snowed_cp == False:
        "This doesn't seem like the correct order."
        $ coldprint_correct_order = False
    else:
        "Hmm, seems like you already did this part."
        $ coldprint_correct_order = False
    if snowtime == False:
        call screen cold_print_collection
    else:
        call screen snow_cp

label toggle_tape_cp:
    play sound "map_location_click.mp3"
    if bagged_cp == True and labeled_cp == False:
        show print_bagseal:
            xpos 0.4
            ypos 0.25
        $ labeled_cp = True
        $ coldprint_collected = True
        play sound "success.mp3" volume 0.2
        "Evidence collected, good work."
        $ evidence_collected = evidence_collected + 1
        if evidence_collected == 5:
            jump end
        jump car_r
    else:
        "This doesn't seem like the correct order."
        $ coldprint_correct_order = False
        if snowtime == False:
            call screen cold_print_collection
        else:
            call screen snow_cp

label inside:
    $ curr_screen = "inside"
    scene bg car_inside
    $ inside_visited = True
    call screen pre_glass

screen pre_glass:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
        idle "evidence_box.png"
        hover "evidence_box_hover.png"
        action [Play("sound", "cardboard_box.mp3"), Jump("box_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.35
        idle "map_icon.png"
        hover "map_icon_hover.png"
        action [Play("sound", "map_furl.mp3"), Jump("map_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.56
        ypos 0.92
        idle "glass_hover_hide.png"
        hover "glass_hover_show.png"
        action [Play("sound", "evidence_click.mp3"), Jump("found_glass")]

label found_glass:
    scene glass0
    if glass_collected == False:
        "You found some glass shards."
        default marked_g = False
        default papered_g = False
        default tweezered_g = False
        default wrapped_g = False
        default bagged_g = False
        default labeled_g = False
        show toolbox:
            xpos 0.0
            ypos 0.02
    else:
        "Looks like we already have everything we need from this area."
        jump inside
    call screen glass_collection

screen glass_collection:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.38
        idle "evidence_markers.png"
        hover "evidence_markers_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_mark_g")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.6
        idle "bags.png"
        hover "bags_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_bag_g")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.8
        idle "evidence_tape.png"
        hover "evidence_tape_hover.png"
        action [Play("sound", "map_location_click.mp3"), Jump("toggle_tape_g")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.15
        idle "tweezers.png"
        hover "tweezers_hover.png"
        action Jump("toggle_tweezers")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.38
        idle "paper.png"
        hover "paper_hover.png"
        action Jump("toggle_paper")

label toggle_mark_g:
    if marked_g == False:
        scene glass0_1
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ marked_g = True
    else:
        "Hmm, seems like you already did this part."
        $ glass_correct_order = False
    call screen glass_collection

label toggle_paper:
    if marked_g == True and papered_g == False:
        play sound "paper_place.mp3"
        scene glass1
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ papered_g = True
    elif marked_g == False:
        play sound "map_location_click.mp3"
        "This doesn't seem like the correct order."
        $ glass_correct_order = False
    else:
        play sound "map_location_click.mp3"
        "Hmm, seems like you already did this part."
        $ glass_correct_order = False
    call screen glass_collection

label toggle_tweezers:
    if papered_g == True and tweezered_g == False:
        play sound "glass.mp3" volume 3
        scene glass2
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ tweezered_g = True
        "Wrapping bundle..."
        play sound "paper_fold.mp3"
        scene glass3
        show toolbox:
            xpos 0.0
            ypos 0.02
    elif papered_g == False:
        play sound "map_location_click.mp3"
        "This doesn't seem like the correct order."
        $ glass_correct_order = False
    else:
        play sound "map_location_click.mp3"
        "Hmm, seems like you already did this part."
        $ glass_correct_order = False
    call screen glass_collection

label toggle_bag_g:
    if tweezered_g == True and bagged_g == False:
        scene glass4
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ bagged_g = True
    elif tweezered_g == False:
        "This doesn't seem like the correct order."
        $ glass_correct_order = False
    else:
        "Hmm, seems like you already did this part."
        $ glass_correct_order = False
    call screen glass_collection

label toggle_tape_g:
    if bagged_g == True and labeled_g == False:
        scene glass5
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ labeled_g = True
        $ glass_collected = True
        play sound "success.mp3" volume 0.2
        "Evidence collected. Great work!"
        $ evidence_collected = evidence_collected + 1
        if evidence_collected == 5:
            jump end
        jump inside
    elif bagged_g == False:
        "This doesn't seem like the correct order."
        $ glass_correct_order = False
        call screen glass_collection
    else:
        "Hmm, seems like you already did this part."
        $ glass_correct_order = False
        call screen glass_collection

label car_b:
    $ curr_screen = "car_b"
    scene bg car_back
    call screen car_b_options

screen car_b_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
        idle "evidence_box.png"
        hover "evidence_box_hover.png"
        action [Play("sound", "cardboard_box.mp3"), Jump("box_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.35
        idle "map_icon.png"
        hover "map_icon_hover.png"
        action [Play("sound", "map_furl.mp3"), Jump("map_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_r")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_l")]

label car_l:
    $ curr_screen = "car_l"
    scene bg car_left
    call screen car_l_options

screen car_l_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.15
        idle "evidence_box.png"
        hover "evidence_box_hover.png"
        action [Play("sound", "cardboard_box.mp3"), Jump("box_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.35
        idle "map_icon.png"
        hover "map_icon_hover.png"
        action [Play("sound", "map_furl.mp3"), Jump("map_scene")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_b")]
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action [Play("sound", "arrow_click.mp3"), Jump("car_f")]

label end:
    # This ends the game.
    scene report_card
    $ coldprint_score = 5
    $ fingerprint_score = 5
    $ glass_score = 5
    "All 5 pieces of evidence collected."
    "Final report:"
    "Toolmark collection 1/1 - well done"
    show checkmark:
        xpos 0.49
        ypos 0.318
        xanchor 0.5
        yanchor 0.5
    
    if invalid_print == True:
        $ coldprint_score = 0
        "Snowprint collection 0/5 - you contaminated the evidence by checking the inside first! Make sure to always work from outside-in."
    elif coldprint_correct_order == True:
        "Snowprint collection 5/5 - well done"
        show checkmark2:
            xpos 0.54
            ypos 0.378
            xanchor 0.5
            yanchor 0.5
        show checkmark3:
            xpos 0.54
            ypos 0.418
            xanchor 0.5
            yanchor 0.5
    else:
        "Snowprint collection 4/5 - order of collection should be: mark, powder, plaster, newspaper, snow, bag, seal"
        $ coldprint_score -= 1
        show checkmark2:
            xpos 0.54
            ypos 0.36
            xanchor 0.5
            yanchor 0.5
    
    if powder_colour == "black":
        $ fingerprint_score -= 3
    if fingerprint_correct_order == False:
        $ fingerprint_score -= 1
    $ string_fp_score = "%d" % fingerprint_score
    "Fingerprint collection [string_fp_score]/5"
    if powder_colour == "black":
        "(Fingerprint cont.) Used incorrectly coloured powder. Make sure to use white powder for black cars."
    else:   
        "(Fingerprint cont.) Well done on choosing white powder to use on a black car!"
        show checkmark4:
            xpos 0.54
            ypos 0.535
            xanchor 0.5
            yanchor 0.5
    if fingerprint_correct_order == False:
        "(Fingerprint cont.) Order of collection should be magnifying glass, mark, powder, scalebar, tape, card"
    else:
        "(Fingerprint cont.) Correct order of collection!"
        show checkmark5:
            xpos 0.54
            ypos 0.58
            xanchor 0.5
            yanchor 0.5
    
    if glass_correct_order == True:
        "Glass collection 5/5 - well done"
        show checkmark6:
            xpos 0.54
            ypos 0.63
            xanchor 0.5
            yanchor 0.5
    else:
        "Glass collection 4/5 - order of collection should be: mark, paper, tweezers, bag, seal"
        $ glass_score -= 1

    $ final_score = 1 + coldprint_score + fingerprint_score + glass_score
    $ string_final_score = "%d" % final_score
    show grade_a:
        xpos 0.68
        ypos 0.68
        xanchor 0.5
        yanchor 0.5
    "Final score: [string_final_score]/16"
    scene entering_lab_screen
    return
