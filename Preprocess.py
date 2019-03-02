import emoji
import subprocess, sys
import unicodedata

def parse_dataset(fp):
    '''
    Loads the dataset .txt file with label-tweet on each line and parses the dataset.
    :param fp: filepath of dataset
    :return:
        corpus: list of tweet strings of each tweet.
        y: list of labels
    '''
    y = []
    corpus = []
    with open(fp, 'rt', encoding='utf8') as data_in:
        for line in data_in:
            if not line.lower().startswith("tweet index"): # discard first line if it contains metadata
                line = line.rstrip() # remove trailing whitespace
                label = int(line.split("\t")[1])
                tweet = line.split("\t")[2]
                y.append(label)
                tweet_PP1 = removeURLs(tweet)  # Preprocess stage 1: Remove any twitter link shortened URLS
                tweet_PP2 = removeEmoji(tweet_PP1)  # Preprocess stage 2: Take any emojis, decode them to text, and make them seperate words out of :pile_of_poo: form
                tweet_PP3 = segmentHashtag(tweet_PP2)  # Preprocess stage 3: Take all hashtags and attempt to segment them into seperate words; #freelesson -> #free #lesson (Has about 65% accuracy)
                # Notes for report: The corncob word dictionary may overfit the data; It matches words that are very uncommon to be used on twitter (eg environment -> environ ment)
                corpus.append(tweet_PP3)


    return corpus, y


def removeURLs(tweet):
    words = tweet.split(" ")
    processedTweet=[]
    for word in words:
        # Find all the words that have a url in them
        # Twitter link shortener is a set 22 or 23 chars depending on http or https
        if word.find("https://") != -1:
            if(len(word)>23):
                newWord = word[23:].replace("|","")
                processedTweet.append(newWord)
        elif word.find("http://") != -1:
            if(len(word)>22):
                newWord = word[22:].replace("|","")
                processedTweet.append(newWord)
        else:
            processedTweet.append(word)
    newTweet = ' '.join(map(str, processedTweet))
    return newTweet


def removeEmoji(tweet):
    processedTweet = []
    # Ensure each emoji is only in the tweet one time to prevent spam/overfitting
    # People often put several of the same emoji in a row
    usedEmoji = []
    for char in tweet:
        if char in emoji.UNICODE_EMOJI:
            if char not in usedEmoji:
                usedEmoji.append(char)
                emojiText = emoji.demojize(char).replace(":","").replace("_"," ")
                processedTweet.append(emojiText)
        else:
            processedTweet.append(char)
    newTweet = ''.join(map(str, processedTweet))
    return newTweet


def segmentHashtag(tweet):
    processedTweet = []
    words = tweet.split(" ")
    for word in words:
        # Find the words that have a hashtag
        hashtag_pos = word.find("#")

        # Add the word connected to the front of the hashtag back to the tweet
        # Eg. tree#wood
        if hashtag_pos > 0 and hashtag_pos != -1:
            processedTweet.append(word[:hashtag_pos])
        elif hashtag_pos == -1:
            processedTweet.append(word)  # Add the word that has no hashtag
        if hashtag_pos != -1:
            # If there are multiple hashtags without spaces
            hashtags = word.split("#")
            hashtags.pop(0)
            for tag in hashtags:
                restoredTag = "#"+tag  # Chop off the words before the hashtag and add the # back as it has been stripped
                segmentedTag = subprocess.check_output("\"D:\Program Files\Python27\python.exe\"" " " "\"SegmentHashtag.py\"" " " + restoredTag.replace("|","").replace(">"," ").replace("&","and"), shell=True)
                decodedTag = str.strip(segmentedTag.decode('ISO-8859-1'))
                processedTweet.append(decodedTag)
    newTweet = ' '.join(map(str, processedTweet))
    return newTweet


def printCorpus(corpus, y):
    for i in range(0, len(corpus)):
        print(y[i],"|",corpus[i])


if __name__ == "__main__":
    # Experiment settings

    DATASET_FP = "Datasets/Train/SemEval2018-T3-train-taskB_emoji.txt"

    # Loading dataset and featurised simple Tfidf-BoW model
    corpus, y = parse_dataset(DATASET_FP)

    printCorpus(corpus, y)