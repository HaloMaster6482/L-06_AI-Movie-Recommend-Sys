import time, pandas as pd
from textblob import TextBlob
from colorama import init, Fore

init(autoreset=True)

try: data_set = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError: print(Fore.RED + f"Error:{Fore.YELLOW} The file {Fore.GREEN}'imdb_top_1000.csv'{Fore.YELLOW} was not found."); raise SystemExit

genres = sorted({g.strip() for xs in data_set["Genre"].dropna().str.split(", ") for g in xs})

def dots():
    for _ in range(3): print(Fore.YELLOW + ".", end="", flush=True); time.sleep(0.5)

def senti(p): return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"

def recommend(genre=None, mood=None, rating=None, n=5):
    d = data_set
    if genre: d = d[d["Genre"].str.contains(genre, case=False, na=False)]
    if rating is not None: d = d[d["IMDB_Rating"] >= rating]
    if d.empty: return "No suitable movie recommendations found."
    d, need_nonneg, out = d.sample(frac=1).reset_index(drop=True), bool(mood), []
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov): continue
        pol = TextBlob(ov).sentiment.polarity
        if (not need_nonneg) or pol >= 0:
            out.append((r["Series_Title"], pol))
            if len(out) == n: break
    return out if out else "No suitable movie recommendations found."

def show(recs, name):
    print(Fore.YELLOW + f"\n🍿 AI-Analyzed Movie Recommendations for {name}:")
    for i, (t, p) in enumerate(recs, 1):
        print(f"{Fore.YELLOW}{i}. 🎥 {Fore.GREEN}{t} {Fore.BLUE}(Polarity: {p:.2f}, {senti(p)})")

def get_genre():
    print(Fore.YELLOW + "Available Genres: ")
    for i, g in enumerate(genres, 1): 
        print(f"{Fore.YELLOW}{i}. {Fore.GREEN}{g}")
    print()
    while True:
        x = input(Fore.YELLOW + "Enter genre number or name: ").strip()
        if x.isdigit() and 1 <= int(x) <= len(genres): return genres[int(x) - 1]
        x = x.title()
        if x in genres: return x
        print(Fore.RED + f"Invalid input.{Fore.YELLOW} Try again.\n")

def get_rating():
    while True:
        x = input(Fore.YELLOW + f"Enter minimum {Fore.GREEN}IMDB rating (7.6-9.3) {Fore.YELLOW}or {Fore.GREEN}'skip'{Fore.YELLOW}: {Fore.BLUE}").strip()
        if x.lower() == "skip": return None
        try:
            r = float(x)
            if 7.6 <= r <= 9.3: return r
            print(Fore.RED + "Rating out of range. Try again.\n")
        except ValueError:
            print(Fore.RED + "Invalid input. Try again.\n")

print(Fore.BLUE + "🎥 Welcome to your Personal Movie Recommendation Assistant! 🎥\n")
name = input(Fore.YELLOW + "What's your name? ").strip()
print(f"\n{Fore.GREEN}Great to meet you, {name}!\n")
print(Fore.BLUE + "\n🔍 Let's find the perfect movie for you!\n")

genre = get_genre()
mood = input(Fore.YELLOW + "How do you feel today? (Describe your mood): ").strip()
print(Fore.BLUE + "\nAnalyzing mood", end="", flush=True); dots()
mp = TextBlob(mood).sentiment.polarity
md = "positive 😊" if mp > 0 else "negative 😞" if mp < 0 else "neutral 😐"
print(f"\n{Fore.GREEN}Your mood is {md} (Polarity: {mp:.2f}).\n")

rating = get_rating()
print(f"{Fore.BLUE}\nFinding movies for {name}", end="", flush=True); dots()
recs = recommend(genre=genre, mood=mood, rating=rating, n=5)
print(Fore.RED + recs + "\n") if isinstance(recs, str) else show(recs, name)

while True:
    a = input(Fore.YELLOW + "\nWould you like more recommendations? (yes/no): ").strip().lower()
    if a == "no":
        print(Fore.GREEN + f"\nEnjoy your movie picks, {name}! 🎬🍿\n"); break
    if a == "yes":
        recs = recommend(genre=genre, mood=mood, rating=rating, n=5)
        print(Fore.RED + recs + "\n") if isinstance(recs, str) else show(recs, name)
    else:
        print(Fore.RED + "Invalid choice. Try again.\n")
