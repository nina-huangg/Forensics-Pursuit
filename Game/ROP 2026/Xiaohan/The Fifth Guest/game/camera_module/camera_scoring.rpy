## Camera Module - Scoring Engine
## Evaluates photo quality across 4 dimensions

init python:
    import json
    import math

    scoring_config = None

    def generate_current_settings_json():
        """Dev tool: export current camera settings to a file for config authoring."""
        import os
        cs = store.camera_state
        cc = store.camera_config
        cur_loc = store.current_photo_location

        settings = {
            "lens": cs.focal_len,
            "aperture_index": cs.aperture,
            "aperture_value": cc.aperture_group[cs.aperture],
            "iso_index": cs.iso_index,
            "iso_value": cc.iso_group[cs.iso_index],
            "zoom_range": [round(cs.theme_zoom - 0.3, 1), round(cs.theme_zoom + 0.3, 1)],
            "zoom_optimal": round(cs.theme_zoom, 1),
            "composition": {
                "theme_x_range": [round(cs.theme_x - 0.05, 2), round(cs.theme_x + 0.05, 2)],
                "theme_y_range": [round(cs.theme_y - 0.05, 2), round(cs.theme_y + 0.05, 2)],
                "theme_x_optimal": round(cs.theme_x, 2),
                "theme_y_optimal": round(cs.theme_y, 2)
            }
        }

        json_str = json.dumps(settings, indent=2)
        file_content = "// Current Location: {}\n// Copy the \"optimal_settings\" block below into scoring config\n\n\"optimal_settings\": {}\n".format(cur_loc, json_str)

        try:
            file_path = os.path.join(config.gamedir, "camera_config_export.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            renpy.notify("Config saved to: game/camera_config_export.txt")
            return True
        except Exception as e:
            renpy.notify("Error saving config: {}".format(str(e)))
            return False

    def reset_scoring_config_cache():
        """Clear cached scoring config so New Game reloads from disk."""
        global scoring_config
        scoring_config = None

    def _error_score_result(message, location_name="Unknown"):
        """Safe score payload so photo_score_display never KeyErrors."""
        return {
            "total": 0,
            "grade": "F",
            "overall_feedback": message,
            "composition": {"score": 0, "max": 0, "feedback": message},
            "exposure": {"score": 0, "max": 0, "feedback": ""},
            "sharpness": {"score": 0, "max": 0, "feedback": ""},
            "completeness": {"score": 0, "max": 0, "feedback": ""},
            "location_name": location_name,
            "tips": "",
            "error": message,
        }

    def load_scoring_config(force=False):
        """Load the photo scoring configuration from JSON file."""
        global scoring_config
        if scoring_config is None or force:
            try:
                cc = store.camera_config
                path_name = cc.scoring_config_path if cc else "camera_scoring_config.json"
                config_path = renpy.loader.transfn(path_name)
                with open(config_path, 'r', encoding='utf-8') as f:
                    scoring_config = json.load(f)
            except Exception as e:
                renpy.notify("Error loading scoring config: {}".format(str(e)))
                scoring_config = {}
        return scoring_config

    def calculate_composition_score(photo, location_config):
        """Calculate composition score based on subject positioning and zoom."""
        cc = store.camera_config
        optimal = location_config["optimal_settings"]
        weights = location_config["scoring_weights"]
        max_score = weights["composition"]

        comp_config = optimal["composition"]
        tolerance = scoring_config["tolerance_ranges"]["composition"]

        score = 0
        feedback_parts = []

        x_diff = photo["theme_x"] - comp_config["theme_x_optimal"]
        x_in_range = comp_config["theme_x_range"][0] <= photo["theme_x"] <= comp_config["theme_x_range"][1]
        y_diff = photo["theme_y"] - comp_config["theme_y_optimal"]
        y_in_range = comp_config["theme_y_range"][0] <= photo["theme_y"] <= comp_config["theme_y_range"][1]

        positioning_score = max_score * 0.5
        if abs(x_diff) <= tolerance["theme_x_tolerance"] * 0.5 and abs(y_diff) <= tolerance["theme_y_tolerance"] * 0.5:
            score += positioning_score
            feedback_parts.append("Subject is perfectly centered - excellent framing for forensic documentation.")
        elif x_in_range and y_in_range:
            score += positioning_score * 0.7
            direction_hints = []
            if x_diff > 0.05:
                direction_hints.append("left")
            elif x_diff < -0.05:
                direction_hints.append("right")
            if y_diff > 0.05:
                direction_hints.append("up")
            elif y_diff < -0.05:
                direction_hints.append("down")
            if direction_hints:
                feedback_parts.append("Subject positioning is acceptable, but could be improved. Try moving the frame {} to center the evidence better.".format(" and ".join(direction_hints)))
            else:
                feedback_parts.append("Good positioning - subject is well-framed.")
        else:
            score += positioning_score * 0.4
            direction_hints = []
            if x_diff > 0.1:
                direction_hints.append("significantly left")
            elif x_diff < -0.1:
                direction_hints.append("significantly right")
            if y_diff > 0.1:
                direction_hints.append("upward")
            elif y_diff < -0.1:
                direction_hints.append("downward")
            feedback_parts.append("Subject is off-center. Move your frame {} to properly center the evidence in the shot.".format(" and ".join(direction_hints) if direction_hints else "to center"))

        zoom_score = max_score * 0.5
        zoom_optimal = optimal["zoom_optimal"]
        zoom_range = optimal["zoom_range"]
        zoom_diff = photo["zoom_level"] - zoom_optimal
        zoom_diff_percent = abs(zoom_diff) / zoom_optimal * 100

        if zoom_diff_percent <= tolerance["zoom_tolerance_percent"] * 0.5:
            score += zoom_score
            feedback_parts.append("Zoom level is optimal - evidence fills the frame appropriately.")
        elif zoom_range[0] <= photo["zoom_level"] <= zoom_range[1]:
            score += zoom_score * 0.7
            if zoom_diff > 0:
                feedback_parts.append("Zoom is slightly too close. Zoom out a bit to include more context around the evidence.")
            else:
                feedback_parts.append("Zoom is slightly too far. Zoom in closer to capture more detail of the evidence.")
        else:
            score += zoom_score * 0.3
            if zoom_diff > 0:
                feedback_parts.append("You're zoomed in too close - important context is cut off. Zoom out significantly to capture the full evidence.")
            else:
                feedback_parts.append("You're zoomed out too far - critical details are too small. Zoom in much closer to properly document the evidence.")

        return round(score, 1), " ".join(feedback_parts)

    def calculate_exposure_score(photo, location_config):
        """Calculate exposure score based on ISO and aperture settings."""
        cc = store.camera_config
        optimal = location_config["optimal_settings"]
        weights = location_config["scoring_weights"]
        max_score = weights["exposure"]

        score = 0
        feedback_parts = []

        iso_score = max_score * 0.5
        iso_diff = photo["iso_index"] - optimal["iso_index"]
        current_iso = cc.iso_group[photo["iso_index"]]
        optimal_iso = cc.iso_group[optimal["iso_index"]]

        if iso_diff == 0:
            score += iso_score
            feedback_parts.append("ISO is perfect at {}.".format(current_iso))
        elif iso_diff > 0:
            score += iso_score * (0.7 if abs(iso_diff) == 1 else 0.3)
            feedback_parts.append("ISO {} is too high - this adds unnecessary noise to your image. Try lowering it to {} for cleaner results.".format(current_iso, optimal_iso))
        else:
            score += iso_score * (0.7 if abs(iso_diff) == 1 else 0.3)
            feedback_parts.append("ISO {} is too low - your image may be underexposed. Increase it to {} for better exposure.".format(current_iso, optimal_iso))

        aperture_score = max_score * 0.5
        aperture_diff = photo["aperture_index"] - optimal["aperture_index"]
        current_aperture = cc.aperture_group[photo["aperture_index"]]
        optimal_aperture = cc.aperture_group[optimal["aperture_index"]]

        if aperture_diff == 0:
            score += aperture_score
            feedback_parts.append("Aperture {} provides excellent depth of field for this evidence.".format(current_aperture))
        elif aperture_diff > 0:
            score += aperture_score * (0.7 if abs(aperture_diff) == 1 else 0.3)
            feedback_parts.append("Aperture {} is too narrow - this limits light and may cause diffraction. Open it up to {} for sharper images.".format(current_aperture, optimal_aperture))
        else:
            score += aperture_score * (0.7 if abs(aperture_diff) == 1 else 0.3)
            feedback_parts.append("Aperture {} is too wide - your depth of field is too shallow. Stop down to {} to keep the entire evidence in focus.".format(current_aperture, optimal_aperture))

        return round(score, 1), " ".join(feedback_parts)

    def calculate_sharpness_score(photo, location_config):
        """Calculate sharpness score based on lens choice and zoom."""
        cc = store.camera_config
        optimal = location_config["optimal_settings"]
        weights = location_config["scoring_weights"]
        max_score = weights["sharpness"]

        score = 0
        feedback_parts = []

        lens_score = max_score * 0.5
        if photo["lens"] == optimal["lens"]:
            score += lens_score
            feedback_parts.append("Lens choice ({}) is correct for this distance and subject matter.".format(photo["lens"]))
        else:
            score += lens_score * 0.3
            feedback_parts.append("You're using the {} lens, but the {} lens would be more appropriate for this evidence.".format(photo["lens"], optimal["lens"]))

        focus_score = max_score * 0.5
        zoom_optimal = optimal["zoom_optimal"]
        tolerance = scoring_config["tolerance_ranges"]["sharpness"]
        zoom_diff_percent = abs(photo["zoom_level"] - zoom_optimal) / zoom_optimal * 100

        if zoom_diff_percent <= tolerance["zoom_perfect_range_percent"]:
            score += focus_score
            feedback_parts.append("Focus is sharp and clear throughout the evidence - excellent technical execution.")
        elif zoom_diff_percent <= tolerance["zoom_acceptable_range_percent"]:
            score += focus_score * 0.7
            feedback_parts.append("Focus is acceptable but could be sharper. Fine-tune your zoom level to achieve critical sharpness.")
        else:
            score += focus_score * 0.4
            feedback_parts.append("Image appears soft or out of focus. Adjust your zoom and ensure your lens is properly focused on the evidence before shooting.")

        return round(score, 1), " ".join(feedback_parts)

    def calculate_completeness_score(photo, location_config):
        """Calculate completeness score based on required elements."""
        cc = store.camera_config
        weights = location_config["scoring_weights"]
        max_score = weights["completeness"]

        # If host game provides a custom completeness scorer, use it
        if cc.custom_completeness_scorer is not None:
            return cc.custom_completeness_scorer(photo, location_config)

        # Default: full score (no special requirements in morgue context)
        score = max_score
        feedback = "All required documentation elements are present."

        if location_config.get("critical", False) and score == max_score:
            bonus = scoring_config["scoring_system"]["completeness_scoring"]["bonus_critical_perfect"]
            score += bonus
            feedback = "EXCELLENT: This is critical evidence and you've documented it perfectly!"

        return round(score, 1), feedback

    def get_overall_feedback(total_score):
        """Get overall grade and feedback based on total score."""
        thresholds = scoring_config["scoring_system"]["grade_thresholds"]

        grade = "F"
        for g, threshold in thresholds.items():
            if total_score >= threshold:
                grade = g
                break

        if total_score >= 90:
            feedback = "Outstanding work! This photograph meets professional forensic documentation standards."
        elif total_score >= 80:
            feedback = "Very good! Your photograph is clear and well-documented. With minor improvements you'll achieve professional-level results."
        elif total_score >= 70:
            feedback = "Good effort. The photograph captures the essential information, but there's room for improvement."
        elif total_score >= 60:
            feedback = "This photo is adequate but has significant issues. Please review the feedback carefully."
        else:
            feedback = "This photograph does not meet forensic documentation standards. Please review each area of feedback below and retake this photo."

        return grade, feedback

    def calculate_photo_score(photo):
        """Main function to calculate comprehensive photo score."""
        load_scoring_config()

        if not scoring_config or "locations" not in scoring_config:
            return _error_score_result("Error: Scoring config not loaded")

        location = photo["location"]
        if location not in scoring_config["locations"]:
            return _error_score_result(
                "Error: Location '{}' not found in config".format(location),
                location_name=location,
            )

        location_config = scoring_config["locations"][location]

        comp_score, comp_feedback = calculate_composition_score(photo, location_config)
        exp_score, exp_feedback = calculate_exposure_score(photo, location_config)
        sharp_score, sharp_feedback = calculate_sharpness_score(photo, location_config)
        complete_score, complete_feedback = calculate_completeness_score(photo, location_config)

        total_score = comp_score + exp_score + sharp_score + complete_score
        total_score = min(100, max(0, total_score))

        grade, overall_feedback = get_overall_feedback(total_score)

        return {
            "total": round(total_score, 1),
            "grade": grade,
            "overall_feedback": overall_feedback,
            "composition": {
                "score": comp_score,
                "max": location_config["scoring_weights"]["composition"],
                "feedback": comp_feedback
            },
            "exposure": {
                "score": exp_score,
                "max": location_config["scoring_weights"]["exposure"],
                "feedback": exp_feedback
            },
            "sharpness": {
                "score": sharp_score,
                "max": location_config["scoring_weights"]["sharpness"],
                "feedback": sharp_feedback
            },
            "completeness": {
                "score": complete_score,
                "max": location_config["scoring_weights"]["completeness"],
                "feedback": complete_feedback
            },
            "location_name": location_config["name"],
            "tips": location_config.get("tips", "")
        }
