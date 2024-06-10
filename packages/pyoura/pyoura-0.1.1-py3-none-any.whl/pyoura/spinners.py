# spinner.py (or pyoura.py)

import sys
import time
import threading
from termcolor import colored
import colorama



colorama.init()
class Oura:
    def __init__(self, text="Loading...", spinner="dots",color="cyan"):
        self.text = text
        self.spinner = spinner
        self.color=color
       

    def start(self, text=None):
        if text:
            self.text = text
        self._spinner_thread = threading.Thread(target=self._spin)
        self._stop_spinner = False
        self._spinner_thread.start()

    def _spin(self):
        spinner_types = {
            "dots": ".oOo",
            "dots2": "..ooOO",
            "dots3": "...oO0o",
            "arrow": "←↖↑↗→↘↓↙",
            "braille": "⡇⣆⣤⣀⣤⣶⣾⣷",
            "box_dots": "▖▘▝▗",
            "clock": "🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚",
            "circle": "◐◓◑◒",
            "pong": "▐⠂       ⠂▌",
            "triangle": "▲▼◄►",
            "worm": "▖▘▝▗",
            "moon": "🌑🌒🌓🌔🌕🌖🌗🌘",
            "dots11": "⣾⣷⣿",
            "vline": "▁▃▄▅▆▇█▇▆▅▄▃",
            "hline": "▏▎▍▌▋▊▉▊▋▌▍▎",
            "cross": "✚✙✛✜",
            "asterisk": "*⋆",
            "slash": "/-\\|",
            "daisy": "✼❁✿❃",
            "bar": "▂▃▄▅▆▇█▇▆▅▄▃",
            "spinner": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
            "toggle": "⢿⣟⣯⣷",
            "dots8bit": "✶✸✹✺✹✷✵✴",
            "dots8bit2": "⣾⣽⣻⢿⡿⣟⣯⣷",
            "dots8bit3": "⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓",
            "line": "▂▃▄▅▆▇█▇▆▅▄▃",
            "triangle2": "◢◣◤◥",
            "squares": "◰◳◲◱",
            "bounce": "⠁⠂⠄⠂",
            "bouncing_ball": "⣾⣽⣻⢿⡿⣟⣯⣷",
            "note": "♩♪♫♬",
            "dots4": "⣾⣷⣿⣶",
            "dots5": "⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓",
            "dots6": "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦",
            "dots7": "⠉⠙⠤⢀⠠⠄⠄⢠⠐⠂",
            "dots8": "⠁⠂⠄⡀⢀⠠⠐⠈",
            "dots9": "⢹⢺⢼⣸⣇⡧⡗⡏",
            "dots10": "⣾⣽⣻⢿⡿⣟⣯⣷",
            "dots12": "⢸⣰⣠⣤⣴⣆⡂⠅⢆⣀⣸⣰⣠",
            "dots13": "⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓",
            "dots14": "⠇⡇⠸⢹⣰⣠⠖⠆⠙⠋",
            "dots15": "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦",
            "dots16": "⠙⠚⠒⠂⠂⠒⠲⠴⠦⠦⠖⠲⠴⠦⠦",
            "dots17": "⠿⠟⠻⠽⠾⠷⠮⠬⠐⠄",
            "dots18": "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦",
            "dots19": "⠈⠉⠋⠓⠒⠐⠐⠒⠖⠦⠴⠲⠳⠓",
            "dots20": "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠦⠴⠲⠦⠦",
            "dots21": "⢹⢺⢼⣸⣇⡧⡗⡏",
            "dots22": "⣾⣽⣻⢿⡿⣟⣯⣷",
            "dots23": "⣿⣾⣷⣶⣭⣽⣻⢿⡿⣟⣯⣷",
            "dots24": "⠉⠙⠚⠒⠂⠂⠒⠲⠴⠦",
            "dots25": "⠁⠂⠄⡀⢀⠠⠐⠈",
            "dots26": "⠁⠂⠄⡀⢀⠠⠐⠈",
            "dots27": "⠁⠂⠄⡀⢀⠠⠐⠈",
            "dots28": "⠁⠂⠄⡀⢀⠠⠐⠈",
            "dots29": "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
            "dots30": "⠁⠉⠙⠚⠒⠂⠂⠒⠒⠲⠲⠴⠴⠦⠦⠖⠲⠲⠴⠴⠦⠦⠖⠲⠲⠦⠦⠐⠈",
            "dots31": "⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀",
            "dots32": "⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉",
            "dots33": "⠁⠉⠙⠚⠒⠂⠂⠒⠒⠲⠲⠴⠴⠦⠦⠖⠲⠲⠴⠴⠦⠦⠖⠲⠲⠦⠦⠐⠈",
            "dots34": "⣿⣷⣶⣦⣄⣀⡀⠄⠂⠁",
            "dots35": "⠉⠛⠿⠿⠷⠶⠶⠶⠶⠶⠖⠒⠦⠤⠤⠤⠤⠤⠤⠴⠶⠶⠶⠾⠿⠿⠷⠶⠾⠛⠉",
            "dots36": "⡁⡈⠳⢶⣤⣬⣄⠉⡁⠐⢀⣠⣴⣶⡾⠯⠉⠁",
            "dots37": "⡁⠈⠑⢄⣀⠔⠋⠉⠉⠙⠓⠲⢤⡀⠂⠒⠚⠛⠂⠉⠉⠉⠉",
            "dots38": "⢀⣀⣠⣤⣶⣶⣶⣶⣦⣤⣄⡀⢀",
            "dots39": "⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣾⣶⣦⣀",
            "dots40": "⡀⡀⠑⠡⢄⣨⣶⣶⡞⠉⢁⣄⣀⡀⢀",
            "dots41": "⣀⣀⡀⢁⠂⠄⠄⠄⠄⠄⠄⠄⠐⠤⣆⡀⢀",
            "dots42": "⡀⠔⠊⠄⠄⠄⢂⣄⡀⠈⠒⠒⠊⠉⠉⠉⠉⠉",
            "dots43": "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠲⠲⠦⠦⠖⠲⠶⠶⠦⠦⠖⠲⠶⠶⠦⠦⠤⠴⠶⠶⠦⠦⠖⠒⠒⠂⠂⠒⠚⠙⠋",
            "dots44": "⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀",
            "dots45": "⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉",
            "dots46": "⡀⣀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣶⣦⣤⣄⡀",
            "dots47": "⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇",
            "dots48": "⠇⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠇",
            "dots49": "⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣶",
            "dots50": "⢀⣠⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣦⣄",
            "dots51": "⠁⠂⠄⡀⢐⠠⠈⠐⠠⠠⠈⢀⠄⠂⡀⢠⠐⠠⠠⠈⢀⠄⠂⡀⠠⠐⠠⠠⠄⡀",
            "dots52": "⣰⣰⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣴⣾",
            "dots53": "⣇⡠⠐⠈⡁⡀⢁⣂⡄⡐⠈⠂⠈⠐⡀⠂⠈⠈⠐⡀⢂⡀⡁⠄⢂⠐⠈⠈⠈⢁⡀",
            "dots54": "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠲⠶⠶⠶⠶⠶⠚⠒⠂⠂⠒⠲⠴⠦⠖⠲⠶⠶⠶⠶⠶",
            "dots55": "⠒⠒⠂⠂⠄⠄⠂⠂⠂⠐⠐⠐⡀⢀⢀⡄⣀⣀⢄⢤⢤⣤⣤⣤⣤⣤⣤⣀⣀⣀⣀",
            "dots56": "⣤⣀⡀⢀⠄⠒⠂⠂⠂⠐⠠⢀⣀⡀⢀⠄⠂⠂⠂⠂⠂⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒",
            "dots57": "⠁⠂⠄⡀⢀⡀⠂⠂⠐⠐⡀⢀⣀⡀⢀⠄⠂⠂⠂⠂⠂⠒⠒⠒⠒⠒⠒⠒⠒⠒",
            "dots58": "⣀⡀⠔⠊⠄⠄⠄⢂⣄⡀⠈⠒⠒⠊⠉⠉⠉⠉⠉⠉⠉",
            "dots59": "⠉⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠲⠶⠶⠶⠶⠶⠚⠒⠂⠂⠒⠲⠴⠦⠖⠲⠶⠶⠶⠶⠶",
            "dots60": "⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣦⣄",
            "dots61": "⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣦⣤⣀",
            "dots62": "⣾⣷⣶⣦⣄⡀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀",
            "dots63": "⢀⣀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣦⣄",
            "dots64": "⣾⣾⣾⣾⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣾",
            "dots65": "⡟⢋⠂⢉⣩⡑⠄⠐⡘⣜⢼⡲⡦⢂⡄⣀⢈⠰⡐⡡⠡⢀⡠⠄⠠⢈⡀⠄⡂",
            "dots66": "⣿⣷⣾⣶⣶⣶⣶⣶⣤⣄⡀⠈⠙⢿⡏⠂⠄⡈⢆⣔⣨⣶⣿⣿",
            "dots67": "⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿",
            "dots68": "⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
            "dots69": "⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
            "dots70": "⡿⠋⠂⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄",
            "dots71": "⣇⣀⣠⣤⣤"

        }
        
        spinner = spinner_types.get(self.spinner, ".oOo")
        while not self._stop_spinner:
            for char in spinner:
                colored_char = colored(char,self.color)
                sys.stdout.write(f"\r {colored_char} {self.text}")
                sys.stdout.flush()
                time.sleep(0.1)
        # Replace spinner with message character when spinner stops
        sys.stdout.write(f"\r ")
        sys.stdout.flush()
       


    def stop(self):
        self._stop_spinner = True
        self._spinner_thread.join()

    def succeed(self, text=None):
        self.stop()  # Stop the spinner
        if text:
            self.text = text
        print(colored(f"\u2714 {self.text}", 'green'))  # Display success message

    def fail(self, text=None):
        self.stop()  # Stop the spinner
        if text:
            self.text = text
        print(colored(f"\u2718 {self.text} ", 'red'))  # Display failure message

    def warn(self, text=None):
        self.stop()  # Stop the spinner
        if text:
            self.text = text
        print(colored(f"⚠️ {self.text}", 'yellow'))  # Display warning message

    def info(self, text=None):
        self.stop()  # Stop the spinner
        if text:
            self.text = text
        print(colored(f"ℹ️ {self.text}", 'blue'))  # Display info message

    def stop_and_persist(self, symbol="", text=None):
        self.stop()  # Stop the spinner
        if text:
            self.text = text
        print(colored(f"{self.text} {symbol}", 'cyan'))  # Persist message

# Additional functionality:
def create_ora(text="Loading...", spinner="dots"):
    # Convenience function to create Ora instance
    return Oura(text, spinner)
