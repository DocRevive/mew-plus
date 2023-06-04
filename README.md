## You must have a main.py file and a settings.json format up-to-date with version 4.0.0!

# mew-plus
An efficient, robust, feature-packed, practical, creative, and customizable overhaul of mewt.

Personal use and modification is permitted. Publication rights of components are reserved.

Features:
- !inventory command that lists items, serials, and dates
- Autorestart, crash detector, and webhook support
- !restart command and a bot functionality overhaul
- View more metrics in !stats like run time and restarts
- Edit normal configuration settings through the bot 
- Solid colors, gradients, moving (animated) gradients
- Fully customizable themes
- Customize bot embeds
- Terminates with Ctrl+C
- No more screen flicker

## Dependencies
Nothing other than mewt dependencies

## Commands
```
add                   Starts watching ID(s)
addbl                 Blacklists ID(s)
addcreators           Adds IDs to autosearch creator whitelist
auto_buypaid_enabled  View or change whether autosearch 'buy paid' is enabled
auto_buypaid_maxprice View or change autosearch buy paid max price
auto_buypaid_maxstock View or change autosearch buy paid max stock (to buy)
help                  Shows this message
inventory             Lists your limiteds and serials
remove                Stops watching ID(s)
removebl              Un-blacklists ID(s)
removecreators        Removes IDs from autosearch creator whitelist
restart               Restarts the program
speed                 View or change speed
stats                 Shows status and metrics
stats all             Shows all data
updateinv             Inventory already auto-updates, but you can use this too
watcher_onlyfree      View or change whether to buy only free
watching              Shows the list of item IDs
```

## Setup
1. Move all files into the mewt folder
2. Use `start_plus.bat` instead of `start.bat`
3. Copy/edit `config_default.py` and follow the instructions inside
4. If you use a theme other than config_default, edit the top of `main_plus.py`

## Examples

config_neon

![config_neon](https://i.imgur.com/xc2181Z.png)

config_box

![config_box](https://i.imgur.com/QEamrqI.png)

config_hex

![config_hex](https://i.imgur.com/SC9AzUL.png)

config_default

![config_default](https://i.imgur.com/qFIiQJK.png)

Go to `config_default.py` and make your own!

