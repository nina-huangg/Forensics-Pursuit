screen blood_detection_tools():
    hbox:
        xpos 0.907 ypos 0.115
        imagebutton:
            idle "ALS.png"
            hover "ALS_hover.png"
            
            action Jump('ALS')
            sensitive tools['ALS']
    
    hbox:
        xpos 0.910 ypos 0.359
        imagebutton:
            idle "swab.png"
            hover "swab_hover.png"
    
            action Jump('swab')
            sensitive tools['swab']

    hbox:
        xpos 0.888 ypos 0.650
        imagebutton:
            idle "Hemastic test strip.png"
            hover "Hemastic test strip_hover.png"
    
            action Jump('hemastic_test')
            sensitive tools['Hemastic test strip']
    hbox:
        xpos 0.033 ypos 0.100
        imagebutton:
            idle "evidence_bag.png"
            hover "evidence_bag_hover.png"
            
            action Jump('evidence_bag')
            sensitive tools['evidence bag']
    hbox:
        xpos 0.003 ypos 0.362
        imagebutton:
            idle "Tamper_evident_tape.png"
            hover "Tamper_evident_tape_hover.png"

            action Jump('tape')
            sensitive tools['tape']



screen default_screen():
    imagemap:
        idle "bathroom.png"
        hover "bathroom.png"
        ground "bathroom.png"

        hotspot (1726, 267, 191, 316) action Jump("investigate_shower") mouse "hover"
        hotspot (520, 694, 167, 194) action Jump("investigate_sink") mouse "hover"

# use ALS to locate the stain
screen sink_locating:
    imagemap:
        idle "sink_ALS.png"
        hover "sink_flurosce.png"
        ground "sink_ALS.png"
        
        hotspot (1055, 468, 229, 182) action Jump("located_stain")

screen shower_locating:
    imagemap:
        idle "shower_ALS.png"
        hover "shower_flurosce.png"
        ground "shower_ALS.png"

        hotspot (748, 484, 526, 212) action Jump("located_stain")

# screen sink_swab:
#     imagemap:
#         idle "sink_stain"
#         hover "sink_flurosce.jpg"
#         ground "sink_stain.jpg"
#         hotspot (571, 403, 326, 153) action Jump("located_stain") mouse "swab"
    
screen moisturize_swab(action, area):
    if area=='sink':
        image "sink_moist"
    elif area=='shower':
        image "shower_moist"

    if action=='lift':
        hbox:
            xpos 0.33 yalign 0.47
            imagebutton:
                idle "water"
                hover "water"
                action Jump("lift_water")
        hbox:
            xpos 0.58 yalign 0.64
            image "unmoist_swab"
    elif action=='drag':
        hbox:
            xpos 0.58 yalign 0.64
            imagebutton:
                idle "unmoist_swab"
                hover "unmoist_swab"
                action Jump("moist_swab")
    elif action=='stick':
        hbox:
            xpos 0.58 yalign 0.64
            image "moist_swab"
    else:
        hbox:
            xpos 0.58 yalign 0.64
            image "moist_swab"
        hbox:
            xpos 0.76 yalign 0.80
            imagebutton:
                idle "checkmark"
                hover "checkmark"
                action Jump("swab_for_test")

        
screen swab_for_test(area):
    if area=='sink':
        imagemap:
            idle "sink.png"
            hover "sink.png"
            ground "sink.png"
            hotspot (1055, 468, 229, 182) action Jump("swab_finished_sink") 
    
    elif area=='shower':
        imagemap:
            idle "shower.png"
            hover "shower.png"
            ground "shower.png"
            hotspot (748, 484, 526, 212) action Jump("swab_finished_shower")

screen swab_for_lab:
    imagemap:
            idle "shower.png"
            hover "shower.png"
            ground "shower.png"
            hotspot (748, 484, 526, 212) action Jump("swab_finished_lab")

screen sink_hemastic_test(action, area):
    if area=='sink':
        image "sink_moist"
    elif area=='shower':
        image "shower_moist"

    if action=='lift':
        hbox:
            xpos 0.58 yalign 0.64
            imagebutton:
                idle "blood_swab"
                hover "blood_swab"
                action Jump("lift_swab")
        hbox:
            xpos 0.25 yalign 0.68
            image "hemastix_unused"
    elif action=='drag':
        hbox:
            xpos 0.25 yalign 0.68
            imagebutton:
                idle "hemastix_unused"
                hover "hemastix_unused"
                action Jump("drag_swab")
    elif action=='stick':
        if area=='sink':
            hbox:
                xpos 0.25 yalign 0.68
                image "negative_result"
        elif area=='shower':
            hbox:
                xpos 0.25 yalign 0.68
                image "positive_result"
    else:
        if area=='sink':
            hbox:
                xpos 0.25 yalign 0.68
                image "negative_result"

            hbox:
                xpos 0.80 yalign 0.80
                imagebutton:
                    idle "checkmark"
                    hover "checkmark"
                    action Jump("finish_sink")
        elif area=='shower':
            hbox:
                xpos 0.25 yalign 0.68
                image "positive_result"
            hbox:
                xpos 0.80 yalign 0.80
                imagebutton:
                    idle "checkmark"
                    hover "checkmark"
                    action Jump("shower_evidence")

screen package_swab(action):
    image "shower_moist"
    if action == 'lift':
        hbox:
            xpos 0.33 yalign 0.47
            image "empty_tube"
        hbox:
            xpos 0.58 yalign 0.64
            imagebutton:
                idle "blood_swab"
                hover "blood_swab"
                action Jump("lift_swab_lab")
    if action == 'drag':
        hbox:
            xpos 0.33 yalign 0.47
            imagebutton:
                idle "empty_tube"
                hover "empty_tube"
                action Jump("close_tube")
    if action == 'close':
        hbox:
            xpos 0.33 yalign 0.47
            image "bloody_swab_in_tube"
        hbox:
            xpos 0.80 yalign 0.80
            imagebutton:
                idle "checkmark"
                hover "checkmark"
                action Jump("put_in_evidence_bag")

screen evidence_bag(action):
    image "shower_moist"
    if action == 'lift':
        hbox:
            xpos 0.33 yalign 0.47
            imagebutton:
                idle "bloody_swab_in_tube"
                hover "bloody_swab_in_tube"
                action Jump("lift_bloody_tube")
        hbox:
            xpos 0.58 yalign 0.64
            image "big_evidence_bag"
    if action == 'drag':
        hbox:
            xpos 0.33 yalign 0.47
            image "bloody_swab_in_tube"
        hbox:
            xpos 0.58 yalign 0.64
            imagebutton:
                idle "big_evidence_bag"
                hover "big_evidence_bag_hover"
                action Jump("finish_evidence_bag")
    if action == 'close':
        hbox:
            xpos 0.58 yalign 0.64
            image "big_evidence_bag"
        hbox:
            xpos 0.80 yalign 0.80
            imagebutton:
                idle "checkmark"
                hover "checkmark"
                action Jump("seal_evidence_bag")

screen tape:
    imagemap:
        idle "moist_bag.png"
        hover "moist_bag_hover.png"
        ground "moist_bag.png"

        hotspot (805, 353, 325, 534) action Jump("finish_tape")
    

screen finish_tape:
    image "moist_bag_sealed"
    hbox:
        xpos 0.80 yalign 0.80
        imagebutton:
            idle "checkmark"
            hover "checkmark"
            action Jump("finish_shower") 

    

