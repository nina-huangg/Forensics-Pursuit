screen study_room_hover():
    frame:
        background "#FFFFFF"
        xfill True
        yfill True

    imagemap:
        if evidence_collected["coffee_in_bag"] and evidence_collected["drug_pill_in_bag"] and evidence_collected["water_bottle_in_bag"] and evidence_collected["hair_in_bag"] and evidence_collected["fingerprint"] and evidence_collected["coffee_on_floor"] and evidence_collected["bagged_pill"]:
            xalign 0.5
            ground "location_selection_finish_idle.png"
            hover "location_selection_finish_hover.png"
            hotspot (50, 160, 650, 450) action Jump("desk_top_label")
            hotspot (50, 620, 550, 400) action Jump("floor_stain_label")
            hotspot (600, 620, 650, 400) action Jump("backpack_label")
            hotspot (700, 160, 550, 450) action Jump("finish_label")
        else:
            xalign 0.5
            ground "location_selection.png"
            hover "location_selection_hover.png"
            hotspot (50, 160, 650, 450) action Jump("desk_top_label")
            hotspot (50, 620, 550, 400) action Jump("floor_stain_label")
            hotspot (600, 620, 650, 400) action Jump("backpack_label")


label prompt_place_scale:
    "Please take your fingerprints and set up your tape measure before taking a photo."
    $ renpy.pause(1.0)
    jump note_fingerprint_label

screen camera_preview_ui():

    if current_location == "note_fingerprint" and not scalebar_state:
        # 等待 0 秒，立刻运行 Jump
        timer 0.1 repeat False action [
            Hide("camera_preview_ui"),
            Show("study_room3_inventory"),
            Function(safe_camera_data, theme_x, theme_y, theme_zoom, aperture, iso_index, focal_len),
            Call("prompt_place_scale")
        ]
    
    frame:
        background "#000000ff"
        xysize (config.screen_width, config.screen_height)

    # 中上方预览图
    if aperture_group[aperture] == "F5.6":
        add "camera/[current_location]-5.6.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F8":
        add "camera/[current_location]-8.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F11":
        add "camera/[current_location]-11.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F16":
        add "camera/[current_location]-16.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)

    if infomation:
        # 半透明背景板
        add Solid("#00000080") xpos 608 ypos 376 xysize (400, 240)

        vbox:
            xpos 608 ypos 376
            xsize 500
            ysize 240
            spacing 6

            text "ISO: [iso_group[iso_index]]" size 40 color "#ffffff" font "ConcertOne-Regular.ttf"
            text "Aperture: [aperture_group[aperture]]" size 40 color "#ffffff" font "ConcertOne-Regular.ttf"
            text "Focal Length: [focal_len]" size 40 color "#ffffff" font "ConcertOne-Regular.ttf"

    # imagemap 实现底部按钮 hover 切换效果
    imagemap:
        ground "camera/camera-idle.png"
        hover  "camera/camera-hover.png"
        xpos 0.5 ypos 1.0 anchor (0.5, 1.0)

        # left button
        hotspot (1471, 547, 60, 58) action SetVariable("theme_x", theme_x + 0.02)

        # right button
        hotspot (1599, 556, 75, 48) action SetVariable("theme_x", theme_x - 0.02)

        # up button
        hotspot (1531, 482, 69, 75) action SetVariable("theme_y", theme_y + 0.02)

        # down button
        hotspot (1547, 616, 47, 55) action SetVariable("theme_y", theme_y - 0.02)
        
        # zoom in button
        # 方式 A：位置参数
        hotspot (1433, 350, 110, 110) action If(
            (focal_len == "50mm" and theme_zoom < 2.0) or
            (focal_len == "105mm" and theme_zoom < 4.0),
            SetVariable("theme_zoom", theme_zoom + 0.02),             # true 分支
            Notify("Cannot zoom in further—please switch lenses first.")  # false 分支
        )


        # zoom out button
        hotspot (1575, 346, 117, 116) action If(
            (focal_len == "50mm" and theme_zoom > 1.0) or 
            (focal_len == "105mm" and theme_zoom > 3.0),
            SetVariable("theme_zoom", theme_zoom - 0.02),
            Notify("Cannot zoom out further—please switch lenses first.")
        )

        
        # Aperture less button
        hotspot (433, 499, 133, 130) action SetVariable("aperture", max(0, aperture - 1))

        # Aperture more button
        hotspot (426, 343, 146, 127) action SetVariable("aperture", min(3, aperture + 1))

        # text "[aperture_group[aperture]]" xpos 0.658 ypos 0.88 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        # take photo button
        hotspot (1663, 76, 187, 159) action [
            Hide("camera_preview_ui"),
            Show("study_room3_inventory"),
            Function(safe_camera_data, theme_x, theme_y, theme_zoom, aperture, iso_index, focal_len),
            SetVariable("show_animation_camera", True),
            Function(renpy.jump, "{}_label".format(current_location))
        ]

        # iso button +
        hotspot (443, 827, 131, 141) action SetVariable("iso_index", max(0, iso_index - 1))

        # iso button -
        hotspot (422, 656, 153, 139) action SetVariable("iso_index", min(4, iso_index + 1))

        # text "[iso_group[iso_index]]" xpos 0.352 ypos 0.87 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        # switch focal length button 50mm
        hotspot (1432, 710, 287, 117) action [ 
            SetVariable("focal_len", "50mm"), 
            SetVariable("theme_zoom", clamp(theme_zoom, 1.0, 2.0)) 
        ]
        # switch focal length button 105mm
        hotspot (1434, 852, 281, 111) action [ 
            SetVariable("focal_len", "105mm"), 
            SetVariable("theme_zoom", clamp(theme_zoom, 3.0, 4.0)) 
        ]

        hotspot (529, 157, 120, 112) action If(
            (infomation == True),
            [SetVariable("infomation", False)],
            [SetVariable("infomation", True)]
        )

