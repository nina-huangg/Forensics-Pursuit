"""This file contains ALL code related to the fingerpring processing system.
In order to add/remove a new print, there are three things you need to do:
    (1) Change the value of NUM_PRINTS below. Right now, it's 7 because
    I have 7 different kinds of fingerprints that I want to show for the
    right comparison image.
    (2) If you're adding a print (or adding closeup images), you must STICK
    TO THE SAME NAMING CONVENTION. All prints should be named print_i where
    i is an integer between 1 and NUM_PRINTS inclusive. All closeup images of
    prints should be named print_i_closeup_j where j is either 1, 2, or 3. You
    can only have 3 closeup images per print.
    (3) If you're adding a print, you must modify the .scores attribute to
    accomodate the new print.
    (4) You must modify the function file_exists depending on where you store
    all of your prints. I suggest having a dedicated folder for all your
    fingerprint photos. All of my photos are in images/data_analysis_lab. You
    can change this to whatever you like.
    (5) If you're creating an importable print, set the scores attribute. If
    you're creating a non-importable print, you may optionally set the multiple
    choice question attribute.
"""

init python:
    import os
    from typing import Optional, List, Dict, Tuple

    pressed = ""
    print_imported = False
    imported_print = ""
    current_print = ""
    NUM_PRINTS = 7
    i = 0
    prints = {}
    
    class MCQ:
        """A custom data type representing a multiple choice question. This
        is used for the mcq attribute in Print.

        Preconditions:
        - 2 <= len(choices) <= 4
        """
        question: str
        choices: List[Tuple[str, bool]]
        responses: List[List[str]]
        __items__: Optional[List[Tuple[str, str]]]

        def __init__(self, question: str, choices: List[Tuple[str, bool]], responses: List[List[str]]) -> None:
            self.question = question
            self.choices = choices
            self.responses = responses
            self.__items__ = self.create_items()
        
        def create_items(self) -> List[Tuple[str, str]]:
            """Returns the items parameter for renpy.display_menu.
            """
            items = []
            for n in range(len(self.choices)):
                items.append((self.choices[n][0], n))
            return items
        
        def is_correct(self, choice: int) -> bool:
            if 0 <= choice < len(self.choices):
                return self.choices[choice][1]
            return False
            
        def say_responses(self, choice: int) -> None:
            for p in range(len(self.responses[choice])):
                renpy.say(None, self.responses[choice][p])

    class Print:
        """A custom data type representing a print registered in the fingerprint 
        analysis system. NON-IMPORTABLE PRINTS means prints that are supposed to be 
        built into the AFIS database and are NOT in your collected evidence bag.

        Instance Attributes:
            - image: Image name of fingerprint. The image's dimensions should be 
                roughly 431 x 578. 
            - closeup_1 (optional): A close-up image of the print
            - closeup_2 (optional): A second close-up image of the print
            - closeup_3 (optional): A third close-up image of the print
            - description (optional): 1-2 sentence description of person (or object) 
                that the print belongs to (or was recovered from)
            - scores: Required for NON-IMPORTABLE PRINTS. A dictionary mapping 
                the non-importable prints to their consistency score with this print
            - mcq (optional): This should only be used for NON-IMPORTABLE PRINTS. 
                This is a label that should jump to a multiple choice question related 
                to the print.
        """
        image: str
        processed: bool
        closeup_1: Optional[str]
        closeup_2: Optional[str]
        closeup_3: Optional[str]
        description: Optional[str]
        scores: Optional[Dict[str, Tuple[bool, float]]]
        mcq: Optional[MCQ]

        def __init__(self, image: str, closeup_1: str = "", closeup_2: str = "", closeup_3: str = "", description: str = "", scores: Dict[str, Tuple[bool, float]] = {}, mcq: MCQ = None):
            self.image = image
            self.processed = False
            self.closeup_1 = closeup_1
            self.closeup_2 = closeup_2
            self.closeup_3 = closeup_3
            self.description = description
            self.scores = scores
            self.mcq = mcq
        
        def process_print(self) -> None:
            self.processed = True
    
    def set_scores(print_name: str, scores: Dict[str, Tuple[bool, float]]) -> None:
        # if file_exists(print_name) and print_name in prints:
        prints[print_name].scores = scores
    
    def set_mcq(print_name: str, mcq: MCQ) -> None:
        # if file_exists(print_name) and print_name in prints:
        prints[print_name].mcq = mcq

    def file_exists(file_name: str) -> bool:
        """file_name has to end in .png
        """
        file_path = os.path.join(renpy.config.gamedir, "images/data_analysis_lab", file_name)

        if os.path.isfile(file_path):
            return True
        else:
            return False

    for k in range(1, NUM_PRINTS + 1):
        image = f"print_{k}"
        prints[image] = Print(image=image)
        for j in range(1, 4):
            closeup_filename = f"print_{k}_closeup_{j}.png"
            closeup = f"print_{k}_closeup_{j}"
            if file_exists(closeup_filename):
                if j == 1:
                    prints[image].closeup_1 = closeup
                elif j == 2:
                    prints[image].closeup_2 = closeup
                else: # j == 3
                    prints[image].closeup_3 = closeup
            else:
                continue
    
    var_scores = {"print_1": (True, 99), 
                "print_2": (False, 15), 
                "print_3": (False, 37),
                "print_4": (False, 46),
                "print_5": (False, 39),
                "print_6": (False, 28),
                "print_7": (False, 15)}

    set_scores(print_name="print_1", scores=var_scores)

    print_1_question = MCQ(
        question = "What kind of pattern is shown in the rightmost fingerprint?",
        choices = [("Checkered", False), ("Zigzags", False), ("Whorls", True)],
        responses = [["This is not a checkered pattern!", "Here's some extra text!", 
                    "And more!", "Try again!"],
                    ["This is not a zigzag pattern!", "Janna really likes Leon.", "And Connor!", "but most of all, she likes Simba!"],
                    ["This is a whorl! Good job!", "Let's finish the rest of the comparison."]]
    )

    set_mcq(print_name="print_1", mcq=print_1_question)

    print_6_question = MCQ(
        question = "What kind of pattern is shown in the righmost fingerprint?",
        choices = [("Double whorls", True), ("Whorls", False), ("Ripples", False)],
        responses = [["That's right!", "Isn't it cool?", "Let's move on."],
                    ["You're right, but there's something more!", "Do you see anything interesting about these whorls?", "Think about it some more and try again."],
                    ["They do look like ripples!", "but not quite!", "Let's try again."]]
    )

    set_mcq(print_name="print_6", mcq=print_6_question)

    var_scores = {"print_1": (False, 12), 
                "print_2": (False, 11), 
                "print_3": (False, 33),
                "print_4": (True, 91),
                "print_5": (False, 26),
                "print_6": (False, 32),
                "print_7": (False, 11)}
    
    set_scores(print_name="print_4", scores=var_scores)

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
        sensitive print_imported and i in range(1, 8)
        auto "afis_button_%s" at Transform(xpos=0.69, ypos=0.76)
        action Jump("compare")
    text "Compare" xpos 0.7 ypos 0.785 size 50

