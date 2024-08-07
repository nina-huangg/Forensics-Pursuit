init python:
    # INVENTORY FUNCTIONS -----------------------------------------------
    """
    Handles hover  - show hand and inspect icons
    Parameters: current event, xy positions of cursor as event occurr, and "at" = time since the sprite is shown on screen (ignore)
    """
    def inventoryEvents(event, x, y, at):
        global mousepos
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in inventory_sprites:
                    if item1.visible == True:
                        item1.x = item1.original_x
                        item1.y = item1.original_y
                        item1.zorder = 0
        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousepos = (x, y)
            for item in inventory_sprites:
                if item.visible == True:
                    if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                        renpy.show_screen("inventoryItemMenu", item = item)
                        renpy.restart_interaction()
                        break
                    else:
                        renpy.hide_screen("inventoryItemMenu")
                        renpy.restart_interaction()

    def toolboxEvents(event, x, y, at):
        global mousepos
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in toolbox_sprites:
                    if item1.visible == True:
                        item1.x = item1.original_x
                        item1.y = item1.original_y
                        item1.zorder = 0
        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousepos = (x, y)
            for item in toolbox_sprites:
                if item.visible == True:
                    if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                        renpy.show_screen("toolboxItemMenu", item = item)
                        renpy.restart_interaction()
                        break
                    else:
                        renpy.hide_screen("toolboxItemMenu")
                        renpy.restart_interaction()

    def toolboxPopupEvents(event, x, y, at):
        global mousepos
        global dialogue
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in toolboxpop_sprites:
                    if item1.visible == True:
                        item1.x = item1.original_x
                        item1.y = item1.original_y
                        item1.zorder = 0

        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousepos = (x, y)
            for item in toolboxpop_sprites:
                if item.visible == True:
                    if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                        renpy.show_screen("toolboxPopItemMenu", item = item)
                        renpy.restart_interaction()
                        break
                    else:
                        renpy.hide_screen("toolboxPopItemMenu")
                        renpy.restart_interaction()

    """
    Repositions after reopen.
    """
    def repositionInventoryItems():
        global inventory_ub_enabled
        global inventory_db_enabled

        for i, item in enumerate(inventory_sprites):
            item.x = first_slot_x
            item.original_x = item.x
            item.y = (first_slot_y + distance_slot * i)
            item.original_y = item.y
            if item.y < first_slot_y or item.y > (first_slot_y + (item.height * 4)) + (slot_padding * 3):
                setItemVisibility(item = item, visible = False)
            elif item != "": # prevent errors
                setItemVisibility(item = item, visible = True)

        if len(inventory_sprites) > 0:
            if inventory_sprites[-1].visible == True:
                inventory_db_enabled = False
            else:
                inventory_db_enabled = True
            if inventory_sprites[0].visible == True:
                inventory_ub_enabled = False
            else:
                inventory_ub_enabled = True

    def repositionToolboxItems():
        global toolbox_ub_enabled
        global toolbox_db_enabled
        for i, item in enumerate(toolbox_sprites):
            item.x = first_slot_x
            item.original_x = item.x
            item.y = (first_slot_y + distance_slot * i)
            item.original_y = item.y
            if item.y < first_slot_y or item.y > (first_slot_y + (item.height * 4)) + (slot_padding * 3):
                setItemVisibility(item = item, visible = False)
            elif item != "": # prevent errors
                setItemVisibility(item = item, visible = True)

        if len(toolbox_sprites) > 0:
            if toolbox_sprites[-1].visible == True:
                toolbox_db_enabled = False
            else:
                toolbox_db_enabled = True
            if toolbox_sprites[0].visible == True:
                toolbox_ub_enabled = False
            else:
                toolbox_ub_enabled = True

    def repositionToolboxPopItems():
        global toolboxpop_ub_enabled
        global toolboxpop_db_enabled
        for i, item in enumerate(toolboxpop_sprites):
            item.x = toolboxpop_first_slot_x
            item.original_x = item.x
            item.y = (toolboxpop_first_slot_y + distance_slot * i)
            item.original_y = item.y
            if item.y < toolboxpop_first_slot_y or item.y > (toolboxpop_first_slot_y + (item.height * 2)) + (slot_padding * 1):
                setItemVisibility(item = item, visible = False)
            elif item != "": # prevent errors
                setItemVisibility(item = item, visible = True)

        if len(toolboxpop_sprites) > 0:
            if toolboxpop_sprites[-1].visible == True:
                toolboxpop_db_enabled = False
            else:
                toolboxpop_db_enabled = True
            if toolboxpop_sprites[0].visible == True:
                toolboxpop_ub_enabled = False
            else:
                toolboxpop_ub_enabled = True


    """
    Adds item list
    """
    def addToInventory(items):
        for item in items:
            inventory_items.append(item)
            item_image = Image("Inventory Items/inventory-{}.png".format(item))
            temp_name = item.replace(" ", "_")

            t = Transform(child = item_image, zoom = 0.5)
            inventory_sprites.append(inventory_SM.create(t))
            # sprite we just created
            inventory_sprites[-1].width = slot_size[0]
            inventory_sprites[-1].height = slot_size[1]
            inventory_sprites[-1].type = temp_name.lower()
            inventory_sprites[-1].item_image = item_image
            inventory_sprites[-1].y = 500
            inventory_sprites[-1].original_y = 500
            inventory_sprites[-1].original_x = 1000
            inventory_sprites[-1].visible = True
            inventory_sprites[-1].state = "default"

            repositionInventoryItems()

            inventory_SM.redraw(0)
            renpy.restart_interaction()
   
    def addToToolbox(items):
        for item in items:
            toolbox_items.append(item)
            item_image = Image("Toolbox Items/toolbox-{}.png".format(item))
            temp_name = item.replace(" ", "_")

            t = Transform(child = item_image, zoom = 0.5)
            toolbox_sprites.append(toolbox_SM.create(t))
            # sprite we just created
            toolbox_sprites[-1].width = slot_size[0]
            toolbox_sprites[-1].height = slot_size[1]
            toolbox_sprites[-1].type = temp_name.lower()
            toolbox_sprites[-1].item_image = item_image
            toolbox_sprites[-1].y = 500
            toolbox_sprites[-1].original_y = 500
            toolbox_sprites[-1].original_x = 1000
            toolbox_sprites[-1].visible = True
            toolbox_sprites[-1].state = "default"

            repositionToolboxItems()

            toolbox_SM.redraw(0)
            renpy.restart_interaction()

    def addToToolboxPop(items):
        for item in items:
            toolboxpop_items.append(item)
            item_image = Image("Toolbox Items/toolbox-{}.png".format(item))
            temp_name = item.replace(" ", "_")
                
            t = Transform(child = item_image, zoom = 0.5)
            toolboxpop_sprites.append(toolboxpop_SM.create(t))
            # sprite we just created
            toolboxpop_sprites[-1].width = slot_size[0]
            toolboxpop_sprites[-1].height = slot_size[1]
            toolboxpop_sprites[-1].type = temp_name.lower()
            toolboxpop_sprites[-1].item_image = item_image
            toolboxpop_sprites[-1].y = 500
            toolboxpop_sprites[-1].original_y = 500
            toolboxpop_sprites[-1].original_x = 1000
            toolboxpop_sprites[-1].visible = True

            repositionToolboxPopItems()

            toolboxpop_SM.redraw(0)
            renpy.restart_interaction()

    
    """
    Removes -- currently not used (could use for markers)
    """
    def removeToolboxItem(item):
        item.destroy()
        toolbox_sprites.pop(toolbox_sprites.index(item))
        toolbox_items.pop(toolbox_items.index(item.type))
        repositionToolboxItems()

    def removeToolboxPopItem(item):
        item.destroy()
        toolboxpop_sprites.pop(toolboxpop_sprites.index(item))
        toolboxpop_items.pop(toolboxpop_items.index(item.type))
        repositionToolboxPopItems()


    """
    Arrow functionality 
    """
    def inventoryArrows(button):
        # determines if arrow buttons should be enabled or disabled - might change to up and down
        global inventory_ub_enabled
        global inventory_db_enabled

        if len(inventory_sprites) > 4:
            citem = "" # current item
            # iterate through inventory items
            for i, item in enumerate(inventory_sprites):
                # up button 
                if button == "down" and inventory_db_enabled == True:
                    # if last item not visible meaning we have at least 1 extra item
                    if inventory_sprites[-1].visible == False:
                        # shift inventory items up
                        item.y -= distance_slot
                        item.original_y = item.y # added
                        citem = item
                elif button == "up" and inventory_ub_enabled == True:
                    if inventory_sprites[0].visible == False:
                        item.y += distance_slot
                        item.original_y = item.y # added
                        citem = item
                # checks if item was moved beyond first or beyond last item in inventory slots
                if citem != "" and (citem.y < first_slot_y or citem.y > (first_slot_y + (item.height * 4)) + (slot_padding * 4)):
                    setItemVisibility(item = item, visible = False)
                elif citem != "": # prevent errors
                    setItemVisibility(item = item, visible = True)

            if inventory_sprites[-1].visible == True:
                inventory_db_enabled = False
            else:
                inventory_db_enabled = True
            if inventory_sprites[0].visible == True:
                inventory_ub_enabled = False
            else:
                inventory_ub_enabled = True
                
            inventory_SM.redraw(0)
            renpy.restart_interaction
    
    def toolboxArrows(button):
        # determines if arrow buttons should be enabled or disabled - might change to up and down
        global toolbox_ub_enabled
        global toolbox_db_enabled

        # check if we have more than 4 items in toolbox (4 is max)
        if len(toolbox_sprites) > 4:            
            # iterate through toolbox items
            for i, item in enumerate(toolbox_sprites):
                if button == "down" and toolbox_db_enabled == True:
                    # if last item not visible meaning we have at least 1 extra item
                    if toolbox_sprites[-1].visible == False:
                        # shift toolbox items up
                        item.y -= distance_slot # changed
                        item.original_y = item.y # added
                elif button == "up" and toolbox_ub_enabled == True:
                    if toolbox_sprites[0].visible == False:
                        item.y += distance_slot
                        item.original_y = item.y # added
                # checks if item was moved beyond first or beyond last item in toolbox slots
                if item != "" and (item.y < first_slot_y) or (item.y > (first_slot_y + (item.height * 4) + (slot_padding * 3))):
                    setItemVisibility(item = item, visible = False)
                elif item != "": # prevent errors
                    setItemVisibility(item = item, visible = True)

            if toolbox_sprites[-1].visible == True:
                toolbox_db_enabled = False
            else:
                toolbox_db_enabled = True
            if toolbox_sprites[0].visible == True:
                toolbox_ub_enabled = False
            else:
                toolbox_ub_enabled = True
                
            toolbox_SM.redraw(0)
            renpy.restart_interaction

    def toolboxPopArrows(button):
        # determines if arrow buttons should be enabled or disabled - might change to up and down
        global toolboxpop_ub_enabled
        global toolboxpop_db_enabled

        # check if we have more than 5 items in toolbox (5 is max)
        if len(toolboxpop_sprites) > 2:

            # iterate through toolbox items
            for i, item in enumerate(toolboxpop_sprites):
                # up button 
                if button == "down" and toolboxpop_db_enabled == True:
                    # if last item not visible meaning we have at least 1 extra item
                    if toolboxpop_sprites[-1].visible == False:
                        # shift toolbox items up
                        item.y -= distance_slot
                elif button == "up" and toolboxpop_ub_enabled == True:
                    if toolboxpop_sprites[0].visible == False:
                        item.y += distance_slot
                        item.original_y = item.y # added
                # checks if item was moved beyond first or beyond last item in toolbox slots
                if item != "" and (item.y < toolboxpop_first_slot_y or item.y > (toolboxpop_first_slot_y + (item.height * 2)) + (slot_padding * 1)):
                    setItemVisibility(item = item, visible = False)

                elif item != "": # prevent errors
                    setItemVisibility(item = item, visible = True)

            if toolboxpop_sprites[-1].visible == True:
                toolboxpop_db_enabled = False
            else:
                toolboxpop_db_enabled = True
            if toolboxpop_sprites[0].visible == True:
                toolboxpop_ub_enabled = False
            else:
                toolboxpop_ub_enabled = True
                
            toolboxpop_SM.redraw(0)
            renpy.restart_interaction


    """
    Item visibility in the toolbar
    """
    def setItemVisibility(item, visible):
        if visible == False:
            item.visible = False
            t = Transform(child = item.item_image, zoom = 0.5, alpha = 0)
            item.set_child(t)
        else:
            item.visible = True
            t = Transform(child = item.item_image, zoom = 0.5, alpha = 100)
            item.set_child(t)
        inventory_SM.redraw(0)
        toolbox_SM.redraw(0)
        toolboxpop_SM.redraw(0)



