init -5 python:
    def use_backing_card():
        renpy.jump("useBackingcard")
    def use_evidence_bag():
        renpy.jump("askWhatToBag")
    def can_magnetic_powder():
        renpy.jump("canMagneticPowder")
    def use_uv_light():
        renpy.jump("useUVLight")
    def use_scale_bar():
        renpy.jump("useScaleBar")
    def use_tape():
        renpy.jump("useTape")
    def use_tamper_tape():
        renpy.jump("useTamperTape")

    def bag_item1():
        renpy.jump("bagItem1")
    def bag_item2():
        renpy.jump("bagItem2")
    def bag_item4():
        renpy.jump("bagItem4")
    def bag_item5():
        renpy.jump("bagItem5")
    def bag_item6():
        renpy.jump("bagItem6")
