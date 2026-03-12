## Camera Module - Configuration & State
## Reusable camera system for forensic photography games
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

            # UI configuration
            self.font = "DejaVuSans.ttf"
            self.scoring_config_path = "camera_scoring_config.json"

        def register_location(self, location_id, name):
            self.locations[location_id] = {"name": name}


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

    def camera_open_viewfinder():
        """Open the camera viewfinder overlay. Called from toolbox."""
        cs = store.camera_state
        cc = store.camera_config
        loc = store.current_photo_location

        if not loc or loc not in cc.locations:
            renpy.notify("Please click on an injury first, then use the camera.")
            return

        cs.active = True
        renpy.show_screen("camera_preview_ui")
        renpy.restart_interaction()

    def camera_take_photo():
        """Take photo, calculate score, show score overlay."""
        cs = store.camera_state
        cc = store.camera_config
        loc = store.current_photo_location

        # Save the photo
        cs.save_photo(loc)

        # Record location as photographed
        if loc and loc not in store.photos_taken_locations:
            store.photos_taken_locations.append(loc)

        # Calculate score
        score_data = calculate_photo_score(cs.photo_data[-1])
        store.last_photo_score = score_data

        # Hide viewfinder, show score
        cs.active = False
        renpy.hide_screen("camera_preview_ui")
        renpy.show_screen("photo_score_display", score_data=score_data)
        renpy.restart_interaction()

    def camera_close_score():
        """Close score overlay. Player is back to the original scene."""
        renpy.hide_screen("photo_score_display")
        renpy.restart_interaction()

    def camera_retake():
        """Close score overlay and reopen viewfinder."""
        renpy.hide_screen("photo_score_display")
        store.camera_state.active = True
        renpy.show_screen("camera_preview_ui")
        renpy.restart_interaction()

    def camera_close_viewfinder():
        """Close viewfinder without taking a photo."""
        store.camera_state.active = False
        renpy.hide_screen("camera_preview_ui")
        renpy.restart_interaction()

    def camera_open_album():
        """Open photo album as modal overlay."""
        renpy.show_screen("photo_album")
        renpy.restart_interaction()

    def camera_close_album():
        """Close photo album overlay."""
        renpy.hide_screen("photo_album")
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


# Global defaults
default camera_config = None
default camera_state = None
default last_photo_score = None
default current_photo_location = ""
default photos_taken_locations = []
