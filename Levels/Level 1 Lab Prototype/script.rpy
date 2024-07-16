default current_cursor = ''
default show_case_files = False
default show_toolbox = False

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]

init python:
    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)
    
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
    show screen case_files_screen onlayer over_screens 
    show screen toolbox_button_screen onlayer over_screens     
    scene lab_hallway_idle
    "Welcome to the lab!"
    "This is where you will spend time analyzing the evidence you have collected."
    "Let's get started!"

label hallway:
    call screen lab_hallway_screen

label data_analysis_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen data_analysis_lab_screen

label afis:
    call screen afis_screen

label materials_lab:
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label wet_lab:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen
    
    
return
