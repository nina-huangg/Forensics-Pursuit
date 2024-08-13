
# ----- Variables -----
default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default default_mouse = None
define flash = Fade(0.1, 0.0, 0.5, color="#fff")


default dust = 0
default default_tools = ["default", "camera"]
default shoeprint_tools = ["shoeprint", "marker", "duster", "lifter", "flattener", "laminate", "evidence_bags"]
default table_tools = ["table", "evidence_bags"]
default swab_tools = ["wall", "uv_light", "marker", "swab", "ethanol", "reagent", "hydrogen_peroxide", "evidence_bags"]
default resample_tools = ["resample", "swab", "evidence_bags"]
default case_files = []
default inspection = {"floor": False, "table": False, "wall": False}
default collectable = ["bottle", "vase", "swab", "shoeprint"]

default steps = {"shoeprint": 1, "table": 1, "wall":1, "resample": 1}

default result = ""


# ----- Transforms -----
transform half_size:
    zoom 0.5

transform shoeprint_lifted:
    zoom 0.5

transform red_swab:
    xpos 0
    ypos 0
    zoom 0.3


init python:
    
    global steps

    global dust_result 
    dust_result = ""

    def reset_toolbox():
        global show_toolbox
        show_toolbox = False

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor

    def dragged_func(dragged_items, dropped_on):
        if dropped_on is not None:
            if dragged_items[0].drag_name == "lifter" and dropped_on.drag_name == "sheet":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.jump("shoeprint_lifter_placed")
            if dragged_items[0].drag_name == "photo_dark" and dropped_on.drag_name == "evidence_bag":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.jump("placed_photo_in_evidence_bag_complete")
            if dragged_items[0].drag_name == "luminol_photo" and dropped_on.drag_name == "evidence_bag":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.jump("seal_bag")
            if dragged_items[0].drag_name == "bottle" and dropped_on.drag_name == "evidence_bag":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.jump("seal_bottle")
    
    def return_mouse_pos():
        return renpy.get_mouse_pos()

    def remove_collectable(item):
        global collectable
        collectable.remove(item)
        case_files.append(item)
        renpy.restart_interaction()

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

    bottle = Evidence(name = 'bottle',
                                afis_details = {
                                    'image': 'bottle-idle',
                                    'xpos':0.18, 'ypos':0.25,
                                    'score': '70'})
    vase = Evidence(name = 'vase',
                                afis_details = {
                                    'image': 'vase-idle',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})

    config.mouse = {
        "duster": [('/images/mouse/magnetic_powder_resized.png', 0, 0)],
        "lifter": [('/images/mouse/lifter_resized.png', 0, 0)],
        "flattener": [('/images/mouse/flattener_resized.png', 0, 0)],
        "laminate": [('/images/mouse/laminate_resized.png', 0, 0)],
        "evidence_bags": [('/images/mouse/evidence_bags_resized.png', 0, 0)],
        "marker": [('/images/mouse/markers_resized.png', 0, 0)],
        "uv_light": [('/images/mouse/uv_light_resized.png', 0, 0)],
        "swab": [("/images/mouse/swab_resized.png", 0, 0)],
        "ethanol": [("/images/mouse/dropper liquid.png", 0, 95)],
        "reagent": [("/images/mouse/dropper reagent.png", 0, 95)],
        "hydrogen_peroxide": [("/images/mouse/dropper liquid.png", 0, 95)],


        
        "blue_star": [('/images/mouse/blue_star_resized.png', 0, 0)]
    }

    config.layers.append("overlay")



label start:
    call screen start_screen

label splash:
    scene entering_splash_screen
    with Dissolve(.8)
    call screen splash_screen

label doorway:
    hide screen splash_screen
    scene doorway
    "The resident of this house was reported dead in the living room. He was found lying on the floor, with appearant head injuries."
    "From police reports, the victim has taken a blow to the head enough to cause bleeding. While the body has been removed, you are tasked with collecting any remaining evidence."
    "Collected evidence can be brought back to the lab for further analysis."
    call screen doorway_screen

label main_room_intro:
    scene main_room
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    "You are in the living room. This is where the body was found."
    "Move cursor around to find places to examine in closer detail."
    call screen main_room_screen

label main_room:
    $ default_mouse = None
    hide screen case_files_screen
    hide screen toolbox_button_screen
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(default_tools) onlayer over_screens
    call screen main_room_screen

label proceed_to_lab:
    hide screen back_button_screen
    hide screen toolbox_button_screen
    hide screen case_files_screen
    $ show_case_files = False 
    $ show_toolbox = False 
    scene entering_lab_screen
    window hide
    $ renpy.pause(hard=True)

