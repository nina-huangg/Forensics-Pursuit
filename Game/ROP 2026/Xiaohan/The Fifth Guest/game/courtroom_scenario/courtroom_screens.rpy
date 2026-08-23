default responses = []


screen reminder:
    hbox:
        xpos 0.8 ypos 0.615
        imagebutton:
            auto "question_%s" at Transform(zoom=0.3)
            action ToggleVariable("reminder_pressed")

    $ reminder_text = responses[-1] if responses else persistent.reminder_text or ""

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
            action Jump("court_lex_intro2")
            sensitive (player_fname.strip() and player_lname.strip() and player_prefix.strip())


screen specialty_exploration_screen(specialty):
    # Read the already-loaded specialty data instead of re-parsing the JSON,
    # so the case-name placeholders are resolved here too.
    python:
        shown_specialty = get_specialty(specialty)
        shown_evidence = shown_specialty.evidence if shown_specialty else None
    
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
        ypos 175
        spacing 18

        text "The Death of [victim_name]\nSpecialty: [specialty]":
            size 30
            bold True
            # Dark ink on the pale corridor background; the light outline keeps
            # it legible over the darker centre of the photo.
            color "#10242f"
            outlines [ (2, "#ffffffb0", 0, 0) ]

        # A specialty can carry several exhibits, so the list scrolls rather
        # than running off the bottom of the screen.
        viewport:
            xsize 1240
            ysize 470
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                xmaximum 1180
                spacing 20

                # Display all evidence items
                if shown_evidence:
                    for court_ev in shown_evidence:
                        frame:
                            background "#ffffff20"
                            padding (20, 20)
                            xfill True

                            vbox:
                                spacing 10
                                text "[court_ev.name]":
                                    size 24
                                    bold True
                                    color "#10242f"
                                text "[court_ev.description]":
                                    size 20
                                    color "#10242f"
                else:
                    text "No evidence found for this specialty.":
                        color "#ff0000"

    hbox:
        xalign 0.5
        yalign 0.8
        spacing 100

        button:
            style "selection_button"
            action Jump("court_specialty_menu")
            text "Return to Specialty Selection" style "selection_button_text"

        button:
            style "selection_button"
            action [SetVariable("persistent.specialty", specialty), If(tutorial_skipped == False, Jump("court_tutorial_lex_diff"), Jump("court_difficulty_selection"))]
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
            action Jump("court_ending_0")


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



screen courtroom_api_key_missing():
    # The courtroom's examination is generated live by the Gemini API, so without a
    # key every one of Lex's lines would come back as an error string.
    tag menu
    modal True

    default _web_key_input = VariableInputValue("persistent.web_gemini_api_key")

    add gui.main_menu_background
    add Solid("#081018e0")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        background Solid("#172c3ee8")
        padding (60, 50)

        vbox:
            spacing 26

            if renpy.variant("web"):
                text "Enter your Gemini API key":
                    size 52
                    color "#ffffff"
                    bold True

                text "Lex Machina's questions and your evaluation are generated live. Each player uses their own free key rather than a shared one, so it does not run out after a few playthroughs.":
                    size 27
                    color "#dceaf2"
                    line_spacing 8

                text "To get one:":
                    size 27
                    color "#8fd3ff"
                    bold True

                text "1.  Get a free key at https://aistudio.google.com/\n2.  Paste it below\n3.  It is remembered in this browser -- you only need to do this once":
                    size 25
                    color "#dceaf2"
                    line_spacing 10

                hbox:
                    xfill True
                    spacing 12

                    frame:
                        xfill True
                        background "#0d1a24"
                        padding (16, 12)
                        input:
                            value _web_key_input
                            length 200
                            color "#ffffff"
                            size 26
                            xfill True
                            # Kept on even though pygame.scrap (what this relies
                            # on) is not available on web -- harmless, and it is
                            # what makes Ctrl+V work on the desktop build.
                            copypaste True

                    textbutton "Paste":
                        text_size 24
                        text_color "#ffffff"
                        background "#245273"
                        hover_background "#2f6c98"
                        padding (22, 14)
                        # Ctrl+V can't reach the clipboard on web (see
                        # web_paste_from_clipboard); this button uses the
                        # browser's Clipboard API directly instead.
                        action Function(web_paste_from_clipboard)

                text "If Paste doesn't work, try right-click > Paste in the box, or type the key.":
                    size 18
                    color "#8fa6b4"

                hbox:
                    xalign 0.5
                    spacing 24

                    textbutton "Continue":
                        text_size 30
                        background "#2ecc71"
                        hover_background "#27ae60"
                        padding (40, 14)
                        sensitive persistent.web_gemini_api_key.strip() != ""
                        action Return()

                    textbutton "Back":
                        text_size 30
                        background "#245273"
                        hover_background "#2f6c98"
                        padding (40, 14)
                        action Return()
            else:
                text "The courtroom needs an API key":
                    size 52
                    color "#ffffff"
                    bold True

                text "Lex Machina's questions and your evaluation are generated live, so this scenario cannot run without a Google Gemini API key.":
                    size 27
                    color "#dceaf2"
                    line_spacing 8

                text "To enable it:":
                    size 27
                    color "#8fd3ff"
                    bold True

                text "1.  Get a free key at https://aistudio.google.com/\n2.  Open {b}game/.env{/b} in this project\n3.  Set {b}GEMINI_API_KEY=your-key-here{/b}\n4.  Restart the game":
                    size 25
                    color "#dceaf2"
                    line_spacing 10

                textbutton "Back":
                    xalign 0.5
                    text_size 30
                    background "#245273"
                    hover_background "#2f6c98"
                    padding (40, 14)
                    action Return()


screen courtroom_loading_overlay():
    # Matches the composition of entering_lab_screen.jpg (title high, caption
    # low) but built in-engine, since there is no courtroom equivalent of that
    # artwork. Not modal -- renpy.pause below must be able to time out.
    zorder 200

    add Solid("#04101ad0")

    text "Forensics Pursuit":
        xalign 0.5
        yalign 0.36
        font "ConcertOne-Regular.ttf"
        size 92
        color "#ffffff"
        outlines [ (4, "#000000aa", 0, 3) ]

    text "ENTERING THE COURTROOM.....":
        xalign 0.5
        yalign 0.70
        font "ConcertOne-Regular.ttf"
        size 52
        color "#dceaf2"
        outlines [ (3, "#000000aa", 0, 2) ]
