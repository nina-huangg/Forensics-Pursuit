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


    def view_item(name, image_name, description) -> None:
        """
        This function is used in the click action of screen inventory_slot's
        view-inventory-item button.
        """
        scr = renpy.get_screen("inventory_info")

        if scr and scr.scope.get("name") != name:
            renpy.hide_screen("inventory_info")
            renpy.show_screen("inventory_info", name=name, image_name=image_name, description=description)
        elif scr and scr.scope.get("name") == name:
            renpy.hide_screen("inventory_info")
        else:
            renpy.show_screen("inventory_info", name=name, image_name=image_name, description=description)
    

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
    
default toolbox = Inventory()
default evidence = Inventory()

screen inventory():
    # This is the main screen for the inventory. To use it, write either
    # "show screen inventory" or "call screen inventory". In almost all
    # cases, you will want to use the former to allow screens below to
    # be clickable. However, if you want to force the player to interact
    # with the inventory before moving on, use the latter.

    $ inventory = selected_inventory

    frame:
        background None

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

        imagebutton:
            auto "close-inv-%s" at Transform(rotate=1, xoffset=49, yoffset=350)
            action [ToggleScreen("inventory"), ToggleScreen("open_inv")]


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
                use inventory_slot(item)


screen inventory_slot(item=None):
    # This screen is used by the inventory screen to create slots for
    # each item. You never need to call this explicitly.

    default show_overlay = False
    default show_info = False

    $ name = item.name if item != None else "No name provided"
    $ image_name = item.image_name if item != None else ""
    $ description = item.description if item != None else "No description provided"
    $ usable = item.usable if item != None else False
    $ item_action = item.action if item != None else None

    fixed:
        fit_first True
        xysize (130, 130)

        mousearea:
            area (0, 0, 130, 130)
            hovered SetLocalVariable("show_overlay", True)
            unhovered SetLocalVariable("show_overlay", False)

        add "inventory-slot"

        if image_name != "":
            fixed:
                add Transform(image_name, zoom=0.45, xoffset=20, yoffset=20)
                xsize 90
                ysize 90
        
            if show_overlay:
                add Transform("inventory-item-overlay", yzoom=0.67, xzoom=0.6)

                hbox:
                    spacing 10
                    xoffset 15
                    yoffset 40

                    imagebutton:
                        auto "use-inventory-item-%s" at Transform(zoom=0.47)
                        action Function(use_item, usable, item_action)

                    imagebutton:
                        auto "view-inventory-item-%s" at Transform(zoom=0.47)
                        action Function(view_item, name=name, image_name=image_name, description=description)

screen inventory_info(name="", image_name="", description=""):
    # This screen is used by the inventory screen to display information
    # about an item when the player chooses to view more information about it.
    # You never need to call this explicitly.

    modal True
    add Solid("#0008")
    add Transform("inventory-icon-bg", zoom=0.7, xalign=0.5, yalign=0.5)
    add Transform(image_name, xalign=0.5, yalign=0.45)
    text f"{name}" at Transform(xalign=0.5, yalign=0.57)
    text f"{description}":
        size 24
        xpos 600
        xmaximum 780
        yalign 0.64
    
    textbutton "✕":
        action Hide("inventory_info")
        text_size 60
        xalign 0.65
        yalign 0.34


screen open_inv():
    # This screen is a button that allows the player to open the inventory.
    # This is also shown when the player closes the inventory.
    # You can use this if you'd like, but it would probably be easier to
    # just use the inventory screen instead.

    imagebutton:
        auto "open-inv-%s" at Transform(yalign=0.53)
        action [ToggleScreen("open_inv"), ToggleScreen("inventory")]


default selected_inventory = toolbox
