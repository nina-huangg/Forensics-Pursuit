screen back_to_cabinet():
    zorder 10
    modal False

    hbox:
        xpos 0.9 ypos 0.1
        imagebutton:
            auto "back_button_%s.png" at Transform(zoom=0.2)
            action Jump("cabinet")


label tylenol:
    hide screen back_button_overlay

    $ analyzing["tylenol"] = True

    show darken_overlay2
    show tylenol at Transform(xpos=0.42, ypos=0.2, zoom=0.8)
    show capsules at Transform(xpos=0.49, ypos=0.4, zoom=0.7, rotate=0.1)

    s write "We should take this back to the lab for further analysis."

    python:
        removal_list = ["uv_light", "magnetic_powder", "scalebar", "tape", "backing_card", "gel_lifter", "evidence_bag"]
        for item in removal_list:
            if item in toolbox_items:
                removeToolboxItem(toolbox_sprites[toolbox_items.index(item)])
    
    $ tools["bag"] = True
    $ packaging = True
    $ addToToolbox(["evidence_bag", "tamper_evident_tape"])
    
    hide darken_overlay2

    call screen toolbox

label vitamins:
    hide screen back_button_overlay
    show darken_overlay2
    show vitamins
    

    "{color=#88F3FF}Various vitamins and supplements.{/color}"

    show screen back_to_cabinet

    $ renpy.pause(hard=True) 