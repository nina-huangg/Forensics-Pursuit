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
label IPC:
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene wet_lab
    call screen full_inventory
    call screen ui

    if not dfo_player.methanol and not dfo_player.dfo and not dfo_player.hfe and not dfo_player.acetic_acid:
        s normal3 "First, we need to gather our materials."
        jump materials_lab
    else:
        jump fumehood

label grinder:
    show screen back_button_screen('materials_lab') onlayer over_screens
    
    if bowl.completed():
        $ hide_all_inventory()
        $ ready_to_mix = False
        s normal3 "We have no more business with the fumehood."
        jump materials_lab

    show screen grinder
    call screen full_inventory
    hide screen grinder
    call screen ui


label fumehood:
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene fumehood
    
    if bowl.completed():
        $ hide_all_inventory()
        $ ready_to_mix = False
        s normal3 "We have no more business with the fumehood."
        jump materials_lab

    call screen full_inventory
    call screen ui

label fumehood_label:
    hide screen casefile_physical
    hide screen ui

    if oven.state == "off":
        s normal2 "Let's preheat the oven first before we do anything."
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
        s "Perfect! Let's dip our label inside."
        # TODO: something that shows that we dipped our label - interactive portion or video
        "The label has been updated."
        $ oven.update_state()
        s "Looks like the oven is ready too!"
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
    s normal1 "Let's remove the label."
    call screen interactive_gin

label label_collected:
    show gin no label at Transform(xpos=0.2, ypos=0.2, zoom=1.7)
    show interactive label as interactive_label at Transform(xpos=0.5, ypos=0.2, zoom=1.5)
    "The label has been added to evidence."
    $ removeInventoryItem(inventory_sprites[inventory_items.index("gin")])
    $ addToInventory(["label"])
    $ gin.process_evidence()
    $ label.enable_evidence()
    jump fumehood

label grinder_pills:
    hide screen back_button_screen onlayer over_screens
    hide screen casefile_physical
    hide screen ui
    s normal1 "Let's grind these pills to analyze them."
    # 直接跳转到动画/研磨过程，不需要玩家点击
    jump pills_grinded

label pills_grinded:
    hide screen grinder
    show expression "materials_lab/grinder_idle.png"
    with dissolve
    pause 0.5
    # 首先显示药丸从上方掉落的动画
    show expression "materials_lab/pill.png" at Transform(xpos=734, ypos=645)
    with dissolve
    
    # 药丸掉落动画
    show expression "materials_lab/pill.png" at Transform(xpos=725, ypos=796):
        linear 1.0 ypos 796
    
    pause 1.5
    
    # 显示研磨工具
    show expression "materials_lab/grinder_tool.png" at Transform(xpos=717, ypos=598)
    with dissolve
    
    # 研磨动画 - 上下磨动
    show expression "materials_lab/grinder_tool.png":
        xpos 717 ypos 598
        # 左边上下一下
        linear 0.3 xpos 700 ypos 620
        linear 0.3 xpos 700 ypos 598
        # 右边上下一下  
        linear 0.3 xpos 734 ypos 620
        linear 0.3 xpos 734 ypos 598
        # 再来几次研磨动作
        linear 0.2 xpos 710 ypos 615
        linear 0.2 xpos 710 ypos 598
        linear 0.2 xpos 730 ypos 615
        linear 0.2 xpos 730 ypos 598
        linear 0.2 xpos 717 ypos 610
        linear 0.2 xpos 717 ypos 598
    
    pause 3.0
    
    # 隐藏原来的药丸和工具，显示研磨后的粉末
    hide expression "materials_lab/pill.png"
    hide expression "materials_lab/grinder_tool.png"
    # show grinded_pills at Transform(xpos=0.4, ypos=0.3, zoom=1.5)
    # with dissolve
    
    s normal1 "The pills have been ground into powder for analysis."
    $ removeInventoryItem(inventory_sprites[inventory_items.index("pills")])
    $ addToInventory(["grinded_pills"])
    $ pills.process_evidence()
    $ grinded_pills.enable_evidence()
    s normal1 "Powder ready for further analysis."
    jump grinder

label bottle_filling:
    hide screen back_button_screen onlayer over_screens
    hide screen casefile_physical
    hide screen ui
    s normal1 "Let's put the powder into a bottle for storage."
    # 直接跳转到倒粉末动画
    jump powder_pouring

