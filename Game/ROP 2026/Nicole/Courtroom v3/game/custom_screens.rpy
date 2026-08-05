screen reminder:
    hbox:
        xpos 0.8 ypos 0.615
        imagebutton:
            auto "question_%s" at Transform(zoom=0.3)
            action ToggleVariable("reminder_pressed")

    $ reminder_text = responses[-1]

    showif reminder_pressed:
        add "reminder pop up" at Transform(xalign=0.5, yalign=0, zoom=0.9, xzoom=0.86, yzoom=0.8)

        frame:
            xalign 0.5
            xsize 1400  # Set width to control text margins
            yalign 0.1
            background None

            text "[reminder_text]":
                xalign 0.5
                text_align 0.5  # Center align text within the frame
                size 35  # Adjust font size as needed
                color "#ffffff"  # Adjust text color as needed
                xmaximum 1300


screen prefix_dropdown():
    modal True
    zorder 999

    frame:
        background "#202020"
        xalign 0.53
        yalign 0.545
        padding (10, 10)

        vbox:
            spacing 5
            for option in ["Mr.", "Ms.", "Mrs.", "Mx.", "Dr."]:
                textbutton option:
                    action [SetVariable("player_prefix", option), Hide("prefix_dropdown")]


screen nameyourself():
    default p_first_name_input = VariableInputValue("player_fname", default=False)
    default p_last_name_input = VariableInputValue("player_lname", default=False)
    add "frame" at Transform(zoom=0.6, xalign=0.5, yalign=0.45)

    frame:
        left_padding 20
        right_padding 20
        xalign 0.5
        yalign 0.3
        background None
        text "Enter your first and last name.":
            xalign 0.5
            yalign 0.3

    vbox:
        xalign 0.5
        yalign 0.48

        text "Prefix (Dr./Mx./Mr./Ms./Mrs.):"
        hbox:
            button:
                background "#4c4c4cd0"
                xsize 200
                action Show("prefix_dropdown", transition=dissolve)
                text "[player_prefix]" xalign 0.5
            textbutton "∇":
                background "#4C4C4C"
                action Show("prefix_dropdown", transition=dissolve)

        text "First Name: "
        button:
            background "#4c4c4cd0"
            xsize 300
            action p_first_name_input.Toggle()
            input:
                pixel_width(500)
                value p_first_name_input
        text "Last Name: "
        button:
            background "#4c4c4cd0"
            xsize 300
            action p_last_name_input.Toggle()
            input:
                pixel_width(1000)
                value p_last_name_input

    hbox:
        xalign 0.6
        yalign 0.7
        button:
            style "selection_button"
            text "Done" style "selection_button_text"
            action Jump("lex_intro2")
            sensitive (player_fname.strip() and player_lname.strip() and player_prefix.strip())


screen return_to_case_selection():
    hbox:
        xpos 0.5
        ypos 0.8
        xanchor 0.5
        yanchor 0.5

        button:
            style "selection_button"
            text "Return to Case Selection" style "selection_button_text"
            action [SetVariable("switch_cases", True), Jump("case_selection_menu")]


# TODO: Update the title of the case to match yours.
screen specialty_exploration_screen(specialty):    
    # Find the matching specialty data from JSON
    python:
        import json
        file_path = renpy.loader.transfn("courtroom.json")
        with open(file_path, "r") as f:
            specialties_data = json.load(f)
        
        # Get evidence for the selected specialty
        evidence_list = None
        for item in specialties_data:
            if item["specialty"] == specialty:
                evidence_list = item["evidence"]
                break
    
    add "frame" at Transform(zoom=0.85, xalign=0.5, yalign=0.3)

    frame:
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.2
        ysize 500
        xsize 1300
        background None

    vbox:
        xalign 0.5
        yalign 0.35
        xmaximum 1200
        spacing 20
        
        text "The Death of Alastor Brahe\nSpecialty: [specialty.capitalize()]":
            size 30
            bold True
        
        # Display all evidence items
        if evidence_list:
            for evidence in evidence_list:
                frame:
                    background "#ffffff20"
                    padding (20, 20)
                    xfill True
                    
                    vbox:
                        spacing 10
                        text "[evidence['name']]":
                            size 24
                            bold True
                        text "[evidence['description']]":
                            size 20
                        # add evidence["image_name"]:
                        #     xalign 0.5
                        #     zoom 0.5
        else:
            text "No evidence found for this specialty.":
                color "#ff0000"

    hbox:
        xalign 0.5
        yalign 0.8
        spacing 100

        button:
            style "selection_button"
            action Jump("specialty_menu")
            text "Return to Specialty Selection" style "selection_button_text"

        button:
            style "selection_button"
            action [SetVariable("persistent.specialty", specialty), If(tutorial_skipped == False, Jump("tutorial_lex_diff"), Jump("difficulty_selection"))]
            text "Choose this Specialty" style "selection_button_text"


screen evaluation_screen:
    modal True  
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800  
        ysize 600  
        background "#222"  

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "Evaluation":
                color "#FFF"
                size 32
                xalign 0.5
 
            viewport:
                xsize 700
                ysize 400
                scrollbars "vertical"
                mousewheel True
                text renpy.store.eval_comments: 
                    color "#FFF"
                    size 16
                    xalign 0.5
            
            text "Total Score: [renpy.store.score]/100": 
                color "#FFF"
                size 24
                xalign 0.5
            
        button:
            style "selection_button"
            text "Done" style "selection_button_text"
            xalign 0.9
            yalign 0.9
            action Jump("ending_0")


screen credits_lol:
    add "thanks-for-playing":
        xalign 0.5
        yalign 0.5
    hbox:
        xalign 0.5
        yalign 0.7
        #spacing 100
        button:
            style "selection_button"
            action [SetVariable("answered_first_question", False), Jump("start")]
            text "Try again" style "selection_button_text"
#           button:
#               background "#4C4C4C"
#               hover_background "#363737"
#               action [SetVariable("LEX_DIFFICULTY", specialty), Jump("interview_loop")]
#               text "Testify for the [unplayed_difficulty]"



style selection_button:
    background "#68c5e1"  
    hover_background "#5092a6"
    insensitive_background "#2a2a2a"
    padding (40, 12)


style selection_button_text:
    color "#050101"  
    hover_color "#ffffff"  
    insensitive_color "#8888887f" 


screen achievement_banner(text):
    zorder 100
    frame:
        xpos 12
        ypos -100
        at slide_in
        xsize 400
        ysize 100
        background "#6bc0d0cc"

        text text size 30 color "#ffffff" xalign 0.5 yalign 0.5

    timer 3.0 action Hide("achievement_banner")


transform slide_in:
    ypos 20
    easein 0.5 ypos 50  # Smooth slide-down effect

