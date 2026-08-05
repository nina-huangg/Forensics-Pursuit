init -10 python:
    """
    Evidence-collection process framework.

    Each real-world procedure (fingerprint, can, wheel, ...) is an
    EvidenceProcess: an ordered list of tool names plus what to say/do at
    each step. Every toolbox item's action just calls use_tool(item_name) -
    it never needs to know which process is active, and a process never
    needs its own bespoke Python function.

    To add a new procedure later (e.g. the gearshift):
        1. Add a new EvidenceProcess below with its step order/messages.
        2. Make sure its tools are usable / "auto" in toolbox.json.
        3. Set `active_process = gearshift_process` when entering that hotspot.
    """

    class EvidenceProcess:
        def __init__(self, name, steps, step_messages=None, bag_item_image=None,
                     bag_drag_name=None, on_complete=None, image_prefix=None, overlay_pos=None,
                     revert_scene=None):
            self.name = name
            self.steps = steps
            self.step_messages = step_messages or {}
            self.bag_item_image = bag_item_image
            self.bag_drag_name = bag_drag_name
            self.on_complete = on_complete
            self.step_index = 0
            ## Which set of step images to use -- defaults to this process's
            ## own name, but processes that do the same physical technique
            ## (dusting a print, say) can share one art set by passing the
            ## same image_prefix, instead of needing separate images per
            ## pickup location.
            self.image_prefix = image_prefix or name
            ## The background scene to return to once this process moves
            ## past whatever close-up art exists (e.g. once it advances
            ## from Tape into Backing Card, which has no dedicated art) --
            ## normally whatever scene was showing before the close-up
            ## started.
            self.revert_scene = revert_scene
            ## (x, y) pixel position (in the 1920x1080 game canvas) to
            ## center the step visual on -- normally the middle of this
            ## process's hotspot, so the close-up appears right over the
            ## door handle / can / wheel instead of a fixed screen corner.
            ## None falls back to a default corner position.
            self.overlay_pos = overlay_pos

        @property
        def complete(self):
            return self.step_index >= len(self.steps)

        def current_step(self):
            return None if self.complete else self.steps[self.step_index]

        def check(self, tool_name):
            """Validate tool_name against this process without changing state."""
            if tool_name not in self.steps:
                return "invalid"
            idx = self.steps.index(tool_name)
            if idx < self.step_index:
                return "late"
            elif idx > self.step_index:
                return "early"
            return "correct"

        def advance(self):
            self.step_index += 1
            if self.complete and self.on_complete:
                self.on_complete()

        def reset(self):
            self.step_index = 0

        def current_image(self):
            """
            Returns the auto-image name for the close-up view: the base
            "<image_prefix>_closeup" before anything's been done, or once a
            step with no dedicated art happens (Backing Card, Evidence Bag,
            Tamper Evident Tape -- meaning the print's been lifted away and
            the surface is clean again); otherwise whichever step was most
            recently completed, e.g. "fingerprint_magnetic_powder" ->
            "fingerprint_scalebar" -> "fingerprint_tape".
            """
            base = "{}_closeup".format(self.image_prefix)
            if self.step_index == 0:
                return base
            slug = self.steps[self.step_index - 1].lower().replace(" ", "_")
            candidate = "{}_{}".format(self.image_prefix, slug)
            if renpy.image_exists(candidate):
                return candidate
            return base


    def use_tool(tool_name):
        """The single entry point every toolbox item's action funnels through."""
        global active_process

        if active_process is None or active_process.complete:
            renpy.notify("Nothing to do with that right now.")
            return

        result = active_process.check(tool_name)

        if result == "invalid":
            renpy.notify("That's not going to help with this.")
        elif result == "late":
            renpy.notify("Already done.")
        elif result == "early":
            renpy.notify("Try the {} first.".format(active_process.current_step()))
        elif result == "correct":
            if tool_name == "Magnetic Powder":
                if renpy.call_in_new_context("magnetic_powder_quiz"):
                    active_process.advance()
                    renpy.notify(active_process.step_messages.get(tool_name, "Done."))
            elif tool_name == "Evidence Bag":
                renpy.show_screen(
                    "drag_to_bag",
                    item_image=active_process.bag_item_image,
                    item_drag_name=active_process.bag_drag_name,
                )
            elif tool_name == "Tamper Evident Tape":
                renpy.show_screen("drag_tape_to_bag")
            else:
                active_process.advance()
                renpy.notify(active_process.step_messages.get(tool_name, "Done."))


    class AutoAction(object):
        """
        A picklable stand-in for a closure. Ren'Py needs to pickle the entire
        store for rollback/save, and a lambda/closure (like
        `make_auto_action` used to return) can't be pickled - only plain
        objects with simple attributes can. This does the same job as the
        old lambda but survives rollback and save/load.
        """
        def __init__(self, tool_name):
            self.tool_name = tool_name

        def __call__(self):
            use_tool(self.tool_name)


    def make_auto_action(tool_name):
        return AutoAction(tool_name)


 ## --- Completion callbacks ---------------------------------------------
    ## Each just records the evidence and notifies — no more auto-jumping to
    ## a "complete" label, since the player loops back to a choice menu now.

    def _fingerprint_on_complete():
        evids = load_items("jsons/evidence.json")
        store.evidence.add_to_inventory(evids["Door Fingerprint"])
        renpy.notify("All steps done!")

    def _can_print_on_complete():
        evids = load_items("jsons/evidence.json")
        store.evidence.add_to_inventory(evids["Can Print"])
        renpy.notify("Print lifted from the can.")

    def _can_dna_on_complete():
        evids = load_items("jsons/evidence.json")
        store.evidence.add_to_inventory(evids["Can Swab"])
        renpy.notify("DNA swab collected from the can.")

    def _can_whole_on_complete():
        evids = load_items("jsons/evidence.json")
        store.did_can = True
        store.evidence.add_to_inventory(evids["Can bag"])
        renpy.notify("Can collected and sealed.")

    def _wheel_print_on_complete():
        evids = load_items("jsons/evidence.json")
        store.evidence.add_to_inventory(evids["Wheel Print"])
        renpy.notify("Print lifted from the wheel.")

    def _wheel_dna_on_complete():
        evids = load_items("jsons/evidence.json")
        store.evidence.add_to_inventory(evids["Wheel Swab"])
        renpy.notify("DNA swab collected from the wheel.")


    ## --- Process definitions ------------------------------------------------

    fingerprint_process = EvidenceProcess(
        "fingerprint",
        steps=["Magnetic Powder", "Scalebar", "Tape", "Backing Card", "Evidence Bag", "Tamper Evident Tape"],
        step_messages={
            "Magnetic Powder": "Step 1/6: Powder applied.",
            "Scalebar": "Step 2/6: Scalebar placed.",
            "Tape": "Step 3/6: Print lifted.",
            "Backing Card": "Step 4/6: Backing card placed.",
        },
        bag_item_image="backing fingerprint",
        bag_drag_name="fingerprint",
        on_complete=_fingerprint_on_complete,
        overlay_pos=(1325, 735),  # center of the door handle hotspot
        revert_scene="bg_car_exterior",
    )

    ## Can - three independent options.
    can_print_process = EvidenceProcess(
        "can_print",
        steps=["Magnetic Powder", "Scalebar", "Tape", "Backing Card", "Evidence Bag", "Tamper Evident Tape"],
        step_messages={
            "Magnetic Powder": "Powder applied to the can.",
            "Scalebar": "Scalebar placed.",
            "Tape": "Print lifted.",
            "Backing Card": "Backing card placed.",
        },
        bag_item_image="backing fingerprint",   # TODO: swap for a can-print backing image if you have one
        bag_drag_name="can_print",
        on_complete=_can_print_on_complete,
        overlay_pos=(1120, 885),  # center of the soda can hotspot
        revert_scene="bg_car_interior",
    )

    can_dna_process = EvidenceProcess(
        "can_dna",
        steps=["Swab Pack", "Tube", "Evidence Bag", "Tamper Evident Tape"],
        step_messages={
            "Swab Pack": "Can swabbed.",
            "Tube": "Swab secured in tube.",
        },
        bag_item_image="sample test tube",
        bag_drag_name="can_dna",
        on_complete=_can_dna_on_complete,
        overlay_pos=(1120, 885),  # center of the soda can hotspot
    )

    can_whole_process = EvidenceProcess(
        "can_whole",
        steps=["Evidence Bag", "Tamper Evident Tape"],
        bag_item_image=" soda-tp",
        bag_drag_name="can",
        on_complete=_can_whole_on_complete,
    )

    ## Wheel - two independent options.
    wheel_print_process = EvidenceProcess(
        "wheel_print",
        steps=["Magnetic Powder", "Scalebar", "Tape", "Backing Card", "Evidence Bag", "Tamper Evident Tape"],
        step_messages={
            "Magnetic Powder": "Powder applied to the wheel.",
            "Scalebar": "Scalebar placed.",
            "Tape": "Print lifted.",
            "Backing Card": "Backing card placed.",
        },
        bag_item_image="backing fingerprint",   # TODO: swap for a wheel-print backing image if you have one
        bag_drag_name="wheel_print",
        on_complete=_wheel_print_on_complete,
        overlay_pos=(325, 515),  # center of the steering wheel hotspot
        revert_scene="bg_car_interior",
    )

    wheel_dna_process = EvidenceProcess(
        "wheel_dna",
        steps=["Swab Pack", "Tube", "Evidence Bag", "Tamper Evident Tape"],
        step_messages={
            "Swab Pack": "Step 1/4: Area swabbed.",
            "Tube": "Step 2/4: Swab in tube.",
        },
        bag_item_image="sample test tube",
        bag_drag_name="wheel_dna",
        on_complete=_wheel_dna_on_complete,
        overlay_pos=(325, 515),  # center of the steering wheel hotspot
    )

    active_process = None
    did_can = False        # True only once the can is physically collected whole (bg swap)
    can_done = False       # True once the player clicks "Move on" for the can, regardless of method
    wheel_done = False     # True once the player clicks "Move on" for the wheel, regardless of method
    visited_can = False
    visited_wheel = False