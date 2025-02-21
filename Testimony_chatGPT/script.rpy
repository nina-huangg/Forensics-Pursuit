define l = Character("Lex Machina")
define s = Character("Tutorial")
define j = Character("Judge")

label start:
    scene bg spec
    $ persistent.case_choice = None
    $ persistent.specialty = None
    $ context_history = []
    $ unintelligible_count = 0
    $ mentioned_truths = set()  

    show sprite happy
    s "Welcome to the courtroom. My name is |Supervisor|, and I'll be guiding you through your preparation before you deliver expert testimony!"
    show sprite explain
    s "Don't worry, this is not a real court, and there currently are no stakes involved. It is simply a training simulation intended to help you practice!"
    show sprite neutral
    s "Let's start by selecting your case. Each one will present different forensic challenges, so read through the case details carefully before making your choice."
    jump case_selection_menu

label case_selection_menu:
    scene bg spec
    menu:
        "Case A: The Death of Ana Konzaki":
            jump case_a_screen
        "Case B: The Park Incident":
            jump case_b_screen
    return

label case_a_screen:
    scene bg black
    call screen case_a_screen

label case_b_screen:
    scene bg black
    call screen case_b_screen

screen case_a_screen:
    frame:
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.2
        text "On the night of March 15th, Ana Konzaki was found dead at a house party hosted by her and her boyfriend, Ezra Verhoesen. The party was a casual gathering with alcohol and marijuana present, but no hard drugs. Witnesses report that a violent altercation broke out between Ezra and an unknown individual, resulting in both men sustaining injuries. Ana was later discovered unconscious with a fatal head wound. One witness claims to have called a drug dealer, Edward Bartlett, on the night of the party. Edward is also the accused on trial, as some witnesses identified him as the individual who attacked Ezra in a lineup."
  
    hbox:
        xalign 0.5
        yalign 0.7
        spacing 100

        button:
            background "#4C4C4C"
            hover_background "#363737"
            action [Jump("case_selection_menu"), SetVariable("persistent.case_choice", None)]
            text "Return to Case Selection"

        button:
            background "#4C4C4C"
            hover_background "#363737"
            action [SetVariable("persistent.case_choice", "Case A"), Jump("tutorial_specialty")]
            text "Choose Case A"

screen case_b_screen:
    frame:
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.2
        text "An unknown body was discovered floating in a lake in a public park by a passer-by. The victim was later identified by family as 13 year old Jacob DeSouza. The cause of death appears to be strangulation, and not drowning. The accused is his adoptive father, Kiernan DeSouza. Kiernan had been reported absent from work and was not at home around the time of Jacob's death. Furthermore, Kiernan's car was discovered near the lake where the body was found. The investigation has been complicated by the lack of direct witnesses and evidence of forced entry into the home."

    hbox:
        xalign 0.5
        yalign 0.7
        spacing 100

        button:
            background "#4C4C4C"
            hover_background "#363737"
            action [Jump("case_selection_menu"), SetVariable("persistent.case_choice", None)]
            text "Return to Case Selection"

        button:
            background "#4C4C4C"
            hover_background "#363737"
            action [SetVariable("persistent.case_choice", "Case B"), Jump("tutorial_specialty")]
            text "Choose Case B"

label tutorial_specialty:
    scene bg spec
    show sprite happy
    s "Perfect! Now, let's choose your forensic specialty."
    show sprite explain
    s "As an expert witness, your role is to analyze and present evidence within your area of expertise. Your selection will determine the type of evidence you'll be responsible for in court."
    show sprite neutral
    s "Because this is just a mock scenario, you will only have to testify for two pieces of evidence. Please look through the evidence carefully!"
    jump specialty_menu

label specialty_menu:
    scene bg spec
    $ chosen_specialty = None
    menu:
        "Anthropology":
            $ chosen_specialty = "Anthropology"
            jump specialty_exploration
        "Biology":
            $ chosen_specialty = "Biology"
            jump specialty_exploration
        "Chemistry":
            $ chosen_specialty = "Chemistry"
            jump specialty_exploration
        "Psychology":
            $ chosen_specialty = "Psychology"
            jump specialty_exploration
        "Identification":
            $ chosen_specialty = "Identification"
            jump specialty_exploration

label specialty_exploration:
    scene bg black

    $ case_details = cases[persistent.case_choice]
    call screen specialty_exploration_screen(chosen_specialty)

screen specialty_exploration_screen(specialty): 
    $ case_details = cases[persistent.case_choice]
    $ evidence_dict = case_details['evidence'][specialty] 

    text "[case_details['case_name']]\nSpecialty: [specialty]":
        xalign 0.5
        yalign 0.3

    text "Evidence Point 1: [evidence_dict['point_1']]":
        xalign 0.5
        yalign 0.4

    text "Evidence Point 2: [evidence_dict['point_2']]":
        xalign 0.5
        yalign 0.5

    hbox:
        xalign 0.5
        yalign 0.7
        spacing 100

        button:
            background "#4C4C4C"
            hover_background "#363737"
            action Jump("specialty_menu")
            text "Return to Specialty Selection"

        button:
            background "#4C4C4C"
            hover_background "#363737"
            action [SetVariable("persistent.specialty", specialty), Jump("tutorial_lex_diff")]
            text "Choose this Specialty"

