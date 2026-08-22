define n = Character(name=("Nina"), image="nina_normal")

init python:
    import os
    from typing import Optional, List, Dict, Tuple

    pressed = ""
    print_imported = False
    imported_track = ""
    current_print = ""
    NUM_TRACKS = 3
    i = 3
    tracks = {}
    
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
                renpy.say(n, self.responses[choice][p])

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
        tracks[print_name].scores = scores
    
    def set_mcq(print_name: str, mcq: MCQ) -> None:
        # if file_exists(print_name) and print_name in prints:
        tracks[print_name].mcq = mcq

    def file_exists(file_name: str) -> bool:
        """file_name has to end in .png
        """
        file_path = os.path.join(renpy.config.gamedir, "images/data_analysis_lab", file_name)

        if os.path.isfile(file_path):
            return True
        else:
            return False
# ---------------------------------------------------------------------------------------
    """The code in this section defines all the fingerprints - importable and 
    non-importable! Feel free to play around with the existing code and/or 
    define more fingerprints here!
    """

    # This for loop defines all non-importable print classes!
    for k in range(1, NUM_TRACKS + 1):
        image = f"track_{k}"
        tracks[image] = Print(image=image)
        for j in range(1, 4):
            closeup_filename = f"track_{k}_closeup_{j}.png"
            closeup = f"track_{k}_closeup_{j}"
            if file_exists(closeup_filename):
                if j == 1:
                    tracks[image].closeup_1 = closeup
                elif j == 2:
                    tracks[image].closeup_2 = closeup
                else: # j == 3
                    tracks[image].closeup_3 = closeup
            else:
                continue
    
    """All code below defines/assigns the .mcq and .scores for the non-importable
    and importable prints respectively. Note that I define .mcq and .scores for
    print_1 because I use print_1 as both an importable and non-importable
    print for testing purposes.
    """
    # var_scores = {"print_1": (True, 99), 
    #             "print_2": (True, 98), 
    #             "print_3": (False, 37),
    #             "print_4": (False, 46),
    #             "print_5": (False, 39),
    #             "print_6": (False, 28),
    #             "print_7": (False, 15)}
    var_scores = {"track_1": (True, 99), 
                "track_2": (True, 98), 
                "track_3": (False, 37),}

    set_scores("track_2", {
        "track_1": (False, 60),
        "track_2": (True, 99), "track_3": (False, 37)
    })

    print_1_question = MCQ(
        question = "What kind of conclusion can you formulate when visually comparing these tire tracks?",
        choices = [("An elimination", False), ("An association", True), ("An individualization", False)],
        responses = [["An elimination (or exclusion) is when the class, wear, and/or individual characteristics do not sufficiently agree between the collected impression and the known shoe/tire.", "These tracks are too similar for an elimination.", "Give it another go!"],
                    ["Good job! An association can be drawn when the class, wear, and some individual characteristics agree between the collected impression and the known shoe/tire.", "But there are differences that prevent us from being certain that they agree overall. Results can range from likely to similar but lacking sufficient detail to be conclusive.", "Let's finish the rest of the comparison."],
                    ["An individualization is when the class, wear, and individual characteristics of the collected impression and the known shoe or tire sufficiently agree with no unexplainable differences.", "Do you think we can be completely certain of agreement, or should we be more conservative? Try again!"]]
    )

    # print_2_question = MCQ(
    #     question = "What kind of pattern is shown in the rightmost fingerprint?",
    #     choices = [("Whorl", False), ("Loop", True), ("Arch", False)],
    #     responses = [["This is not a whorl pattern!", "Give it another go!"],
    #                 ["This is a loop! Good job!", "Let's finish the rest of the comparison."],
    #                 ["This is not an arch pattern!", "Try again!"]]
    # )

    set_mcq(print_name="track_2", mcq=print_1_question)
    # set_mcq(print_name="print_2", mcq=print_2_question)

    # print_6_question = MCQ(
    #     question = "What kind of pattern is shown in the righmost fingerprint?",
    #     choices = [("Double whorls", True), ("Whorls", False), ("Ripples", False)],
    #     responses = [["That's right!", "Isn't it cool?", "Let's move on."],
    #                 ["You're right, but there's something more!", "Do you see anything interesting about these whorls?", "Think about it some more and try again."],
    #                 ["They do look like ripples!", "but not quite!", "Let's try again."]]
    # )

    # set_mcq(print_name="print_6", mcq=print_6_question)

    # var_scores = {"print_1": (False, 12), 
    #             "print_2": (False, 11), 
    #             "print_3": (False, 33),
    #             "print_4": (True, 91),
    #             "print_5": (False, 26),
    #             "print_6": (False, 32),
    #             "print_7": (False, 11)}
    
    # set_scores(print_name="print_4", scores=var_scores)

# ---------------------------------------------------------------------------------------

screen afis:
    imagebutton:
        auto "afis_button_%s" at Transform(xpos=0.18, ypos=0.76)
        action [SetVariable("pressed", "import"), ToggleScreen("inventory")]
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
        sensitive print_imported and i in range(1, 4)
        auto "afis_button_%s" at Transform(xpos=0.69, ypos=0.76)
        action [Hide("inventory"), Jump("compare")]
    text "Compare" xpos 0.7 ypos 0.785 size 50

screen analyzing:
    text "Analyzing..." xpos 0.425 ypos 0.785 size 50

