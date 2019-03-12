# Preprocessing Dictionaries

An important step in the preprocessing of data for analysis is the sanitizing of the input. In the case of twitter, many users write in "SMS" or "texting" style slang, which must be translated to proper English.

To translate this slang to English, we use custom and sourced dictionaries that can translate the slang terms into their correct English representation

> The resulting translation from all dictionaries was also manually reviewed for incorrect, missing or improper translations and all dictionaries were respectively modified.

---

##Slang Translation

### slang-dictionary.txt
##### Custom and Sourced

This dictionary was initially sourced from Webopedia in their [Online Chat Abbreviations](https://www.webopedia.com/quick_ref/textmessageabbreviations.asp) Database. It mostly consists of abbreviations that people would use in their text conversations to avoid typing large phrases. We manually reviewed and added many entries to this dictionary as well to resolve issues:

* Obscure terms that also represent real words
 * Eg. gas → Got a Second | sir → strike it rich | bag → Busting a Gut
* Change the translation of terms from their acronym to their true current slang use
 * LoL → Laughing (Not "Laugh out Loud")
* Addition of slang spellings
 * Eg. da → the | y → why | v → very
* Added terms missed by all other sourced dictionaries

### slang_dict.py
##### Sourced

This dictionary was sourced from the python library (ekphrasis)[https://github.com/cbaziotis/ekphrasis]. It is a large dataset consisting mostly of slang spellings of words and the correction to the correct word. It also includes more recent informal abbreviations then the Webopedia dictionary with much more of a slang focus. Slight changes were made from the base ekphrasis version for usability as it suffers from "over-slanging":

* Removal of some slang terms that not commonly used as slang
 * Eg. FT → F**k That (Often means "Full Time" in today's twitter speak, not the slang meaning)

---
 
## Emoji Translation

### emoji-real-dictionary.txt
##### Custom

A common issue with current emoji translation dictionaries, such as (ekphrasis)[https://github.com/cbaziotis/ekphrasis] or (emoji)[https://pypi.org/project/emoji/] is they translate the literal developer emoji text as defined in (Emojipedia)[https://emojipedia.org/].

* 🙂 → Slightly Smiling Face
* 😂 → Face With Tears of Joy
* ❤ → Red Heart
* 💩 → Pile of Poo

By definition an emoji is "*a small digital image or icon used to express an emotion*". These translations while defining the small picture, do not portray the emotion it captures. In addition, they carry extra text that is not important to the meaning, which will cause a neural network to have more difficulty understanding the meaning from ambiguous or extra terms. 

The translations should be kept simple and demonstrate the **emotion** of the emoticon only. In addition, in the twitter language space, many emojis are commonly used adversely from their depicted emotion, creating a new **slang definition** for its use. Therefore this dictionary considers primarily the slang definitions where present and then the true emotion definition as a second.

* 🙂 → Happy
* 😂 → Laughing
* ❤ → Love
* 💩 → Sh*t

##### Normalization

To aid in learning from translations from this dictionary, we also apply normalization to the emojis. In the set of all emojis, there are multiple emojis that all express the same emotion, either by slang or normal definition. These are also often used sequentially to add variety to a message while expressing the sentiment as more powerful.

> That was a very memorable new years kiss 💘💋❤️ #lovemyrelationship

In this message, the author is using all love centered emojis that all mean the same, while looking slightly different. Therefore in the dictionary, these should all translate to *Love*.

In addition to this similar emotion normalization, we also normalize non-emotions. Since emojis have evolved past emotions to also include subjects such as food, animals, sports, etc., we want to normalize these for better learning. Therefore we define set categories and translate "noun" emojis to whichever category these fit in best.

##### Future Considerations

One emoji concept that this dictionary does not handle in its current form is *emoji sentences*. This is a set of emojis sequentially in text that are selected and arranged to provide an alternative meaning to our emotion definition.

> Yay I love being awake at 5 in the morning 😀🔫 

The emoji sequence here is used to portray *shoot self in head* to express that the author is very unhappy about their current task. The dictionary translation for this set will translate it to *very happy gun*, which does not successfully capture the correct sentiment.

###### Disclaimer
This is not a fully comprehensive dictionary of all emojis like Webopedia due to the sheer effort required in manually defining every emoji. As this is a twitter based dictionary, we have sampled 1000k tweets from the date 03/02/2019 - 03/15-2019

This dictionary is provided as open source and may be used in any non-commercial application. If you use this dictionary in any research or other application, please credit this repository as the source. If you have any improvements or would like to expand the dictionary, please submit a pull request with your revisions.

### custom_emoticons.py
##### Sourced and Extended

The most basic form of expression emotion over text are chat emoticons. Like emojis, they are simple faces created from typed symbols to express simple emotions. This dictionary is sourced from the ekphrasis python library, where it translates basic emoticons to the emotion that they represent. We have modified some of the translations in the dictionary to match the same terminology as our custom emoji dictionary to keep the translation learning consistent. In addition, we have also done a manual random sampling of twitter data to look for any emoticons that are not present in the dictionary and have added translations for them.

---

## Swearing Translation

### swear-dictionary.txt
##### Custom

Vulgar language and swearing is very common in today's dialect and slang. The exact meaning of swear words has changed over time, as well as which words are considered swears. Words that in the past or in proper English had a real meaning, can now be considered swear words with a different definition. Overall, all swear words contain a negative connotation and additional emphasis of feeling. Therefore we use this dictionary to normalize all swear words in tweets to a **<swear>** token. This will allow a neural network to not get confused with the meaning of words and learn their true sentiment.

The dictionary was created from sampling tweets and digital media to search for the different base swear words, or words used as vulgar in the majority of their uses. Since there is no fine line on what is considered a swear, we have included some negative words that may not be considered a swear word by all in today's dialect.

Further sampling was done on tweets to find all the alternate and misspellings of the base swear words as the dictionary replacements operate on exact match.

##### Future Considerations

As previously mentioned, it can be argued that all swear words do not carry the same emotional impact that others do. Our dictionary translates all swear words to a static neutral emphasis. It may be worthwhile to expand the dictionary to label emphasis/impact of each word. All the base words could be categorized into different emphasis levels and have that added to the <swear> token for additional learning.

This is not a fully comprehensive dictionary of all swear words and spellings. With vulgar words constantly changing it is very difficult to have all words represented. Combine that with common improper and creative spellings of swears and the task becomes even more difficult. Adding to this dictionary is a manual process where tweets must be manually scanned for new swear words and misspellings and will be expanded over time.