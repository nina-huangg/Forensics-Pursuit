# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define o = Character(_("Officer Meow"))


# The game starts here.

label start:
    scene officer_meow
    o "Good meowning student. You know who I am, let's get started."
    scene steal1
    pause
    scene steal2
    pause
    scene steal3
    pause
    scene steal4
    pause
    scene steal5
    pause
    scene steal6
    pause
    scene steal7
    pause
    jump car_f_initial

label car_f_initial:
    scene bg car_front with dissolve
    jump car_f

label car_f:
    scene bg car_front
    call screen car_f_options

screen car_f_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action Jump("car_l")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action Jump("car_r")

label car_r:
    scene bg car_right
    call screen car_r_options

screen car_r_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action Jump("car_f")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action Jump("car_b")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.4
        ypos 0.445
        idle "car_hover_hide.png"
        hover "car_hover_show.png"
        action Jump("inside")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.19
        ypos 0.82
        idle "fp_right_hover_hide.png"
        hover "fp_right_hover_show.png"
        action Jump("cold_print")

label cold_print:
    scene footprint0
    "You found a footprint in the snow!"
    default marked_cp = False
    default powdered_cp = False
    default bucketed_cp = False
    default news_cp = False
    default snowed_cp = False
    default bagged_cp = False
    default labeled_cp = False
    show toolbox:
        xpos 0.0
        ypos 0.02
    call screen cold_print_collection

screen cold_print_collection:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.38
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
        xpos 0.9
        ypos 0.85
        idle "back.png"
        hover "back_hover.png"
        action Jump("car_r")

label toggle_mark_cp:
    if marked_cp == False:
        scene footprint1
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ marked_cp = True
    else:
        "Hmm, seems like you already did this part."
    call screen cold_print_collection

label toggle_powder_cp:
    if marked_cp == True and powdered_cp == False:
        scene footprint2
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ powdered_cp = True
    elif marked_cp == False:
        "This doesn't seem like the correct order."
    else:
        "Hmm, seems like you already did this part."
    call screen cold_print_collection

label toggle_bucket_cp:
    if powdered_cp == True and bucketed_cp == False:
        scene footprint3
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ bucketed_cp = True
        "Mixing for 60 seconds..."
        scene footprint4
        show toolbox:
            xpos 0.0
            ypos 0.02
        "Pouring mixture..."
        scene footprint5
        show toolbox:
            xpos 0.0
            ypos 0.02
    elif powdered_cp == False:
        "This doesn't seem like the correct order."
    else:
        "Hmm, seems like you already did this part."
    call screen cold_print_collection

label toggle_news_cp:
    if bucketed_cp == True and news_cp == False:
        scene footprint6
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ news_cp = True
        call screen snow_cp
    elif bucketed_cp == False:
        "This doesn't seem like the correct order."
        call screen cold_print_collection
    else:
        "Hmm, seems like you already did this part."
        call screen cold_print_collection

screen snow_cp:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.38
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
        xpos 0.9
        ypos 0.85
        idle "back.png"
        hover "back_hover.png"
        action Jump("car_r")
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
    "Waiting 10 mins for footprint to harden..."
    hide screen snow_cp
    scene footprint8
    show toolbox:
        xpos 0.0
        ypos 0.02
    call screen cold_print_collection

label toggle_bag_cp:
    if snowed_cp == True and bagged_cp == False:
        scene footprint9
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ bagged_cp = True
    elif snowed_cp == False:
        "This doesn't seem like the correct order."
    else:
        "Hmm, seems like you already did this part."
    call screen cold_print_collection

label toggle_tape_cp:
    if bagged_cp == True and labeled_cp == False:
        $ labeled_cp = True
        "Evidence collected, good work."
        jump car_r
    else:
        "This doesn't seem like the correct order."
        call screen cold_print_collection

label inside:
    scene bg car_inside
    call screen pre_glass

screen pre_glass:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.56
        ypos 0.92
        idle "glass_hover_hide.png"
        hover "glass_hover_show.png"
        action Jump("found_glass")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.2
        ypos 0.85
        idle "back.png"
        hover "back_hover.png"
        action Jump("car_r")

label found_glass:
    scene glass0
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
    call screen glass_collection

screen glass_collection:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.38
        idle "evidence_markers.png"
        hover "evidence_markers_hover.png"
        action Jump("toggle_mark_g")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.6
        idle "bags.png"
        hover "bags_hover.png"
        action Jump("toggle_bag_g")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.08
        ypos 0.8
        idle "evidence_tape.png"
        hover "evidence_tape_hover.png"
        action Jump("toggle_tape_g")
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
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.85
        idle "back.png"
        hover "back_hover.png"
        action Jump("inside")

label toggle_mark_g:
    if marked_g == False:
        scene glass0_1
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ marked_g = True
    else:
        "Hmm, seems like you already did this part."
    call screen glass_collection

label toggle_paper:
    if marked_g == True and papered_g == False:
        scene glass1
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ papered_g = True
    elif marked_g == False:
        "This doesn't seem like the correct order."
    else:
        "Hmm, seems like you already did this part."
    call screen glass_collection

label toggle_tweezers:
    if papered_g == True and tweezered_g == False:
        scene glass2
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ tweezered_g = True
        "Wrapping bundle..."
        scene glass3
        show toolbox:
            xpos 0.0
            ypos 0.02
    elif papered_g == False:
        "This doesn't seem like the correct order."
    else:
        "Hmm, seems like you already did this part."
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
    else:
        "Hmm, seems like you already did this part."
    call screen glass_collection

label toggle_tape_g:
    if bagged_g == True and labeled_g == False:
        scene glass5
        show toolbox:
            xpos 0.0
            ypos 0.02
        $ labeled_g = True
        "Evidence collected. Great work!"
        jump inside
    elif bagged_g == False:
        "This doesn't seem like the correct order."
        call screen glass_collection
    else:
        "Hmm, seems like you already did this part."
        call screen glass_collection

label car_b:
    scene bg car_back
    call screen car_b_options

screen car_b_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action Jump("car_r")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action Jump("car_l")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.5
        ypos 0.9
        idle "down_arrow.png"
        hover "down_arrow_hover.png"
        action Jump("car_down")

label car_down:
    scene car_down
    "Tire tracks!"
    call screen tracks

screen tracks:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.85
        ypos 0.85
        idle "camera.png"
        hover "camera_hover.png"
        action Jump("take_picture")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.15
        ypos 0.85
        idle "back.png"
        hover "back_hover.png"
        action Jump("car_b")

label take_picture:
    $ flash = Fade(.25, 0, .75, color="#fff")
    scene picture
    with flash
    "Wowzers!"
    call screen tracks

label car_l:
    scene bg car_left
    call screen car_l_options

screen car_l_options:
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.05
        ypos 0.5
        idle "arrow_left.png"
        hover "arrow_left_hover.png"
        action Jump("car_b")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.95
        ypos 0.5
        idle "arrow_right.png"
        hover "arrow_right_hover.png"
        action Jump("car_f")

label end:
    # This ends the game.

    return
