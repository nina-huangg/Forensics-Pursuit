# ----- Mouse -----
define config.mouse = { }
define config.mouse['tape'] = [('/images/mouse/evident_tape_resized.png', 0, 0)]
define config.mouse['duster']= [('/images/mouse/magnetic_powder_resized.png', 0, 0)]
define config.mouse['evidence_bags'] = [('/images/mouse/evidence_bags_resized.png', 0, 0)]
define config.mouse['evidence_markers'] = [('/images/mouse/evidence_markers_resized.png', 0, 0)]
define config.mouse['uv_light'] = [('/images/mouse/uv_light_resized.png', 0, 0)]
define config.mouse['scalebar'] = [('/images/mouse/scalebar_resized.png', 0, 0)]
define config.mouse['lifting_tape'] = [('/images/mouse/lifting_tape_resized.webp', 0, 0)]
define config.mouse['tape_print_scalebar'] = [('/images/mouse/tape_print_scalebar_resized.webp', 0, 0)]
define config.mouse['flattener'] = [('/images/mouse/flattener_resized.png', 0, 0)]
define config.mouse['laminate'] = [('/images/mouse/laminate_resized.png', 0, 0)]

# ----- Toolboxes -----
default shoeprint_tools = {"duster": False, "lifter": False, "flattener": False, "laminate": False}
default fingerprint_tools = {"tape" : False, "bag": False, "powder": False, "marker": False, "scalebar": False, "light": True, "lifting_tape": False}
default als_tools = {"flashlight": False}
default luminol_tools = {}
default kmt_tools = {}


# Dust level variable
default dust = 0
    
label start:
    call screen opening_screen

label enter_splash_screen:
    scene entering_splash_screen
    with Dissolve(.8)
    call screen splash_screen

label intro:
    hide entering_splash_screen
    scene house
    "A person supposedly took their own life with a firearm. However the scene looks suspicious..."
    "While the person and firearm has been removed, you are to investigate what happened and pick up any clues."
    call screen entrance_screen

label room:
    hide house
    scene room_side
    "You are in the living room of the house. There seems to be some fluids on the floor..."
    call screen inspect_room
    
label examine_shoeprint:
    scene room_floor_0
    "Hmm seems like something is there..."
    call screen shoeprint_toolbox_contracted

label shoeprint_toolbox:
    hide screen shoeprint_toolbox_contracted
    show screen shoeprint_toolbox_expanded
    "There seems to be oil on the floor. Try using the duster and dust powder to make out its shape."

label shoeprint_duster:
    show screen shoeprint_toolbox_expanded
    $ default_mouse = 'duster'
    $ dust_level = dust if dust <= 5 else 5
    $ result = renpy.call_screen("update_dust")
    if result == "next_dust_level":
        $ dust += 1
        jump shoeprint_duster
    elif result == "complete_dusting":
        jump shoeprint_duster_complete

label shoeprint_duster_complete:
    if dust < 3:
        "The shoeprint is really faint...might need a little more dusting."
        # return to the dusting screen
        jump shoeprint_duster
    elif dust == 3:
        "Perfect amount of dusting! Looks clearly like a shoeprint. Let's proceed with collecting it."
        # continue to next stage
        jump shoeprint_lifter
    else:
        "Too much dusting! You have to restart."
        $ dust = 0
        jump shoeprint_duster

label shoeprint_lifter:
    scene room_floor_4
    $ default_mouse = None
    "Click on the gelatin lifter to lift the shoeprint."
    jump drag_lifter

label drag_lifter:
    call screen lifter_drag_drop

label shoeprint_lifter_complete:
    hide screen lifter_drag_drop
    scene room_floor_lifter
    "Lifter has been placed... but there seems to be air pockets. This might effect the result of our lifted shoeprint."
    "Click on the flatten roller to get rid of the air pockets between the lifter and the floor."
    pause

label shoeprint_flattener:
    $ default_mouse = 'flattener'
    call screen flattener 

transform shoeprint_lifted:
    zoom 0.5

label shoeprint_flattener_complete:
    $ default_mouse = None
    scene room_floor_flattened
    "Looks good!"
    "Press space to lift and take a look at the collected shoeprint"
    show shoeprint_lifted at shoeprint_lifted, Position(xalign=0.5, yalign=0.5)
    "Now click on the laminater to seal off this shoeprint."
    pause

label shoeprint_laminate:
    hide shoeprint_lifted
    $ default_mouse = 'laminate'
    call screen laminate_screen
    

label shoeprint_complete:
    hide screen shoeprint_toolbox_expanded
    $ default_mouse = None
    scene room_side
    "Now that the shoeprint is laminated, we can proceed with the investigation."
    call screen inspect_room

label center:
    scene room_front
    "If a firearm was involved in the taking of ones life, there should be blood but there appears to be no blood..."
    "Lets take a closer look at the wall."
    call screen examine_center

label examine_wall:
    scene wall 
    "Hmm...don't see any blood."
    "Sometimes using alternative light sources at an oblique angle can reveal traces not visible to the human eye."
    "But before using ALS, we should ensure we are in a dark room."
    "Lets close the curtains first."
    jump curtains

label curtains:
    scene curtains 
    call screen close_curtains

label curtains_closed:
    scene curtains_closed 
    "Woah thats dark! Lets revisit the wall, this time for ALS examination."
    scene wall_toolbox_dark
    call screen blood_toolbox_contracted
    
label blood_toolbox:
    hide screen bloodt_toolbox_contracted
    show screen blood_toolbox_expanded
    pause 

label blood_uv_light:
    scene wall_als
    call screen dark_overlay_with_mouse
    pause

label presumptive_test:
    scene wall_als_dark
    "Woah there sure was something!"
