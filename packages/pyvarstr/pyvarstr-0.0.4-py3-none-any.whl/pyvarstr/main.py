def help():
  return "dec exdec exlist exsort exclass sort list"

def dec():
  return """
#1 декоратор, который будет выводить время выполнения функции и сохра-нять его в файл

import time

def measure_running_time(function):
    def wrapper(*args, **kwargs):
      bt = time.time()
      result = function(*args, **kwargs)
      et = time.time()
      f = open("01-log.txt", "a")
      f.write(f'{function.__name__}: Код выполнялся {et-bt} секунд(ы)\n')
      f.close()
      return result
    return wrapper

@measure_running_time
def api_call():
  time.sleep(1)  
  print("API call")

api_call()

#2 декоратор, который будет выводить на экран результат выполненияфункции

def print_result(function):
    def wrapper(*args, **kwargs):
      result = function(*args, **kwargs)
      print(result)
      return result
    return wrapper

@print_result
def api_call():
  return "API called successfully!"

api_call()

#3 декоратор, который будет выводить на экран аргументы функции и ихтипы

def print_args(function):
    def wrapper(*args, **kwargs):
      result = function(*args, **kwargs)
      for a in args:
        print(a, type(a))            
      for k,v in kwargs.items():
        print(v, type(v))
      return result
    return wrapper

@print_args
def api_call(a, b, c, flag):
  return True

api_call(1, "a", 0.1, flag=True)

#4 декоратор, который будет выводить на экран имя функции и модуль, гдеона определена

def print_function_name(function):
    def wrapper(*args, **kwargs):
      result = function(*args, **kwargs)
      print(function.__name__, function.__module__)
      return result
    return wrapper

@print_function_name
def api_call():
  return True

api_call()

#5 декоратор, который будет выводить на экран количество вызовов функ-ции за определенный период времени.

import functools
import time

def num_calls_per_period(period_sec):
  calls = []
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      nonlocal calls
      now = time.time()
      calls.insert(0, now)
      result = function(*args, **kwargs)
      num_calls = 0
      for c in calls:
        if now - c > period_sec:
          break
        num_calls += 1
      print(f"Function called {num_calls} times during last {period_sec} seconds")
      return result
    return wrapper
  return decorator

@num_calls_per_period(period_sec=5)
def api_call():
  time.sleep(1)
  return 1

for i in range(10):
  api_call()

#7 декоратор, который будет кэшировать результаты выполнения функциии очищать кэш при превышении заданного размера

import functools
import math

def use_cache(max_entries):
    cache_dict = {}
    def decorator(function):
      @functools.wraps(function)
      def wrapper(*args, **kwargs):
        nonlocal cache_dict
        if len(args) != 1 or len(kwargs) !=0:
          raise ArgumentError("wrong number of arguments! only functions with 1 argument are supported!")
        arg = args[0]
        if arg in cache_dict:
          print("cache hit!")
          return cache_dict[arg]
        else:
          print("cache miss!")
          result = function(arg)
          if len(cache_dict) > max_entries:
            print("cache emptied!")
            cache_dict = {}
          cache_dict[arg] = result
          return result
      return wrapper
    return decorator

@use_cache(max_entries=5)
def calc_exp(x):
  return math.exp(x)

print(calc_exp(100))
print(calc_exp(100))

print('first run')
for i in range(6):
  calc_exp(i)
print('second run')
for i in range(6):
  calc_exp(i)

#8 декоратор, который будет логировать ошибки, возникающие при выпол-нении функции, и отправлять уведомления об этих ошибках

import functools
import smtplib

def exception_handler(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      try:
        result = function(*args, **kwargs)
        return result
      except Exception as e:
        print("ОШИБКА!", repr(e))
        f = open("08-log.txt", "a")
        f.write(f"ОШИБКА! {repr(e)}\n")
        f.close()
        try:
          # ниже должен быть указан настоящий IP адрес почтового сервера
          # и настоящий e-mail адрес получателя
          s = smtplib.SMTP('localhost')
          s.sendmail('robot@nowhere.nn', ['admin@nowhere.nn'], repr(e))
          s.quit()
        except:
          print("Не удалось отправить уведомление об ошибке на e-mail адрес администратора!")
        return None
    return wrapper

@exception_handler
def div2(a, b):
  return a / b

print(div2(10,2))
print(div2(10,0))

#9 декоратор, который будет проверять аргументы функции на корректностьи выбрасывать исключение при обнаружении некорректных данных

import functools

def validate_arguments(check_function):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      for a in args:
        if not check_function(a):
          raise ValueError('function argument check failed!')
      for k,v in kwargs.items():
        if not check_function(v):
          raise ValueError('function argument check failed!')
      result = function(*args, **kwargs)
      return result
    return wrapper
  return decorator

@validate_arguments(lambda x: x > 0)
def calculate_cube_volume(x):
  return x**3

print(calculate_cube_volume(3))
print(calculate_cube_volume(-3))

#10 декоратор, который будет проверять возвращаемое значение функции накорректность и заменять его на предопределенное значение при обнаружении не-корректных данных

import functools

def validate_return_value(check_function):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      result = function(*args, **kwargs)
      if not check_function(result):
        return 0
      return result
    return wrapper
  return decorator

@validate_return_value(lambda x: x > 0)
def calculate_cube_volume(x):
  return x**3

print(calculate_cube_volume(3))
print(calculate_cube_volume(-3))

#11 декоратор, который будет заменять исключения, возникающие при вы-полнении функции, на заданное значение и логировать эти замены

import functools
import smtplib

def exception_handler(exception_retvalue):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      try:
        result = function(*args, **kwargs)
        return result
      except Exception as e:
        print("ОШИБКА!", repr(e))
        f = open("11-log.txt", "a")
        f.write(f"ОШИБКА! {repr(e)}\n")
        f.close()
        return exception_retvalue
    return wrapper
  return decorator

@exception_handler(exception_retvalue = 0)
def div2(a, b):
  return a / b

print(div2(10,2))
print(div2(10,0))

#13 декоратор, который будет ограничивать количество вызовов функцииза определенный период времени

import functools
import time

def limit_calls_per_period(max_calls, period_sec):
  calls = []
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      nonlocal calls
      now = time.time()
      calls.insert(0, now)
      num_calls = 0
      for c in calls:
        if now - c > period_sec:
          break
        num_calls += 1
      print(f"Function called {num_calls} times during last {period_sec} seconds")
      if (num_calls <= max_calls):
        print("Calling the function...")
        result = function(*args, **kwargs)
        return result
      else:
        print("Function call limit reached!")
        return None
    return wrapper
  return decorator

@limit_calls_per_period(max_calls = 5, period_sec=1)
def api_call():
  return 1

for i in range(10):
  api_call()

#14 декоратор, который будет принимать аргументы и передавать их в функ-цию в ОБРАТНОМ порядке

def reverse_args(function):
    def wrapper(*args):
      aa = []
      for a in args:
        aa.insert(0, a)
      result = function(*aa)
      return result
    return wrapper

@reverse_args
def api_call(a, b, c):
  print(a, b, c)

api_call(1, 2, 3)

#15 декоратор, который будет принимать аргументы и передавать их в функ-цию в качестве ключевых параметров с заданными значениями по умолчанию

def kvargs_default(default_value):
  def decorator(function):
    def wrapper(*args):
      a = default_value
      b = default_value
      c = default_value
      if len(args) > 0:
        a = args[0]
      if len(args) > 1:
        b = args[1]
      if len(args) > 2:
        c = args[2]
      result = function(a=a, b=b, c=c)
      return result
    return wrapper
  return decorator

@kvargs_default(-1)
def api_call(a, b, c):
  print(a, b, c)

api_call(4, 2)

#16 декоратор, который будет принимать аргументы и передавать их в функ-цию в качестве позиционных параметров с заданными значениями по умолчанию

from inspect import signature

def args_default(default_value):
  def decorator(function):
    def wrapper(*args):
      sig = signature(function)
      num_args = len(sig.parameters)
      aa = [default_value]*num_args
      for i in range(num_args):
        if i < len(args):
          aa[i] = args[i]
      result = function(*aa)
      return result
    return wrapper
  return decorator

@args_default(-1)
def api_call(a, b, c):
  print(a, b, c)

api_call(4, 2)

#22 декоратор, который будет принимать список аргументов и передавать егов функцию в ОБРАТНОМ порядке

from inspect import signature

def args_list_reverse(function):
    def wrapper(*args):
      aa = list(args[0])
      aa.reverse()
      result = function(*aa)
      return result
    return wrapper

@args_list_reverse
def api_call(a, b, c):
  print(a, b, c)

api_call([3, 2, 1])

#23 декоратор, который будет принимать словарь аргументов и передаватьего в функцию с заданными значениями по умолчанию.

from inspect import signature

def args_dict(function):
    def wrapper(*args):
      result = function(**args[0])
      return result
    return wrapper

@args_dict
def api_call(a, b, c):
  print(a, b, c)

api_call({'a':3, 'b':2, 'c':1})

#25 декоратор, который будет заменять значение аргумента на заданное зна-чение только если оно удовлетворяет определенному условию

import functools

def fix_arguments(check_function, fix_value):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      aa = []
      for a in args:
        if not check_function(a):
          aa.append(fix_value)
        else:
          aa.append(a)
      kv = {}
      for k, v in kwargs.items():
        if not check_function(v):
          kv[k] = fix_value
        else:
          kv[k] = v
      result = function(*aa, **kv)
      return result
    return wrapper
  return decorator

@fix_arguments(lambda x: x > 0, 1)
def calculate_cube_volume(x):
  return x**3

print(calculate_cube_volume(3))
print(calculate_cube_volume(-3))
"""

