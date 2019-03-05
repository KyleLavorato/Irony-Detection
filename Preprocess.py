import emoji
import subprocess, sys
import unicodedata
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.spellcorrect import SpellCorrector
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from spellchecker import SpellChecker  #pyspellchecker
import csv, re, os # For slang translator


# Source: https://www.webopedia.com/quick_ref/textmessageabbreviations.asp
# Manually reviewed to fix duplicates and add swear words; Added some missing slang misspellings
def buildSlangDict():
    os.remove("slang-dictionary.txt")
    with open("slang-source-dictionary.txt", "r") as f:
        with open("slang-dictionary.txt", "a") as out:
            line = ""
            i = 0
            for data in f:
                read = str.strip(data)
                if read == "":
                    line = line + "="
                    i += 1
                else:
                    line = line + read
                    i += 1
                if i == 3:
                    line = line + '\n'
                    out.write(line)
                    line = ""
                    i = 0
                    try:
                        next(f)
                    except:
                        pass

def readDictionaries():
    slangDictionary = []
    swearDictionary = []
    with open("slang-dictionary.txt", "r") as f:
        # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            slangDictionary.append(row)
    with open("swear-dictionary.txt", "r") as f:
        # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            swearDictionary.append(row)
    return slangDictionary, swearDictionary


def parseDataset(fp):
    y = []
    corpus = []
    with open(fp, 'rt', encoding='utf8') as data_in:
        for line in data_in:
            if not line.lower().startswith("tweet index"): # discard first line if it contains metadata
                line = line.rstrip() # remove trailing whitespace
                label = int(line.split("\t")[1])
                tweet = line.split("\t")[2]
                y.append(label)
                corpus.append(tweet)

    return corpus, y


def preprocessCorpus(corpus):
    newCorpus = []
    text_processor = TextPreProcessor(
        normalize=['url', 'money', 'phone', 'user', 'time', 'date'],
        annotate={"hashtag", "allcaps", "elongated"},
        fix_html=True,
        segmenter="twitter",
        corrector="twitter",
        unpack_hashtags=True,  # perform word segmentation on hashtags
        unpack_contractions=True,  # Unpack contractions (can't -> can not)
        spell_correct_elong=False,  # spell correction for elongated words
        # tokenizer=SocialTokenizer(lowercase=True).tokenize,
    )
    for tweet in corpus:
        newTweet = "".join(text_processor.pre_process_doc(tweet))
        newCorpus.append(newTweet)

    # nn = []
    # sp = SpellCorrector(corpus="english")
    # for tweet in newCorpus:
    #     for word in tweet:
    #         print(sp.correct(word))
    return newCorpus


def deslangify(user_string, dict):
    user_string = user_string.split(" ")
    j = 0
    for _str in user_string:
        # Removing Special Characters.
        _str = re.sub('[^a-zA-Z0-9-_.]', '', _str)
        for row in dict:
            # Check if selected word matches short forms[LHS] in text file.
            if _str.upper() == row[0]:
                # If match found replace it with its Abbreviation in text file.
                user_string[j] = row[1]
        j = j + 1
    # Replacing commas with spaces for final output.
    return ' '.join(user_string)


def printCorpus(corpus, y):
    for i in range(0, len(corpus)):
        print(y[i],"|",corpus[i])


if __name__ == "__main__":
    # Experiment settings

    buildSlangDict()  # Build the slang dictionary from source

    DATASET_FP = "Datasets/Train/SemEval2018-T3-train-taskB_emoji.txt"

    # Loading dataset and featurised simple Tfidf-BoW model
    corpus, y = parseDataset(DATASET_FP)

    # processedCorpus = preprocessCorpus(corpus)
    #
    # printCorpus(processedCorpus, y)

    slangDictionary, swearDictionary = readDictionaries()

    print(deslangify("CYA B4 u leave 4 camp app atm asm aom", slangDictionary))
    print(deslangify("fuck shit, asshole", swearDictionary))


## Preprocessing Goals in order:

# Convert emoji's to street meaning

# X Replace acronyms and slang (eg r = are)
    # Needs manual review to look for missed slang

# Preprocessing library
    # Normalize
    # Segment hashtags
    # ...