default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default location = "hallway"

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]
# default correct_dfo_mixture = {"dfo", "hfe", "acetic acid", "methanol"}
# default player_dfo_mixture = {}
# default player_tool = ""
define s = "Supervisor"

init python:
    config.mouse = {
        "default": [("cursor.png", 0, 0)],
        "dropper": [("dropper.png", 0, 49)],
        "dropper filled": [("dropper filled.png", 0, 49)],
        "hand": [("hand.png", 0, 47)]
    }

    default_mouse = "default"

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def analyzed_everything() -> None:
        return prints["print_1"].processed and prints["print_4"].processed
    
    def set_timer(item: str):
        item = False
    
    def disable_timer(item: str):
        item = True

    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)

    def close_menu():
        if renpy.get_screen("casefile_physical"):
            renpy.hide_screen("casefile_physical")
        elif renpy.get_screen("casefile_photos"):
            renpy.hide_screen("casefile_photos")
        elif renpy.get_screen("casefile"):
            renpy.hide_screen("casefile")
        else:
            renpy.show_screen("casefile")

    
    class Evidence:
        def __init__(self, name, afis_details):
            self.name = name
            self.afis_details = afis_details
            self.processed = False
    
    ### declare each piece of evidence
    laptop_fingerprint = Evidence(name = 'laptop_fingerprint',
                                afis_details = {
                                    'image': 'laptop_fingerprint',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})
    screwdriver = Evidence(name = 'screwdriver',
                        afis_details = {
                            'image': 'screwdriver_fingerprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '70'})
    
    ### declare afis relevant evidence
    afis_evidence = [laptop_fingerprint, screwdriver]

    ### set current_evidence to track which evidence is currently active
    current_evidence = screwdriver


#################################### START #############################################
label start:
    scene entering_lab_screen
    with Dissolve(1.5)

label lab_hallway_intro:  
    scene lab_hallway_idle
    show ema normal as character
    s "Officer, good to see you again."
    show ema glasses as character
    s "Great job processing the scene! I knew I could count on you"
    # s "While you’ve been busy, I talked to the other officers who were on the scene that day. They collected this."
    s "Welcome to the lab! Here, you can analyze all the evidence you collected from the crime scene."
    show ema normal as character
    s "I need you to perform a pattern analysis on the fingerprint you found on the door and on the gin bottle you collected."
    s "For the gin bottle, you'll have to remove the label and use DFO to actually get a print to load into the fingerprint pattern analysis application."
    s "You can go wherever you want - but I suggest beginning with the oven first so we won't have to waste time waiting for it to heat up."

label hallway:
    $ location = ""
    scene lab_hallway_idle
    python:
        if analyzed_everything():
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    call screen lab_hallway_screen

label data_analysis_lab:
    $ location = ""
    python:
        if analyzed_everything():
            renpy.jump("end")
    show screen back_button_screen('hallway') onlayer over_screens  
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('data_analysis_lab') onlayer over_screens  
    call screen afis_screen

label materials_lab:
    $ location = ""
    python:
        if analyzed_everything():
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label wet_lab:
    $ location = ""
    python:
        if analyzed_everything():
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    python:
        if analyzed_everything():
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

label end:
    hide screen back_button_screen onlayer over_screens
    show ema normal as character
    s "It looks like you've analyzed all the evidence. Great work!"
    s "I hope you took note of the results. Tomorrow, you'll be testifying in court about your findings."
    show ema glasses as character
    s "But for now, give yourself a pat on the back and go get some rest!"
    return