label floor:
    hide screen main_room_screen
    hide screen case_files_screen
    hide screen toolbox_button_screen
    scene floor
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(shoeprint_tools) onlayer over_screens
    show screen back_button_screen('main_room') 
    if not inspection['floor']:
        "There appears to be oil on the floor. Click on the toolbox for the appropriate tools to further inspect the floor."
        "Place evidence markers on the oil stains."
        window hide
        $ renpy.pause(hard=True)
    else:
        "You've already collected a sample from this area."
        window hide
        $ renpy.pause(hard=True)

label shoeprint_marker:
    hide screen back_button_screen
    scene floor
    call screen shoeprint_marker_screen
    $ steps["shoeprint"] += 1
    scene shoeprint_marker_placed
    "Now use the duster to dust for the shoeprint."
    window hide
    $ renpy.pause(hard=True)


label shoeprint_duster:
    hide screen back_button_screen
    hide screen shoeprint_marker_screen 
    $ result = renpy.call_screen("shoeprint_duster_screen", dust)
    if result == "next_dust_level":
        $ dust += 1
        jump shoeprint_duster
    elif result == "dusting_complete":
        jump check_shoeprint_duster

label check_shoeprint_duster:
    if dust < 3:
        scene expression "shoeprint_dusting_{}".format(dust)
        "The shoeprint is really faint...might need a little more dusting."
        jump shoeprint_duster
    elif dust == 5:
        scene expression "shoeprint_dusting_{}".format(dust)
        "Too much dusting! You have to restart."
        $ dust = 0
        jump shoeprint_duster
    else:
        scene expression "shoeprint_dusting_{}".format(dust)
        "Perfect amount of dusting! Looks clearly like a shoeprint. Let's proceed with collecting it."
        "Click on the gelatin lifter to lift the shoeprint."
        $ steps["shoeprint"] += 1
        $ default_mouse = None
        window hide
        $ renpy.pause(hard=True)
        

label shoeprint_lifter:
    hide screen shoeprint_duster_screen
    call screen shoeprint_lifter_screen
    
label shoeprint_lifter_placed:
    scene shoeprint_lifter_placed
    "Lifter has been placed... but there seems to be air pockets. This might effect the result of the lifted shoeprint."
    "Click on the flatten roller to get rid of the air pockets between the lifter and the floor."
    $ steps["shoeprint"] += 1
    $ default_mouse = None
    window hide
    $ renpy.pause(hard=True)

label shoeprint_flattener:
    hide screen shoeprint_lifter_screen
    call screen shoeprint_flattener_screen
    scene shoeprint_flattened
    $ default_mouse = None
    "The air pockets have been removed. The shoeprint has been successfully lifted."
    "Press space to lift and take a look at the collected shoeprint"
    show expression "floor/shoeprint_lifted.png" at shoeprint_lifted, Position(xalign=0.5, yalign=0.5)
    "Now we need to put the shoeprint in a laminate to preserve it."
    "Click on the laminater to laminate the shoeprints."
    $ steps["shoeprint"] += 1
    window hide
    $ renpy.pause(hard=True)

label shoeprint_laminate:
    call screen shoeprint_laminate_screen
    show expression "floor/shoeprint_laminated_idle.png" at shoeprint_lifted, Position(xalign=0.5, yalign=0.5)
    "Click on the evidence bags to collect the shoeprint"
    $ steps["shoeprint"] += 1
    $ default_mouse = None
    window hide
    $ renpy.pause(hard=True)
    
label shoeprint_evidence_bags:
    hide shoeprint_laminate_screen
    hide expression "floor/shoeprint_lifted.png"
    scene shoeprint_marker_placed
    call screen shoeprint_evidence_bags_screen
    window hide 
    $ renpy.pause(hard=True)

label shoeprint_complete:
    $ steps["shoeprint"] += 1 
    hide screen shoeprint_collect_screen
    scene shoeprint_marker_placed
    show screen back_button_screen('main_room')
    "Shoeprint has been successfully collected. You can see the shoeprint collected under case files."
    "Return to the main room."
    $ inspection['floor'] = True
    window hide
    $ renpy.pause(hard=True)

