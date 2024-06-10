# Дано предложение без знаков препинания.
# Превратить предложение в список слов.
# При помощи механизма map/filter/reduce найти количество слов,
# длина которых больше 4 и склеить их в одну строку

from functools import reduce

sentence = "искусственный интеллект не сравнится с природной глупостью"

words = sentence.split()

long_words = list(filter(lambda word: len(word) > 4, words))

count_long_words = len(long_words)

concatenated_words = reduce(lambda acc, word: acc + word, long_words, "")

print("Количество слов длиной больше 4:", count_long_words)
print("Склеенные слова:", concatenated_words)

