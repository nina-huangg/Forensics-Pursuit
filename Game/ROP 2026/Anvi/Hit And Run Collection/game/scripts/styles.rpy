# init python:
    # style.dark_text = Style(style.default)
    # style.dark_text.color = "#555555"

    # # To-Do List
    # style.strikethrough_text = Style(style.dark_text)
    # style.strikethrough_text.strikethrough = True
    # style.strikethrough_text.color = "#888"

    # # Heading
    # style.heading_text = Style(style.dark_text)
    # style.heading_text.size = 30
    # style.heading_text.bold = True

    # Instructions
    # style.instructions_text = Style(style.dark_text)
    # style.instructions_text.size = 20
    # style.instructions_strikethrough_text = Style(style.dark_text)
    # style.instructions_strikethrough_text.strikethrough = True
    # style.instructions_strikethrough_text.color = "#888"
    # style.instructions_strikethrough_text.size = 20
style heading_text is default:
    color "#555555"
    size 30
    bold True

style instructions_text is default:
    color "#555555"
    size 20

style strikethrough_text is default:
    color "#888888"
    strikethrough True

style more_details_text is default:
    size 20
    color "#ffcc00"
    hover_color "#5c5c5c"