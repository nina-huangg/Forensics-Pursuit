"""
This file contains all custom screens used in the game.
"""


# SCREEN: clothing_body ------------------------------------------------------------ #

screen clothing_body:
    imagemap:
        ground "body_with_clothing.png"
        hover "body_with_clothing.png"

    imagebutton:
        idle "buttons/pocket_highlight_invisible.png"
        hover "buttons/pocket_highlight.png"
        xpos 856
        ypos 288
        action Return()


screen viv_tip_clipboard:
    imagebutton:
        idle "viv_icon_base.png"
        hover "vivienne_icon_name.png"
        xalign 0.95
        yalign 0.95
        action [Function(renpy.notify, "Click on the clipboard icon to record your observations.")]


# SCREEN: injuries_body (Front) ---------------------------------------------------- #

screen injuries_body:

    imagemap:
        ground "body_base.png"
        hover "body_base.png"
    
    imagebutton:
        idle "viv_icon_base.png"
        hover "vivienne_icon_name.png"
        xalign 0.95
        yalign 0.95
        action [Function(renpy.notify, "Click on any injuries or personal identifications to take photos of them.")]

    imagebutton:
        xpos 0.98
        ypos 0.3
        anchor (1.0, 1.0)
        idle "buttons/to_back_body_button.png"
        hover "buttons/to_back_body_button_hover.png"
        action [Hide("injuries_body"), Show("injuries_body_back")]

    timer 0.1 repeat True action If(len(photos_taken_locations) > 0, Jump("finished_photography"))


# SCREEN: injuries_body_back (Back) ------------------------------------------------ #

screen injuries_body_back:
    imagemap:
        ground "body_back_base.png"
        hover "body_back_hover.png"
    
    imagebutton:
        idle "viv_icon_base.png"
        hover "vivienne_icon_name.png"
        xalign 0.95
        yalign 0.95
        action [Function(renpy.notify, "   Click on any injuries or personal identifications to take photos of them.")]

    imagebutton:
        xpos 0.98
        ypos 0.3
        anchor (1.0, 1.0)
        idle "buttons/to_front_body_button.png"
        hover "buttons/to_front_body_button_hover.png"
        action [Hide("injuries_body_back"), Show("injuries_body")]

    # tattoo button
    imagebutton:
        idle "tattoo_base.png"
        hover "tattoo_hover.png"
        xalign 0.83
        yalign 0.35
        action Function(injury_hotspot_click, "tattoo")


# SCREEN: injury_photo_view -------------------------------------------------------- #

init python:
    injury_image_map = {
        "tattoo": "images/injury_screens/tattoo_close_base.png",
    }

    def injury_hotspot_click(location_id):
        """Called when player clicks an injury hotspot.
        Sets current photo location and shows injury close-up."""
        store.current_photo_location = location_id
        renpy.show_screen("injury_photo_view", location_id=location_id)
        renpy.restart_interaction()

screen injury_photo_view(location_id="knuckle1"):
    zorder 50

    $ _img = injury_image_map.get(location_id, "images/injury_screens/knuckle1.png")
    $ _loc_name = camera_config.locations.get(location_id, {}).get("name", location_id) if camera_config else location_id

    add _img

    text "[_loc_name]" xpos 0.5 ypos 0.05 anchor (0.5, 0.0) size 40 color "#ffffff" outlines [(2, "#000000", 0, 0)] font "ConcertOne-Regular.ttf"

    imagebutton:
        idle "buttons/back_button.png"
        hover "buttons/back_button_hover.png"
        xalign 0.96
        yalign 0.05
        action [SetVariable("current_photo_location", None), Hide("injury_photo_view")]

screen tattoo:
    imagemap:
        ground "images/injury_screens/tattoo_close_base.png"
        hover "images/injury_screens/tattoo_close_base.png"

    imagebutton:
        xpos 0.98
        ypos 0.90
        anchor (1.0, 1.0)
        idle "buttons/back_button.png"
        hover "buttons/back_button_hover.png"
        action [Hide("tattoo"), Show("injuries_body_back")]


# SCREEN: viv_screen --------------------------------------------------------------- #

screen viv_screen:

    imagebutton:
        idle "viv_icon_base.png"
        hover "vivienne_icon_name.png"
        xalign 0.95
        yalign 0.95
        action NullAction()


# SCREEN: viv_check ---------------------------------------------------------------- #

screen viv_check(label, tool):
    imagebutton:
        idle "sprites/vivienne_icon_hand.png"
        hover "sprites/vivienne_icon_hand_hover.png"
        xalign 0.95
        yalign 0.95
        action If(
            default_mouse == tool,
            [SetVariable("default_mouse", "default"), Jump(label)],
            [
                Function(renpy.notify, "You need to select a {} from your toolbox.".format(tool)),
                Show("full_inventory"),
                SetVariable("default_mouse", "default")
            ]
        )


# SCREEN: container_choice --------------------------------------------------------- #

screen container_choice():

    add Solid("#00000088")

    frame:
        background None
        xalign 0.5
        yalign 0.5

        hbox:
            spacing 150
            xalign 0.5
            yalign 0.5

            imagebutton:
                idle "jar_base.png"
                hover "jar_hover.png"
                action Jump("sampling_complete")
                focus_mask True

            imagebutton:
                idle "bucket_base.png"
                hover "bucket_hover.png"
                action Function(renpy.notify, "That container is not suitable.")
                focus_mask True

            imagebutton:
                idle "bin_base.png"
                hover "bin_hover.png"
                action Function(renpy.notify, "That container is not suitable.")
                focus_mask True


# SCREEN: clipboard_icon ----------------------------------------------------------- #

image clipboard_idle = im.Scale("clipboard_icon_base.png", 150, 150)
image clipboard_hover = im.Scale("clipboard_icon_hover.png", 150, 150)

screen clipboard_icon:

    imagebutton:
        idle "clipboard_idle"
        hover "clipboard_hover"
        xalign 0.98
        yalign 0.02
        action [Hide("clipboard_icon"), Call("clipboard_open")]


# SCREEN: clipboard_open ----------------------------------------------------------- #

default clipboard_state = 0

screen clipboard_open():

    modal True
    zorder 100

    add Solid("#00000088")

    frame at clipboard_slide_in:
        background None
        xalign 0.5
        yalign 0.5

        imagemap:
            ground "form[clipboard_state].png"
            hover "form[clipboard_state]_hover.png"

            if clipboard_state == 0:
                hotspot (604, 409, 380, 111) action SetVariable("clipboard_state", 1)

            if clipboard_state == 1:
                hotspot (950, 415, 370, 100) action SetVariable("clipboard_state", 2)

            if clipboard_state == 2 and location == "postphoto":
                hotspot (864, 803, 50, 40) action SetVariable("clipboard_state", 3)

            if (clipboard_state == 2 and location != "postphoto") or clipboard_state == 3:
                imagebutton:
                    xpos 0.60
                    ypos 0.8
                    idle "buttons/back_button.png"
                    hover "buttons/back_button_hover.png"
                    action [Show("clipboard_icon"), Return()]

label clipboard_open:
    call screen clipboard_open
    return