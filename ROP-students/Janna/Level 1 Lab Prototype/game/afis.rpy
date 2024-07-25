$ import renpy.random

default pressed = ""
default print_imported = False
default prints = ["print_1", "print_2", "print_3", "print_4", "print_5", "print_6", "print_7"]
default selected_print = ""
default current_print = ""
default current_print_name = ""
default i = 0
default j = 7

screen afis:
    imagebutton:
        auto "afis_button_%s" at Transform(xpos=0.18, ypos=0.76)
        action [SetVariable("pressed", "import"), ToggleScreen("casefile_physical")]
    text "Import" xpos 0.205 ypos 0.785 size 50

    imagebutton:
        sensitive print_imported
        auto "afis_button_%s" at Transform(xpos=0.35, ypos=0.76)
        action Jump("show_prev")
    text "Prev" xpos 0.385 ypos 0.785 size 50

    imagebutton:
        sensitive print_imported
        auto "afis_button_%s" at Transform(xpos=0.52, ypos=0.76)
        action Jump("show_next")
    text "Next" xpos 0.559 ypos 0.785 size 50

    imagebutton:
        sensitive print_imported
        auto "afis_button_%s" at Transform(xpos=0.69, ypos=0.76)
        action Jump("compare")
    text "Compare" xpos 0.7 ypos 0.785 size 50

label computer:
    scene afis_plain_with_bar
    call screen afis

# Light switch fingerprint
label import_print_1:
    show print_bg at Transform(xpos=0.17, ypos=0.25) 
    show print_bg as print_bg_r at Transform(xpos=0.37, ypos=0.25)
    show print_1 at Transform(xpos=0.175, ypos=0.25, zoom=0.83)
    $ selected_print = "print_1"
    call screen afis

label show_next:
    python:
        i = 1 if i == 7 else i + 1
        last_print = "print_7_r" if i == 1 else f"print_{(i - 1) % 7}_r"
        renpy.hide(last_print)
        current_print = f"print_{i}"
        current_print_name = f"print_{i}_r"
        renpy.show(name=current_print_name, at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen afis

label show_prev:
    python:
        renpy.hide(f"print_{i}_r")
        i = 7 if i == 1 or i == 0 else i - 1
        current_print = f"print_{i}"
        current_print_name = f"print_{i}_r"
        renpy.show(name=current_print_name, at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen afis

label compare:
    if current_print == selected_print:
        show print_bg at Transform(xpos=0.3, ypos=0.25)
        show print_1 at Transform(xpos=0.3, ypos=0.25)
        show print_bg as print_bg_r at Transform(xpos=0.5, ypos=0.25)
        show print_1 as print_1_r at Transform(xpos=0.5, ypos=0.25)
        "99%% consistency!"
        if oven.state != "baked":
            $ oven.update_state()
            "Looks like the oven is finished baking!"
        $ fingerprint.process_evidence()
        jump hallway
    else:
        "16%% consistency."
        call screen afis