label computer:
    scene afis_plain_with_bar
    # if fingerprint.processed and oven.state != "finished":
    #     s "We've analyzed all available prints. We have no more business here."
    #     jump hallway
    # if oven.state == "off":
    #     s "Let's preheat the oven first - that way it can start heating up while we're analyzing prints."
    #     jump hallway
    # elif oven.state == "preheated" or oven.state == "baked": 
    #     s "Hold on. It looks like your oven has already [oven.state]. Let's check up on that first before we get started with analyzing prints."
    #     jump hallway
    # else:
    #     $ location = "afis"
    #     call screen afis
    $ location = "afis"
    call screen afis

label import_print:
    hide screen casefile_physical
    if not prints[imported_print].processed:
        show print_bg as print_bg_l at Transform(xpos=0.17, ypos=0.25) 
        show print_bg as print_bg_r at Transform(xpos=0.37, ypos=0.25)
        $ print_imported = True
        $ renpy.show(name="print_l", at_list=[Transform(xpos=0.175, ypos=0.25, zoom=0.83)], what=imported_print)
        call screen afis
    else:
        "We've already processed this print."
        call screen afis

label show_next:
    python:
        i = 1 if i == NUM_PRINTS else i + 1
        current_print = f"print_{i}"
        renpy.show(name="print_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen afis

label show_prev:
    python:
        i = NUM_PRINTS if i == 1 or i == 0 else i - 1
        current_print = f"print_{i}"
        renpy.show(name="print_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=current_print)
    call screen afis

label compare:
    python:
        renpy.hide_screen("back_button_screen")
        renpy.show(name="print_bg_l", at_list=[Transform(xpos=0.3, ypos=0.25)], what="print_bg")
        renpy.show(name="print_bg_r", at_list=[Transform(xpos=0.5, ypos=0.25)], what="print_bg")

        closeups_l = [prints[imported_print].closeup_1, prints[imported_print].closeup_2, prints[imported_print].closeup_3, prints[imported_print].image]
        closeups_r = [prints[current_print].closeup_1, prints[current_print].closeup_2, prints[current_print].closeup_3, prints[current_print].image]

        if closeups_l[0] != "":
            renpy.show(name="print_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25)], what=closeups_l[0])
        else:
            renpy.show(name="print_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25)], what=prints[imported_print].image)

        if closeups_r[0] != "":
            renpy.show(name="print_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25)], what=closeups_r[0])
        else:
            renpy.show(name="print_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25)], what=prints[current_print].image)
        renpy.pause(1.0)

label quiz:
    python:
        if prints[current_print].mcq is not None:
            renpy.say(None, prints[current_print].mcq.question)
            choice = renpy.display_menu(prints[current_print].mcq.__items__)
            prints[current_print].mcq.say_responses(choice)
            if prints[current_print].mcq.is_correct(choice):
                renpy.jump("show_results")
            else:
                renpy.jump("quiz")

label show_results:
    python:
        for m in range(1, 4):
            
            if closeups_l[0] != "":
                renpy.show(name="print_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25)], what=closeups_l[m])
            else:
                renpy.show(name="print_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25)], what=prints[imported_print].image)
            
            if closeups_r[m] != "":
                renpy.show(name="print_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25)], what=closeups_r[m])
            else:
                renpy.show(name="print_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25)], what=prints[current_print].image)
            renpy.pause(1.0)

    "[prints[imported_print].scores[current_print][1]]%% consistency."

    if prints[imported_print].scores[current_print][0]:
        $ prints[imported_print].process_print()
        "This looks like the print with the highest consistency!"
        if imported_print == "print_1":
            s "Who does this print belong to?"
            "According to the database... it belongs to a certain Dorag Deelar."
            s "Dorag Deelar, huh? I'll pass that information onto the officers."
            s "They can track him down for us."
            if oven.state == "preheating" or oven.state == "baking":
                s "Meanwhile, it looks like the oven is finished [oven.state]!"
                s "Why don't you have a look at it?"
                $ oven.update_state()
            $ fingerprint.process_evidence()
        else: # imported_print == "print_4"
            s "Who does this print belong to?"
            "Looks like it belongs to Mark Thompson."
            s "That's the victim's boyfriend. He was found unconscious at the scene."
            s "Currently, he's being held for questioning at the local precinct."
            s "We'll be sure to question him some more."
        $ print_imported = False
        $ imported_print = ""
        jump hallway
    else:
        $ renpy.show(name="print_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=closeups_r[m])
        jump import_print
        call screen afis