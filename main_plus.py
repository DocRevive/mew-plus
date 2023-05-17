# Up-to-date with 3.1.0
# Created by Revive#8798

theme_name = "theme_default" # name of python theme file WITHOUT .py
debug_mode = False

from io import StringIO
import subprocess
import threading
import importlib
import rgbprint
import colorama
import time
import sys
import os
import re

restarts = 0
print_cache = {}
colorama.just_fix_windows_console()
os.environ["PYTHONUNBUFFERED"] = "x"
color_regex = re.compile(r"\x1B.*?m")
split_regex = re.compile(r"> |: ")
line_regex = re.compile(r"(?<!\x1b)\[(.*?)\]\[(.*?)\]", flags=re.MULTILINE)
block_regex = re.compile(r"(?<!\x1b)\[\[\[(.*?)\]\]\]\[(.*?)\]", flags=re.DOTALL)
frame_placeholder_regex = re.compile(r"\[\|\[\(.*?\)\]\|\]", flags=re.DOTALL)
function_types = ["rgbprint", "gradient_print", "gradient_scroll", "gradient_change"]
os_clear = "cls" if os.name == "nt" else "clear"

theme = importlib.import_module(theme_name)
minutes_per_restart = theme.minutes_per_restart
color_props = theme.color_props
template = theme.template
fps = theme.fps

os.system(os_clear)
print("Contribute: https://github.com/DocRevive/mew-plus", "Starting Mew+, please wait...", sep="\n")

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
    result = template
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
            if self.view == None: continue
            self.in_progress = True
            view_frame = update_frames(self.view)
            if view_frame == False:
                self.anim_enabled = False
                self.in_progress = False
                self.print(self.view)
                break
            time.sleep(1 / fps)
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
            greenlight = not self.in_progress
            attempts = 0
            while not greenlight:
                time.sleep(0.1)
                attempts += 1
                greenlight = not self.in_progress
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

if __name__ == "__main__":
    mpr = minutes_per_restart
    process = subprocess.Popen([sys.executable, "main.py"], stdout=subprocess.PIPE)
    frame_thread = FrameThread()
    frame_thread.start()

    while True:
        start_time = time.time()
        view_updates_since_clear = 0
        first = True

        try:
            nameToNum = { "Restarts": restarts }
            for line in process.stdout:
                elapsed_secs = time.time() - start_time
                if mpr > 0 and elapsed_secs > mpr * 60: break
                if line == None: continue
                if first:
                    os.system(os_clear)
                    first = False

                utf_line = line.rstrip().decode("utf-8")
                cleaned_line = re.sub(color_regex, "", utf_line)

                if len(cleaned_line) != 0:
                    if ":" in cleaned_line:
                        split = re.split(split_regex, cleaned_line)
                        nameToNum[split[1]] = split[2]
                    if "Watching" in cleaned_line:
                        view_precursor = generate_view(nameToNum)
                        view_updates_since_clear += 1
                        if view_updates_since_clear > 30:
                            frame_thread.set_view(view_precursor, True, data=nameToNum)
                            frame_thread.send_clear()
                            view_updates_since_clear = 0
                        else: frame_thread.set_view(view_precursor, False)
        except KeyboardInterrupt:
            print("Exiting")
            process.kill()
            sys.exit(1)
        except ModuleNotFoundError:
            print("Please run manually: pip install requests colorama pyarmor python-socketio[client]")
            os.system("pause")
            break
        except Exception as e:
            print(e)
            pass

        process.kill()
        restarts += 1
        print("Restarting")
        process = subprocess.Popen([sys.executable, "main.py"], stdout=subprocess.PIPE)
        continue