# INVENTORY SCREENS ------------------------- (might move to custom_screens)
screen full_inventory:
    zorder 1
    image "UI/inv-icon-bg.png" xpos 0.014 ypos -0.03 at half_size
    imagebutton auto "UI/inventory-icon-%s.png" action If(renpy.get_screen("inventory") == None, true= [Show("inventory"), Hide("toolbox"), Hide("toolboxpop")], 
                                                        false= [Hide("inventory"), Hide("toolboxpop"), Hide("toolboxpop")]) xpos 0.087 ypos 0.02 at half_size
    imagebutton auto "UI/tool-inventory-icon-%s.png" action If(renpy.get_screen("toolbox") == None, true= [Function(repositionToolboxItems), Show("toolbox"), Hide("inventory"), Hide("toolboxpop"), 
                                                                                                            Hide('physical_screen', _layer='over_screens'), Hide('digital_screen', _layer='over_screens')],
                                                            false= [Hide("toolbox"), Hide("toolboxpop"), Hide("toolboxpop"), Hide('physical_screen', _layer='over_screens'), 
                                                                    Hide('digital_screen', _layer='over_screens')]) xpos 0.037 ypos 0.02 at half_size

# Evidence box:
screen inventory:
    zorder 3
    image "UI/inventory-bg.png" xpos 0.02 ypos 0.09 at half_size
    image "UI/inventory-slots.png" xpos 0.047 ypos 0.25 at half_size
    imagebutton idle If(inventory_db_enabled == True, true= "UI/inventory-arrow-down-enabled-idle.png", false= "UI/inventory-arrow-down-disabled.png") hover If(inventory_db_enabled == True, true= "UI/inventory-arrow-down-enabled-hover.png", false= "UI/inventory-arrow-down-disabled.png") action Function(inventoryArrows, button = "down") xpos 0.063 ypos 0.89 at half_size
    imagebutton idle If(inventory_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-idle.png", false= "UI/inventory-arrow-up-disabled.png") hover If(inventory_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-hover.png", false= "UI/inventory-arrow-up-disabled.png") action Function(inventoryArrows, button = "up") xpos 0.063 ypos 0.15 at half_size
    add inventory_SM

