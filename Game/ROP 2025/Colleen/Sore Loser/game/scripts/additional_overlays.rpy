"""
To fit new UI needs.
"""
screen back_button_overlay():
    zorder 10
    modal False

    hbox:
        xpos 0.9 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action Function(return_to_stage)

