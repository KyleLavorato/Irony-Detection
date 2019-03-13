import emoji #emoji
from ekphrasis.classes.preprocessor import TextPreProcessor #ekphrasis
from ekphrasis.classes.tokenizer import SocialTokenizer
import csv, re, os # For slang translator

from Dictionaries.custom_emoticons import emoticons
from Dictionaries.slang_dict import slangdict
from settings import normalize_emoji

# Import the preprocessing functions
import Preprocess


def new_readDictionaries():
    slangDictionary = []
    swearDictionary = []
    emojiDictionary = []
    with open("../Preprocessing/Dictionaries/slang-dictionary.txt", "r") as f:
        # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            slangDictionary.append(row)
    with open("../Preprocessing/Dictionaries/swear-dictionary.txt", "r") as f:
        # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            swearDictionary.append(row)
    with open("../Preprocessing/Dictionaries/emoji-real-dictionary.txt", "r", encoding="utf-8") as f:
        # Reading file as CSV with delimiter as " = ", so that emojis are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            emojiDictionary.append(row)
    return slangDictionary, swearDictionary, emojiDictionary
Preprocess.readDictionaries = new_readDictionaries


def readInitialDatasets():
    randomCorpus = []
    ironyCorpus = []

    # Removing duplicates from the large dataset is too costly to do in memory here
    # Use: awk '!seen[$0]++' FILENAME > OUTPUT
    print("Reading Random Dataset")
    with open("../Pretraining/corpus-random.txt", "r", encoding="utf-8") as f:
        for line in f:
            lineFixed = str.strip(line)
            randomCorpus.append(lineFixed)
    yRandom = [0] * len(randomCorpus)

    print("Reading Irony Dataset")
    with open("../Pretraining/corpus-irony.txt", "r", encoding="utf-8") as f:
        for line in f:
            lineFixed = str.strip(line).replace("#irony","").replace("#Irony","").replace("#not","").replace("#Not","").replace("#Sarcasm","").replace("#sarcasm","")
            if lineFixed not in ironyCorpus:
                ironyCorpus.append(lineFixed)
    yIrony = [1] * len(ironyCorpus)


    return randomCorpus, ironyCorpus, yRandom, yIrony

if __name__ == "__main__":
    randomCorpus, ironyCorpus, yRandom, yIrony = readInitialDatasets()

    processedRandom = Preprocess.preprocessCorpus(randomCorpus)
    Preprocess.writeCorpus(processedRandom, yRandom, "corpus-random-processed.txt")

    processedIrony = Preprocess.preprocessCorpus(ironyCorpus)
    Preprocess.writeCorpus(processedIrony, yIrony, "corpus-irony-processed.txt")

    os.remove("../Pretraining/slangdict.pickle")