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
    def use_glove():
        renpy.jump("useGlove")

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

    #fingerprint analysis in the lab
    def bag_finger_1():
        renpy.jump("bagFinger1")
    def bag_finger_2():
        renpy.jump("bagFinger2")

    # LAB SPE
    def use_Methanol():
        renpy.jump("useMethanol")
    def use_step3():
        renpy.jump("useStep3")
    def use_postbs():
        renpy.jump("usePost")
    def use_prebs():
        renpy.jump("usePre")
    def use_01formic():
        renpy.jump("use01Formic")
    def use_5amm():
        renpy.jump("use5Amm")
    def use_ppostbs():
        renpy.jump("usePpostBS")
    def use_pprebs():
        renpy.jump("usePpreBS")
    def use_water():
        renpy.jump("useWater")