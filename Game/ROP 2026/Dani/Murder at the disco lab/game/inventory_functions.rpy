init python:
    # This function will run when the player uses the item
    def use_swab_pack():
        # You can jump to labels from python using renpy.jump()
        renpy.jump("swab_use_label")
        renpy.restart_interaction()
    
    def use_hungarian():
        renpy.jump("hungarian_use_label")
        renpy.restart_interaction()
    
    def use_uv_light():
        renpy.jump("uv_use_label")
        renpy.restart_interaction()

    def use_lifter():
        renpy.jump("lifter_use_label")
        renpy.restart_interaction()

    def use_powder():
        renpy.jump("powder_use_label")
        renpy.restart_interaction()

    def use_tamper():
        renpy.jump("tamper_use_label")
        renpy.restart_interaction()
    
    def use_bag():
        renpy.jump("bag_use_label")
        renpy.restart_interaction()

    def use_backing_card():
        renpy.jump("card_use_label")
        renpy.restart_interaction()

    def use_ethanol():
        renpy.jump("e_use_label")
        renpy.restart_interaction()
    
    def use_reagent():
        renpy.jump("r_use_label")
        renpy.restart_interaction()
    
    def use_hp():
        renpy.jump("h_use_label")
        renpy.restart_interaction()

    def use_tape():
        renpy.jump("tape_use_label")
        renpy.restart_interaction()
    
    def use_scalebar():
        renpy.jump("bar_use_label")
        renpy.restart_interaction()

    def use_tube():
        renpy.jump("tube_use_label")
        renpy.restart_interaction()

    def use_lysis():
        renpy.jump("lysis_use_label")
        renpy.restart_interaction()

    def use_phenol():
        renpy.jump("phenol_use_label")
        renpy.restart_interaction()

    def use_protein():
        renpy.jump("protein_use_label")
        renpy.restart_interaction()

    def use_scissors():
        renpy.jump("scissors_use_label")
        renpy.restart_interaction()

    def use_pipette():
        renpy.jump("pipette_use_label")
        renpy.restart_interaction()

    def use_te():
        renpy.jump("te_use_label")
        renpy.restart_interaction()