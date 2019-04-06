normalize_emoji = 1
TEST_PACKAGE=77

## Test Package Modes:
# 1 - Minor preprocessing; Only normalization of Usernames and URLs; Translation of emoji to std definition
# 2 - Most preprocessing; Our slang correction and emoji translation
# 3 - Major preprocessing; Full pipeline with custom dictionaries
# 77 - BERT Mode; Elimination of <XXX></XXX> tags that bert has issues with