def exdec():
  return """

#1-2 перехватывает исключения и выдаёт своё сообщение об ошибке

import functools

def exception_handler(def_response="An error occurred!"):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      try:
        result = function(*args, **kwargs)
        return result
      except:
        print(def_response)
        return None
    return wrapper
  return decorator

@exception_handler(def_response="Division failed!")
def div2(a, b):
  return a / b

@exception_handler()
def sum2(a, b):
  return a + b

print(div2(10,2))
print(div2(10,0))

print(sum2(2, 2))
print(sum2(2, "a"))

#2-2 выдаёт исключение, если возвращаемое значение не проходит проверку

import functools

def validate_arguments(check_function):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      result = function(*args, **kwargs)
      if not check_function(result):
        raise ValueError('function return value check failed!')
      return result
    return wrapper
  return decorator

@validate_arguments(lambda x: x > 0)
def calculate_cube_volume(x):
  return x**3

print(calculate_cube_volume(3))
print(calculate_cube_volume(-3))

#8-2 задерживает выполнение функции на заданное время

import functools
import time

def delay_execution(delay):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      time.sleep(delay)
      result = function(*args, **kwargs)
      return result
    return wrapper
  return decorator

@delay_execution(delay=10)
def api_call():
  print("API call delayed...")

api_call()

#21-2 ограничивает кол-во вызовов функции

import functools

def limit_calls(max_calls):
  calls = 0
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      nonlocal calls
      calls += 1
      if calls <= max_calls:
        result = function(*args, **kwargs)
        return result
      return None
    return wrapper
  return decorator

@limit_calls(max_calls=6)
def api_call():
  print("API call executed succesfully...")

for i in range(10):
  api_call()

#24-2 - преобразует тип возвращаемого значения функции

import functools

def convert_to_data_type(dt_func):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      result = function(*args, **kwargs)
      return dt_func(result)
    return wrapper
  return decorator

@convert_to_data_type(str)
def concatenate_strings(x, y):
  return x + y

@convert_to_data_type(int)
def sum2(x, y):
  return x + y

a = concatenate_strings("1","2")
print(a, type(a))
b = sum2("1","2")
print(b, type(b))

#15-2 - новый - вызывает декорированную функцию несколько раз, пока не получит возвращаемое значение не None

import functools
import random

def retry_on_failure(max_retries=3):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      for i in range(max_retries):
        result = function(*args, **kwargs)
        if result is not None:
          return result
      return None
    return wrapper
  return decorator

@retry_on_failure()
def api_call():
  print("API call")
  return None if random.randint(0, 1)==0 else 1

api_call()
"""

def exlist():
  return """
#1-3 стэк

class Stack():
  def __init__(self):
    self.stack = []

  def print(self):
    print(self.stack)

  def push(self, item):
    self.stack.append(item)

  def pop(self):
    return self.stack.pop()

s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.print()
a = s.pop()
print(a)
s.print()

#2-3 двусвязный список (заказы в инетмагазине)

from datetime import date

class Item:
  def __init__(self, name, quantity, cost):
    self.name = name
    self.quantity = quantity
    self.cost = cost
  def print(self):
    print(self.name, self.quantity, self.cost)

class Order:
  def __init__(self, number, date, items):
    self.number = number
    self.date = date
    self.items = items
    self.next = None
    self.prev = None
  def print(self):
    print(self.number, self.date)
    for item in self.items:
      item.print()
    print()

class Orders:
  def __init__(self):
    self.head = None
    self.tail = None

  def append(self, order):
    if self.head is None:
      self.head = order
    order.prev = self.tail
    if self.tail is not None:
      self.tail.next = order
    self.tail = order

orders = Orders()
orders.append(Order(1, date.today(), [Item("Болты", 10, 20), Item("Гайки", 10, 30)]))
orders.append(Order(2, date.today(), [Item("Саморезы", 20, 40)]))
orders.append(Order(3, date.today(), [Item("Шайбы", 20, 30), Item("Втулки", 10, 50), Item("Скобы", 15, 35)]))

order = orders.head
while order is not None:
  order.print()
  order = order.next

#25-3 односвязный список
class Item:
  def __init__(self, value):
    self.value = value
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = None

  def append(self, value):
    if self.head is None:
      self.head = Item(value)
    else:
      item = self.head
      while item.next is not None:
        item = item.next
      item.next = Item(value)

  def delete_last(self):
    if self.head is None:
      return
    elif self.head.next is None:
      self.head = None
    else:
      prev = None
      item = self.head
      while item.next is not None:
        prev = item
        item = item.next
      prev.next = None

  def print(self):
    item = self.head
    while item is not None:
      print(item.value)
      item = item.next

l = LinkedList()
l.append(1)
l.append(2)
l.append(3)
l.append(4)
l.print()
print("\n")
l.delete_last()
l.delete_last()
l.print()
"""

