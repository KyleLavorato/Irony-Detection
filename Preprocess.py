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
    # Slang added Eg. da -> the, ur -> you are, y -> why, v -> very, b -> be, etc.
    # True slang meaning replaced for some acronyms; Eg. lol -> Laughing (not laugh out loud; Nobody means that with it), SYS -> System (Not See You Soon)
# Manually reviewed to remove acronyms that are common words and not intended to be acronyms
    # Eg. so -> Significant Other, we -> Whatever, gas -> Got a Second, sir -> strike it rich, bag -> Busting a Gut
    # The dictionary is very extensive and carries data that is rarely every used
# Occasional issue not processing non-letter characters he'll -> hell -> <swear>

# The emoji dictionary was manually written to capture the real meaning/emotion of each emoji as
# the names of them contain garbage text and non-representitive emotions
    # Normalized emojis of the same general feeling to aid in generalizing training
    # Eg. All different hearts get normalized to <love> instead of :red_heart:, :green_heart:, :heart_with_arrow:
    # Eg. <Animal>, <Music>, <Sports>
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
    emojiDictionary = []
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
    with open("emoji-real-dictionary.txt", "r", encoding="utf-8") as f:
        # Reading file as CSV with delimiter as " = ", so that emojis are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            emojiDictionary.append(row)
    return slangDictionary, swearDictionary, emojiDictionary


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

    slangDictionary, swearDictionary, emojiDictionary = readDictionaries()

    # text_processor = TextPreProcessor(
    #     normalize=['url', 'money', 'phone', 'user', 'time', 'date'],
    #     annotate={"hashtag", "allcaps", "elongated"},
    #     fix_html=True,
    #     segmenter="twitter",
    #     corrector="twitter",
    #     unpack_hashtags=True,  # perform word segmentation on hashtags
    #     unpack_contractions=True,  # Unpack contractions (can't -> can not)
    #     spell_correct_elong=False,  # spell correction for elongated words
    #     # tokenizer=SocialTokenizer(lowercase=True).tokenize,
    # )
    for tweet in corpus:
        # newTweet = "".join(text_processor.pre_process_doc(tweet))
        newTweet = deslangify(tweet, slangDictionary, 0)
        newTweet = deslangify(newTweet, swearDictionary, 0)
        newTweet = demoji(newTweet, emojiDictionary, 0, 1)
        newCorpus.append(newTweet)

    # nn = []
    # sp = SpellCorrector(corpus="english")
    # for tweet in newCorpus:
    #     for word in tweet:
    #         print(sp.correct(word))
    return newCorpus


def deslangify(user_string, dict, showReplacements):
    user_string = user_string.split(" ")
    j = 0
    for _str in user_string:
        # Removing Special Characters.
        _str = re.sub('[^a-zA-Z0-9-_.]', '', _str)
        for row in dict:
            # Check if selected word matches short forms[LHS] in text file.
            if _str.upper() == row[0]:
                if showReplacements:
                    # Print the tweet before deslangify and show replacement
                    # If match found replace it with its Abbreviation in text file.
                    print(" ".join(user_string), end=" | ")
                    user_string[j] = row[1]
                    print(row[0],"->",row[1])
                else:
                    # If match found replace it with its Abbreviation in text file.
                    user_string[j] = row[1]
        j = j + 1
    # Replacing commas with spaces for final output.
    return ' '.join(user_string)


def demoji(tweet, dict, showReplacements, tagging):
    # emoji.demojize(char) can be used to get actual name from emojis
    processedTweet = []
    usedEmoji = []
    # Ensure each emoji is only in the tweet one time to prevent spam/overfitting
    # People often put several of the same emoji in a row
    for char in tweet:
        if char in emoji.UNICODE_EMOJI:
            if char not in usedEmoji:
                for row in dict:
                    if char == row[0]:
                        if showReplacements:
                            print(tweet, end=" | ")
                            print(row[0],"->",row[1])
                        if tagging:
                            usedEmoji.append(char)
                            processedTweet.append("<emoji>" + row[1] + "</emoji>")
                        else:
                            usedEmoji.append(char)
                            processedTweet.append(row[1])
        else:
            processedTweet.append(char)
    newTweet = ''.join(map(str, processedTweet))
    return newTweet


def printCorpus(corpus, y):
    for i in range(0, len(corpus)):
        print(y[i],"|",corpus[i])


def writeCorpus(corpus, y):
    with open ("processed-corups.txt", "w", encoding='utf8') as f:
        for i in range(0, len(corpus)):
            f.write(str(y[i]) + " | " + corpus[i]+ "\n")
    print("\nCorpus written to file")


if __name__ == "__main__":
    # Experiment settings

    buildSlangDict()  # Build the slang dictionary from source

    DATASET_FP = "Datasets/Train/SemEval2018-T3-train-taskB_emoji.txt"

    # Loading dataset and featurised simple Tfidf-BoW model
    corpus, y = parseDataset(DATASET_FP)

    processedCorpus = preprocessCorpus(corpus)

    #printCorpus(processedCorpus, y)
    #writeCorpus(processedCorpus, y)


## Preprocessing Goals in order:

# X Convert emoji's to true feeling meaning
    # X Custom manual normalized emoji dictionary
# Convert text emoticons to feeling meaning

# X Replace acronyms and slang (eg r = are)
    # X Needs manual review to look for missed slang
# X Replace swear words with <swear> normalization
    # X Needs manual review to look for missed swears

# Preprocessing library
    # Normalize
    # Segment hashtags
    # Spelling correction?
    # ...