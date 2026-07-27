## start
[112] (Nina): We have a critical situation. Dispatch logged a forced carjacking; the vehicle owner was hospitalized with severe injuries, and the perpetrator fled the scene.

[114] (Nina): The vehicle was located abandoned in a commercial parking lot.

[116] (Nina): The MO aligns closely with an active serial carjacking investigation targeting high-end vehicles. We need to process this scene immediately to establish if the perpetrator is indeed our primary suspect, known as the "Pontiac Bandit."
## scene_parking

- **[125]** (Nina):  Click the licence plate on the vehicle to run the plates first.

## ran_plates
[137] (Nina): Plate verified. This is the victim's vehicle.

[138] (Nina): This vehicle is now an active crime scene tied to a violent felony. Secure the perimeter and proceed with methodical documentation.

## scence_exterior
[144] (Nina): Visual inspection of the exterior indicates the driver-side door handle remains untouched by emergency responders.

[145] (Nina): This is a primary contact point for the suspect. We will attempt a latent print lift here. Click the door handle to isolate the area.

## hotspot_door_handle

- **[160]** (Nina):  Now we can process it for prints.
- **[161]** (Nina): Process the print using the inventory.

## hotspot_door_handle
[160] (Nina): Photo taken of the door handle.

[161] (Nina): Access your field kit to begin processing the latent friction ridges on the surface.

## fingerprint_complete
[172] (Nina): The latent print is successfully lifted, mounted on a backing card, and sealed.

- **[173]** (Nina): Let's take a look at the interior now.

## scene_interior
[184] (Nina): The interior environment is preserved. We need to locate and isolate high-contact surfaces where biological or friction ridge evidence could transfer.

[185] (Nina): Methodically scan the cabin. Photograph all evidence in situ before executing collection protocols.

- **[185]** (Nina): Click on any evidence to take a photo and examine it.

## hotspot_soda_can

- **[193]** (Nina): Photo taken of the soda can.
[194] (Nina): This object represents a dual-matrix evidence source: latent prints on the body and potential salivary DNA on the rim.

## can_menu
[198] (Narrator): Select the forensic processing protocol you want for the beverage container:

## hotspot_steering_wheel

- **[226]** (Nina): Photo taken of the steering wheel. Plenty of trace evidence here.
[227] (Nina): The steering wheel substrate is highly conducive to trapping epithelial cells via friction, though it often yields complex, overlapping mixtures.

## wheel_menu

[231] (Narrator): Select the appropriate forensic processing protocol for the steering wheel:

## scene_wrap_up

[266] (Nina): Let us review the field documentation and collection sequence before transport:

[268] (Nina): Scene Documentation: Photographic evidence of each item was captured in situ with an appropriate scale bar prior to handling.

[269] (Nina): Latent Fingerprints: Developed using physical developer, documented with a scale bar, lifted with tape, and secured on a high-contrast backing card.

[270] (Nina): Biological Materials: Swabbed high-contact areas, focusing on the can rim for salivary epithelial cells to generate an STR profile.

[271] (Nina): Chain of Custody: Chronological tracking log has been signed, ensuring a continuous, unbroken chain. The integrity of the physical evidence is intact.

[274] (Nina): Transport all sealed packets to the lab for diagnostic analysis.


## AFIS quiz section
[362] (AFIS quiz): Q: Examine the core and delta positioning. What is the primary ridge classification?

[363] (AFIS quiz): choice: Loop

[363] (AFIS quiz): choice: Arch

[363] (AFIS quiz): choice: Whorl

[371] (AFIS quiz): Q: Identify the ridge flow pattern shown in this sample.

[372] (AFIS quiz): choice: Whorl

[372] (AFIS quiz): choice: Loop

[372] (AFIS quiz): choice: Arch

[380] (AFIS quiz): Q: Classify the friction ridge pattern displayed below.

[381] (AFIS quiz): choice: Arch

[381] (AFIS quiz): choice: Whorl

[381] (AFIS quiz): choice: Loop

[389] (AFIS quiz): Q: Determine the structural pattern group based on the lack of a true delta.

[390] (AFIS quiz): choice: Whorl

[390] (AFIS quiz): choice: Arch

[390] (AFIS quiz): choice: Loop

