init python:
    import json
    from typing import List

    class Evidence:
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
        evidence: List[Evidence]

        def __init__(self, name: str, case_points: List[str], evidence: List[Evidence]) -> None:
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
    

    def get_specialty(specialty_name: str) -> Specialty:
        global specialties_list
        for specialty in specialties_list:
            if specialty_name.lower() == specialty.name.lower():
                return specialty
        print(f"Specialty '{specialty_name}' not found.")


    def get_evidence(evidence_name: str) -> Evidence:
        global evidence_list
        for evidence in evidence_list:
            if evidence_name.lower() == evidence.name.lower():
                return evidence
        print(f"Evidence '{evidence_name}' not found.")

    
    def get_evidence_by_image(image_name: str) -> Evidence:
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

        # TODO: Replace the description below with your case details. Do not change the name of the evidence
        # as the AI fetches the details from here when writing the report card.
        evidences.add_to_inventory(
            Item(
                name="Casefile",
                image_name="casefile",
                description="On the night of June 15th, 2026, a motorcyclist was struck from behind during a hit-and-run collision on Highway 407. The motorcyclist sustained critical injuries, and the driver of the vehicle fled the scene before emergency services arrived. At the scene, investigators collected paint chip evidence and a tire tread impression believed to be associated with the fleeing vehicle. Surveillance footage later identified several vehicles of interest, and known paint and tire samples were collected from each vehicle for comparison. Following microscopic and chemical paint analysis, along with tire tread comparison, the suspect vehicle was narrowed down to a silver 2006 Dodge Durango SLT."
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
    file_path = renpy.loader.transfn("courtroom.json")
    with open(file_path, "r") as f:
        courtroom_data = json.load(f)

    specialties_list = []
    evidence_list = []

    for specialty_data in courtroom_data:
        specialty_name = specialty_data["specialty"]
        specialty_case_points = specialty_data.get("case_points", [])
        specialty_evidence = []

        for evidence_data in specialty_data["evidence"]:
            evidence = Evidence(
                name = evidence_data["name"],
                description = evidence_data["description"],
                image = evidence_data["image"],
                truth_base = evidence_data.get("truth_base", [])
            )
        
            specialty_evidence.append(evidence)
            evidence_list.append(evidence)
        
        specialty = Specialty(
            name = specialty_name,
            case_points = specialty_case_points, 
            evidence = specialty_evidence
        )

        specialties_list.append(specialty)

    