def exsort():
  return """
#8-3 сортировка фильмов по годам по возрастанию и по убыванию быстрой сортировкой

def quick_sort(arr, compare_function):
  quick_sort_helper(arr, 0, len(arr) - 1, compare_function)
  return arr

def quick_sort_helper(arr, first, last, compare_function):
  if first < last:
    split_point = partition(arr, first, last, compare_function)
    quick_sort_helper(arr, first, split_point - 1, compare_function)
    quick_sort_helper(arr, split_point + 1, last, compare_function)

def partition(arr, first, last, compare_function):
  pivot_value = arr[first]
  left_mark = first + 1
  right_mark = last
  done = False
  
  while not done:
    while left_mark <= right_mark and compare_function(arr[left_mark], pivot_value) <= 0:
      left_mark += 1
    while compare_function(arr[right_mark], pivot_value) >= 0 and right_mark >= left_mark:
      right_mark -= 1

    if right_mark < left_mark:
      done = True
    else:
      arr[left_mark], arr[right_mark] = arr[right_mark], arr[left_mark]

  arr[first], arr[right_mark] = arr[right_mark], arr[first]

  return right_mark

def compare_movies_by_year(a, b):
  an, ay = a
  bn, by = b
  return ay - by

def compare_movies_by_year_descending(a, b):
  an, ay = a
  bn, by = b
  return by - ay

List = [("Inception", 2010), ("The Matrix", 1999), ('Pulp Fiction', 1994),
("The Godfather", 1972), ("The Dark Knight", 2008),("Forrest Gump", 1994), 
("Fight Club", 1999), ('Interstellar', 2014), ('The Shawshank Redemption', 1994),
('Gladiator', 2000), ('Avatar', 2009), ('Titanic', 1997), 
('The Lord of the Rings', 2001), ('Star Wars', 1977), ('Jurassic Park', 1993)]

print(f'Sorted list ascending: {quick_sort(List, compare_movies_by_year)}\n')
print(f'Sorted list descending: {quick_sort(List, compare_movies_by_year_descending)}\n')

#23-3 сортировка строк по возрастанию и убыванию длины быстрой сортировкой с измерением времени выполнения

import time

def measure_running_time(function):
    def wrapper(*args, **kwargs):
      bt = time.time()
      result = function(*args, **kwargs)
      et = time.time()
      print(f'Код выполнялся {et-bt} секунд(ы)')
      return result
    return wrapper

@measure_running_time
def selection_sort(arr, compare_function):
  n = len(arr)
  for i in range(n):
    min_idx = i
    for j in range(i + 1, n):
      if compare_function(arr[j], arr[min_idx]) < 0:
        min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
  return arr

@measure_running_time
def quick_sort(arr, compare_function):
  quick_sort_helper(arr, 0, len(arr) - 1, compare_function)
  return arr

def quick_sort_helper(arr, first, last, compare_function):
  if first < last:
    split_point = partition(arr, first, last, compare_function)
    quick_sort_helper(arr, first, split_point - 1, compare_function)
    quick_sort_helper(arr, split_point + 1, last, compare_function)

def partition(arr, first, last, compare_function):
  pivot_value = arr[first]
  left_mark = first + 1
  right_mark = last
  done = False
  
  while not done:
    while left_mark <= right_mark and compare_function(arr[left_mark], pivot_value) <= 0:
      left_mark += 1
    while compare_function(arr[right_mark], pivot_value) >= 0 and right_mark >= left_mark:
      right_mark -= 1

    if right_mark < left_mark:
      done = True
    else:
      arr[left_mark], arr[right_mark] = arr[right_mark], arr[left_mark]

  arr[first], arr[right_mark] = arr[right_mark], arr[first]

  return right_mark

def compare_strings_by_len(a, b):
  return len(a) - len(b)

def compare_strings_by_len_descending(a, b):
  return len(b) - len(a)

List = ["Inception", "The Matrix", 'Pulp Fiction', "The Godfather", "The Dark Knight", 
"Forrest Gump", "Fight Club", 'Interstellar', 'The Shawshank Redemption',
'Gladiator', 'Avatar', 'Titanic', 'The Lord of the Rings', 'Star Wars', 'Jurassic Park']

print(f'Quicksorted list ascending: {quick_sort(List, compare_strings_by_len)}\n')
print(f'Quicksorted list descending: {quick_sort(List, compare_strings_by_len_descending)}\n')

print(f'Selectionsorted list ascending: {selection_sort(List, compare_strings_by_len)}\n')
print(f'Selectionsorted list descending: {selection_sort(List, compare_strings_by_len_descending)}\n')

List *= 100
print("Quick sort")
quick_sort(List, compare_strings_by_len)
print("Selection sort")
selection_sort(List, compare_strings_by_len)

#24-3 бинарный поиск

import random

def binary_search(arr, x):
  low = 0
  high = len(a) - 1
  while low <= high:
    mid = (low + high) // 2
    if arr[mid] == x:
      return mid
    elif arr[mid] < x:
      low = mid + 1
    else:
      high = mid - 1
  return -1

a = []
for i in range(10):
    a.append(random.randint(1, 50))
a.sort()
print(a)

v = random.choice(a)
print(v)

print(binary_search(a, v))

#1-3 - новый - сортировка вставками товаров по продажам

import time

def measure_running_time(function):
    def wrapper(*args, **kwargs):
      bt = time.time()
      result = function(*args, **kwargs)
      et = time.time()
      print(f'Код выполнялся {et-bt} секунд(ы)')
      return result
    return wrapper

@measure_running_time
def insertion_sort(arr, compare_function):
    for i in range(1, len(arr)):
        val = arr[i]
        j = i - 1
        while j >= 0 and compare_function(arr[j], val) > 0:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = val
    return arr

def compare_goods_by_sales(a, b):
  a1, a2 = a
  b1, b2 = b
  return a2 - b2

def compare_goods_by_sales_descending(a, b):
  a1, a2 = a
  b1, b2 = b
  return b2 - a2

List = [('Товар1', 53), ('Товар2', 72), ('Товар3', 30), ('Товар4', 85), ('Товар5', 47)]

print(f'Insertion sorted list ascending: {insertion_sort(List, compare_goods_by_sales)}\n')
print(f'Insertion sorted list descending: {insertion_sort(List, compare_goods_by_sales_descending)}\n')

#13-3 - новый - сортировка пузырьком и шейкерная чисел по сумме цифр

import time
import random

def measure_running_time(function):
    def wrapper(*args, **kwargs):
      bt = time.time()
      result = function(*args, **kwargs)
      et = time.time()
      print(f'Код выполнялся {et-bt} секунд(ы)')
      return result
    return wrapper

@measure_running_time
def bubble_sort(arr, compare_function):
  n = len(arr)
  for i in range(n):
    for j in range(0, n-i-1):
      if compare_function(arr[j], arr[j+1]) > 0:
        arr[j], arr[j+1] = arr[j+1], arr[j]
  return arr

@measure_running_time
def cocktail_sort(arr, compare_function):
  n = len(arr)
  start = 0
  end = n - 1
  swapped = True
  while swapped:
    swapped = False
    for i in range(start, end):
      if (compare_function(arr[i], arr[i + 1]) > 0):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
        swapped = True
    if not swapped:
      break
    swapped = False
    end = end - 1
    for i in range(end - 1, start - 1, -1):
      if (compare_function(arr[i], arr[i + 1]) > 0):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
        swapped = True
    start = start + 1
  return arr

def sum_digits(number):
  return sum(int(digit) for digit in str(number))

def compare_numbers_by_sum_of_digits(a, b):
  return sum_digits(a) - sum_digits(b)

def compare_numbers_by_sum_of_digits_descending(a, b):
  return sum_digits(b) - sum_digits(a)

List = []
for i in range(100):
    List.append(random.randint(1, 12))


print(f'Bubble sorted list ascending: {bubble_sort(List, compare_numbers_by_sum_of_digits)}\n')
print(f'Bubble sorted list descending: {bubble_sort(List, compare_numbers_by_sum_of_digits_descending)}\n')

print(f'Cocktail sorted list ascending: {cocktail_sort(List, compare_numbers_by_sum_of_digits)}\n')
print(f'Cocktail sorted list descending: {cocktail_sort(List, compare_numbers_by_sum_of_digits_descending)}\n')

#5-3 - новый - сортировка чисел выбором по сумме цифр

import time

def selection_sort(arr, compare_function):
  n = len(arr)
  for i in range(n):
    min_idx = i
    for j in range(i + 1, n):
      if compare_function(arr[j], arr[min_idx]) < 0:
        min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
  return arr

def sum_digits(number):
  return sum(int(digit) for digit in str(number))

def compare_numbers_by_sum_of_digits(a, b):
  return sum_digits(a) - sum_digits(b)

List = [12,45,67,23,89,12,77,54,31,90,68,35,101,211,13,17]

print(f'Selection sorted list: {selection_sort(List, compare_numbers_by_sum_of_digits)}\n')

#15-3 - новый - сортировка чисел выбором по сумме цифр. СПИСОК НЕ ДАН!!!

import random

def selection_sort(arr, compare_function):
  n = len(arr)
  for i in range(n):
    min_idx = i
    for j in range(i + 1, n):
      if compare_function(arr[j], arr[min_idx]) < 0:
        min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
  return arr

def sum_digits(number):
  return sum(int(digit) for digit in str(number))

def compare_numbers_by_sum_of_digits(a, b):
  return sum_digits(a) - sum_digits(b)

List = []
for i in range(100):
    List.append(random.randint(1, 12))

print(f'Selection sorted list: {selection_sort(List, compare_numbers_by_sum_of_digits)}\n')
"""