[398] (AFIS quiz): Q: What dermatoglyphic classification does this print exhibit?

[399] (AFIS quiz): choice: Loop

[399] (AFIS quiz): choice: Whorl

[399] (AFIS quiz): choice: Arch

[407] (AFIS quiz): Q: Identify the focal points to determine the ridge pattern group.

[408] (AFIS quiz): choice: Whorl

[408] (AFIS quiz): choice: Loop

[408] (AFIS quiz): choice: Arch

## lab_fingerprint_station
[681] (Nina): The automated fingerprint identification system (AFIS) requires a high-resolution digitized input file. We cannot run a database query until the scene processing is finalized.

## afis_show_results
[751] (Narrator): Search complete. The AFIS algorithm reports an optimal minutiae configuration match.

[756] (Nina): Confirming match. The minutiae points match a record within our active database: [afis_prints[_db_key].description].

[759] (Nina): Search concluded. The configuration returned no corresponding profiles within the repository: [afis_prints[_db_key].description].

[760] (Nina): This exclusion is forensically valuable. It confirms the latent print does not belong to the victim, [_owner_name].

[762] (Nina): No matching fingerprint records identified within the database.

Here is the lab section dialed down. The advanced forensic science accuracy is still exactly where it needs to be for a college-level game, but the sentences are much shorter, the pacing is faster, and the overly dense textbook jargon has been stripped out.

## scene_lab
[777] (Nina): Welcome to the lab. Now we let the physical evidence tell the story.

[778] (Nina): Take the latent print card over to the Data Analysis desk for AFIS scanning. Then, we’ll head to the DNA bench to extract our biological sample.

## lab_hub_loop (Toasts)
[1166] (Notify toast): Swab extraction phase initiated.

[1195] (Notify toast): Centrifuge cycle complete.

[1197] (Notify toast): Protocol error: Incorrect step order.

[1218] (Notify toast): Protocol error: Reagents added out of sequence.

[1221] (Notify toast): Separation column spun successfully.

[1241] (AFIS quiz): choice: vortex_clicked

[1242] (Notify toast): Action error: Tube is empty. Nothing to vortex.

[1254] (AFIS quiz): choice: dna_swab_is_vortexed_2

[1260] (Notify toast): Sample mixed. Vortexed for 15 seconds.

[1278] (Notify toast): Action error: Incubator is empty. Load your sample.

[1295] (Notify toast): Protocol error: Incubation skipped out of sequence.

## dna_lab_entry
[1420] (Nina): We can't extract DNA from thin air. Go back to the vehicle and collect a physical sample first.

## dna_incubator_question
[1468] (Narrator): Set the incubator temperature and timer for cell lysis:

[1470] (Menu choice): 37°C for 15 minutes

[1471] (Nina): That temperature is too low. We need 56°C for 10 minutes to activate the Proteinase K enzyme and break open the cell membranes. Try again.

[1474] (Menu choice): 56°C for 10 minutes

[1478] (Menu choice): 95°C for 5 minutes

[1479] (Nina): Too hot. 95°C will destroy our active enzymes before they can do their job. Save that heat for the PCR machine later. Set it to 56°C.

## dna_finish_step_1
[1568] (Nina): Lysis complete. The cells are broken down and the DNA is suspended in the liquid lysate.

[1570] (Nina): Now we begin the purification steps to separate the DNA from unwanted proteins and fats. Keep your pipetting precise.

[1572] (Nina): That's the final wash done. The spin column is dry and ready for us to collect the clean DNA.

## dna_swab_question_1
[1583] (Narrator): The sample is loaded into the spin column, and the DNA is bound to the filter matrix. Next, we need a purification wash using Buffer AW1.

[1584] (Narrator): How much Buffer AW1 should be pipetted into the column?

[1586] (Menu choice): 200µL Buffer AW1

[1587] (Nina): Not enough volume. 200µL won't wash away all the leftover proteins, leaving our final sample contaminated. We need exactly 500µL.

[1591] (Menu choice): 500µL Buffer AW1

[1595] (Menu choice): 1000µL Buffer AW1

[1596] (Nina): That will flood the column assembly and ruin the wash. Bring it back down to 500µL.

