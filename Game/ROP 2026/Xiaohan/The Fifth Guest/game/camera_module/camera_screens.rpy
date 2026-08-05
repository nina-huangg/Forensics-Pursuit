## Camera Module - Screens
## All screens are modal overlays (show screen / hide screen only)
## No label jumps, no scene changes
## Adapted for The Fifth Guest with aperture-image fallbacks

init python:
    from math import ceil

    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))


## ---- Viewfinder ----

screen camera_preview_ui():
    tag camera_overlay
    modal True
    zorder 100

    # Full black background
    add Solid("#000000ff")

    $ _cs = camera_state
    $ _cc = camera_config
    $ _cur_loc = current_photo_location
    $ _ap_name = _cc.aperture_group[_cs.aperture]
    $ _ap_num = _ap_name.replace("F", "")
    $ _alpha = _cc.iso_to_alpha.get(_cc.iso_group[_cs.iso_index], 1.0)
    $ _img = camera_get_location_image(_cur_loc, _ap_num)

    add _img xpos _cs.theme_x ypos _cs.theme_y anchor (0.5, 0.5) zoom _cs.theme_zoom alpha _alpha

    if _cs.show_info_overlay:
        add Solid("#00000080") xpos 608 ypos 376 xysize (400, 240)
        vbox:
            xpos 608 ypos 376
            xsize 500
            ysize 240
            spacing 6
            text "ISO: [_cc.iso_group[_cs.iso_index]]" size 40 color "#ffffff" font _cc.font
            text "Aperture: [_cc.aperture_group[_cs.aperture]]" size 40 color "#ffffff" font _cc.font
            text "Focal Length: [_cs.focal_len]" size 40 color "#ffffff" font _cc.font

    # Bottom control panel imagemap
    imagemap:
        ground "camera/camera-idle.png"
        hover  "camera/camera-hover.png"
        xpos 0.5 ypos 1.0 anchor (0.5, 1.0)

        # D-pad
        hotspot (1471, 547, 60, 58) action SetField(_cs, "theme_x", _cs.theme_x + 0.02)
        hotspot (1599, 556, 75, 48) action SetField(_cs, "theme_x", _cs.theme_x - 0.02)
        hotspot (1531, 482, 69, 75) action SetField(_cs, "theme_y", _cs.theme_y + 0.02)
        hotspot (1547, 616, 47, 55) action SetField(_cs, "theme_y", _cs.theme_y - 0.02)

        # Zoom in / out
        hotspot (1433, 350, 110, 110) action If(
            (_cs.focal_len == "50mm" and _cs.theme_zoom < 2.0) or
            (_cs.focal_len == "105mm" and _cs.theme_zoom < 4.0),
            SetField(_cs, "theme_zoom", _cs.theme_zoom + 0.02),
            Notify("Cannot zoom in further—please switch lenses first.")
        )
        hotspot (1575, 346, 117, 116) action If(
            (_cs.focal_len == "50mm" and _cs.theme_zoom > 1.0) or
            (_cs.focal_len == "105mm" and _cs.theme_zoom > 3.0),
            SetField(_cs, "theme_zoom", _cs.theme_zoom - 0.02),
            Notify("Cannot zoom out further—please switch lenses first.")
        )

        # Aperture
        hotspot (433, 499, 133, 130) action SetField(_cs, "aperture", max(0, _cs.aperture - 1))
        hotspot (426, 343, 146, 127) action SetField(_cs, "aperture", min(3, _cs.aperture + 1))

        # Take photo button → Python function, no jump
        hotspot (1663, 76, 187, 159) action Function(camera_take_photo)

        # ISO
        hotspot (443, 827, 131, 141) action SetField(_cs, "iso_index", max(0, _cs.iso_index - 1))
        hotspot (422, 656, 153, 139) action SetField(_cs, "iso_index", min(4, _cs.iso_index + 1))

        # Focal length
        hotspot (1432, 710, 287, 117) action [
            SetField(_cs, "focal_len", "50mm"),
            SetField(_cs, "theme_zoom", clamp(_cs.theme_zoom, 1.0, 2.0))
        ]
        hotspot (1434, 852, 281, 111) action [
            SetField(_cs, "focal_len", "105mm"),
            SetField(_cs, "theme_zoom", clamp(_cs.theme_zoom, 3.0, 4.0))
        ]

        # Info toggle
        hotspot (529, 157, 120, 112) action ToggleField(_cs, "show_info_overlay")

    # Progressive photography hints
    textbutton "Hint":
        xpos 40
        ypos 40
        text_size 28
        background "#1f4b63dd"
        hover_background "#2d6f8f"
        padding (18, 10)
        action Function(camera_show_hint)
        tooltip "Get a tip for better settings"

    # ESC to close viewfinder without taking photo
    key "K_ESCAPE" action Function(camera_close_viewfinder)


