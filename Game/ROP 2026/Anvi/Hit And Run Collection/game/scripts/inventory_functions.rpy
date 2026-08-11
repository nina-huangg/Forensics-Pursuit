init -100 python:
    def use_druggist_paper():
        renpy.jump("druggist_paper_use_label")
        renpy.restart_interaction()
        
    def use_druggist_fold():
        renpy.jump("druggist_fold_use_label")
        renpy.restart_interaction()

    def use_swab_pack():
        renpy.jump("swab_use_label")
        renpy.restart_interaction()
    
    def use_evidence_bag():
        renpy.jump("evidence_bag_use_label")
        renpy.restart_interaction()

    def use_hungarian():
        renpy.jump("hungarian_use_label")
        renpy.restart_interaction()

    def use_uv_light():
        renpy.jump("uv_use_label")
        renpy.restart_interaction()

    def use_backing_card():
        renpy.jump("backing_card_use_label")
        renpy.restart_interaction()

    def use_scalebar():
        renpy.jump("scalebar_use_label")
        renpy.restart_interaction()

    def use_tape():
        renpy.jump("tape_use_label")
        renpy.restart_interaction()

    def use_gel_lifter():
        renpy.jump("gel_lifter_use_label")
        renpy.restart_interaction()

    def use_magnetic_powder():
        renpy.jump("magnetic_powder_use_label")
        renpy.restart_interaction()

    def use_tube():
        renpy.jump("tube_use_label")
        renpy.restart_interaction()

    def use_tamper_evident_tape():
        renpy.jump("tamper_evident_tape_use_label")
        renpy.restart_interaction()

    def use_gel_lifter():
        renpy.jump("gel_lifter_use_label")
        renpy.restart_interaction()
    
    def use_gel_lifter_cover():
        renpy.jump("gel_lifter_cover_use_label")
        renpy.restart_interaction()

    def use_roller():
        renpy.jump("roller_use_label")
        renpy.restart_interaction()

    def use_envelope():
        renpy.jump("envelope_use_label")
        renpy.restart_interaction()
        
    def use_fingerprint_1():
        renpy.jump("fingerprint_1_use_label")
        renpy.restart_interaction()

    def use_fingerprint_2():
        renpy.jump("fingerprint_2_use_label")
        renpy.restart_interaction()

    def use_known_paint_sample():
        renpy.store.paint_sample = "known_paint"
        if location == "stereomicroscope":
            renpy.restart_interaction()
        if location == "ftir_station":
            renpy.jump("ftir_station_use_label")
            renpy.restart_interaction()

    def use_unknown_paint_sample_1():
        renpy.store.paint_sample = "unknown1_paint"
        if location == "stereomicroscope":
            renpy.restart_interaction()
        if location == "ftir_station":
            renpy.jump("ftir_station_use_label")
            renpy.restart_interaction()

    def use_unknown_paint_sample_2():
        renpy.store.paint_sample = "unknown2_paint"
        if location == "stereomicroscope":
            renpy.restart_interaction()
        if location == "ftir_station":
            renpy.jump("ftir_station_use_label")
            renpy.restart_interaction()

    def use_unknown_paint_sample_3():
        renpy.store.paint_sample = "unknown3_paint"
        if location == "stereomicroscope":
            renpy.restart_interaction()
        if location == "ftir_station":
            renpy.jump("ftir_station_use_label")
            renpy.restart_interaction()