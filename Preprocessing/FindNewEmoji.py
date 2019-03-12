import emoji #emoji
import csv, os # For slang translator

from settings import normalize_emoji



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
    corpus = []
    with open(fp, 'rt', encoding='utf8') as data_in:
        for line in data_in:
            line = line.rstrip() # remove trailing whitespace
            corpus.append(line)

    return corpus



emojiNotInDict = []
def demoji(tweet, dict, showReplacements, showNotInDict):
    # emoji.demojize(char) can be used to get actual name from emojis
    processedTweet = []
    usedEmoji = []
    # Ensure each emoji is only in the tweet one time to prevent spam/overfitting
    # People often put several of the same emoji in a row
    for char in tweet:
        if char in emoji.UNICODE_EMOJI:
            if char not in usedEmoji:
                if showNotInDict and (char not in emojiNotInDict):
                    exists = 0
                    for row in dict:
                        if char in row[0]:
                            exists = 1
                    if not exists:
                        emojiNotInDict.append(char)
                        with open("newEmoji.txt", "a", encoding="utf-8") as f:
                            f.write(char+"\n")
                for row in dict:
                    if char == row[0]:
                        if showReplacements:
                            print(tweet, end=" | ")
                            print(row[0],"->",row[1])
                        if normalize_emoji:
                            usedEmoji.append(char)
                            processedTweet.append("<emoji>" + row[1] + "</emoji>")
                        else:
                            usedEmoji.append(char)
                            processedTweet.append(row[1])
        else:
            processedTweet.append(char)
    newTweet = ''.join(map(str, processedTweet))
    return newTweet


if __name__ == "__main__":
    # Experiment settings

    slangDictionary, swearDictionary, emojiDictionary = readDictionaries()

    DATASET_FP = "../Pretraining/corpus-random.txt"

    corpus = parseDataset(DATASET_FP)

    for tweet in corpus:
        res = demoji(tweet, emojiDictionary, 0, 1)

    os.remove("slangdict.pickle")  # Delete temporary file

