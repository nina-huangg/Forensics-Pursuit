"""
This .rpy file contains all code (screens and labels alike) related to the wet lab portion of the game. Notably, it contains the code for the DFO mixture process.
"""
init python:
    tool = ""

    class DFO:
        """A custom data type that represents a DFO mixture."""
        methanol: int
        dfo: float
        hfe: int
        acetic_acid: int

        def __init__(self, methanol: int = 0, dfo: float = 0, hfe: int = 0, acetic_acid: int = 0):
            self.methanol = methanol
            self.dfo = dfo
            self.hfe = hfe
            self.acetic_acid = acetic_acid

        def add_methanol(self, amount: int):
            self.methanol += amount
        
        def add_dfo(self, amount: float):
            self.dfo += amount

        def add_hfe(self, amount: int):
            self.hfe += amount
        
        def add_acetic_acid(self, amount: int):
            self.acetic_acid += amount
        
        def compare(self, mixture: "DFO"):
            return self.methanol == mixture.methanol and self.dfo == mixture.dfo and self.hfe == mixture.hfe and self.acetic_acid == mixture.acetic_acid

    # Initializing correct DFO mixture: 20mL methanol, 0.125g DFO, 470mL HFE-7100, and 10mL of acetic acid
    dfo_recipe = DFO(
        methanol = 20,
        dfo = 0.125,
        hfe = 470,
        acetic_acid = 10
    )

    # Initializing player's DFO mixture
    dfo_player = DFO()

    def tool_action(player_tool):
        """Used by screen dfo_bottle"""
        global tool
        tool = ""
        if player_tool == "methanol":
            renpy.jump("methanol")
        elif player_tool == "dfo":
            renpy.jump("dfo")
        elif player_tool == "acetic acid":
            renpy.jump("acetic acid")
        elif player_tool == "hfe":
            renpy.jump("hfe")

# Screens -----------------------------------------------------------------------------
screen toolbox_dfo():
    zorder 1
    hbox:
        xpos 0.86 ypos 0
        imagebutton:
            # sensitive methanol.available
            idle "methanol" at Transform(zoom=0.5)
            action Jump("methanol")
        text "Methanol" xpos 0.5 ypos 0.5 xanchor 0.5 yanchor 0.5

    hbox:
        xpos 0.89 ypos 0.27
        imagebutton:
            # sensitive dfo.available
            idle "dfo" at Transform(zoom=0.6)
            action Jump("dfo")
            
    hbox:
        xpos 0.86 ypos 0.45
        imagebutton:
            # sensitive acetic_acid.available
            idle "acetic acid" at Transform(zoom=0.6)
            action Jump("acetic_acid")

    hbox:
        xpos 0.88 ypos 0.72
        imagebutton:
            # sensitive hfe.available
            idle "hfe" at Transform(zoom=0.5)
            action Jump("hfe")

screen dfo_bottle:
    imagebutton:
        idle "dfo bottle" at Transform(zoom=2, xpos=0.3, ypos=0.3)
        # action Function(tool_action(tool))
        action [If(tool == "methanol", Jump("methanol")), If(tool == "dfo", Jump("dfo")), If(tool == "acetic acid", Jump("acetic_acid")), If(tool == "hfe", Jump("hfe"))]

# Labels -------------------------------------------------------------------------------
label fumehood:
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene fumehood
    call screen ui

label fumehood_label:
    hide screen casefile_physical
    hide screen ui

    if oven.state == "off":
        "Let's preheat the oven first before we do anything."
        hide dfo_bottle_opened
        hide dfo bottle
        jump materials_lab

    "Let's begin mixing the DFO!"
    show dfo_bottle_opened at Transform(zoom=2, xpos=0.3, ypos=0.3)
    call screen toolbox_dfo

