# Scenario: Detecting Cleaned Up Blood
All the game files can be found in the directory titled "Detecting Cleaned Up Blood". Details about the scenario can be found below.

## Flowchart:
Link to flowchart: https://lucid.app/lucidchart/460a0ce6-e35b-43e3-a535-18c7940649b1/edit?viewport_loc=-652%2C612%2C1653%2C667%2C0_0&invitationId=inv_a7faac27-1046-419a-9ea2-b73c05ab4c53

## What is Currently Completed:
- Navigation between the main scenes:
  - Implemented navigation between the view of the entire kitchen, the stove, inside the oven, viewing the dish towel, a closeup of the floor and the closeup of the wall
  - Visual elements included a white outline around the object when hovered over and the mouse cursor changes into a magnifying glass
  - How the player can navigate through the scenes:
    - Player can select the floor where there is cleaned up blood only after they discovered it with ALS
    - Player can select the wall where there is cleaned up blood only after they discovered it with ALS
    - Player can select the stove to investigate it further
      - Player can then select the dish towel to get a closer view or the oven door to look inside the oven
- Added the button for ALS flashlights (the picture for the button is temporary)
  - When the player selects the button, a panel with each available ALS flashlight appears for the player to choose which one to use. So far only the UVA and 415nm flashlights have been implemented for the main kitchen scene.

## Feedback Received:
- Limit the scenario to one room/seciton (completed, the scenario now only takes place in the kitchen near the stove)
- Limit things that the player is able to click on

## What Needs to be Developed/Bug Fixes:
- Need to replace the temporary pictures (most of which are temporary) with the actual pictures once they are taken and change the hotspot locations to match the new pictures
- Need to implement the forensic tools and how they can be used (if they can be) for each object
- Need to implement the mistakes the player can make
- Bug Fixes:
  - Sometimes toolbox disappears after using the ALS flashlight

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
