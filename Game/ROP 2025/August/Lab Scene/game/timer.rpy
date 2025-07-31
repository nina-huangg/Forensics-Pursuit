#### TIMER CODE ####
# You don't need to modify most of this file, except for the comment marked TODO.
# Comments are provided for readability.

# starting label
label timer:
    show timer_bg
    default time_numbers = [0, 0, 0, 0, 0, 0] # stores the input values
    default number_chosen = 0 # the number of variables inputted so far
    default set = False # controls if the user pressed the "SET" button
    default current_choice = -1 # the user's current choice
    call screen timer_screen

# updates the numbers in the array on each input
label set_variables:
    if number_chosen != 0:
        # for i in range(0, 5):
        #     $ time_numbers[i] = time_numbers[i + 1]
        $ time_numbers[0] = time_numbers[0 + 1]
        $ time_numbers[1] = time_numbers[1 + 1]
        $ time_numbers[2] = time_numbers[2 + 1]
        $ time_numbers[3] = time_numbers[3 + 1]
        $ time_numbers[4] = time_numbers[4 + 1]
    $ time_numbers[5] = current_choice
    $ number_chosen = number_chosen + 1
    call screen timer_screen

# sets the time when the user presses "SET"
label confirm_set:
    jump timer_set

# clears the array when the user presses "CLEAR"
label clear_variables:
    # for i in range(0, 5):
    #     $ time_numbers[i] = 0
    $ time_numbers[0] = 0
    $ time_numbers[1] = 0
    $ time_numbers[2] = 0
    $ time_numbers[3] = 0
    $ time_numbers[4] = 0
    $ time_numbers[5] = 0
    call screen timer_screen

# provides the UI for the timer
screen timer_screen:
    hbox:
        xalign 0.705 yalign 0.41
        for i in range(0, 10):
            if time_numbers[5] == i:
                imagebutton:
                    idle f'{i}_display'
                break
    hbox:
        xalign 0.635 yalign 0.41
        for i in range(0, 10):
            if time_numbers[4] == i:
                imagebutton:
                    idle f'{i}_display'
                break
    hbox:
        xalign 0.535 yalign 0.41
        for i in range(0, 10):
            if time_numbers[3] == i:
                imagebutton:
                    idle f'{i}_display'
                break
    hbox:
        xalign 0.465 yalign 0.41
        for i in range(0, 10):
            if time_numbers[2] == i:
                imagebutton:
                    idle f'{i}_display'
                break
    hbox:
        xalign 0.365 yalign 0.41
        for i in range(0, 10):
            if time_numbers[1] == i:
                imagebutton:
                    idle f'{i}_display'
                break
    hbox:
        xalign 0.295 yalign 0.41
        for i in range(0, 10):
            if time_numbers[0] == i:
                imagebutton:
                    idle f'{i}_display'
                break
    hbox:
        xalign 0.222 yalign 0.615
        imagebutton:
            idle "5_button"
            hover "5_button_hover"
            action [SetVariable("current_choice", 5), Jump("set_variables")]
    hbox:
        xalign 0.3195 yalign 0.615
        imagebutton:
            idle "6_button"
            hover "6_button_hover"
            action [SetVariable("current_choice", 6), Jump("set_variables")]
    hbox:
        xalign 0.416 yalign 0.615
        imagebutton:
            idle "7_button"
            hover "7_button_hover"
            action [SetVariable("current_choice", 7), Jump("set_variables")]
    hbox:
        xalign 0.513 yalign 0.615
        imagebutton:
            idle "8_button"
            hover "8_button_hover"
            action [SetVariable("current_choice", 8), Jump("set_variables")]
    hbox:
        xalign 0.608 yalign 0.615
        imagebutton:
            idle "9_button"
            hover "9_button_hover"
            action [SetVariable("current_choice", 9), Jump("set_variables")]
    hbox:
        xalign 0.22 yalign 0.735
        imagebutton:
            idle "0_button"
            hover "0_button_hover"
            action [SetVariable("current_choice", 0), Jump("set_variables")]
    hbox:
        xalign 0.3195 yalign 0.735
        imagebutton:
            idle "1_button"
            hover "1_button_hover"
            action [SetVariable("current_choice", 1), Jump("set_variables")]
    hbox:
        xalign 0.416 yalign 0.735
        imagebutton:
            idle "2_button"
            hover "2_button_hover"
            action [SetVariable("current_choice", 2), Jump("set_variables")]
    hbox:
        xalign 0.513 yalign 0.735
        imagebutton:
            idle "3_button"
            hover "3_button_hover"
            action [SetVariable("current_choice", 3), Jump("set_variables")]
    hbox:
        xalign 0.608 yalign 0.735
        imagebutton:
            idle "4_button"
            hover "4_button_hover"
            action [SetVariable("current_choice", 4), Jump("set_variables")]
    hbox:
        xalign 0.765 yalign 0.615
        imagebutton:
            idle "set_button"
            hover "set_button_hover"
            action Jump("confirm_set")
    hbox:
        xalign 0.765 yalign 0.735
        imagebutton:
            idle "clear_button"
            hover "clear_button_hover"
            action Jump("clear_variables")