# Toolbox:
screen toolbox:
    zorder 3
    image "UI/tools-bg.png" xpos 0.02 ypos 0.09 at half_size
    image "UI/inventory-slots.png" xpos 0.047 ypos 0.25 at half_size
    imagebutton idle If(toolbox_db_enabled == True, true= "UI/inventory-arrow-down-enabled-idle.png", false= "UI/inventory-arrow-down-disabled.png") hover If(toolbox_db_enabled == True, true= "UI/inventory-arrow-down-enabled-hover.png", false= "UI/inventory-arrow-down-disabled.png") action Function(toolboxArrows, button = "down") xpos 0.063 ypos 0.89 at half_size
    imagebutton idle If(toolbox_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-idle.png", false= "UI/inventory-arrow-up-disabled.png") hover If(toolbox_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-hover.png", false= "UI/inventory-arrow-up-disabled.png") action Function(toolboxArrows, button = "up") xpos 0.063 ypos 0.15 at half_size
    add toolbox_SM

# Secondary toolbox:
screen toolboxpop:
    zorder 3
    image "UI/toolboxpop-bg.png" xpos 0.13 ypos 0.28 at half_size
    image "UI/toolboxpop-slots.png" xpos 0.1415 ypos 0.41 at half_size
    imagebutton idle If(toolboxpop_db_enabled == True, true= "UI/inventory-arrow-down-enabled-idle.png", false= "UI/inventory-arrow-down-disabled.png") hover If(toolboxpop_db_enabled == True, true= "UI/inventory-arrow-down-enabled-hover.png", false= "UI/inventory-arrow-down-disabled.png") action Function(toolboxPopArrows, button = "down") xpos 0.157 ypos 0.73 at half_size
    imagebutton idle If(toolboxpop_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-idle.png", false= "UI/inventory-arrow-up-disabled.png") hover If(toolboxpop_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-hover.png", false= "UI/inventory-arrow-up-disabled.png") action Function(toolboxPopArrows, button = "up") xpos 0.157 ypos 0.32 at half_size
    add toolboxpop_SM

