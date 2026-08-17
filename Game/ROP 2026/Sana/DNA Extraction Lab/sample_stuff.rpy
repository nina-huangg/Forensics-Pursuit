init -10 python:
    def discard_spin_column(sample):
        """
        Function for discard sample screen
        """
        if curr_sample.has_spin_column:
            curr_sample.has_spin_column = False
            curr_sample._mass_DNA_bound = 0
        else:
            renpy.notify("Tube has no spin column to discard!")
        renpy.hide_screen("choose_discard_type")
    

    def discard_sample(sample):
        """
        Function for discard sample screen
        """
        global curr_sample
        item = evidence.get_item(sample.label)
        if item is not None:
            evidence.delete_from_inventory(item)
        if curr_sample is sample:
            curr_sample = None
        
        renpy.hide_screen("choose_discard_type")


    class Solvent(object):
        def __init__(self, name, introduces_impurity=False, impurity_type=None):
            self.name = name
            self.introduces_impurity = introduces_impurity
            self.impurity_type = impurity_type

    SOLVENTS = {
        "ethanol":   Solvent("Ethanol"),
        "bufferAE":  Solvent("Buffer AE"),
        "PBS":       Solvent("PBS"),
        "proteaseK": Solvent("Proteinase K", introduces_impurity=True, impurity_type="protein"),
        "bufferAL":  Solvent("Buffer AL", introduces_impurity=True, impurity_type="chaotropic_salt"),
        "bufferAW1": Solvent("Buffer AW1", introduces_impurity=True, impurity_type="ethanol_residue"),
        "bufferAW2": Solvent("Buffer AW2", introduces_impurity=True, impurity_type="ethanol_residue"),
    }

    class Tube_2ml:
        """
        A 2ml tube used during the DNA extraction process as well as all the relevant contents of such a tube.

        For the sake of convenient numerical representation, the smallest unit within the tube will be a microliter. Remember, this is by no means a
        perfect simulation (if it was there would be quite a pretty penny to be earned) but a basic tool to help forensic science students gain familiarity
        with the DNA extraction process. I will also say that a more optimally class design would be to have a composition with a DNA class but we do not need
        to worry about that for the scope of this project.

        Class Attributes:
            max_volume: The maximum volume of the tube in microliters. In this case, 2000.
          
        Instance Attributes:
            -label: A user given string that identifies the contents of the tube

            _mass_DNA: The total mass of DNA contained within the collected blood cells. Initially all DNA is contained within the
            membranes of the cell. That is the mass represented by this variable.

            _mass_DNA_free: The mass of DNA in solution. This is the mass that is used for the concentration calculation displayed to players.
            Its existence is mandated by the fact that there are instances where there is no free DNA within the solution. This occurs initially when
            DNA is stil trapped within cells and when DNA adheres to spin columns.

            _mass_DNA_bound: The mass of DNA that has been bound to the spin column within the sample tube.

            _volume_impurity: The volume of impurities, that is non-DNA solids, within the tube in microliters

            _volume_solvent: The volume of the combined liquids (e.g. water, buffers, ethanol, etc.) within the tube microliters

            has_spin_column: A boolean value that denotes if the tube has a spin column in it

            uniformly_mixed: A boolean value that denotes if the mixture within the tube is homogenous through vortexing and spinning

            centrifuged: A boolean value that denotes if the tube has been centrifuged. 

            _concentration_DNA: The concentration of DNA within the tube. This is the value that should be represented to the player and around which the game should revolve.
            For more info on how it is calculated, see the calculate_concentration_DNA method.

            _decay_rate: The rate, in mass of DNA per second, at which free DNA degrades while
            it sits in solution. Represents nucleases and general instability acting on DNA
            that isn't yet bound to a column or otherwise protected. Does not affect DNA
            still trapped in unlysed cells (_mass_DNA) or DNA already bound to a spin column
            (_mass_DNA_bound) - those are assumed comparatively protected. 

            has_protease: A boolean that indicates if there is a protein digesting enzyme within the tube.
        """
        label: str

        _mass_DNA: int
        _mass_DNA_free: int
        _mass_DNA_bound: int

        _volume_solvent: int
        _concentration_DNA: float

        has_spin_column: bool
        uniformly_mixed: bool
        centrifuged: bool

        has_ethanol: bool
        has_protease: bool
        has_AW1: bool
        has_AW2: bool
        proteins_washed: bool
        has_chaotropic_salts: bool

        max_volume = 2000

        def __init__(self, label: str, mass_DNA=0, volume_solvent=0, decay_rate=0):
            #These variables store the amount, in microliters, of DNA, solvent, and impurities within the sample for concentration calculations
            self.label = label 

            self._mass_DNA = mass_DNA

            #For scope I will simply treat impurities as boolean 
            #self._volume_impurity = volume_impurity

            self._volume_solvent = volume_solvent
            self._mass_DNA_free = 0
            self._mass_DNA_bound = 0
            self._decay_rate = decay_rate

            self.has_spin_column = False
            self.uniformly_mixed = False
            self.centrifuged = False

            self.has_ethanol = False
            self.has_AW1 = False
            self.has_AW2 = False
            self.has_AE = False
            self.has_protease = False
            self.has_chaotropic_salts = False
            self.proteins_washed = False

            self._concentration_DNA = 0
            self.calculate_concentration_DNA()
        
     
            #This represents DNA concentration within the sample. It will be the main resource the extraction stage revolves around
            #Make it mass of DNA as opposed to concentration
        def calculate_concentration_DNA(self) -> None:
            """
            Updates the DNA concentration attribute to reflect changes in the amount of solutes or solvents within the tube.
            """
            volume_total = self.get_total_volume()
            
            #There is no sample
            if volume_total == 0:
                self._concentration_DNA = 0
            else:
                #Ensures concentration is a precentage (May need to change later)
                self._concentration_DNA = round( ( (self._mass_DNA_free / volume_total) * 100) )
            print(self._concentration_DNA)

    
        #TODO What can be introduced into a sample tube through adding reagents? What can be removed from doing so? 
        def add_impurity(self, value: int) -> None:
            """
            Increases volume of impurities and ensures change is reflected in DNA concentration
            """
            #Check ensures that there is no negative mass possible
            self._volume_impurity = max(0, self._volume_impurity + value)
            self.calculate_concentration_DNA()
        
        def add_solvent(self, value: int) -> None:
            """
            Increases volume of solvent and ensures change is reflected in DNA concentration
            """
            self._volume_solvent = max(0, self._volume_solvent + value)
            self.calculate_concentration_DNA()

        def add_proteaseK(self) -> None:
            self.has_protease = True
        
        def add_spin_column(self) -> None:
            #TODO Later on perhaps make it so that spin column occupies some volume although this is not mandatory.
            self.has_spin_column = True
    
        
        def get_total_volume(self) -> int:
            """
            Returns the total volume of tube through summation of all components
            """
            #At the moment the 1 g of DNA is equivalent to 1 microliter of DNA. This is likely to not be accurate but it is
            #good enough for the purpose of this project. The if is to account for the reduced amount that can fit within a spin column before overflow.
            return self._mass_DNA_free + self._volume_solvent   

        def has_space(self, value: int) -> bool:
            """
            Returns a boolean based on if the tube has space for additional amount, value
            """
            return self.get_total_volume() + value < self.max_volume
            
        def free_DNA(self, percentage: float) -> None:
            """
            Converts given percentage of _mass_DNA into mass_free_DNA
            """
            percentage = max(0, min(1, percentage))
            value = self._mass_DNA * percentage
            self._mass_DNA -= value
            self._mass_DNA_free += value

            self.calculate_concentration_DNA()
        
        def free_bound_DNA(self, percentage: float) -> None:
            percentage = max(0, min(1, percentage))
            value = self._mass_DNA_bound * percentage
            self._mass_DNA_bound -= value
            self._mass_DNA_free += value

            self.calculate_concentration_DNA()
        

        def degrade(self, elapsed_seconds: float) -> None:
            """
            Reduces free DNA to reflect degradation over time. Only affects
            _mass_DNA_free - DNA still trapped pre-lysis or bound to a spin
            column is left untouched, since it isn't the pool this models.
            """
            if self._mass_DNA_free <= 0:
                return

            loss = self._decay_rate * elapsed_seconds
            self._mass_DNA_free = max(0, self._mass_DNA_free - loss)
            
            #If there is protease at room temperature it will not function optimally; however, I believe it should still be digesting to some small
            #extent reducing DNAses and the damage they cause. 
            if self.has_protease:
                self._decay_rate *= 0.99

                #More uniform distribution of protease means that slightly more DNase digestion can occur at room temperature.
                if self.uniformly_mixed:
                    self._decay_rate *= 0.99

            self.calculate_concentration_DNA()
        
        def incubate(self) -> None:
            if self.has_protease:
                self._decay_rate *= 0.20

                if self.uniformly_mixed:
                    self._decay_rate = 0
             
    

