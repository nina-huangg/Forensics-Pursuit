# Prototypes of the First Level

## Crime Scene
tbd

## Lab Scene
The Lab Scene contains a backbone structure that students can copy and use. There is currently no configuration for any of the analyzing steps, as I realize that everyone will have different implementations and use different tools. The goal is to first provide a structure so that the interface is consistent. My goal is that after looking at everyone's projects, I can incorporate and structure all the different machines used more cleanly and create a version that includes all these tools. 
* If students want a version of the fingerprint development process using the CA fuming chamber, they can refer to the tutorial lab scene. 

## Testimony Scene
The Testimony Scene is very easy to configure, there is essentially no coding involved.  
To configure this level, there are two parts.
#### Load the questions
In ```script.py```, under the python function ```load_q_a()```, insert all your questions, potential answers, and the correct answer like the following example.
Here is an example: 
```
function load_q_a() {
  global q_a_bank // a list of dictionaries containing info about the question
  q_a_bank.append({
            'question': "What method did you use to develop fingerprints on the firearm and why?",
            'choice_1': "Cyanoacrylate fuming, abbreviated as CA fuming",
            'choice_2': "Ninhydrin powder",
            'choice_3': "Fluorescent powder",
            'answer': 'choice_1'
  })
}
```
#### Insert Evidence Photos
To help with a player's memory during the testimony scene, I included the evidence hotbar developed by Vivian S. The hotbar essentially just contains all the pieces of evidence developed in the lab that the user can refer back to.
* If there is time, I would like to include documents of fingerprint analysis (produced by CSIPix) that the users can refer to. 

## How to use these files
Feel free to copy these files into your folder as a template to develop from! 
Please go by this naming convention if possible: 
- [name]_crime_scene_prototype
- [name]_lab_scene_prototype
- [name]_testimony_scene_prototype
