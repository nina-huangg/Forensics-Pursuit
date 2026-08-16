"""This file contains ZERO code. It is a guide for how to customize the AFIS system.
First, here's some terminology you'll need to know:

    (1) Importable print
            Importable prints show up on the left comparison image on AFIS.
            These are associated with a piece of evidence in your inventory.
            The scores attribute MUST be defined for these types of prints.
            I suggest naming importable prints with print_ followed by a letter
            (i.e. print_a, print_b, print_a_closeup_1). Note that you can only
            have 3 closeup images per print.
    
    (2) Non-importable print
            Non-importable prints show up on the right comparison image on AFIS.
            These are NOT associated with anything in your inventory and are
            inside the AFIS database itself. The multiple choice attribute may
            be defined for these types of prints (but it's not mandatory). 
            
            You MUST name non-importable prints with the following naming convention:
                All prints should be named print_i where i is an integer between 1 and 
                NUM_PRINTS inclusive. All closeup images of prints should be named 
                print_i_closeup_j where j is either 1, 2, or 3. You can only have 3 
                closeup images per print.

IMPORTANT: you'll need to change the function of import in screen afis since mine
opens a custom screen I made with my inventory. You can probably change it to open
Vivian S' inventory code.



How to add an IMPORTABLE print:
    (1) Prepare your image (and closeups if you want). You can name this image
    (and the closeups) whatever you want, but dimensions for both images should
    be roughly 431 x 578 in size. 

    (2) Define a Print class for your print. Suppose my print image is called
    print_a and my closeups are called print_a_closeup_1 and print_a_closeup_2.
    For an importable print, we need to define a scores attribute. scores
    is a dictionary mapping non-importable prints to their score with this print.
    Every single non-importable print should be accounted for (up to NUM_PRINTS).
    Here's an example:

    prints["print_a"] = Print(image = "print_a",
                            closeup_1 = "print_a_closeup_1",
                            closeup_2 = "print_a_closeup_2",
                            scores = {"print_1": (True, 99), 
                                    "print_2": (False, 15), 
                                    "print_3": (False, 37),
                                    "print_4": (False, 46),
                                    "print_5": (False, 39),
                                    "print_6": (False, 28),
                                    "print_7": (False, 15)}
    )

    In this example scores["print_1"][0] is True because it is the print with the
    highest consistency. Make sure to assign the class to prints[image] so that it's
    in the list of prints!

    (3) Now, you can tie this into whatever piece of evidence you want. In my case,
    clicking on the fingerprint backing card in the inventory when I'm at the afis
    location will trigger an import to the system. I use the following code:

    python:
        if location == "afis":
            imported_print = "print_a"
            renpy.jump("import_print")
         
    You must always set the value of imported_print before jumping to import_print.
    And now you're done!



How to remove an IMPORTABLE print:
    (1) Remove step 3 from above and that's it!



How to add a NON-IMPORTABLE print:
    (1) Change the value of NUM_PRINTS. I have 7 non-importable prints so NUM_PRINTS
    is 7 - but if I'm adding one more it should be changed to 8.

    (2) Prepare your image (and closeups if you want). Dimensions for both images 
    should be roughly 431 x 578 in size. You MUST name non-importable prints with the following naming convention:
        All prints should be named print_i where i is an integer between 1 and 
        NUM_PRINTS inclusive. All closeup images of prints should be named 
        print_i_closeup_j where j is either 1, 2, or 3. You can only have 3 
        closeup images per print.
    
    This naming convention must be adhered to because I use a for loop to
    automatically define the non-importable prints for you. Since you're adding
    a print, this means i should be equal to NUM_PRINTS. Using my same example,
    if NUM_PRINTS = 8, then the image names of the print I want to add should be
    called print_8, print_8_closeup_1 etc.

    (3) Change the argument passed into file_exists(). In my case, all my fingerprints
    are in images/data_analysis_lab so that's what I passed in.

    ex.
        def file_exists(file_name: str) -> bool:
            file_path = os.path.join(renpy.config.gamedir, 
                                    "images/data_analysis_lab", file_name)

    (4) OPTIONAL: Change the for loop that automatically defines classes for you.
    Right now, all my fingerprint images are pngs, but yours might be jpg or
    something else. You can change the end of closeup_filename to .jpg or .webm or
    anything else depending on your images - but note that all of your images must
    adhere to whatever you change it to.

    ex.
        for k in range(1, NUM_PRINTS + 1):
        image = f"print_{k}"
        prints[image] = Print(image=image)
        for j in range(1, 4):
            closeup_filename = f"print_{k}_closeup_{j}.png"
            closeup = f"print_{k}_closeup_{j}"
            if file_exists(closeup_filename):
                if j == 1:
                    prints[image].closeup_1 = closeup
                elif j == 2:
                    prints[image].closeup_2 = closeup
                else: # j == 3
                    prints[image].closeup_3 = closeup
            else:
                continue

    (5) OPTIONAL: add a multiple choice question by manually setting the mcq
    attribute.



How to set the mcq attribute for NON-IMPORTABLE prints:
    IMPORTANT: the same mcq assigned to a print will be asked for every importable
    print. ex. comparing print_a and print_1 will ask print_1.mcq - comparing
    print_d and print_1 will also ask print_1.mcq. If you want to explicitly
    customize questions for specific comparison pairings, you can create an
    if-else tree in label quiz.

    (1) Define an MCQ class. choices is a List[Tuple(str, bool)] where the str is
        one of the options that show up and bool is whether the option is True or False.
        responses is a List[List[str]] where each list is the response that shows up after
        selecting an option. len(choices) should equal len(responses) because
        responses[0] is associated with choices[0] and so on. This is the case even if
        you have no responses - then responses = [ [], [], [] ] or only one response
        responses = [ ["You're right"], ["Wrong"], ["Incorrect."] ].

        ex. 
        print_1_question = MCQ(
                question = "What kind of pattern is shown in the rightmost fingerprint?",
                choices = [("Checkered", False), ("Zigzags", False), ("Whorls", True)],
                responses = [["This is not a checkered pattern!", "Here's some extra text!", 
                            "And more!", "Try again!"],
                            ["This is not a zigzag pattern!", "Janna really likes Leon.", "And Connor!", "but most of all, she likes Simba!"],
                            ["This is a whorl! Good job!", "Let's finish the rest of the comparison."]]
            )

    (2) Assign it to your print using the following function:
        
        set_mcq(print_name="print_1", mcq=print_1_question)

        or you can set it manually with :
        
        prints["print_1"].mcq = print_1_question



How to remove a NON-IMPORTABLE print:
    (1) Change the value of num_prints. I have 7 non-importable prints so NUM_PRINTS
    is 7 - but if I'm removing one it should be changed to 6.

    And that's it!

    VERY IMPORTANT: you can only remove the prints from bottom to top - one by one
    (i.e. remove 7 then 6 then 5 then 4). You can't remove any print from the middle -
    you can only remove the most recently added print (like a stack).
"""