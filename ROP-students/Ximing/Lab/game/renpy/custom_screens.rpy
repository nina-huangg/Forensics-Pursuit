screen hallway_screen():
    image "lab_hallway_dim"
    
    hbox:
        xpos 0.22 yalign 0.5
        imagebutton:
            idle "DNA_analysis_lab.jpeg"
            hover "DNA_analysis_lab.jpeg"
            hovered Notify("DNA Analysis Lab")
            unhovered Notify('')
            action Jump("enter_DNA_lab")

    hbox:
        xpos 0.234 yalign 0.628
        hbox:
            text("{size=-6}DNA Analysis Lab{/size}")

    hbox:
        xpos 0.63 yalign 0.5
        imagebutton:
            idle "bone_lab"
            hover "bone_lab"
            hovered Notify("Bone Lab")
            unhovered Notify('')
            action Jump('enter_bone_lab')

    hbox:
        xpos 0.68 yalign 0.628
        hbox:
            text("{size=-6}Bone Lab{/size}")

screen dark_overlay_with_mouse():
    modal True

    default mouse = (0, 0)

    # Timer to repeatedly update the mouse position
    timer 0.02 repeat True action SetScreenVariable("mouse", renpy.get_mouse_pos())
    # Adding the darkness overlay with the current mouse position
    add "darkness" pos mouse anchor (0.5, 0.5)

screen back_button_screen(location):
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at checkmark_small
            hover "back_button_hover"
            action Jump(location)

screen choose_piece():  
    imagemap:
        idle "filled_tray"
        hover "filled_tray_hover.png"
        ground "filled_tray.png"

        hotspot (480, 224, 194, 331) action Jump("first_sample")
        hotspot (676, 319, 104, 166) action Jump("sample_2")
        hotspot (791, 287, 181, 219) action Jump("sample_3")
        hotspot (967, 338, 120, 137) action Jump("sample_4")
        hotspot (1085, 278, 162, 232) action Jump("sample_5")
        hotspot (1233, 277, 179, 244) action Jump("sample_6")


screen bone_lab():
    imagemap:
        idle "bone_lab_idle"
        hover "bone_lab_hover"
        ground "bone_lab_idle"
        hotspot (932, 604, 771, 156) action Jump("investigate_bone")
    hbox:
        xalign 0.97 yalign 0.98
        imagebutton:
            idle "back_button" at checkmark_small
            hover "back_button_hover"
            action Jump('hallway')


screen right_arrow(target):
    hbox:
        xalign 0.95 yalign 0.5
        imagebutton:
            idle "right"
            hover "right"
            action Jump(target)

screen left_arrow(target):
    hbox:
        xalign 0.05 yalign 0.5
        imagebutton:
            idle "left"
            hover "left"
            action Jump(target)

screen result_button(target):
    hbox:
        xalign 0.40 yalign 0.90
        imagebutton:
            idle "result"
            hover "result"
            action Jump(target)

screen microscope_button(target):
    hbox:
        xalign 0.60 yalign 0.90
        imagebutton:
            idle "microscope_icon"
            hover "microscope_icon"
            action Jump(target)

screen test_button(target):
    hbox:
        xalign 0.90 yalign 0.90
        imagebutton:
            idle "test_icon"
            hover "test_icon"
            action Jump(target)

screen microscope(name):
    if name == 'sample_2':
        imagemap:
            ground "wood_hover"
            idle "wood_hover"
            hover "wood_hover"
            hotspot (535, 588, 185, 241) action Jump("wood_stereo1")
            hotspot (1034, 580, 194, 151) action Jump("wood_stereo2")
        use test_button('test_2')

    elif name == 'sample_3':
        imagemap:
            ground "bone2_hover"
            idle "bone2_hover"
            hover "bone2_hover"
            hotspot (483, 698, 236, 119) action Jump("bone2_stereo1")
            hotspot (1141, 654, 255, 146) action Jump("bone2_stereo2")
        use test_button('test_3')

    elif name == 'sample_4':
        imagemap:
            ground "stone_hover"
            idle "stone_hover"
            hover "stone_hover"
            hotspot (720, 540, 162, 178) action Jump("stone_stereo1")
            hotspot (846, 732, 205, 161) action Jump("stone_stereo2")
            hotspot (1044, 552, 194, 222) action Jump("stone_stereo3")
        use test_button('test_4')

    elif name == 'sample_5':
        imagemap:
            ground "bone3_hover"
            idle "bone3_hover"
            hover "bone3_hover"
            hotspot (183, 608, 221, 180) action Jump("bone3_stereo1")
            hotspot (1420, 579, 260, 238) action Jump("bone3_stereo2")
        use test_button('test_5')

    elif name == 'sample_6':
        imagemap:
            ground "metal_hover"
            idle "metal_hover"
            hover "metal_hover"
            hotspot (225, 544, 187, 209) action Jump("metal_stereo1")
            hotspot (845, 554, 213, 209) action Jump("metal_stereo2")
            hotspot (1398, 533, 271, 262) action Jump("metal_stereo3")
        use test_button('test_6')

    

screen samples(name, show_checkmark, checked_radiograph):
    if name == 'sample_1':
        image "bone1_closeup1"
        use right_arrow('sample_2')
        use result_button('result_1')

    elif name == 'sample_2':
        image "wood_closeup"
        use right_arrow('sample_3')
        use left_arrow('first_sample')
        use result_button('result_2')
        if checked_radiograph:
            use microscope_button('microscope2')

    elif name == 'sample_3':
        image "bone2_closeup1"  
        use right_arrow('sample_4')
        use left_arrow('sample_2')
        use result_button('result_3')
        if checked_radiograph:
            use microscope_button('microscope3')
    
    elif name == 'sample_4':
        image "stone_closeup1"
        use right_arrow('sample_5')
        use left_arrow('sample_3')
        use result_button('result_4')
        if checked_radiograph:
            use microscope_button('microscope4')

    elif name == 'sample_5':
        image "bone3_closeup1"
        use left_arrow('sample_4')
        use right_arrow('sample_6')
        use result_button('result_5')
        if checked_radiograph:
            use microscope_button('microscope5')

    elif name == 'sample_6':
        image "metal_closeup1"
        use left_arrow('sample_5')
        use result_button('result_6')
        if checked_radiograph:
            use microscope_button('microscope6')
    
    if show_checkmark == 'show':
        hbox:
            xalign 0.8 yalign 0.8
            imagebutton:
                idle "checkmark"
                hover "checkmark"
                action Jump('finish_first_stage_bone')

    

   
screen result_finish(name):
    $ images = {
        'sample_1': ("bone1_radiograph", 'first_sample'),
        'sample_2': ("wood_radiograph", 'sample_2'),
        'sample_3': ("bone2_radiograph", 'sample_3'),
        'sample_4': ("stone_radiograph", 'sample_4'),
        'sample_5': ("bone3_radiograph", 'sample_5'),
        'sample_6': ("metal_radiograph", 'sample_6')
    }
    
    $ image_name, jump_label = images.get(name, (None, None))

    if image_name and jump_label:
        image image_name
        hbox:
            xalign 0.8 yalign 0.8
            imagebutton:
                idle "checkmark"
                hover "checkmark"
                action Jump(jump_label)




transform checkmark_small():
    zoom 0.2

transform evidence_small():
    zoom 0.4