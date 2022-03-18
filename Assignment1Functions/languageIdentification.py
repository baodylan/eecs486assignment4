# Dylan Bao
# baodylan

# import libraries
import os
from re import L
import sys
import math
import numpy

# Input: string - training text in a given language
# Output: dict - character frequencies collected from the input
#         dict - character-bigram frequencies collected from the string
# Function: given an input string, calculate the frequencies for all single characters and for all the bigram characters in the string
def trainBigramLanguageModel(text):
    char_freq = {}
    bigram_freq = {}

    # Calculating single character frequencies
    for char in text:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1

    # Calculating bigram character frequencies
    for char_ind in range(len(text) - 1):
        bigram = text[char_ind:char_ind+2]
        if bigram in bigram_freq:
            bigram_freq[bigram] += 1
        else:
            bigram_freq[bigram] = 1
    
    return char_freq, bigram_freq

# Input: string         - text
#        list (string)  - each string to language
#        list (dict)    - characater frequency
#        list (dict)    - bigram character frequencies in a language
# Output: string - the name of the most likely language
def identifyLanguage(text, languages, char_freqs, bigram_freqs):
    text = text.split()

    # Initializing each language probability to 1
    language_probability = {}
    for language in languages:
        language_probability[language] = 1

    # Finding the probability of this text for each language
    for language in range(len(languages)):
        V = len(char_freqs[language])

        # Calculating the probability for each word in this language
        for word in text:
            prob = 1
            for char_ind in range(0, len(word) - 1):
                first_char = word[char_ind:char_ind+1]
                both_chars = word[char_ind:char_ind+2]
                
                if first_char not in char_freqs[language]:
                    single_char_count = 0
                else:
                    single_char_count = char_freqs[language][first_char]

                if both_chars not in bigram_freqs[language]:
                    both_chars_count = 0
                else:
                    both_chars_count = bigram_freqs[language][both_chars]
                
                prob *= (both_chars_count + 1) / (single_char_count + V)

            # Using square root to avoid extremely small numbers (instead of log)
            language_probability[languages[language]] *= math.sqrt(prob)

    # Find which language has the highest probability
    best_prob = 0
    best_language = ""
    for language in language_probability:
        if language_probability[language] > best_prob:
            best_language = language
            best_prob = language_probability[language]
 
    return best_language

def main():
    # Opening each language file
    english = open('languageIdentification.data/training/English', 'r', encoding='latin-1').read()
    french = open('languageIdentification.data/training/French', 'r', encoding='latin-1').read()
    italian = open('languageIdentification.data/training/Italian', 'r', encoding='latin-1').read()

    # Calculating character frequencies
    english_char_freq, english_bigram_freq = trainBigramLanguageModel(english)
    french_char_freq, french_bigram_freq = trainBigramLanguageModel(french)
    italian_char_freq, italian_bigram_freq = trainBigramLanguageModel(italian)

    # Creating set lists
    languages = ["English", "French", "Italian"]
    char_freqs = [english_char_freq, french_char_freq, italian_char_freq]
    bigram_freqs = [english_bigram_freq, french_bigram_freq, italian_bigram_freq]

    # Reading in test file line by line
    test_file = sys.argv[1]
    test_lines = open(test_file, 'r', encoding='latin-1').readlines()

    # Writing to output file
    with open('languageIdentification.output', 'w') as f:
        line_num = 1
        for line in test_lines:
            f.write(str(line_num) + " " + identifyLanguage(line, languages, char_freqs, bigram_freqs) + "\n")
            line_num += 1

if __name__ == "__main__":
    main()