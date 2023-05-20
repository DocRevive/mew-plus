# Up-to-date with 3.1.0
# Created by Revive#8798

config_name = "config_default" # name of mew+ config file WITHOUT .py
theme_enabled = True # set to False if themes are taking too long to load
# If you disable themes, you can still use everything, including restart & bot, except for theme
debug_mode = False

from discord.ext import commands
from datetime import datetime
from io import StringIO
import subprocess
import threading
import importlib
import rgbprint
import colorama
import requests
import discord
import time
import json
import sys
import os
import re

colorama.just_fix_windows_console()
os.environ["PYTHONUNBUFFERED"] = "x"
color_regex = re.compile(r"\x1B.*?m")
line_regex = re.compile(r"(?<!\x1b)\[(.*?)\]\[(.*?)\]", flags=re.MULTILINE)
block_regex = re.compile(r"(?<!\x1b)\[\[\[(.*?)\]\]\]\[(.*?)\]", flags=re.DOTALL)
frame_placeholder_regex = re.compile(r"\[\|\[\(.*?\)\]\|\]", flags=re.DOTALL)
os_clear = "cls" if os.name == "nt" else "clear"

config = importlib.import_module(config_name)
color_props = getattr(config, "color_props", {})

print_cache = {}
name_to_num = {}
kill_trigger = False
user_id = getattr(config, "roblox_id", None)

restarts = {
    "count": 0,
    "trigger": False,
    "reason": ""
}

serials = {
    "last_bought_needs_update": False,
    "update_trigger": False,
    "last_updated": False,
    "error": None,
    "status": None,
    "inventory_cache": []
}

type_to_id = {
    "Hat": 8,
    "HairAccessory": 41,
    "FaceAccessory": 42,
    "NeckAccessory": 43,
    "ShoulderAccessory": 44,
    "FrontAccessory": 45,
    "BackAccessory": 46,
    "WaistAccessory": 47,
    "TShirtAccessory": 64,
    "ShirtAccessory": 65,
    "PantsAccessory": 66,
    "JacketAccessory": 67,
    "SweaterAccessory": 68,
    "ShortsAccessory": 69,
}

types = ",".join(list(type_to_id.keys()))

with open("settings.json", "r") as file:
    settings = json.load(file)

os.system(os_clear)
print("Contribute: https://github.com/DocRevive/mew-plus")

def enforce_length(str, length):
    int_length = int(length)
    if int_length != int_length: return str
    if len(str) == int_length:
        return str
    elif len(str) > int_length:
        return str[:int_length]
    else:
        return str.ljust(int_length)

processing_funcs = {
    "length": enforce_length
}

def generate_view(data):
    result = getattr(config, "template", "")
    for prop in data:
        result = re.sub(r"\{\{" + prop + r"\}\}", str(data[prop]), result)

    regex_list = [line_regex, block_regex]
    output = StringIO()
    real_stdout = sys.stdout
    sys.stdout = output

    for regex in regex_list:
        curr_match = re.search(regex, result)
        while curr_match != None:
            if curr_match[0] in print_cache:
                str_output = print_cache[curr_match[0]]["replacement"]
                print_cache[curr_match[0]]["last_use"] = data["Run Time"]
            else:
                content = curr_match[1]
                args = re.split(r"\|", curr_match[2])
                color_prop = args[0]

                if color_prop not in color_props: break
                prop_data = color_props[color_prop]

                preprocess = []
                if len(args) > 1:
                    for arg in args:
                        parts = re.split("=", arg, 1)
                        if len(parts) != 2: continue
                        if parts[0] in processing_funcs:
                            preprocess.append(lambda str : processing_funcs["length"](str, parts[1]))
                
                for fxn in preprocess:
                    content = fxn(content)

                if prop_data["function"] == "rgbprint": values = [content]
                else: values = [*content]

                start_offset = output.tell()
                animated = False
                if prop_data["function"] == "gradient_change" or prop_data["function"] == "gradient_scroll":
                    prop_data["options"]["delay"] = 0
                    prop_data["options"]["times"] = 1
                    animated = True
                getattr(rgbprint, prop_data["function"])(*values, **prop_data["options"], sep="", end="")

                output.seek(start_offset)
                str_output = output.read()

                if animated:
                    frames = str_output.split("\r")
                    str_output = curr_match[0]
                    print_cache[curr_match[0]] = {
                        "replacement": f"[|[({frames[0]})]|]",
                        "frames": frames,
                        "current_frame": 0,
                        "last_use": data["Run Time"],
                        "rate": prop_data["rate_multiplier"]
                    }
                else:
                    print_cache[curr_match[0]] = {
                        "replacement": str_output,
                        "last_use": data["Run Time"]
                    }
            result = re.sub(regex, str_output, result, 1)
            curr_match = re.search(regex, result)
    sys.stdout = real_stdout
    return result

