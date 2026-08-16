################################################################################
## CA Chamber (cyanoacrylate fuming chamber) settings interface
################################################################################

init python:
    on_ca_temperature = False
    on_ca_timer = False
    ca_correct_label = ""
    ca_incorrect_label = ""
    ca_correct_time_start = ""
    ca_correct_time_end = ""
    ca_correct_temp_start = ""
    ca_correct_temp_end = ""

    class CANumberEntry:
        """A custom data type representing a multi-digit number entry (temp or time)."""
        hundred_digit: int
        ten_digit: int
        one_digit: int
        curr_digit: str
        selected: str

        def __init__(self, start_digit="hundred") -> None:
            self.hundred_digit = None
            self.ten_digit = None
            self.one_digit = None
            self.selected = ""
            self.curr_digit = start_digit

        def increase_place(self) -> None:
            if self.curr_digit == "hundred":
                self.curr_digit = "ten"
            elif self.curr_digit == "ten":
                self.curr_digit = "one"
            self.update_selected()

        def update_hundred_digit(self, hundred_digit: int) -> None:
            self.hundred_digit = hundred_digit

        def update_ten_digit(self, ten_digit: int) -> None:
            self.ten_digit = ten_digit

        def update_one_digit(self, one_digit: int) -> None:
            self.one_digit = one_digit

        def update_selected(self) -> None:
            hundred_digit = 0 if self.hundred_digit is None else self.hundred_digit
            ten_digit = 0 if self.ten_digit is None else self.ten_digit
            one_digit = 0 if self.one_digit is None else self.one_digit
            self.selected = f"{hundred_digit}{ten_digit}{one_digit}"

        def reset(self, start_digit="hundred") -> None:
            self.hundred_digit = None
            self.ten_digit = None
            self.one_digit = None
            self.curr_digit = start_digit

    def ca_decrease_place(entry: CANumberEntry) -> None:
        if entry.curr_digit == "one":
            if entry.one_digit is not None:
                entry.one_digit = None
            else:
                entry.curr_digit = "ten"
                entry.ten_digit = None
        elif entry.curr_digit == "ten":
            if entry.ten_digit is not None:
                entry.ten_digit = None
            else:
                entry.curr_digit = "hundred"
                entry.hundred_digit = None
        elif entry.curr_digit == "hundred":
            entry.hundred_digit = None
        entry.update_selected()

    def ca_update_number(entry: CANumberEntry, i: int):
        if entry.curr_digit == "one":
            entry.update_one_digit(i)
        elif entry.curr_digit == "ten":
            entry.update_ten_digit(i)
        elif entry.curr_digit == "hundred":
            entry.update_hundred_digit(i)
        entry.increase_place()

    def ca_verify_time(start: str, end: str, value: str) -> bool:
        return int(start) <= int(value) < int(end)

    def ca_verify_temp(start: str, end: str, value: str) -> bool:
        return int(start) <= int(value) < int(end)

    def reset_ca_chamber_entry():
        global on_ca_temperature, on_ca_timer
        on_ca_temperature = False
        on_ca_timer = False
        ca_temp.reset()
        ca_timer.reset(start_digit="ten")

    ca_temp = CANumberEntry()
    ca_timer = CANumberEntry(start_digit="ten")

screen ca_chamber_keyboard():
    frame:
        align (0.49, 0.82)
        xsize 1440
        ysize 240
        background "#c8c6cb"

    for i, x in enumerate([0.175, 0.3, 0.425, 0.55, 0.675], start=1):
        $ j = 0 if i + 5 == 10 else i + 5
        vbox:
            align (x, 0.72)
            spacing 10
            textbutton f"{i}":
                action If(on_ca_temperature, Function(ca_update_number, ca_temp, i), Function(ca_update_number, ca_timer, i))
                style "keyboard_button"
                text_style "keyboard_text"
        vbox:
            align (x, 0.83)
            spacing 10
            textbutton f"{j}":
                action If(on_ca_temperature, Function(ca_update_number, ca_temp, j), Function(ca_update_number, ca_timer, j))
                style "keyboard_button"
                text_style "keyboard_text"

    vbox:
        align (0.825, 0.83)
        spacing 10
        textbutton "enter" action Jump("ca_chamber_settings_main") style "keyboard_button_2" text_style "keyboard_text"

    vbox:
        align (0.825, 0.72)
        imagebutton:
            idle "backspace_button_idle"
            hover "backspace_button_hover"
            action If(on_ca_temperature, Function(ca_decrease_place, ca_temp), Function(ca_decrease_place, ca_timer))
            at Transform(xsize=200, ysize=85)

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