screen camera_hint_overlay(hint_text=""):
    zorder 110
    modal False

    frame:
        xalign 0.5
        yalign 0.12
        xmaximum 1100
        background "#17354aee"
        padding (24, 18)

        vbox:
            spacing 10
            text "CAMERA HINT" size 22 color "#7ec8e3" bold True
            text "[hint_text]" size 24 color "#ffffff"
            textbutton "Dismiss":
                xalign 1.0
                text_size 18
                action Function(camera_hide_hint)

    timer 8.0 action Function(camera_hide_hint)


## ---- Photo Album ----

screen photo_album():
    tag camera_overlay
    modal True
    zorder 100

    add Solid("#000")

    $ _cs = camera_state
    $ _cc = camera_config

    default photo_index = 0
    default current_page = ceil(photo_index / 6.0)
    default total_photos = len(_cs.photo_data) if _cs.photo_data else 0
    default total_pages = ceil(len(_cs.photo_data) / 6.0) if _cs.photo_data else 0

    default photo_location_list = [(440, 350), (950, 350), (1480, 350), (440, 780), (950, 780), (1480, 780)]

    # Render photo thumbnails
    for i in range(6):
        if _cs.photo_data and photo_index + i < len(_cs.photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]
            $ x -= 60
            $ p = _cs.photo_data[idx]
            $ aperture_number = _cc.aperture_group[p["aperture_index"]].replace("F", "")
            $ img_path = camera_get_location_image(p["location"], aperture_number)
            $ alpha_value = _cc.iso_to_alpha.get(_cc.iso_group[p["iso_index"]], 1.0)
            $ zoom_value = p["zoom_level"] / 2.3

            viewport:
                xpos x
                ypos y
                anchor (0.5, 0.5)
                xmaximum 400
                ymaximum 300
                draggable False
                mousewheel False
                add img_path xpos 0 ypos 0 zoom zoom_value alpha alpha_value

    # Clickable photo buttons
    for i in range(6):
        if _cs.photo_data and photo_index + i < len(_cs.photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]

            button:
                xpos x
                ypos y
                anchor (0.5, 0.5)
                xsize 400
                ysize 300
                background None
                action Function(camera_open_viewer, idx)

    imagemap:
        ground "camera/photographs-idle.png"
        hover "camera/photographs-hover.png"

        if photo_index < total_photos:
            hotspot (230, 120, 460, 460) action Function(camera_open_viewer, photo_index + 0)
        if photo_index + 1 < total_photos:
            hotspot (720, 120, 460, 460) action Function(camera_open_viewer, photo_index + 1)
        if photo_index + 2 < total_photos:
            hotspot (1210, 120, 460, 460) action Function(camera_open_viewer, photo_index + 2)
        if photo_index + 3 < total_photos:
            hotspot (230, 570, 460, 460) action Function(camera_open_viewer, photo_index + 3)
        if photo_index + 4 < total_photos:
            hotspot (720, 570, 460, 460) action Function(camera_open_viewer, photo_index + 4)
        if photo_index + 5 < total_photos:
            hotspot (1210, 570, 460, 460) action Function(camera_open_viewer, photo_index + 5)

    # Location name labels
    for i in range(6):
        if _cs.photo_data and photo_index + i < len(_cs.photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]
            $ p = _cs.photo_data[idx]
            $ loc_name = _cc.locations.get(p["location"], {}).get("name", p["location"])

            text "[loc_name]" xpos x ypos y+200 anchor (0.5, 0.5) size 40 color "#0f0f0f" font _cc.font

    text "[current_page + 1] / [total_pages]" xpos 0.5 ypos 0.95 anchor (0.5, 0.5) size 40 color "#0f0f0f" font _cc.font

    # Back button — just hide this screen
    imagebutton:
        xpos 0.1
        ypos 0.2
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at Transform(zoom=0.4)
        action Function(camera_close_album)

    # Pagination
    if photo_index > 0:
        imagebutton:
            xpos 0.12
            ypos 0.95
            at Transform(zoom=0.8)
            anchor (1.0, 1.0)
            idle "left_icon-idle.png"
            hover "left_icon-hover.png"
            action [SetScreenVariable("photo_index", max(0, photo_index - 6)),
                    SetScreenVariable("current_page", ceil((photo_index - 6) / 6.0)),
                    Function(renpy.restart_interaction)]
    if photo_index + 6 < total_photos:
        imagebutton:
            xpos 0.98
            ypos 0.95
            at Transform(zoom=0.8)
            anchor (1.0, 1.0)
            idle "right_icon-idle.png"
            hover "right_icon-hover.png"
            action [SetScreenVariable("photo_index", photo_index + 6),
                    SetScreenVariable("current_page", ceil((photo_index + 6) / 6.0)),
                    Function(renpy.restart_interaction)]

    key "K_ESCAPE" action Function(camera_close_album)