# Evidence box item menu
screen inventoryItemMenu(item):
    zorder 7
    frame:
        xysize (slot_size[0], slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("inventoryItemMenu")]
        if item.type == "bag" or item.type == "tape":
            imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Function(set_tool, item.type), Hide("inventoryItemMenu")]
        elif item.type == "physical_evidence":
            imagebutton auto "UI/expand-inventory-item-%s.png" align (1.0, 0.5) at half_size action [ToggleVariable('show_physical'), Hide("inventoryItemMenu"), Show('physical_screen', _layer='over_screens')]
        elif item.type == "digital_evidence":
            imagebutton auto "UI/expand-inventory-item-%s.png" align (1.0, 0.5) at half_size action [ToggleVariable('show_digital'), Hide("inventoryItemMenu"), Show('digital_screen', _layer='over_screens')]

# Toolbox item menu
screen toolboxItemMenu(item):
    zorder 7
    frame:
        xysize (slot_size[0], slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Hide("toolboxpop"), Show("inspectItem", items = [item.type])]
        imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Hide("toolboxpop"), Function(set_tool, item.type)]


# Secondary toolbox item menu
screen toolboxPopItemMenu(item):
    zorder 7
    frame:
        xysize (slot_size[0], slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("toolboxPopItemMenu")]
        imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Function(set_tool, item.type), Hide("toolboxPopItemMenu")]


"""
Item inspection (info button)
"""
screen inspectItem(items):
    modal True
    zorder 4
    button:
        xfill True
        yfill True
        action If(len(items) > 1, true = RemoveFromSet(items, items[0]), false= [Hide("inspectItem")])
        image "Items Pop Up/items-pop-up-bg.png" align (0.5, 0.55) at half_size

        python:
            item_name = ""
            item_desc = ""
            for name in inventory_item_names:
                temp_name = name.replace(" ", "-")
                temp_name = name.replace(" ", "_")
                if temp_name.lower() == items[0]:
                    item_name = name

        text "{}".format(item_name) size 30 align (0.5, 0.65) color "#000000"
        image "Items Pop Up/{}-pop-up.png".format(items[0]) align (0.5, 0.5) at half_size
