screen arrow_screen():
    image "courtroom_dark_bg"
    hbox:
        xpos 0.16 ypos 0.01
        image("arrow") at Transform (zoom=0.05)
        
screen score_screen():
    image("courtroom_dark_bg")
    python:
        total_score = len(q_a_bank)
    hbox:
        image("score")
    hbox:
        xalign 0.5 yalign 0.3
        text("Your score is:")
    hbox:
        xalign 0.5 yalign 0.4
        text("[score]/[total_score]")
    hbox:
        xalign 0.5 ypos 0.5
        textbutton("Click To Retry"):
            style "custom_button"
            action [Function(reset_answers), Return(value="retry")]

screen question_screen(q_a):
    image "courtroom_dark_bg"
    frame:
        xalign 0.48 yalign 0.2
        text(q_a['question'])
    hbox:
        xalign 0.5 ypos 0.3
        textbutton(q_a['choice_1']):
            style "custom_button"
            action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_1'), Return()]
    hbox:
        xalign 0.5 ypos 0.4
        textbutton(q_a['choice_2']):
            style "custom_button"
            action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_2'), Return()]
    hbox:
        xalign 0.5 ypos 0.5
        textbutton(q_a['choice_3']):
            style "custom_button"
            action [Function(check_answer, correct_answer=q_a['answer'], choice='choice_3'), Return()]
