init -4 python:
    import os

    pressed = ""
    print_imported = False
    current_print = ""
    NUM_PRINTS = 7
    i = 1
    prints = {}

    class LabMCQ:
        def __init__(self, question, choices, responses):
            self.question = question
            self.choices = choices
            self.responses = responses
            self.items = [(choice[0], index) for index, choice in enumerate(choices)]

        def is_correct(self, choice):
            return 0 <= choice < len(self.choices) and self.choices[choice][1]

        def say_responses(self, choice):
            for response in self.responses[choice]:
                renpy.say(None, response)

    class LabPrint:
        def __init__(self, image, closeup_1="", closeup_2="", closeup_3="", scores=None, mcq=None):
            self.image = image
            self.processed = False
            self.closeup_1 = closeup_1
            self.closeup_2 = closeup_2
            self.closeup_3 = closeup_3
            self.scores = scores or {}
            self.mcq = mcq

        def process_print(self):
            self.processed = True

    def lab_afis_file_exists(file_name):
        path = os.path.join(renpy.config.gamedir, "images", "data_analysis_lab", file_name)
        return os.path.isfile(path)

    for print_number in range(1, NUM_PRINTS + 1):
        image_name = "print_{}".format(print_number)
        prints[image_name] = LabPrint(image_name)
        for closeup_number in range(1, 4):
            closeup_name = "{}_closeup_{}".format(image_name, closeup_number)
            if lab_afis_file_exists(closeup_name + ".png"):
                setattr(prints[image_name], "closeup_{}".format(closeup_number), closeup_name)

    prints["print_1"].scores = {
        "print_1": (True, 99),
        "print_2": (False, 60),
        "print_3": (False, 37),
        "print_4": (False, 46),
        "print_5": (False, 39),
        "print_6": (False, 28),
        "print_7": (False, 15),
    }
    prints["print_2"].scores = {
        "print_1": (False, 60),
        "print_2": (True, 98),
        "print_3": (False, 37),
        "print_4": (False, 46),
        "print_5": (False, 39),
        "print_6": (False, 28),
        "print_7": (False, 15),
    }

    prints["print_1"].mcq = LabMCQ(
        "What kind of pattern is shown in the rightmost fingerprint?",
        [("Checkered", False), ("Zigzags", False), ("Whorls", True)],
        [
            ["This is not a checkered pattern. Try again."],
            ["This is not a zigzag pattern. Try again."],
            ["This is a whorl. Good job!"],
        ],
    )
    prints["print_2"].mcq = LabMCQ(
        "What kind of pattern is shown in the rightmost fingerprint?",
        [("Whorl", False), ("Loop", False), ("Arch", True)],
        [
            ["This is not a whorl pattern. Try again."],
            ["This is not a loop pattern. Try again."],
            ["This is an arch. Good job!"],
        ],
    )


screen lab_afis():
    imagebutton:
        auto "afis_button_%s"
        xpos 0.18 ypos 0.76
        action Show("lab_fingerprint_upload")
    text "Upload" xpos 0.195 ypos 0.785 size 46

    imagebutton:
        sensitive print_imported
        auto "afis_button_%s"
        xpos 0.35 ypos 0.76
        action Jump("lab_show_prev")
    text "Prev" xpos 0.385 ypos 0.785 size 50

    imagebutton:
        sensitive print_imported
        auto "afis_button_%s"
        xpos 0.52 ypos 0.76
        action Jump("lab_show_next")
    text "Next" xpos 0.559 ypos 0.785 size 50

    imagebutton:
        sensitive print_imported and i in range(1, NUM_PRINTS + 1)
        auto "afis_button_%s"
        xpos 0.69 ypos 0.76
        action Jump("lab_compare")
    text "Compare" xpos 0.7 ypos 0.785 size 50

    textbutton "Back":
        xpos 30 ypos 30
        action Jump("impression_station")


