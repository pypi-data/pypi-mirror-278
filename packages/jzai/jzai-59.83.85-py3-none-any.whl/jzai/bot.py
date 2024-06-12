import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
import random
import requests
from functools import lru_cache
import threading
from sys import stdout
from time import sleep
import subprocess
from sys import platform
import os


def check_for_updates():
    current_version = "59.83.85"
    version_parts = list(map(int, current_version.split(".")))

    def version_to_str(parts):
        return ".".join(map(str, parts))

    def increment_version(parts):
        parts[2] += 1
        if parts[2] >= 100:
            parts[2] = 0
            parts[1] += 1
            if parts[1] >= 100:
                parts[1] = 0
                parts[0] += 1

    def decrement_version(parts):
        if parts[2] > 0:
            parts[2] -= 1
        elif parts[1] > 0:
            parts[1] -= 1
            parts[2] = 99
        else:
            parts[0] -= 1
            parts[1] = 99
            parts[2] = 99

    current_version_str = version_to_str(version_parts)
    while True:
        increment_version(version_parts)
        next_version_str = version_to_str(version_parts)
        response = requests.get(f"https://pypi.org/project/jzai/{next_version_str}/")
        if response.status_code == 404:
            decrement_version(version_parts)
            latest_version_str = version_to_str(version_parts)
            break

    latest_version = ".".join(map(str, version_parts))

    if latest_version > current_version:
        user_input = (
            input(
                f"New version {latest_version} available. Do you want to upgrade? (yes/no): "
            )
            .strip()
            .lower()
        )
        if user_input == "yes" or user_input == "y":
            if platform.lower().startswith("win"):
                subprocess.run(["pip", "install", "jzai", "-U"])
            else:
                subprocess.run(["pip3", "install", "jzai", "-U"])
        else:
            print("Upgrade canceled.")


check_for_updates()

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)


class Bot:
    def __init__(self, name):
        self.name = name
        self.users = {}
        self.current_user = None
        self.conversations = []
        self.preprocessed_conversations = []
        self.conversations_loaded = threading.Event()
        threading.Thread(
            target=self.load_conversations_async,
            args=("http://jzai.atwebpages.com/convo.json",),
        ).start()

    @lru_cache(maxsize=None)
    def preprocess_text(self, text):
        corrected_text = str(TextBlob(text).correct())
        stop_words = set(stopwords.words("english"))
        tokens = [
            re.sub(r"[^a-zA-Z]", "", token).lower()
            for token in word_tokenize(corrected_text)
            if token.lower() not in stop_words
        ]
        tokens = [token for token in tokens if token]

        return tokens

    def generate_response(self, user_input):
        try:
            user_input_tokens = self.preprocess_text(user_input)
            if len(user_input) < 4:
                return f"Input must be a minimum of 4 characters. Not {len(user_input)}."

            max_similarity = 0
            best_response = None

            for question_tokens, answers in self.preprocessed_conversations:
                try:
                    if question_tokens and user_input_tokens:
                        common_tokens = set(question_tokens) & set(user_input_tokens)
                        similarity = len(common_tokens) / max(
                            len(question_tokens), len(user_input_tokens)
                        )
                    else:
                        similarity = 0
                except ZeroDivisionError:
                    similarity = (
                        0  # Handle ZeroDivisionError by setting similarity to 0
                    )

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = answers

            if best_response:
                return random.choice(best_response)
            else:
                return "I'm sorry, I didn't understand."
        except Exception as e:
            return f"Error: {e}"

    def load_conversations_async(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.conversations = response.json()
            self.preprocessed_conversations = [
                (self.preprocess_text(entry["question"]), entry["answers"])
                for entry in self.conversations
            ]
            self.conversations_loaded.set()
        except Exception as e:
            print(f"Error loading conversations from {url}: {e}")
            self.conversations_loaded.set()


bot = Bot(name="JZ")

def typewriter(txt):
    for char in txt:
        stdout.write(char)
        stdout.flush()
        sleep(0.01)
        
try:
    while True:
        if not bot.conversations_loaded.is_set():
            print("Loading...")
            while not bot.conversations_loaded.is_set():
                if bot.conversations_loaded.is_set():
                    if platform.lower().startswith("win"):
                        os.system('cls')
                    else:
                        os.system('clear')
                    continue

        user_input = input("You: ")
        if user_input.lower() == "exit":
            typewriter("Exiting...")
            quit()
        else:
            response = bot.generate_response(user_input)
            typewriter(f'{bot.name}: {response}\n')

except KeyboardInterrupt:
    typewriter("\nExiting...")
