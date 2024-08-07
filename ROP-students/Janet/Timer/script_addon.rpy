# TODO: Add the command "jump timer" to the appropriate block in your script.rpy!
# (timer is the label from timer.rpy)
### Example (from my code):
# label fumigation:
#     scene chamber_outside
#     "Let's time this. How long should the fuming process take?"
#     jump timer

label timer_set:
    
    # TODO: Call the background image of your scene here. See my script.rpy in fp lab level on GitHub if you want an example.
    
    # TODO: Input min and max times. If there is no min then input all 0 for min values, and if there is no max then input 9 for all max values.
    # Example values are for 7min 50sec and 10min 10sec.
    $ min_hours = 0 # TODO: Replace this with your own value.
    $ min_minutes = 7 # TODO: Replace this with your own value.
    $ min_seconds = 50 # TODO: Replace this with your own value.
    $ max_hours = 0 # TODO: Replace this with your own value.
    $ max_minutes = 10 # TODO: Replace this with your own value.
    $ max_seconds = 10 # TODO: Replace this with your own value.

    # Calculations
    $ min_time = min_hours * 3600 + min_minutes * 60 + min_seconds
    $ max_time = max_hours * 3600 + max_minutes * 60 + max_seconds
    $ true_time = time_numbers[5] + time_numbers[4] * 10 + time_numbers[3] * 60 + time_numbers[2] * 600 + time_numbers[1] * 3600 + time_numbers[0] * 36000

    # Default messsages, customize to your liking
    if true_time >= min_time and true_time <= max_time:
        "That's correct."
        $ string_min_1 = "%d" % time_numbers[2]
        $ string_min_2 = "%d" % time_numbers[3]
        $ string_sec_1 = "%d" % time_numbers[4]
        $ string_sec_2 = "%d" % time_numbers[5]
        if string_min_1 == "0":
            if string_sec_1 != "0":
                "Waiting for [string_min_2] minutes and [string_sec_1][string_sec_2] seconds... (press space to continue)"
            elif string_sec_2 != "0":
                "Waiting for [string_min_2] minutes and [string_sec_2] seconds... (press space to continue)"
            else:
                "Waiting for [string_min_2] minutes... (press space to continue)"
        else:
            if string_sec_1 != "0" and string_sec_2 != "0":
                "Waiting for [string_min_1][string_min_2] minutes and [string_sec_1][string_sec_2] seconds... (press space to continue)"
            elif string_sec_2 != "0":
                "Waiting for [string_min_1][string_min_2] minutes and [string_sec_2] seconds... (press space to continue)"
            else:
                "Waiting for [string_min_1][string_min_2] minutes... (press space to continue)"
        jump timer_completed
    elif true_time < min_time:
        "That's not enough time, try again."
        jump timer
    elif true_time > max_time:
        "That's too much time, try again."
        jump timer