import os

DB_FILE = "TinyLib.db"

class StrStyle():
    GRAY = '\033[90m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * 40)
    print(" " * 10 + StrStyle.BOLD + "📚 T i n y L i b 📚" + StrStyle.RESET)
    print("-" * 40)