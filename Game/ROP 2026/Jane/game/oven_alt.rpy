init python:
    import math
    def dial_events(event, x, y, st):
        global dial_rotate
        global old_mousepos
        global old_degrees
        global degrees
        global dial_start_rotate
        global dial_text
        global dial_number
        global previous_dial_text
        global dial_changed
        global combination_check
        global combination_length
        global completed_combination_numbers
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONDOWN:
            if event.button == 1:
                if dial_start_rotate:   # left mouse
                    if dial_sprite.x <= x <= dial_sprite.x + dial_size[0] + dial_offset and dial_sprite.y <= y <= dial_sprite.y + dial_size[1] + dial_offset:
                        dial_rotate = True
                        old_mousepos = (x, y)
                        angle_radians = math.atan2((dial_sprite.y + dial_size[1] - dial_offset / 2) - y, (dial_sprite.x + dial_size[0] - dial_offset / 2) - x)
                        old_degrees = math.degrees(angle_radians) % 360
                else:
                    if dial_sprite.x <= x <= dial_sprite.x + dial_size[0] and dial_sprite.y <= y <= dial_sprite.y + dial_size[1]:
                        dial_rotate = True
                        old_mousepos = (x, y)
                        angle_radians = math.atan2((dial_sprite.y + dial_size[1] / 2) - y, (dial_sprite.x + dial_size[0] / 2) - x)
                        old_degrees = math.degrees(angle_radians) % 360
        elif event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                dial_rotate = False
                # safe = "safe_{}".format(current_safe)
                # if dial_changed:
                #     if combination_length < 4:
                #         dial_changed = False
                #         combination_check = None
                #         if len(completed_combination_numbers) == 0:
                #             completed_combination_numbers[safe] = []
                #             completed_combination_numbers[safe].append(dial_text)
                #         else:
                #             completed_combination_numbers[safe].append(dial_text)
                #         combination_length += 1
                #     if combination_length == 4:
                #         if completed_combination_numbers[safe] == combinations[safe]:
                #             dial_changed = False
                #             combination_length = 0
                #             completed_combination_numbers = {}
                #             combination_check = "correct"
                #             renpy.play("audio/success.ogg", "sound")
                #         else:
                #             dial_changed = False
                #             combination_length = 0
                #             completed_combination_numbers = {}
                #             combination_check = "wrong"
                #             renpy.play("audio/error.ogg", "sound")
                renpy.restart_interaction()
        elif event.type == renpy.pygame_sdl2.MOUSEMOTION:
            if dial_rotate:
                angle_radians = math.atan2((dial_sprite.y + dial_size[1] / 2) - y, (dial_sprite.x + dial_size[0] / 2) - x)
                degrees = math.degrees(angle_radians) % 360
                rotate_amount = math.hypot(x - old_mousepos[0], y - old_mousepos[1]) / 5
                if degrees > old_degrees:
                    dial_sprite.rotate_amount += rotate_amount
                elif degrees < old_degrees:
                    dial_sprite.rotate_amount -= rotate_amount

                t = Transform(child = dial_image, zoom = 0.5)
                t.rotate = 0.7 * round(dial_sprite.rotate_amount / 0.7)
                if int(t.rotate / 0.7) % 500 == 0 and int(t.rotate / 0.7) != 0:
                    dial_number = 0
                    dial_sprite.rotate_amount = 0.0
                else:
                    dial_number = int(t.rotate / 0.7)

                if dial_number > 0:
                    dial_text = 500 - dial_number
                elif dial_number < 0:
                    dial_text = abs(dial_number)
                else:
                    dial_text = dial_number

                dial_text = round(dial_text / 50) * 50
                
                if dial_text != previous_dial_text:
                    dial_changed = True
                    renpy.music.play("audio/dial.ogg", "sound", relative_volume = 0.3)
                
                previous_dial_text = dial_text

                t.subpixel = True
                dial_start_rotate = True
                dial_sprite.set_child(t) 
                dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2 - dial_offset
                dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2 - dial_offset
                old_degrees = math.degrees(angle_radians) % 360
                old_mousepos = (x, y)
                dial_sprite_manager.redraw(0)
                renpy.restart_interaction()

    def reset_safe():
        global dial_number
        global dial_text
        global completed_combination_numbers
        global combination_length
        global combination_check
        global dial_start_rotate

        dial_number = 0
        dial_text = 0
        dial_sprite.rotate_amount = 0
        completed_combination_numbers = {}
        combination_length = 0
        combination_check = None
        dial_start_rotate = False

        t = Transform(child = dial_image, zoom = 0.5)
        dial_sprite.set_child(t)
        dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
        dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
        dial_sprite_manager.redraw(0)
        

