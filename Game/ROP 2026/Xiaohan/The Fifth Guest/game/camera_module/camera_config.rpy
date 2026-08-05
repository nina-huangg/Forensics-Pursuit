## Camera Module - Configuration & State
## Adapted for The Fifth Guest (Item/Inventory evidence system)
## All-overlay architecture: no label jumps, no scene changes

init python:

    class CameraConfig(object):
        def __init__(self):
            # Camera hardware constants
            self.aperture_group = ["F5.6", "F8", "F11", "F16"]
            self.iso_group = [100, 200, 300, 400, 800]
            self.iso_to_alpha = {100: 0.2, 200: 0.4, 300: 0.6, 400: 0.8, 800: 1.0}
            self.focal_lengths = ["50mm", "105mm"]
            self.zoom_ranges = {
                "50mm": (1.0, 2.0),
                "105mm": (3.0, 4.0),
            }

            # Location registry: { location_id: {"name": display_name} }
            self.locations = {}

            # Optional custom completeness scorer
            self.custom_completeness_scorer = None

            # Called after a photo is saved: on_photo_taken(location_id)
            self.on_photo_taken = None

            # Optional location -> base image fallback when aperture variants are missing
            self.location_base_images = {}

            # UI configuration
            self.font = "ConcertOne-Regular.ttf"
            self.scoring_config_path = "camera_scoring_config.json"

        def register_location(self, location_id, name, base_image=None):
            self.locations[location_id] = {"name": name}
            if base_image:
                self.location_base_images[location_id] = base_image


    class CameraState(object):
        def __init__(self):
            self.reset_viewfinder()
            self.photo_data = []
            self.photo_show_index = 0
            self.show_info_overlay = True
            self.active = False  # True when viewfinder is open

        def reset_viewfinder(self):
            self.theme_x = 0.54
            self.theme_y = 0.54
            self.theme_zoom = 2.0
            self.aperture = 1
            self.iso_index = 1
            self.focal_len = "50mm"

        def save_photo(self, location_id):
            self.photo_data.append({
                "location": location_id,
                "iso_index": self.iso_index,
                "aperture_index": self.aperture,
                "zoom_level": self.theme_zoom,
                "lens": self.focal_len,
                "theme_x": self.theme_x,
                "theme_y": self.theme_y,
            })


    ## ---- Core camera functions (called from screen actions) ----

    def camera_reset_equipped_tool():
        """Unequip camera/tool cursor so the viewfinder does not leave it active."""
        store.active_tool = None
        store.default_mouse = "default"

    def camera_get_location_image(location_id, aperture_number):
        """Resolve aperture image, falling back to a registered base scene image."""
        primary = "camera/{}-{}.png".format(location_id, aperture_number)
        if renpy.loadable(primary):
            return primary

        cc = store.camera_config
        if cc is not None:
            base = cc.location_base_images.get(location_id)
            if base and renpy.loadable(base):
                return base

        # Last resort: avoid hard crash with a solid placeholder if nothing loads
        if renpy.loadable("gui/frame.png"):
            return "gui/frame.png"
        return primary

    def camera_open_viewfinder():
        """Open the camera viewfinder overlay. Called from toolbox/hotspots."""
        cs = store.camera_state
        cc = store.camera_config
        loc = store.current_photo_location

        if cc is None or cs is None:
            renpy.notify("Camera system is not ready.")
            return

        if not loc or loc not in cc.locations:
            renpy.notify("Click a photographic hotspot with the camera equipped first.")
            return

        camera_reset_equipped_tool()
        cs.active = True
        store.camera_hint_level = 0
        renpy.hide_screen("inventory")
        renpy.hide_screen("open_inv")
        renpy.show_screen("camera_preview_ui")
        renpy.restart_interaction()

    def camera_take_photo():
        """Take photo, calculate score, show score overlay.

        Evidence is NOT granted here — only after the player Continues from
        the score screen (and fingerprint requires score >= 90).
        """
        cs = store.camera_state
        loc = store.current_photo_location

        # Save the photo to the album
        cs.save_photo(loc)

        if loc and loc not in store.photos_taken_locations:
            store.photos_taken_locations.append(loc)

        score_data = calculate_photo_score(cs.photo_data[-1])
        store.last_photo_score = score_data
        store.pending_photo_location = loc
        store.pending_photo_accepted = False

        # Fingerprint requires professional quality before evidence is accepted
        if loc == "fingerprint":
            total = score_data.get("total", 0) if score_data else 0
            if total >= 90:
                store.pending_photo_accepted = True
                score_data["acceptance_note"] = (
                    "Score meets the professional standard. Continue to add this fingerprint photograph to evidence."
                )
            else:
                score_data["acceptance_note"] = (
                    "Fingerprint photographs must score at least 90 (grade A). "
                    "This shot stays in your album, but evidence will not be granted — please retake."
                )
                score_data["requires_retake"] = True
        else:
            store.pending_photo_accepted = True

        camera_reset_equipped_tool()

        cs.active = False
        renpy.hide_screen("camera_preview_ui")
        renpy.hide_screen("camera_hint_overlay")
        renpy.show_screen("photo_score_display", score_data=score_data)
        renpy.restart_interaction()

    def camera_accept_pending_photo():
        """Grant evidence for the pending shot if it was accepted."""
        cc = store.camera_config
        loc = store.pending_photo_location
        if not loc:
            return

        if not store.pending_photo_accepted:
            renpy.notify("Photo kept in album only. Retake for a higher score to collect evidence.")
            store.pending_photo_location = ""
            return

        if cc is not None and cc.on_photo_taken is not None:
            try:
                cc.on_photo_taken(loc)
            except Exception as e:
                renpy.notify("Photo saved, but evidence update failed: {}".format(e))

        store.pending_photo_location = ""
        store.pending_photo_accepted = False

    def camera_close_score():
        """Close score overlay after accepting (or declining fingerprint quality)."""
        score = store.last_photo_score or {}
        if score.get("requires_retake"):
            # Fingerprint below threshold: do not grant evidence; stay closable
            # but nudge the player.
            renpy.notify("Retake recommended — fingerprint photo was not added to evidence.")
            store.pending_photo_location = ""
            store.pending_photo_accepted = False
        else:
            camera_accept_pending_photo()

        camera_reset_equipped_tool()
        renpy.hide_screen("photo_score_display")
        if not renpy.get_screen("inventory"):
            renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def camera_retake():
        """Close score overlay and reopen viewfinder without granting evidence."""
        store.pending_photo_location = ""
        store.pending_photo_accepted = False
        renpy.hide_screen("photo_score_display")
        store.camera_state.active = True
        store.camera_hint_level = 0
        camera_reset_equipped_tool()
        renpy.show_screen("camera_preview_ui")
        renpy.restart_interaction()

    def camera_close_viewfinder():
        """Close viewfinder without taking a photo."""
        store.camera_state.active = False
        camera_reset_equipped_tool()
        renpy.hide_screen("camera_preview_ui")
        renpy.hide_screen("camera_hint_overlay")
        if not renpy.get_screen("inventory"):
            renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def camera_open_album():
        """Open photo album as modal overlay."""
        if store.camera_state is None:
            renpy.notify("No photos yet.")
            return
        renpy.hide_screen("inventory")
        renpy.hide_screen("inventory_info")
        renpy.show_screen("photo_album")
        renpy.restart_interaction()

    def camera_close_album():
        """Close photo album overlay."""
        renpy.hide_screen("photo_album")
        if not renpy.get_screen("inventory"):
            renpy.show_screen("open_inv")
        renpy.restart_interaction()

    def camera_open_viewer(index):
        """Open single photo viewer overlay."""
        store.camera_state.photo_show_index = index
        if index >= 0 and index < len(store.camera_state.photo_data):
            renpy.hide_screen("photo_album")
            renpy.show_screen("photo_viewer", index=index)
            renpy.restart_interaction()

    def camera_close_viewer():
        """Close photo viewer, go back to album."""
        renpy.hide_screen("photo_viewer")
        renpy.show_screen("photo_album")
        renpy.restart_interaction()

    def camera_has_photos():
        cs = store.camera_state
        return cs is not None and bool(cs.photo_data)

    def camera_get_progressive_hint():
        """Return the next progressive hint for the current viewfinder settings."""
        cfg = load_scoring_config()
        cs = store.camera_state
        cc = store.camera_config
        loc = store.current_photo_location

        if not cfg or "locations" not in cfg:
            return "Adjust ISO, aperture, lens, zoom, and framing, then take the photo."

        loc_cfg = cfg.get("locations", {}).get(loc)
        if not loc_cfg:
            return "No scoring tips are configured for this location."

        optimal = loc_cfg.get("optimal_settings", {})
        hints = []

        # 1) Lens
        want_lens = optimal.get("lens")
        if want_lens and cs.focal_len != want_lens:
            hints.append(
                "Switch to the {} lens for this subject.".format(want_lens)
            )

        # 2) ISO
        want_iso = optimal.get("iso_index")
        if want_iso is not None and cs.iso_index != want_iso:
            iso_val = cc.iso_group[want_iso] if want_iso < len(cc.iso_group) else want_iso
            hints.append("Set ISO to {} for clean exposure.".format(iso_val))

        # 3) Aperture
        want_ap = optimal.get("aperture_index")
        if want_ap is not None and cs.aperture != want_ap:
            ap_val = cc.aperture_group[want_ap] if want_ap < len(cc.aperture_group) else want_ap
            hints.append("Set aperture to {} for the right depth of field.".format(ap_val))

        # 4) Zoom
        zoom_range = optimal.get("zoom_range", [])
        zoom_opt = optimal.get("zoom_optimal")
        if zoom_range and len(zoom_range) == 2:
            if not (zoom_range[0] <= cs.theme_zoom <= zoom_range[1]):
                if zoom_opt is not None:
                    if cs.theme_zoom < zoom_opt:
                        hints.append("Zoom in closer — aim near {:.1f}x.".format(zoom_opt))
                    else:
                        hints.append("Zoom out a bit — aim near {:.1f}x.".format(zoom_opt))
                else:
                    hints.append("Adjust zoom into the recommended range.")

        # 5) Framing
        comp = optimal.get("composition", {})
        x_range = comp.get("theme_x_range")
        y_range = comp.get("theme_y_range")
        x_opt = comp.get("theme_x_optimal")
        y_opt = comp.get("theme_y_optimal")
        if x_range and y_range:
            x_ok = x_range[0] <= cs.theme_x <= x_range[1]
            y_ok = y_range[0] <= cs.theme_y <= y_range[1]
            if not x_ok or not y_ok:
                dirs = []
                if x_opt is not None:
                    if cs.theme_x > x_opt + 0.03:
                        dirs.append("left")
                    elif cs.theme_x < x_opt - 0.03:
                        dirs.append("right")
                if y_opt is not None:
                    if cs.theme_y > y_opt + 0.03:
                        dirs.append("up")
                    elif cs.theme_y < y_opt - 0.03:
                        dirs.append("down")
                if dirs:
                    hints.append("Move the frame {} to center the evidence.".format(" and ".join(dirs)))
                else:
                    hints.append("Re-center the subject in the frame.")

        if not hints:
            tip = loc_cfg.get("tips", "")
            if tip:
                return "Looking good! " + tip
            return "Settings look solid — take the photo when ready."

        # Progressive: reveal one more hint each press
        level = int(getattr(store, "camera_hint_level", 0) or 0)
        shown = hints[: min(level + 1, len(hints))]
        store.camera_hint_level = min(level + 1, len(hints))
        return " | ".join(shown)

    def camera_show_hint():
        text = camera_get_progressive_hint()
        store.camera_hint_text = text
        renpy.show_screen("camera_hint_overlay", hint_text=text)
        renpy.restart_interaction()

    def camera_hide_hint():
        renpy.hide_screen("camera_hint_overlay")
        renpy.restart_interaction()


# Global defaults
default camera_config = None
default camera_state = None
default last_photo_score = None
default current_photo_location = ""
default photos_taken_locations = []
default camera_hint_text = ""
