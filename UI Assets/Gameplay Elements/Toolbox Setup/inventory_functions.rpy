init -5 python:
    def use_backing_card():
        renpy.hide_screen("inventory")
        renpy.jump("sample")

    def use_scalebar():
        renpy.hide_screen("inventory")
        renpy.jump("sample_2")