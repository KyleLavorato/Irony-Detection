import emoji #emoji
import random
from ekphrasis.classes.preprocessor import TextPreProcessor #ekphrasis
from ekphrasis.classes.tokenizer import SocialTokenizer
import csv, re, os # For slang translator

from Dictionaries.custom_emoticons import emoticons
from Dictionaries.slang_dict import slangdict
from settings import normalize_emoji
from settings import TEST_PACKAGE



# Run through 4 slang dictionaries for best results
    # Our custom one to add missed things from manual review
    # One of SMS abbreviations
    # One from the internet
    # One from ekphrasis
# They have overlap but all contain replacements that the others miss

# Source: https://www.webopedia.com/quick_ref/textmessageabbreviations.asp + Manual revisions
# Manually reviewed to fix duplicates and add swear words; Added some missing slang misspellings
    # Slang added Eg. da -> the, ur -> you are, y -> why, v -> very, b -> be, etc.
    # True slang meaning replaced for some acronyms; Eg. lol -> Laughing (not laugh out loud; Nobody means that with it), SYS -> System (Not See You Soon)
# Manually reviewed to remove acronyms that are common words and not intended to be acronyms
    # Eg. so -> Significant Other, we -> Whatever, gas -> Got a Second, sir -> strike it rich, bag -> Busting a Gut
    # The dictionary is very extensive and carries data that is rarely every used
# Manually added slang missed by ekphrasis such as contractions without '
    # CANT -> Can not; Ekphrasis leaves as cant
# Occasional issue not processing non-letter characters he'll -> hell -> <swear>

# The emoji dictionary was manually written to capture the real meaning/emotion of each emoji as
# the names of them contain garbage text and non-representitive emotions
    # Normalized emojis of the same general feeling to aid in generalizing training
    # Eg. All different hearts get normalized to <love> instead of :red_heart:, :green_heart:, :heart_with_arrow:
    # Eg. <Animal>, <Music>, <Sports>
# Modified ekphrasis emoticon dictionary to use same normalization terms used in our emojis; Added a few missing entries

def readDictionaries():
    slangDictionary = []
    swearDictionary = []
    emojiDictionary = []
    with open("Dictionaries/slang-dictionary.txt", "r") as f:
        # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            slangDictionary.append(row)
    with open("Dictionaries/swear-dictionary.txt", "r") as f:
        # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            swearDictionary.append(row)
    with open("Dictionaries/emoji-real-dictionary.txt", "r", encoding="utf-8") as f:
        # Reading file as CSV with delimiter as " = ", so that emojis are stored in row[0] and phrases in row[1]
        fileData = csv.reader(f, delimiter="=")
        for row in fileData:
            emojiDictionary.append(row)
    return slangDictionary, swearDictionary, emojiDictionary


def parseDataset(fp):
    y = []
    corpus = []
    with open(fp, 'rt', encoding='utf8') as data_in:
        next(data_in)
        for line in data_in:
            line = line.rstrip() # remove trailing whitespace
            label = int(line.split("\t")[1])
            tweet = line.split("\t")[2]
            y.append(label)
            corpus.append(tweet)

    return corpus, y


