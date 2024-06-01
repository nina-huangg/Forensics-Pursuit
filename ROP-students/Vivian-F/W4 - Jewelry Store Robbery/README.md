# Vivian F. (W4) Game: Jewlery Store Robbery

This folder contains code to the second level demo presented in Week 4.  All code contained in the “game” folder, in which all folders and its contents except “images” and RenPy codes out of folders were default RenPy data.

## Scenario
The scenario is a mall store robbery, and forensics support is needed for in and out of store evidence development (fingerprint and footprint). The code and setup is based on Nina’s Level 1 Prototype.
### Concepts tests:
  * Path of contamination
  * Finding latent evidence
  * Oblique lighting
  * 2D footprint development (inside and outside footprint)
  * 2D non-porous fingerprint development (tabletop)
  * Contextual clues (jewel - fingerprint)

## Flowchart
https://www.canva.com/design/DAGGtwH9U2I/lt68HDaaf4Tu0JLxr6QfHw/view?utm_content=DAGGtwH9U2I&utm_campaign=designshare&utm_medium=link&utm_source=editor


## Images
Loose images are main scene background images, and each folder contains screen specific images. Out of which, contents in “casefile”, “footprints”, “icons”, “mouse”, and “toolbox” were directly from Nina’s Level 1 prototype assets. Folders “tabletop” and “footprints” contain related images for demo-ed fingerprint and footprint developed under this demo scenario, respectively. 


## RenPy Code
### Miscellaneous: 
“gui.rpy” and “screens.rpy” code is default from RenPy. And “options.rpy” code was also no different from default except for added definitions for the various mouse icons, based on Nina’s adjustments. 
### Main: 
“script.rpy” contains code to the main flow logic of the scenes and materials, which calls upon screens in “custom_screens.rpy” for screen displays and interactions. “styles.rpy” contains code from Nina used for styling.


## Note: 
### Currently Implmented:
  * marking in-store evidences
  * tabletop (with fingerprints)
  * floor (with footprints)
### Features to be implemented:
  * exploring jewels in-store for fingerprints and others (jewel itself goes straight to evidence bag and filed)
  * outside scene of the storefront should also be made interactive for developing at least footprint evidence

