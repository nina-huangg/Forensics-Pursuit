# Scenario: Detecting Cleaned Up Blood
All the game files can be found in the directory titled "Detecting Cleaned Up Blood". Details about the scenario can be found below.

## Flowchart:
Link to flowchart: https://lucid.app/lucidchart/460a0ce6-e35b-43e3-a535-18c7940649b1/edit?viewport_loc=-652%2C612%2C1653%2C667%2C0_0&invitationId=inv_a7faac27-1046-419a-9ea2-b73c05ab4c53

## What is Currently Completed:
- Navigation between the main scenes:
  - Implemented navigation between the view of the entire kitchen, the stove, viewing the dish towel, and a closeup of the floor
  - Visual elements include the mouse cursor changeing into a magnifying glass or an exclamation point
  - How the player can navigate through the scenes:
    - Player can select the floor where there is cleaned up blood only after they discovered it with ALS
    - Player can select the stove to investigate it further
      - Player can look down and then select the dish towel to get a closer view
- Added the button for ALS flashlights (the picture for the button is temporary)
  - When the player selects the button, a panel with each available ALS flashlight appears for the player to choose which one to use. So far only the UVA and 415nm flashlights have been implemented for the main kitchen scene.
  - Implemented collecting the knife, including:
    - Placing the evidence marker
    - Putting the knife in an evidence bag
    - Sealing the evidence bag with tape
  - Implemented collecting the dish towel, including:
    - Placing te evidence marker
    - Putting the dish towel in an evidence bag
    - Sealing the evidence bag with tape
  - Implemented the pool of blood, including:
    - The kastle-meyer test, selecting the cotton swab, wetting it, swabbing the floor, applying ethanol, phenolphthalein and hydrogen peroxide. Also allowed for some mistakes (if ot done in the correct order, will not get the correct result)
    - Collecting the blood, selecting the cotton swab, wetting the swab, swabbing the floor, putting it in the tube (the rest needs to be further implemented
    - Making the luminol and spraying it, selecting the spray bottle, adding distilled water, adding the luminol tablet, and spraying the floor 3 times, then seeing the fluorescing blood
  - Started implementing the fingerprint:
    - Can select the uv flashlight and find the fingerprint, when the fingerprint is selected, the evidence marker is placed

## Feedback Received:
- Limit the scenario to one room/seciton (completed, the scenario now only takes place in the kitchen near the stove)
- Limit things that the player is able to click on (completed)
- Remove the wall spatter, remove the knife from the oven and instead have it on top of the stove, add a fingerprint on the stovetop (completed)
- Make the flashlight effect match what Luke's

## What Needs to be Developed/Bug Fixes:
- Need to replace the temporary pictures (most of which are temporary) with the actual pictures once they are taken and change the hotspot locations to match the new pictures
- Need to finish implementing the fingerprint collection
- Need to fully implement the mistakes the player can make (only somewhat implemented so far)
- Still need to implement the flashlight effect for the ALS flashlights and the uv flashlight
- Bug Fixes:
  - Sometimes toolbox disappears after using the ALS flashlight
  - Tools disappear after selecting the spray bottle and the distilled water when the spray bottle has been selected
  - Tools disappear when switching between different areas (I think the toolbox might still be open but the tools are not showing so need to click on the toolbox twice to see the tools)
  - Evidence marker for fingerprint disappears
  - After selecting the cotton swab the first time, all the tools disappear but can still be clicked on
  - After selecting the cotton swab a second time, the distilled water, ethanol and cotton swab buttons are visible but cannot be clicked on/selected

___

# Scenario: Trespassing Gone Wrong
## Overview of Scenario:
A neighbour reported seeing someone entering the abandoned house nextdoor. When police arrive at the house, they find nobody but notice the door is unlocked. Upon entering the house, they find human skeletal remains along with a gun and some used syringes, evidence that someone is currently living there. Your job is to collect all the available forensic evidence to help solve this potential homicide.

## Flowchart:
Link to flowchart: https://lucid.app/lucidchart/c6df9aad-4867-4477-8d4a-0da4b3b091f2/edit?viewport_loc=-41%2C-570%2C2054%2C829%2C0_0&invitationId=inv_f09d1801-f7dc-4e0f-96ba-160139165f32

## What is Currently Completed:
- The section of the game involving collecting evidence outside, including:
  - Collecting the footprints left in nearby soil
  - Collecting a fingerprint left on the door of the house

## What Needs to be Developed:
1. Collecting evidence inside of the house, including:
   - Collecting the human skeletal remains that will be behind the couch
   - Collecting the gun on the table
   - Collecting the 2 used syringes that are also on the table
   - Allowing the player to investigate the couch and collect a strand of hair off it
   - Allowing the player to look through drawers in a dresser for any evidence
2. Bug fixes:
   - Fixing bug where toolbox visually disappears after placing evidence marker by the footprints (you currently need to click where the toolbox is to make it reappear)
