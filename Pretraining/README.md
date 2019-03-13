# System Pretraining

The system was pretrained on a dataset of 650k tweets scraped from the Twitter API during the time period of 03/02/2019 to 03/15-2019. These Tweets are all randomly selected from the API, with no particular subject matter. There is also a dataset of 5k ironic tweets, identified by the hashtags #irony, #not and #sarcasm, with those hashtags removed.

The data was scraped using the python script `twitter-corpus-builder.py` using valid developer API credentials. If you wish to use the script yourself, you must have access to the Twitter developer API.

The script `PreprocessPretraining.py` will clean the pretraining dataset and apply the preprocessing pipeline from the preprocessing [script](../Preprocessing/Preprocess.py)

### Dataset

Due to Twitter's devoleper [terms of use](https://developer.twitter.com/en/developer-terms/agreement-and-policy.html) the dataset is not publicly available. If you wish to gain access via the encryption key, please get in contact with us with your use case for the data.