screen lab_fingerprint_upload():
    modal True
    zorder 220
    add Solid("#000000b8")

    frame:
        align (0.5, 0.5)
        xsize 680
        padding (45, 40)
        background Solid("#172c3eee")

        vbox:
            xalign 0.5
            spacing 28

            text "SELECT A FINGERPRINT TO UPLOAD":
                xalign 0.5
                size 30
                color "#ffffff"
                bold True

            if lab_fingerprint_loaded:
                button:
                    xalign 0.5
                    xsize 520
                    padding (25, 20)
                    background Solid("#264b63")
                    hover_background Solid("#34749b")
                    action [Hide("lab_fingerprint_upload"), Jump("lab_load_preloaded_print")]

                    hbox:
                        spacing 25
                        yalign 0.5

                        add Transform("inventory-fingerprint-photo", xysize=(120, 120))

                        vbox:
                            yalign 0.5
                            spacing 8
                            text "Fingerprint Photograph" size 25 color "#ffffff" bold True
                            text "Recovered from the study lamp" size 19 color "#d8e8f2"
            else:
                text "No fingerprint photograph was collected for this case.":
                    xalign 0.5
                    text_align 0.5
                    size 23
                    color "#ffcccc"

            textbutton "Cancel":
                xalign 0.5
                action Hide("lab_fingerprint_upload")
                text_size 22


screen lab_analyzing():
    text "Analyzing..." xpos 0.425 ypos 0.785 size 50


label lab_computer:
    $ hide_notebook()
    $ renpy.hide_screen("inventory")
    $ renpy.hide_screen("open_inv")
    scene afis_plain_with_bar
    show nina talk at right
    if not lab_fingerprint_loaded:
        s "No fingerprint is loaded or available for AFIS analysis."
        $ fingerprint_tasks["fingerprint_1_analyzed"] = True
        $ tasks["Fingerprint analysis"] = True
        hide nina
        jump impression_station
    s "Click Upload, then select the fingerprint photograph collected from the scene."
    hide nina
    call screen lab_afis


label lab_load_preloaded_print:
    if not lab_fingerprint_loaded:
        $ custom_notify("No fingerprint is loaded or available.", False)
        show nina talk at right
        s "There is no collected fingerprint to load into AFIS."
        hide nina
        jump impression_station
    $ imported_print = "print_1"
    $ print_imported = True
    $ current_print = "print_1"
    $ i = 1
    show print_bg as print_bg_l at Transform(xpos=0.17, ypos=0.25)
    show print_bg as print_bg_r at Transform(xpos=0.37, ypos=0.25)
    $ renpy.show(name="print_l", at_list=[Transform(xpos=0.175, ypos=0.25, zoom=0.83)], what=imported_print)
    $ renpy.show(name="print_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen lab_afis


label lab_show_next:
    python:
        i = 1 if i == NUM_PRINTS else i + 1
        current_print = "print_{}".format(i)
        renpy.show(name="print_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen lab_afis


label lab_show_prev:
    python:
        i = NUM_PRINTS if i == 1 else i - 1
        current_print = "print_{}".format(i)
        renpy.show(name="print_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen lab_afis


label lab_compare:
    show screen lab_analyzing
    python:
        closeups_l = [
            prints[imported_print].closeup_1,
            prints[imported_print].closeup_2,
            prints[imported_print].closeup_3,
            prints[imported_print].image,
        ]
        closeups_r = [
            prints[current_print].closeup_1,
            prints[current_print].closeup_2,
            prints[current_print].closeup_3,
            prints[current_print].image,
        ]
        left_image = closeups_l[0] or prints[imported_print].image
        right_image = closeups_r[0] or prints[current_print].image
        renpy.show(name="print_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25)], what=left_image)
        renpy.show(name="print_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25)], what=right_image)
        renpy.pause(1.0)
    jump lab_afis_quiz


label lab_afis_quiz:
    python:
        question = prints[current_print].mcq
        if question is not None:
            renpy.say(None, question.question)
            choice = renpy.display_menu(question.items)
            question.say_responses(choice)
            if not question.is_correct(choice):
                renpy.jump("lab_afis_quiz")
    jump lab_show_results


label lab_show_results:
    python:
        for closeup_index in range(1, 4):
            left_image = closeups_l[closeup_index] or prints[imported_print].image
            right_image = closeups_r[closeup_index] or prints[current_print].image
            renpy.show(name="print_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25)], what=left_image)
            renpy.show(name="print_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25)], what=right_image)
            renpy.pause(1.0)
    hide screen lab_analyzing
    "[prints[imported_print].scores[current_print][1]]%% consistency."

    if prints[imported_print].scores[current_print][0]:
        $ prints[imported_print].process_print()
        "This print has the highest consistency."
        show nina talk at right
        s "According to the database, it belongs to Emily Exgirlfriend."
        s "I'll pass that information to the officers."
        hide nina
        $ fingerprint_tasks["fingerprint_1_analyzed"] = True
        $ tasks["Fingerprint analysis"] = True
        $ custom_notify("Fingerprint analyzed!", True)
        $ print_imported = False
        jump impression_station
    else:
        "This is not the best match. Try another database print."
        call screen lab_afis
