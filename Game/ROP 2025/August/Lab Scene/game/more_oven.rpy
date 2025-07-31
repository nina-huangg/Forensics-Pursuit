init python:
    on_temperature = False
    on_timer = False
    correct_time = ""
    correct_temp = ""
    correct_label = ""
    correct_time_start = ""
    correct_time_end = ""
    correct_temp_start = ""
    correct_temp_end = ""

    temp_button_active = {}
    time_button_active = {}
    for p in range(0, 10):
        temp_button_active[p] = True
        time_button_active[p] = True
    temp_button_active[0] = False

    class Temperature:
        """A custom data type representing the oven temperature.
        
        Preconditions:
        - 0 <= hundred_digit <= 9
        - 0 <= ten_digit <= 9
        - 0 <= one_digit <= 9
        - curr_digit == "hundred" or curr_digit == "ten" or curr_digit == "one"
        """
        hundred_digit: int
        ten_digit: int
        one_digit: int
        curr_digit: str
        selected: str
        modifying: bool

        def __init__(self) -> None:
            """Initializes the temperature as 100.
            """
            self.hundred_digit = None
            self.ten_digit = None
            self.one_digit = None
            self.selected = ""
            self.curr_digit = "hundred"
        
        def update_status(self) -> None:
            self.modifying = not self.modifying
        
        def increase_place(self) -> None:
            if self.curr_digit == "hundred":
                if on_temperature:
                    for i in [1, 3, 4, 6, 8, 9]:   
                        temp_button_active[i] = False
                    temp_button_active[0] = True
                else:
                    for i in [6, 7, 8, 9]:
                        time_button_active[i] = False
                    time_button_active[0] = True
                self.curr_digit = "ten"
            elif self.curr_digit == "ten":
                for i in [2, 7]:
                    if on_temperature:
                        temp_button_active[i] = False
                    if on_timer:
                        for i in [6, 7, 8, 9]:
                            time_button_active[i] = True
                self.curr_digit = "one"
            self.update_selected()

        def update_hundred_digit(self, hundred_digit: int) -> None:
            self.hundred_digit = hundred_digit
        
        def update_ten_digit(self, ten_digit: int) -> None:
            self.ten_digit = ten_digit

        def update_one_digit(self, one_digit: int) -> None:
            self.one_digit = one_digit
            
        def update_selected(self) -> None:
            hundred_digit = 0 if self.hundred_digit == None else self.hundred_digit
            ten_digit = 0 if self.ten_digit == None else self.ten_digit
            one_digit = 0 if self.one_digit == None else self.one_digit
            self.selected = f"{hundred_digit}{ten_digit}{one_digit}"

        def reset_temperature(self) -> None:
            self.hundred_digit = None
            self.ten_digit = None
            self.one_digit = None
    
    def decrease_place(temperature: Temperature) -> None:
        if temperature.curr_digit == "one":
            if temperature.one_digit != None:
                temperature.one_digit = None
            else:
                if on_temperature:
                    for i in [2, 7]:
                        temp_button_active[i] = True
                else:
                    for i in [6, 7, 8, 9]:
                        time_button_active[i] = False
                temperature.curr_digit = "ten"
                temperature.ten_digit = None
        elif temperature.curr_digit == "ten":
            if temperature.ten_digit != None:
                temperature.ten_digit = None
            else:
                if on_temperature:
                    for i in [1, 3, 4, 6, 8, 9]:
                        temp_button_active[i] = True
                    temp_button_active[0] = False
                else:
                    for i in [6, 7, 8, 9]:
                        time_button_active[i] = True
                temperature.curr_digit = "hundred"
                temperature.hundred_digit = None
        elif temperature.curr_digit == "hundred":
            temperature.hundred_digit = None
            if on_temperature:
                temp_button_active[0] = False
        temperature.update_selected()
    
    def update_number(temperature: Temperature, i: int):
        if temperature.curr_digit == "one":
            temperature.update_one_digit(i)
        elif temperature.curr_digit == "ten":
            temperature.update_ten_digit(i)
        elif temperature.curr_digit == "hundred":
            temperature.update_hundred_digit(i)
        temperature.increase_place()

    def calculate_true_time(time: str) -> int:
        """Returns time as a number of minutes. time should be f"{hundred_place}{ten_place}{one_place}".
        """
        return time[0] * 60 + time[1] * 10 + time[2] 

    def verify_time(start: str, end: str, time: str):
        true_time = calculate_true_time(time)
        true_start = calculate_true_time(start)
        true_end = calculate_true_time(end)
        return true_start <= true_time and true_time < true_end

    def verify_temp(start: str, end: str, temp: str):
        return int(start) <= int(temp) and int(temp) < int(end)

    temp = Temperature()
    timer = Temperature()
        
