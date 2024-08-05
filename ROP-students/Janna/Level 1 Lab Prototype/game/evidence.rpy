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
        renpy.say(None, "{color=#30b002}The {evidence.name} has been updated.{/color}")

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
            renpy.hide_screen("casefile_physical")
            renpy.jump("fumehood_label_v2")
        elif location == "oven" and oven.state == "preheated":
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