init -10 python:
    """
    This file contains all code related to the inventory system. 

    Loading inventory items ---------------------------------------------------------------
    
    You must create two json files, one for your toolbox items and one for your
    evidence items. You can load your items using the load_items(filename) function.
    This function will return a dictionary of item names to Item objects for filename.
    script.rpy currently loads in items from toolbox.json and evidence.json. However, it
    is possible that in later scenarios (lab, courtroom) you may want to separate item
    jsons by level.

    Each object in the jsons takes values for the attrbutes in the Item class (name, description,
    image_name, usable, action). The only mandatory attributes are name and image_name (this
    will allow the item to show up in the inventory at minimum). To make the item usable,
    you should include the usable (set this to True) and action attributes.
    The action attribute should link to a function that you want to run when the item is clicked.
    You can place these functions in the inventory_functions.rpy file.

    Adding and removing inventory items ---------------------------------------------------
    
    To add items to the toolbox, use "toolbox.add_to_inventory(<tool-item>)".
    <tool-item> must be of type Item. You can use the dictionary generated from load_items
    to do this. Similarly, to add items to the evidence, use "evidence.add_to_inventory(<evidence-item>)".

    To remove items from the tooblox, use "toolbox.delete_from_inventory(<Item>)". You
    can use the same function to remove from the evidence.

    Displaying the inventory --------------------------------------------------------------

    You may use either "show screen inventory" or "call screen inventory". In almost all
    cases, you will want to use the former to allow screens below to be clickable. 
    However, if you want to force the player to interact with the inventory before moving 
    on, use the latter.

    To hide the inventory, use "hide screen inventory"
    """

    from typing import Optional, List, Dict, Callable
    import json
    
    class Item:
        """
        This class is responsible for instantiating an item (either a toolbox or evidence
        item). 

        Instance Attributes:
            - name: The name of the item. Rendered when the player chooses to view more
            details about the item. This is required.
            - description: A brief description of the item. Rendered when the player 
            chooses to view more details about the item. By default, set to an empty string.
            - imagename: The name of the image for this item. This should be approximately
            200x200px and either a png, jpg, or jpeg. Do not include the png, jpg, jpeg
            suffix. This is required.
            - usable: If the item is usable, then upon clicking the Use (left hand) icon,
            the action below will run. You will not want your tools to be accessible in
            all cases. By default, set to False.
            - action: This will run when the player chooses to use the item. By default,
            set to None.
        """
        name: str
        description: str
        image_name: str
        usable: bool
        action: Optional[Callable]


        def __init__(self, name: str, image_name: str, description: str = "", usable: bool = False, action: Callable = None) -> None:
            self.name = name
            self.description = description
            self.image_name = image_name
            self.usable = usable
            self.action = action


        def set_name(self, name: str) -> None:
            self.name = name


        def set_description(self, description: str) -> None:
            self.description = description


        def set_image_name(self, image_name: str) -> None:
            self.image_name = image_name


        def set_usable(self, usable: bool) -> None:
            self.usable = usable


        def set_action(self, action: Callable) -> None:
            self.action = action


    class Evidence(Item):
        """
        An extension of the Item class for an evidence item. This is not required, nor
        is it explicitly used in the default inventory code. If by any chance,
        you need to explicitly keep track of an evidence item's collection status, you 
        may use this class. However, you could also just add and remove from your
        evidence inventory as necessary to do that as well.
        """
        collected: bool


        def __init__(self, name: str, description: str, image_name: str, usable: bool = False, action: Callable = None, collected: bool = False) -> None:
            super().__init__(name, description, image_name, usable, action)
            self.collected = collected


        def set_collected(self, collected: bool) -> None:
            self.collected = collected


    class Inventory:
        """
        This class is responsible for instantiating the toolbox and evidence inventories
        respectively. 

        Instance Attributes:
            - _inventory: This houses all accessible inventory items. All inventory items
            are not necessarily visible. The player can only see at most 5 inventory items
            at a time.
            - visible_inventory: This is a paginated version of _inventory. This is the
            portion of the inventory that is displayed to the player.
            - page: The current page of the inventory.
            - start_index: The index of the first item of visible_inventory with respect
            to _inventory.
        """
        _inventory: List[Item]
        visible_inventory: List[Optional[Item]]
        page: int
        start_index: int


        def __init__(self) -> None:
            self._inventory = []
            self.visible_inventory = [None, None, None, None, None]
            self.page = 1
            self.start_index = 0
        

        def set_inventory(self, inventory: List[Item]) -> None:
            self._inventory = inventory
            self.page = 1
            self.start_index = 0
            self.refresh_visible_inventory()


        def reset_inventory(self) -> None:
            self._inventory = []
            self.page = 1
            self.start_index = 0
            self.refresh_visible_inventory()
            

        def add_to_inventory(self, item: Item) -> None:
            self._inventory.append(item)
            self.refresh_visible_inventory()
            if self == store.evidence:
                if not getattr(store, "is_packing_evidence", False):
                    renpy.show_screen(
                        "evidence_collected_notice",
                        item_name=item.name
                    )
                    renpy.restart_interaction()
                store.check_lab_transition()


        def get_item_by_name(self, name: str) -> Optional[Item]:
            """Return the first inventory item with the given name, if one exists."""
            for item in self._inventory:
                if item is not None and item.name == name:
                    return item

            return None


        def delete_from_inventory(self, item: Item) -> None:
            if item in self._inventory:
                self._inventory.remove(item)
                self.refresh_visible_inventory()


        def refresh_visible_inventory(self) -> None:
            if len(self._inventory) == 0:
                self.start_index = 0
            elif self.start_index >= len(self._inventory):
                self.start_index = ((len(self._inventory) - 1) // 5) * 5

            self.page = (self.start_index // 5) + 1
            self.set_visible_inventory(self._inventory[self.start_index : self.start_index + 5])


        def set_visible_inventory(self, visible_inventory: List[Item]) -> None:
            self.visible_inventory = visible_inventory[:5]

            if (len(self.visible_inventory) < 5):
                for i in range(5 - len(self.visible_inventory)):
                    self.visible_inventory.append(None)
        

        def previous(self) -> None:
            if self.page > 1:
                self.start_index -= 5
                self.refresh_visible_inventory()


        def next(self) -> None:
            if self.start_index + 5 < len(self._inventory):
                self.start_index += 5
                self.refresh_visible_inventory()


    def inventory_hover_enter(item_name, slot_index):
        """Remember which slot is hovered so the name badge can be drawn at the
        panel level, where it is not constrained to the 130px tile width."""
        store.hovered_item_name = item_name
        store.hovered_item_slot = slot_index

    def inventory_hover_exit(item_name):
        # Ren'Py does not guarantee unhovered fires before the next hovered, so
        # only clear if this slot is still the one being reported.
        if store.hovered_item_name == item_name:
            store.hovered_item_name = ""


    def view_item(name, image_name, description) -> None:
        """
        This function is used in the click action of screen inventory_slot's
        view-inventory-item button.
        """
        # Always dismiss first so a stuck/hidden-behind popup can reopen cleanly.
        if renpy.get_screen("inventory_info"):
            renpy.hide_screen("inventory_info")
            renpy.restart_interaction()
        renpy.show_screen(
            "inventory_info",
            name=name,
            image_name=image_name,
            description=description or "No description provided.",
        )
        renpy.restart_interaction()
    

    def use_item(usable, action) -> None:
        """
        This function is used in the click action of screen inventory_slot's
        use-inventory-item button.
        """
        if action != None and usable:
            action()


    def resolve_inventory_action(action_name):
        """
        This function is used in the load_items function below to assign the
        specified Callable in the json file to an Item if it exists.
        """
        if action_name == None:
            return None

        action = getattr(renpy.store, action_name, None)
        if action is None:
            action = globals().get(action_name)

        if callable(action):
            return action

        return None

    
    def load_items(filename: str) -> Dict[str, Item]:
        """
        This function is used to load items from a json file. It returns a
        dictionary of item names to their respective Item objects.
        """
        items = {}

        with renpy.file(filename) as item_file:
            item_data = json.loads(item_file.read().decode("utf-8"))
        
        for item in item_data:
            new_item = Item(
                item["name"],
                item["image_name"],
                item.get("description", ""),
                item.get("usable", False),
                resolve_inventory_action(item.get("action"))
            )

            items[item["name"]] = new_item
        
        return items
    

    toolbox = Inventory()
    evidence = Inventory()


screen inventory():
    modal True
    zorder 200
    on "show" action [SetVariable("inventory_open", True), Hide("open_inv")]
    on "replace" action [SetVariable("inventory_open", True), Hide("open_inv")]
    on "hide" action [SetVariable("inventory_open", False), Show("open_inv")]
    on "replaced" action [SetVariable("inventory_open", False), Show("open_inv")]

    $ inventory = evidences if courtroom_ui_active else selected_inventory

    # Click outside the inventory panel → warn player to close it first.
    button:
        background "#00000055"
        xfill True
        yfill True
        action Show("lab_notify", message="Close the inventory before interacting with the scene.", correct=False)

    # Mouse wheel pagination for both the toolbox and evidence tabs.
    key "mousedown_4" action If(
        inventory.page > 1,
        Function(inventory.previous),
        NullAction()
    )
    key "mousedown_5" action If(
        inventory.start_index + 5 < len(inventory._inventory),
        Function(inventory.next),
        NullAction()
    )

    frame:
        background None

        # Catch empty-panel clicks so they do not trigger the outside warning.
        button:
            background None
            xpos 0
            ypos 0
            xysize (340, 1080)
            action NullAction()

        # The courtroom has a single case-file list, so it has nothing to tab between.
        if not courtroom_ui_active:
            hbox:
                xoffset 10
                yoffset 17

                imagebutton:
                    auto "tool-inventory-icon-%s" at Transform(zoom=0.85)
                    insensitive "tool-inventory-icon-hover"
                    sensitive (inventory != toolbox)
                    action SetVariable("selected_inventory", toolbox)

                imagebutton:
                    auto "inventory-icon-%s" at Transform(zoom=0.85)
                    insensitive "inventory-icon-hover"
                    sensitive (inventory != evidence)
                    action SetVariable("selected_inventory", evidence)


        add Transform("inventory-bg", xzoom=0.83, yzoom=0.95, yoffset=40)

        if getattr(store, "held_evidence", None) is not None:
            frame:
                background "#e67e22dd"
                padding (15, 10)
                xpos 230
                ypos 100
                hbox:
                    spacing 15
                    add Transform(held_evidence.image_name, xysize=(50, 50), yalign=0.5)
                    vbox:
                        spacing 5
                        text "Holding: [held_evidence.name]" size 16 color "#ffffff" bold True
                        if not asked_lab_transition:
                            text "Open Toolbox & click Evidence Bag to pack it." size 14 color "#eeeeee"

        imagebutton:
            auto "close-inv-%s" at Transform(rotate=1, xoffset=49, yoffset=350)
            action [SetVariable("dialogue_boxes_visible", True), Hide("inventory"), Show("open_inv")]

        # Photo album access from Evidence tab (Item/Inventory compatible)
        if not courtroom_ui_active and inventory == evidence and camera_has_photos():
            textbutton "Photo Album":
                xpos 230
                ypos 55
                text_size 18
                background "#1f4b63dd"
                hover_background "#2d6f8f"
                padding (12, 6)
                action Function(camera_open_album)
                tooltip "Browse photographs you have taken"


        vbox:
            xoffset 32

            imagebutton:
                idle ("inventory-arrow-up-enabled-idle" if inventory.page > 1 else "inventory-arrow-up-disabled")
                hover ("inventory-arrow-up-enabled-hover" if inventory.page > 1 else "inventory-arrow-up-disabled")
                at Transform(yoffset=60)
                action If(inventory.page > 1, Function(inventory.previous), NullAction())

            imagebutton:
                idle ("inventory-arrow-down-enabled-idle" if inventory.start_index + 5 < len(inventory._inventory) else "inventory-arrow-down-disabled")
                hover ("inventory-arrow-down-enabled-hover" if inventory.start_index + 5 < len(inventory._inventory) else "inventory-arrow-down-disabled")
                at Transform(yoffset=949)
                action If(inventory.start_index + 5 < len(inventory._inventory), Function(inventory.next), NullAction())

        vbox:
            spacing 30
            xoffset 60
            yoffset 160

            for i, item in enumerate(inventory.visible_inventory):
                use inventory_slot(item, slot_index=i)

    # Name badge for the hovered tile. Drawn here rather than inside the slot so
    # it gets the full screen width and long names stay on one line.
    if hovered_item_name:
        frame:
            xpos 205
            ypos 160 + hovered_item_slot * 160 + 42
            background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
            padding gui.notify_frame_borders.padding
            text "[hovered_item_name]":
                style "notify_text"
                xmaximum 420


screen inventory_slot(item=None, slot_index=0):
    # This screen is used by the inventory screen to create slots for
    # each item. You never need to call this explicitly.

    default show_overlay = False
    default show_info = False

    $ name = item.name if item != None else "No name provided"
    $ image_name = item.image_name if item != None else ""
    $ description = item.description if item != None else "No description provided"
    $ is_evidence_item = (item in store.evidence._inventory) if item != None else False
    # Usable evidence reagents (e.g. Buffer ATL + ProK) keep their own action.
    $ has_own_action = (item is not None and item.usable and item.action is not None)
    $ usable = (item.usable or is_evidence_item) if item != None else False
    $ item_action = (
        item.action if has_own_action
        else (Function(toggle_hold_evidence, item) if is_evidence_item else (item.action if item != None else None))
    )

    fixed:
        fit_first True
        xysize (130, 130)

        mousearea:
            area (0, 0, 130, 130)
            hovered [
                SetLocalVariable("show_overlay", True),
                Function(inventory_hover_enter, name, slot_index),
            ]
            unhovered [
                SetLocalVariable("show_overlay", False),
                Function(inventory_hover_exit, name),
            ]

        add "inventory-slot"

        if image_name != "":
            add Transform(image_name, xysize=(90, 90), xoffset=20, yoffset=20)
            
            if name == "Evidence Bag":
                text "x[evidence_bags_left]" color "#fff" size 18 bold True xalign 0.85 yalign 0.85
        
            if show_overlay:
                add Transform("inventory-item-overlay", yzoom=0.67, xzoom=0.6)

                hbox:
                    spacing 10
                    xoffset 15
                    yoffset 40

                    imagebutton:
                        auto "use-inventory-item-%s" at Transform(zoom=0.47)
                        action Function(use_item, usable, item_action)
                        sensitive usable

                    imagebutton:
                        auto "view-inventory-item-%s" at Transform(zoom=0.47)
                        action Function(view_item, name=name, image_name=image_name, description=description)


screen inventory_info(name="", image_name="", description=""):
    # Shown above the inventory (zorder 300). Click outside, Escape, or Close to dismiss.

    modal True
    zorder 300

    key "K_ESCAPE" action Hide("inventory_info")
    key "mouseup_3" action Hide("inventory_info")

    # Backdrop dismiss.
    button:
        background "#000000aa"
        xfill True
        yfill True
        action Hide("inventory_info")

    # Card content (absorbs clicks so backdrop does not steal Close).
    frame:
        xalign 0.5
        yalign 0.5
        xmaximum 920
        ymaximum 760
        background None
        padding (20, 20)

        fixed:
            xysize (880, 720)

            # Absorb clicks on the card body (not the Close button).
            button:
                background None
                xpos 0
                ypos 0
                xysize (880, 620)
                action NullAction()

            if image_name == "images/transcript.png":
                add Transform(image_name, zoom=0.85, xalign=0.5, yalign=0.32)
            else:
                add Transform("inventory-icon-bg", zoom=0.7, xalign=0.5, yalign=0.38)
                add Transform(image_name, xysize=(200, 200), xalign=0.5, yalign=0.32)

            text "[name]":
                size 28
                xalign 0.5
                yalign 0.58
                color "#ffffff"
                outlines [ (1, "#000000", 0, 0) ]

            text "[description]":
                size 22
                xalign 0.5
                yalign 0.70
                xmaximum 780
                text_align 0.5
                color "#eeeeee"
                outlines [ (1, "#000000", 0, 0) ]

            textbutton "Close":
                action Hide("inventory_info")
                text_size 32
                xalign 0.5
                yalign 0.92
                background "#333333cc"
                hover_background "#555555"
                padding (24, 12)


screen evidence_collected_notice(item_name="Evidence"):
    zorder 200

    frame at evidence_notice_appear:
        xalign 0.98
        yalign 0.14
        xmaximum 540
        padding (24, 20)
        background Solid("#17354aee")

        vbox:
            spacing 8

            text "EVIDENCE COLLECTED":
                size 24
                color "#8fd3ff"
                bold True

            text "[item_name]":
                size 22
                color "#ffffff"
                bold True

            text "It was added to your Evidence inventory. Open the Evidence tab and click the hand button to hold it.":
                size 18
                color "#e2edf3"

    timer 4.5 action Hide("evidence_collected_notice")


transform evidence_notice_appear:
    on show:
        alpha 0.0
        xoffset 50
        easeout 0.25 alpha 1.0 xoffset 0
    on hide:
        easein 0.25 alpha 0.0 xoffset 50


screen deferred_lab_transition():
    # Invisible queue: waits for the current collection/packing interaction to
    # finish before allowing Nina's lab-transition dialogue to begin.
    timer 0.25 repeat True action Function(begin_pending_lab_transition)


screen open_inv():
    zorder 200
    # This screen is a button that allows the player to open the inventory.
    if (
        not renpy.get_screen("inventory")
        and not renpy.get_screen("backing_card_form_screen")
        and not renpy.get_screen("scalebar_label_screen")
        and not renpy.get_screen("camera_setup_screen")
        and not renpy.get_screen("camera_preview_ui")
        and not renpy.get_screen("photo_score_display")
        and not renpy.get_screen("photo_album")
        and not renpy.get_screen("photo_viewer")
        and not renpy.get_screen("pack_evidence_screen")
        and not renpy.get_screen("blood_test_screen")
    ):
        imagebutton:
            auto "open-inv-%s" at Transform(yalign=0.53)
            action [SetVariable("dialogue_boxes_visible", False), Show("inventory"), Hide("open_inv")]

        if getattr(store, "held_evidence", None) is not None:
            frame:
                background "#e67e22dd"
                padding (15, 10)
                align (0.5, 0.05)
                hbox:
                    spacing 15
                    align (0.5, 0.5)
                    add Transform(held_evidence.image_name, xysize=(50, 50), yalign=0.5)
                    vbox:
                        spacing 5
                        text "Holding: [held_evidence.name]" size 18 color "#ffffff" bold True xalign 0.5
                        if not asked_lab_transition:
                            text "Open Toolbox -> Click 'Evidence Bag' to pack it." size 14 color "#eeeeee" xalign 0.5


default selected_inventory = toolbox
default inventory_open = False

# Set while the courtroom scenario owns the shared say/input/inventory screens.
default hovered_item_name = ""
default hovered_item_slot = 0

default courtroom_ui_active = False
# Lowered while the inventory covers the courtroom's dialogue box.
default dialogue_boxes_visible = True

screen blood_test_screen(location="lamp"):
    modal True
    zorder 120
    add Solid("#000000b8")

    $ _applied = blood_test_applied_count(location)
    $ _positive = get_blood_test_positive(location)
    $ _label = BLOOD_TEST_LABELS.get(location, location)
    $ _instruction = blood_test_instruction(location)

    frame:
        align (0.5, 0.5)
        background Frame("gui/frame.png", 10, 10)
        padding (36, 30)
        xsize 720

        vbox:
            spacing 14
            xfill True

            text "Presumptive Blood Test" size 30 color "#ffffff" bold True xalign 0.5
            text "Location: [_label]" size 20 color "#dddddd" xalign 0.5

            # Reaction / swab area only — no reagent list (students discover tools themselves).
            fixed:
                xysize (280, 180)
                xalign 0.5

                frame:
                    xysize (280, 180)
                    background "#2b2b2b"
                    padding (12, 12)

                    vbox:
                        spacing 8
                        xalign 0.5
                        yalign 0.5
                        text "Testing swab" size 18 color "#aaaaaa" xalign 0.5

                        if _positive:
                            frame:
                                xysize (160, 70)
                                background "#ff4d8d"
                                xalign 0.5
                                text "PINK +" size 28 color "#ffffff" bold True xalign 0.5 yalign 0.5
                        elif _applied > 0:
                            frame:
                                xysize (160, 70)
                                background "#e8e8e8"
                                xalign 0.5
                                text "Waiting..." size 18 color "#555555" xalign 0.5 yalign 0.5
                        else:
                            frame:
                                xysize (160, 70)
                                background "#555555"
                                xalign 0.5
                                text "Ready" size 18 color "#cccccc" xalign 0.5 yalign 0.5

            frame:
                background "#1a3344"
                padding (16, 12)
                xfill True
                text "[_instruction]" size 18 color "#eeeeee"

            if _positive:
                text "TEST COMPLETE — Presumptive positive only, not a confirmatory human-blood ID." size 16 color "#f1c40f" bold True xalign 0.5
            else:
                text "Close this panel, choose reagents from the toolbox, then click the stain to apply them." size 15 color "#cccccc" xalign 0.5

            textbutton "Close":
                xalign 0.5
                text_size 22
                action Function(close_blood_test_screen)

screen pack_evidence_screen():
    modal True
    add Solid("#000b")
    
    frame:
        align (0.5, 0.5)
        background Frame("gui/frame.png", 10, 10)
        padding (45, 40)
        xsize 700
        ysize 650
        
        vbox:
            spacing 25
            align (0.5, 0.5)
            
            text "Evidence Packing Station" size 30 color "#fff" bold True xalign 0.5
            
            # The bag and the evidence item
            fixed:
                xysize (350, 350)
                xalign 0.5
                
                # Draw the evidence item first (so it appears inside the bag)
                if store.held_evidence:
                    add Transform(store.held_evidence.image_name, zoom=1.5, xalign=0.5, yalign=0.5)
                
                # Draw the transparent evidence bag on top of it
                add Transform("inventory-evidence_bag", zoom=1.5, xalign=0.5, yalign=0.5)
                    
                # If sealed, draw the tamper evident tape on top of the bag's seal area (near the top)
                if store.bag_sealed:
                    add Transform("toolbox-tamper_evident_tape", zoom=0.7, xalign=0.5, yalign=0.18, yoffset=10)
            
            # Status and controls
            if not store.bag_sealed:
                vbox:
                    spacing 10
                    xalign 0.5
                    text "Bag Status: UNSEALED" color "#e74c3c" bold True xalign 0.5 size 20
                    
                    # Clickable tape button to seal it
                    imagebutton:
                        idle "toolbox-tamper_evident_tape"
                        hover "toolbox-tamper_evident_tape"
                        action SetVariable("bag_sealed", True)
                        align (0.5, 0.5)
                        at Transform(zoom=0.8)
                        tooltip "Apply Tamper Evident Tape to seal"
                    text "Click tape to seal the bag" size 14 color "#aaa" xalign 0.5
            else:
                vbox:
                    spacing 10
                    xalign 0.5
                    text "Bag Status: SEALED" color "#2ecc71" bold True xalign 0.5 size 20
                    text "Ready to store in evidence inventory." size 14 color "#aaa" xalign 0.5
            
            hbox:
                spacing 40
                xalign 0.5
                yoffset 10
                
                textbutton "Finish Packing" action Function(finish_packing_evidence):
                    padding (20, 10)
                    background "#27ae60"
                    hover_background "#2ecc71"
                
                textbutton "Cancel" action [Hide("pack_evidence_screen"), Show("inventory")]:
                    padding (20, 10)
                    background "#c0392b"
                    hover_background "#e74c3c"

