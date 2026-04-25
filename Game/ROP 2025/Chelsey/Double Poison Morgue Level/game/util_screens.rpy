
screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at Transform(zoom=0.2)
            hover "back_button_hover"
            action [Jump(location), Hide('afis_screen')]


screen body_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "body_button" at Transform(zoom=0.2)
            hover "body_button_hover"
            action [Jump(location), Hide('afis_screen')]


screen body_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "body_button" at Transform(zoom=0.2)
            hover "body_button_hover"
            action [Jump(location), Hide('afis_screen')]



## Tools table screen

screen tools_table():
    zorder 3

    # Background photo for the tools table area
    image "tools_table.png" xpos 1201 ypos 0 

    # Tool buttons with hover notifications
    imagebutton:
        idle "surgery tools/scalpel_idle.png"
        hover "surgery tools/scalpel_hover.png"
        action Function(use_tool, "scalpel")
        xpos 0.63
        ypos 0.03
        hovered Notify("Scalpel")

    imagebutton:
        idle "surgery tools/autopsy_knife_idle.png"
        hover "surgery tools/autopsy_knife_hover.png"
        action Function(use_tool, "autopsy knife")
        xpos 0.66
        ypos 0.03
        hovered Notify("Autopsy Knife")

    imagebutton:
        idle "surgery tools/rib_shears_idle.png"
        hover "surgery tools/rib_shears_hover.png"
        action Function(use_tool, "rib shears")
        xpos 0.71
        ypos 0
        hovered Notify("Rib Shears")

    imagebutton:
        idle "surgery tools/stryker_saw_idle.png" at Transform(zoom=0.5)
        hover "surgery tools/stryker_saw_hover.png"
        action Function(use_tool, "stryker saw")
        xpos 0.79
        ypos 0
        hovered Notify("Stryker Saw (Oscillating Saw)")



init python:
    def use_tool(tool_name):
        renpy.Notify(f"You selected the {tool_name} tool.")
        # Add logic to equip tool, change mouse, etc.