label powder_pouring:
    hide screen grinder
    show expression "materials_lab/scale_and_grinder_empty.png"
    with dissolve
    pause 0.5
    
    # 显示粉末在起始位置
    show expression "materials_lab/Inventory-grinded_pills.png" at Transform(xpos=847, ypos=562) zorder 100
    with dissolve
    
    # 显示瓶子在起始位置
    show expression "materials_lab/teflon.png" at Transform(xpos=959, ypos=687) zorder 101
    with dissolve
    
    pause 1.0
    
    # 粉末倾斜倒入动画 - 模拟粉末向瓶子倾斜
    show expression "materials_lab/Inventory-grinded_pills.png" at Transform(xpos=847, ypos=562) zorder 100:
        # 粉末开始倾斜，向瓶子方向移动并旋转
        linear 0.5 xpos 900 ypos 600 rotate 15
        linear 0.5 xpos 950 ypos 630 rotate 30
        linear 0.8 xpos 959 ypos 650 rotate 45
    
    pause 2.0

    hide expression "materials_lab/Inventory-grinded_pills.png"
    
    # 倒完后瓶子向左移动
    show expression "materials_lab/teflon.png" at Transform(xpos=959, ypos=687) zorder 101:
        linear 1.0 xpos 1216 ypos 687
    
    pause 1.5
    
    # 隐藏粉末（已经倒入瓶子）
    hide expression "materials_lab/Inventory-grinded_pills.png"
    
    # 显示装满粉末的瓶子（如果有这样的图片的话）
    # show expression "materials_lab/teflon_filled" at Transform(xpos=1216, ypos=687) zorder 101
    
    s normal1 "The powder has been successfully stored in the bottle."
    $ removeInventoryItem(inventory_sprites[inventory_items.index("grinded_pills")])
    $ bottled_powder.enable_evidence()
    s normal1 "Sample is ready for further testing."
    s normal1 "Now let's proceed to the digestion process."
    jump digestion

label digestion:
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene expression "materials_lab/digestion_idle.png"
    $ location = "digestion"
    $ ready_to_digest = True
    
    "Click on the toolbox items to add reagents to the Teflon digestion vessel."
    
    show screen digestion
    call screen full_inventory
    hide screen digestion
    call screen ui

# Digestion reagent pouring animations
label pour_nitric_acid:
    hide screen digestion
    show expression "materials_lab/digestion_idle.png"
    $ digestion_vessel_x = 539
    $ digestion_vessel_y = 182
    
    # Show the bottle moving to the vessel
    show expression "Toolbox Items/toolbox-nitric_acid.png" as nitric_bottle:
        zoom 2
        xpos 100 ypos 100 
        linear 2.0 xpos digestion_vessel_x ypos digestion_vessel_y - 100
        linear 1.0 rotate 45  # Tilt for pouring
        
    
    "Adding 4 mL of nitric acid to the digestion vessel..."
    
    # Pouring effect
    show expression "images/liquid_pour.png" as pour_effect:
        xpos digestion_vessel_x ypos digestion_vessel_y - 50
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide nitric_bottle
    hide pour_effect
    
    # Mark nitric acid as added
    $ reagents_added["nitric_acid"] = True
    
    # Check if all reagents are added
    python:
        if check_all_reagents_added():
            addToInventory(["teflon_pills"])
            renpy.say(None, "All reagents added! Teflon digestion vessel is ready for microwave digestion.")
            renpy.jump("mds")
    
    jump digestion

label pour_hydrofluoric_acid:
    hide screen digestion
    show expression "materials_lab/digestion_idle.png"

    $ digestion_vessel_x = 539
    $ digestion_vessel_y = 182
    
    # Show the bottle moving to the vessel
    show expression "Toolbox Items/toolbox-hydrofluoric_acid.png" as hf_bottle:
        zoom 2
        xpos 150 ypos 100
        linear 2.0 xpos digestion_vessel_x ypos digestion_vessel_y - 100
        linear 1.0 rotate 45  # Tilt for pouring
    
    "Adding 0.5 mL of hydrofluoric acid to the digestion vessel..."
    
    # Pouring effect (smaller amount)
    show expression "images/liquid_pour.png" as pour_effect:
        xpos digestion_vessel_x ypos digestion_vessel_y - 50
        alpha 0.0
        linear 0.3 alpha 0.8
        linear 1.0 alpha 0.8
        linear 0.3 alpha 0.0
    
    hide hf_bottle
    hide pour_effect
    
    # Mark hydrofluoric acid as added
    $ reagents_added["hydrofluoric_acid"] = True
    
    # Check if all reagents are added
    python:
        if check_all_reagents_added():
            addToInventory(["teflon_pills"])
            renpy.say(None, "All reagents added! Teflon digestion vessel is ready for microwave digestion.")
            renpy.jump("mds")
    
    jump digestion

label pour_hydrogen_peroxide:
    hide screen digestion
    show expression "materials_lab/digestion_idle.png"
    $ digestion_vessel_x = 539
    $ digestion_vessel_y = 182
    
    # Show the bottle moving to the vessel
    show expression "Toolbox Items/toolbox-hydrogen_peroxide.png" as h2o2_bottle:
        zoom 2
        xpos 200 ypos 100
        linear 2.0 xpos digestion_vessel_x ypos digestion_vessel_y - 100
        linear 1.0 rotate 45  # Tilt for pouring
    
    "Adding 2 mL of hydrogen peroxide to the digestion vessel..."
    
    # Pouring effect (medium amount)
    show expression "images/liquid_pour.png" as pour_effect:
        xpos digestion_vessel_x ypos digestion_vessel_y - 50
        alpha 0.0
        linear 0.4 alpha 0.9
        linear 1.5 alpha 0.9
        linear 0.4 alpha 0.0
    
    hide h2o2_bottle
    hide pour_effect
    
    # Mark hydrogen peroxide as added
    $ reagents_added["hydrogen_peroxide"] = True
    
    # Check if all reagents are added
    python:
        if check_all_reagents_added():
            addToInventory(["teflon_pills"])
            renpy.say(None, "All reagents added! Teflon digestion vessel is ready for microwave digestion.")
            renpy.jump("mds")
    
    jump digestion