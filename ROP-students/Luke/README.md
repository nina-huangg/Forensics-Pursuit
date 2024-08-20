# Overview
A person is found dead in his living room. From police reports, the victim has taken a blow to the head, strong enough to cause bleeding. The player is tasked with collecting evidence at the crime scene, processing it in the labs and finally presenting their case and conclusions as testimony in the courtroom. 
### Flow charts
https://drive.google.com/file/d/1BMnW111uZiUWMuw_IWntZOoNyBglS18L/view?usp=sharing 
https://app.diagrams.net/#G1GTegTCqITtN6Ppul04Gd2r5cTUEg-JZv#%7B%22pageId%22%3A%225R1Ep1ZRfNg14T2-pnC7%22%7D
https://app.diagrams.net/#G1Yqex8UCL1sX58kxBmkI7Bt3PB0pXX2yi#%7B%22pageId%22%3A%22x35-wouxuZ1qwb7TEoSw%22%7D 
https://www.figma.com/board/1WFBQCPg455ryA7anEl4n2/FigJam-basics 
# Game Play
## Crime Scene 1
### Evidence and forensic techniques
- Shoeprint collection using gelatin lifter. The player is tested on awareness of under/over dusting and remembers to remove air bubbles before lifting a gelatin sheet.
  - The player should see an oil stain on the floor as the shoeprint is currently hard to see. The first step is to any evidence is to place down evidence markers. 
  - The next step is to use granular dusting to refine the shoeprint. They should be careful to not over or under dust.
  - The shoeprint should be visible. Now the player should place a gelatin sheet and flatten it out.
  - Finally the player is to lift the shoeprint.
- Tangible objects that are suspected to be primary evidence are usually collected. The player should recognize the importance of preserving the crime scene while also understanding that some items may need to be tested in a lab for a more controlled analysis.
  - The player is prompted to simply collect an alcohol bottle and a vase.
- Identify blood using Alternative Light Sources (ALS), perform Kestle Meyer presumptive test and swab sample collection. The player should understand that while blood can be wiped/cleaned off smooth surfaces like a wall, traces like dna in blood still remain on the wall. These traces can be identified in a dark environment and ALS. Additionally they should be able to read the results of the Kestle Meyer test (pink sample means blood)
  - The player is to close curtains to simulate a dark environment.
  - Then the player is able to use ALS (uv light) to shine on the wall. They should notice a pattern on the wall that was not there before. 
  - Next, the player should place down evidence markers around the pattern spotted on the wall.
  - The player can now swab a sample from the wall and perform the Kestle Meyer test.
### Implementation
- The player can do shoeprint collection, blood identification and swabbing, and item collection in any order. After completing a stage, images and variables will be updated accordingly. For example, after collecting items on the living room table, all images including the living room scene and the main room scene has been updated to exclude the items. Furthermore, upon revisiting the table, there is a prompt notifying the player that all evidence on the table has already been collected. 
- There is a cool "flashlight effect" that effectively simulates using a flashlight by making the whole room much darker except for a "bright spot" that follows your cursor.
- The player can over dust or under dust the shoeprint with granular powder. If they under dust, they are prompted to dust further. If they over dust, they have to restart.
- Added "idle" and "hover" to all objects that can be clicked on. Sometimes it is not obvious where to put your mouse. To stay consistent with everything else, I redid all the images that required mouse interactions so that even in its idle state, there would be a grey outline prompting the player to hover over a certain area and upon hovering, the outline turns orange, and upon clicking, the image updates. This means where there were once 2 images, now there are 4 (idle and hover states are additional).
### Bugs, Fixes, Improvement
- I don't think there are any bugs. Due to the lack of time, I did not test thoroughly.
- This is a general problem that applies to all my levels, so this point will be repeated.
  - The majority of player interactions in the game are limited to short clicks. I attempted to add drag-and-drop and "long press" mechanics, but due to the difficulty of implementation, they were rarely used. I believe the game experience could be significantly enhanced with more interactive options beyond just clicking. Vivian S has introduced a "drawing" feature, and while I'm unsure how this can be applied to my forensic techniques, I would have liked to explore a "click+hold" interaction, not necessarily involving drawing, if more time were available.