init python:
    from math import ceil

    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))
    def safe_camera_data(theme_x, theme_y, theme_zoom, aperture, iso_index, focal_len):
        print("Saving camera data...")
        global photo_data
        photo_data.append({
            "location": current_location,
            "iso_index": iso_index,
            "aperture_index": aperture,
            "zoom_level": theme_zoom,
            "lens": focal_len,
            "theme_x": theme_x,
            "theme_y": theme_y
        })

screen photo_flying():
    default aperture_index_local = photo_data[-1]["aperture_index"]
    default aperture_number_local = aperture_group[aperture_index_local].replace("F", "")
    add "camera/[current_location]-[aperture_number_local].png" xpos theme_x ypos theme_y anchor (0.5, 0.5) alpha iso_to_alpha.get(iso_group[photo_data[-1]["iso_index"]], 1.0) at photo_slide_out
    timer 1.1 action [
        Hide("photo_flying"),
        SetVariable("show_animation_camera", False),
    ]

transform photo_slide_out:
    xpos 0.5 ypos 1.0 zoom 0.5
    linear 1.0 xpos 0 ypos -0.15 zoom 0.2
    
screen photo_album():

    add Solid("#000")

    default photo_index = 0
    default current_page = ceil(photo_index / 6.0)
    default total_photos = len(photo_data) if photo_data else 0
    default total_pages = ceil(len(photo_data) / 6.0) if photo_data else 0
    default current_location_local = "{}_label".format(current_location)

    default photo_location_list =[(440, 350), (950, 350), (1480, 350), (440, 780), (950, 780), (1480, 780)]
    
    for i in range(6):
        if photo_data and photo_index + i < len(photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]
            $ x -= 60
            $ p = photo_data[idx]
            $ aperture_number = aperture_group[p["aperture_index"]].replace("F", "")
            $ img_path = "camera/{}-{}.png".format(p["location"], aperture_number)
            $ alpha_value = iso_to_alpha.get(iso_group[p["iso_index"]], 1.0)
            $ zoom_value = p["zoom_level"] / 2.3
            $ location_name = p["location"]

            
            viewport:
                xpos x
                ypos y
                anchor (0.5, 0.5)
                xmaximum 400
                ymaximum 300
                draggable False
                mousewheel False
                add img_path xpos 0 ypos 0 zoom zoom_value alpha alpha_value
        
    for i in range(6):
        if photo_data and photo_index + i < len(photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]

            button:
                xpos x
                ypos y
                anchor (0.5, 0.5)
                xsize 400
                ysize 300
                background None
                action Function(open_photo_viewer_with_index, idx)

    imagemap:
        ground "camera/photographs-idle.png"
        # hover "desk_top_hover.png"
        hover "camera/photographs-hover.png"

        # if desk_top_marks["marker1"] and desk_top_marks["marker2"] and desk_top_marks["marker3"] and desk_top_marks["marker4"] and desk_top_marks["marker5"]:
        if photo_index < total_photos:
            hotspot (230, 120, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 0)
        if photo_index + 1 < total_photos:
            hotspot (720, 120, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 1)
        if photo_index + 2 < total_photos:
            hotspot (1210, 120, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 2)

        if photo_index + 3 < total_photos:
            hotspot (230, 570, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 3)
        if photo_index + 4 < total_photos:
            hotspot (720, 570, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 4)
        if photo_index + 5 < total_photos:
            hotspot (1210, 570, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 5)

    for i in range(6):
        if photo_data and photo_index + i < len(photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]
            $ p = photo_data[idx]
            $ location_name = p["location"]

            text "[location_name_dict[location_name]]" xpos x ypos y+200 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"

    text "[current_page + 1] / [total_pages]" xpos 0.5 ypos 0.95 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"

    imagebutton:
        xpos 0.1
        ypos 0.2
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action [
            Show("study_room3_inventory"),
            Hide("photo_album"),
            Function(renpy.jump, "{}_label".format(current_location)),
        ]

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




        # 右上角“关闭”按钮
        # textbutton "关闭" action Hide("photo_album") xpos 0.95 ypos 0.05

        # frame:
        #     background "#e61212"
        #     xpos 270
        #     ypos 120
        #     xsize 380
        #     ysize 380

