init python:
    class Oven:
        """A custom data type representing the various states of the oven.
        The oven state is one of the following:
            (1) off
            (2) preheating
            (3) preheated
            (4) baking
            (5) baked
        
        When the oven is in states (2) or (4), in_use is True.
        """
        state: str
        in_use: bool
        
        def __init__(self) -> None:
            self.state = "off"
            self.in_use = False

        def update_state(self) -> None:
            if self.state == "off":
                self.state = "preheating"
                self.in_use = True
            elif self.state == "preheating":
                self.state = "preheated"
                self.in_use = False
            elif self.state == "preheated":
                self.state = "baking"
                self.in_use = True
            elif self.state == "baking":
                self.state = "baked"
                self.in_use = False
            # May omit else altogether since it could proc the preheating after baking
            else: # oven.state == baked
                self.state = "off"
                self.in_use = False
    
    oven = Oven()

screen oven:
    imagemap:
        auto "oven_closed_%s"

        hotspot (474, 28, 965, 790) action [If(oven.state == "off", Jump("preheat")),
                                            If(oven.state == "preheated", Jump("bake")),
                                            If(oven.state == "baked", Jump("label_baked"))]

label oven:
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene oven_closed_idle
    if oven.in_use:
        "The oven isn't finished [oven.state] yet. Let's come back another time."
        jump materials_lab
    call screen oven

label preheat:
    scene oven_closed_idle
    "What temperature would you like to preheat the oven to?"
    menu:
        "100 F":
            "That's not quite right..."
            jump preheat
        "100 C":
            "Excellent!"
            "Let's do something else while waiting."
            $ oven.update_state()
            jump materials_lab
        "300 C":
            "This is way too high!"
            jump preheat

label bake:
    scene oven open empty
    "Let's place our label inside."
    call screen ui

label label_placed_in_oven:
    scene oven open before preheat
    "Let's close this up."
    scene oven_closed_idle

label set_timer:
    "What would you like to set the cooking time to?"
    menu:
        "10 minutes":
            $ oven.update_state() # to baking
            jump materials_lab
            if fingerprint.processed:
                "Now all we need to do is wait."
                "{color=#30b002}10 minutes later...{/color}"
                $ oven.update_state()
                "{color=#30b002}Ding!{/color}"
                "Looks like it's ready to take out!"
                jump label_baked
        "100 minutes":
            "Added an extra zero there..."
            jump set_timer
        "1 hour":
            "What made you think that?!"
            jump set_timer

label label_baked:
    scene oven open after preheat
    "Wow, this looks great!"
    $ label.image = "baked label %s"
    $ label.process_evidence()
    "{color=#30b002}The label has been updated.{/color}"
    call screen ui
    jump materials_lab
