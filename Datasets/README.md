# Datasets

### SemEval Constrained Dataset

The dataset provided by SemEval for the task is located in `Train/` and `Test/`. These datasets are annotated separately for Subtask A and Subtask B where the classification is binary or multi-class irony.

### Unconstrained Pre-Training Dataset

The dataset that we collected from the Twitter API for pre-training is located in `../Pretraining/Data`. It is annotated for binary classification is is broken down into a 90% train and 10% test set.

---

### Feature Testing

In order to validate the success of the preprocessing custom dictionaries, we provide several feature ablation test sets. The test sets and features included are as follows:

* Test-Package-1:
	- Normalization of URLs, Usernames, etc and base emoji name translation (Eg. Face With Tears of Joy)
	- This is the baseline system
* Test-Package-2:
	- Slang correction from ekphrasis slang dictionary
	- Secondary baseline with an established slang translation
* Test-Package-3:
	- Full preprocessing pipeline with custom translations
	- Full effectiveness of custom preprocessing