def preprocessCorpus(corpus, TEST_MODE):
    newCorpus = []

    slangDictionary, swearDictionary, emojiDictionary = readDictionaries()

    text_processor = TextPreProcessor(
        normalize=['url', 'money', 'phone', 'user', 'time', 'date'],
        annotate={"hashtag", "allcaps", "elongated"},
        fix_html=True,
        segmenter="twitter",
        corrector="twitter",
        unpack_hashtags=True,  # perform word segmentation on hashtags
        unpack_contractions=True,  # Unpack contractions (can't -> can not)
        spell_correct_elong=False,  # spell correction for elongated words
    )

    text_processor_test1 = TextPreProcessor(
        normalize=['url', 'money', 'phone', 'user', 'time', 'date'],
        fix_html=True,
    )

    text_tokenizer = TextPreProcessor(
        unpack_contractions=True,  # Unpack contractions (can't -> can not)
        spell_correct_elong=False,  # spell correction for elongated words
        tokenizer=SocialTokenizer(lowercase=True).tokenize,
        dicts =[emoticons, slangdict]
    )

    for tweet in corpus:
        if TEST_MODE <= 2:
            newTweet = "".join(text_processor_test1.pre_process_doc(tweet))
            newTweet = translateStdEmoji(newTweet)
        elif TEST_MODE == 2:
            newTweet = "".join(text_processor_test1.pre_process_doc(tweet))
            newTweet = deslangify(newTweet, slangDictionary, 0)
            newTweet = deslangify(newTweet, emojiDictionary, 0)
        else:
            newTweet = "".join(text_processor.pre_process_doc(tweet))
            newTweet = deslangify(newTweet, slangDictionary, 0)
            newTweet = deslangify(newTweet, swearDictionary, 0)
            newTweet = demoji(newTweet, emojiDictionary, 0)
            newTweet = " ".join(text_tokenizer.pre_process_doc(newTweet))  # Tokenizer should be last step after we apply our preprocessing
            newTweet = deslangify(newTweet, swearDictionary, 0)  # Take anoter swear word pass to get any new ones the tokenizer created
            newTweet = newTweet.replace("|","")
            newTweet = " ".join(text_tokenizer.pre_process_doc(newTweet))  # Retokenize to get rid of any extra spaces left by garbage removal
            if TEST_MODE == 77:
                newTweet = bertProcess(newTweet)
                newTweet = " ".join(text_tokenizer.pre_process_doc(newTweet))  # Retokenize to get rid of spaces from removed <XXXX> forms
        newCorpus.append(newTweet)

    return newCorpus


def translateStdEmoji(tweet):
    processedTweet = []
    for char in tweet:
        if char in emoji.UNICODE_EMOJI:
            emojiText = emoji.demojize(char)
            emojiText = emojiText.replace(":", " ")
            emojiText = emojiText.replace("_", " ")
            processedTweet.append(emojiText)
        else:
            processedTweet.append(char)
    return ''.join(map(str, processedTweet))


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


def demoji(tweet, dict, showReplacements):
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
                        if normalize_emoji and TEST_PACKAGE != 77:
                            usedEmoji.append(char)
                            processedTweet.append("<emoji>" + row[1] + "</emoji>")
                        else:
                            usedEmoji.append(char)
                            processedTweet.append(row[1])
        else:
            processedTweet.append(char)
    newTweet = ''.join(map(str, processedTweet))
    return newTweet


def bertProcess(tweet):
    newTweet = tweet.replace("<hashtag>", "hashtag")
    newTweet = newTweet.replace("</hashtag>", "")
    newTweet = newTweet.replace("<allcaps>", "allcaps")
    newTweet = newTweet.replace("</allcaps>", "")
    return newTweet


def printCorpus(corpus, y):
    for i in range(0, len(corpus)):
        print(y[i],"|",corpus[i])


def writeCorpus(corpus, y, fp):
    with open (fp, "w", encoding='utf8') as f:
        for i in range(0, len(corpus)):
            f.write(str(y[i]) + "|" + corpus[i]+ "\n")
    print("\nCorpus written to file")