init python:
    def open_photo_viewer_with_index(index):
        global photo_show_index
        global photo_data
        photo_show_index = index
        if index >= 0 and index < len(photo_data):
            renpy.jump("photo_viewer_label")

screen photo_viewer(index=photo_show_index):
    tag photo_viewer
    modal True

    add Solid("#000")

    # 背景
    
    # 获取照片信息
    $ info = photo_data[index]
    $ aperture_value = aperture_group[info["aperture_index"]]
    $ zoom_value = "{:.1f}x".format(info["zoom_level"]* 0.8) 
    $ lens_value = info["lens"]
    $ iso_value = iso_group[info["iso_index"]]

    # 生成要显示的照片路径
    $ aperture_number = aperture_group[info["aperture_index"]].replace("F", "")
    $ img_path = "camera/{}-{}.png".format(info["location"], aperture_number)

    $ x = round(500 + 900 * info["theme_x"])
    $ y = round(100 + 670 * info["theme_y"])
    
    add img_path xpos x ypos y zoom info["zoom_level"] anchor (0.5, 0.5) alpha iso_to_alpha.get(iso_value, 1.0)
    
    add "camera/single-photo.png"

    text "Taken at [location_name_dict[info['location']]]" xpos 0.5 ypos 0.16 anchor (0.5, 0.5) size 45 color "#0f0f0f" font "ConcertOne-Regular.ttf"
    text "Aperture: [aperture_value]" xpos 0.5 ypos 0.9 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"
    text "Lens: [lens_value]" xpos 0.3 ypos 0.90 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"
    text "ISO: [iso_value]" xpos 0.73 ypos 0.90 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"

    imagebutton:
        xpos 0.1
        ypos 0.2
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action [
            Hide("photo_viewer"),
            Jump("photo_album_label"),
        ]



## Desktop Interaction Screen ###############################
screen desk_top_hover():

    imagemap:
        xalign 0.5
        if water_bottle_get and pill_bottle_get:
            ground "desk_top_out_all.png"
        elif water_bottle_get:
            ground "desk_top_out_water.png"
        elif pill_bottle_get:
            ground "desk_top_out_pill.png"
        else:
            ground "desk_top_full.png"

        hover "desk_top_hover.png"

        if desk_top_marks["marker1"] and desk_top_marks["marker2"] and desk_top_marks["marker3"] and desk_top_marks["marker4"] and desk_top_marks["marker5"]:
            hotspot (180, 400, 275, 520) action Jump("coffee_cup_theme_label")
            hotspot (450, 632, 820, 320) action Jump("laptop_label")
            hotspot (1280, 820, 290, 290) action Jump("note_label")
            if not water_bottle_get:
                hotspot (1320, 130, 500, 670) action Jump("water_bottle_label")
            if not pill_bottle_get:
                hotspot (900, 400, 400, 232) action Jump("pill_label")
        else:
            text "Put all the evidence markers to begin the investigation." xpos 0.5 ypos 0.05 anchor (0.5, 0.5) size 40 color "#ffffff" font "ConcertOne-Regular.ttf"
            hotspot (180, 400, 275, 520) action Jump("desk_top_label")
            hotspot (450, 632, 820, 320) action Jump("desk_top_label")
            hotspot (1280, 820, 290, 290) action Jump("desk_top_label")
            hotspot (1320, 130, 500, 670) action Jump("desk_top_label")
            hotspot (900, 400, 400, 232) action Jump("desk_top_label")
    
    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("location_selection_label")
    
    if desk_top_marks["marker1"]:
        add "em1.png" xpos 0.07 ypos 0.7
    if desk_top_marks["marker2"]:
        add "em2.png" xpos 0.26 ypos 0.75
    if desk_top_marks["marker3"]:
        add "em3.png" xpos 0.63 ypos 0.8
    if desk_top_marks["marker4"]:
        add "em4.png" xpos 0.65 ypos 0.6
    if desk_top_marks["marker5"]:
        add "em5.png" xpos 0.48 ypos 0.45

