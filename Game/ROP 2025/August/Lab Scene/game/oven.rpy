init python:
    class Oven:
        """A custom data type representing the various states of the oven.
        The oven state is one of the following:
            (1) off
            (2) preheating
            (3) preheated
            (4) baking
            (5) baked
            (6) finished
        
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
                self.state = "finished"
                self.in_use = False
    
    oven = Oven()

screen oven:
    python:
        if oven.state == "off" or oven.state == "finished":
            background = "oven_closed_normal_%s"
        elif oven.state == "preheating" or oven.state == "baking":
            background = "oven_closed_baking_%s"
        elif oven.state == "preheated" or oven.state == "baked":
            background = "oven_closed_complete_%s"

    imagemap:
        auto background

        hotspot (757, 569, 371, 224) action [If(oven.state == "off", Jump("preheat")),
                                            If(oven.state == "preheated", Jump("bake")),
                                            If(oven.state == "baked", Jump("label_baked"))]
    


label oven:
    show screen back_button_screen('materials_lab') onlayer over_screens
    $ hide_all_inventory()
    if oven.in_use:
        scene oven_closed_baking_idle
        s normal3 "The oven isn't finished [oven.state] yet. Let's come back another time."
        jump materials_lab
    elif not label.dipped and oven.state == "preheated":
        scene oven_closed_normal_idle
        s normal2 "The oven is ready for baking - but our label isn't."
        s normal3 "You should go to the fumehood and dip this label in DFO - which you'll have to make yourself, of course."
        jump materials_lab
    elif oven.state == "finished":
        scene oven_closed_normal_idle
        s normal3 "We have no more business with the oven."
        jump materials_lab
    call screen oven

label preheat:
    hide screen back_button_screen onlayer over_screens
    scene oven_closed_normal_idle
    s normal1 "Let's set the time between 0h00 and 1h00 and the temperature between 200 and 300."
    hide screen oven
    scene black
    $ correct_time_start = "000"
    $ correct_time_end = "100"
    $ correct_temp_start = "200"
    $ correct_temp_end = "300"
    $ correct_label = "preheat_confirmed"
    call screen main_interface

label preheat_confirmed:
    scene oven_closed_normal_idle
    $ oven.update_state() # to preheating
    scene baking_in_progress
    s happy2 "Excellent!"
    if not gin.processed or not fingerprint.processed:
        s normal1 "Let's do something else while waiting."
        jump materials_lab
    else:
        s normal1 "We've already finished analyzing the other pieces of evidence."
        s normal1 "Looks like we'll have to wait this out."
        "10 minutes later..."
        scene baking_complete
        $ oven.update_state() # to preheated
        "Ding!"
        s happy2 "The oven's ready!"
        jump bake

label bake:
    hide screen back_button_screen onlayer over_screens
    scene oven open empty
    if not label.dipped:
        scene baking_complete
        s normal2 "The oven is ready for baking - but our label isn't."
        s normal3 "You should go to the fumehood and dip this label in DFO - which you'll have to make yourself, of course."
        jump materials_lab
    else:
        s normal1 "Let's place our label inside."
        show screen back_button_screen('materials_lab') onlayer over_screens
        call screen full_inventory    
        call screen ui

label label_placed_in_oven:
    scene oven open before preheat
    hide screen back_button_screen onlayer over_screens
    $ hide_all_inventory()
    s normal1 "Let's close this up."
    scene oven_closed_normal_idle

label set_timer:
    hide screen back_button_screen onlayer over_screens
    s normal1 "Let's set the time for 10 minutes and the temperature in between 100 and 200."
    $ correct_time_start = "010"
    $ correct_time_end = "011"
    $ correct_temp_start = "100"
    $ correct_temp_end = "200"
    $ correct_label = "time_set"
    call screen main_interface

label time_set:
    $ oven.update_state() # to baking
    s normal1 "That's right."
    if not gin.processed or not fingerprint.processed:
        s normal1 "Let's do something else while waiting."
        jump materials_lab
    else:
        s happy2 "We've finished processing the rest of our evidence."
        s normal1 "Now all we need to do is wait."
        "10 minutes later..."
        $ oven.update_state()
        "Ding!"
        s happy2 "Looks like it's ready to take out!"
        jump label_baked


label label_baked:
    hide screen back_button_screen onlayer over_screens
    scene oven open after preheat
    s normal3 "Wow, this looks great!"
    $ label.image = "baked label %s"
    $ label.process_evidence()
    "The label has been updated."
    $ oven.update_state() # to finished
    $ removeInventoryItem(inventory_sprites[inventory_items.index("label")])
    $ addToInventory(["baked_label"])
    s normal1 "Let's run this through AFIS."
    jump materials_lab
