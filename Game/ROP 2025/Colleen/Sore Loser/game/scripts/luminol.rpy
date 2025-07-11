"""
This file contains the logic for the luminol minigame.
"""
screen luminol1:
    image "luminol1.png"

screen luminol2:
    image "luminol2.png"

screen luminol3:
    image "luminol3.png"


init python:
    luminol1 = False
    luminol2 = False
    luminol3 = False

screen luminol_game:
    imagemap:
        ground "dark_apt"

        hotspot (0, 850, 500, 300) action If(analyzing["luminol"], [SetVariable("luminol1", True), Show("luminol1"), Play("sound", "audio/spray.mp3")]) mouse "luminol_tilt"
        hotspot (900, 850, 800, 300) action If(analyzing["luminol"], [SetVariable("luminol2", True), Show("luminol2"), Play("sound", "audio/spray.mp3")]) mouse "luminol_tilt"
        hotspot (800, 600, 500, 300) action If(analyzing["luminol"], [SetVariable("luminol3", True), Show("luminol3"), Play("sound", "audio/spray.mp3")]) mouse "luminol_tilt"
    
    timer 0.2 repeat True action If(luminol1 and luminol2 and luminol3, Jump("luminol_finish"))

label luminol:
    play sound "audio/lightswitch.mp3"
    
    $ default_mouse = "luminol"
    scene dark_apt
    hide screen casefile_physical
    hide screen casefile_photos
    hide screen back_button_overlay

    $ analyzing["luminol"] = True

    call screen luminol_game

        # $ renpy.pause(0.1)

label luminol_finish:
    $ default_mouse = "default"

    s write "Looks like there's the last of it..."
    $ analyzed["luminol"] = True

    show screen back_button_overlay

    $ renpy.pause(hard=True) 


