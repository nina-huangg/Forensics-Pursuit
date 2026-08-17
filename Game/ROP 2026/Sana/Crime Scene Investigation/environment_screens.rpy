init python: 
    class Scene:
        #Hardcoded but okay because we always start from main bedroom
        current = "bedroom_main"

        def __init__(self, name: str, background: str = None, states: dict = {}):
            self.name = name
            self.background = background
            self.states = {"scene_photographed": False}
            self.states.update(states)

        def set_state(self, key, value=True):
            if key not in self.states:
                return

            self.states[key] = value

        def get_state(self, key, default=False):
            return self.states.get(key, default)

        @staticmethod
        def set_current(scene_name):
            Scene.current = scene_name
    

default scenes = {
    "bedroom_main": 
        Scene(
            "bedroom_main", 
            background="bg bedroom", 
            states={
                "swabbed": False,
                "right_swab": False,
                "presumptive_test_attempt": False,
                "correct_presumptive_test": False,
                "false_positive": False,
                "test_swab_current": False
            }
            ),

    "angel_statues": 
        Scene(
            "angel_statues", 
            background="bg angel_statues", 
            states={ 
                "dusted": False, 
                "right_dust": False,
                "dusted_photographed": False, 
                "scale_bar": False, 
                "scale_bar_photographed": False,
                "lifted": False,
                }
            ),

    "angel_head": 
        Scene(
            "angel_head", 
            background="bg angel_head",
            states={
                "examined": False,
                "enhanced": False,
                "enhanced_photographed": False,
                "swabbed": False
            }
            )
    }

"""
This variable is how the game will be able to tell if the player has a swab equipped. I wanted to tie this check to what the mouse pointer was
but the value of that variable, mouse.config, cannot be directly accessed from within the game.

After further examination there is a function that does exactly what I wanted making this variable redundant.

After further, further, playtesting, the current mouse changes when you are hovering over a button. This is an issue if you want to interact with a hotspot 
while swabbing is on going. Thus, we must have a swabbing variable.
"""
default swabbing = False
default testing = False


screen main():
    """
    I've addded this screen to help make the visual parts of the game more modular. For example, the bedroom_screen previously implemented 
    the interactable hotspots and also used the leave_button. While this is fine, I found that it made implementing the presumptive test portion
    more difficult as I wanted to only have the interactable hotspots without the leave button. In other words, there was high coupling between the 
    two screens.

    The solution was to add this new screen. In this way every single screen has a single responsibility. The leave_button is responsible for ending the
    game, the bedroom_main screen is responsible for implementing user interaction with the environment, and the main screen is the top screen that controls
    everything that is being show to the player.

    I went back to the CSC207 notes to try understanding what kind of design pattern this was. If I am not mistaken, this screen will essentially be the 
    view of the clean architecture engine. The ViewModel of my program would then be the Scene class. By definition a view model stores the information
    that the view must acess to display something. In this case, that information would be the variable Scene.current.
    
    I should mention that the Scene class does violate the SRP as it is also a member of the entity layer and stores all temporary information on player
    progress trough the level, Additionally, the swabbing variable should ideally be an attribute of the view model class as it is also used to determine what is 
    displayed; however, given how little information is required by the view model and the limited scope of this project, I see no point in 
    refactoring to address these issues :)
    """
    #The nice thing about this single line is that I never need to explicitly show or hid an environment scene again. 
    #All that is required is a change to Scene.current!
    use expression Scene.current

    
    """
    In addition to the above, there are a few more really convenient things about moving this logic here:

        - 1: In my mind, the back_button and leave_button are analgous to one another. They both take the use a step out of where they are
        currently and are both displayed in the top right. Previously, I had to split the usage of this button in every single environment screen.
        By centralizing the logic, this relationship is made far more clear.

        - 2: Previously I had to explicitly control every single bedroom screen. This meant using a show statement every time the user clicked on the
        relevant hotspot and a hide statement when they used the back button. Furthermore, to make this hide statement work, the back button needed a parameter
        that represented what screen should be hidden. Encapsulating the logic of screen changes behind the use expression above allowed me to avoid
        copy pasting use statements in every class and allowed me to remove that extra parameter from the back_button screen!
    """ 
    vbox:
        at topright

        if Scene.current != "bedroom_main":
            use back_button

        if testing:
            use presumptive_testing
        elif swabbing:
            use discard_swab_button
        elif Scene.current == "bedroom_main":
            use leave_button
        

