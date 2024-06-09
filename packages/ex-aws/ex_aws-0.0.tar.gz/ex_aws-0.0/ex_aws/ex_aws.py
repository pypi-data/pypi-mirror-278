def sort():
    """# СОРТИРОВКИ
# 1. пузырьком (bubble_sort)
def bubble_sort(a, reverse):
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if reverse == False:
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
            else:
                if a[j] < a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
    return a
bubble_sort([1, 6, 3, -5, 111, 9], False)

# 2. шейкерная сортировка (cocktail shaker sort)
def cocktail_shaker_sort(a, reverse):
    left = 0
    right = len(a) - 1
    flag = right
    while left < right:
        for i in range(left, right):
            if (not reverse and a[i] > a[i + 1]) or (reverse and a[i] < a[i + 1]):
                a[i], a[i + 1] = a[i + 1], a[i]
                flag = i
        right = flag
        for i in range(right, left, -1):
            if (not reverse and a[i] < a[i - 1]) or (reverse and a[i] > a[i - 1]):
                a[i], a[i - 1] = a[i - 1], a[i]
                flag = i
        left = flag
    return a
cocktail_shaker_sort([1, 6, 3, -5, 111, 9], False)

# 3. сортировка расческой (comb sort)
def comb_sort(a, reverse):
    step = int(len(a) / 1.247)
    swap = 1
    while step > 1 or swap > 0:
        swap = 0
        i = 0
        while i + step < len(a):
            if (not reverse and a[i] > a[i + step]) or (reverse and a[i] < a[i + step]):
                a[i], a[i + step] = a[i + step], a[i]
                swap += 1
            i = i + 1
        if step > 1:
            step = int(step / 1.247)
    return a
comb_sort([1, 6, 3, -5, 111, 9], True)

# 4. выбором (selection sort)
def selection_sort(a, reverse):
    n = len(a)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if (not reverse and a[j] < a[min_index]) or (reverse and a[j] > a[min_index]):
                min_index = j
        if i != min_index:
            a[min_index], a[i] = a[i], a[min_index]
    return a
selection_sort([1, 6, 3, -5, 9, 11], False)

# 5. вставсками (insertion sort)
def insertion_sort(a, reverse):
    n = len(a)
    for i in range(1, n):
        elem_now = a[i]
        j = i
        while j > 0 and ((not reverse and a[j - 1] > elem_now) or (reverse and a[j - 1] < elem_now)):
            a[j] = a[j - 1]
            j -= 1
        a[j] = elem_now
    return a
insertion_sort([1, 6, 3, -5, 9, 11], False)

# 6. быстрая сортирловка (quick sort)
def quick_sort(a, reverse):
    if len(a) <= 1:
        return a
    elem = a[0]
    left = [i for i in a if (not reverse and i < elem) or (reverse and i > elem)]
    center = [i for i in a if i == elem]
    right = [i for i in a if (not reverse and i > elem) or (reverse and i < elem)]

    return quick_sort(left, reverse) + center + quick_sort(right, reverse)
quick_sort([1, 6, 3, -5, 111, 9], False)

# 7. сортировка Шелла (shell sort)
def shell_sort(a, reverse):
    half = len(a) // 2
    while half != 0:
        for i in range(half, len(a)):
            elem_now = a[i]
            j = i
            while j >= half and ((not reverse and a[j - half] > elem_now) or (reverse and a[j - half] < elem_now)):
                a[j] = a[j - half]
                j = j - half
            a[j] = elem_now
        half = half // 2
    return a
shell_sort([1, 6, 3, -5, 111, 9], False)

# 8. сортировка слиянием (merge sort)
def merge_two_list(list_1, list_2, reverse):
    answer = []
    i, j = 0, 0
    while i < len(list_1) and j < len(list_2):
        if (not reverse and list_1[i] < list_2[j]) or (reverse and list_1[i] > list_2[j]):
            answer.append(list_1[i])
            i += 1
        else:
            answer.append(list_2[j])
            j += 1
    if i < len(list_1):
        answer += list_1[i:]
    if j < len(list_2):
        answer += list_2[j:]
    return answer
def merge_sort(list_1, reverse):
    if len(list_1) == 1:
        return list_1
    middle = len(list_1) // 2
    left = merge_sort(list_1[:middle], reverse)
    right = merge_sort(list_1[middle:], reverse)
    return merge_two_list(left, right, reverse)
merge_sort([1, 6, 3, -5, 111, 9], False)

# ПРИМЕР ДЕКОРАТОРА
import time
def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(func.__name__, end_time - start_time)
        return res
    return wrapper

@decorator
def sort_1():
    with open('rrr.txt', 'r') as f:
        s = f.readlines()
    d = {}
    for i in s:
        elem = i.rstrip().split()
        d[int(elem[1])] = elem[0]
    a = list(d.keys())
    n = len(a)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if a[j] < a[min_index]:
                min_index = j
        if i != min_index:
            a[min_index], a[i] = a[i], a[min_index]

    new_d = {i: d[i] for i in a}
    return new_d

@decorator
def sort_2():
    with open('rrr.txt', 'r') as f:
        s = f.readlines()
    d = {}
    for i in s:
        elem = i.rstrip().split()
        d[int(elem[1])] = elem[0]
    a = list(d.keys())
    n = len(a)
    for i in range(1, n):
        elem_now = a[i]
        j = i
        while j > 0 and a[j - 1] > elem_now:
            a[j] = a[j - 1]
            j -= 1
        a[j] = elem_now

    new_d = {i: d[i] for i in a}
    return new_d
sort_1()
sort_2()

# КЛАСС С КНИГОЙ
class Book:
    def __init__(self, author, title, year):
        self.author = author
        self.title = title
        self.year = year
def quick_sort(list_1, key, reverse):
    if len(list_1) <= 1:
        return list_1

    elem = getattr(list_1[0], key)
    left = [i for i in list_1 if (not reverse and getattr(i, key) < elem) or ((reverse and getattr(i, key) > elem))]
    center = [i for i in list_1 if getattr(i, key) == elem]
    right = [i for i in list_1 if (not reverse and getattr(i, key) > elem) or (reverse and getattr(i, key) < elem)]

    return quick_sort(left, key, reverse) + center + quick_sort(right, key, reverse)

books = [("Pushlin", "dw", "1989"), ("Dostoyevsky", "po", "1400"), ("Fet", "fd", "1221"), ("Tutchev", "fs", "1333")]
list_books = []
for i in books:
    author, title, year = i[0], i[1], i[2]
    list_books.append(Book(author, title, year))
[[i.author, i.title, i.year] for i in quick_sort(list_books, 'author', False)]"""