## dna_swab_question_2
[1602] (Narrator): After the first wash, Buffer AW2 is added to remove remaining salts. How long should we spin the sample in the centrifuge for this step?

[1604] (Menu choice): 1 minute

[1605] (Nina): Too short. A 1-minute spin leaves residual ethanol in the filter, which will completely ruin our later PCR reactions. It needs a full 3 minutes.

[1609] (Menu choice): 3 minutes

[1613] (Menu choice): 10 minutes

[1614] (Nina): Spinning for 10 minutes is overkill and risks tearing the DNA apart under intense friction. Stick to the standard 3 minutes.

## dna_swab_question_3
[1620] (Narrator): The purified DNA is ready to be washed off the filter into a clean tube. How much of this extracted DNA template should go into our 50µL PCR reaction mix?

[1622] (Menu choice): 1µL extracted DNA

[1626] (Menu choice): 5µL extracted DNA

[1627] (Nina): If the sample is too concentrated, leftover chemicals from the extraction will overwhelm the DNA polymerase. Keep it to a clean 1µL.

[1631] (Menu choice): 10µL extracted DNA

[1632] (Nina): That much volume will stall out the reaction entirely. 1µL is all it takes for a 50µL target mix.

## dna_finish_swab
[1639] (Nina): Clean yield. The DNA is isolated, purified, and ready in the tube.

[1640] (Nina): Let’s run a quick qPCR assay to measure exactly how much human DNA we recovered from the car.

## dna_reaction_question_1
[1646] (Narrator): Which of these components is NOT used in a standard DNA profiling mix?

[1648] (Menu choice): Master mix

[1649] (Nina): Incorrect. The master mix holds the essential polymerase and building blocks for replication. We definitely need it.

[1653] (Menu choice): Forward and reverse primers

[1654] (Nina): Incorrect. Primers act as chemical markers to target the specific DNA regions we want to look at.

[1658] (Menu choice): Nuclease-free water

[1659] (Nina): Incorrect. We use it to bring the chemical mix up to volume safely without degrading the DNA.

[1663] (Menu choice): Reverse transcriptase

[1664] (Nina): Correct. That enzyme is used to copy RNA, not DNA. It has no place in an STR profiling kit.

[1668] (Menu choice): Magnesium chloride

[1669] (Nina): Incorrect. Magnesium ions are required to catalyze the duplication process.

## dna_reaction_question_2
[1676] (Narrator): What size microcentrifuge tube should be used to prepare this mix?

[1678] (Menu choice): 1.0 mL tube

[1679] (Nina): Non-standard size. Grab a standard 1.5 mL tube so we have enough room to mix the reagents safely.

[1683] (Menu choice): 1.5 mL tube

[1687] (Menu choice): 2.0 mL tube

[1688] (Nina): Too large. A 2.0 mL tube won't sit properly in our benchtop centrifuges, and it makes it harder to see the liquid pellet. Stick to 1.5 mL.

## dna_reaction_question_3
[1693] (Nina): Good. Dilute the purified DNA 1:1 with nuclease-free water to stabilize our final working solution.

## dna_pcr
[1708] (Nina): The quantification data looks great. We have more than enough DNA to get a profile.

[1710] (Nina): Now for the real test. We'll load the DNA, the master mix, and the fluorescent primers into the thermal cycler to copy our target forensic markers.

[1711] (Nina): Amplification is complete. The markers are copied millions of times over. Let's move the tube to the capillary electrophoresis unit to read the data.

## dna_cem_finish
[1723] (Nina): The electropherogram results are printing out now.

[1724] (Nina): It’s a clean, single-source profile. The lack of genetic noise means we pulled skin cells from touch transfer, not fluid.

[1725] (Nina): Running the data through the criminal database now... We have an exact match for [_robber_name].

[1729] (Nina): That solidifies our biological evidence. Let's head back to the main desk and wrap this up.

## lab_conclusion
[1740] (Nina): The forensic data is clear. The fingerprint minutiae from the outside handle and the DNA markers from the cabin lead to one person: [_robber_name], our Pontiac Bandit.

[1741] (Nina): We have undeniable physical proof placing him inside that vehicle. I'm calling the District Attorney to get a felony arrest warrant signed.

[1743] (Nina): Excellent protocol work today. The evidence is airtight. Case closed.