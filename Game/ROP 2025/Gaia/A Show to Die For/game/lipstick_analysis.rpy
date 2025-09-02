"""
This file contains all labels and functions related to the lipstick analysis once it's been clicked on
"""
## ─── the interactive scene ────────────────────────────────────

    
screen lipstick_scene():
    modal True
    tag lipstick_scene

    add "images/lipstick_scene/lipstick_bg.JPG" at full_screen_crop_top
        
    on "show" action If(
        not encountered.get("lipstick", False),
        Jump("first_time_lipstick"),
        NullAction()
    )

    imagebutton:
        idle   "images/lipstick_scene/lipstick.png"
        hover  "images/lipstick_scene/lipstick_hover.png" 
        at Transform(zoom=0.9)
        xpos      640 ypos 480
        action If(
            # If they aren’t gloved yet, prompt them
            not asked["lipstick_glove"],
            [
                Notify("You need to put on protective gloves first."),
                SetVariable("default_mouse", "default")
            ],
            # If they have the glass_jar, they can move on to the next step
            If(
                default_mouse == "glass_jar",
                [
                    SetVariable("default_mouse", "default"),
                    Hide("lipstick_scene"),
                    Jump("lipstick_bagging"),
                    #Return(True),
                    #Function(renpy.jump, "lipstick_final")
                ],
                # if they chose the paper bag, let them know it's wrong and restart them
                If(
                    default_mouse == "paper_bag",
                    [
                        SetVariable("default_mouse", "default"),
                        Hide("lipstick_scene"),
                        Jump("lipstick_paper_bag"),
                    ],
                # catch all
                    Notify("Pick a method to transport this open lipstick to the lab")
                )
            )
        )



# ----------------- labels -----------------------------
        
label lipstick:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    # If they’ve already fully processed the lipstick, bail out:
    if analyzed["lipstick"]:
        $ analyzing["lipstick"] = False
        s normal2 "You've already processed this lipstick."
        jump desk

# First‐time entry:
    $ analyzing["lipstick"]   = True
    scene lipstick_bg_lip at full_screen_crop_top      # your wide shot of the lipstick on the table

    
# Give them the tools they need:
    $ tools["lipstick_glove"]         = True
    $ tools["glass_jar"]  = True
    $ tools["paper_bag"]        = True
    $addToToolbox(["lipstick_glove", "glass_jar", "paper_bag"]) 
    
    call screen lipstick_scene
    return

label first_time_lipstick():
    $ encountered["lipstick"] = True
    "New photo added to evidence."
    call screen lipstick_scene

label lipstick_paper_bag():
    s dismayed2 "This isn't the right container to pick up the lipstick in."
    call screen lipstick_scene

label lipstick_bagging():
    scene lipstick_bg at full_screen_crop_top
    $ clear_toolbox()
    call screen jar_to_bag
    
    call screen tape_to_bag


    
label lipstick_final:
    $ default_mouse = "default"
    "Lipstick stored"
    $ addToInventory(["lipstick"])
    $ analyzed["lipstick"] = True
    $ tools["lipstick_glove"]         = False
    $ tools["glass_jar"]  = False
    $ tools["paper_bag"]        = False
    $ clear_toolbox()
    $ close_inventory()
    jump desk

# ----------------- dragging  --------- #
screen jar_to_bag():
    draggroup:
        drag:
            drag_name "jar"
            child "glass_jar_lipstick"
            xpos 0.25 ypos 0.23
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

transform lipstick_overlay:
    zoom 0.8
    xpos 650
    ypos 570