screen chat_viewer(images):
    default index = 0

    key "K_UP" action If(index > 0, SetScreenVariable("index", index - 1))
    key "K_DOWN" action If(index < len(images) - 1, SetScreenVariable("index", index + 1))
    key "K_ESCAPE" action Return()

    frame:
        background "desk_top_full.png"
        yfill True
        add Solid("#00000080") 

    text "click up and down arrow keys to navigate through the images" xpos 0.5 ypos 0.05 anchor (0.5, 0.5) size 30 color "#ffffff" font "ConcertOne-Regular.ttf"

    add images[index] xpos 0.501 ypos 0.47 anchor (0.5, 0.5) zoom 1.24
    add "macbook.png" xpos 0.5 ypos 0.5 anchor (0.5, 0.5) zoom 6

    text "[index+1]/[len(images)]" xpos 0.95 ypos 0.95 size 30

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top_label")

screen coffee_cup_theme_viewer():
    default note_book_opened = False

    frame:
        background "coffee_cup_theme.png"
        yfill True
    

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top_label")
    if sample_vial_state == "empty":
        add "sample_bottle_open.png" xpos 0.29 ypos 0.5 anchor (0.5, 0.5) zoom 0.4
    elif sample_vial_state == "coffee":
        add "sample_bottle_coffee.png" xpos 0.29 ypos 0.5 anchor (0.5, 0.5) zoom 0.5
    elif sample_vial_state == "not_taken":
        pass
    
    if show_animation_camera:
        use photo_flying
    # frame:
    #         background "#e61212"
    #         xpos 380
    #         ypos 
    #         xsize 230
    #         ysize 300

    # imagebutton:
    #     xpos 0.83 ypos 0.4
    #     idle "pipette_idle.png"
    #     hover "pipette_hover.png"
    #     if not coffee_cup_evidence["sample_taken"]:
    #         action [SetDict(coffee_cup_evidence, "sample_taken", True)]

screen note_viewer():
    
    frame:
        background "note_theme.png"
        yfill True

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top_label")

init python:
    fingerprint_find_global = False  # 全局变量，指纹是否已找到

screen note_viewer_with_fingerprints():

    # ─── 状态变量 ───
    # default uv_on = False           # UV 灯是否开启\
    default fingerprint_find = False
    if scalebar_state:
        $ fingerprint_find = True

    default mouse = (960, 540)      # 灯圈中心（初始居中）

    # ─── 背景图层 ───
    add "note_theme.png"              # ① 常规视图：纸条

    imagemap:
        xalign 0.5
        if not fingerprint_find:
            ground "note_theme.png"

            hotspot (1100, 300, 200, 180) action [
                SetScreenVariable("fingerprint_find", True)
            ]
        else:
            if scalebar_state:
                ground "note_finger_with_bar_theme.png"  # ② 指纹视图：带刻度尺的暗幕遮罩
            else:
                ground "note_finger_theme.png"  # ① 指纹视图：暗幕遮罩

    if fingerprint_find:
        $ fingerprint_find_global = True  # 设置全局变量，指纹已找到

    # ─── 如果还没找到指纹 ───
    if not fingerprint_find:
        add "note_finger_theme.png"   # ② 整张指纹图（平常被暗幕挡住）
        add "darkness" pos mouse anchor (0.5, 0.5)  # ③ 零散遮罩跟随鼠标

        # ─── 鼠标跟随 Timer ───
        timer 0.02 repeat True action SetScreenVariable(
            "mouse", renpy.get_mouse_pos()
        )

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top_label")

