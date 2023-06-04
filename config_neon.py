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
embed_color = 0xA653F5  # 0x and then hex color value
bot_prefix = "!"        # Goes before every command
cache_num = 100         # A multiple of 100; number of inventory acccessories to fetch initially. Not necessarily number of limiteds.

# Roblox-provided times may be a few hours behind or ahead. Use time_offset_minutes if you find that recent !inventory item dates are off.
# Use a positive number if the current times are some number of minutes behind, and a negative number if the current times are ahead.
time_offset_minutes = 60

# Webhook to notify you, with a reason, when the bot restarts. (Optional)
restart_webhook = ""
webhook_color = 0xA653F5

# You can edit color_props.
# All of the possible effects (called "function") are demonstrated below.
# - Functions: rgbprint, gradient_print, gradient_scroll, gradient_change
# Color values are (r, g, b).
color_props = {
    "pink": { # rgbprint (solid color) example
        "function": "rgbprint",
        "options": {
            "color": (251, 146, 251)
        }
    },
    "gray": {
        "function": "rgbprint",
        "options": {
            "color": (50, 50, 50)
        }
    },
    "main_gradient": { # gradient_print example
        "function": "gradient_print",
        "options": {
            "start_color": (143, 140, 242),
            "end_color": (101, 184, 191)
        }
    },
    "neon_scroll": { # gradient_scroll/gradient_change example
        "function": "gradient_scroll", # (for gradient_change, only 'function' changes)
        "rate_multiplier": 20, # NOT IN 'options'. multiplier > 1 means faster scroll/change
        "options": {
            "start_color": (166, 83, 245),
            "end_color": (249, 108, 255),
            "reverse": False
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
                                  _____ 
        _______ ___________      ___  /_
        __  __ `__ \  _ \_ | /| / /  __/
        _  / / / / /  __/_ |/ |/ // /_  
        /_/ /_/ /_/\___/____/|__/ \__/  
                                


                discord.gg/mewt - v{{Version}}
               github.com/DocRevive/mew-plus]]][color=neon_scroll]
              [═══════════════════════════════][color=gray]
             [Current User:][color=main_gradient] [{{Current User}}][color=pink]
            [Online Users:][color=main_gradient] [{{Online Users}}][color=pink]
           [Bought:][color=main_gradient] [{{Bought}}][color=pink]
          [Last Bought:][color=main_gradient] [{{Last Bought}}][color=pink]
         [Autosearch:][color=main_gradient] [{{Connected}}][color=pink]
        [═══════════════════════════════][color=gray]
       [Errors:][color=main_gradient] [{{Errors}}][color=pink]           
      [Latency:][color=main_gradient] [{{Latency}}][color=pink]
     [Checks:][color=main_gradient] [{{Checks}}][color=pink]
    [═══════════════════════════════][color=gray]
   [Restarts:][color=main_gradient] [{{Restarts}}][color=pink]
  [Run Time:][color=main_gradient] [{{Run Time}}][color=pink]
 [Watching:][color=main_gradient] [{{Watching}}][color=pink]
""" # Template ends with the line above