def exclass():
  return """

#19-3 студенты с оценками

class Student:
  def __init__(self, firstname, lastname, age, marks):
    self.firstname = firstname
    self.lastname = lastname
    self.age = age
    self.marks = marks
  def __len__(self):
    return len(self.marks)
  def add_mark(self, mark):
    self.marks.append(mark)
  def mean_mark(self):
    if len(self):
      return sum(self.marks) / len(self)
    else:
      return 0
  def print(self):
    print(f'Студент {self.firstname} {self.lastname}, возраст - {self.age}, cр.балл - {self.mean_mark()}')

a = Student('Ivan', 'Ivanov', 18, [5,4,4,4])
a.print()
a.add_mark(5)
a.print()

#21-3 автомобили со скоростью

class Car:
  def __init__(self, brand, model, year, speed):
    self.brand = brand
    self.model = model
    self.year = year
    self.speed = speed
  def speed_up(self, speed_increment):
    self.speed += speed_increment
  def speed_down(self, speed_decrement):
    self.speed -= speed_decrement
  def __eq__(self, other):
    return self.speed == other.speed
  def print(self):
    print(f'Автомобиль {self.brand} {self.model}, год выпуска - {self.year}, скорость - {self.speed}')

a = Car('Ford', 'Focus', 2008, 90)
a.print()
a.speed_up(10)
a.print()
a.speed_down(10)
a.print()
b = Car('Lada', 'Vesta', 2022, 90)
b.print()
if a == b:
  print('У двух автомобилей скорость одинакова')
else:
  print('У двух автомобилей скорость разная')

#23-2 геометрические фигуры с вычислением площади

import math

class Shape:
  def area(self):
    raise NotImplementedError("Method not implemented")

class Rectangle(Shape):
  def __init__(self, a, b):
    self.a = a
    self.b = b
  def area(self):
    return self.a*self.b

class Circle(Shape):
  def __init__(self, r):
    self.r = r
  def area(self):
    return math.pi*self.r**2

objects = [Rectangle(2,2), Circle(1)]
for o in objects:
  print(o.area())

#12-3 - новый - персоны с определением возраста

from datetime import datetime
from dateutil.relativedelta import relativedelta

class Person:
  def __init__(self, name, country, birthdate):
    self.name = name
    self.country = country
    self.birthdate = birthdate
  def get_age(self):
    delta = relativedelta(datetime.utcnow(), self.birthdate)
    return delta.years
  def print(self):
    print(f'Имя - {self.name}; страна - {self.country}, дата рождения - {self.birthdate}, возраст - {self.get_age()}')

a = Person('Иван Иванов', 'Russia', datetime(1981, 12, 2))
b = Person('Jean Dubois', 'France', datetime(1958, 6, 15))
a.print()
b.print()
"""

