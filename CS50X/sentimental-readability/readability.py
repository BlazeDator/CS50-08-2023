import re

text = input("Text: ")

# This re findall command will capture all letters, so len(letters), is all the letters
checker = re.findall("[a-zA-Z]", text)
letters = len(checker)
# This re findall command will capture all words, by looking for parts of the strings that start alphanumerical
# and end alphanumerical, so whenever something appears, like a space it stops counting(also apostrophes and hyphens)
checker = re.findall("[\w'-]*[\w]", text)
words = len(checker)
# This findall is configured for counting the punctuation, so when i do len() I know how many sentences
checker = re.findall("[!?.]", text)
sentences = len(checker)

# the Coleman-Liau index
# 0.0588 * L - 0.296 * S - 15.8
# where L is the average number of letters per 100 words in the text
# and S is the average number of sentences per 100 words in the text

L = (letters * 100) / words
S = (sentences * 100) / words

grade = 0.0588 * L - 0.296 * S - 15.8
grade = round(grade)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print("Grade: ", grade)

