init -4 python:
    class ForwardOnlyValue(BarValue):
        """A bar bound to a store variable that can only be dragged up, never back down.

        Pouring is one-directional in real life — once the level reaches 160 the
        player shouldn't be able to drag it back to 150. Dragging past the value
        still works normally; dragging backward is simply ignored (use a Reset
        button to actually empty it).
        """

        def __init__(self, name, range, step=1):
            self.name = name
            self.range = range
            self.step = step

        def get_adjustment(self):
            current = getattr(store, self.name)
            return ui.adjustment(
                range=self.range,
                value=current,
                step=self.step,
                adjustable=True,
                changed=self.changed,
            )

        def changed(self, value):
            current = getattr(store, self.name)
            if value > current:
                setattr(store, self.name, value)
                renpy.restart_interaction()

        def get_style(self):
            return "bar", "vbar"

    def pour_increment(name, max_value, step=1):
        """Bump a pour-bar variable up by step (right-arrow key), clamped to max_value."""
        current = getattr(store, name)
        setattr(store, name, min(current + step, max_value))
        renpy.restart_interaction()

    style.strikethrough_text = Style(style.default)
    style.strikethrough_text.strikethrough = True
    style.strikethrough_text.color = "#888"

    style.heading_text = Style(style.default)
    style.heading_text.size = 30
    style.heading_text.bold = True

    style.instructions_text = Style(style.default)
    style.instructions_text.size = 20

    style.instructions_strikethrough_text = Style(style.default)
    style.instructions_strikethrough_text.strikethrough = True
    style.instructions_strikethrough_text.color = "#888"
    style.instructions_strikethrough_text.size = 20

style more_details_text is default:
    size 20
    color "#ffcc00"
    hover_color "#5c5c5c"

style lab_notebook_heading is default:
    size 26
    bold True
    color "#111111"

style lab_todo_text is default:
    size 21
    color "#111111"

style lab_todo_complete is lab_todo_text:
    color "#555555"
    strikethrough True

style lab_details_heading is default:
    size 25
    bold True
    color "#111111"

style lab_page_text is default:
    size 19
    color "#333333"

style lab_detail_text is default:
    size 19
    color "#111111"
    line_spacing 2

style lab_detail_complete is lab_detail_text:
    color "#555555"
    strikethrough True

style lab_page_button is button_text:
    size 20
    color "#111111"
    hover_color "#315f86"
    insensitive_color "#999999"

style lab_close_button is default:
    background "#f0c040"
    hover_background "#ffd666"
    padding (28, 14)
    xminimum 140

style lab_close_button_text is button_text:
    size 26
    bold True
    color "#1a1a1a"
    hover_color "#000000"
    text_align 0.5
    xalign 0.5

## Playful motion for the lab scene #############################################

transform lab_pop_in:
    zoom 0.6
    alpha 0.0
    ease 0.16 zoom 1.12 alpha 1.0
    ease 0.10 zoom 1.0

transform lab_notify_correct:
    on show:
        zoom 0.55
        rotate -8
        alpha 0.0
        ease 0.18 zoom 1.12 rotate 3 alpha 1.0
        ease 0.12 zoom 1.0 rotate 0
    on hide:
        ease 0.2 alpha 0.0 zoom 0.85

transform lab_notify_wrong:
    on show:
        xoffset 0
        alpha 0.0
        ease 0.05 alpha 1.0
        ease 0.05 xoffset -14
        ease 0.05 xoffset 12
        ease 0.05 xoffset -9
        ease 0.05 xoffset 6
        ease 0.05 xoffset 0
    on hide:
        ease 0.2 alpha 0.0

transform lab_wait_wobble:
    rotate -2
    linear 0.4 rotate 2
    linear 0.4 rotate -2
    repeat

transform lab_button_bounce:
    on hover:
        ease 0.12 zoom 1.06
    on idle:
        ease 0.12 zoom 1.0
