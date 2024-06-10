# 7. Дано предложение без знаков препинания. Превратить предложение в список слов. При помощи механизма
# map/filter/reduce отбросить у каждого слова последнюю букву и склеить в одну строку те обрезанные слова,
# длина которых больше 5.

from functools import reduce

sentence = "это пример предложения без знаков препинания для демонстрации кода"

words = sentence.split()
def remove_last_char(word):
    return word[:-1]

modified_words = map(remove_last_char, words)

filtered_words = filter(lambda word: len(word) > 5, modified_words)

result = reduce(lambda acc, word: acc + word, filtered_words, "")

print(result)