label table:
    hide screen main_room_screen
    hide screen case_files_screen
    hide screen toolbox_button_screen
    scene table_no_items
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(table_tools) onlayer over_screens
    show screen back_button_screen('main_room') 
    if "vase" not in collectable and "bottle" not in collectable:
        $ default_mouse = None
        $ inspection["table"] = True
    if not inspection['table']:
        call screen table_screen
        window hide
        $ renpy.pause(hard=True)

    else:
        "You've already collected the samples from this area."
        window hide
        $ renpy.pause(hard=True)

label table_evidence_bags:
    call screen table_collect_evidence_screen

label table_complete:
    scene table_no_items
    show screen back_button_screen('main_room')
    "You've collected all the samples from this area."
    $ default_mouse = None
    hide screen toolbox_button_screen
    window hide
    $ renpy.pause(hard=True)

label wall:
    if not inspection['wall']:
        hide screen main_room_screen
        scene wall
        show screen back_button_screen('main_room') 
        "Hmm...don't see any blood."
        "Sometimes using alternative light sources at an oblique angle can reveal traces not visible to the human eye."
        "But before using ALS, we should ensure we are in a dark room."
        "Lets close the curtains first."
        jump close_curtains
    else:
        scene wall
        "You've already collected a sample from this area."
        show screen back_button_screen('main_room')

label close_curtains:
    scene curtains 
    call screen close_curtains_screen

label curtains_closed:
    scene curtains_closed 
    hide screen case_files_screen
    hide screen toolbox_button_screen
    $ show_toolbox = False
    show screen case_files_screen(case_files) onlayer over_screens
    show screen toolbox_button_screen(swab_tools) onlayer over_screens
    "Now that it is dark, lets revisit the wall, this time for ALS examination."
    jump revisit_wall


label revisit_wall:
    hide screen main_room_screen
    hide screen back_button_screen
    
    scene wall_dark 
    "Use the flashlight from toolbox for any signs of blood."
    window hide 
    $ renpy.pause(hard=True)


label wall_uv_light:
    $ result = renpy.call_screen("dark_overlay_with_mouse")
    if result == "found_blood":
        $ default_mouse = None
        scene wall_blood_outline
        "Using oblique lighting, you have found splatters on the wall that were invisible to the naked eye."
        "A faint outline has been marked so you remember where this is, but this is not actually in the crime scene."
        "Place evidence markers on the splatters before conducting any tests."
        $ steps["wall"] += 1
        window hide
        $ renpy.pause(hard=True)

label wall_marker:
    call screen blood_marker_screen
    $ default_mouse = None
    $ steps["wall"] += 1
    scene wall_blood_marker_placed
    "We need to analyze the splat pattern and ensure that this is indeed blood. How should we proceed?"
    jump make_choice

label make_choice: 
    menu:
        "Spray luminol": 
            "If we spray luminol, the remaining blood will be contaminated by chemicals, and the presumptive test will not behave as expected."
            jump make_choice
        "Presumptive test": 
            "Get a swab from the toolbox before clicking on the blood to get a sample"
            window hide
            $ renpy.pause(hard=True)

label wall_swab:
    call screen swab_sample_screen
    $ steps["wall"] += 1
    scene wall_with_background
    show screen red_swab_screen
    "You have retrieved a sample. Conduct presumptive test to see if it is blood."
    window hide 
    $ renpy.pause(hard=True)

label wall_ethanol:
    call screen ethanol_screen
    $ steps["wall"] += 1
    "You have added ethanol."
    window hide 
    $ renpy.pause(hard=True)

label wall_reagent:
    call screen reagent_screen
    $ steps["wall"] += 1
    "You have added reagent."
    window hide 
    $ renpy.pause(hard=True)

label wall_hydrogen_peroxide:
    call screen hydrogen_peroxide_screen
    "You have added hydrogen peroxide."
    hide screen hydrogen_peroxide_screen
    # timer animation

    show screen pink_swab_screen
    "The results show it is indeed blood. We should resample on a new swab to get the blood without any chemicals mixed in it."
    hide screen pink_swab_screen
    hide screen red_swab_screen
    scene wall_blood_marker_placed 

    hide screen toolbox_button_screen
    show screen toolbox_button_screen(resample_tools) onlayer over_screens
    window hide 
    $ renpy.pause(hard=True)

label resample_swab:
    scene wall_blood_marker_placed 
    call screen new_swab_screen
    $ steps["resample"] += 1
    jump resample_evidence_bags

label resample_evidence_bags:
    scene wall_with_background
    show screen back_button_screen('main_room')
    call screen collect_swab_screen
    window hide 
    $ renpy.pause(hard=True)

label wall_complete:
    "You've collected all the samples from this area."
    window hide
    $ renpy.pause(hard=True)


