###############################
# EVIDENCE COLLECTION CLICKS
###############################

image bg closeup = Transform("closeup", xysize=(1920, 1080))
image bg motorcycle = Transform("motorcycle", xysize=(1920, 1080))

label shards:
    show shards

    $ analyzing["shards"] = True

    if analyzed["shards"] == False:
        if encountered["shards"] == False:
            $ encountered["shards"] = True
            "New photo added to evidence."

        "These look like fragments from a broken taillight."
        "I should collect and package them properly for later comparison."

        call screen inventory
    else:
        "Looks like you've already analyzed the taillight shards."
        jump game

label tiretracks:
    scene bg motorcycle
    show tiretracks at truecenter

    $ analyzing["tiretracks"] = True

    if analyzed["tiretracks"] == False:
        if encountered["tiretracks"] == False:
            $ encountered["tiretracks"] = True
            "New photo added to evidence."

            "There are visible skid marks on the roadway."
            "I should document and measure them before they're disturbed."

        call screen inventory
    else:
        "Looks like you've already analyzed the tire tracks."
        jump game

label paint:
    scene bg closeup
    show paint at truecenter

    if paint_step > 0:
        hide paint

    $ analyzing["paint"] = True

    if analyzed["paint"] == False:
        if encountered["paint"] == False:
            $ encountered["paint"] = True
            "New photo added to evidence."

            "There's a small paint chip on the pavement."
            "It may have come from the car involved in the collision."
            "I should collect it carefully to preserve the evidence."

        call screen inventory
    else:
        "Looks like you've already analyzed the paint chip."
        jump game

###############################
# LAB SCENE CLICKS
###############################

label use_computer:
    $ hide_notebook()
    $ hide_afis()
    hide afis_screen
    scene bg stereomicroscope
    $ stereomicroscope_focus = renpy.random.choice(
        [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]
    )
    # "Entering use_computer label"
    if tasks["Run stereomicroscope on all samples"] == True:
        n "You have already finished using the stereomicroscope."
        jump bio_station
    # else:
    #     $ custom_notify("Incorrect step order!", correct=False)
    #     jump bio_station
    if encountered_stereomicroscope == False:
        n "Use the stereomicroscope to analyze the layers of the paint chip samples from suspected vehicles."
        n "Use the left and right arrows to adjust the focus. Once you have a clear view, click the checkmark to confirm."
    $ encountered_stereomicroscope = True
    $ location = "stereomicroscope"
    show screen inventory
    call screen computer_screen

label use_ftir:
    $ hide_notebook()
    $ hide_afis()
    hide afis_screen
    scene bg ftir
    if encountered_ftir == False:
        n "Use the FTIR spectrometer to analyze the chemical composition of the paint samples."
        n "You will need your notebook to track the results."
        n "Choose a sample from your inventory to analyze."
    $ encountered_ftir = True
    $ location = "ftir_station"
    show screen inventory
    call screen ftir_station