# Vivian F. Level 1: Office Incident

This folder contains code to the partnered scene for level 1 (with Kathryn).

## Scenario
The scenario is an incident (murder) in the Bahen Centre. Criminal had entered Bahen midnight and broke through the library front door in reach for the donor cheques kept in the office space. The inexperienced criminal was carrying a gun and was suddenly met with the building security. Security was soon after shot and killed by the panicking criminal. The perpetrator left the scene within a couple minutes and tried his best to clean up, but he was in a hurry. Player's job is to analyze the scene, collect evidence, process evidence, generate results, and give testimony to help finding the murderer.

## Evidence Processing Concepts tests:
  * 2D Footprint Cast Development (Knaap Process - waxy footprint on desk)
  * 2D Paper Fingerprint Development (Ninhydrin - cheque)
  * Blood Reagent Test (Hungarian Red Dye - lantent blood stain, cleaned)
    * with bloody footprint
    * Note: fails
  * Bullet cartridge fingerprint (Gun Blue)

## RenPy Code - General
### Miscellaneous: 
“gui.rpy” and “screens.rpy” code is default from RenPy. And “options.rpy” code was only modified to add definitions for the various mouse icons. 
### Main: 
“script.rpy” contains code to the main flow logic of the scenes and materials, which calls upon screens in “custom_screens.rpy” for screen displays and interactions. “styles.rpy” contains code for styling custom buttons and frames. "inventory.rpy" contains all code to toolbox and evidence box bar (cut version of Vivian S' inventory).

## Flowchart (planned ver)
https://www.canva.com/design/DAGG0kkiwEM/9pRe7AJhNyqtqoo-AAvbkw/edit?utm_content=DAGG0kkiwEM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton 

## Stage 1: Evidence Collection
### Currently Implmented:
  * All evidences in place
  * Evidence marker required before detail scene interaction
    * markers numbered based on user-clicked order
    * numbers shows up correspondingly in detail scene and in camera photo
  * Evidence interactions: 
    * prompt (if applicable)
    * development step by step
    * mistake points (if applicable: under/over spray/mix/cure, wrong tools choice)
    * tagging
    * photo taking (flash)
    * bagging
    * result in photo stored in both camera and evidence bin
    * returning to zoom-in shots after collection displays evidence piece gone
  * Toolbox (contains only tools relevant to this scenario)
  * Evidence bin (shows each evidence object itself)
  * Camera (shows photos of evidences taken with scale, tag, and/or evidence marker, in gallery-style)
  * Custom cursors (magnifying glass for analyzing, gloves for picking tools, and mouse for each tool)
### To improve:
  * Add dialogue style guidance on what and when to place tools
  * Implement step-by-step rollback with back button within processing in action
  * Give captions to evidences collected when click back to them
  * Timers for wait times

## Stage 2: Lab
### Added Code Files
Screens for evidence case files are moved to "util_screen.rpy". Code related to timer in "timer.rpy" are linked from step in "custom_screen" to label in "script". 
### Currently Implmented:
  * All physical evidences are (already processed on site) or (to be processed in fumehood)
    * Cheque to be processed using Ninhydrin
    * Bullet cartridge to be processed using Gun Blue
    * associated mistake points with above
    * dialogue guides
    * hover image hints to steps
  * All digital evidences either (has print to process) or (incmoplete print cannot process)
    * Cheque and KNAAP footprint can be uploaded to afis and render results
  * All steps supports step-by-step rollback through back button
### To improve:
  * Show afis results somewhere when clicking on digital evidence (report?)
  * Obtain a set of prints to compare prints to in afis
  * More ratio options for Gun Blue mixing? (75:25)

## Stage 3: Courtroom
### Currently Implmented:
 * Name asked and proper swearing procedure proceeded before other questions
 * All questions and answers obtained from Kathryn
 * Focused on leading player to common answer mistakes
 * Included many trick answers of slight difference but important procedural knowledge
 * Score and result viewing at end to show for each question player's answer and its correctness
### To improve:
 * At results viewing, give facts on why wrong answers selected are wrong and why correct are correct


## Possible Improvements for All Levels
  * Align with proper procedural steps (gloves, markers, ...)
  * Follow professional photo protocols (need scale, tag, markers in photo)
  * Unify textbutton sizing/padding
  * Obtain description of tools to display as info when inspected from bar
  * Error reports at end of evidence collection and lab scene
  * Inventory icons size up (playtest feedback too small)
  * Inventory info/hand icons change hover to yellow highlight (feedback unnoticeable)
  * Show tool name when hover over bar items underneath their image (feedback want name)
  * Mouse images add corner highlight so easier to identify when mouse is clicking