screen oven_keyboard():
    frame:
        align (0.49, 0.82)  # Center of the screen
        xsize 1440         # Width of the rectangle
        ysize 240         # Height of the rectangle
        background "#c8c6cb"  # Grey color

    for i, x in enumerate([0.175, 0.3, 0.425, 0.55, 0.675], start=1):
        $ top_button_active = temp_button_active[i] if on_temperature else time_button_active[i]
        $ j = 0 if i + 5 == 10 else i + 5
        $ bottom_button_active = temp_button_active[j] if on_temperature else time_button_active[j]
        vbox:
            align (x, 0.72)
            spacing 10

            textbutton f"{i}" action If(on_temperature, Function(update_number, temp, i), Function(update_number, timer, i)) style "keyboard_button" text_style "keyboard_text" sensitive top_button_active
        vbox:
            align (x, 0.83)
            spacing 10

            textbutton f"{j}" action If(on_temperature, Function(update_number, temp, j), Function(update_number, timer, j)) style "keyboard_button" text_style "keyboard_text" sensitive bottom_button_active

    # vbox:
    #     align (0.825, 0.72)
    #     spacing 10

    #     textbutton "<-" action If(on_temperature, Function(decrease_place, temp), Function(decrease_place, timer)) style "keyboard_button_3" text_style "keyboard_text"

    vbox:
        align (0.825, 0.83)
        spacing 10

        textbutton "enter" action Jump("main") style "keyboard_button_2" text_style "keyboard_text"
    
    vbox:
        align (0.825, 0.72)
        imagebutton:
            idle "backspace_button_idle"
            hover "backspace_button_hover"
            action If(on_temperature, Function(decrease_place, temp), Function(decrease_place, timer))
            at Transform(xsize=200, ysize=85)
    
    # vbox:
    #     align (0.025, 0.025)
    #     spacing 10

    #     textbutton "<" action NullAction() text_style "back_button"

style adjust_button:
    background "#f1eff4"  
    hover_background "#9b9b9b"  
    insensitive_background "#757474"
    padding (50, 20)

style keyboard_button:
    background "#f1eff4"  
    hover_background "#9b9b9b"  
    insensitive_background "#757474"
    padding (60, 10)

style keyboard_button_2:
    background "#e3e2e4"
    hover_background "#9b9b9b" 
    padding (20, 10)

style keyboard_button_3:
    background "#e3e2e4"
    hover_background "#9b9b9b" 
    padding (64, 10)

style keyboard_text:
    size 60
    color "#474646"   

style adjust_text:
    size 52
    color "#474646"

style back_button:
    size 90
    color "#ffffff"

screen temperature:
    add "oven_interface_bg"
    vbox:
        align (0.14, 0.16)
        spacing 10

        textbutton "<" action Jump("main") text_style "back_button"

    frame:
        align (0.5, 0.55)  # Center of the screen
        xsize 500        # Width of the rectangle
        ysize 5         # Height of the rectangle
        background "#5e17eb"  # Grey color
    
    text "{size=120}°F":
        xalign 0.68
        yalign 0.4
    
    text "{size=54}Adjust temperature between 100°F and 975°F.":
        xalign 0.5
        yalign 0.27
    
    $ hundred_digit = " " if temp.hundred_digit == None else temp.hundred_digit

    text f"{hundred_digit}":
        size 250
        xalign 0.4
        yalign 0.42
    
    $ ten_digit = " " if temp.ten_digit == None else temp.ten_digit
    
    text f"{ten_digit}":
        size 250
        xalign 0.5
        yalign 0.42
    
    $ one_digit = " " if temp.one_digit == None else temp.one_digit
    
    text f"{one_digit}":
        size 250
        xalign 0.6
        yalign 0.42