## ---- Single Photo Viewer ----

screen photo_viewer(index=0):
    tag camera_overlay
    modal True
    zorder 100

    add Solid("#000")

    $ _cs = camera_state
    $ _cc = camera_config
    $ info = _cs.photo_data[index]
    $ aperture_value = _cc.aperture_group[info["aperture_index"]]
    $ zoom_value = "{:.1f}x".format(info["zoom_level"] * 0.8)
    $ lens_value = info["lens"]
    $ iso_value = _cc.iso_group[info["iso_index"]]

    $ aperture_number = _cc.aperture_group[info["aperture_index"]].replace("F", "")
    $ img_path = camera_get_location_image(info["location"], aperture_number)

    $ x = round(500 + 900 * info["theme_x"])
    $ y = round(100 + 670 * info["theme_y"])

    add img_path xpos x ypos y zoom info["zoom_level"] anchor (0.5, 0.5) alpha _cc.iso_to_alpha.get(iso_value, 1.0)

    add "camera/single-photo.png"

    $ loc_name = _cc.locations.get(info["location"], {}).get("name", info["location"])
    text "Taken at [loc_name]" xpos 0.5 ypos 0.16 anchor (0.5, 0.5) size 45 color "#0f0f0f" font _cc.font
    text "Aperture: [aperture_value]" xpos 0.5 ypos 0.9 anchor (0.5, 0.5) size 40 color "#0f0f0f" font _cc.font
    text "Lens: [lens_value]" xpos 0.3 ypos 0.90 anchor (0.5, 0.5) size 40 color "#0f0f0f" font _cc.font
    text "ISO: [iso_value]" xpos 0.73 ypos 0.90 anchor (0.5, 0.5) size 40 color "#0f0f0f" font _cc.font

    # Back to album
    imagebutton:
        xpos 0.1
        ypos 0.2
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at Transform(zoom=0.4)
        action Function(camera_close_viewer)

    key "K_ESCAPE" action Function(camera_close_viewer)


## ---- Transforms ----

transform photo_slide_out:
    xpos 0.5 ypos 1.0 zoom 0.5
    linear 1.0 xpos 0 ypos -0.15 zoom 0.2