def update_frames(precursor):
    result = precursor
    curr_match = re.findall(frame_placeholder_regex, precursor)
    
    if len(curr_match) == 0: return False
    keys = list(print_cache.keys())
    for key in keys:
        data = print_cache[key]
        temp = data["replacement"]
        if temp in curr_match:
            result = re.sub(re.escape(temp), data["frames"][int(data["current_frame"])] + "\033[0m", result, 1)
            data["current_frame"] += data["rate"]
            if data["current_frame"] >= len(data["frames"]):
                data["current_frame"] %= len(data["frames"])
            curr_match.remove(temp)

    return result

def fill_block(text):
    justified = ""
    maxlen = 0
    lines = text.split("\n")
    lines_norm = re.sub(color_regex, "", text).split("\n")

    for line in lines_norm:
        if len(line) > maxlen: maxlen = len(line)
    for i in range(len(lines)):
        justified += lines[i] + " " * (maxlen - len(lines_norm[i])) + "\n"
    return justified

def update_settings(new_data):
    try:
        with open("settings.json", "r+") as file:
            file.seek(0)
            json.dump(new_data, file, indent=4)
            file.truncate()
        return True
    except Exception as e:
        return (False, str(e))

def get_request(url, timeout=4, cursor=None):
    try:
        response = requests.get(url if cursor == None else url + f"&cursor={cursor}", timeout=timeout,
                                cookies={ ".ROBLOSECURITY": settings["MAIN_COOKIE"]})
    except Exception as e:
        serials["error"] = str(e)
        print("Couldn't update inventory:", serials["error"])
        return False
    
    serials["error"] = None
    return response.json()

def update_serial_status(message, print_msg):
    if print_msg: print(message)
    serials["status"] = message

def populate_inventory_cache(wait=2, max_retry=3, print=False):
    overall_inv_url = f"https://inventory.roblox.com/v2/users/{user_id}/inventory?assetTypes={types}&filterDisapprovedAssets=false&limit=100&sortOrder=Desc"
    type_to_oldest = {}
    item_counts = {}
    cursor = None
    retry_count = 0

    if len(serials["inventory_cache"]) == 0:
        count = 0
        iters = int(getattr(config, "cache_num", 100) / 100)
        update_serial_status(f"Populating cache with the last {iters * 100} inventory items", print)

        while count < iters:
            response = get_request(overall_inv_url, cursor=cursor)
            time.sleep(wait)
            if not response:
                retry_count += 1
                if retry_count <= max_retry:
                    update_serial_status(serials["error"] + ". Retrying", print)
                    continue
                else:
                    update_serial_status("Too many retries", print)
                    return False
            cursor = response["nextPageCursor"]
            data = response["data"]

            for item in data:
                this_seconds = datetime.fromisoformat(item["created"]).timestamp()
                type_name = item["assetType"]
                asset_id = item["assetId"]

                if asset_id in item_counts: item_counts[asset_id] += 1
                else: item_counts[asset_id] = 1
                if type_name not in type_to_oldest or this_seconds < type_to_oldest[type_name][0]:
                    type_to_oldest[type_name] = [this_seconds, asset_id]

            count += 1
            if cursor == None: break
    else:
        resolved = False
        update_serial_status("Updating inventory cache with new items", print)

        while not resolved:
            response = get_request(overall_inv_url, cursor=cursor)
            time.sleep(wait)
            if not response:
                retry_count += 1
                if retry_count <= max_retry:
                    update_serial_status(serials["error"] + ". Retrying", print)
                    continue
                else:
                    update_serial_status("Too many retries", print)
                    return False
            current_recent = serials["inventory_cache"][0]["created_timestamp"]
            cursor = response["nextPageCursor"]
            data = response["data"]

            for item in data:
                this_seconds = datetime.fromisoformat(item["created"]).timestamp()
                if this_seconds <= current_recent:
                    resolved = True
                    break
                type_name = item["assetType"]
                asset_id = item["assetId"]

                if asset_id in item_counts: item_counts[asset_id] += 1
                else: item_counts[asset_id] = 1
                if type_name not in type_to_oldest or this_seconds < type_to_oldest[type_name][0]:
                    type_to_oldest[type_name] = [this_seconds, asset_id]

            if cursor == None: resolved = True
    
    to_add = []
    for type_name, oldest in type_to_oldest.items():
        type_id = type_to_id[type_name]
        url = f"https://inventory.roblox.com/v2/users/{user_id}/inventory/{type_id}?limit=100&sortOrder=Desc"
        cursor = None
        resolved = False
        retry_count = 0
        update_serial_status(f"Getting new {type_name}", print)

        while not resolved:
            response = get_request(url, cursor=cursor)
            time.sleep(wait)
            if not response:
                retry_count += 1
                if retry_count <= max_retry:
                    update_serial_status(serials["error"] + ". Retrying", print)
                    continue
                else:
                    update_serial_status("Too many retries", print)
                    return False
            cursor = response["nextPageCursor"]
            data = response["data"]
            curr_count = 0
            end_count = item_counts[oldest[1]]

            for item in data:
                this_seconds = datetime.fromisoformat(item["created"]).timestamp()
                serial = item["serialNumber"] if "serialNumber" in item else "none"
                if item["assetId"] == oldest[1]:
                    curr_count += 1
                    if curr_count == end_count:
                        resolved = True
                        break
                if item["collectibleItemId"] != None:
                    to_add.append({
                            "asset_id": item["assetId"],
                            "asset_name": item["assetName"],
                            "serial": serial,
                            "created_timestamp": this_seconds
                        })

            if cursor == None: resolved = True

    to_add.sort(key=lambda obj : obj["created_timestamp"], reverse=True)
    serials["inventory_cache"] = to_add + serials["inventory_cache"]

    update_serial_status("Finished updating", print)
    serials["last_updated"] = time.time()
    return True

