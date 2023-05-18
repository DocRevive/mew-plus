# Up-to-date with 3.1.0
# Created by Revive#8798

# If minutes_per_restart is positive, the program will periodically restart every  
# minutes_per_restart minutes. If this is negative, it will not deliberately restart.
# Crash prevention is always enabled.
minutes_per_restart = 30

# If you put your bot's token here to customize bot messages, you must NOT put the
# token in settings.json. (All optional)
bot_token = ""
embed_color = 0xf7b8cf # 0x and then hex color value
allowed_users = [""] # Put the IDs or tags of the users (including you) who should be able to use the bot
bot_prefix = "!"

# Webhook to notify you, with a reason, when the bot restarts. (Optional)
restart_webhook = ""
webhook_color = 0xf7b8cf

# You can edit color_props.
# All of the possible effects (called "function") are demonstrated below.
# - Functions: rgbprint, gradient_print, gradient_scroll, gradient_change
# Color values are (r, g, b).
color_props = {
    "one_color": { # rgbprint (solid color) example
        "function": "rgbprint",
        "options": {
            "color": (247, 184, 207) # You should only change this.
        }
    },
    "multi_color": { # gradient_print example
        "function": "gradient_print",
        "options": {
            "start_color": (255, 111, 163),
            "end_color": (247, 184, 207)
        }
    },
    "multi_color_scroll": { # gradient_scroll/gradient_change example
        "function": "gradient_scroll", # (for gradient_change, only 'function' changes)
        "rate_multiplier": 3, # NOT IN 'options'. multiplier > 1 means faster scroll/change
        "options": {
            "start_color": (50, 50, 50),
            "end_color": (255, 255, 255),
            "reverse": False
        }
    }
}

# FPS (frames per second) affects animation quality and speed, not the rate the numbers update.
fps = 5

# You can edit the template below.
# Single brackets enclose single-line color rules i.e. [ ... ][color_prop]
# Triple brackets enclose multi-line color rules i.e. [[[ ... ]]][color_prop]
# Do not put more color rules within the brackets of an animated rule (scroll/change)
# color_prop is a key from color_props above (e.g. one_color, multi_color)
# You can have just [color_prop] or also [color_prop|length=#], which means the actual length
#       will be enforced to # by either adding spaces or truncating excess characters
# Placeholders for metrics go in double curly braces i.e. {{...}}
# - Available metrics: Current User, Bought, Autosearch, Errors, Latency, Checks,
#                      Restarts, Run Time, Watching
# Design your whitespace as if the bracket notation doesn't exist. 
# Template starts on the line after the next line.
template = """[[[
                                            d8P
                                            d888888P
        88bd8b,d88b  d8888b ?88   d8P  d8P  ?88'
        88P'`?8P'?8b d8b_,dP d88  d8P' d8P'  88P
        d88  d88  88P 88b     ?8b ,88b ,88'   88b
        d88' d88'  88b `?888P' `?888P'888P'    `?8b
]]][multi_color]

                discord.gg/mewt - v3.1.0
             github.com/DocRevive/mew-plus


> Current User: [{{Current User}}][one_color]
> Bought: [{{Bought}}][one_color]
> Autosearch: [{{Autosearch}}][one_color]

>> Main
> Errors: [{{Errors}}][one_color]
> Latency: [{{Latency}}][one_color]
> Checks: [{{Checks}}][one_color]

> Restarts: [{{Restarts}}][one_color]
> Run Time: [{{Run Time}}][one_color]
> Watching: [{{Watching}}][one_color]
""" # Template ends with the line above