def sort():
  return """
import time

def measure_time(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(f"Время выполнения функции {func.__name__}: {end - start:.6f} ceк.\n")
    return result
  return wrapper

#сортировка выбором

students = {3.25 : 'Ivanov', 4.2 : 'Petrov', 2.1 : 'Sidorov', 5.0 : 'Losev'}

@measure_time
def selection_sort(a_dict):
  lst = list(a_dict.keys())
  for i in range(len(lst) - 1):
    pos_of_min = i
    for j in range(i + 1, len(lst)):
      if lst[j] < lst[pos_of_min]:
        pos_of_min = j
    lst[pos_of_min], lst[i] = lst[i], lst[pos_of_min]

  new_dict = dict()
  for i in range(len(lst)):
    new_dict[lst[i]] = a_dict[lst[i]]
  return new_dict

print(selection_sort(students))

#быстрая сортировка

students = {3.25 : 'Ivanov', 4.2 : 'Petrov', 2.1 : 'Sidorov', 5.0 : 'Losev'}

@measure_time
def sort_quick(ss):
  arr = list(ss.keys())
  l = quick_sort(arr)
  d = dict()
  for i in range(len(l)):
    d[l[i]] = ss[l[i]]
  return d

def quick_sort(arr):
  quick_sort_helper(arr, 0, len(arr) - 1)
  return arr

def quick_sort_helper(arr, first, last):
  if first < last:
    split_point = partition(arr, first, last)
    quick_sort_helper(arr, first, split_point - 1)
    quick_sort_helper(arr, split_point + 1, last)

def partition(arr, first, last):
  pivot_value = arr[first]
  left_mark = first + 1
  right_mark = last
  done = False

  while not done:
    while left_mark <= right_mark and arr[left_mark] <= pivot_value:
      left_mark += 1
    while arr[right_mark] >= pivot_value and right_mark >= left_mark:
      right_mark -= 1
    if right_mark < left_mark:
      done = True
    else:
      arr[left_mark], arr[right_mark] = arr[right_mark], arr[left_mark]

  arr[first], arr[right_mark] = arr[right_mark], arr[first]

  return right_mark

sort_quick(students)

#сортировка Шелла

students = {3.25 : 'Ivanov', 4.2 : 'Petrov', 2.1 : 'Sidorov', 5.0 : 'Losev'}

@measure_time
def sort_shell(ss):
   arr = list(ss.keys())
   l = shell_sort(arr)
   d = dict()
   for i in range(len(l)):
       d[l[i]] = ss[l[i]]
   return d

def shell_sort(arr):
  gap = len(arr) // 2
  while gap > 0:
    for i in range(gap, len(arr)):
      temp = arr[i]
      j = i
      while j >= gap and arr[j - gap] > temp:
        arr[j] = arr[j - gap]
        j -= gap
      arr[j] = temp
    gap //= 2
  return arr

arr = [64, 34, 25, 12, 22, 11, 90]
print(sort_shell(students))

#сортировка слиянием

students = {3.25 : 'Ivanov', 4.2 : 'Petrov', 2.1 : 'Sidorov', 5.0 : 'Losev'}

@measure_time
def sort_sliyanie(ss):
  arr = list(ss.keys())
  l = merge_sort(arr)
  d = dict()
  for i in range(len(l)):
    d[l[i]] = ss[l[i]]
  return d

def merge_sort(arr):
  if len(arr) <= 1:
    return arr
  mid = len(arr) // 2
  left_half = arr[:mid]
  right_half = arr[mid:]
  left_half = merge_sort(left_half)
  right_half = merge_sort(right_half)
  return merge(left_half, right_half)

def merge(left_half, right_half):
  result = []
  i = 0
  j = 0
  while i < len(left_half) and j < len(right_half):
    if left_half[i] <= right_half[j]:
      result.append(left_half[i])
      i += 1
    else:
      result.append(right_half[j])
      j += 1
  result += left_half[i:]
  result += right_half[j:]
  return result

print(sort_sliyanie(students))

#2

class Book():
  def __init__(self, author, name, year):
    self.author = author
    self.name = name
    self.year = year

  def __info__(self):
        return f"Book(author='{self.author}', title='{self.name}', year={self.year})"

books = [
    Book("George Orwell", "1984", 1949),
    Book("Fyodor Dostoevsky", "Crime and Punishment", 1866),
    Book("Leo Tolstoy", "War and Peace", 1869),
    Book("Mark Twain", "Adventures of Huckleberry Finn", 1885),
    Book("Gabriel Garcia Marquez", "One Hundred Years of Solitude", 1967),
    Book('Steven King', 'It', 1986),
    Book('Alexander Pushkin', 'Evgeniy Onegin', 1830),
    Book('Fyodor Dostoevski', 'The Brothers Karamazov', 1880),
    Book('Natalia Makuni', 'Ikarus', 2013)
]

#пузырьковая сортировка

@measure_time
def bubble_sort(arr, key):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if key(arr[j]) > key(arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# реализация алгоритма шейкерной сортировки
def cocktail_sort(arr):
  n = len(arr)
  start = 0
  end = n - 1
  swapped = True
  while swapped:
    swapped = False
    for i in range(start, end):
      if (arr[i] > arr[i + 1]):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
        swapped = True
    if not swapped:
      break
    swapped = False
    end = end - 1
    for i in range(end - 1, start - 1, -1):
      if (arr[i] > arr[i + 1]):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
        swapped = True
    start = start + 1
  return arr

# реализация алгоритма сортировки расчёской
def comb_sort(arr):
  n = len(arr)
  gap = n
  shrink = 1.3
  swapped = True
  while swapped:
    gap = int(gap/shrink)
    if gap < 1:
      gap = 1
    i = 6
    swapped = False
    while i + gap < n:
      if arr[i] > arr[i + gap]:
        arr[i], arr[i + gap] = arr[i + gap], arr[i]
        swapped = True
      l += 1
  return arr

#сортировка вставками

@measure_time
def insertion_sort(arr, key):
    for i in range(1, len(arr)):
        current_book = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key(current_book):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current_book
    return arr

#быстрая сортировка

@measure_time
def quick_sort(arr, key):
  quick_sort_helper(arr, 0, len(arr) - 1, key)
  return arr

def quick_sort_helper(arr, first, last, key):
  if first < last:
    split_point = partition(arr, first, last, key)
    quick_sort_helper(arr, first, split_point - 1, key)
    quick_sort_helper(arr, split_point + 1, last, key)

def partition(arr, first, last, key):
  pivot_value = key(arr[first])
  left_mark = first + 1
  right_mark = last
  done = False

  while not done:
    while left_mark <= right_mark and key(arr[left_mark]) <= pivot_value:
      left_mark += 1
    while key(arr[right_mark]) >= pivot_value and right_mark >= left_mark:
      right_mark -= 1
    if right_mark < left_mark:
      done = True
    else:
      arr[left_mark], arr[right_mark] = arr[right_mark], arr[left_mark]

  arr[first], arr[right_mark] = arr[right_mark], arr[first]

  return right_mark

#сортировка Шелла

@measure_time
def shell_sort(arr, key):
  gap = len(arr) // 2
  while gap > 0:
    for i in range(gap, len(arr)):
      temp = arr[i]
      j = i
      while j >= gap and key(arr[j - gap]) > key(temp):
        arr[j] = arr[j - gap]
        j -= gap
      arr[j] = temp
    gap //= 2
  return arr

#сортировка слиянием

@measure_time
def sort_merge(arr, key):
  return merge_sort(arr, key)

def merge_sort(arr, key):
  if len(arr) <= 1:
    return arr
  mid = len(arr) // 2
  left_half = arr[:mid]
  right_half = arr[mid:]
  left_half = merge_sort(left_half, key)
  right_half = merge_sort(right_half, key)
  return merge(left_half, right_half, key)

def merge(left_half, right_half, key):
  result = []
  i = 0
  j = 0
  while i < len(left_half) and j < len(right_half):
    if key(left_half[i]) <= key(right_half[j]):
      result.append(left_half[i])
      i += 1
    else:
      result.append(right_half[j])
      j += 1
  result += left_half[i:]
  result += right_half[j:]
  return result

sort_criteria = input("Введите критерий сортировки (author, name, year): ")

if sort_criteria == "author":
    sorted_books_bubble = bubble_sort(books.copy(), key=lambda x: x.author)
    print(sorted_books_bubble)
    sorted_books_insertion = insertion_sort(books.copy(), key=lambda x: x.author)
    print(sorted_books_insertion)
    sorted_books_quick = quick_sort(books.copy(), key=lambda x: x.author)
    print(sorted_books_quick)
    sorted_books_shell = shell_sort(books.copy(), key=lambda x: x.author)
    print(sorted_books_shell)
    sorted_books_merge = sort_merge(books.copy(), key=lambda x: x.author)
    print(sorted_books_merge)
elif sort_criteria == "name":
    sorted_books_bubble = bubble_sort(books.copy(), key=lambda x: x.name)
    print(sorted_books_bubble)
    sorted_books_insertion = insertion_sort(books.copy(), key=lambda x: x.name)
    print(sorted_books_insertion)
    sorted_books_quick = quick_sort(books.copy(), key=lambda x: x.name)
    print(sorted_books_quick)
    sorted_books_shell = shell_sort(books.copy(), key=lambda x: x.name)
    print(sorted_books_shell)
    sorted_books_merge = sort_merge(books.copy(), key=lambda x: x.name)
    print(sorted_books_merge)
elif sort_criteria == "year":
    sorted_books_bubble = bubble_sort(books.copy(), key=lambda x: x.year)
    print(sorted_books_bubble)
    sorted_books_insertion = insertion_sort(books.copy(), key=lambda x: x.year)
    print(sorted_books_insertion)
    sorted_books_quick = quick_sort(books.copy(), key=lambda x: x.year)
    print(sorted_books_quick)
    sorted_books_shell = shell_sort(books.copy(), key=lambda x: x.year)
    print(sorted_books_shell)
    sorted_books_merge = sort_merge(books.copy(), key=lambda x: x.year)
    print(sorted_books_merge)
else:
    print("Некорректный критерий сортировки. Пожалуйста, выберите из 'author', 'name', 'year'.")

#3

#сортировка пузырьком

strings = ['banana', 'apple', 'kiwi', 'orange', 'grape', 'pear', 'plum', 'cherry', 'apricot', 'lemon']

@measure_time
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

bubble_sort(strings)

#сортировка слиянием

strings = ['banana', 'apple', 'kiwi', 'orange', 'grape', 'pear', 'plum', 'cherry', 'apricot', 'lemon']

@measure_time
def sort_merge(arr):
  return merge_sort(arr)

def merge_sort(arr):
  if len(arr) <= 1:
    return arr
  mid = len(arr) // 2
  left_half = arr[:mid]
  right_half = arr[mid:]
  left_half = merge_sort(left_half)
  right_half = merge_sort(right_half)
  return merge(left_half, right_half)

def merge(left_half, right_half):
  result = []
  i = 0
  j = 0
  while i < len(left_half) and j < len(right_half):
    if left_half[i] <= right_half[j]:
      result.append(left_half[i])
      i += 1
    else:
      result.append(right_half[j])
      j += 1
  result += left_half[i:]
  result += right_half[j:]
  return result

print(sort_merge(strings))

#быстрая сортировка

strings = ['banana', 'apple', 'kiwi', 'orange', 'grape', 'pear', 'plum', 'cherry', 'apricot', 'lemon']

@measure_time
def quick_sort(arr):
  quick_sort_helper(arr, 0, len(arr) - 1)
  return arr

def quick_sort_helper(arr, first, last):
  if first < last:
    split_point = partition(arr, first, last)
    quick_sort_helper(arr, first, split_point - 1)
    quick_sort_helper(arr, split_point + 1, last)

def partition(arr, first, last):
  pivot_value = arr[first]
  left_mark = first + 1
  right_mark = last
  done = False

  while not done:
    while left_mark <= right_mark and arr[left_mark] <= pivot_value:
      left_mark += 1
    while arr[right_mark] >= pivot_value and right_mark >= left_mark:
      right_mark -= 1
    if right_mark < left_mark:
      done = True
    else:
      arr[left_mark], arr[right_mark] = arr[right_mark], arr[left_mark]

  arr[first], arr[right_mark] = arr[right_mark], arr[first]

  return right_mark

quick_sort(strings)

#сортировка Шелла

@measure_time
def shell_sort(arr):
  gap = len(arr) // 2
  while gap > 0:
    for i in range(gap, len(arr)):
      temp = arr[i]
      j = i
      while j >= gap and arr[j - gap] > temp:
        arr[j] = arr[j - gap]
        j -= gap
      arr[j] = temp
    gap //= 2
  return arr

strings = ['banana', 'apple', 'kiwi', 'orange', 'grape', 'pear', 'plum', 'cherry', 'apricot', 'lemon']
shell_sort(strings)

#сортировка слиянием

@measure_time
def sort_merge(arr):
  return merge_sort(arr)

def merge_sort(arr):
  if len(arr) <= 1:
    return arr
  mid = len(arr) // 2
  left_half = arr[:mid]
  right_half = arr[mid:]
  left_half = merge_sort(left_half)
  right_half = merge_sort(right_half)
  return merge(left_half, right_half)

def merge(left_half, right_half):
  result = []
  i = 0
  j = 0
  while i < len(left_half) and j < len(right_half):
    if left_half[i] <= right_half[j]:
      result.append(left_half[i])
      i += 1
    else:
      result.append(right_half[j])
      j += 1
  result += left_half[i:]
  result += right_half[j:]
  return result

strings = ['banana', 'apple', 'kiwi', 'orange', 'grape', 'pear', 'plum', 'cherry', 'apricot', 'lemon']
sort_merge(strings)
"""