screen scene_1:
    image "images/scene-1-background.png" at half_size
    imagebutton auto "images/scene-1-safe-door-%s.png" focus_mask True action [Show("safe_puzzle", Fade(1, 1, 1)), Hide("scene_1")] at half_size

screen safe_opened:
    on "show" action Hide("safe_puzzle")
    image "safe-opened-background.png" at half_size
    imagebutton auto "images/back-button-%s.png" action [Show("scene_1", Fade(1, 1, 1)), Hide("safe_opened")] align(0.95, 0.95) at half_size
    if current_safe == 1:
        imagebutton auto "book-%s.png" focus_mask True action NullAction() at half_size

screen safe_puzzle:
    # on "show" action Function(reset_safe)
    image "images/safe-closeup-background.png" at half_size
    # if combination_check == "wrong":
    #     imagebutton auto "images/safe-handle-ind-red-%s.png" focus_mask True action Play(file = "audio/locked-door.ogg", channel = "sound") at half_size
    # elif combination_check == "correct":
    #     imagebutton auto "images/safe-handle-ind-green-%s.png" focus_mask True action [Play(file = "audio/open-door.ogg", channel = "sound"), Show("safe_opened", Fade(1, 1, 1))] at half_size
    # elif combination_check == None:
    #     imagebutton auto "images/safe-handle-ind-normal-%s.png" focus_mask True action Play(file = "audio/locked-door.ogg", channel = "sound") at half_size
    image "images/dial-shadow.png" align(0.48, 0.5) alpha 0.3 at half_size
    image "images/dial-backing.png" align(0.5, 0.5) at half_size
    add dial_sprite_manager
    imagebutton auto "images/dial-reset-button-%s.png" align(0.5, 0.5) focus_mask True action Function(reset_safe) at half_size
    imagebutton auto "images/oven-button-%s.png" align(0.8, 0.5) focus_mask True action Jump("evaluate") at half_size
    image "images/dial-text-background.png" align(0.5, 0.17) at half_size
    imagebutton auto "images/back-button-%s.png"align(0.95, 0.95) action [Show("scene_1", Fade(1, 1, 1)), Hide("safe_puzzle")] at half_size
    text "[dial_text]" color "#000000" align(0.505, 0.18) text_align 0.5

transform half_size:
    zoom 0.5

label oven_start:
    # Dial variables
    $ dial_image = "images/dial.png"
    $ dial_size = (660 / 2, 660 / 2)
    $ t = Transform(child = dial_image, zoom = 0.5)
    $ dial_sprite_manager = SpriteManager(event = dial_events)
    $ dial_sprite = dial_sprite_manager.create(t)
    $ dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
    $ dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
    $ dial_rotate = False
    $ dial_sprite.rotate_amount = 0
    $ dial_offset = 68.2
    $ dial_start_rotate = False
    $ dial_number = 0
    $ dial_text = 0
    $ previous_dial_text = 0
    $ dial_changed = False

    # Other variables
    $ old_mousepos = (0.0, 0.0)
    $ degrees = 0
    $ old_degrees = 0
    $ combinations = {"safe_1" : 50, "safe_2" : [23, 5, 75, 44]}
    $ completed_combination_numbers = {}
    $ combination_check = None
    $ current_safe = 1
    $ combination_length = 0
    call screen scene_1
    return

label evaluate:
    show screen safe_puzzle
    python:
        global dial_text
        safe = "safe_{}".format(current_safe)
        if dial_text == combinations[safe]:
            renpy.say(None, "You got it!")
        else:
            renpy.say(None, "Not it!")
    call screen safe_puzzle