screen cooking_time:
    add "oven_interface_bg"
    vbox:
        align (0.14, 0.16)
        spacing 10

        textbutton "<" action Jump("main") text_style "back_button"

    frame:
        align (0.27, 0.58)  # Center of the screen
        xsize 250        # Width of the rectangle
        ysize 5         # Height of the rectangle
        background "#5e17eb"  # Grey color

    frame:
        align (0.62, 0.58)  # Center of the screen
        xsize 400        # Width of the rectangle
        ysize 5         # Height of the rectangle
        background "#5e17eb"  # Grey color

    $ hour = " " if timer.hundred_digit == None else timer.hundred_digit

    text f"{hour}":
        size 220
        xalign 0.29
        yalign 0.495
    
    text "{size=100}hr":
        xalign 0.39
        yalign 0.54
    
    $ ten_digit = " " if timer.ten_digit == None else timer.ten_digit
    
    text f"{ten_digit}":
        size 220
        xalign 0.56
        yalign 0.495
    
    $ one_digit = " " if timer.one_digit == None else timer.one_digit
    
    text f"{one_digit}":
        size 220
        xalign 0.66
        yalign 0.495

    text "{size=100}min":
        xalign 0.78
        yalign 0.54
    
    text "{size=51}Set cooking time. Note that setting the time to":
        xalign 0.54
        yalign 0.25

    text "{size=51}zero will let the oven preheat.":
        xalign 0.54
        yalign 0.32

screen main_interface:
    add "oven_interface_bg"
    text "{size=90}{b}Bake{/b}":
        xalign 0.5
        yalign 0.36

    text "{size=125}°F":
        xalign 0.66
        yalign 0.47

    text "{size=60}Cook Time":
        xalign 0.16
        yalign 0.17

    vbox:
        align(0.24, 0.8)
        imagebutton:
            auto "oven_adjust_time_button_%s"
            action [ToggleVariable("on_timer"), ToggleScreen("cooking_time"), ToggleScreen("oven_keyboard"), ToggleScreen("main_interface")]
            at Transform(zoom=0.2)
    
    python:
        hours = "0" if timer.hundred_digit == None else timer.hundred_digit
        if timer.hundred_digit == None and timer.ten_digit == None and timer.one_digit == None:
            hours = "0"
            minutes = "00"
        if timer.ten_digit == None and timer.one_digit == None:
            minutes = "00"
        elif timer.ten_digit != None and timer.one_digit == None:
            minutes = f"0{timer.ten_digit}"
        else:
            minutes = f"{timer.ten_digit}{timer.one_digit}"
        complete_time = str(hours) + str(minutes)

    text "{b}[hours] hours [minutes] minutes{/b}":
        size 60
        xalign 0.205
        yalign 0.24

    vbox:
        align(0.5, 0.8)
        imagebutton:
            auto "oven_adjust_temperature_button_%s"
            action [ToggleVariable("on_temperature"), ToggleScreen("temperature"),ToggleScreen("oven_keyboard"), ToggleScreen("main_interface")]
            at Transform(zoom=0.2)

    $ temperature = "350" if temp.hundred_digit == None or temp.ten_digit == None or temp.one_digit == None else f"{temp.hundred_digit}{temp.ten_digit}{temp.one_digit}"
    
    text "{b}[temperature]{/b}":
        size 225
        align(0.5, 0.54)

    # text "{b}correct time: [correct_time], select time: [complete_time], correct temp: [correct_temp], select temp: [temperature]{/b}":
    #     size 20
    #     align(0.1, 0.54)
    
    vbox:
        align(0.76, 0.8)
        imagebutton:
            auto "oven_start_button_%s"
            action If(verify_time(correct_time_start, correct_time_end, complete_time) and verify_temp(correct_temp_start, correct_temp_end, temperature), Jump(correct_label), Jump("incorrect_label"))
            at Transform(zoom=0.2)

label incorrect_label:
    scene oven_closed_idle
    s sweat "This isn't quite right... Let's do this again!"
    $ on_timer = False
    $ on_temperature = False
    hide screen oven_keyboard
    hide screen temperature
    hide screen cooking_time
    call screen main_interface

label main:
    $ on_timer = False
    $ on_temperature = False
    hide screen oven_keyboard
    hide screen temperature
    hide screen cooking_time
    call screen main_interface