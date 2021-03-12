# Irony-Detection

In this repository we present a deep-learning system constructed to solve the [SemEval-2018 Task 3 "Irony Detection in English Tweets"](https://www.aclweb.org/anthology/S18-1005/). We solve both subtasks of the problem, involving detecting if irony is present in a tweet and classifying that irony by type. We use Keras to create TensorFlow Dense LSTM networks with deep learning to accomplish this goal. The input to our system is cleaned and normalized with a custom slang preprocessing system. Both our text processing pipeline and model are available in this repository. Also, we present an adaption of the BERT transformer architecture to this task for results comparison. Our results show an F1 score of 0.6500 and 0.5076 for Subtask A and B which would rank us 1st and 3rd in accordance with the official rankings of the competition.

### Dataset

Training was done with a constrained and unconstrained dataset. The constrained set was provided by the SemEval task and the unconstrained dataset was scraped using the twitter API as an additional training set. Details on the datasets used can be found [here](https://github.com/KyleLavorato/Irony-Detection/tree/master/Datasets)

### Pre-Processing

The datasets were pre-processed before feeding them to the network. Pre-processing was completed with a python script that uses custom emoji and slang dictionaries to normalize the data to a form that the network can more easily understand. The full details of the pre-processing translations can be found [here](https://github.com/KyleLavorato/Irony-Detection/tree/master/Preprocessing/Dictionaries)

### Pre-Training

The system was pre-trained using a dataset of 11k tweets scraped from the twitter API that were randomly selected. The constrained dataset of 5k tweets with irony hashtags (hashtags removed from messages) was also used for training.

### IEEE Research Paper

A full IEEE research paper on the results of the created network is available in this repository. The unpublished paper is available as [Irony_Detection_in_Tweets_IEEE_Paper](https://github.com/KyleLavorato/Irony-Detection/blob/master/Irony_Detection_in_Tweets_IEEE_Paper.pdf)