screen normal_uv_light_viewer():
    default mouse = (960, 540)
    imagemap:
        xalign 0.5
        ground location_name_pic_dict[current_location]

    add location_name_pic_dict[current_location]
    add "darkness" pos mouse anchor (0.5, 0.5)

    # ─── 鼠标跟随 Timer ───
    timer 0.02 repeat True action SetScreenVariable(
        "mouse", renpy.get_mouse_pos()
    )

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump(current_location + "_label")


screen pill_viewer():
    frame:
        background "pill_theme.png"
        yfill True

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top_label")


screen water_bottle_viewer():
    frame:
        background "water_bottle_theme.png"
        yfill True
    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top_label")

    # frame:
    #     background "#e61212"
    #     xpos 800
    #     ypos 0
    #     xsize 700
    #     ysize 1080

init python:
    import datetime

screen observation_form():
    
    imagemap:
        xalign 0.3
        ground "observation/stand_idle.png"
        hover "observation/stand_hover.png"

        text "[datetime.date.today().strftime('%Y-%m-%d')]" xalign 0.43 yalign 0.34 size 39 color "#363636" font "ConcertOne-Regular.ttf"

        input id "in1" value exhibit_no length 8 xalign 0.55 yalign 0.45 font "ConcertOne-Regular.ttf" size 39 color "#363636"

        input id "in2" value picked_color length 8 xalign 0.55 yalign 0.55 font "ConcertOne-Regular.ttf" size 39 color "#363636"

    # frame:
    #     background "#e61212"
    #     xpos 400
    #     ypos 300
    #     xsize 550
    #     ysize 120

### floor_stain Interaction Screen ###############################

screen floor_stain_hover():
    imagemap:
        xalign 0.5
        if not hair_get:
            ground "desk_under_idle.png"
        else:
            ground "desk_under_nohair_idle.png"
        hover "desk_under_hover.png"
        if desk_top_marks["marker6"] and desk_top_marks["marker7"]:
            hotspot (600, 400, 550, 550) action Jump("coffee_on_floor_label")
            if not hair_get:
                hotspot (1000, 800, 290, 190) action Jump("hair_label")
        else:
            text "Put all the evidence markers to begin the investigation." xpos 0.5 ypos 0.05 anchor (0.5, 0.5) size 40 color "#ffffff" font "ConcertOne-Regular.ttf"
            hotspot (600, 400, 550, 550) action Jump("floor_stain_label")
            hotspot (1000, 800, 290, 190) action Jump("floor_stain_label")

    if desk_top_marks["marker6"]:
        add "em6.png" xpos 0.3 ypos 0.7

    if desk_top_marks["marker7"]:
        add "em7.png" xpos 0.5 ypos 0.8

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("location_selection_label")


screen coffee_on_floor_viewer():
    frame:
        background "coffee_on_floor_theme.png"
        yfill True

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("floor_stain_label")
    
    # frame:
    #     background "#e61212"
    #     xpos 700
    #     ypos 300
    #     xsize 800
    #     ysize 900

screen hair_viewer():
    frame:
        background "hair_theme.png"
        yfill True

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("floor_stain_label")
## chair_backpack_hover Screen ###############################

screen chair_backpack_hover():
    imagemap:
        xalign 0.5
        ground "desk_bag.png"
        hover "desk_bag_hover.png"

        hotspot (350, 150, 600, 900) action Jump("collect_empty_pill")

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("location_selection_label")


screen outside_study1():
    frame:
        xcenter 0.5 ycenter 0.5
        hbox:
            spacing 30
            xsize 800
            text "This is the study room where the victim was allegedly attacked! Before we go inside and investigate, let's put on some vinyl gloves as a precaution! \n\n>> press space to continue"
    key "K_SPACE" action Jump("gloves1")

screen outside_study2():
    imagebutton:
        xalign 0.625
        yalign 0.616
        idle "doorknob_idle"
        hover "doorknob_hover"
        action Jump("toolbox_init")

screen gloves():
    imagebutton:
        xalign 0.5
        yalign 0.5
        idle "gloves_box_idle"
        hover "gloves_box_hover"
        action Jump("gloves2")