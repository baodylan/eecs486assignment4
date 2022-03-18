# Dylan Bao
# baodylan

import sys
import os
import math
from numpy import real
from Assignment1Functions.preprocess import removeSGNL
from Assignment1Functions.preprocess import tokenizeText
from Assignment1Functions.preprocess import removeStopwords
from Assignment1Functions.preprocess import stemWords


# Input: list (string) - File paths used for training
# Output: dict - Class probabilities
#         dict - Word conditional probabilities
def trainNaiveBayes(paths):
    fake_count = 0
    real_count = 0
    vocab = []
    fake_words = []
    real_words = []

    for path in paths:
        # Creating the vocabulary
        with open(path, 'r') as f:
            text = f.read()
            tokens = tokenizeText(text)

            for token in tokens:
                if token not in vocab:
                    vocab.append(token)

                if path[9] == 'f':
                        fake_count += 1
                        fake_words.append(token)
                else:
                    real_count += 1

                    if token not in real_words:
                        real_words.append(token)        

    # Calculating class probabilities
    class_prob = {}
    class_prob['fake'] = fake_count / (fake_count + real_count)
    class_prob['true'] = real_count / (fake_count + real_count)

    # Calculating word conditional probabilities
    word_prob = {'fake': {}, 'true': {}}
    for token in tokens:
        word_prob['fake'][token] = (fake_words.count(token) + 1) / (len(fake_words) + len(vocab))
        word_prob['true'][token] = (real_words.count(token) + 1) / (len(real_words) + len(vocab))

    return class_prob, word_prob, len(vocab)

# Input: string - File path to directory containing the data files
#        string - Output file produced by trainNaiveBayes
# Output: string - Predicted class ("true" or "false")
def testNaiveBayes(class_prob, word_prob, vocab_size, filename):
    test_prob = {'fake': class_prob['fake'], 'true': class_prob['true']}
    with open(filename, 'r') as f:
        text = f.read()
        tokens = tokenizeText(text)

        for token in tokens:
            if token not in word_prob['fake']:
                test_prob['fake'] *= math.log((1 / vocab_size))
            else:
                test_prob['fake'] *= math.log(word_prob['fake'][token])
            
            if token not in word_prob['true']:
                test_prob['true'] *= math.log((1 / vocab_size))
            else:
                test_prob['true'] *= math.log(word_prob['true'][token])

    if test_prob['fake'] > test_prob['true']:
        return 'fake'
    else:
        return 'true'

def main():
    # Taking in arguments
    folder = sys.argv[1]

    filenames = []
    # Open the folder, read in files
    for file in os.listdir(folder):
        filenames.append(os.path.join(folder, file))

    count = 1
    output_filename = 'naivebayes.output.' + folder[:-1]
    with open(output_filename, 'w') as output:
        for file in filenames:
            print(count)
            count += 1
            filenames_copy = filenames.copy()
            filenames_copy.remove(file)

            class_prob, word_prob, vocab_size = trainNaiveBayes(filenames_copy)
            pred_class = testNaiveBayes(class_prob, word_prob, vocab_size, file)
            output.write(file[9:] + " " + pred_class + '\n')


if __name__ == "__main__":
    main()