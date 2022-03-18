# Dylan Bao
# baodylan

# import libraries
from concurrent.futures import process
from lib2to3.pgen2 import token
import re
from Assignment1Functions.porterStemmer import PorterStemmer
import os
import sys


# Input: string
# Output: String
# Function: Removes all SGNL tags from input
def removeSGNL(input):
    filter = re.compile('<.*?>')
    return re.sub(filter, '', input)

# Input: String
# Output: list (of tokens)
# Separate the punctuation from the words, whenever punctuation is
#   not an integral part of the word
def tokenizeText(input):
    output = []
    input = input.split()
    
    for word in input:
        if word[0] == '(':
            word = word[1:]
        if len(word) > 0 and word[-1] == ')':
            word = word[:-1]
        if '.' in word:
            # If the word is just a comma
            if word == '.':
                output.append('.')
                continue

            # If the word has multiple periods, it is an abbreviation
            count = 0
            for char in word:
                if char == '.':
                    count += 1
            if count > 1:
                output.append(word)
                continue
            
            # If the period isn't at the end of the string, it is not a sentence
            if word[-1] != '.':
                output.append(word)
                continue
            
            # If the period is at the end, append the word and the period
            output.append(word[:-1])
            output.append(word[-1])
        elif ',' in word:
            if word == ',':
                output.append(',')
                continue

            # If the comma isn't at the end, append the word and the comma
            if word[-1] == ',':
                output.append(word[:-1])
                output.append(word[-1])
            else:
                output.append(word)
        elif '\'' in word:
            # Handling special cases with apostrophe's
            index = word.find('\'')
            if word[-1] == '\'':
                output.append(word[:-1])
                output.append(word[-1])
            elif word[index + 1] == 's':
                output.append(word[:index])
                output.append(word[index])
            elif word.lower() == 'i\'m':
                output.append("I")
                output.append("am")
            elif word.lower() == "they're":
                output.append("they")
                output.append("are")
            elif word.lower() == "they've":
                output.append("they")
                output.append("have")
            elif word.lower() == "isn't":
                output.append("is")
                output.append("not")
            elif word.lower() == "wasn't":
                output.append("was")
                output.append("not")
            elif word.lower() == "we'll":
                output.append("we")
                output.append("will")
            elif word.lower() == "it'll":
                output.append("it")
                output.append("will")
            elif word.lower() == "i'd":
                output.append("I")
                output.append("would")
            elif word.lower() == "you're":
                output.append("you")
                output.append("are")
            elif word.lower() == "we're":
                output.append("we")
                output.append("are")
            elif word.lower() == "would've":
                output.append("would")
                output.append("have")
            elif word.lower() == "i'll":
                output.append("I")
                output.append("will")
        elif not word.isspace():
            output.append(word)

    return output

# Input: list (of tokens)
# Output: list (of stemmed tokens)
# Function: Remove the stopwords from the input tokens
def removeStopwords(tokens, stopwords):
    output = []
    for token in tokens:
        if token not in stopwords:
            output.append(token)

    return output

# Input: list (of tokens)
# Output: list (of stemmed tokens)
# Function: 
def stemWords(tokens):
    output = []
    ps = PorterStemmer()

    for token in tokens:
        # Remove periods, commas, and apostrophes when stemming
        if token != '.' and token != ',' and token != '\'':
            output.append(ps.stem(token, 0, len(token)-1))

    return output

def process_files(files):
    stopwords = open('stopwords', 'r').read().split()

    total_words = 0
    word_frequency = {}

    for filename in os.listdir(files):
        path = os.path.join(files, filename)
        text = open(path, 'r').read()

        text = removeSGNL(text)                         # Remove SGNL tags
        tokens = tokenizeText(text)                     # Tokenize each word
        tokens = removeStopwords(tokens, stopwords)     # Remove stopwords from list
        tokens = stemWords(tokens)                      # Stem each word

        total_words += len(tokens)
        for token in tokens:
            if token not in word_frequency:
                word_frequency[token] = 1
            else:
                word_frequency[token] += 1

    # Sort the word requencies in descending order
    word_frequency = {a: b for a, b in sorted(word_frequency.items(), key=lambda item: item[1], reverse=True)}

    return total_words, word_frequency

def write_output(total_words, word_frequency, filename):
    with open(filename, 'w') as f:
        f.write("Words " + str(total_words) + '\n')
        f.write("Vocabulary " + str(len(word_frequency)) + '\n')
        f.write("Top 50 words\n")
        
        count = 0
        for word in word_frequency:
            if count == 50:
                break
            f.write(word + " " + str(word_frequency[word]) + '\n')
            count += 1


def calculate_25(word_frequency, target):
    count = 0
    current = 0
    for word in word_frequency:
        if current >= target:
            break

        current += word_frequency[word]
        count += 1
    print(count)
    print(current)

def main():
    dir = sys.argv[1]
    total_words, word_frequency = process_files(dir)
    write_output(total_words, word_frequency, 'preprocess.output')

    # Calculating the numnber of unique words that make up 25% of the collection
    calculate_25(word_frequency, 36441)

    # Repeat for two subsets
    subsetOne = 'cranfieldDocsSubsetOne'
    subsetTwo = 'cranfieldDocsSubsetTwo'

    total_words1, word_frequency1 = process_files(subsetOne)
    total_words2, word_frequency2 = process_files(subsetTwo)
    write_output(total_words1, word_frequency1, "preprocess_subset_one.output")
    write_output(total_words2, word_frequency2, "preprocess_subset_two.output")

if __name__ == "__main__":
    main()