label tutorial_lex_diff:
    scene bg spec
    show sprite happy
    s "Great choice! Now, there's just one more thing before you step into court."
    show sprite think 
    s "Inside the courtroom, you'll be examined by Lex Machina, a mock trial lawyer."
    show sprite neutral
    s "Depending on your selection, Lex will take on one of two roles—either as the prosecution or the defense."
    show sprite explain
    s "If you choose prosecution, Lex will act as the Crown attorney. This is the easier option." 
    show sprite happy
    s "As a prosecutor, Lex's goal is to establish the truth and ensure your testimony is clear, credible, and useful to the court. In this difficulty, if you miss something important, Lex may prompt you to clarify or expand on your findings."
    show sprite explain
    s "If you choose defense, Lex will act as the defense attorney. This is the harder option."
    show sprite neutral
    s "A defense lawyer's priority is to protect their client, which means they will work to discredit you and your testimony. Expect Lex to challenge you with leading or loaded questions, and other cross-examination techniques designed to undermine your credibility." 
    s "You'll need to stay composed, justify your conclusions, and ensure your testimony remains admissible."
    show sprite happy
    s "Choose wisely! Your decision will shape the difficulty of your examination."
    show sprite think
    s "Once you've made your selection, the court room awaits! I'll be seeing you after your trial. Good luck!"
    jump difficulty_selection 

label difficulty_selection:
    scene bg spec
    menu:
        "Prosecution":
            $ LEX_DIFFICULTY = "prosecution"
            $ unplayed_difficulty = "defense"
            jump lex_intro
        "Defense":
            $ LEX_DIFFICULTY = "defense"
            $ unplayed_difficulty = "prosecution"
            jump lex_intro

label lex_intro:
    scene bg room
    "A figure walks into the room, wearing a crisp suit and carrying a briefcase."
    show lawyer
    l "Hello, my name is Lex Machina. I'll be examining you as an expert witness for this case."
    l "Before we start, let me introduce you to the Judge presiding over this case, |judge name|."
    show judge
    j "Nice to meet you! Since this is not a real case, I will not be making any verdicts today, but I will be evaluating your testimony with Lex."
    hide judge
    show lawyer
    l "I believe you've chosen to testify as an expert for [persistent.case_choice] in [persistent.specialty]. Very well, let's proceed."
    $ user_name = renpy.input("Could you please state your full first and last name for the court?", length=25)
    if not user_name:
        $ user_name = "Witness"
    $ case_details = cases[persistent.case_choice] 
    $ ai_first_question = generate_response("Generate the first question for the expert witness to establish qualification in their field. Keep it short.", user_name, persistent.specialty, case_details, context_history, unintelligible_count,)
    l "Thank you, [user_name]. Let's begin."
    jump first_question

label first_question:
    $ responses = divide_response_v2(ai_first_question)
    $ say_responses(responses)
    $ context_history.append(f"AI: {ai_first_question}")
    $ user_prompt = renpy.input("Your answer here:")
    $ context_history.append(f"User: {user_prompt}")
    python:
        all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty)
    $ ai_response = generate_response(user_prompt, user_name, persistent.specialty, case_details, context_history, unintelligible_count)
    $ responses = divide_response_v2(ai_response)
    $ say_responses(responses)
    $ context_history.append(f"AI: {ai_response}")

    if "QUALIFICATION: UNQUALIFIED" in ai_response:
        jump game_over
    elif "QUALIFICATION: QUALIFIED" in ai_response:
        $ mentioned_truths = set()
        python:
            for evidence_point in truth_bases[persistent.case_choice][persistent.specialty]:
                for truth in truth_bases[persistent.case_choice][persistent.specialty][evidence_point]:
                    if truth.lower() in user_prompt.lower():
                        mentioned_truths.add(truth.lower())
        jump interview_loop
    elif "unintelligible response" in ai_response:
        $ unintelligible_count += 1
        if unintelligible_count >= 3:
            jump game_over
        else:
            jump first_question
    else:
        "An unexpected error occurred. Please restart the game."
        return

