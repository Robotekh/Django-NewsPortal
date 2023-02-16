# from django import template
#
# register = template.Library()
#
#
# @register.filter()
# def currency(value):
#     """
#    value: значение, к которому нужно применить фильтр
#    code: код валюты
#    """
#
#     def distance(a, b):
#         "Вычисляет дистанцию Левенштейна a and b."
#         n, m = len(a), len(b)
#         if n > m:
#             # Make sure n <= m, to use O(min(n, m)) space
#             a, b = b, a
#             n, m = m, n
#
#         current_row = range(n + 1)  # Keep current and previous row, not entire matrix
#         for i in range(1, m + 1):
#             previous_row, current_row = current_row, [i] + [0] * n
#             for j in range(1, n + 1):
#                 add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
#                 if a[j - 1] != b[i - 1]:
#                     change += 1
#                 current_row[j] = min(add, delete, change)
#
#         return current_row[n]
#
#     def check_word(phrase):
#         text = phrase
#         # Фраза, которую будем проверять.
#         phrase = phrase.lower().replace(" ", "")
#
#         d = {'а': ['а', 'a', '@'],
#              'б': ['б', '6', 'b'],
#              'в': ['в', 'b', 'v'],
#              'г': ['г', 'r', 'g'],
#              'д': ['д', 'd'],
#              'е': ['е', 'e'],
#              'ё': ['ё', 'e'],
#              'ж': ['ж', 'zh', '*'],
#              'з': ['з', '3', 'z'],
#              'и': ['и', 'u', 'i'],
#              'й': ['й', 'u', 'i'],
#              'к': ['к', 'k', 'i{', '|{'],
#              'л': ['л', 'l', 'ji'],
#              'м': ['м', 'm'],
#              'н': ['н', 'h', 'n'],
#              'о': ['о', 'o', '0'],
#              'п': ['п', 'n', 'p'],
#              'р': ['р', 'r', 'p'],
#              'с': ['с', 'c', 's'],
#              'т': ['т', 'm', 't'],
#              'у': ['у', 'y', 'u'],
#              'ф': ['ф', 'f'],
#              'х': ['х', 'x', 'h', '}{'],
#              'ц': ['ц', 'c', 'u,'],
#              'ч': ['ч', 'ch'],
#              'ш': ['ш', 'sh'],
#              'щ': ['щ', 'sch'],
#              'ь': ['ь', 'b'],
#              'ы': ['ы', 'bi'],
#              'ъ': ['ъ'],
#              'э': ['э', 'e'],
#              'ю': ['ю', 'io'],
#              'я': ['я', 'ya']
#              }
#
#         for key, value in d.items():
#             # Проходимся по каждой букве в значении словаря. То есть по вот этим спискам ['а', 'a', '@'].
#             for letter in value:
#                 # Проходимся по каждой букве в нашей фразе.
#                 for phr in phrase:
#                     # Если буква совпадает с буквой в нашем списке.
#                     if letter == phr:
#                         # Заменяем эту букву на ключ словаря.
#                         phrase = phrase.replace(phr, key)
#
#         with open('words.txt', 'r', encoding="utf-8") as f:  # Загружаем список плохих слов
#             words = f.read().splitlines()
#         # import os.path
#         #
#         # cur_dir = os.path.abspath(os.curdir)
#         # cur_file = os.path.abspath(__file__)
#         #
#         # print("Директория скрипта: " + cur_dir)
#         # print("Путь к файлу: " + cur_file)
#
#
#
#         #words = ['13', '12312']
#         # Проходимся по всем словам.
#
#         for word in words:
#             # Разбиваем слово на части, и проходимся по ним.
#             for part in range(len(phrase)):
#                 # Вот сам наш фрагмент.
#                 fragment = phrase[part: part + len(word)]
#                 # Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
#                 if distance(fragment, word) <= len(word) * 0.25:
#                     # Если они равны, заменяем найденное слово на * и помещаем в text.
#                     a = text.replace(word, word[0] + "*" * (len(word) - 1))
#                     b = a.replace(word[0].upper() + word[1:len(word)], word[0].upper() + "*" * (len(word) - 1))
#                     text = b
#
#         return text
#     return check_word(value)
