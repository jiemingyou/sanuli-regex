import re
import random

class Sanuli:

    def __init__(self, wordlist):
        self._wordlist = set(wordlist)
        self._remaining = set(wordlist)

    def reset(self):
        self._remaining = self._wordlist
    
    def guess(self, letters: list, colors: list):

        n = len(letters)
        greens = [i for i, x in enumerate(colors) if x == "v"]
        yellows = [i for i, x in enumerate(colors) if x == "k"]
        grays = [i for i, x in enumerate(colors) if x == "h"]
        
         # REGEX filter for grays
        NOT_IN_WORD = ""
        for i in grays:
            NOT_IN_WORD += letters[i]
        NOT_IN_WORD = f"(?=^[^{NOT_IN_WORD}]*$)" if grays else ""

        # REGEX filter for greens
        IN_WORD = list("."*n)
        for i in greens:
            IN_WORD[i] = letters[i]
        IN_WORD = "".join(IN_WORD)

        # REGEX filter for yellows
        CONTAINS_IN_WORD = ""
        POSITION_FILTER = ""
        for i in yellows:
            CONTAINS_IN_WORD += letters[i]
            POSITION_FILTER += f"(?!^{i*'.'}{letters[i]})"
        CONTAINS_IN_WORD = f'(?=.*[{CONTAINS_IN_WORD}])' if yellows else ""
        POSITION_FILTER = POSITION_FILTER if yellows else ""

        expression = '^' + NOT_IN_WORD + CONTAINS_IN_WORD + POSITION_FILTER + IN_WORD + '$'

        regex = re.compile(expression, re.IGNORECASE)
        words_left = {word for word in self._remaining if re.match(regex, word)}

        print("Possible words:", words_left)

        self._remaining = words_left


if __name__ == "__main__":
    
    words = set()
    with open("kotus_wordlist.txt") as f:
        for word in f:
            word = word.strip()
            words.add(word)

    peli = Sanuli(words)
    peli.reset()

    while True:
        guess = list(input("Guessed word: "))
        colors = list(input("Letter colors: "))
        peli.guess(guess, colors)