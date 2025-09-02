"""
This file contains all labels and functions related to the smoke machine analysis once it's been clicked on
"""


screen smoke_screen():
    modal True
    tag smoke_machine
        
    on "show" action If(
        not encountered.get("smoke", False),
        Jump("first_time_smoke"),
        NullAction()
    )
    
    imagebutton:
        idle  "images/smoke_scene/smoke_machine.png"
        hover "images/smoke_scene/smoke_machine_hover.png"
        at Transform(zoom=1.2)
        xpos      640 ypos 10
        action If(
            # 1) Do they have gloves on?
            not asked["smoke_glove"],
            Notify("You need to put on protective gloves first."),

            # 2) Otherwise, have they put on goggles?
            If(
                not asked["smoke_goggle"],
                Notify("You need to put on protective goggles first."),

                # 3) Otherwise, proceed with your normal box-click logic
                If(
                    default_mouse == "box_tamper",
                    [
                        Hide("smoke_screen"),
                        SetVariable("default_mouse", "default"),
                        Jump("sealing_smoke"),
                    ],
                    # 4) else if they tried paper bag
                    If(
                        default_mouse == "paper_bag",
                        [
                            Hide("smoke_screen"),
                            SetVariable("default_mouse", "default"),
                            Jump("paper_bag_click")
                        ],
                        # 5) final fallback
                        Notify("This is a smoke machine. Look in the toolbox to see what you can use to transport it back to the lab!")
                    )
                )
            )
        )


screen evidence_box_popup():
    modal True
    tag evidence_box


    imagebutton:
        idle       "images/smoke_scene/evidence_box.png"
        hover      "images/smoke_scene/evidence_box_hover.png"
        at         Transform(zoom=0.8)
        xalign     0.25 yalign 0.5
        action If(
            default_mouse == "tamper",
            [ 
                Hide("evidence_box_popup"),
                SetVariable("default_mouse", "box_tamper"),
                Show("smoke_screen") 
            ],
            [
                Hide("evidence_box_popup"),
                Jump("box_no_tamper")
            ]
        )

#-------------------------------------------------------------- Labels -----------------------------------        
label smoke:
    $ default_mouse = "default"
    hide screen casefile_physical
    hide screen casefile_photos

    # If already done, skip:
    if analyzed["smoke"]:
        $ analyzing["smoke"] = False
        scene smoke_bg at full_screen_crop_top     
        s normal2 "You've already collected the smoke sample."
        jump desk

    # First time here:
    $ analyzing["smoke"] = True
    scene smoke_bg_smoke at full_screen_crop_top

    $ tools["smoke_glove"]      = True
    $ tools["smoke_goggle"]     = True
    $ tools["evidence_box"]= True
    $ tools["paper_bag"]   = True
    $ tools["tamper"]   = True
    $addToToolbox(["smoke_glove", "smoke_goggle", "paper_bag", "evidence_box", "tamper"])

    call screen smoke_screen

    return

label first_time_smoke():
    $ encountered["smoke"] = True
    "New photo added to evidence."
    show nina_write
    s normal1 "It's hard to access the liquid in this model of smoke machine so the theatre said we can take the full thing."
    hide nina_write
    call screen smoke_screen

label box_no_tamper():
    s normal2 "Cool evidence box! It isn't ready to pick up the smoke machine yet. Maybe you have to do something to it so it can hold the smoke machine..."
    call screen evidence_box_popup

label paper_bag_click():
    s dismayed2 "Unfortunately a simple paper bag isn't strong enough to hold a whole smoke machine. What can we use that's stronger..."
    call screen smoke_screen
    
label sealing_smoke():
    scene smoke_bg at full_screen_crop_top
    $ clear_toolbox()
    call screen tape_to_box

label smoke_final:
    $ default_mouse = "default"
    "Sample sealed and stored."
    $ addToInventory(["smoke"])
    $ analyzed["smoke"] = True
    $ tools["smoke_glove"]      = False
    $ tools["smoke_goggle"]     = False
    $ tools["evidence_box"]= False
    $ tools["paper_bag"]   = False
    $ clear_toolbox()
    $ close_inventory()
    jump house

screen tape_to_box():
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
            drag_name "box"
            child "evidence_box"
            xpos 0.40 ypos 0
            draggable True
            droppable True
            dragging item_dragging_package
            dragged item_dragged_package
