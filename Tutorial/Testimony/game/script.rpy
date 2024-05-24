default total_score = 0
default show_evidence = False

init python:
    def answer_correct():
        global total_score
        total_score += 1
    
    def answer_incorrect():
        global total_score
        total_score -= 1
        if total_score <= 0:
            total_score=0



label start:
    scene enter_courtroom_screen
    with Dissolve(1.5)

label enter_courtroom:
    scene courtroom_bg
    with Dissolve(0.8)
    "Welcome to the courtroom."
    "In this scene, you will give a testimony with regards to the evidence you've analyzed, as well as help your counsels to find holes in the opposing testimony."
    show screen arrow_screen
    show screen evidence_button_screen
    "Remember, you can click on the evidence button to remind you of your analysis reusult."
    hide screen arrow_screen
    "First, you will give a testimony in response to the questions posed.\nPlease select the most appropriate answer."
    hide screen arrow_screen
    scene courtroom_bg


menu methods:
    "What method did you use to develop fingerprints on the firearm and why?"
    

    "Cyanoacrylate fuming, abbreviated as CA fuming.\nIt is ideal for non-porous surfaces, such as a firearm, as polymers can form on the fingerprint residues.":
        $ answer_correct()
    
    "Cyanoacrylate fuming (super glue fuming).\nIt facilitates the development of fingerprints by creating a magnetic field that attracts fingerprint residues, making it well-suited for firearms.":
        $ answer_incorrect()
    
    "Ninhydrin powder.\nWhen applied to non-porous surfaces like a firearm, this powder adheres to amino acid residues from the fingerprint and can be visualized under ambient light.":
        $ answer_incorrect()
    
    "Fluorescent powder.\nThis powder, when applied to a firearm, allows latent fingerprints to be visualized under appropriate lighting conditions.":
        $ answer_incorrect()


menu findings:
    "What were your findings based on the evidence collected?"

    "The fingerprints on the firearm were different from those collected on the stove top.":
        $ answer_incorrect()
    
    "The fingerprints on the firearm matched those on the stove top.":
        $ answer_correct()
    
    "Inclusive analysis.":
        $ answer_incorrect()

menu percentage:
    "What level of certainty do you have regrading the match of the fingerprints?"

    "100\%":
        $ answer_incorrect()
    
    "80\%":
        $ answer_correct()
    
    "50\%":
        $ answer_incorrect()

menu evidence:
    "What conclusions can be drawn from the forensic evidence?"

    "The evidence strongly suggests a single perpetrator.":
        $ answer_correct()
    
    "There may be more than one person involved in the arsenal.":
        $ answer_incorrect()
    
    "Inconclusive analysis, more procedure is needed.":
        $ answer_incorrect()


label next:
    "Now, you are going to find flaws in the opposing testimony."


label end:
    call screen score_screen


return
