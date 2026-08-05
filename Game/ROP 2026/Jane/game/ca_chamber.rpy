default ca_chamber_water_added    = False
default ca_chamber_glue_added     = False
default ca_chamber_firearm_placed = False
default ca_chamber_state          = "empty"   # "empty" -> "loaded" -> "closed"
default ca_chamber_done           = False
default ca_chamber_step    = 1     # checklist image step from 1-8
default ca_pending_mcq     = None  # "water" or "glue" when an mcq is open
default ca_pending_message = None  # queued dialogue line, said from script context

init python:
    def ca_chamber_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if dragged_image == "toolbox-distilled_water" and store.ca_chamber_step == 1 and not store.ca_chamber_water_added:
            store.ca_pending_mcq = "water"
            renpy.show_screen("ca_chamber_amount_check")
        elif dragged_image == "toolbox-superglue" and store.ca_chamber_step == 2 and not store.ca_chamber_glue_added:
            store.ca_pending_mcq = "glue"
            renpy.show_screen("ca_chamber_amount_check")
        elif dragged_image == "inventory-firearm" and store.ca_chamber_step == 3 and not store.ca_chamber_firearm_placed:
            store.ca_chamber_step = 4
            store.ca_chamber_firearm_placed = True
            store.ca_pending_message = "Firearm placed in the CA chamber."
        else:
            store.ca_pending_message = "That doesn't belong in the CA chamber right now."
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def check_ca_amount(item, amount):
        if item == "water":
            if 100 <= amount <= 200:
                store.ca_chamber_water_added = True
                store.ca_chamber_step = 2
                store.ca_pending_message = "Distilled water added."
            else:
                store.ca_pending_message = "Wrong amount."
        elif item == "glue":
            if 1 <= amount <= 3:
                store.ca_chamber_glue_added = True
                store.ca_chamber_step = 3
                store.ca_pending_message = "Superglue added."
            else:
                store.ca_pending_message = "Wrong amount."

        store.ca_pending_mcq = None
        renpy.hide_screen("ca_chamber_amount_check")
        store.selected_tool = None
        renpy.restart_interaction()

    def close_ca_chamber():
        if store.ca_chamber_state != "empty":
            return
        if not (store.ca_chamber_water_added and store.ca_chamber_glue_added and store.ca_chamber_firearm_placed):
            store.ca_pending_message = "Add the distilled water, superglue, and firearm first."
            return
        store.ca_chamber_state = "closed"
        store.ca_chamber_step = 5
        renpy.restart_interaction()

label ca_chamber:
    $ hide_all_lab_screens()
    $ hide_all_inventory()
    $ location = "ca_chamber"
    scene materials_lab
    show screen ca_chamber_screen
    show screen ca_chamber_checklist
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens

label ca_chamber_load_dialogue:
    if ca_chamber_done or ca_chamber_state != "closed":
        jump ca_chamber_wait_step

    hide screen ca_chamber_screen

    $ reset_ca_chamber_entry()
    $ ca_correct_temp_start = "120"
    $ ca_correct_temp_end   = "151"
    $ ca_correct_time_start = "12"
    $ ca_correct_time_end   = "16"
    $ ca_correct_label      = "ca_chamber_settings_confirmed"
    $ ca_incorrect_label    = "ca_chamber_settings_incorrect"

    call screen ca_chamber_main_interface

label ca_chamber_settings_incorrect:
    n normal1 "That's not quite right. Remember: 120-150 degrees, 12-15 minutes."
    call screen ca_chamber_main_interface

label ca_chamber_settings_confirmed:
    hide screen ca_chamber_keyboard
    hide screen ca_chamber_temperature_screen
    hide screen ca_chamber_cooking_time_screen
    hide screen ca_chamber_checklist
    $ ca_chamber_state = "loaded"
    $ ca_chamber_step = 6
    n normal1 "You've correctly set the CA chamber between 120-150 degrees for 12-15 minutes!"
    show screen ca_chamber_screen
    show screen ca_chamber_checklist
    n normal1 "Now wait an additional 5 minute purging period..."
    jump ca_chamber_purging_complete

label ca_chamber_purging_complete:
    n normal1 "Purging complete."
    $ ca_chamber_step = 7
    jump ca_chamber_wait_step

label ca_chamber_wait_step:
    if ca_pending_message:
        $ ca_wait_msg = ca_pending_message
        $ ca_pending_message = None
        n normal1 "[ca_wait_msg]"
    if ca_chamber_state == "loaded" and not ca_chamber_done:
        jump ca_chamber_finish
    $ renpy.pause(0.2)
    jump ca_chamber_wait_step

label ca_chamber_finish:
    $ ca_chamber_done = True
    $ ca_chamber_step = 8
    hide screen ca_chamber_screen
    hide screen inventory
    hide screen back_button_screen onlayer over_screens
    show firearm_fumed at Transform(xalign=0.5, yalign=0.1)
    n normal1 "The superglue fumes have bonded to the fingerprint."
    n normal3 "Let's take the firearm out and capture a macro photograph of it."
    hide firearm_fumed
    show firearm_fingerprint at Transform(xalign=0.5, yalign=0.1)
    "You took a photo of the fingerprints on the fumed firearm."
    $ ca_chamber_step = 8
    n normal1 "CA Fuming checklist complete!" 
    hide firearm_fingerprint
    hide screen ca_chamber_checklist
    hide screen ca_chamber_amount_check
    $ evidence.add_to_inventory(evids_by_key["firearm_fingerprint"])
    jump materials_lab