def stack():
    """# СТЭК
class Stack:
    def __init__(self, mx):
        self.__stack = []
        self.mx = mx
    def __len__(self):
        return len(self.__stack)
    def is_empty(self):
        return len(self.__stack) == 0
    def push(self, element):
        if len(self.__stack) < self.mx:
            self.__stack.append(element)
    def pop(self):
        if self.is_empty():
            raise IndexError('Stack is empty')
        return self.__stack.pop()
    def top(self):
        if self.is_empty():
            raise IndexError('Stack is empty')
        return self.__stack[-1]

#ОДНОНАПРАВЛЕНЫЙ СПИСОК
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None
    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

#ДВУНАПРАВЛЕННЫЙ СПИСОК
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
class DoublyLinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
    def append_Node(self, data):
        new_Node = Node(data)
        if not self.head:
            self.head = new_Node
            self.tail = new_Node
        else:
            self.tail.next = new_Node
            new_Node.prev = self.tail
            self.tail = new_Node
    def print_list(self):
        current_Node = self.head
        while current_Node:
            print(current_Node.data, end=' ')
            current_Node = current_Node.next
        print()
    def del_all_values(self, value):
        current_Node = self.head
        while current_Node:
            next_Node = current_Node.next
            if current_Node.data == value:
                if current_Node.prev:
                    current_Node.prev.next = current_Node.next
                else:
                    self.head = current_Node.next

                if current_Node.next:
                    current_Node.next.prev = current_Node.prev
                else:
                    self.tail = current_Node.prev
            current_Node = next_Node
    def del_repeat_values(self):
        datas = set()
        current_Node = self.head
        while current_Node:
            next_Node = current_Node.next
            if current_Node.data in datas:
                if current_Node.prev:
                    current_Node.prev.next = current_Node.next
                if current_Node.next:
                    current_Node.next.prev = current_Node.prev

                if current_Node == self.head:
                    self.head = current_Node.next
                if current_Node == self.tail:
                    self.tail = current_Node.prev
            else:
                datas.add(current_Node.data)
            current_Node = next_Node
    def split_list(self, value):
        first_list = DoublyLinkedList()
        second_list = DoublyLinkedList()
        current_Node = self.head
        while current_Node:
            if current_Node.data >= value:
                first_list.append_Node(current_Node.data)
            else:
                second_list.append_Node(current_Node.data)
            current_Node = current_Node.next
        return first_list, second_list
    def On_sum(self):
        current_Node = self.head
        sum1 = 0
        while current_Node:
            sum1 += current_Node.data
            current_Node = current_Node.next
        return sum1

#ОЧЕРЕДЬ
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
    def dequeue(self):
        if not self.head:
            return None
        else:
            dequeued_item = self.head.data
            self.head = self.head.next
            return dequeued_item
    def is_empty(self):
        return self.head is None
    def print_queue(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" ")
            current_node = current_node.next
        print()"""


