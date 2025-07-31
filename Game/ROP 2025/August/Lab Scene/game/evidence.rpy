init python:
    class Evidence_v2:
        """A custom data type that represents data for an evidence."""
        name: str
        processed: bool
        available: bool
        image: str
        description: str
        xpos: float
        ypos: float

        def __init__(self, name: str, image: str = "", description: str = "", xpos: float = 0, ypos: float = 0) -> None:
            """Initialize a new Evidence_v2 object."""
            self.name = name
            self.processed = False
            self.available = True
            self.image = image
            self.description = description
            self.xpos = xpos
            self.ypos = ypos
        
        def update_name(self, new_name: str) -> None:
            self.name = new_name
        
        def process_evidence(self) -> None:
            self.processed = True
        
        def disable_evidence(self) -> None:
            self.available = False
        
        def enable_evidence(self) -> None:
            self.available = True
        
        def update_image(self, new_image: str) -> None:
            self.image = new_image
        
        def update_description(self, new_desc: str) -> None:
            self.description = new_desc
        
        def update_xpos(self, new_xpos: float) -> None:
            self.xpos = new_xpos
        
        def update_ypos(self, new_ypos: float) -> None:
            self.ypos = new_ypos
        
    def update_evidence(evidence: Evidence_v2, image: str = "", desc: str = "") -> None:
        """Updates a piece of evidence in the inventory and notifies the player.
        If provided, the image and the description are updated as well.
        """
        if image != "": 
            evidence.update_image(image)
        if desc != "": 
            evidence.update_description(desc) 
        renpy.say(None, "The {evidence.name} has been updated.")

    def create_evidence(name: str, image: str = "", description: str = "", xpos: float = 0, ypos: float = 0) -> Evidence_v2:
        """Creates a new piece of evidence with the provided attributes.
        """
        return Evidence_v2(
            name = name,
            image = image,
            description = description,
            xpos = xpos,
            ypos = ypos
        )

    def label_function() -> None:
        global location
        global imported_print
        global oven
        if location == "fumehood":
            hide_all_inventory()
            renpy.jump("fumehood_label_v2")
        elif location == "oven" and oven.state == "preheated" and label.dipped:
            hide_all_inventory()
            renpy.jump("label_placed_in_oven")
        elif location == "afis" and label.processed:
            imported_print = "print_4"
            renpy.jump("import_print")

    def label_function_alt() -> None:
        global location
        global imported_print
        global oven
        if location == "fumehood":
            renpy.hide_screen("casefile_physical")
            renpy.jump("fumehood_label_v2")
        elif location == "oven" and oven.state == "preheated" and label.dipped:
            renpy.hide_screen("casefile_physical")
            renpy.jump("label_placed_in_oven")
        elif location == "afis" and label.processed:
            imported_print = "print_4"
            renpy.jump("import_print")

    gin = Evidence_v2(
        name = "gin bottle",
        image = "gin %s",
        description = "The gin bottle collected from the table at the crime scene. The label may contain some prints."
    )

    label = Evidence_v2(
        name = "label",
        image = "label_%s",
        description = "The label collected from the gin bottle. May contain prints."
    )

    # Additional attribute for label
    label.dipped = False

    pills = Evidence_v2(
        name = "pills",
        image = "pills %s",
        description = "Suspicious pills found at the crime scene. Need to be ground for analysis."
    )

    grinded_pills = Evidence_v2(
        name = "grinded pills",
        image = "grinded_pills %s",
        description = "Ground pills ready for chemical analysis."
    )

    # Initially disable grinded_pills since they need to be created
    grinded_pills.disable_evidence()

    bottled_powder = Evidence_v2(
        name = "bottled powder",
        image = "bottled_powder %s",
        description = "Ground pills stored in a bottle, ready for chemical testing."
    )

    # Initially disable bottled_powder since it needs to be created
    bottled_powder.disable_evidence()

    # Teflon digestion vessel with pills and reagents
    teflon_pills = Evidence_v2(
        name = "teflon digestion vessel",
        image = "teflon_pills %s",
        description = "Teflon digestion vessel containing ground pills and all required reagents (nitric acid, hydrofluoric acid, hydrogen peroxide). Ready for microwave digestion."
    )

    # Initially disable teflon_pills since it needs to be created
    teflon_pills.disable_evidence()

    # Digested sample ready for ICP analysis
    digested_sample = Evidence_v2(
        name = "digested sample",
        image = "digested_sample %s",
        description = "Clear, completely digested sample ready for ICP analysis. Processed through three-step microwave digestion: 250W, 400W, 600W for 10 minutes each."
    )

    # Initially disable digested_sample since it needs to be created
    digested_sample.disable_evidence()

    # Diluted sample ready for ICP analysis
    diluted_sample = Evidence_v2(
        name = "diluted sample",
        image = "diluted_sample %s",
        description = "Digested sample diluted to 50 mL with deionized water in polypropylene container. Ready for ICP analysis."
    )

    # Initially disable diluted_sample since it needs to be created
    diluted_sample.disable_evidence()

    # Deionized water for dilution
    deionized_water = Evidence_v2(
        name = "deionized water",
        image = "deionized_water %s",
        description = "High-purity deionized water for sample dilution to 50 mL total volume."
    )

    # ICP analysis results
    icp_results = Evidence_v2(
        name = "ICP analysis results",
        image = "icp_results %s",
        description = "Elemental analysis results from ICP showing concentration of selected elements in ppm."
    )

    # Initially disable icp_results since it needs to be created
    icp_results.disable_evidence()

    # Digestion reagents for chemical analysis
    nitric_acid = Evidence_v2(
        name = "nitric acid",
        image = "nitric_acid %s",
        description = "Concentrated nitric acid (4 mL) for sample digestion."
    )

    hydrofluoric_acid = Evidence_v2(
        name = "hydrofluoric acid", 
        image = "hydrofluoric_acid %s",
        description = "Hydrofluoric acid (0.5 mL) for silicate sample digestion."
    )

    hydrogen_peroxide = Evidence_v2(
        name = "hydrogen peroxide",
        image = "hydrogen_peroxide %s", 
        description = "Hydrogen peroxide (2 mL) for oxidative digestion."
    )

    fingerprint = Evidence_v2(
        name = "fingerprint",
        image = "fingerprint %s",
        description = "The fingerprint gathered from the light switch."
    )