label interview_loop:
    while True:
        $ user_prompt = renpy.input("Your answer here:")
        if user_prompt.lower() in ["exit", "quit", "stop"]:
            l "Thank you for your time, [user_name]. This concludes the interview."
            return
        $ context_history.append(f"User: {user_prompt}")
        python:
            all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty) 
            for evidence_point in truth_bases[persistent.case_choice][persistent.specialty]:
                for truth in truth_bases[persistent.case_choice][persistent.specialty][evidence_point]:
                    if truth.lower() in user_prompt.lower():
                        mentioned_truths.add(truth.lower()) 

        $ ai_response = generate_response(user_prompt, user_name, persistent.specialty, case_details, context_history, unintelligible_count)
        $ responses = divide_response_v2(ai_response)
        $ say_responses(responses)
        $ context_history.append(f"AI: {ai_response}")

        python:
            if "i have no further questions, your honour" in ai_response.lower(): 
                renpy.jump("interview_end")

        if "QUALIFICATION: UNQUALIFIED" in ai_response:
            jump game_over
        if "unintelligible response" in ai_response:
            $ unintelligible_count += 1
            if unintelligible_count >= 3:
                jump game_over
            elif "examination cannot continue" in ai_response.lower():
                jump game_over
            else:
                $ ai_response = generate_response("Generate a question for the user. Ensure that they follow the rules of the court and establish key information for the triers of fact.", user_name, persistent.specialty, case_details, context_history, unintelligible_count)
                $ responses = divide_response_v2(ai_response)
                $ say_responses(responses)
                $ context_history.append(f"AI: {ai_response}")
                jump interview_loop
        else:
            $ unintelligible_count = 0
    return

label game_over:
    scene bg gameover
    "The examination has been terminated because you were deemed unqualified to testify as an expert witness."
    "Please select \"Restart\" to try again."
    menu:
        "Restart":
            jump start
        "Quit":
            $ renpy.quit()

python:
    if LEX_DIFFICULTY == "prosecution":
        unplayed_difficulty = "defense"
    elif LEX_DIFFICULTY == "defense":
        unplayed_difficulty = "prosecution"
    else:
        unplayed_difficulty = "error"

label interview_end:
    scene bg room
    show lawyer
    l "Thank you for your time, [user_name]."
    show judge
    j "Thank you, Lex. [user_name], you may leave the court room. You will receive your evaluation outside with your supervisor."
    hide judge
    hide lawyer
    python:
        try:
            all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty)
            full_transcript = "\n".join(context_history)
            evaluation_prompt = (
                f"Evaluate the expert witness testimony based on the following transcript:\n\n{full_transcript}\n\n"
                f"The expert testified as a {persistent.specialty} in {case_details['case_name']}.\n\n"
                f"All the truth bases they needed to say are:\n\n{all_truths}\n\n"
                f"Evaluate the testimony considering these grading criteria in mind:\n\n{grading_criteria}\n\n"
                f"Generate 3-5 concise bullet points that explain the evaluation and give a total score out of 100 based on the grading criteria by saying exactly 'Score: X'. Please ensure points are 20 words or less each."
            )
            evaluation_response = generate_response(evaluation_prompt, user_name, persistent.specialty, case_details, context_history, unintelligible_count)
            score_match = re.search(r"Score: (\d+)", evaluation_response)
            if score_match:
                score = int(score_match.group(1))
                eval_comments = re.sub(r"Score: \d+", "", evaluation_response).strip()
            else:
                score = 0
                eval_comments = "Score not found in evaluation."

            renpy.store.eval_comments = evaluation_response
            renpy.store.score = score  

            print(f"EVAL COMMENTS:\n{renpy.store.eval_comments}")
            print(f"SCORE:\n{renpy.store.score}")

        except Exception as e:
            renpy.store.eval_comments = f"Error: {str(e)}"
            renpy.store.score = 0

    scene bg spec
    show sprite happy
    s "Welcome back, [user_name]! In just a second, Lex and the Judge will return with any feedback they have for you."
    show sprite explain
    s "After you receive your feedback, I encourage you to testify again for the [unplayed_difficulty] to get the full court room experience."
    show sprite neutral
    s "You can also choose a whole new case and specialty and start again! The choice is yours!"
    #ADD FOOTSTEPS SOUND HERE HEHEHE
    show sprite think
    s "Oh! Sounds like Lex and the Judge are about to join us. Don't worry, I'm sure you did great!"
    jump evaluation_sec

label evaluation_sec:
    scene bg spec
    show lawyer
    l "Hi |supervisor| and [user_name]. Are you ready to receive your evaluation?"
    hide lawyer
    call screen evaluation_screen                                                                                

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
            
        textbutton "Done":
            background "#4C4C4C"
            hover_background "#363737"
            xalign 0.9
            yalign 0.9
            action Jump("ending_0")

label ending_0:
    scene bg spec
    call screen credits_lol

screen credits_lol:
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800  
        ysize 600  
        background "#222"  

        vbox:
            xalign 0.5
            yalign 0.5

            text "THANKS FOR PLAYING":
                color "#FFF"
                size 32
        hbox:
            xalign 0.5
            yalign 0.7
            #spacing 100
            button:
                background "#4C4C4C"
                hover_background "#363737"
                action Jump("start")
                text "Try again"
##### INCOMPLETE: SWITCHING SIDES ####
#            button:
#                background "#4C4C4C"
#                hover_background "#363737"
#                action Jump("interview_loop")
#                text "Testify for [unplayed_difficulty]"
