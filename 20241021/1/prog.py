def count_unique_letter_pairs(text):
    text = text.lower()

    unique_pairs = set()

    for i in range(len(text) - 1):
        if text[i].isalpha() and text[i + 1].isalpha():
            pair = text[i] + text[i + 1]
            unique_pairs.add(pair)

    return len(unique_pairs)


print(count_unique_letter_pairs(input()))