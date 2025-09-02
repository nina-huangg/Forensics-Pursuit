"""
This file contains all labels and functions related to the clothing rack analysis once it's been clicked on
"""
#-------------------------------------------------------------Screens-----------------------------------
image rack_fold_sealed_overlay = "images/rack_scene/druggist_fold_sealed_large.png"

screen rack_scene():
    modal True
    tag rack_fold
    add "images/rack_scene/rack_close_powder.jpg" at full_screen
    imagebutton:
        idle  "images/rack_scene/powder.png"
        hover "images/rack_scene/powder_hover.png"
        xpos 730
        ypos 425
        action If(
            not asked["rack_glove"],
            Notify("You need to put on protective gloves first."),
            If(
                default_mouse == "druggist_paper",
                [
                    SetVariable("default_mouse", "default"),
                    Hide("rack_scene"),
                    Show("fold_scene")
                ],
                If(
                    default_mouse == "scalpel",
                    [
                        SetVariable("default_mouse", "default"),
                        Hide("rack_scene"),
                        Jump("scalpel_no_paper")
                    ],
                    Notify("Looks like there's some powder on this costume. I wonder how we can transport it back to the lab...")
                )
            )
        )


        
screen fold_scene():
    modal True
    tag rack_fold


    imagebutton:
        idle  "images/rack_scene/powder.png"
        hover "images/rack_scene/powder_hover.png"
        xpos 730
        ypos 425
        
        action If(
            default_mouse == "scalpel",
            [
                SetVariable("default_mouse", "scalpel_powder"),
                Notify("you scrape up powder onto your scalpel.")
            ],
            Notify("This is a clothing rack")
            )
    imagebutton:
        idle  "images/rack_scene/druggist_paper.png"
        hover "images/rack_scene/druggist_paper_hover.png"
        at Transform(xalign=0.8, yalign=0.8, zoom=1.5)
        action If(
                default_mouse == "scalpel_powder",
                [
                    Hide("fold_scene"),
                    SetVariable("default_mouse", "default"),
                    Show("paper_powder_screen"),
                    ],
                Notify("You need to use a tool to collect powder so you can deposit it onto the paper.")
            )

screen paper_powder_screen():
    modal True
    tag rack_paper_powder

    add "images/rack_scene/druggist_paper_powder.png" xalign 0.5 yalign 0.5

    frame:
        background Solid("#00000080")  # black at 50% opacity
        xalign 0.5 yalign 0.8
        xpadding 30 ypadding 30

        vbox:
            spacing 20

            text "What kind of fold would you like to perform?" size 30 color "#FFF"

            textbutton "Simple Fold":
                background Solid("#FFFFFF50")
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("simple_fold_chosen"),
                ]

            textbutton "Envelope Fold":
                background Solid("#FFFFFF50")
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("envelope_fold_chosen"),
                ]

            textbutton "Druggist Fold":
                background Solid("#FFFFFF50") # white at 30% opacity
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("druggist_fold_taping"),
                ]

            textbutton "No Fold":
                background Solid("#FFFFFF50")
                padding (10, 5)
                action [
                    Hide("paper_powder_screen"),
                    Jump("no_fold_chosen"),
                ]
        


#-------------------------------------------------------------- Labels -----------------------------------

                
label rack:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    # Already done?
    if analyzed.get("rack", False):
        $ analyzing["rack"] = False
        scene rack_done
        "You've already collected the rack sample."
        jump house

    # First time here
    $ analyzing["rack"] = True
    scene rack_close_powder at full_screen
    if not encountered.get("rack", False):
        $ encountered["rack"] = True
        "New photo added to evidence."

    $ clear_toolbox()
    $ tools["rack_glove"]           = True
    $ tools["druggist_paper"]    = True
    $ tools["adhesive_tape"]    = True
    $ tools["brush"]            = True
    $ tools["scalpel"]      = True
    $ addToToolbox(["rack_glove","druggist_paper", "adhesive_tape", "brush", "scalpel"])

    call screen rack_scene

    return



label scalpel_no_paper():
    s think "the scalpel is the right tool to pick up the powder, but you first need to get something ready so you can deposit the powder you collect onto it"
    call screen rack_scene


label druggist_fold_taping():
    $ clear_toolbox()
    call screen tape_to_druggist

    call screen fold_to_bag

    call screen tape_to_bag
    
label rack_final:
    $ addToInventory(["powder_in_bag"])
    $ default_mouse = "default"
    "Sample sealed and stored."
    $ analyzed["rack"] = True
    $ tools["rack_glove"]           = False
    $ tools["druggist_paper"]    = False
    $ tools["adhesive_tape"]    = False
    $ tools["brush"]            = False
    $ tools["evidence_bag"]            = False
    $ tools["scalpel"]            = False
    $ close_inventory()

    $ clear_toolbox()
    jump house

#---- labels for MCQ
label simple_fold_chosen():
    s think "That won't secure the sample properly."
    call screen paper_powder_screen

label envelope_fold_chosen():
    s dismayed2 "That wastes evidence – try again."
    call screen paper_powder_screen

label no_fold_chosen():
    s dismayed1 "You need to fold it to keep the fibers inside."
    call screen paper_powder_screen

        
screen tape_to_druggist():
    draggroup:
        drag:
            drag_name "tape"
            child "tamper evident tape"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
        
        drag:
            drag_name "bag"
            child "druggist_fold"
            xpos 0.55 ypos 0.2
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package

screen fold_to_bag():
    draggroup:
        drag:
            drag_name "fold"
            child "druggist_fold_sealed_large"
            xpos 0.25 ypos 0.3
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




    
  
    
