init python:
    def check_kastle_meyer(current_order):
        for valid_order in valid_kastle_meyer_orders:
            if current_order == valid_order:
                return "complete"

            if current_order == valid_order[:len(current_order)]:
                return "progress"

        return "fail"

label big_splatter:
    if analyzed["big splatter"] == False:
        scene storyboard
        if flag1 == False:
            "New photo taken for evidence."
            "This blood still looks wet."
            $ toolbox.add_to_inventory(tools["Swab Pack"])
            $ toolbox.add_to_inventory(tools["Tube"])
            $ toolbox.add_to_inventory(tools["Ethanol"])
            $ toolbox.add_to_inventory(tools["Reagent"])
            $ toolbox.add_to_inventory(tools["Hydrogen Peroxide"])
            $ toolbox.add_to_inventory(tools["Evidence Bag"])
            $ toolbox.add_to_inventory(tools["Tamper Evident Tape"])
            $ flag1 = True
        if cased["big splatter"] == False:
            $ analyzing["big splatter"] = True
        $ result = check_kastle_meyer(player_kastle_meyer_order)
        if identified["big splatter"] == False:
            if result == "fail":
                jump kastle_meyer_fail
            elif result == "complete":
                jump kastle_meyer_success
        call screen inventory
        jump game
    else:
        "You've already analyzed this area."
        jump game

label left_wall:
    if analyzed["handprint"] == False:
        if flag4 == False:
                    $ toolbox.add_to_inventory(tools["UV Light"])
                    $ toolbox.add_to_inventory(tools["Magnetic Powder"])
                    $ toolbox.add_to_inventory(tools["Gel Lifter"])
                    $ toolbox.add_to_inventory(tools["Backing Card"])
                    $ toolbox.add_to_inventory(tools["Evidence Bag"])
                    $ toolbox.add_to_inventory(tools["Tamper Evident Tape"])
                    $ flag4 = True
        $ analyzing["handprint"] = True
        if identified["handprint"]:
            scene left wall mag
        else:
            scene left wall
        call screen inventory
        jump game
    else:
        "You've already analyzed this area."
        jump game

label right_wall:
    if analyzed["small splatter"] == False or analyzed["fingerprint"] == False:
        if flag3 == False:
                    "New photo taken for evidence."
                    "The blood here looks really dry."
                    $ toolbox.add_to_inventory(tools["Swab Pack"])
                    $ toolbox.add_to_inventory(tools["Hungarian Red"])
                    $ toolbox.add_to_inventory(tools["Ethanol"])
                    $ toolbox.add_to_inventory(tools["Reagent"])
                    $ toolbox.add_to_inventory(tools["Hydrogen Peroxide"])
                    $ toolbox.add_to_inventory(tools["Tape"])
                    $ toolbox.add_to_inventory(tools["Scalebar"])
                    $ toolbox.add_to_inventory(tools["Backing Card"])
                    $ toolbox.add_to_inventory(tools["Evidence Bag"])
                    $ toolbox.add_to_inventory(tools["Tamper Evident Tape"])
                    $ flag3 = True
        if flag2 == False:
                    "New photo taken for evidence."
                    $ toolbox.add_to_inventory(tools["Swab Pack"])
                    $ toolbox.add_to_inventory(tools["Hungarian Red"])
                    $ toolbox.add_to_inventory(tools["Ethanol"])
                    $ toolbox.add_to_inventory(tools["Reagent"])
                    $ toolbox.add_to_inventory(tools["Hydrogen Peroxide"])
                    $ toolbox.add_to_inventory(tools["Tape"])
                    $ toolbox.add_to_inventory(tools["Scalebar"])
                    $ toolbox.add_to_inventory(tools["Backing Card"])
                    $ toolbox.add_to_inventory(tools["Evidence Bag"])
                    $ toolbox.add_to_inventory(tools["Tamper Evident Tape"])
                    $ flag2 = True
        $ analyzing["small splatter"] = not analyzed["small splatter"]
        $ analyzing["fingerprint"] = analyzed["small splatter"] and not analyzed["fingerprint"]
        if identified["fingerprint"] and not scalebar and not tape:
            scene right wall evidence
        elif scalebar and not tape and identified["fingerprint"]:
            scene right wall bar
        elif tape and scalebar and identified["fingerprint"]:
            scene right wal lifted
        else:
            scene right wall plain
        $ result = check_kastle_meyer(player_kastle_meyer_order)
        if identified["small splatter"] == False:
            if result == "fail":
                jump kastle_meyer_fail
            elif result == "complete":
                jump kastle_meyer_success
        call screen inventory
    #   jump game
    else:
        "You've already analyzed this area."
        jump game