def list():
  return """

#1.1 сбалансированные скобки deque

from collections import deque

class Stack(deque):
  def push(self, a):
    self.append(a)

def is_balanced(expression):
  stack = Stack()
  opening_brackets = ['(', '{', '[']
  closing_brackets = [')', '}', ']']
  for char in expression:
    if char in opening_brackets:
      stack.push(char)
    elif char in closing_brackets:
      if len(stack)==0:
        return False
      top = stack.pop()
      if opening_brackets.index(top) != closing_brackets.index(char):
        return False
  return len(stack) == 0

def check_balance(expression):
  print('Скобки сбалансированы' if is_balanced(expression) else 'Скобки не сбалансированы')

expression1 = input('Введите математическое выражение: ')
check_balance(expression1)

expression2 = input('Введите математическое выражение: ')
check_balance(expression2)

#1.2 сбалансированные скобки без deque

class Stack():
  def __init__(self, l):
    self.__stack = []
    self.__maxlen = l
  def push(self, e):
    if len(self.__stack)<self.__maxlen:
      self.__stack.append(e)
    else:
      raise ValueError("Stack is full")
  def pop(self):
    return self.__stack.pop()
  def top(self):
    return self.__stack[-1]
  def is_empty(self):
    if len(self.__stack)==0:
      return True
    return False
  def __len__(self):
    return len(self.__stack)
  def __str__(self):
    return str(self.__stack)
    
def is_balanced(expression):
  stack = Stack(100)
  opening_brackets = ['(', '{', '[']
  closing_brackets = [')', '}', ']']
  for char in expression:
    if char in opening_brackets:
      stack.push(char)
    elif char in closing_brackets:
      if len(stack)==0:
        return False
      top = stack.pop()
      if opening_brackets.index(top) != closing_brackets.index(char):
        return False
  return len(stack) == 0

def check_balance(expression):
  print('Скобки сбалансированы' if is_balanced(expression) else 'Скобки не сбалансированы')

expression1 = input('Введите математическое выражение: ')
check_balance(expression1)

expression2 = input('Введите математическое выражение: ')
check_balance(expression2)

#2.1 стэк

class Stack():
  def __init__(self, l):
    self.__stack = []
    self.__maxlen = l
  def push(self, e):
    if len(self.__stack)<self.__maxlen:
      self.__stack.append(e)
    else:
      raise ValueError("Stack is full")
  def pop(self):
    return self.__stack.pop()
  def top(self):
    return self.__stack[-1]
  def is_empty(self):
    if len(self.__stack)==0:
      return True
    return False
  def __len__(self):
    return len(self.__stack)
  def __str__(self):
    return str(self.__stack)
    
s=Stack(2)
s.push(5)
s.push(5)
print(s)

s.push(5)

s.pop()
s.pop()
print(str(s))
print(len(s))
s.is_empty()

s.top()

#2.2 стэк на array

import array

class Stack:
    def __init__(self, l):
        self.__stack = array.array('i')
        self.__maxlen = l
    def push(self, e):
        if len(self.__stack) < self.__maxlen:
            self.__stack.append(e)
        else:
            raise ValueError("Stack is full")
    def pop(self):
        return self.__stack.pop()
    def top(self):
        return self.__stack[-1]
    def is_empty(self):
        return len(self.__stack) == 0
    def length(self):
        return len(self.__stack)
    def __str__(self):
        return str(list(self.__stack))

stack = Stack(5)
stack.push(1)
stack.push(2)
stack.push(3)

print(stack.length())
print(stack.top())
print(stack)
stack.push(4)
stack.push(5)
print(stack)
stack.pop()
print(stack)

#3) Реализовать класс однонаправленного связанного списка.

class ListItem:
  def __init__ (self,elem):
    self.elem = elem
    self.nextitem = None

class LinkedList:
  def __init__(self):
    self.head = None

class ListItem:
  def __init__ (self,elem):
    self.elem = elem
    self.nextitem = None

class LinkedList:
  def __init__(self):
    self.head = None
  def AddToBegin(self, newelem):
    newitem = ListItem(newelem)
    newitem.nextitem = self.head
    self.head = newitem
  def __str__(self):
    l = []
    item = self.head
    if item is None:
      return ''
    l.append(item.elem)
    while (item.nextitem):
      item = item.nextitem
      l.append(item.elem)
    return str(l)

l = LinkedList()
l.AddToBegin(1)
l.AddToBegin(2)
l.AddToBegin(3)
print(l)

#4) На базе класса однонаправленного связанного списка реализовать двунаправленный связанный список.

class ListItem:
  def __init__ (self,elem):
    self.elem = elem
    self.nextitem = None
    self.previtem = None

class LinkedList:
  def __init__(self):
    self.head = None
    
#4.1) Реализовать метод добавления элемента в начало списка.

class ListItem:
  def __init__ (self,elem):
    self.elem = elem
    self.nextitem = None
    self.previtem = None

class LinkedList:
  def __init__(self):
    self.head = None
  def AddToBegin(self, newelem):
    newitem = ListItem(newelem)
    newitem.nextitem = self.head
    if self.head is not None:
      self.head.previtem = newitem
    self.head = newitem
  def __str__(self):
    l = []
    item = self.head
    if item is None:
      return ''
    l.append(item.elem)
    while (item.nextitem):
      item = item.nextitem
      l.append(item.elem)
    return str(l)
  def PrintReversed(self):
    i = self.head
    if i is None:
      return
    while (i.nextitem):
      i = i.nextitem
    while (i.previtem):
      print(i.elem)
      i = i.previtem
    print(i.elem)

l = LinkedList()
l.AddToBegin(1)
l.AddToBegin(2)
l.AddToBegin(3)
l.PrintReversed()

#5) При помощи класса связанного списка реализовать очередь.

class ListItem:
  def __init__ (self,elem):
    self.elem = elem
    self.nextitem = None
    self.previtem = None

class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None
  def AddToBegin(self, newelem):
    newitem = ListItem(newelem)
    newitem.nextitem = self.head
    if self.head is not None:
      self.head.previtem = newitem
    else:
      self.tail = newitem
    self.head = newitem
  def GetFromEnd(self):
    i = self.tail
    if i is None:
      return None
    if i.previtem:
      i.previtem.nextitem = None
      self.tail = i.previtem
    return i.elem
  def __str__(self):
    l = []
    item = self.head
    if item is None:
      return ''
    l.append(item.elem)
    while (item.nextitem):
      item = item.nextitem
      l.append(item.elem)
    return str(l)

l = LinkedList()
l.AddToBegin(1)
l.AddToBegin(2)
l.AddToBegin(3)
print(l)
a = l.GetFromEnd()
print(a)
print(l)

#5.2

class ListItem:
  def __init__ (self,elem):
    self.elem = elem
    self.nextitem = None
    self.previtem = None

class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None
  def AddToEnd(self, newelem):
    newitem = ListItem(newelem)
    if self.head == None:
      self.head = newitem
      self.tail = newitem
    else:
      self.tail.nextitem = newitem
      self.tail=newitem
  def GetFromBegin(self):
    i = self.head
    if i is None:
      return None
    if i.nextitem:
      i.nextitem.previtem = None
      self.head = i.nextitem
    return i.elem
  def __str__(self):
    l = []
    item = self.head
    if item is None:
      return ''
    l.append(item.elem)
    while (item.nextitem):
      item = item.nextitem
      l.append(item.elem)
    return str(l)

l = LinkedList()
l.AddToEnd(1)
l.AddToEnd(2)
l.AddToEnd(3)
print(l)
a = l.GetFromBegin()
print(a)
print(l)

#6) Реализовать генератор, который возвращает значение поочередно извлекаемое из конца двух очередей (в качестве очереди используется deque из collections). Если очередь из которой извлекается элемент пуста - генератор заканчивает работу.

from collections import deque

def alternatequeuevalue(queue1, queue2):
    while queue1 and queue2:
        if queue1:
            yield queue1.pop()
        if queue2:
            yield queue2.pop()

queue1 = deque([1, 2, 3, 4, 5, 0])
queue2 = deque([6, 7, 8, 9, 10])

gen = alternatequeuevalue(queue1, queue2)

for value in gen:
    print(value)

#1- Реализовать функцию, которая находит сумму всех элементов двусвязного списка, надо решать задачу двумя способами 1) сложность метода О(1), 2) сложность О(n).

class node:
    def __init__(self, data=None, linkn=None, linkp = None):
        self.data = data
        self.linkn = linkn
        self.linkp = linkp

class linklist2:
    def __init__(self):
        self.head = None
        self.tail = None
        self.__summ=0

    def addnode(self, data):
        newnode = node(data)
        if not self.head:
          self.head = newnode
          self.tail = newnode
        else:
          self.tail.linkn = newnode
          newnode.linkp = self.tail
          self.tail = newnode
        self.__summ+= data

    def addfirst(self, data):
        newnode = node(data)
        if not self.head:
          self.head = newnode
          self.tail = newnode
        else:
          newnode.linkn = self.head
          self.head.linkp = newnode
          self.head = newnode
        self.__summ+= data

    def printback(self):
        s = self.tail
        strr=""
        while s:
          strr+= str(s.data) + "<-"
          s = s.linkp
        return strr

    def printforward(self):
        s = self.head
        strr=""
        while s:
            strr+= str(s.data) + "->"
            s = s.linkn
        return strr

    def __len__(self):
        count = 0
        s = self.head
        while s:
          count += 1
          s = s.linkn
        return count

    def summ (self):
        "O(n)"
        summ = 0
        s = self.head
        while s:
          summ +=s.data
          s = s.linkn
        return summ

    def summo1 (self):
        "O(1)"
        return self.__summ

l = linklist2()
l.addnode(1)
l.addnode(2)
l.addnode(3)
print(l.summ())
l.summo1()

#2- реализовать функцию, которая удаляет все элементы с заданным значением из двусвязного списка.

class node:
    def __init__(self, data=None, linkn=None, linkp = None):
        self.data = data
        self.linkn = linkn
        self.linkp = linkp

class linklist2:
    def __init__(self):
        self.head = None
        self.tail = None
        self.__summ=0

    def addnode(self, data):
        newnode = node(data)
        if not self.head:
          self.head = newnode
          self.tail = newnode
        else:
          self.tail.linkn = newnode
          newnode.linkp = self.tail
          self.tail = newnode
        self.__summ+= data

    def printforward(self):
        s = self.head
        strr=""
        while s:
            strr+= str(s.data) + "->"
            s = s.linkn
        return strr

    def delfixed(self, number):
      s = self.head
      while s:
        if s.data == number:
          if s == self.head:
            #if s.linkn == None:
              #return None
            s.linkn.linkp = None
            self.head = s.linkn
          elif s != self.tail:
            s.linkn.linkp = s.linkp
            s.linkp.linkn = s.linkn
          elif s == self.tail:
            s.linkp.linkn = None
            s.linkp = None
        s = s.linkn

l = linklist2()
l.addnode(1)
l.addnode(2)
l.addnode(3)
l.addnode(2)
l.addnode(2)
l.addnode(1)
l.addnode(1)
print(l.printforward())
l.delfixed(1)
print(l.printforward())

#3- Реализовать функцию, которая удаляет все повторяющиеся элементы из двусвязного списка

class node:
    def __init__(self, data=None, linkn=None, linkp = None):
        self.data = data
        self.linkn = linkn
        self.linkp = linkp

class linklist2:
    def __init__(self):
        self.head = None
        self.tail = None
        self.__dict=dict()

    def addnode(self, data):
        newnode = node(data)
        if not self.head:
          self.head = newnode
          self.tail = newnode
        else:
          self.tail.linkn = newnode
          newnode.linkp = self.tail
          self.tail = newnode

    def printforward(self):
        s = self.head
        strr=""
        while s:
            strr+= str(s.data) + "->"
            s = s.linkn
        return strr

    def delpovtor(self):
      s = self.head
      while s:
        if s.data not in self.__dict:
          self.__dict[s.data] = 1
        else:
          if s == self.tail:
            s.linkp.linkn = None
          else:
            s.linkn.linkp = s.linkp
            s.linkp.linkn = s.linkn
        s = s.linkn

l = linklist2()
l.addnode(1)
l.addnode(2)
l.addnode(3)
l.addnode(2)
l.addnode(4)
l.addnode(1)
print(l.printforward())
l.delpovtor()
print(l.printforward())

#4- Реализовать функцию, которая разделяет двусвязный список на два списка, один из которых содержит все элементы, меньшие заданного значения, а другой — все элементы, большие или равные заданному значению.

class node:
    def __init__(self, data=None, linkn=None, linkp = None):
        self.data = data
        self.linkn = linkn
        self.linkp = linkp

class linklist2:
    def __init__(self):
        self.head = None
        self.tail = None
        self.__dict=dict()

    def addnode(self, data):
        newnode = node(data)
        if not self.head:
          self.head = newnode
          self.tail = newnode
        else:
          self.tail.linkn = newnode
          newnode.linkp = self.tail
          self.tail = newnode

    def printforward(self):
        s = self.head
        strr=""
        while s:
            strr+= str(s.data) + "->"
            s = s.linkn
        return strr

    def splitlist(self, number):
      minlist = linklist2()
      maxlist = linklist2()
      s = self.head
      while s:
        if s.data < number:
          minlist.addnode(s.data)
        else:
          maxlist.addnode(s.data)
        s = s.linkn
      return (minlist.printforward(), maxlist.printforward())

l = linklist2()
l.addnode(1)
l.addnode(2)
l.addnode(3)
l.addnode(3)
l.addnode(0)
l.addnode(5)
print(l.printforward())
l.splitlist(3)

# стэк на основе двусвязного списка

class node:
  def __init__(self, data=None, next=None, prev=None):
    self.data = data
    self.next = next
    self.prev = prev

class Stack:
  def __init__(self):
    self.head = None
    self.tail = None
  def addnodetoend(self, data):
    newnode = node(data)
    if not self.head:
      self.head = newnode
      self.tail = newnode
    else:
      self.tail.next = newnode
      self.tail = newnode
  def popnodefromend(self):
    if not self.tail:
      return None
    else:
      data = self.tail.data
      self.tail = self.tail.prev
    return data
  def __str__(self):
    l = []
    item = self.head
    if item is None:
      return ''
    l.append(item.data)
    while (item.next):
      item = item.next
      l.append(item.data)
    return str(l)

s = Stack()
s.addnodetoend(1)
s.addnodetoend(2)
s.addnodetoend(3)
print(s)
k = s.popnodefromend()
print(k)
print(s)
"""