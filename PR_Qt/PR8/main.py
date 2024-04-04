# Задание 1
numbers = [10, 20, 30, 20, 40]
if 20 in numbers:
 index_20 = numbers.index(20)
 numbers[index_20] = 200
print(numbers)

# Задание 2
strings = ["hello", None, "world", " ", "python"]
filtered_strings = list(filter(lambda item: item is not None, strings))

print(filtered_strings)

# Задание 3
numbers = [1, 2, 3, 4, 5]
squared_numbers = [x**2 for x in numbers]
print(squared_numbers)

# Задание 4
numbers = [10, 20, 30, 20, 40]
numbers_without_20 = [x for x in numbers if x != 20]
print(numbers_without_20)
