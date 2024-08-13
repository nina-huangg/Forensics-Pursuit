# Scenario: Detecting Cleaned Up Blood 
# Crime Scene Collection:
All the game files can be found in the directory titled "Detecting Cleaned Up Blood". Details about the scenario can be found below.

## Flowchart:
Link to flowchart: https://lucid.app/lucidchart/460a0ce6-e35b-43e3-a535-18c7940649b1/edit?viewport_loc=-652%2C612%2C1653%2C667%2C0_0&invitationId=inv_a7faac27-1046-419a-9ea2-b73c05ab4c53

## What is Currently Completed:
- Navigation between the main scenes:
  - Implemented navigation between the view of the entire kitchen, the stove, viewing the dish towel, and a closeup of the floor
  - Visual elements include the mouse cursor changing into a magnifying glass or an exclamation point
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
  - Implemented the fingerprint:
    - Can select the uv flashlight and find the fingerprint, when the fingerprint is selected, the evidence marker is placed
    - Can then dust the fingerprint, once that happens the view is zoomed in on the dusted fingerprint
    - The player can then place the scalebar, lifting tape place on a backing card and put in an evidence bag and seal it
  - Implemented the flashlight effect for the ALS flashlights and the UV flashlight
  - Added outlines to interactable objects
  - Added the different cursors
  - Added dialogue messages, for events such as colledcting a piece of evidence, discovering blood or a fingerprint, and warning/guiding messages for the player
  - Changed the casefile evidence to be two separate screens, one for the collected evidence, one for the pictures
  - Fixed how the knife is packaged, you now first need to put the knife in a plastic tube, seal it with the tamper tape, then put the tube in the evidence bag and tape it
  - Changed how water is put on the swab to match how the chemical solutions are put on the swab
  - Added separate button for the backing card
  - Added the debrief scene before the player enters the house
  - Fixed bug that kept leading the player to the fingerprint scene and taping the evidence bag
  - Implemented Vivian's inventory system
  - Added a camera button to take pictures of the current scene and evidence, and implemented a system so the photos are shown in the order taken
  - Changed the way the screen looked when looking through the photos taken
  - Replaced all stock photos

## Feedback Received:
- Limit the scenario to one room/seciton (completed, the scenario now only takes place in the kitchen near the stove)
- Limit things that the player is able to click on (completed)
- Remove the wall spatter, remove the knife from the oven and instead have it on top of the stove, add a fingerprint on the stovetop (completed)
- Make the flashlight effect match Luke's
- Blur the background for the subcategories of forensic tools (completed)
- Change the colour of the exclamation point from red to another colour (completed, changed from red to yellow)

## What Needs to be Developed/Bug Fixes:
- Bug Fixes:
  - Currently do not know of any bugs
 
# Lab Scene:

## What is Currently Completed:
- Navigation within the materials lab, can currently navigate between the lab bench, fumehood and cyanosafe
- Implemented the hemastix and collecting a sample on both the dish towel and knife on the lab bench
  - Guiding messages have been added to inform the player that:
    - That they need to use a hemastix before collecting a sample
    - Are using a hemastix when trying to start swabbing and vice versa
    - They messed up the presumptive test with the hemastix, and prompt the player to try again
    - The player is trying to collect an incorrect sample
    - The player has successfully performed the presumptive test and should photograph the positive result next to the evidence and then collect a sample
- Implemented lifting the print in the cyanosafe
  - Guiding messages have been added to inform the player that:
    - A sample has not been collected and that should be done first (the player can bypass this and continue with lifting the fingerprint which will result in damaged DNA)
    - The time provided by the player is incorrect and should try again
    - After the print has been lifted, a message hints toward staining the knife and provides further guidance if the player is still unsure about what to do, directly telling them to stain the knife
  - The player is able to put the knife, superglue and distilled water into the cyanosafe in any order, once the player has put the knife in the cyanosafe, they cannot go back
- Implemented staining the knife in the fumehood
  - The player is able to put the knife in the fumehood, select the stain and stain the knife blade, and then collect the knife once again to use ALS to see the fingerprint
  - When the player has stained the knife a message guides them to use ALS on the knife
- Implemented using ALS on the knife
  - Allows the player to use the UVA, 415nm, 450nm, or 530nm (only the 450nm flashlight will work)
  - The player can select the scalebar and place it by the fingerprint to take a scaled photo of the print
  - The player must take a scaled photo of the fingerprint under ALS and has the option to take a scaled photo of the fingerprint without ALS
- When the player selects a sample swab, a message will appear asking the player if they would like to send the sample off to start the extraction process. Upon answering yes, the player will receive the extracted DNA (not implemented yet), if they answered no the sample remains in their inventory
- Implemented the DNA analysis procedure
  - Implemented the use of the DNA machines, the centrifuge, PCR, thermal cycler, plate centrifuge and MiSeq, and messages for when the player does not need to use them.
  - Implemented comparing the genetic profiles in the data analysis lab, adding the profiles to the table of findings and the explanation once the table is complete.
- Implemented info buttons for each of the machines that provide a description of the machine when clicked on
- Implemented Janet's timer
- Implemented Janna's AFIS code to allow the player to analyze the two fingerprints collected

## Feedback Recieved:
- The amount of guiding messages so far is good

## What needs to be Developed/Bug Fixes:
- Bug Fixes:
  - Currently do not know of any

# Testimony Scene

## What is currently completed
- The player's name is collected and they are sworn in (code for player being sworn in is from Vivian F.)
- Player is asked 19 questions
- Player is told their score and then go over what questions they answered incorrectly

## What needs to be developed
- Bug Fixes:
  - Currently do not know of any

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