screen ca_chamber_temperature_screen():
    add "ca_chamber_interface_bg"
    vbox:
        align (0.14, 0.16)
        spacing 10
        textbutton "<" action Jump("ca_chamber_settings_main") text_style "back_button"

    frame:
        align (0.5, 0.55)
        xsize 500
        ysize 5
        background "#5e17eb"

    text "{size=120}°C":
        xalign 0.68
        yalign 0.4

    text "{size=54}Adjust temperature between 120°C and 150°C.":
        xalign 0.5
        yalign 0.27

    $ hundred_digit = " " if ca_temp.hundred_digit is None else ca_temp.hundred_digit
    text f"{hundred_digit}":
        size 250
        xalign 0.4
        yalign 0.42

    $ ten_digit = " " if ca_temp.ten_digit is None else ca_temp.ten_digit
    text f"{ten_digit}":
        size 250
        xalign 0.5
        yalign 0.42

    $ one_digit = " " if ca_temp.one_digit is None else ca_temp.one_digit
    text f"{one_digit}":
        size 250
        xalign 0.6
        yalign 0.42


screen ca_chamber_cooking_time_screen():
    add "ca_chamber_interface_bg"
    vbox:
        align (0.14, 0.16)
        spacing 10
        textbutton "<" action Jump("ca_chamber_settings_main") text_style "back_button"

    frame:
        align (0.62, 0.58)
        xsize 400
        ysize 5
        background "#5e17eb"

    text "{size=51}Set the fuming time. Valid range: 12-15 minutes.":
        xalign 0.6
        yalign 0.25

    $ ten_digit = " " if ca_timer.ten_digit is None else ca_timer.ten_digit
    text f"{ten_digit}":
        size 220
        xalign 0.56
        yalign 0.495

    $ one_digit = " " if ca_timer.one_digit is None else ca_timer.one_digit
    text f"{one_digit}":
        size 220
        xalign 0.66
        yalign 0.495

    text "{size=100}min":
        xalign 0.78
        yalign 0.54


screen ca_chamber_main_interface():
    add "ca_chamber_interface_bg"
    text "{size=90}{b}CA Chamber{/b}":
        xalign 0.5
        yalign 0.36

    text "{size=125}°C":
        xalign 0.66
        yalign 0.47

    text "{size=60}Fuming Time":
        xalign 0.16
        yalign 0.17

    vbox:
        align(0.24, 0.8)
        imagebutton:
            auto "ca_chamber_adjust_time_button_%s"
            action [ToggleVariable("on_ca_timer"), ToggleScreen("ca_chamber_cooking_time_screen"), ToggleScreen("ca_chamber_keyboard"), ToggleScreen("ca_chamber_main_interface")]
            at Transform(zoom=0.2)

    python:
        ten_disp = "0" if ca_timer.ten_digit is None else ca_timer.ten_digit
        one_disp = "0" if ca_timer.one_digit is None else ca_timer.one_digit
        complete_ca_time = str(ten_disp) + str(one_disp)

    text "{b}[ten_disp][one_disp] minutes{/b}":
        size 60
        xalign 0.205
        yalign 0.24

    vbox:
        align(0.5, 0.8)
        imagebutton:
            auto "ca_chamber_adjust_temperature_button_%s"
            action [ToggleVariable("on_ca_temperature"), ToggleScreen("ca_chamber_temperature_screen"), ToggleScreen("ca_chamber_keyboard"), ToggleScreen("ca_chamber_main_interface")]
            at Transform(zoom=0.2)

    $ ca_temperature_disp = "135" if (ca_temp.hundred_digit is None or ca_temp.ten_digit is None or ca_temp.one_digit is None) else f"{ca_temp.hundred_digit}{ca_temp.ten_digit}{ca_temp.one_digit}"

    text "{b}[ca_temperature_disp]{/b}":
        size 225
        align(0.5, 0.54)

    vbox:
        align(0.76, 0.8)
        imagebutton:
            auto "ca_chamber_start_button_%s"
            action If(
                ca_verify_time(ca_correct_time_start, ca_correct_time_end, complete_ca_time) and ca_verify_temp(ca_correct_temp_start, ca_correct_temp_end, ca_temperature_disp),
                Jump(ca_correct_label),
                Jump(ca_incorrect_label)
            )
            at Transform(zoom=0.2)


label ca_chamber_settings_main:
    $ on_ca_timer = False
    $ on_ca_temperature = False
    hide screen ca_chamber_keyboard
    hide screen ca_chamber_temperature_screen
    hide screen ca_chamber_cooking_time_screen
    call screen ca_chamber_main_interface