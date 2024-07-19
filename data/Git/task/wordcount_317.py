import re

def word_count(text):
    # Preprocess the text: convert to lowercase and remove punctuation/special characters
    processed_text = re.sub(r'[^\w\s]', '', text.lower())

    # Split the text into a list of words
    words = processed_text.split()

    # Initialize an empty dictionary for counting words
    word_count_dict = {}

    # Count each word in the list
    for word in words:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1

    return word_count_dict

text = """
Got this panda plush toy for my daughter's birthday,
who loves it and takes it everywhere. It's soft and
super cute, and its face has a friendly look. It's
a bit small for what I paid though. I think there
might be other options that are bigger for the
same price. It arrived a day earlier than expected,
so I got to play with it myself before I gave it
to her.
"""

print(word_count(text))