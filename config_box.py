# Up-to-date with 4.0.0
# Created by Revive#8798

# If minutes_per_restart is positive, the program will periodically restart every  
# minutes_per_restart minutes. If this is negative, it will not deliberately restart.
# Crash prevention is always enabled.
minutes_per_restart = 30

# If you put your bot's token here to customize bot messages, you must NOT put the
# token in settings.json. (All optional)
bot_token = ""
allowed_users = [""]    # Put the discord IDs or tags of the users (including you) who can use the bot
roblox_id = ""          # The roblox ID of your main account, corresponding with the first cookie in settings.json (For !serials command)
embed_color = 0xf7b8cf  # 0x and then hex color value
bot_prefix = "!"        # Goes before every command
cache_num = 100         # A multiple of 100; number of inventory acccessories to fetch initially. Not necessarily number of limiteds.

# Roblox-provided times may be a few hours behind or ahead. Use time_offset_minutes if you find that recent !inventory item dates are off.
# Use a positive number if the current times are some number of minutes behind, and a negative number if the current times are ahead.
time_offset_minutes = 60

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
    }
}

# FPS (frames per second) affects animation quality and speed, not the rate the numbers update.
fps = 20

# You can edit the template below.
# Single brackets enclose single-line color rules i.e. [ ... ][color=color_prop]
# Triple brackets enclose multi-line color rules i.e. [[[ ... ]]][color=color_prop]
# Do not put more color rules within the brackets of an animated rule (scroll/change)
# color_prop is a key from color_props above (e.g. one_color, multi_color)
# You can have just [color=color_prop] or:
#       [color=color_prop|length=#] - the actual length will be enforced to # by either adding spaces or truncating excess characters
#       [color=color_prop|length_centered=#] - the text will be centered within a total width of # (make this the
#                                              maximum width of the whole template including spaces on both ends)
#                                              (do not add your own whitespace on this line. the line will be formatted automatically)
#       Or just [length=#] or [length_centered=#]
# Placeholders for metrics go in double curly braces i.e. {{...}}
# - Available metrics: Version, Current User, Online Users, Bought, Last Bought, Connected (for autosearch),
#                      Errors, Latency, Checks, Restarts, Run Time, Watching
# Design your whitespace as if the bracket notation doesn't exist. 
# Template starts on the line after the next line.
template = """[[[
███╗   ███╗███████╗██╗    ██╗████████╗
████╗ ████║██╔════╝██║    ██║╚══██╔══╝
██╔████╔██║█████╗  ██║ █╗ ██║   ██║   
██║╚██╔╝██║██╔══╝  ██║███╗██║   ██║   
██║ ╚═╝ ██║███████╗╚███╔███╔╝   ██║   
╚═╝     ╚═╝╚══════╝ ╚══╝╚══╝    ╚═╝   

discord.gg/mewt - Version {{Version}}
github.com/DocRevive/mew-plus]]][color=multi_color|length_centered=63]
    ╔════════════════════════════════════════════════════╗
    ║ Current User: [{{Current User}}][color=one_color|length=11] Errors: [{{Errors}}][color=one_color|length=17]║
    ║ Online Users: [{{Online Users}}][color=one_color|length=11] Latency: [{{Latency}}][color=one_color|length=16]║
    ║ Bought: [{{Bought}}][color=one_color|length=17] Checks: [{{Checks}}][color=one_color|length=17]║
    ║ Last Bought: [{{Last Bought}}][color=one_color|length=12] Restarts: [{{Restarts}}][color=one_color|length=15]║
    ║ Autosearch: [{{Connected}}][color=one_color|length=13] Run Time: [{{Run Time}}][color=one_color|length=15]║
    ╚════════════════════════════════════════════════════╝

    ☆ Watching: [{{Watching}}][color=one_color]
""" # Template ends with the line above