screen bedroom_main():
    imagemap:
        #ground "bg bedroom_idle.png"
        idle scenes["bedroom_main"].background
        hover "bg bedroom_hover"

        hotspot (1044, 241, 79, 78) action Function(Scene.set_current,"angel_statues")
        hotspot (382, 655, 282, 180) action If(swabbing, Function(swab_something), Notify("A dried blood pool"))
        hotspot (1335, 874, 20, 16) action [Function(Scene.set_current,"angel_head"), Function(scenes["angel_head"].set_state, "examined")]

screen angel_statues():
    imagemap:
        #ground "bg bedroom_idle.png"
        idle scenes["angel_statues"].background
        hover "bg bedroom_hover"
    
screen angel_head():
    imagemap:
        #ground "bg bedroom_idle.png"
        idle scenes["angel_head"].background
        hover "bg bedroom_hover"
    

screen back_button():
    imagebutton:
        idle "back_button"
        hover "back_button_hover"
        #Horrendous hardcode for the Scene.set_current but we do not have to worry about scalability :)
        action Function(Scene.set_current,"bedroom_main")

screen discard_swab_button():
    imagebutton:
        idle "images/Environment Items/garbage_idle.png"
        hover "images/Environment Items/garbage_hover.png"
        action Confirm("Are you sure you want to throw away the swab you are currently holding?", Function(discard_swab))

screen presumptive_test_button():
    frame:
        textbutton "Test Swab":
            action Confirm("Run presumptive test on this swab?", Function(discard_swab))

screen collect_swab_button():
    frame:
        textbutton "Collect Swab":
            action Confirm("Place swab in collection tube and add to evidence?", Function(discard_swab))


screen leave_button():
    frame:
        textbutton "Leave the Scene?":
            action Confirm("Are you sure you want to leave and conclude the crime scene investigation?", Jump("review_mistakes"))


screen mistake_screen():
    grid 3 7:
        at top
        yoffset 100
        spacing 30  

        for i, item in enumerate(mistake_inventory._inventory):
                use inventory_slot(item)
        
    use restart_game()


screen restart_game():
    imagebutton:
        xpos 1700
        ypos 0
        idle "back_button"
        hover "back_button_hover"

        action MainMenu()


screen presumptive_testing():
    """
    This screen is where the presumptive test will be implemented. There will be four image buttons. Three for the 
    Kastle-meyer reagents and one return button. 
    
    I will not allow the player to make the mistake of adding too much of a reagent as this quantitative error is hard 
    to accurately represent. I will allow them to make the mistake of doing the procedure in the wrong order and allow
    for a false positive to occur. These will be implemented by making each button interactable with once and having a colour
    change after adding the phenophtahlin. 
    """
    default curr_attempt = []

    vbox:
        imagebutton: 
            idle "images/Environment Items/x_idle.png" 
            hover "images/Environment Items/x_hover.png"
            action Function(stop_test)
        imagebutton:
            idle "images/Environment Items/ethanol_idle.png" 
            hover "images/Environment Items/ethanol_hover.png"
            action [Function(add_reagent, curr_attempt, 'e'), SetLocalVariable("sensitive", False)]
        text "Ethanol"
        imagebutton: 
            idle  "images/Environment Items/reagent_idle.png" 
            hover "images/Environment Items/reagent_hover.png"
            action [Function(add_reagent, curr_attempt, 'p'), SetLocalVariable("sensitive", False)]
        text "Phenolphthalin"
        imagebutton: 
            idle "images/Environment Items/hydrogen_peroxide_idle.png" 
            hover "images/Environment Items/hydrogen_peroxide_hover.png"
            action [Function(add_reagent, curr_attempt, 'h'), SetLocalVariable("sensitive", False)]
        text "Hydrogen Peroxide"
        

screen environment_tester():
    #For the past three weeks I have tried and failed to make a simple variable change work after using one of the items.
    #Or so I thought. I was checking by using the built in renpy console that is brought up by shift+o. The issue is,
    #That stupid thing for some reason does not reflect changes made to global variables within functions. 
    #If you want to ensure that a function does change what you want it to...USE A KEY LIKE BELOW.
    zorder 100
    
    key "d" action Function(lambda: renpy.notify(f"{scenes[Scene.current].get_state('dusted')}"))
    key "g" action Function(lambda: renpy.notify(f"{clean_gloves}"))
    key "s" action Function(lambda: renpy.notify(f"{scenes[Scene.current].states}"))
    key "m" action Function(lambda: renpy.notify(f"{mistake_inventory._inventory}"))
    key "b" action Function(lambda: renpy.notify(f"{swabbing}"))
    key "t" action Function(lambda: renpy.notify(f"{testing}"))







