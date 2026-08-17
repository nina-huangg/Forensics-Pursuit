init -5 python:
    """
    I have made the decision not to include anything glove related. 
    
    The most frequently repeated mistake in playtesting was people forgetting to put gloves on or to change gloves between evidence items. 
    Initially I felt that this was an indication that testing for proper gloving was essential. In my mind it is simlar to taking photographs of 
    everything: an unglamorous step that is integral to ensuring that the integrity of evidence and your credibility as an investigator is maintained.

    With that said, I feel that there is no proper way to include gloving within the game as gloves are entirely tactile. By the very nature of video games,
    there is a diminishing of touch. Players cannot feel their hands getting sweaty in a pair of gloves or the sensation of grabbing an object and rendering
    the gloves unclean. In Ren'py especially, there is no body that the player can look at and they exist as naught but a crime solving ghostly apparition. 

    The issue can be simplified as a single implication: if you touch an item without gloves then you have contaminated it and made a mistake in the crime
    scene investigation. Given that the feeling of touch essentially does not exist within the game, this statement will always be vaccuously true rendering
    a gloving mechanic useless.

    There is likely a way to invoke the missing tactile sensation but I feel that Ren'py is poorly suited for such a task and that I lack the visual design
    elements to sucessfully execute such a task.


    from enum import Enum

    class GloveStatus(Enum):
        CLEAN = 1
        GLOVELESS = 0
        DIRTY_MAIN = -1
        DIRTY_ANGEL_HEAD = -2
        DIRTY_ANGEL_STATUES = -3
    
    def use_gloves():
        global clean_gloves
        renpy.notify("You have put a clean pair of gloves on.")
        clean_gloves = GloveStatus.CLEAN.value
        renpy.play("gloves.mp3")
    
    def glove_check():
        global clean_gloves
        if clean_gloves == -1:
            mistake_inventory.add_to_inventory(mistakes["Dirty Gloves"])
        elif clean_gloves == 0:
            mistake_inventory.add_to_inventory(mistakes["No Gloves"])
        else:
            clean_gloves = -1
    """

    import random


    #TODO I am pretty sure I can encapsulate the screen change logic with the Scene class itself. This would make the code a lot cleaner but 
    #I highkey don't feel like doing all that
    def use_camera():
        #This ordering ensures that if anything has been done to manipulate scene the initial scene photorgraph can no longer be captured allowing for a critical failure.
        if scenes[Scene.current].get_state("scale_bar"): scenes[Scene.current].set_state("scale_bar_photographed", True)
        elif scenes[Scene.current].get_state("dusted"): scenes[Scene.current].set_state("dusted_photographed", True)
        elif scenes[Scene.current].get_state("enhanced"): 
            scenes[Scene.current].set_state("enhanced_photographed", True)
            evidence.add_to_inventory(evies["Angel Statue Fingerprint Photo"])
        else: scenes[Scene.current].set_state("scene_photographed", True)

        renpy.play("camera_flash.mp3")

        #TODO Make the camera flash work with the new image map screens if you have the time
        #renpy.show_screen(Scene.current, at="camera_flash")

    def use_hungarian_red():
        if Scene.current is not "angel_head":
            renpy.notify("There is nothing to enhance here!")
        else:
            scenes[Scene.current].set_state("enhanced", True)
            scenes[Scene.current].background = "bg angel_head_enhanced"
    
    def collect_evidence():
        if renpy.invoke_in_new_context(renpy.confirm, "Are you certain you would like to bag this item and submit it for testing?"):
            if swabbing:
                evidence.add_to_inventory(evies["Blood Sample"])

                if not scenes[Scene.current].get_state("presumptive_test_attempt"):
                    mistake_inventory.add_to_inventory(mistakes["No Presuptive Test"])
                elif scenes[Scene.current].get_state("false_positive") and not scenes[Scene.current].get_state("correct_presumptive_test"):
                    mistake_inventory.add_to_inventory(mistakes["False Positive Collected"])
                elif not scenes[Scene.current].get_state("correct_presumptive_test"):
                    mistake_inventory.add_to_inventory(mistakes["Wrong Blood Test Order"])
                
                if scenes[Scene.current].get_state("test_swab_current"):
                    mistake_inventory.add_to_inventory(mistakes["Test Swab Collected"])
                
                if not scenes[Scene.current].get_state("right_swab"):
                    mistake_inventory.add_to_inventory(mistakes["Wrong Swab Type"])



                discard_swab()
            else:
                renpy.notify("You don't have anything to bag!")


    #
    #Fingerprinting Functions
    #
    def use_black_granular_powder():
        if Scene.current is not "angel_statues":
            renpy.notify("Click on the item that you want to dust first.")
        elif scenes[Scene.current].get_state("dusted"):
            renpy.notify("You have already dusted this item")
        else:
            #No photo of scene taken before dusting.
            if not scenes[Scene.current].get_state('scene_photographed'):
                mistake_inventory.add_to_inventory(mistakes["No Photo Scene"])

            scenes[Scene.current].set_state("dusted", True)
            scenes[Scene.current].set_state("right_dust", True)

            scenes[Scene.current].background = "bg angel_statues_dusted_black"
            scenes["bedroom_main"].background = "bg bedroom_statue_black"
    
    def use_white_granular_powder():
        if Scene.current is not "angel_statues":
            renpy.notify("Click on the item that you want to dust first.")
        elif scenes[Scene.current].get_state("dusted"):
            renpy.notify("You have already dusted this item")
        else:
            if not scenes[Scene.current].get_state('scene_photographed'):
                mistake_inventory.add_to_inventory(mistakes["No Photo Scene"])

            scenes[Scene.current].set_state("dusted", True)
            mistake_inventory.add_to_inventory(mistakes["Wrong Colour Dust"])

            scenes[Scene.current].background = "bg angel_statues_dusted_white"
            scenes["bedroom_main"].background = "bg bedroom_statue_white"

    
    def use_scalebar():
        if not scenes[Scene.current].get_state("right_dust"):
            renpy.notify("Do you see any fingerprints to scale?")
        else:
            if not scenes[Scene.current].get_state('dusted_photographed'):
                mistake_inventory.add_to_inventory(mistakes["No Picture Dusted Fingerprint"])

            scenes[Scene.current].set_state("scale_bar")

            scenes[Scene.current].background = "bg angel_statues_dusted_black_scale"
            scenes["bedroom_main"].background = "bg bedroom_statue_black_scale"

    def use_tape():
        if not scenes[Scene.current].get_state("dusted"):
            renpy.notify("There is nothing for the tape to pick up!")
        elif not scenes[Scene.current].get_state("right_dust"):
            renpy.notify("Do you see a fingerprint anywhere?")
        else:
            #We do not want to give the no photo scalebar error if they did not use one at all
            if not scenes[Scene.current].get_state("scale_bar"):
                mistake_inventory.add_to_inventory(mistakes["No Scale Bar"])
            elif not scenes[Scene.current].get_state("scale_bar_photographed"):
                mistake_inventory.add_to_inventory(mistakes["No Picture Scale Bar"])

            scenes[Scene.current].set_state("lifted")

            scenes[Scene.current].background = "bg angel_statues_lifted"
            scenes["bedroom_main"].background = "bg bedroom_statue_black_lifted"
    
    def use_backing_card():
        #This is where we add stuff to our inventories. We add things to the evidence and mistake inventories here. 
        if scenes[Scene.current].get_state("lifted"): evidence.add_to_inventory(evies["Angel Statue Fingerprint"])

        
    def use_backing_card_and_tape():
        use_tape()
        use_backing_card()
    
    #
    #Blood Sample Collection Functions
    #
    def use_swab_pack():
        global default_mouse
        global swabbing
        right = renpy.invoke_in_new_context(renpy.display_menu, [("Wet Swab", True), ("Dry Swab", False)])
        scenes[Scene.current].set_state("right_swab", right)
        default_mouse = "clean swab"
        swabbing = True

    def swab_something():
        global default_mouse
        if not scenes[Scene.current].get_state("scene_photographed"):
            mistake_inventory.add_to_inventory(mistakes["No Photo Scene"])

        scenes[Scene.current].set_state("swabbed", True)
        default_mouse = "red swab"
    
    def discard_swab():
        global default_mouse
        global swabbing
        default_mouse = "default"
        swabbing = False
        scenes[Scene.current].set_state("test_swab_current", False)
        scenes[Scene.current].set_state("right_swab", False)

    def begin_Kastle_Meyer():
        global testing

        if not swabbing:
            renpy.notify("You need a swab to test!")
        else:
            testing = True
    
    def add_reagent(attempt_list, reagent):
        attempt_list.append(reagent)
        check_Kastle_Meyer(attempt_list)
    
    def check_Kastle_Meyer(added: List[str]) -> None:
        global default_mouse
        print(added)

        if added == ['e','p','h'] and not default_mouse == "pink swab":
            scenes[Scene.current].set_state("correct_presumptive_test", True)
            default_mouse = "pink swab"
        elif added == ['e','p']:
            #False positive case:
            if random.randint(1,7) == 1:
                scenes[Scene.current].set_state("false_positive", True)
                default_mouse = "pink swab"
        elif len(added) >= 1:
            scenes[Scene.current].set_state("presumptive_test_attempt", True)
            scenes[Scene.current].set_state("test_swab_current", True)
    
    #This function is necesarry as calling a function as an Action by default updates screens which is needed to clos presumptive_testing
    def stop_test():
        global testing
        testing = False
    
transform camera_flash:
    matrixcolor TintMatrix("#ffffff") * BrightnessMatrix(0)
    linear 0.0 matrixcolor TintMatrix("#ccccff") * BrightnessMatrix(1)
    linear 0.4 matrixcolor TintMatrix("#ffffff") * BrightnessMatrix(0)

 
