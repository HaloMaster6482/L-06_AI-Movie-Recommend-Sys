import time, pandas as pd
from textblob import TextBlob
from colorama import Fore, init

init(autoreset=True)

try df = pd.("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + f"ERROR: {Fore.YELLOW} The file {Fore.GREEN}'imdb_top_1000.csv' was not found")