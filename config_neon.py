# Up-to-date with 3.5.1
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
                                  _____ 
        _______ ___________      ___  /_
        __  __ `__ \  _ \_ | /| / /  __/
        _  / / / / /  __/_ |/ |/ // /_  
        /_/ /_/ /_/\___/____/|__/ \__/  
                                


              discord.gg/mewt - v3.1.0
             github.com/DocRevive/mew-plus]]][neon_scroll]
            [═══════════════════════════════][gray]
           [Current User:][main_gradient] [{{Current User}}][pink]
          [Bought:][main_gradient] [{{Bought}}][pink]
         [Autosearch:][main_gradient] [{{Autosearch}}][pink]
        [═══════════════════════════════][gray]
       [Errors:][main_gradient] [{{Errors}}][pink]           
      [Latency:][main_gradient] [{{Latency}}][pink]
     [Checks:][main_gradient] [{{Checks}}][pink]
    [═══════════════════════════════][gray]
   [Restarts:][main_gradient] [{{Restarts}}][pink]
  [Run Time:][main_gradient] [{{Run Time}}][pink]
 [Watching:][main_gradient] [{{Watching}}][pink]
""" # Template ends with the line above
