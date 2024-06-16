
style custom_button:
    idle_background Frame("button glossy idle", 12, 12)
    hover_background Frame("button glossy hover", 12, 12)
    insensitive_background Frame("button glossy idle", 12, 12)
    xpadding 5
    ypadding 10
    xmargin 0
    ymargin 5
    xalign 0.5
    size_group "custom_button"
    xfill False

style custom_button_text:
    idle_color "#c0c0c0"
    hover_color "#ffffff"
    insensitive_color "#202020"
    xalign 0.5

style back_button:
    idle_background Frame("button glossy idle", 8, 8)
    hover_background Frame("button glossy hover", 8, 8)
    insensitive_background Frame("button glossy idle", 8, 8)
    xpadding 12
    ypadding 12
    xmargin 2
    ymargin 0
    xalign 0.5
    size_group "back_button"

style back_button_text:
    idle_color "#ffffff"
    hover_color "#ffffff"
    insensitive_color "#202020"
    xalign 0.5