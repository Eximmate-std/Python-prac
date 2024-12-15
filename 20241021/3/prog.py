import re
from collections import Counter

N = int(input())

text_lines = []
while True:
    line = input()
    if line == "":
        break
    text_lines.append(line)
text = " ".join(text_lines)

cleaned_text = re.sub(r'[^a-zA-Zs]', ' ', text).lower()
word_counts = Counter([word for word in cleaned_text.split() if len(word) == N])

if word_counts:
    max_count = max(word_counts.values())
    most_common_words = [word for word, count in word_counts.items() if count == max_count]
    most_common_words.sort()
    print(" ".join(most_common_words))