def ost():
    '''#РЕКУРСИЯ
y = 0
def printIn(s):
    global y
    print("    " * y + s)
    y += 1
def printOut(s):
    global y
    y = max(0, y - 1)
    print("    " * y + s)
def factorial_inout(n):
    global y
    printIn(f"factorial({n})")
    if n == 0:
        printOut("1")
        return 1
    else:
        result = n * factorial_inout(n - 1)
        printOut(str(result))
        return result
factorial_inout(5)

#ДЕКОРАТОР
def logger(func):
    def wrapper(*args, **kwargs):
        """wrapper """
        print(f"Вызвана функция {func.__name__} с аргументами {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат выполнения функции {func.__name__}: {result}")
        return result
    return wrapper
@logger
def add(a, b):
    """add a+b"""
    return a + b
add(2, 3)
print(add.__name__)
print(add.__doc__)

#ФУНКЦИЯ ВЫСШЕГО ПОРЯДКА
def add(a, b):
    return a + b
def apply_operation(operation, arg1, arg2):
    'operation - callback function; arg1, arg2 - arguments'
    return operation(arg1, arg2)
apply_operation(add, 2, 3)

#ЗАМЫКАНИЕ
def outer_func(n):
    def inner_func(x):
        return x**n
    return inner_func
power_2 = outer_func(3)
print(power_2(2))

#БИНАРНЫЙ ПОИСК
def binary_search(a, x):
    left = 0
    right = len(a) - 1
    while left <= right:
        i = (left + right) // 2
        if a[i] == x:
            return i
        elif a[i] < x:
            left = i + 1
        else:
            right = i - 1
binary_search([1, 2, 4, 10, 18, 30], 30)

#ПРИМЕР  КЛАССА
class Schoolboy:
    def __init__(self, name, age, group, all_marks):
        self.name = name
        self.age = age
        self.group = group
        self.all_marks = all_marks
    def change_mark(self, new_mark):
        subject = new_mark[0]
        mark = new_mark[1]
        if subject in self.all_marks:
            self.all_marks[subject] = mark
        else:
            self.all_marks[subject] = [mark]
    def calculate(self):
        total_marks = 0
        num_subjects = 0
        for subject, marks in self.all_marks.items():
            total_marks += sum(marks)
            num_subjects += len(marks)
        if num_subjects != 0:
            return total_marks / num_subjects
        else:
            return 0
    def add_new(self, subject, mark):
        if subject in self.all_marks:
            self.all_marks[subject].append(mark)
        else:
            self.all_marks[subject] = [mark]
    def display_info(self):
        print(self.name, self.age, self.group, self.all_marks)
    def change_name(self, new_name):
        self.name = new_name
    def change_age(self, new_age):
        self.age = new_age
student = Schoolboy("Илья", 19, "ПМ23-4", {'math': [75]})
student.change_mark(('math', 80))
student.add_new('english', [85, 90])
student.change_name("Иван")
student.change_age(18)
student.display_info()'''


def tickets():
    """#БИЛЕТ 8 И 19

# ДККОРАТОР С ЗАДЕРЖКОЙ
import time
def delay(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator
@delay(1)
def say_hello():
    print("Hello, world!")
say_hello()


#БИЛЕТ 20 И 22

# ДЕКОРАТОР, ВЫЗЫВАЮЩИЙ ИСКЛЮЧЕНИЯ
def handle_exceptions(handler):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as x:
                return handler(x)
        return wrapper
    return decorator
def my_exception_handler(x):
    print(f"An error occurred: {x}")
@handle_exceptions(my_exception_handler)
def may_raise_exception(divide_by):
    return 10 / divide_by
result = may_raise_exception(0)


#БИЛЕТ 21 И 25
#ДЕКАРЫТОР, ОГРАНИЧИВАЮЩИЙ КОЛ-ВО МЕТОДОВ
def limit_calls(max_calls):
    def decorator(func):
        func._call_count = 0
        def wrapper(*args, **kwargs):
            if func._call_count >= max_calls:
                print(f"Function '{func.__name__}' exceeded call limit of {max_calls}")
                return None  # Или любое другое значение, указывающее на превышение лимита
            func._call_count += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator
@limit_calls(3)
def test_function():
    print("123")
test_function()
test_function()
test_function()
result = test_function()
if result is None:
    print("Call limit was exceeded.") Б


#БИЛЕТ 24

#ДЕКОРАТОР В УКАЗАННЫЙ ТИП ДАННЫХ
def convert_return_type(return_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                return return_type(result)
            except (ValueError, TypeError):
                print(f"Cannot convert {result} to {return_type}")
        return wrapper
    return decorator
@convert_return_type(int)
def get_number_as_string():
    return "123"
print(get_number_as_string())


#ББЛЕТ 18

#ДЕКОРАТОР ДЛЯ ПРОВЕРКИ АРГУМЕНТОВ ПОД УСЛОВИЕ
def check_arguments(condition, error_message="Invalid arguments"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not condition(*args, **kwargs):
                raise ValueError(error_message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
@check_arguments(lambda x, y: x > 0 and y > 0, "Both arguments must be greater than zero")
def add_positive_numbers(x, y):
    return x + y
try:
    print(add_positive_numbers(1, 2))
    print(add_positive_numbers(-1, 2))
except ValueError as e:
    print(e)"""