- If I go through the scenes carefully, there may be moments where I could've added some animations. Again this is building off the point above, where the game feels like the "same interactions" repeated over and over again. Click something and the image updates. So adding animations might've smoothed things out more. However, I did not know how to do animations at the time the crime scene was designed. Given more time, I would like to see this feature added.
- Add Vivian S inventory system. I did do a demo in one of the meetings where I had Vivian's inventory system integrated for a portion of my crime scene. However, I notice there are a lot of bugs with the inventory behaviour, for example, the "tool" once selected sometimes doesn't go back into the inventory, or appears to be overlapping with another tool. I also did not know how to detect if the player had the wrong tool selected. This was problematic because for example if the player selects the tools in a non-intended way ie. selecting the gelatin lifter before the evidence markers or dusting powder may cause unintentional "jumps" forward. To prevent this, I tried to make my own inventory system as versatile as possible instead.
  
## Lab Scene 1
### Lab Techniques and Procedure
- The alcohol bottle contains liquid substances. Since the material is glass, the player should also feel inclined to do fingerprint dusting.
  - Granular fingerprint dusting is done at the lab bench. The procedure is standard and white dusting powder is used instead of black. 
  - The substance in the bottle must be extracted with a pipette and put into a mason jar before putting it in a Gas Chromatography Headspace Instrument. Upon running the instrument, the results show the substance is Diphenhydramine. note: Diphenhydramine is a substance that can mix into alcohol and its taste is hard to detect, however it is lethal to human health.
- The vase has blood that should be swabbed and fingerprints to be developed in the Cyanosafe and wet labs.
  - A presumptive test should be done first, but since it is the exact same procedure done in the crime scene, the player can take for granted that the substance on the vase is indeed blood. The player is prompted to swab the vase before doing any other forensic development techniques in the lab.
  - The vase should be put in a Cyanosafe chamber for about 10 minutes and then taken to a wet lab for further fingerprint examination. The fingerprint is then photographed and saved.
- There was a swab from the wall at the crime scene and an additional swab from the vase. Both swabs are to be dropped off in the Bio Lab and after waiting for a while, the player will get two DNA profiling samples corresponding to each of the swabs.
- There should be two fingerprints and two DNA profiles developed at the end of all the materials lab. These can be compared in the data analysis lab.
### Implementation
- All forensic evidence development techniques and procedures can be done in any order unless there are specified orders such as the vase must be swabbed before any other forensic development technique to preserve the DNA in the blood.
- The inventory is updated as the player proceeds further in the game. For example, if they developed the alcohol bottle fingerprint and proceeded to do the vase swabbing, but they have not done substance extraction from the bottle nor wet lab fingerprint development for the vase, then the player will still have the alcohol bottle and a "processed vase" with the blood removed from the icon. Furthermore, if the player now decides to do the substance extraction and put it through the Gas Chromatography Headspace Instrument, then there are no more forensic developments left for the alcohol bottle, and thus it is removed from the inventory.
- To avoid the repetitive theme of click to change image, I tried to add animations wherever it felt right to have one. For example, there is animations for timers for Cyanosafe and Gas Chromatography Headspace.
- Fixed the vase to be vertical when put into the Cyanosafe chamber
- Changed all the UI boxes to be consistent. I had checkmarks, back buttons, textboxes and textboxes that had a button that said "Okay". Now I have reduced it to just back buttons and all textboxes have a button that says "Okay". Note: the "Okay" is for the player to click to make the textbox go away. Otherwise, the textbox stays on the screen.
- Added "idle" and "hover" to all objects that can be clicked on. Sometimes it is not obvious where to put your mouse. To stay consistent with everything else, I redid all the images that required mouse interactions so that even in its idle state, there would be a grey outline prompting the player to hover over a certain area and upon hovering, the outline turns orange, and upon clicking, the image updates. This means where there were once 2 images, now there are 4 (idle and hover states are additional).
- There is previous and next buttons in the data analysis lab to cycle through all the different DNA and fingerprints. I think this part was really nicely done to simulate how DNA and fingerprints are processed in a data lab. 
### Bugs, Fixes, Improvement
- I don't think there should be any bugs.
- Add Vivian S inventory system
- 
## Testimony Scene 1
### Lab Techniques and Procedure
The player is to answer questions regarding both the forensic techniques and procedures done in the crime scene and lab scene. Every question has the equal weighting, and the score is simply the total sum of all questions answered correctly.




