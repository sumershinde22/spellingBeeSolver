import json
import re
import requests
from bs4 import BeautifulSoup

# Fetching the game data from NYT Spelling Bee page
URL = "https://www.nytimes.com/puzzles/spelling-bee"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="js-hook-pz-moment__game")
script = results.find_all("script")[0].text

# Extract and parse JSON data
json_str = re.search(r'\{.*\}', script).group(0)
json_data = json.loads(json_str)

# Retrieve the game details
center = json_data['today']['centerLetter']
outer = json_data['today']['outerLetters']
all_letters = json_data['today']['validLetters']
answers = json_data['today']['answers']

print(f'Center letter: {center}')
print(f'Outer letters: {", ".join(outer)}')

# Read word list
with open("words.txt", "r") as word_file:
    wordlist = [word.strip().lower() for word in word_file]

# Define a function to solve the spelling bee
def solve_spelling_bee(letters_list, center_letter, words):
    acceptable_letters = set(letters_list)
    unacceptable_letters = set('abcdefghijklmnopqrstuvwxyz') - acceptable_letters

    # Collect words that meet the criteria
    return [
        word
        for word in words
        if center_letter in word
        and len(word) > 3
        and unacceptable_letters.isdisjoint(word)
    ]

# Get the acceptable words
acceptable_words = solve_spelling_bee(all_letters, center, wordlist)
print(acceptable_words)
common_elements = set(acceptable_words) & set(answers)
print(str(len(common_elements)) + " common accepted words: " + ", ".join(common_elements))
