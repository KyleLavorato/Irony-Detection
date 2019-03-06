from settings import normalize_emoji

if normalize_emoji:
    emoticons = {
        ':*': '<emoji>kiss</emoji>',
        ':-*': '<emoji>kiss</emoji>',
        ':x': '<emoji>kiss</emoji>',
        ':-)': '<emoji>happy</emoji>',
        ':-))': '<emoji>happy</emoji>',
        ':-)))': '<emoji>happy</emoji>',
        ':-))))': '<emoji>happy</emoji>',
        ':-)))))': '<emoji>happy</emoji>',
        ':-))))))': '<emoji>happy</emoji>',
        ':)': '<emoji>happy</emoji>',
        ':))': '<emoji>happy</emoji>',
        ':)))': '<emoji>happy</emoji>',
        ':))))': '<emoji>happy</emoji>',
        ':)))))': '<emoji>happy</emoji>',
        ':))))))': '<emoji>happy</emoji>',
        ':)))))))': '<emoji>happy</emoji>',
        ':o)': '<emoji>happy</emoji>',
        ':]': '<emoji>happy</emoji>',
        ':3': '<emoji>happy</emoji>',
        ':c)': '<emoji>happy</emoji>',
        ':>': '<emoji>happy</emoji>',
        '=]': '<emoji>happy</emoji>',
        '8)': '<emoji>happy</emoji>',
        '=)': '<emoji>happy</emoji>',
        ':}': '<emoji>happy</emoji>',
        ':^)': '<emoji>happy</emoji>',
        '|;-)': '<emoji>happy</emoji>',
        ":'-)": '<emoji>happy</emoji>',
        ":')": '<emoji>happy</emoji>',
        '\o/': '<emoji>happy</emoji>',
        '*\\0/*': '<emoji>happy</emoji>',
        ':-D': '<emoji>laughing</emoji>',
        ':D': '<emoji>laughing</emoji>',
        # '(\':': '<emoji>laughing</emoji>',
        '8-D': '<emoji>laughing</emoji>',
        '8D': '<emoji>laughing</emoji>',
        'x-D': '<emoji>laughing</emoji>',
        'xD': '<emoji>laughing</emoji>',
        'X-D': '<emoji>laughing</emoji>',
        'XD': '<emoji>laughing</emoji>',
        '=-D': '<emoji>laughing</emoji>',
        '=D': '<emoji>laughing</emoji>',
        '=-3': '<emoji>laughing</emoji>',
        '=3': '<emoji>laughing</emoji>',
        'B^D': '<emoji>laughing</emoji>',
        '>:[': '<emoji>sad</emoji>',
        ':-(': '<emoji>sad</emoji>',
        ':-((': '<emoji>sad</emoji>',
        ':-(((': '<emoji>sad</emoji>',
        ':-((((': '<emoji>sad</emoji>',
        ':-(((((': '<emoji>sad</emoji>',
        ':-((((((': '<emoji>sad</emoji>',
        ':-(((((((': '<emoji>sad</emoji>',
        ':(': '<emoji>sad</emoji>',
        ':((': '<emoji>sad</emoji>',
        ':(((': '<emoji>sad</emoji>',
        ':((((': '<emoji>sad</emoji>',
        ':(((((': '<emoji>sad</emoji>',
        ':((((((': '<emoji>sad</emoji>',
        ':(((((((': '<emoji>sad</emoji>',
        ':((((((((': '<emoji>sad</emoji>',
        ':-c': '<emoji>sad</emoji>',
        ':c': '<emoji>sad</emoji>',
        ':-<': '<emoji>sad</emoji>',
        ':<': '<emoji>sad</emoji>',
        ':-[': '<emoji>sad</emoji>',
        ':[': '<emoji>sad</emoji>',
        ':{': '<emoji>sad</emoji>',
        ':-||': '<emoji>sad</emoji>',
        ':@': '<emoji>sad</emoji>',
        ":'-(": '<emoji>sad</emoji>',
        ":'(": '<emoji>sad</emoji>',
        'D:<': '<emoji>sad</emoji>',
        'D:': '<emoji>sad</emoji>',
        'D8': '<emoji>sad</emoji>',
        'D;': '<emoji>sad</emoji>',
        'D=': '<emoji>sad</emoji>',
        'DX': '<emoji>sad</emoji>',
        'v.v': '<emoji>sad</emoji>',
        "D-':": '<emoji>sad</emoji>',
        '(>_<)': '<emoji>sad</emoji>',
        ':|': '<emoji>sad</emoji>',
        '>:O': '<emoji>surprised</emoji>',
        ':-O': '<emoji>surprised</emoji>',
        ':-o': '<emoji>surprised</emoji>',
        ':O': '<emoji>surprised</emoji>',
        '°o°': '<emoji>surprised</emoji>',
        'o_O': '<emoji>surprised</emoji>',
        'o_0': '<emoji>surprised</emoji>',
        'o.O': '<emoji>surprised</emoji>',
        'o-o': '<emoji>surprised</emoji>',
        '8-0': '<emoji>surprised</emoji>',
        '|-O': '<emoji>surprised</emoji>',
        ';-)': '<emoji>wink</emoji>',
        ';)': '<emoji>wink</emoji>',
        '*-)': '<emoji>wink</emoji>',
        '*)': '<emoji>wink</emoji>',
        ';-]': '<emoji>wink</emoji>',
        ';]': '<emoji>wink</emoji>',
        ';D': '<emoji>wink</emoji>',
        ';^)': '<emoji>wink</emoji>',
        ':-,': '<emoji>wink</emoji>',
        '>:P': '<emoji>laughing</emoji>',
        ':-P': '<emoji>laughing</emoji>',
        ':P': '<emoji>laughing</emoji>',
        'X-P': '<emoji>laughing</emoji>',
        'x-p': '<emoji>laughing</emoji>',
        'xp': '<emoji>laughing</emoji>',
        'XP': '<emoji>laughing</emoji>',
        ':-p': '<emoji>laughing</emoji>',
        ':p': '<emoji>laughing</emoji>',
        '=p': '<emoji>laughing</emoji>',
        ':-Þ': '<emoji>laughing</emoji>',
        ':Þ': '<emoji>laughing</emoji>',
        ':-b': '<emoji>laughing</emoji>',
        ':b': '<emoji>laughing</emoji>',
        ':-&': '<emoji>laughing</emoji>',
        '>:\\': '<emoji>annoyed</emoji>',
        '>:/': '<emoji>annoyed</emoji>',
        ':-/': '<emoji>annoyed</emoji>',
        ':-.': '<emoji>annoyed</emoji>',
        ':/': '<emoji>annoyed</emoji>',
        ':\\': '<emoji>annoyed</emoji>',
        '=/': '<emoji>annoyed</emoji>',
        '=\\': '<emoji>annoyed</emoji>',
        ':L': '<emoji>annoyed</emoji>',
        '=L': '<emoji>annoyed</emoji>',
        ':S': '<emoji>annoyed</emoji>',
        '>.<': '<emoji>annoyed</emoji>',
        ':-|': '<emoji>annoyed</emoji>',
        '<:-|': '<emoji>annoyed</emoji>',
        ':-X': '<emoji>quiet</emoji>',
        ':X': '<emoji>quiet</emoji>',
        ':-#': '<emoji>quiet</emoji>',
        ':#': '<emoji>quiet</emoji>',
        'O:-)': '<emoji>angel</emoji>',
        '0:-3': '<emoji>angel</emoji>',
        '0:3': '<emoji>angel</emoji>',
        '0:-)': '<emoji>angel</emoji>',
        '0:)': '<emoji>angel</emoji>',
        '0;^)': '<emoji>angel</emoji>',
        '>:)': '<emoji>devil</emoji>',
        '>:D': '<emoji>devil</emoji>',
        '>:-D': '<emoji>devil</emoji>',
        '>;)': '<emoji>devil</emoji>',
        '>:-)': '<emoji>devil</emoji>',
        '}:-)': '<emoji>devil</emoji>',
        '}:)': '<emoji>devil</emoji>',
        '3:-)': '<emoji>devil</emoji>',
        '3:)': '<emoji>devil</emoji>',
        'o/\o': '<emoji>high five</emoji>',
        '^5': '<emoji>high five</emoji>',
        '>_>^': '<emoji>high five</emoji>',
        '^<_<': '<emoji>high five</emoji>',  # todo:fix tokenizer - MISSES THIS
        '<3': '<emoji>love</emoji>',
        '<33': '<emoji>love</emoji>',
        '<333': '<emoji>love</emoji>',
        '<3333': '<emoji>love</emoji>',
        '</3': '<emoji>no love</emoji>',
        '</33': '<emoji>no love</emoji>',
    }