#TODO come back and clean up this abomination of a screen
screen sample_info:
    #This timer is specifically placed here as sample screen will always be show and thus the timer will always be active.
    timer DECAY_TICK_SECONDS repeat True action Function(degrade_all_samples)

    hbox:
        at topright
        vbox:
            use sample_name
            hbox:
                box_reverse True
                if curr_sample is not None:
                    if transfer_source is None:
                        use discard_sample
                    use transfer_sample
            if transfer_source is None:
                use submit_sample
        if curr_sample is not None and transfer_source is None:
            use tube_concentration_bar

    if curr_sample is not None and transfer_source is None and curr_sample.has_spin_column:
        add "spin_column_visual" at topright
        
        
screen sample_name:
    $sample_label = curr_sample.label if curr_sample is not None else "No Tube Selected"
    frame:
        xminimum 290
        text sample_label

    
screen discard_sample:
    imagebutton:
        auto "discard-inventory-icon-%s"
        action Show("choose_discard_type")


screen transfer_sample:
    imagebutton:
        auto "transfer-inventory-icon-%s"
        action If(transfer_source is None, Function(start_transfer), Function(cancel_transfer))


screen submit_sample:
    imagebutton:
        idle "images/UI/submit_idle.png"
        hover "images/UI/submit_hover.png" 
        action Confirm("Are you sure you want to submit the current tube for quantification and conclude the extraction process?", If(curr_sample is not None, Jump("end"), Notify("You cannot submit nothing. At least give me an empty tube!")))


screen tube_concentration_bar:
    """
    The win condition of the extraction stage is managing to extract concentrated enough DNA
    for usage in the PCR process. It is hard to represent concentration but I think volume should be easy enough to 
    do. The volume we will look at are the volumes within the tube bar.
    """
    if curr_sample is not None:
        #This makes it so that the bar is not an interactable and only used for display
        sensitive 0
        
        #I had the idea of using multiple bars within the same screen to overlay one another and give the effect of a multi variable bar.
        #Unfortunately, this did not work as the bars cover each other when I attempt to over lay them.

        vbar at right:
            yfill True
            xsize 210
            top_bar "gui/bar/tube_top.png"
            bottom_bar "gui/bar/tube_bottom.png"
            bar_resizing True
            value AnimatedValue(curr_sample._concentration_DNA, 100, 0.7)
            range 100 

    """
    #Extra Bars for testing stuff
    vbar at right:
        xoffset -300
        bar_resizing True
        value AnimatedValue(sample._volume_solvent, 2000, 0.7)
        range 100 
    
    vbar at right:
        xoffset -500
        bar_resizing True
        value AnimatedValue(sample._volume_impurity, 2000, 0.7)
        range 100 
    """