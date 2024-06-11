# utils/banner.py

from colorama import Fore, init
import pyfiglet

class Banner:
    def __init__(self, text):
        self.text = text

        init(autoreset=True)

    def print_ascii_banner(self):
        ascii_banner = pyfiglet.figlet_format(self.text)
        print(ascii_banner)
    def print_simple_banner(self):
        T="By Bharath_kannan"
        width = len(T) + 4
        print(f"{T} ")
        