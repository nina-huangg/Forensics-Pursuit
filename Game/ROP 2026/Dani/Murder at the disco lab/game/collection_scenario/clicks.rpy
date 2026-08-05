init python:
    def check_kastle_meyer(current_order):
        for valid_order in valid_kastle_meyer_orders:
            if current_order == valid_order:
                return "complete"

            if current_order == valid_order[:len(current_order)]:
                return "progress"

        return "fail"

label laboratory:
    scene lab
    show screen lab
    if snipped == False:
        $ toolbox.add_to_inventory(tools["Scissors"])
    call screen inventory