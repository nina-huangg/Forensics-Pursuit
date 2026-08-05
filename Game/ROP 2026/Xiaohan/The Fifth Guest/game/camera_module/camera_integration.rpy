## The Fifth Guest — camera module bridge
## Registers locations, maps photos to evidence Items, opens viewfinder from hotspots.
## Does NOT use SpriteManager inventory instructions from upstream.

init -4 python:

    CAMERA_LOCATION_EVIDENCE = {
        "shoeprint": "Photo of Shoeprint",
        "shoeprint_scale": "Photo of Shoeprint with Scalebar",
        "blood_splatter": "Photo of Blood Splatter",
        "lamp_far": "Photo of Lamp (Far)",
        "lamp_close": "Photo of Lamp",
        "blood_pool": "Photo of Blood Pool",
        # fingerprint resolved dynamically
    }

    CAMERA_LOCATION_BASE_IMAGES = {
        "shoeprint": "images/Scenes/door-view-bg.png",
        "shoeprint_scale": "images/Scenes/door-view-bg.png",
        "blood_splatter": "images/Scenes/study-bg.png",
        "lamp_far": "images/Scenes/study-bg.png",
        "lamp_close": "images/Scenes/lamp-bg.png",
        "blood_pool": "images/Scenes/blood-pool-bg.png",
        "fingerprint": "images/Scenes/fingerprint-zoom-bg.png",
    }

    def resolve_fingerprint_photo_name():
        """Match prior fingerprint photo selection rules."""
        if not store.fingerprint_powder and not store.fingerprint_scalebar_placed:
            if not store.fingerprint_circled:
                return "Fingerprint Alone Photo"
            return "Fingerprint Circled Photo"
        return "Fingerprint Photo"

    def resolve_camera_evidence_name(location_id):
        if location_id == "fingerprint":
            return resolve_fingerprint_photo_name()
        return CAMERA_LOCATION_EVIDENCE.get(location_id)

    def evidence_item_already_collected(item_name):
        item = store.evids.get(item_name) if store.evids else None
        if item is None:
            return False
        return item in store.evidence._inventory

    def camera_on_photo_taken(location_id):
        """Grant the matching evidence Item once via evidence.add_to_inventory."""
        item_name = resolve_camera_evidence_name(location_id)
        if not item_name:
            return

        item = store.evids.get(item_name)
        if item is None:
            renpy.notify("Missing evidence definition: {}".format(item_name))
            return

        if item in store.evidence._inventory:
            # Retake path: album already has another shot; do not duplicate Item.
            return

        store.evidence.add_to_inventory(item)

        if location_id == "shoeprint_scale":
            store.scalebar_placed = False

        if item_name == "Fingerprint Photo":
            store.fingerprint_photo_taken = True

    def initialize_camera_system():
        """Fresh camera config/state for New Game / route resets."""
        reset_scoring_config_cache()

        cc = CameraConfig()
        cc.font = "ConcertOne-Regular.ttf"
        cc.scoring_config_path = "camera_scoring_config.json"
        cc.on_photo_taken = camera_on_photo_taken

        cc.register_location(
            "shoeprint", "Shoeprint (No Scale)",
            CAMERA_LOCATION_BASE_IMAGES["shoeprint"],
        )
        cc.register_location(
            "shoeprint_scale", "Shoeprint (With Scale)",
            CAMERA_LOCATION_BASE_IMAGES["shoeprint_scale"],
        )
        cc.register_location(
            "blood_splatter", "Blood Splatter",
            CAMERA_LOCATION_BASE_IMAGES["blood_splatter"],
        )
        cc.register_location(
            "lamp_far", "Lamp (Far)",
            CAMERA_LOCATION_BASE_IMAGES["lamp_far"],
        )
        cc.register_location(
            "lamp_close", "Lamp (Close)",
            CAMERA_LOCATION_BASE_IMAGES["lamp_close"],
        )
        cc.register_location(
            "blood_pool", "Blood Pool",
            CAMERA_LOCATION_BASE_IMAGES["blood_pool"],
        )
        cc.register_location(
            "fingerprint", "Fingerprint",
            CAMERA_LOCATION_BASE_IMAGES["fingerprint"],
        )

        store.camera_config = cc
        store.camera_state = CameraState()
        store.current_photo_location = ""
        store.photos_taken_locations = []
        store.last_photo_score = None
        store.camera_hint_level = 0
        store.camera_hint_text = ""
        store.pending_photo_location = ""
        store.pending_photo_accepted = False

        # Prefetch scoring config so first photo does not fail loudly
        load_scoring_config(force=True)

    def open_crime_scene_camera(location_id, already_msg=None):
        """
        Set registered location and open the overlay viewfinder.
        Requires camera to already be the active tool (caller checks).
        """
        if store.camera_config is None or store.camera_state is None:
            initialize_camera_system()

        if location_id not in store.camera_config.locations:
            renpy.notify("Unknown photo location: {}".format(location_id))
            return

        if location_id == "fingerprint":
            missing = missing_fingerprint_camera_attachment()
            if missing is not None:
                reset_tool()
                renpy.call_in_new_context(
                    "nina_fingerprint_camera_setup_warning",
                    missing,
                )
                renpy.restart_interaction()
                return

        item_name = resolve_camera_evidence_name(location_id)
        if item_name and evidence_item_already_collected(item_name):
            renpy.notify(already_msg or "You already have {}.".format(item_name))
            reset_tool()
            renpy.restart_interaction()
            return

        store.current_photo_location = location_id
        # Unequip happens inside camera_open_viewfinder as well
        camera_open_viewfinder()
