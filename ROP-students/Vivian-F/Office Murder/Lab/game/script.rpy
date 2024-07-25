default show_evidence = False
default show_toolbox = False
default show_case_files = False

default evidence_complete_process = {'gun_blue': False, 'ninhydrin': False, 'bullet_AFIS': False, 'cheque_AFIS': False, 'deskfoot_AFIS': False}

default current_cursor = ''
default current_process = ''
default process_fumehood = False
default process_afis = False

default case_file_dict = {'bullet': False, 'cheque': False, 'deskfoot': False, 'blood': False}
default current_casefile = {'evidence': False, 'digi_evidence': False, 'report': False}
default casefile_title = {'evidence': 'Physical Evidence', 'digi_evidence': 'Digital Evidence', 'report': 'Report'}

default bool_show_case = False
default bool_show_case_evidence = False
default bool_show_case_digi = False
default bool_show_case_report = False
default case_type_selected = ''

default tools = {'gun_blue': False, 'water': False, 'bottle': False, 'ninhydrin': False, 'bag': False, 'tape': False}

# entries on afis when search
default afis_search = []
default afis_search_coordinates = {'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}

# transition for photo taking flash (0 in/out so middle screen don't last long)
define flash = Fade(.25, 0, 0, color="#fff")

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
    
    def set_tool(tool):
        global tools

        if tools[tool]:
            set_cursor('')
            tools[tool] = False
        else:
            set_cursor(tool)
            tools[tool] = True
            for t in tools:
                if t!= tool:
                    tools[t] = False
    
    def set_state_to_processed(process):
        global evidence_complete_process
        evidence_complete_process[process] = True

    def set_current_casefile(type_case):
        global current_casefile
        global case_type_selected
        for case in current_casefile:
            if case == type_case:
                current_casefile[case] = True
                case_type_selected = casefile_title[case]
            else:
                current_casefile[case] = False
    
    def set_case_file_dict(evidence):
        for key in case_file_dict:
            case_file_dict[key] = False
        case_file_dict[evidence] = True
    
    def add_afis(evidence):
        afis_search.append(evidence)
        evidence.afis_processed = True
    
    class Evidence:
        def __init__(self, name, afis_details, afis_processed):
            self.name = name
            self.afis_details = afis_details
            self.afis_processed = False
    
    # declare each piece of evidence
    no_evidence = Evidence(name = '', afis_details = {}, afis_processed = False)

    bullet = Evidence(name = 'bullet',
                        afis_details = {
                            'image': 'bullet_fingerprint',
                            'xpos': 0.18, 'ypos': 0.3,
                            'score': '0'},
                        afis_processed = False)
    cheque = Evidence(name = 'cheque',
                        afis_details = {
                            'image': 'cheque_fingerprint',
                            'xpos':0.22, 'ypos':0.28,
                            'score': '80'},
                        afis_processed = False)
    deskfoot = Evidence(name = 'deskfoot',
                        afis_details = {
                            'image': 'deskfoot_footprint',
                            'xpos':0.22, 'ypos':0.28,
                            'score': '80'},
                        afis_processed = False)
    blood = Evidence(name = 'blood',
                        afis_details = {
                            'image': 'blood_footprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '0'},
                        afis_processed = False)
    
    # declare afis relevant evidence
    afis_evidence = [bullet, cheque, deskfoot, blood]
    current_evidence = no_evidence



# The game starts here.
label start:
    scene entering_lab_screen

label hallway_intro:
    show screen toolbox_button_screen onlayer over_screens  
    show screen case_files_screen onlayer over_screens    
    scene lab_hallway_idle
    "Welcome to the lab!\nThis is where you can analyze the evidences you have collected from the scene."
    "All of your evidences can be accessed from the evidence bin on the left."
    call screen hallway_screen()

label hallway:
    scene lab_hallway_idle
    show screen toolbox_button_screen onlayer over_screens
    show screen case_files_screen onlayer over_screens  
    hide screen afis_screen
    $ show_evidence = False
    $ show_toolbox = False
    $ current_evidence = no_evidence
    call screen hallway_screen()

label data_analysis_lab:
    scene afis_interface
    show screen toolbox_button_screen onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    show screen case_files_screen onlayer over_screens  
    "Pick digital evidence data in case files to compare prints against known prints from AFIS using CSIpix."
    call screen data_analysis_lab_screen

label materials_lab:
    show screen toolbox_button_screen onlayer over_screens
    show screen case_files_screen onlayer over_screens  
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label fumehood_lab:
    scene fumehood_bg
    show screen toolbox_button_screen onlayer over_screens
    show screen case_files_screen onlayer over_screens  
    "Analyze your evidence using chemical methods here inside the fumehood ."
    show screen back_button_screen('hallway') onlayer over_screens
    "First, put on your gloves!"
    show hands
    call screen gloves

label fumehood_pick:
    hide hands
    show gloved_hands
    "Now let's pick an evidence to analyze"
    hide gloved_hands
    $ process_fumehood = True
    call screen fumehood_screen

label take_bullet:
    scene bullet_ruler with flash
    "Now your can secure the processed physical evidence into a new evidence bag and tape to store safely"
    call screen gun_blue_tobag

label take_cheque:
    scene ninhydrin_take_photo with flash
    "Now your can secure the processed physical evidence into a new evidence bag and tape to store safely"
    call screen ninhydrin_tobag

label wet_lab:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen


# To be called
label end_lab:
    scene lab_hallway_idle
    "Congratulations! You have finished the lab scene part of the tutorial."
    "Let's head on over to the court room."
    scene enter_courtroom_screen 

    return