screen ui():
    zorder 1
    hbox:
        # xpos 0.02 ypos 0.3
        xpos 0.02 ypos 0.12
        imagebutton:
            auto "case_file_%s" at Transform(zoom=2.5)
            hovered Notify("evidence")
            action ToggleScreen("casefile_physical")

screen casefile_physical():
    zorder 1
    modal True
    add "casefile_inventory"
    text "Evidence Collected" xpos 0.42 ypos 0.15
    hbox:
        xpos 0.17 ypos 0.1
        imagebutton:
            auto "back_button_%s" at Transform(zoom=0.2)
            action ToggleScreen("casefile_physical")

    hbox:
        # xpos 0.2 ypos 0.51
        xpos 0.2 ypos 0.24
        imagebutton:
            if gin.processed:
                auto "gin_no_label_%s" at Transform(zoom=0.7)
            else:
                auto "gin %s" at Transform(zoom=0.7)
            action If(location == "fumehood" and not gin.processed, [ToggleScreen("casefile_physical"), Jump("fumehood_bottle")])
    
    showif gin.processed:
        hbox:
            # xpos 0.2 ypos 0.24
            xpos 0.5 ypos 0.24
            imagebutton:
                if label.processed:
                    auto "baked label %s" at Transform(zoom=0.7)
                else:
                    auto "label_%s" at Transform(zoom=0.7)
                action Function(label_function)
    
    # showif label.processed:
    # hbox:
    #     xpos 0.65 ypos 0.51
    #     imagebutton:
    #         auto "baked label %s" at Transform(zoom=0.7)
    #         action NullAction()

    # hbox:
    #     xpos 0.35 ypos 0.24
    #     imagebutton:
    #         auto "handprint %s" at Transform(zoom=0.7)
    #         action NullAction()
    
    hbox:
        # xpos 0.5 ypos 0.24
        xpos 0.35 ypos 0.24
        imagebutton:
            auto fingerprint.image at Transform(zoom=0.7)
            action If(location == "afis" and pressed == "import", [SetVariable("imported_print", "print_1"), Jump("import_print")])

    hbox:
        xpos 0.2 ypos 0.51
        imagebutton:
            if not pills.processed:
                auto "pills %s" at Transform(zoom=0.7)
                action If(location == "grinder", [ToggleScreen("casefile_physical"), Jump("grinder_pills")])
            elif pills.processed and grinded_pills.available and not bottled_powder.available:
                auto "grinded_pills %s" at Transform(zoom=0.7) 
                action If(location == "grinder", [ToggleScreen("casefile_physical"), Jump("bottle_filling")])
            elif bottled_powder.available:
                auto "bottled_powder %s" at Transform(zoom=0.7)
                action NullAction()

    # hbox:
    #     xpos 0.5 ypos 0.51
    #     imagebutton:
    #         auto "sample splatter %s" at Transform(zoom=0.7)
    #         action NullAction()

    # hbox:
    #     xpos 0.35 ypos 0.51
    #     imagebutton:
    #         auto "sample footprint %s" at Transform(zoom=0.7)
    #         action NullAction()