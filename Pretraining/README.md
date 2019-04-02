# System Pretraining

The system was pretrained on a dataset of 11k tweets scraped from the Twitter API during the time period of 03/02/2019 to 03/15-2019. These Tweets are all randomly selected from the API, with no particular subject matter. There is also a dataset of 5k ironic tweets, identified by the hashtags #irony, #not and #sarcasm, with those hashtags removed.

The data was scraped using the python script `twitter-corpus-builder.py` using valid developer API credentials. If you wish to use the script yourself, you must have access to the Twitter developer API.