def list_add(list, new):
    added = []
    not_added = []
    already_added = []

    for id in new:
        id_int = 0
        if id.isnumeric():
            id_int = int(id)
            if id_int in list:
                already_added.append(id)
            else:
                list.append(id_int)
                added.append(id)
        else: not_added.append(id)
    
    result = ""
    if len(added) > 0: result += "Added `" + "`, `".join(added) + "`. "
    if len(already_added) > 0: result += "Already watching `" + "`, `".join(already_added) + "`. "
    if len(not_added) > 0: result += "Couldn't add `" + "`, `".join(not_added) + "`."
    if result == "": result = "Nothing happened."
    elif len(added) > 0: result += "Use !restart to put changes into effect"
    return result

def list_remove(list, remove):
    removed = []
    not_removed = []
    not_watching = []

    for id in remove:
        id_int = 0
        if id.isnumeric():
            id_int = int(id)
            if id_int in list:
                list.remove(id_int)
                removed.append(id)
            else:
                not_watching.append(id)
        else: not_removed.append(id)
    
    result = ""
    if len(removed) > 0: result += "Removed `" + "`, `".join(removed) + "`. "
    if len(not_watching) > 0: result += "Wasn't watching `" + "`, `".join(not_watching) + "`. "
    if len(not_removed) > 0: result += "Couldn't remove `" + "`, `".join(not_removed) + "`. "
    if result == "": result = "Nothing happened."
    elif len(removed) > 0: result += "Use !restart to put changes into effect"
    return result

def user_can_use_bot(user):
    whitelist = getattr(config, "allowed_users", [])
    return str(user.id) in whitelist or str(user) in whitelist

