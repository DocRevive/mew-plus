# Up-to-date with 3.5.6
# Created by Revive#8798

# If minutes_per_restart is positive, the program will periodically restart every  
# minutes_per_restart minutes. If this is negative, it will not deliberately restart.
# Crash prevention is always enabled.
minutes_per_restart = 30

# If you put your bot's token here to customize bot messages, you must NOT put the
# token in settings.json. (All optional)
bot_token = ""
allowed_users = [""]    # Put the discord IDs or tags of the users (including you) who can use the bot
roblox_id = ""          # The roblox ID of your main account (for !serials command)
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
    "blue": { # rgbprint (solid color) example
        "function": "rgbprint",
        "options": {
            "color": (90, 121, 200)
        }
    },
    "multi_color": {
        "function": "gradient_print",
        "options": {
            "start_color": (90, 121, 200),
            "end_color": (147, 233, 190),
        }
    }
}

# FPS (frames per second) affects animation quality and speed, not the rate the numbers update.
fps = 30

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
# - Available metrics: Version, Current User, Online Users, Bought, Last Bought, Enabled (for autosearch),
#                      Errors, Latency, Checks, Restarts, Run Time, Watching
# Design your whitespace as if the bracket notation doesn't exist. 
# Template starts on the line after the next line.
template = """[[[
                                                                      
                      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                  ░░██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
                ░░██░░                        ▒▒██
              ░░██░░[Errors: {{Errors}}][length_centered=28]▓▓██
            ░░██░░[Latency: {{Latency}}][length_centered=32]▓▓██
            ██░░[Checks: {{Checks}}][length_centered=36]▓▓██
        ░░██░░[Autosearch: {{Enabled}}][length_centered=40]████
        ██░░[Current User: {{Current User}}][length_centered=44]████
      ██░░                                                ████
    ██░░                                                    ████
    ██[                          _ ][length_centered=54]░░██
    ██[  ___ __ _ _____      ___| |][length_centered=54]░░██
    ██[ / _ ' _` / _ \ \ /\ / |__ |][length_centered=54]░░██
    ██[| | | | | \__  \ V  V / _| |][length_centered=54]░░██
    ██[|_| |_| |_|___/ \_/\_/ |__/ ][length_centered=54]░░██
    ██                                                      ░░██
    ▓▓██                                                  ░░██░░
      ▓▓██                                                ██
        ▓▓██[Online Users: {{Online Users}}][length_centered=44]██░░
          ████[Run Time: {{Run Time}}][length_centered=40]██░░
            ████[Restarts: {{Restarts}}][length_centered=36]██░░
              ████[Bought: {{Bought}}][length_centered=32]██░░
                ████                            ██░░
                  ████  ░░░░░░░░░░░░░░░░░░░░  ██░░
                    ██████████████████████████░░
]]][color=multi_color]
Watching: [{{Watching}}][color=blue]
""" # Template ends with the line above
