### Forensics Pursuits: Car in the Snow Break-in

😺🚨 Play the evidence collection stage here: https://itsja.net/fpintrolevel3-1.0-web/index.html

🔎🧪 Play the lab analysis stage here: https://itsja.net/ForensicsLabL1Prototype-1.0-web/index.html

📝⚖️ Play the courtroom stage here: https://itsja.net/ForensicsTestimonySceneTutorial-1.0-web/index.html


Lab scene flowchart: https://coggle.it/diagram/ZomJ-5zP2LgRqOFn/t/enter-the-lab/e09c9b956420601cf5acc6f5799f4f5775e43a0c7da87a118abc0b1d157951b8

---
### Timer instructions:
There are three things in the folder that you need to add:
1. **timer.rpy**  - no modifications need to be made to this file.
2. **script_addon.rpy** - siphon the code from this file into your actual script.rpy after the code block you want to use it with. I included TODOs for everything you need to modify to get it to work.
3. **timer_pictures** - a file folder with images for the UI.
---

### Stage 1: Evidence Collection (Description)
Pieces of evidence and their collection methods:
- Toolmarks on the garage - took a photo of the evidence
- Footprint in the snow - lifted using plaster
- Fingerprint on the doorhandle - lifted using powder + tape
- Broken shards on the car seat - collected with tweezers, wrapped in paper bundle

Places the player can mess up:
- The order you visit the evidence in is important. Start from the outside of the car and work your way in, or you'll mess up the footprint evidence outside.
- The player can use the wrong coloured powder; if they use black powder on the black card they won't be able to see properly and the print will be cut off.
- The player can get the order in which they're supposed to use the tools wrong.

---

### Stage 2: Lab Analysis (Description)
Pieces of evidence and their analysis methods:
- Crowbar (corresponding to the toolmarks found in Stage 1) - collect the fingerprint using CA fuming, then develop the print in the correct lighting, and match it with the AFIS database
- Paint chip (from the car of the suspect) - perform analysis using a scalpel and a stereoscopic microscope, then match the results to a fingerprint database

Places the player can mess up:
- They can choose the incorrect time needed to develop the fingerprint using the timer feature.
- They can misidentify the layers for the paint chip.
- The scalpel can be misaligned with the blade.
- They can choose the wrong technique to use for each piece of evidence in multiple different areas.
- The player can choose the incorrect car type from the database.

---

### Stage 3: Courtroom (Description)
The first set of questions are related to techniques used in the evidence collection level and the lab analysis level, and the second set are more "psychological" questions about the behaviour of the forensic scientist.

---

TODO:
- Toolmark evidence colllection with plaster instead of just a picture
- Make it take a picture for each scene of the crime
- Clean up/redesign the report collection at the end
