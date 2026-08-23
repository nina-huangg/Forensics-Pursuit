# Developer-only tooling. Nothing here is discoverable in game: there are no menu
# entries, no indicators and no help text, and every hotkey is inert unless dev
# mode is on. Delete this file to strip the whole feature.
#
#   Ctrl+Shift+D   toggle developer mode
#   Ctrl+Shift+J   jump to a scene          (dev mode only)
#   Ctrl+Shift+H   toggle the state HUD     (dev mode only)

default dev_mode = False
default dev_hud = False

init python:

    def apply_dev_skip_settings():
        """Skipping is player-facing normally, so it follows dev_mode.

        Ren'Py refuses to skip text the player has not already read, which is
        exactly the case worth skipping when testing new content.
        """
        _preferences.skip_unseen = store.dev_mode
        config.allow_skipping = True
        config.fast_skipping = store.dev_mode

        # options.rpy empties config.keymap["skip"]; restore hold-to-skip in dev.
        config.keymap["skip"] = ["K_LCTRL", "K_RCTRL"] if store.dev_mode else []

        # Required: this edits the keymap at runtime, so the cached binding
        # would otherwise stay stale. (The rollback edit in options.rpy runs at
        # init and needs no such call.)
        renpy.display.behavior.clear_keymap_cache()

    def toggle_dev_mode():
        store.dev_mode = not store.dev_mode
        if not store.dev_mode:
            store.dev_hud = False
            renpy.hide_screen("dev_jump_menu")
            renpy.hide_screen("dev_state_hud")
        apply_dev_skip_settings()
        renpy.notify("Developer mode " + ("ON" if store.dev_mode else "OFF"))
        renpy.restart_interaction()

    def toggle_dev_hud():
        # Shown explicitly rather than via config.overlay_screens: overlay
        # screens are suppressed in some contexts (interface.suppress_overlay),
        # and a debug readout should appear whenever it is switched on.
        if not store.dev_mode:
            return
        store.dev_hud = not store.dev_hud
        if store.dev_hud:
            renpy.show_screen("dev_state_hud")
        else:
            renpy.hide_screen("dev_state_hud")
        renpy.restart_interaction()

    def open_dev_jump_menu():
        if not store.dev_mode:
            return
        renpy.show_screen("dev_jump_menu")
        renpy.restart_interaction()

    # ---- jump targets ------------------------------------------------------
    # Jumping mid-scenario needs the route initialised first, or the target
    # reads uninitialised state (empty toolbox, no samples, no case files).

    def dev_setup_collection():
        initialize_collection_route()

    def dev_setup_lab():
        initialize_standalone_lab_route()
        reset_lab_gameplay_state()

    def dev_setup_courtroom():
        initialize_courtroom_route()
        enter_courtroom_ui()

    # (label, caption, setup callable)
    DEV_JUMP_TARGETS = [
        ("study_bg",                     "Crime scene - the study",       dev_setup_collection),
        ("lab_hallway_intro",            "Lab - intro",                   dev_setup_lab),
        ("bio_station",                  "Lab - biology station",         dev_setup_lab),
        ("impression_station",           "Lab - AFIS / fingerprints",     dev_setup_lab),
        ("cem_finish",                   "Lab - allele table",            dev_setup_lab),
        ("courtroom_start",              "Courtroom - from the top",      dev_setup_courtroom),
        ("court_generate_first_question","Courtroom - examination",       dev_setup_courtroom),
        ("court_evaluation_sec",         "Courtroom - evaluation",        dev_setup_courtroom),
    ]

    def dev_jump_to(label_name, setup):
        renpy.hide_screen("dev_jump_menu")
        if setup is not None:
            setup()
        renpy.jump(label_name)

    config.keymap["dev_mode_toggle"] = ["ctrl_shift_K_d"]
    config.keymap["dev_jump_menu"] = ["ctrl_shift_K_j"]
    config.keymap["dev_hud_toggle"] = ["ctrl_shift_K_h"]

    # Bound through config.underlay rather than config.overlay_screens: the
    # underlay is walked on every interaction, including the `call screen`
    # station screens where the quick_menu overlay does not appear.
    config.underlay.append(renpy.Keymap(
        dev_mode_toggle=toggle_dev_mode,
        dev_jump_menu=open_dev_jump_menu,
        dev_hud_toggle=toggle_dev_hud,
    ))


screen dev_state_hud():
    zorder 400

    if dev_mode and dev_hud:
        # Values are computed here rather than inside the text tags: Ren'Py
        # interpolation uses string.Formatter field names, which cannot call
        # functions like len().
        $ _ev_count = len(evidence._inventory)
        $ _tb_count = len(toolbox._inventory)

        frame:
            xpos 10
            ypos 30
            background "#0b1620ee"
            padding (14, 10)

            vbox:
                spacing 3

                text "DEV":
                    size 15
                    bold True
                    color "#ffd479"

                text "route [game_route]  loc [location]":
                    size 14
                    color "#c5d0d8"
                text "track [analysis_track]  ev [_ev_count]  tools [_tb_count]":
                    size 14
                    color "#c5d0d8"
                text "score [evidence_score]  mistakes [evidence_wrong_moves]":
                    size 14
                    color "#c5d0d8"

                for _t, _done in tasks.items():
                    text "[_t]: [_done]":
                        size 13
                        color ("#7ddc9a" if _done else "#8fa6b4")


screen dev_jump_menu():
    zorder 450
    modal True

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 740
        background "#0b1620f2"
        padding (30, 24)

        vbox:
            spacing 10

            text "Jump to scene":
                size 26
                bold True
                color "#ffd479"

            for _lbl, _caption, _setup in DEV_JUMP_TARGETS:
                textbutton "[_caption]":
                    text_size 20
                    text_color "#dceaf2"
                    text_hover_color "#ffffff"
                    background "#17354a"
                    hover_background "#245273"
                    padding (16, 8)
                    xfill True
                    action Function(dev_jump_to, _lbl, _setup)

            textbutton "Close":
                text_size 20
                text_color "#8fa6b4"
                padding (16, 8)
                xalign 1.0
                action Hide("dev_jump_menu")

    key "K_ESCAPE" action Hide("dev_jump_menu")
