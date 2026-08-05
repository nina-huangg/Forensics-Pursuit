screen drag_to_bag(item_image, item_drag_name):
    modal True
    add Solid("#0008")
    
    draggroup:
        drag:
            drag_name item_drag_name
            child item_image
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragged item_dragged_package

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.25
            draggable True
            droppable True
            dragged item_dragged_package

screen drag_tape_to_bag():
    modal True
    add Solid("#0008")

    draggroup:
        drag:
            drag_name "tape"
            child "tamper evident tape"
            xpos 0.25 ypos 0.3
            draggable True
            droppable True
            dragged item_dragged_package

        drag:
            drag_name "bag"
            child "evidence bag large"
            xpos 0.55 ypos 0.25
            draggable True
            droppable True
            dragged item_dragged_package

## Camera flash effect #########################################################
## A quick white flash + shutter sound, used to indicate a photo was taken.

transform camera_flash_transform:
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.25 alpha 0.0

screen camera_flash():
    zorder 300
    add Solid("#fff") at camera_flash_transform

label flash_camera:
    show screen camera_flash
    play sound "audio/camera_shutter.ogg"
    pause 0.6
    hide screen camera_flash
    return


screen evidence_closeup_view():
    ## A real full-screen close-up, shown/hidden explicitly at specific
    ## story points (see hotspot_door_handle, can_menu, wheel_menu) rather
    ## than tied to a one-shot scene statement. Being a screen means it's
    ## reactive -- it automatically redraws with whatever
    ## active_process.current_image() returns right now, every single time
    ## anything changes, so it just naturally holds steady through all 6
    ## steps with zero extra sync calls needed anywhere.
    ## acts as a background, so it needs to render BEHIND the inventory
    ## panel, dialogue box, and everything else -- not on top of them.
    zorder -10
    if active_process:
        $ _img = active_process.current_image()
        if _img and renpy.image_exists(_img):
            add _img:
                xalign 0.5
                yalign 0.5
                xsize 1920
                ysize 1080
                fit "cover"
