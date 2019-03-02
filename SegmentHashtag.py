import re
import sys


def partitioner(hashtag, words):
    while hashtag:
        word_found = longest_word(hashtag, words)
        yield word_found
        hashtag = hashtag[len(word_found):]

def longest_word(phrase, words):
    current_try = phrase
    while current_try:
        if current_try in words or current_try.lower() in words:
            return current_try
        current_try = current_try[:-1]
    # if nothing was found, return the original phrase
    return phrase

def partition_hashtag(text, words):
    return re.sub(r'#(\w+)', lambda m: ' '.join(partitioner(m.group(1), words)), text)

def read_dictionary_file(filename):
    with open(filename, 'rb') as f:
        return set(word.strip() for word in f)


if __name__ == '__main__':
    words = read_dictionary_file('corncob_lowercase.txt')
    segmented = partition_hashtag(sys.argv[1], words)
    segWords = segmented.split(" ")
    for i in range(0, len(segWords)):
        segWords[i] = '#'+segWords[i]
    finalHashtag = ' '.join(map(str, segWords))
    print(finalHashtag)

    #print(partition_hashtag("#iwanttogohome #freelesson #nosurprisethere #seaandwhitesands #sundaydateday #skateeverydamnday", words))