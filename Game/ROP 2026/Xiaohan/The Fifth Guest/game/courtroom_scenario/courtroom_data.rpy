init -9 python:
    import json

    # ---- Case names -------------------------------------------------------
    # Single source of truth. courtroom.json and the courtroom dialogue use
    # {victim} / {suspect} placeholders that are filled in from these, and
    # lab_scenario/script.rpy's victim_name / suspect_name point here too.
    CASE_VICTIM = "Nadia Vale"
    CASE_SUSPECT = "Rowan Mallory"
    CASE_DATE = "June 4, 2026"

    # ---- Gemini access -----------------------------------------------------
    # Both platforms call Gemini directly (see courtroom_ai.rpy) -- desktop
    # uses game/.env, web asks each player for their own free key, so there is
    # no shared server-side quota to run out.
    #
    # gemini-2.5-flash was retired for new API keys (Google now 404s it,
    # pointing callers at gemini-3.6-flash). Confirmed against this project's
    # own key with the full courtroom system prompt before switching.
    GEMINI_MODEL = "gemini-3.6-flash"

    def case_text(text):
        """Fill the case-name placeholders in authored courtroom text."""
        return text.replace("{victim}", CASE_VICTIM).replace("{suspect}", CASE_SUSPECT)
    from typing import List

    class CourtEvidence:
        name: str
        image: str
        description: str
        truth_base: List[str]

        def __init__(self, name: str, description: str, image: str, truth_base: List[str]) -> None:
            self.name = name
            self.image = image
            self.description = description
            self.truth_base = truth_base

        def display(self) -> None:
            print("Evidence:")
            print("  Name:", self.name)
            print("  Image:", self.image)
            print("  Description:", self.description)
            print("  Truth Base:")
            for item in self.truth_base:
                print("   -", item)

    class Specialty:
        name: str
        case_points: List[str]
        evidence: List[CourtEvidence]

        def __init__(self, name: str, case_points: List[str], evidence: List[CourtEvidence]) -> None:
            self.name = name
            self.case_points = case_points
            self.evidence = evidence
    
        def display(self) -> None:
            print("Specialty:", self.name)
            print("Case Points:")
            for point in self.case_points:
                print(" -", point)
            print("Evidence List:")
            for ev in self.evidence:
                ev.display()
                print("")
    

    # The courtroom keeps its case files in a third Inventory, separate from the
    # crime scene's toolbox and evidence inventories.
    evidences = Inventory()


    def get_specialty(specialty_name: str) -> Specialty:
        global specialties_list
        for specialty in specialties_list:
            if specialty_name.lower() == specialty.name.lower():
                return specialty
        print(f"Specialty '{specialty_name}' not found.")


    def get_evidence(evidence_name: str) -> CourtEvidence:
        global evidence_list
        for evidence in evidence_list:
            if evidence_name.lower() == evidence.name.lower():
                return evidence
        print(f"Evidence '{evidence_name}' not found.")

    
    def get_evidence_by_image(image_name: str) -> CourtEvidence:
        global evidence_list
        for evidence in evidence_list:
            if evidence.image.lower() == image_name.lower():
                return evidence
        print(f"Evidence with image '{image_name}' not found.")


    def create_all_truths_set(specialty_name):
        """Create a set of all truth bases for a given specialty"""
        specialty = get_specialty(specialty_name)
        all_truths = set()
        
        for evidence in specialty.evidence:
            for truth in evidence.truth_base:
                all_truths.add(truth.lower())
        
        return all_truths

    
    def enable_evidence(specialty: Specialty) -> None:
        global evidences

        evidences.reset_inventory()

        # Keep the item name "Casefile" -- the AI looks it up by name when writing
        # the report card at the end of the trial.
        evidences.add_to_inventory(
            Item(
                name="Casefile",
                image_name="casefile",
                description=case_text(
                    "On the night of {date}, at approximately 11:55 p.m., {victim} was found "
                    "dead inside the study of their residence at 41 Columbia Street, Delhi, "
                    "Ontario. Earlier that evening, the victim had been hosting a small "
                    "gathering with four guests present at the residence. The victim was "
                    "discovered with a fatal head injury consistent with blunt force trauma.\n\n"
                    "Investigators identified several individuals who had been present at the "
                    "gathering and began examining physical evidence recovered from the scene, "
                    "including biological samples and a latent fingerprint, to determine who "
                    "may have been involved in the victim's death."
                ).replace("{date}", CASE_DATE)
            )
        )

        for ev in specialty.evidence:
            description = "No description set." if ev.description == None or ev.description == "" else ev.description
            item = Item(
                name=ev.name,
                image_name=ev.image,
                description=description
            )
            evidences.add_to_inventory(item)


    # Load courtroom data from JSON
    file_path = renpy.loader.transfn("jsons/courtroom.json")
    with open(file_path, "r") as f:
        courtroom_data = json.load(f)

    specialties_list = []
    evidence_list = []

    for specialty_data in courtroom_data:
        specialty_name = specialty_data["specialty"]
        specialty_case_points = specialty_data.get("case_points", [])
        specialty_evidence = []

        for evidence_data in specialty_data["evidence"]:
            # NB: this loop runs at the store level, so its variables must not
            # shadow host globals -- `evidence` is the crime scene's Inventory.
            court_ev = CourtEvidence(
                name = case_text(evidence_data["name"]),
                description = case_text(evidence_data["description"]),
                image = evidence_data["image"],
                truth_base = [case_text(t) for t in evidence_data.get("truth_base", [])]
            )

            specialty_evidence.append(court_ev)
            evidence_list.append(court_ev)

        court_sp = Specialty(
            name = specialty_name,
            case_points = specialty_case_points,
            evidence = specialty_evidence
        )

        specialties_list.append(court_sp)

    

