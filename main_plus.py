# Up-to-date with 3.1.0
# Created by Revive#8798

theme_name = "theme_default" # name of python theme file WITHOUT .py
debug_mode = False

from discord.ext import commands
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

theme = importlib.import_module(theme_name)
color_props = getattr(theme, "color_props", {})

restarts = 0
print_cache = {}
name_to_num = {}
restart_trigger = False
kill_trigger = False

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
    result = getattr(theme, "template", "")
    for prop in data:
        result = re.sub(r"\{\{" + prop + r"\}\}", str(data[prop]), result)

    regex_list = [line_regex, block_regex]
    output = StringIO()
    real_stdout = sys.stdout
    sys.stdout = output

    for regex in regex_list:
        curr_match = re.search(regex, result)
        while curr_match != None:
            if curr_match[0] not in print_cache:
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
            else: 
                str_output = print_cache[curr_match[0]]["replacement"]
                print_cache[curr_match[0]]["last_use"] = data["Run Time"]
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
    else: result += "Use !restart to put changes into effect"
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
    else: result += "Use !restart to put changes into effect"
    return result

def user_can_use_bot(user):
    whitelist = getattr(theme, "allowed_users", [])
    return str(user.id) in whitelist or user.discriminator in whitelist

def bot_login(token, ready_event):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=getattr(theme, "bot_prefix", "!"),
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
        if "Watching" not in name_to_num:
            await ctx.reply("Still starting up...")
            return
        
        all = False
        color = getattr(theme, "embed_color", 0xf7b8cf)
        if len(args) > 0: all = args[0].lower() == "all"
        embed = discord.Embed(title="Mewt Sniper Stats", color=color)
        embed.set_footer(text="mew+")
        
        if all:
            embed.description = "\n".join(map(lambda pair : f"**{pair[0]}**: `{pair[1]}`", list(name_to_num.items())))
        else:
            embed.add_field(name="Local Thread", value=f"**Errors**: `{name_to_num['Errors']}`\n" +
                                                       f"**Latency**: `{name_to_num['Latency']}`\n" +
                                                       f"**Checks**: `{name_to_num['Checks']}`\n" +
                                                       f"**Restarts**: `{name_to_num['Restarts']}`")
            embed.add_field(name="Bought", value=f"`{name_to_num['Bought']}`")

        await ctx.reply(embed=embed)

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
        if "Watching" in name_to_num:
            await ctx.reply(", ".join(name_to_num["Watching"].split(", ")))
        else:
            await ctx.reply("Still starting up...")

    @bot.command(
        brief="Restarts the program",
        help="Restarts the program and indicates success or failure"
    )
    async def restart(ctx):
        global restart_trigger

        if not user_can_use_bot(ctx.message.author): return
        msg = await ctx.reply("Restarting...")
        restart_trigger = True
        for _ in range(100):
            time.sleep(0.5)
            if not restart_trigger:
                await msg.edit(content="Restarted!")
                return
        await msg.edit(content="Couldn't detect restart after 50 seconds.")

    @bot.command(
        brief="View or change speed",
        help="To view, use without arguments. To change to 0.9, for example, use '!speed 0.9'"
    )
    async def speed(ctx, *args):
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
            time.sleep(1 / getattr(theme, "fps", 5))
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


try:
    token = getattr(theme, "bot_token", False)
    frame_thread = FrameThread()

    if token:
        ready_event = threading.Event()
        main_thread = threading.Thread(target=bot_login, args=[token, ready_event], daemon=True)
        print("Logging into bot...")
        main_thread.start()
        ready_event.wait()
        print("Logged in!")

    print("Starting Mew+, please wait...")
    mpr = getattr(theme, "minutes_per_restart", -1)
    process = subprocess.Popen([sys.executable, "-u", "main.py"], stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
    frame_thread.start()
except (KeyboardInterrupt, SystemExit):
    print("Exiting")
    sys.exit(1)

while True:
    start_time = time.time()
    view_updates_since_clear = 0
    restart_trigger = False
    webhook = getattr(theme, "restart_webhook", False)
    webhook_color = getattr(theme, "webhook_color", 0xf7b8cf)
    restart_reason = ""
    first = True

    try:
        name_to_num = { "Restarts": restarts }
        process.stdout.flush()
        for line in process.stdout:
            if debug_mode:
                print(line)
                continue
            if restart_trigger or kill_trigger:
                restart_reason = "Bot command"
                print("Restart triggered")
                break
            restart_trigger = False

            elapsed_secs = time.time() - start_time
            if mpr > 0 and elapsed_secs > mpr * 60:
                restart_reason = f"Restart every {mpr} minutes"
                break
            if line == None: continue
            if first:
                os.system(os_clear)
                print("Startup may take up to 3 minutes on some systems")
                first = False

            utf_line = line.rstrip()
            cleaned_line = re.sub(color_regex, "", utf_line)

            if len(cleaned_line) != 0:
                if ":" in cleaned_line:
                    split = re.split(r"> |: ", cleaned_line)
                    name_to_num[split[1]] = split[2]
                if "Watching" in cleaned_line:
                    view_precursor = generate_view(name_to_num)
                    view_updates_since_clear += 1
                    if view_updates_since_clear > 15:
                        frame_thread.set_view(view_precursor, True, data=name_to_num)
                        frame_thread.send_clear()
                        view_updates_since_clear = 0
                    else: frame_thread.set_view(view_precursor, False)
        process.stdout.close()
    except (KeyboardInterrupt, SystemExit):
        kill_trigger = True
        print("Exiting")
    except ModuleNotFoundError:
        print("Please run manually: pip install requests colorama pyarmor python-socketio[client]")
        os.system("pause")
    except Exception as e:
        print(e)
        restart_reason = str(e)
        pass

    process.kill()
    if kill_trigger: break

    restarts += 1
    
    if webhook:
        print("Sending webhook")
        requests.post(webhook, json={"content": None, "embeds": [{
            "color": webhook_color,
            "title": "Mewt restarted",
            "fields": [ {"name": "Reason", "value": restart_reason, "inline": True},
                       {"name": "Restart count", "value": restarts, "inline": True} ],
            "footer": { "text": "mew+" }
        }]})
    print("Restarting")
    process = subprocess.Popen([sys.executable, "-u", "main.py"], stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
    continue
