from collections import Counter

task_text = """
Got this panda plush toy for my daughter's birthday,
who loves it and takes it everywhere. It's soft and
super cute, and its face has a friendly look. It's
a bit small for what I paid though. I think there
might be other options that are bigger for the
same price. It arrived a day earlier than expected,
so I got to play with it myself before I gave it
to her.
"""


def wordcount(text: str):
    text = text.lower()
    text = (
        text.replace("\n", " ")
        .replace(".", " ")
        .replace(",", " ")
        .replace("  ", " ")
        .strip()
    )
    return Counter(text.split(" "))


print(dict(wordcount(task_text)))
