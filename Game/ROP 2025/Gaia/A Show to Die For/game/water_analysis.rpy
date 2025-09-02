"""
This file contains all labels and functions related to the water analysis once it's been clicked on
"""

            
## ─── the interactive scene ────────────────────────────────────
screen water_scene():
    modal True
    tag water_scene

    add "images/water_scene/water_bg.JPG" at full_screen_crop_top

    on "show" action If(
        not encountered.get("water", False),
        Jump("first_time_water"),
        NullAction()
    )

    imagebutton:
        idle   "images/water_scene/water.png"
        hover  "images/water_scene/water_hover.png"
        at Transform(zoom=0.65)
        xpos      610 ypos 240
        action If(
            # 1) If they aren’t gloved yet, prompt them
            not asked["water_glove"],
            Notify("You need to put on protective gloves first."),
            # 2) Otherwise, if they have a dropper, fill it
            If(
                default_mouse == "dropper",
                [
                    SetVariable("default_mouse", "dropper_filled"),
                    Hide("water_scene"),
                    Show("glass_vial_popup"),
                ],
                # 3) If they are gloved but don't have the dropper
                Notify("What tool can you use to collect a sample of the water?")
            )
        )
        
screen glass_vial_popup():
    modal True
    tag glass_vial_popup

    text "Choose a container:" xalign 0.5 yalign 0.3 size 32 color "#FFF"

    hbox:
        xalign 0.5 yalign 0.5
        spacing 80

        # Glass vial button
        imagebutton:
            idle  "images/water_scene/glass_vial_open.png"
            hover "images/water_scene/glass_vial_open_hover.png"
            at Transform(zoom=0.8)
            action If(
                default_mouse == "dropper_filled",
                [
                    Hide("glass_vial_popup"),
                    SetVariable("default_mouse", "default"),
                    SetVariable("water_vial_checkpoint", True),
                    Show("water_filled_vial")
                ],
                Notify("Your dropper is empty.")
            )

        # Polystyrene jar button
        imagebutton:
            idle  "images/water_scene/polystyrene_jar.png"
            hover "images/water_scene/polystyrene_jar_hover.png"
            at Transform(zoom=0.8)
            action If(
                default_mouse == "dropper_filled",
                [
                    Hide("glass_vial_popup"),
                    Jump("polystyrene_jar_click")

                ],
                Notify("Your dropper is empty.")
            )

screen water_filled_vial():
    modal True
    tag water_filled_vial

    imagebutton:
        idle  "images/water_scene/glass_vial_filled.png"
        hover "images/water_scene/glass_vial_filled_hover.png"
        xalign 0.5 yalign 0.5
        at Transform(zoom=1)
        action [
                Hide("water_filled_vial"),
                Jump("filled_vial_click")
            ]
        
        
screen vial_to_cooler():
    draggroup:
        drag:
            drag_name "glass_vial_filled"
            child "glass_vial_filled"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "cooler"
            child "cooler"
            xpos 0.40 ypos 0
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
#-------------------------------------------------------------- Labels -----------------------------------


label polystyrene_jar_click():
    s dismayed1 "You can't use the polystyrene jar, you should fill the glass vial instead."
    call screen glass_vial_popup
    
label water:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    if analyzed["water"]:
        $ analyzing["water"] = False
        scene water_bg_water at full_screen_crop_top     
        s normal2 "You've already collected this water sample."
        jump desk

    $ analyzing["water"] = True
    scene water_bg_water at full_screen_crop_top


    # Give them the tools they need:
    $ tools["water_glove"]   = True
    $ tools["syringe"]  = True
    $ tools["cooler"]  = True
    $addToToolbox(["water_glove", "syringe", "cooler"])

    call screen water_scene

    #call screen toolbox_water
    return

label first_time_water():
    $ encountered["water"] = True
    "New photo added to evidence."
    call screen water_scene


label filled_vial_click():
    s normal2 "You have filled the vial with a sample of water! Now what do you have to do with it to transport it back to the lab..."
    call screen water_filled_vial

label clicked_cooler():
    call screen vial_to_cooler
    jump water_final_vial
    
label water_final_vial:
    hide screen vial_to_cooler
    $ default_mouse = "default"
    "Sample sealed and stored on ice."
    $ addToInventory(["water"])
    $ analyzed["water"] = True
    $ tools["water_glove"]   = False
    $ tools["syringe"]  = False
    $ tools["cooler"]  = False
    $ clear_toolbox()
    $ close_inventory()
    jump desk





