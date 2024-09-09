# screen arrow_screen():
#     image "courtroom_dark_bg"
#     hbox:
#         xpos 0.16 ypos 0.01
#         image("arrow") at Transform (zoom=0.05)


screen score_screen():
    image("courtroom_dark_bg")
    python:
        total_score = len(q_a_bank)
    hbox:
        image("score")
    hbox:
        xalign 0.5 yalign 0.3
        text("Your score is:") color "#ffffff"
    hbox:
        xalign 0.5 yalign 0.4
        text("[score]/[total_score]") color "#ffffff"
    hbox:
        xalign 0.35 ypos 0.5
        textbutton("Click To Retry"):
            style "retry"
            action [Function(reset_answers), Return(value="retry")]
    hbox:
        xalign 0.65 ypos 0.5
        textbutton("Click to view results"):
            style "retry"
            action [Show('results_screen')]

screen results_screen():
    image("courtroom_dark_bg")
    default index_counter = 0
    hbox:
        image("score")
    frame:
        xalign 0.5 ypos 0.2
        xysize(1000,140)
        hbox:
            text(q_a_bank[index_counter]['question']) color "#000000"
    frame:
        xalign 0.5 ypos 0.35
        xysize(1000,200)
        hbox:
            text(q_a_bank[index_counter][user_answers[index_counter]]) color "#000000"
    showif [user_answers[index_counter]] == q_a_bank[index_counter]['answer']:
        hbox:
            xalign 0.5 ypos 0.55
            text("You answered correctly! :)") color "#24840f"
    else:
        hbox:
            xalign 0.5 ypos 0.55
            text("You answered this wrong :(") color "#a30b0b"
    hbox:
        xalign 0.35 ypos 0.6
        textbutton("Click To Retry"):
            style "retry"
            action [Function(reset_answers), Hide('results_screen'), Show('swear')]
    showif (index_counter+1) < len(q_a_bank):
        hbox:
            xalign 0.65 ypos 0.6
            textbutton("Next"):
                style "retry"
                action [SetLocalVariable('index_counter', index_counter+1)]

screen question_screen(q_a):
    image "courtroom_dark_bg"
    frame:
        xalign 0.48 yalign 0.2
        xysize(1300,100)
        hbox:
            xalign 0.5 yalign 0.5
            text(q_a['question'])
    hbox:
        xalign 0.5 ypos 0.3
        textbutton(q_a['choice_1']):
            style "custom_button"
            action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_1'), Return()]
    hbox:
        xalign 0.5 ypos 0.45
        textbutton(q_a['choice_2']):
            style "custom_button"
            action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_2'), Return()]
    hbox:
        xalign 0.5 ypos 0.6
        textbutton(q_a['choice_3']):
            style "custom_button"
            action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_3'), Return()]
    showif q_a['choice_4'] != "":
        hbox:
            xalign 0.5 ypos 0.75
            textbutton(q_a['choice_4']):
                style "custom_button"
                action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_4'), Return()]


screen swear():
    image "courtroom_dark_bg"
    frame:
        xalign 0.48 yalign 0.35
        xysize(1300,100)
        hbox:
            xalign 0.5 yalign 0.5
            text("Do you, [name], swear that the evidence you shall give the court within trial shall be the truth, the whole truth and nothing but the truth?")
    hbox:
        xalign 0.5 ypos 0.5
        textbutton("Yes"):
            style "retry"
            action [Jump('start_questions')]
    hbox:
        xalign 0.5 ypos 0.6
        textbutton("No"):
            style "retry"
            action [Hide('swear'), Show('disqualified')]

screen disqualified():
    image "courtroom_dark_bg"
    frame:
        xalign 0.5 ypos 0.3
        xysize(1200,100)
        hbox:
            xalign 0.5 yalign 0.5
            text("You are disqualified as a witness.\nAll witnesses must be sworn in to tell the truth during testimony.")
    frame:
        xalign 0.5 ypos 0.45
        xysize(1200,200)
        hbox:
            yalign 0.5
            text("Fact: Lying or being untruthful by omission under oath is called Perjury. Perjury is a serious crime and an indictable offence with a potential prison sentence of up to 14 years according to section 131.1 subsection 3 of the Criminal Code of Canada.") 
    hbox:
        xalign 0.5 ypos 0.7
        textbutton("Click To Retry"):
            style "retry"
            action [Hide('disqualified'), Show('swear')]