define config.mouse = {
    "dropper": [("dropper cursor.png", 18, 250)],
    "blood": [("with blood.png", 84, 122)],
    "swab": [("swab cursor.png", 83, 120)],
    "hover": [("hover cursor.png", 0, 0)],
    "ALS": [("ALS cursor.png", 255, 120)],
    "tube": [("bloody_tube_cursor.png", 0, 0)],
    "tape": [("Tamper_evident_tape_cursor.png", 0, 0)]
}

# tools for blood detection
default tools = {
    "ALS": False,
    "goggles": False,
    "switch": False,
    "water": False,
    "swab": False,
    "Hemastic test strip": False,
    "evidence bag": False,
    "tape": False
}

default first_visit = {
    "ALS": True,
    "moist": True,
    "water": True,
    "swab": True,
    "Hemastic test strip": True
}

default area = {
    "shower": False,
    "sink": False
}

default investigated = {
    "shower": False,
    "sink": False
}

image sink_ALS = "sink_ALS.png"
image shower_ALS = "shower_ALS.png"

default swab_reason = {"lab": False}

label start:
    scene bathroom
    "You've arrived at the crime scene."
    "Let's use your forensics knowledge to solve this crime case!"

    label bathroom:
        call screen default_screen

    label investigate_sink:
        if investigated["sink"]:
            "This area has already been examined."
            call screen default_screen
        else:
            hide screen default_screen
            scene sink
            $ tools["ALS"] = True
            $ area["sink"] = True
            call screen blood_detection_tools

    label investigate_shower:
        if investigated["shower"]:
            "This area has already been examined."
            call screen default_screen
        else:
            hide screen default_screen
            scene shower
            $ tools["ALS"] = True
            $ area["shower"] = True
            call screen blood_detection_tools

    label ALS: 
        $ default_mouse = "ALS"
        # Set the background scene based on the area
        if area["sink"]:
            scene sink_ALS
            show sink_ALS
        elif area["shower"]:
            scene shower_ALS
            show shower_ALS

        pause 0.5
        # Display the dialogue
        if first_visit['ALS']:
            $ first_visit['ALS'] = False
            "Different materials carry unique characteristics that make them fluoresce differently under various specific wavelengths of light."
            "At a crime scene, evidence such as fibres, chemicals, and biological fluids can be detected using this method."

        # Set the default mouse and call the appropriate screen
        if area["sink"]:
            call screen sink_locating
        elif area["shower"]:
            call screen shower_locating    
    
    label located_stain:
        $ default_mouse = ''
        $ tools["ALS"] = False
        $ tools["swab"] = True
    
        if area["sink"]:
            scene sink
        elif area["shower"]:
            scene shower
        
        "Now you've located a stain. Use your knowledge to test whether it is blood!"
    
        call screen blood_detection_tools

    label swab:
        if first_visit['moist']:
            $ first_visit['moist'] = False
            "Remember that you have to use a moist swab."
        
        if not swab_reason['lab']:
            $ tools['swab'] = False
            $ tools['Hemastic test strip'] = True
            if area["sink"]:
                scene sink_moist
                call screen moisturize_swab('lift', 'sink')
            elif area["shower"]:
                scene shower_moist
                call screen moisturize_swab('lift', 'shower')
        else:
            call screen moisturize_swab('lift', 'shower')


    label lift_water:
        $ default_mouse = "dropper"
        if area['sink']:
            call screen moisturize_swab('drag', 'sink')
        elif area['shower']:
            call screen moisturize_swab('drag', 'shower')

    label moist_swab:
        $ default_mouse = ''
        if area['sink']:
            show screen moisturize_swab('stick', 'sink')
            call screen moisturize_swab('complete', 'sink')
        elif area['shower']:
            show screen moisturize_swab('stick', 'shower')
            call screen moisturize_swab('complete', 'shower')

    label swab_for_test:
        if not swab_reason['lab']:
            if first_visit['swab']:
                $ first_visit['swab'] = False
                "Now let's do the presumptive test."
                "Presumptive tests are used to determine if an unknown substance is likely to be blood."
                "They are helpful in adapting the next most appropriate action to take, but they can by no means confirm whether a sample is truly blood or not."
                "If the test is positive, further samples can be taken to a lab for testing."
            $ default_mouse = "swab"
            if area['sink']:
                scene sink
                call screen swab_for_test('sink')
            elif area['shower']:  
                scene shower 
                call screen swab_for_test('shower')
        else:
            $ default_mouse = "swab"
            call screen swab_for_lab

    label swab_finished_lab:
        $ default_mouse = ''
        scene after_swab_shower
        call screen package_swab('lift')

    label lift_swab_lab:
        $ default_mouse = "blood"
        call screen package_swab('drag')

    label close_tube:
        $ default_mouse = ''
        call screen package_swab('close')

    label put_in_evidence_bag:
        scene shower_moist
        "Good! Now click on the evidence bags to package the collected sample."
        $ tools["evidence bag"] = True
        call screen blood_detection_tools
        # call screen evidence_bad('lift')
    
    label evidence_bag:
        $ tools["evidence bag"] = False
        call screen evidence_bag('lift')

    label lift_bloody_tube:
        $ default_mouse = "tube"
        call screen evidence_bag('drag')

    label finish_evidence_bag:
        $ default_mouse = ''
        call screen evidence_bag('close')
        
    label seal_evidence_bag:
        scene moist_bag
        "You've packaged your evidence."
        "Lastly, let's secure the bag to prevent tampering of any kind."
        $ tools["tape"] = True
        call screen blood_detection_tools

    label tape:
        $ default_mouse = 'tape'
        scene moist_bag
        call screen tape
    
    label finish_tape:
        $ default_mouse = ''
        call screen finish_tape

    label swab_finished_sink:
        $ default_mouse = ''
        scene after_swab_sink
        call screen blood_detection_tools

    label swab_finished_shower:
        $ default_mouse = ''
        scene after_swab_shower
        call screen blood_detection_tools

    label hemastic_test:
        $ tools['Hemastic test strip'] = False
        if area["sink"]:
            scene sink
            call screen sink_hemastic_test('lift', 'sink')
        elif area["shower"]:
            scene shower
            call screen sink_hemastic_test('lift', 'shower')

    label lift_swab:
        $ default_mouse = "blood"
        if area["sink"]:
            call screen sink_hemastic_test('drag', 'sink')
        elif area["shower"]:
            call screen sink_hemastic_test('drag', 'shower')

    label drag_swab:
        $ default_mouse = ''
        if area["sink"]:
            show screen sink_hemastic_test('stick', 'sink')
            call screen sink_hemastic_test('finish', 'sink')
        elif area["shower"]:
            show screen sink_hemastic_test('stick', 'shower')
            call screen sink_hemastic_test('finish', 'shower')
        
    label shower_evidence:
        "Dark green or black, indicating a positive result with the Hemastix! Let's swab another time for further lab testing."
        $ tools['swab'] = True
        $ swab_reason['lab'] = True
        call screen blood_detection_tools

    
    label finish_sink:
        "Looks like a yellow colour-change, meaning a negative result with the Hemastix."
        $ area['sink'] = False
        $ investigated['sink'] = True
        jump check_finish
    
    label finish_shower:
        scene moist_bag_sealed
        $ area['shower'] = False
        $ investigated['shower'] = True
        $ swab_reason['lab'] = False
        jump check_finish

    label check_finish:
        if investigated['sink'] and investigated['shower']:
            jump end
        else:
            "Now you have the result for the presumptive test. \nTry investigate other areas!"
            pause 1.0
            jump bathroom
        
    label end:
        scene bathroom
        "Congrats! You have now finished evidence collection for this stage"
        "Now, let's bring the evidence to the lab for DNA testing."
        return