else:
    emoticons = {
        ':*': '<kiss>',
        ':-*': '<kiss>',
        ':x': '<kiss>',
        ':-)': '<happy>',
        ':-))': '<happy>',
        ':-)))': '<happy>',
        ':-))))': '<happy>',
        ':-)))))': '<happy>',
        ':-))))))': '<happy>',
        ':)': '<happy>',
        ':))': '<happy>',
        ':)))': '<happy>',
        ':))))': '<happy>',
        ':)))))': '<happy>',
        ':))))))': '<happy>',
        ':)))))))': '<happy>',
        ':o)': '<happy>',
        ':]': '<happy>',
        ':3': '<happy>',
        ':c)': '<happy>',
        ':>': '<happy>',
        '=]': '<happy>',
        '8)': '<happy>',
        '=)': '<happy>',
        ':}': '<happy>',
        ':^)': '<happy>',
        '|;-)': '<happy>',
        ":'-)": '<happy>',
        ":')": '<happy>',
        '\o/': '<happy>',
        '*\\0/*': '<happy>',
        ':-D': '<laughing>',
        ':D': '<laughing>',
        # '(\':': '<laughing>',
        '8-D': '<laughing>',
        '8D': '<laughing>',
        'x-D': '<laughing>',
        'xD': '<laughing>',
        'X-D': '<laughing>',
        'XD': '<laughing>',
        '=-D': '<laughing>',
        '=D': '<laughing>',
        '=-3': '<laughing>',
        '=3': '<laughing>',
        'B^D': '<laughing>',
        '>:[': '<sad>',
        ':-(': '<sad>',
        ':-((': '<sad>',
        ':-(((': '<sad>',
        ':-((((': '<sad>',
        ':-(((((': '<sad>',
        ':-((((((': '<sad>',
        ':-(((((((': '<sad>',
        ':(': '<sad>',
        ':((': '<sad>',
        ':(((': '<sad>',
        ':((((': '<sad>',
        ':(((((': '<sad>',
        ':((((((': '<sad>',
        ':(((((((': '<sad>',
        ':((((((((': '<sad>',
        ':-c': '<sad>',
        ':c': '<sad>',
        ':-<': '<sad>',
        ':<': '<sad>',
        ':-[': '<sad>',
        ':[': '<sad>',
        ':{': '<sad>',
        ':-||': '<sad>',
        ':@': '<sad>',
        ":'-(": '<sad>',
        ":'(": '<sad>',
        'D:<': '<sad>',
        'D:': '<sad>',
        'D8': '<sad>',
        'D;': '<sad>',
        'D=': '<sad>',
        'DX': '<sad>',
        'v.v': '<sad>',
        "D-':": '<sad>',
        '(>_<)': '<sad>',
        ':|': '<sad>',
        '>:O': '<surprised>',
        ':-O': '<surprised>',
        ':-o': '<surprised>',
        ':O': '<surprised>',
        '°o°': '<surprised>',
        'o_O': '<surprised>',
        'o_0': '<surprised>',
        'o.O': '<surprised>',
        'o-o': '<surprised>',
        '8-0': '<surprised>',
        '|-O': '<surprised>',
        ';-)': '<wink>',
        ';)': '<wink>',
        '*-)': '<wink>',
        '*)': '<wink>',
        ';-]': '<wink>',
        ';]': '<wink>',
        ';D': '<wink>',
        ';^)': '<wink>',
        ':-,': '<wink>',
        '>:P': '<laughing>',
        ':-P': '<laughing>',
        ':P': '<laughing>',
        'X-P': '<laughing>',
        'x-p': '<laughing>',
        'xp': '<laughing>',
        'XP': '<laughing>',
        ':-p': '<laughing>',
        ':p': '<laughing>',
        '=p': '<laughing>',
        ':-Þ': '<laughing>',
        ':Þ': '<laughing>',
        ':-b': '<laughing>',
        ':b': '<laughing>',
        ':-&': '<laughing>',
        '>:\\': '<annoyed>',
        '>:/': '<annoyed>',
        ':-/': '<annoyed>',
        ':-.': '<annoyed>',
        ':/': '<annoyed>',
        ':\\': '<annoyed>',
        '=/': '<annoyed>',
        '=\\': '<annoyed>',
        ':L': '<annoyed>',
        '=L': '<annoyed>',
        ':S': '<annoyed>',
        '>.<': '<annoyed>',
        ':-|': '<annoyed>',
        '<:-|': '<annoyed>',
        ':-X': '<quiet>',
        ':X': '<quiet>',
        ':-#': '<quiet>',
        ':#': '<quiet>',
        'O:-)': '<angel>',
        '0:-3': '<angel>',
        '0:3': '<angel>',
        '0:-)': '<angel>',
        '0:)': '<angel>',
        '0;^)': '<angel>',
        '>:)': '<devil>',
        '>:D': '<devil>',
        '>:-D': '<devil>',
        '>;)': '<devil>',
        '>:-)': '<devil>',
        '}:-)': '<devil>',
        '}:)': '<devil>',
        '3:-)': '<devil>',
        '3:)': '<devil>',
        'o/\o': '<high five>',
        '^5': '<high five>',
        '>_>^': '<high five>',
        '^<_<': '<high five>',  # todo:fix tokenizer - MISSES THIS
        '<3': '<love>',
        '<33': '<love>',
        '<333': '<love>',
        '<3333': '<love>',
        '</3': '<no love>',
        '</33': '<no love>',
    }