label methanol:
    if dfo_player.methanol > 0:
        "There is currently [dfo_player.methanol] mL of methanol in the mixture."

    "How much methanol would you like to put in the mixture?"
    menu:
        "10 mL":
            "10 mL of methanol has been added to the mixture."
            $ dfo_player.add_methanol(10)
        "20 mL":
            "20 mL of methanol has been added to the mixture."
            $ dfo_player.add_methanol(20)
        "5 mL":
            "5 mL of methanol has been added to the mixture."
            $ dfo_player.add_methanol(5)

    if dfo_player.methanol > dfo_recipe.methanol:
        "I think I put too much methanol inside. I better restart."
        # TODO: need some kind of transition to show that we got a new bottle - possibly a black screen fade in/out with a message?
        $ dfo_player = DFO()

    jump mixture

label dfo:
    if dfo_player.dfo == dfo_recipe.methanol:
        "I think we have enough DFO inside."
        jump mixture

    "How much DFO would you like to put in the mixture?"
    menu:
        "1.25 g":
            "Too much! Let's rethink that."
            jump dfo
        "0.125 g":
            "Perfect!"
            $ dfo_player.add_dfo(0.125)
        "12.5 g":
            "WAY too much! Let's try this again."
            jump dfo
        "0.5 g":
            "A little too much! Let's try this again"
            jump dfo
    
    # Not a necessary piece of code - but it's here just in case
    if dfo_player.dfo > dfo_recipe.dfo:
        "I think I put too much DFO inside. I better restart."
        $ dfo_player = DFO()

    jump mixture

label hfe:
    if dfo_player.hfe > 0:
        "There is currently [dfo_player.hfe] mL of HFE in the mixture."

    "How much HFE would you like to put in the mixture?"
    menu:
        "100 mL":
            "100 mL of HFE has been added to the mixture."
            $ dfo_player.add_hfe(100)
        "200 mL":
            "200 mL of HFE has been added to the mixture."
            $ dfo_player.add_hfe(200)
        "50 mL":
            "50 mL of HFE has been added to the mixture."
            $ dfo_player.add_hfe(50)
        "20 mL":
            "20 mL of HFE has been added to the mixture."
            $ dfo_player.add_hfe(20)
    
    if dfo_player.hfe > dfo_recipe.hfe:
        "I think I put too much HFE inside. I better restart."
        $ dfo_player = DFO()

    jump mixture

label acetic_acid:
    if dfo_player.hfe > 0:
        "There is currently [dfo_player.acetic_acid] mL of acetic acid in the mixture."

    "How much acetic acid would you like to put in the mixture?"
    menu:
        "10 mL":
            "10 mL of acetic acid has been added to the mixture."
            $ dfo_player.add_acetic_acid(10)
        "5 mL":
            "5 mL of acetic acid has been added to the mixture."
            $ dfo_player.add_acetic_acid(5)
        "2 mL":
            "2 mL of acetic acid has been added to the mixture."
            $ dfo_player.add_acetic_acid(2)
        "3 mL":
            "3 mL of acetic acid has been added to the mixture."
            $ dfo_player.add_acetic_acid(3)

    if dfo_player.acetic_acid > dfo_recipe.acetic_acid:
        "I think I put too much acetic acid inside. I better restart."
        $ dfo_player = DFO()

    jump mixture

label mixture:
    if dfo_recipe.compare(dfo_player):
        hide screen toolbox_dfo
        "Perfect! Let's dip our label inside."
        # TODO: something that shows that we dipped our label - interactive portion or video
        "{color=#30b002}The label has been updated.{/color}"
        $ oven.update_state()
        "Looks like the oven is ready too!"
        hide dfo_bottle_opened
        jump materials_lab
    else:
        call screen toolbox_dfo

screen interactive_gin:
    imagebutton:
        auto "interactive gin %s" at Transform(xpos=0.325, ypos=0.2, zoom=1.7)
        action Jump("label_collected")

label fumehood_bottle:
    hide screen back_button_screen onlayer over_screens
    hide screen casefile_physical
    hide screen ui
    "Let's remove the label."
    call screen interactive_gin

label label_collected:
    show gin no label at Transform(xpos=0.2, ypos=0.2, zoom=1.7)
    show interactive label as interactive_label at Transform(xpos=0.5, ypos=0.2, zoom=1.5)
    "{color=#30b002}The label has been added to evidence.{/color}"
    $ gin.process_evidence()
    $ label.enable_evidence()
    jump fumehood