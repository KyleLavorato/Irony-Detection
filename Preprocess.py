import emoji

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
                tweet_PP1 = removeURLs(tweet)  # Preprocess stage 1
                tweet_PP2 = removeEmoji(tweet_PP1)
                corpus.append(tweet_PP2)


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
                emojiText = emoji.demojize(char).replace(":","")
                processedTweet.append(emojiText)
        else:
            processedTweet.append(char)
    newTweet = ''.join(map(str, processedTweet))
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