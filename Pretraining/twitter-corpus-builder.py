import tweepy
import unicodedata
import datetime
import api-settings

auth = tweepy.auth.OAuthHandler(settings.publicAPI, settings.privateAPI)
auth.set_access_token(settings.publicAccess, settings.privateAccess)

api = tweepy.API(auth, wait_on_rate_limit=True)

IRONY_MODE = 0  # Select which type of tweets to search for
                # 0 - Random (Includes the word "the")
                # 1 - Ironic (Indludes the hashtag "#irony")

# Open/create a file to append data to
if IRONY_MODE:
    file = open('corpus-irony.txt', 'a', encoding="utf-8")
else:
    file = open('corpus-random.txt', 'a', encoding="utf-8")

counter = 0

if IRONY_MODE:
    # searchString = "#irony -filter:retweets"
    # searchString = "#not -filter:retweets"
    searchString = "#sarcasm -filter:retweets"
else:
    searchString = "the -filter:retweets"

now = datetime.datetime.now()
currentDate = str(now.year)+"-"+str(now.month)+"-"+str(now.day)
endRange = str(now.year)+"-"+str(now.month)+"-"+str(now.day-6)

while counter != 50000:
    for tweet in tweepy.Cursor(api.search,
                               q = searchString,
                               count=50000,
                               since = endRange,
                               until = currentDate,
                               tweet_mode="extended",
                               lang = "en").items():

        # Write a row to the file. I use encode UTF-8
        file.write(str.strip(unicodedata.normalize('NFKD',tweet.full_text)).replace("\n"," ")+"\n")
        counter = counter + 1
        if (counter % 200) == 0:
            print(counter)  # Show scraping progress
file.close()