if __name__ == "__main__":

    print("TEST MODE:", TEST_PACKAGE)

    DATASET_A_TRAIN = "../Datasets/Train/SemEval2018-T3-train-taskA_emoji.txt"
    DATASET_A_TEST = "../Datasets/Test/SemEval2018-T3_gold_test_taskA_emoji.txt"

    DATASET_B_TRAIN = "../Datasets/Train/SemEval2018-T3-train-taskB_emoji.txt"
    DATASET_B_TEST = "../Datasets/Test/SemEval2018-T3_gold_test_taskB_emoji.txt"

    PRETRAIN_RANDOM = "../Pretraining/Data/corpus-random-balanced.txt"
    PRETRAIN_IRONY = "../Pretraining/Data/corpus-irony-balanced.txt"

    # Loading and processing pre-training dataset
    pt_random_corpus, pt_random_scores = parseDataset(PRETRAIN_RANDOM)
    pt_irony_corpus, pt_irony_scores = parseDataset(PRETRAIN_IRONY)

    processed_pt_random_corpus = preprocessCorpus(pt_random_corpus, TEST_PACKAGE)
    processed_pt_irony_corpus = preprocessCorpus(pt_irony_corpus, TEST_PACKAGE)

    # Create combined pretraining dataset
    processed_pt_corpus = processed_pt_random_corpus + processed_pt_irony_corpus
    pt_scores = pt_random_scores + pt_irony_scores
    # Randomize order of dataset
    random_pt_corpus = []
    random_pt_scores = []
    for i in range(0, len(processed_pt_corpus)):
        index = random.randint(0,len(processed_pt_corpus)-1)
        random_pt_corpus.append(processed_pt_corpus.pop(index))
        random_pt_scores.append(pt_scores.pop(index))

    # Divide into train and test set
    ninetyIndex = round(len(random_pt_corpus) * 0.9)
    pt_corpus_train = random_pt_corpus[:ninetyIndex]
    pt_scores_train = random_pt_scores[:ninetyIndex]
    pt_corpus_test = random_pt_corpus[ninetyIndex:]
    pt_scores_test = random_pt_scores[ninetyIndex:]

    trainA_corpus, trainA_scores = parseDataset(DATASET_A_TRAIN)
    testA_corpus, testA_scores = parseDataset(DATASET_A_TEST)

    trainB_corpus, trainB_scores = parseDataset(DATASET_B_TRAIN)
    testB_corpus, testB_scores = parseDataset(DATASET_B_TEST)

    trainA_processed = preprocessCorpus(trainA_corpus, TEST_PACKAGE)
    testA_processed = preprocessCorpus(testA_corpus, TEST_PACKAGE)

    trainB_processed = preprocessCorpus(trainB_corpus, TEST_PACKAGE)
    testB_processed = preprocessCorpus(testB_corpus, TEST_PACKAGE)

    if TEST_PACKAGE <= 3:
        DIR_PKG = TEST_PACKAGE
    else:
        DIR_PKG = "BERT"

    DIR = "../Datasets/TEST-PACKAGE-" + str(DIR_PKG) + "/"
    writeCorpus(trainA_processed, trainA_scores, DIR + "train-taskA.txt")
    writeCorpus(testA_processed, testA_scores, DIR + "test-taskA.txt")
    writeCorpus(trainB_processed, trainB_scores, DIR + "train-taskB.txt")
    writeCorpus(testB_processed, testB_scores, DIR + "test-taskB.txt")
    writeCorpus(pt_corpus_train, pt_scores_train, DIR + "pretrain-train.txt")
    writeCorpus(pt_corpus_test, pt_scores_test, DIR + "pretrain-test.txt")

    os.remove("slangdict.pickle")  # Delete temporary file


## Preprocessing Goals in order:

# X Convert emoji's to true feeling meaning
    # X Custom manual normalized emoji dictionary
    # Could maybe replace them with a sentiment instead of an emotion <positive> or <negative>
# Convert text emoticons to feeling meaning

# X Replace acronyms and slang (eg r = are)
    # X Needs manual review to look for missed slang
# X Replace swear words with <swear> normalization
    # X Needs manual review to look for missed swears


# FUTURE WORK - Design a better spell check
# Abstain from using a spell checker; Despite the fact that words being spelled correctly are necessary for pretrained
# networks to understand them, the spell checkers make too many incorrect choices or replace words where no replacement
# should be make, like in the case of acronyms. At this time automated tools are not confident enough to make the replacement
# choices.

# Preprocessing library
    # Normalize
    # Segment hashtags
    # Spelling correction?
    # ...