label computer:
    scene afis_plain_with_bar
    # if fingerprint.processed and oven.state != "finished":
    #     n "We've analyzed all available prints. We have no more business here."
    #     jump hallway
    # if oven.state == "off":
    #     n "Let's preheat the oven first - that way it can start heating up while we're analyzing prints."
    #     jump hallway
    # elif oven.state == "preheated" or oven.state == "baked": 
    #     n "Hold on. It looks like your oven has already [oven.state]. Let's check up on that first before we get started with analyzing prints."
    #     jump hallway
    # else:
    #     $ location = "afis"
    #     call screen afis
    if tasks["Perform tire track analysis"]:
        n "We've analyzed all available tracks. We have no more business here."
        jump afis
    $ location = "afis"
    call screen afis

label import_print:
    hide screen inventory
    if not tracks[imported_track].processed:
        show print_bg as print_bg_l at Transform(xpos=0.17, ypos=0.25) 
        show print_bg as print_bg_r at Transform(xpos=0.37, ypos=0.25)
        $ print_imported = True
        $ renpy.show(name="track_l", at_list=[Transform(xpos=0.175, ypos=0.25, zoom=0.83, xysize=(432, 577))], what=imported_track)
        $ current_print = f"track_{i}"
        $ renpy.show(name="track_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83, xysize=(432, 577))], what=current_print)
        call screen afis
    else:
        n "We've already processed this track."
        call screen afis

label show_next:
    python:
        i = 1 if i == NUM_TRACKS else i + 1
        current_print = f"track_{i}"
        renpy.show(name="track_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83, xysize=(432, 577))], what=current_print)
    call screen afis

label show_prev:
    python:
        i = NUM_TRACKS if i == 1 or i == 0 else i - 1
        current_print = f"track_{i}"
        renpy.show(name="track_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83, xysize=(432, 577))], what=current_print)
    call screen afis

label compare:
    hide screen back_button_screen #onlayer over_screens
    show screen analyzing
    python:
        renpy.show(name="print_bg_l", at_list=[Transform(xpos=0.3, ypos=0.25)], what="print_bg")
        renpy.show(name="print_bg_r", at_list=[Transform(xpos=0.5, ypos=0.25)], what="print_bg")

        closeups_l = [tracks[imported_track].closeup_1, tracks[imported_track].closeup_2, tracks[imported_track].closeup_3, tracks[imported_track].image]
        closeups_r = [tracks[current_print].closeup_1, tracks[current_print].closeup_2, tracks[current_print].closeup_3, tracks[current_print].image]

        if closeups_l[0] != "":
            renpy.show(name="track_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25, xysize=(432, 577))], what=closeups_l[0])
        else:
            renpy.show(name="track_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25, xysize=(432, 577))], what=tracks[imported_track].image)

        if closeups_r[0] != "":
            renpy.show(name="track_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25, xysize=(432, 577))], what=closeups_r[0])
        else:
            renpy.show(name="track_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25, xysize=(432, 577))], what=tracks[current_print].image)
        renpy.pause(1.0)

label quiz:
    python:
        if tracks[current_print].mcq is not None:
            renpy.say(None, tracks[current_print].mcq.question)
            choice = renpy.display_menu(tracks[current_print].mcq.__items__)
            tracks[current_print].mcq.say_responses(choice)
            if tracks[current_print].mcq.is_correct(choice):
                renpy.jump("show_results")
            else:
                renpy.jump("quiz")

label show_results:
    python:
        for m in range(1, 4):
            
            if closeups_l[0] != "":
                renpy.show(name="track_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25, xysize=(432, 577))], what=closeups_l[m])
            else:
                renpy.show(name="track_l", at_list=[Transform(zoom=0.83, xpos=0.3, ypos=0.25, xysize=(432, 577))], what=tracks[imported_track].image)
            
            if closeups_r[m] != "":
                renpy.show(name="track_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25, xysize=(432, 577))], what=closeups_r[m])
            else:
                renpy.show(name="track_r", at_list=[Transform(zoom=0.83, xpos=0.5, ypos=0.25, xysize=(432, 577))], what=tracks[current_print].image)
            renpy.pause(1.0)

    hide screen analyzing
    # "[tracks[imported_track].scores[current_print][1]]%% consistency."
    # we don't really say things like xx% consistency and we should avoid this. This is why we ask the player to draw their own conclusion

    if tracks[imported_track].scores[current_print][0]:
        $ tracks[imported_track].process_print()
        # "This looks like the print with the highest consistency!"
        if imported_track == "track_2":
            n "According to the database... this is a silver 2006 Dodge Durango SLT."
            n "I'll pass that information onto the officers."
            $ fingerprint_tasks["track_analyzed"] = True
            $ custom_notify("Analyzed the tire track!", True)
        # elif imported_track == "print_2":
        #     n "Looks like this print belongs to Peter Painter."
        #     $ fingerprint_tasks["fingerprint_2_analyzed"] = True
        #     $ custom_notify("Analyzed one fingerprint!", True)
        $ print_imported = False
        $ imported_track = ""
        $ hide_afis()
        hide track_l
        hide track_r
        hide print_bg_l
        hide print_bg_r
        hide screen afis_screen
        jump impression_station
    else:
        "These tracks are not the most visually similar ones available to you. Try another one!"
        $ renpy.show(name="track_r", at_list=[Transform(xpos=0.375, ypos=0.25, zoom=0.83)], what=closeups_r[m])
        jump import_print
        call screen afis
