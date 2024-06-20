# Vivian F. Level 1: Office Murder

This folder contains code to the partnered scene for level 1 (with Kathryn).

## Scenario
The scenario is murder in the Bahen Centre. Criminal had entered Bahen midnight and broke through the library front door in reach for the donor cheques kept in the office space. The inexperienced criminal was carrying a gun and was suddenly met with the building security. Security was soon after shot and killed by the panicking criminal. The perpetrator left the scene within a couple minutes and tried his best to clean up, but he was in a hurry. Player's job now is to analyze the scene and collect evidence to find him.
### Concepts tests:
  * 2D Footprint Cast Development (Knaap Process - waxy footprint on desk)
  * 2D Paper Dingerprint Development (Ninhydrin - cheque)
  * Blood Reagent Test (Hungarian Red Dye - lantent blood stain, cleaned)
    * with bloody footprint
  * Bullet cartridge fingerprint (Gun Blue)

## Flowchart (to be updated)
https://www.canva.com/design/DAGG0kkiwEM/9pRe7AJhNyqtqoo-AAvbkw/edit?utm_content=DAGG0kkiwEM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton 


## Images
Loose images are main scene background images, and each folder contains screen/layer specific images.  


## RenPy Code
### Miscellaneous: 
“gui.rpy” and “screens.rpy” code is default from RenPy. And “options.rpy” code was only modified to add definitions for the various mouse icons. 
### Main: 
“script.rpy” contains code to the main flow logic of the scenes and materials, which calls upon screens in “custom_screens.rpy” for screen displays and interactions. “styles.rpy” contains code from Nina used for stylingcustom buttons.


## Note: 
### Currently Implmented:
  * All evidences in place
  * Evidence marker required before detail scene interaction
  * Evidence interactions: 
    * prompt (if applicable)
    * development step by step
    * mistake points (if applicable: under/over spray/mix/cure, wrong tools choice)
    * tagging
    * photo taking (flash)
    * bagging
    * result in photo stored in both camera and evidence bin
    * returning to zoom-in shots after collection displays evidence piece gone
  * Toolbox (contains only tools relevant to scene)
  * Evidence bin (shows each evidence object itself)
  * Camera (shows photos of evidences taken with scale, tag, and/or evidence marker, in gallery-style)
  * Added more custom cursors (magnifying glass for analyzing, gloves for picking tools, and mouse for each tool)
### Features to be implemented:
  * New toolbox (bar)
  * Dental stone mixture tweaking (until pancake consistency)
  * Automate textbutton sizing and placement
  * Evidence/Photo descriptions when clicked