def bot_login(token, ready_event):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=getattr(config, "bot_prefix", "!"),
                       intents=intents)

    @bot.event
    async def on_ready():
        ready_event.set()

    @bot.command(
        brief="Shows status and metrics",
        help="Sends an embed with program status and metrics. Use '!stats all' to show more data."
    )
    async def stats(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        if "Watching" not in name_to_num and theme_enabled:
            await ctx.reply("Still starting up...")
            return
        
        all = False
        color = getattr(config, "embed_color", 0xf7b8cf)
        if len(args) > 0: all = args[0].lower() == "all"
        embed = discord.Embed(title="Mewt Sniper Stats", color=color)
        embed.set_footer(text="mew+")
        
        if not theme_enabled:
            embed.description = "Theme disabled, metrics reduced."
            embed.add_field(name="Restarts", value=str(name_to_num["Restarts"]))
        elif all:
            embed.description = "\n".join(map(lambda pair : f"**{pair[0]}**: `{pair[1]}`", list(name_to_num.items())))
        else:
            embed.add_field(name="Local Thread", value=f"**Errors**: `{name_to_num['Errors']}`\n" +
                                                       f"**Latency**: `{name_to_num['Latency']}`\n" +
                                                       f"**Checks**: `{name_to_num['Checks']}`\n" +
                                                       f"**Restarts**: `{name_to_num['Restarts']}`")
            embed.add_field(name="Bought", value=f"`{name_to_num['Bought']}`")

        await ctx.reply(embed=embed)

    @bot.command(
        brief="Lists your limiteds and serials",
        help="Lists main account's limiteds and their serials, recent first. Updates automatically whenever mewt is buying something. Manually update with !updateinv. !inventory <page number> to go to a certain page, e.g. !inventory 2"
    )
    async def inventory(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        cache = serials["inventory_cache"]
        if not user_id:
            await ctx.reply("You need to set roblox_id in the config file you're using.")
            return
        if len(cache) == 0:
            await ctx.reply("Still starting up...")
            return

        color = getattr(config, "embed_color", 0xf7b8cf)
        page = 1
        max_page = (len(cache) / 10).__ceil__()
        if len(args) > 0:
            if not args[0].isnumeric():
                await ctx.reply("Page must be a number.")
                return
            if int(args[0]) > max_page:
                await ctx.reply(f"Currently, the last page is {max_page}")
                return
            page = int(args[0])
        embed = discord.Embed(title="Limited Inventory", color=color)
        embed.set_footer(text=f"mew+ | Page {page}/{max_page}")

        desc = f"Total cached: {len(cache)}\n"
        if serials["last_bought_needs_update"] != False or serials["update_trigger"]:
            if serials["last_bought_needs_update"] != False: desc += f"Items bought <t:{int(serials['last_bought_needs_update'])}:R>, awaiting update...\n"
            elif serials["update_trigger"]: desc += "Update triggered, awaiting update...\n"
            desc += f"Status: {serials['status']}\n"
            desc += f"Errors: {serials['error'] if serials['error'] != None else 'none'}\n"
        desc += f"Last updated: <t:{int(serials['last_updated'])}:R>\n\n"
        
        page_list = cache[(page - 1) * 10 : page * 10]
        for item in page_list:
            desc += f"[{item['asset_name']}](https://roblox.com/catalog/{item['asset_id']})\n"
            desc += f"`#{item['serial']}` | <t:{int(item['created_timestamp'])}:R>\n\n"

        embed.description = desc[:4000]

        await ctx.reply(embed=embed)

    @bot.command(
        brief="Inventory already auto-updates, but you can use this too"
    )
    async def updateinv(ctx):
        if not user_can_use_bot(ctx.message.author): return
        if serials["update_trigger"] or serials["last_bought_needs_update"]:
            await ctx.reply("Update already underway!")
            return    
        await ctx.reply("Starting update. Monitor progress with the inventory command")
        serials["update_trigger"] = True

    @bot.command(
        brief="Starts watching ID(s)",
        help="Starts watching space-separated IDs"
    )
    async def add(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        message = list_add(settings["ITEMS"], args)
        status = update_settings(settings)
        if status: await ctx.reply(message)
        else: await ctx.reply("Error! " + status[1])

    @bot.command(
        brief="Stops watching ID(s)",
        help="Stops watching space-separated IDs"
    )
    async def remove(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        message = list_remove(settings["ITEMS"], args)
        status = update_settings(settings)
        if status: await ctx.reply(message)
        else: await ctx.reply("Error! " + status[1])
        
    @bot.command(
        brief="Blacklists ID(s)",
        help="Blacklists space-separated IDs"
    )
    async def addbl(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        message = list_add(settings["BLACKLIST"], args)
        status = update_settings(settings)
        if status: await ctx.reply(message)
        else: await ctx.reply("Error! " + status[1])

    @bot.command(
        brief="Un-blacklists ID(s)",
        help="Un-blacklists space-separated IDs"
    )
    async def removebl(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        message = list_remove(settings["BLACKLIST"], args)
        status = update_settings(settings)
        if status: await ctx.reply(message)
        else: await ctx.reply("Error! " + status[1])
        
    @bot.command(
        brief="Shows the list of item IDs",
        help="Sends a comma-separated list of currently watched item IDs"
    )
    async def watching(ctx):
        if not user_can_use_bot(ctx.message.author): return
        if len(settings["ITEMS"]) == 0:
            await ctx.reply("No items watched")
            return
        await ctx.reply(", ".join(map(str, settings["ITEMS"])))

    @bot.command(
        brief="Restarts the program",
        help="Restarts the program and indicates success or failure"
    )
    async def restart(ctx):
        if not user_can_use_bot(ctx.message.author): return
        msg = await ctx.reply("Restarting...")
        restarts["trigger"] = True
        for _ in range(100):
            time.sleep(0.5)
            if not restarts["trigger"]:
                await msg.edit(content="Restarted!")
                return
        await msg.edit(content="Couldn't detect restart after 50 seconds.")

    @bot.command(
        brief="View or change speed",
        help="To view, use without arguments. To change to 0.9, for example, use '!speed 0.9'"
    )
    async def speed(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        if len(args) == 0:
            await ctx.reply(str(settings["MISC"]["SCAN_SPEED"]))
        else:
            if "".join(args[0].split(".", 1)).isnumeric():
                settings["MISC"]["SCAN_SPEED"] = float(args[0])
                status = update_settings(settings)
                if status: await ctx.reply(f"Speed set to {args[0]}. Use !restart to put changes into effect")
                else: await ctx.reply("Could not update settings.json! " + status[1])
            else:
                await ctx.reply("Argument must be a number.")

    @bot.command(
        brief="View or change whether to buy only free",
        help="To view, use without arguments. To change to 'false' (to buy watched paid items), use '!buyonlyfree false'"
    )
    async def buyonlyfree(ctx, *args):
        if not user_can_use_bot(ctx.message.author): return
        if len(args) == 0:
            await ctx.reply(str(settings["MISC"]["BUY_ONLY_FREE"]))
        else:
            lower = args[0].lower()
            if lower == "false" or lower == "no":
                setting = False
            elif lower == "true" or lower == "yes":
                setting = True
            else:
                await ctx.reply("Try using 'true' or 'false'")
                return

            settings["MISC"]["BUY_ONLY_FREE"] = setting

            status = update_settings(settings)
            if status:
                if setting: await ctx.reply(f"Set to 'true', meaning only free items can be bought. Use !restart to put changes into effect")
                else: await ctx.reply(f"Set to 'false', meaning paid items can be bought. Use !restart to put changes into effect")
            else: await ctx.reply("Could not update settings.json! " + status[1])
    
    bot.run(token)

class FrameThread(threading.Thread):
    def __init__(self):
        super(FrameThread, self).__init__()
        self.daemon = True
        self.view = None
        self.current_frame = None
        self.in_progress = False
        self.anim_enabled = True

    def run(self): # Only for animated
        while True:
            if kill_trigger: break
            if self.view == None: continue
            self.in_progress = True
            view_frame = update_frames(self.view)
            if view_frame == False:
                self.anim_enabled = False
                self.in_progress = False
                self.print(self.view)
                break
            time.sleep(1 / getattr(config, "fps", 5))
            self.print(view_frame)
            self.current_frame = view_frame
            self.in_progress = False
    
    def print(self, text, row=1, col=1):
        if text == None: return
        if not debug_mode: print(f"\x1b[{row};{col}H")
        print(fill_block(text))

    def set_view(self, view, clear_cache=False, data=None):
        if clear_cache:
            self.view = None
            attempts = 0
            while self.in_progress:
                time.sleep(0.05)
                attempts += 1
                if attempts > 100: return
            keys = list(print_cache.keys())
            for key in keys:
                if print_cache[key]["last_use"] != data["Run Time"]:
                    del print_cache[key]
        if not self.anim_enabled: self.print(view)
        self.view = view

    def send_clear(self):
        os.system(os_clear)
        if self.anim_enabled: self.print(self.current_frame)
        else: self.print(self.view)

def start_mewt():
    stdout = subprocess.PIPE if theme_enabled else sys.stdout
    return subprocess.Popen([sys.executable, "-u", "main.py"], stdout=stdout, universal_newlines=True, bufsize=1)

def check_restart(current_time):
    if restarts["trigger"] or kill_trigger:
        restarts["reason"] = "Bot command"
        print("Restart triggered")
        return True

    elapsed_secs = current_time - start_time
    if mpr > 0 and elapsed_secs > mpr * 60:
        restarts["reason"] = f"Restart every {mpr} minutes"
        return True
    
    return False

def check_inventory_loop():
    while True:
        if not serials["last_bought_needs_update"] and not serials["update_trigger"]: continue
        if time.time() - serials["last_bought_needs_update"] > 5 or serials["update_trigger"]:
            populate_inventory_cache()
            serials["last_bought_needs_update"] = False
            serials["update_trigger"] = False
        time.sleep(0.5)

try:
    token = getattr(config, "bot_token", False)
    frame_thread = FrameThread()

    if token:
        ready_event = threading.Event()
        bot_thread = threading.Thread(target=bot_login, args=[token, ready_event], daemon=True)
        print("Logging into bot...")
        bot_thread.start()
        ready_event.wait()
        print("Logged in!")

    if not theme_enabled: print("Theme disabled. Some features are not available.")
    if not user_id: print("Roblox ID not set; !serials command not available")
    else:
        print("Fetching inventory data, please wait...")
        populate_inventory_cache(wait=1, max_retry=8, print=True)
        serials_thread = threading.Thread(target=check_inventory_loop, daemon=True)
        serials_thread.start()

    print("Starting Mew+, please wait...")
    mpr = getattr(config, "minutes_per_restart", -1)
    process = start_mewt()
    frame_thread.start()
except (KeyboardInterrupt, SystemExit):
    print("Exiting")
    sys.exit(1)

while True:
    start_time = time.time()
    view_updates_since_clear = 0
    restarts["trigger"] = False
    webhook = getattr(config, "restart_webhook", False)
    webhook_color = getattr(config, "webhook_color", 0xf7b8cf)
    stage = 0

    try:
        name_to_num = { "Restarts": restarts["count"] }
        if theme_enabled:
            process.stdout.flush()
            for line in process.stdout:
                if debug_mode:
                    print(line)
                    continue
                current_time = time.time()
                if check_restart(current_time): break
                if line == None: continue
                if stage == 0:
                    os.system(os_clear)
                    print("Startup may take up to 3 minutes on some systems. Set theme_enabled to False in main_plus.py if this takes too long.")
                    stage = 1

                utf_line = line.rstrip()
                cleaned_line = re.sub(color_regex, "", utf_line)

                if len(cleaned_line) != 0:
                    if "Buying" in cleaned_line:
                        print(cleaned_line)
                        serials["last_bought_needs_update"] = current_time
                        continue
                    if ":" in cleaned_line:
                        split = re.split(r"> |: ", cleaned_line)
                        if len(split) == 3: name_to_num[split[1]] = split[2]
                    if "Current User" in cleaned_line: continue
                    if "Watching" in cleaned_line:
                        if stage == 1:
                            stage = 2
                            os.system(os_clear)
                        view_precursor = generate_view(name_to_num)
                        view_updates_since_clear += 1
                        if view_updates_since_clear > 15:
                            frame_thread.set_view(view_precursor, True, data=name_to_num)
                            frame_thread.send_clear()
                            view_updates_since_clear = 0
                        else: frame_thread.set_view(view_precursor, False)
            process.stdout.close()
        else:
            while True:
                current_time = time.time()
                if check_restart(current_time): break
                time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        kill_trigger = True
        print("Exiting")
    except ModuleNotFoundError:
        print("Please run manually: pip install requests colorama pyarmor python-socketio[client]")
        os.system("pause")
    except Exception as e:
        print(e)
        restarts["reason"] = str(e)
        pass

    process.kill()
    if kill_trigger: break

    restarts["count"] += 1
    
    if webhook:
        print("Sending webhook")
        try:
            requests.post(webhook, timeout=4, json={"content": None, "embeds": [{
                "color": webhook_color,
                "title": "Mewt restarted",
                "fields": [ {"name": "Reason", "value": restarts["reason"], "inline": True},
                        {"name": "Restart count", "value": restarts["count"], "inline": True} ],
                "footer": { "text": "mew+" }
            }]})
        except Exception as e:
            print("Couldn't send webhook:", e)
    print("Restarting")
    process = start_mewt()
    continue
