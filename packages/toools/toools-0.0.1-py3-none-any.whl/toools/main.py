def sort():
    return """
#пузырек лучший О(n) общая и худшая O(n**2)
def bubble_sort_2(a_list):
    for pass_num in range(len(a_list) - 1, 0, -1):
        flag = False
        for i in range(pass_num):
            if a_list[i] > a_list[i + 1]:
                temp = a_list[i]
                a_list[i] = a_list[i + 1]
                a_list[i + 1] = temp
                flag = True
        if not flag:
            return a_list

bubble_sort_2(list(test_list))

#Сортировка выбором (извлечением) (Selection Sort) лучший, общая и худшая O(n**2)

#С учетом того, что количество рассматриваемых на очередном шаге элементов уменьшается на единицу, общее количество операций:
#(n-1)+(n-2)+(n-3)+...+1 = 1/2(n-1)(n-1+1) = 1/2(n^2-n)=O(n^2)

#По сравнению с обменной сортировкой:
#(+) существенно меньше перестановок элементов O(n) по сравнению O(n^2)
#(–) нет возможности быстро отсортировать почти отсортированный массив

#Естественной идеей улучшения алгоритма выбором является идея использования информации, полученной при сравнении элементов при поиске максимального (минимального) элемента на предыдущих шагах.
В общем случае, если — точный квадрат, можно разделить массив на n^1/2 групп по n^1/2 лементов и находить максимальный элемент в каждой подгруппе. Любой выбор, кроме первого, требует не более чем (n-2)^1/2 сравнений внутри группы ранее выбранного элемента плюс (n-1)^1/2 сравнений среди «лидеров групп» Этот метод получил название квадратичный выбор общее время его работы составляет порядка O(n*(n)^1/2) что существенно лучше, чем O(n^2)
def selection_sort(a_list):
    for fill_slot in range(len(a_list) - 1, 0, -1):
        pos_of_max = 0
        for location in range(1, fill_slot + 1):
            if a_list[location] > a_list[pos_of_max]:
                pos_of_max = location

        temp = a_list[fill_slot]
        a_list[fill_slot] = a_list[pos_of_max]
        a_list[pos_of_max] = temp
    return a_list

selection_sort(list(test_list))


#Сортировка включением (вставками) (Insertion Sort)
лучший О(n) общая и худшая O(n**2)

Алгоритм имеет сложность O(n^2) , но в случае исходно отсортированного массива внутренний цикл не будет выполняться ни разу, поэтому метод имеет в этом случае временную сложность O(n) (+) является эффективным алгоритмом для маленьких наборов данных; (+) на практике более эффективен, чем остальные простые квадратичные сортировки.

def insertion_sort(a_list):
    for index in range(1, len(a_list)):

        current_value = a_list[index]
        position = index

        while position > 0 and a_list[position - 1] > current_value:
            a_list[position] = a_list[position - 1]
            position -= 1

        a_list[position] = current_value
    return a_list

insertion_sort(list(test_list))

#улучшение 1-ый минимальный максимум вправо минимальный влево

#Сортировка Шелла (Shell Sort)

#лучший nlog(n) средний n*(4/3) плохой n **(3/2)

def gap_insertion_sort(a_list, start, gap):
    for i in range(start + gap, len(a_list), gap):
        current_value = a_list[i]
        position = i

        while position >= gap and a_list[position - gap] > current_value:
            a_list[position] = a_list[position - gap]

            position = position - gap

        a_list[position] = current_value


def shell_sort(a_list):
    sublist_count = len(a_list) // 2
    while sublist_count > 0:
        for start_position in range(sublist_count):
            gap_insertion_sort(a_list, start_position, sublist_count)

        print("After inc. of size", sublist_count, "Lst:", a_list)

        sublist_count = sublist_count // 2

shell_sort(list(test_list))

#Для достаточно больших массивов рекомендуемой считается такая последовательность, что h(i+1) = 3h(i) + 1, h(1) = 1
#получается последовательность : 1, 4, 13, 40, 121,...,(h(i+1) = 3h(i) + 1) 
#Начинается процесс с h(m-2) такого, что: h(m-2) >= [n/9]

#Быстрая сортировка (Quick Sort)
def quick_sort(a_list):
    quick_sort_helper(a_list, 0, len(a_list) - 1)
    return a_list

def quick_sort_helper(a_list, first, last):
    if first < last:

        split_point = partition(a_list, first, last)
        #print(a_list[first:split_point-1+1], a_list[split_point], a_list[split_point + 1:last+1])

        quick_sort_helper(a_list, first, split_point - 1)
        quick_sort_helper(a_list, split_point + 1, last)

def partition(a_list, first, last):
    pivot_value = a_list[first]

    left_mark = first + 1
    right_mark = last

    done = False
    while not done:

        while left_mark <= right_mark and a_list[left_mark] <= pivot_value:
            left_mark = left_mark + 1

        while a_list[right_mark] >= pivot_value and right_mark >= left_mark:
            right_mark = right_mark - 1

        if right_mark < left_mark:
            done = True
        else:
            temp = a_list[left_mark]
            a_list[left_mark] = a_list[right_mark]
            a_list[right_mark] = temp

    temp = a_list[first]
    a_list[first] = a_list[right_mark]
    a_list[right_mark] = temp

    return right_mark

quick_sort(list(test_list))

#лучший nlog(n) средний nlogn худший n**2

#улучшение брать не первый а рандомный и в идеале наибольший

##Сортировка слиянием (Merge Sort)
def merge_sort(a_list):
    print("Splitting ", a_list)
    if len(a_list) > 1:
        mid = len(a_list) // 2
        left_half = a_list[:mid]
        right_half = a_list[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = 0
        j = 0
        k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                a_list[k] = left_half[i]
                i += 1
            else:
                a_list[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            a_list[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            a_list[k] = right_half[j]
            j += 1
            k += 1

        print("Merging ", a_list)
    return a_list

merge_sort(list(test_list))

#все разы nlog(n)
"""

def two():
    return """
#СТЕК
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

# Пример использования
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(f"Stack after pushes: {stack}")  # Output: [1, 2, 3]
print(f"Popped item: {stack.pop()}")   # Output: 3
print(f"Stack after pop: {stack}")     # Output: [1, 2]
print(f"Peek item: {stack.peek()}")    # Output: 2
print(f"Is stack empty? {stack.is_empty()}")  # Output: False
print(f"Stack size: {stack.size()}")   # Output: 2


#ОЧЕРЕДЬ
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.items[0]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

# Пример использования
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(f"Queue after enqueues: {queue}")  # Output: [1, 2, 3]
print(f"Dequeued item: {queue.dequeue()}")  # Output: 1
print(f"Queue after dequeue: {queue}")     # Output: [2, 3]
print(f"Peek item: {queue.peek()}")    # Output: 2
print(f"Is queue empty? {queue.is_empty()}")  # Output: False
print(f"Queue size: {queue.size()}")   # Output: 2

#ОДНОНАПРАВЛЕННЫЙ СПИСОК
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        if self.is_empty():
            return

        # Если нужно удалить голову списка
        if self.head.data == key:
            self.head = self.head.next
            return

        # Поиск узла для удаления
        current = self.head
        while current.next and current.next.data != key:
            current = current.next

        if current.next:
            current.next = current.next.next

    def search(self, key):
        current = self.head
        while current and current.data != key:
            current = current.next
        return current

    def __str__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)

# Пример использования
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
print(f"Linked list after appends: {ll}")  # Output: 1 -> 2 -> 3

ll.prepend(0)
print(f"Linked list after prepend: {ll}")  # Output: 0 -> 1 -> 2 -> 3

ll.delete(2)
print(f"Linked list after deletion: {ll}")  # Output: 0 -> 1 -> 3

found_node = ll.search(1)
print(f"Found node: {found_node}")  # Output: 1

not_found_node = ll.search(4)
print(f"Not found node: {not_found_node}")  # Output: None



#ДВУНАПРАВЛЕННЫЙ СПИСОК
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.data)

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def prepend(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def delete(self, key):
        if self.is_empty():
            return

        current = self.head
        while current and current.data != key:
            current = current.next

        if current is None:
            return  # Узел с таким значением не найден

        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

    def search(self, key):
        current = self.head
        while current and current.data != key:
            current = current.next
        return current

    def __str__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " <-> ".join(nodes)

# Пример использования
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
print(f"Doubly linked list after appends: {dll}")  # Output: 1 <-> 2 <-> 3

dll.prepend(0)
print(f"Doubly linked list after prepend: {dll}")  # Output: 0 <-> 1 <-> 2 <-> 3

dll.delete(2)
print(f"Doubly linked list after deletion: {dll}")  # Output: 0 <-> 1 <-> 3

found_node = dll.search(1)
print(f"Found node: {found_node}")  # Output: 1

not_found_node = dll.search(4)
print(f"Not found node: {not_found_node}")  # Output: None

#БИНАРНЫЙ ПОИСК

#в словаре

def binary_search(d, x, p=1):
    arr = [item for item in d.items()]
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid][p] == x:
            return mid
        elif arr[mid][p] < x: 
            low = mid + 1
        else:
            high = mid - 1
    return 'not in dict'

"""

def three():
    return """
#ДЕКОРАТОР
def validate_arguments(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not all(f(arg) for arg in args):
                raise ValueError("Invalid argument passed")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_arguments(lambda x: x > 0)
def calculate_cube_volume(x):
    return x**3
print(calculate_cube_volume(3))
print(calculate_cube_volume(-3))

#####

def exception_handler(def_response):
    def decorator(func):
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except :
                return def_response
        return wrapper
    return decorator

@exception_handler(def_response='An error occured!')
def divide_numbers(x,y):
    return x/y

divide_numbers(1,10)
#####

def exception_handler(def_response):
    def decorator(func):
        def wrapper(*args,**kwargs):
            if len(args)!=2:
                return print(def_response)
            if args[1] == 0 :
                return print(def_response)
            else:
                return func(*args,**kwargs)
        return wrapper
    return decorator

@exception_handler(def_response='An error occured!')
def divide_numbers(x,y):
    return x/y

divide_numbers(1,10)
#####

def convert_to_data_type(f):
    def decorator(func):
        def wrapper(*args,**kwargs):
            return f(func(*args,**kwargs))
        return wrapper
    return decorator
@convert_to_data_type(str)
def concatenate_strings(x,y):
    return x+y
"""
def four():
    return """
1. Концепция класса и объекта. Принципы и механизмы ООП.
Класс в Python — это шаблон, определяющий структуру и поведение объектов, которые могут быть созданы на его основе. Объект — это экземпляр класса, обладающий уникальным состоянием и поведением. Основные принципы объектно-ориентированного программирования (ООП) включают инкапсуляцию (скрытие деталей реализации и предоставление публичного интерфейса), наследование (способность одного класса унаследовать свойства и методы другого класса), полиморфизм (возможность использования объектов разных классов через единый интерфейс) и абстракцию (выделение ключевых характеристик объекта и сокрытие ненужных деталей).

2. Объявление класса, конструктор, создание объектов и одиночное наследование в Python. Управление доступом к атрибутам класса в Python.
В Python класс объявляется с использованием ключевого слова class, за которым следует имя класса. Конструктор — это специальный метод __init__, который вызывается при создании нового объекта класса и инициализирует его атрибуты. Одиночное наследование позволяет одному классу (подклассу) наследовать атрибуты и методы другого класса (базового класса). Управление доступом к атрибутам осуществляется с помощью соглашений о наименовании: атрибуты, начинающиеся с одного подчеркивания (_), считаются защищенными, а с двумя подчеркиваниями (__) — приватными.

3. Полиморфизм и утиная типизация и проверка принадлежности объекта к классу в языке Python.
Полиморфизм в Python позволяет функциям и методам обрабатывать объекты различных типов, если они поддерживают необходимый интерфейс или методы. Утиная типизация (duck typing) означает, что тип объекта определяется не его классом, а набором методов и свойств, которые он поддерживает: "Если что-то выглядит как утка, плавает как утка и крякает как утка, то это, вероятно, утка". Проверка принадлежности объекта к классу выполняется с помощью функции isinstance(obj, Class) или issubclass(SubClass, Class).

4. Методы классов и статические переменные и методы в Python. Специальные методы для использования пользовательских классов со стандартными операторами и функциями.
Методы классов определяются внутри класса и принимают первым аргументом ссылку на экземпляр класса (обычно self). Статические методы и переменные связаны с самим классом, а не с его экземплярами, и определяются с помощью декоратора @staticmethod. Специальные методы, такие как __str__, __repr__, __eq__, __lt__ и другие, позволяют переопределить поведение стандартных операторов и функций (например, сравнение, преобразование в строку и т. д.) для пользовательских классов, что обеспечивает более интуитивное и удобное использование объектов этих классов.

5. Основные возможности, поддерживаемые функциональными языками программирования. Поддержка элементов функционального программирования в Python.
Функциональные языки программирования поддерживают такие возможности, как функции высшего порядка (функции, принимающие или возвращающие другие функции), чистые функции (без побочных эффектов), неизменяемость данных, каррирование и композицию функций. В Python элементы функционального программирования включают функции map, filter, reduce, поддержку лямбда-функций, функции высшего порядка, а также встроенные функции, такие как all, any, sum и sorted.

6. Концепция «функции – граждане первого класса» в языке программирования, поддержка этой концепции в Python. Специфика лямбда-функций в Python их возможности и ограничения. Типичные сценарии использования лямбда-функций в Python.
Концепция "функции – граждане первого класса" означает, что функции можно передавать как аргументы другим функциям, возвращать их из других функций, присваивать переменным и хранить в структурах данных. В Python это полностью поддерживается. Лямбда-функции — это анонимные функции, создаваемые с помощью ключевого слова lambda. Они ограничены одним выражением и используются в случаях, когда необходимо создать небольшую, короткую функцию. Типичные сценарии использования включают сортировку, фильтрацию и трансформацию данных в комбинации с функциями высшего порядка.

7. Глобальные и локальные переменные в функциях на примере Python. Побочные эффекты вызова функций и их последствия.
В Python переменные, объявленные внутри функции, являются локальными и видны только в пределах этой функции. Глобальные переменные объявляются вне функции и доступны из любой точки кода. Использование глобальных переменных может привести к непредсказуемым побочным эффектам, так как изменение их значений в одной части программы может влиять на другую часть программы, что затрудняет отладку и тестирование. Локальные переменные уменьшают вероятность побочных эффектов и делают код более предсказуемым.

8. Вложенные функции и замыкания, специфика реализации в Python.
Вложенные функции определяются внутри других функций и могут использовать переменные из внешней функции. Замыкания — это функции, которые "замыкают" значения из своей области видимости на момент их создания, даже если внешняя функция завершила выполнение. В Python это достигается за счет механизма хранения состояния функции. Замыкания используются для создания функций с предварительно настроенным поведением и данных.

9. Функции высшего порядка и декораторы в Python.
Функции высшего порядка принимают другие функции в качестве аргументов или возвращают их. Декораторы — это функции высшего порядка, которые изменяют или расширяют поведение других функций. Они определяются с помощью символа @ перед именем функции и широко используются для добавления функциональности, такой как логирование, контроль доступа и управление кэшированием.

10. Концепция map/filter/reduce. Реализация map/filter/reduce в Python и пример их использования.
map, filter и reduce — это функции для обработки и преобразования коллекций данных. map применяет функцию к каждому элементу и возвращает итератор с результатами. filter отбирает элементы, удовлетворяющие условию, заданному функцией. reduce применяет функцию к элементам и сводит их к одному значению. В Python map и filter встроены, а reduce доступен в модуле functools.

11. Итераторы в Python: встроенные итераторы, создание собственных итераторов, типичные способы обхода итераторов и принцип их работы. Встроенные функции для работы с итераторами и возможности модуля itertools.
Итераторы в Python позволяют последовательно обходить элементы коллекций. Встроенные итераторы включают списки, кортежи, словари и строки. Для создания собственных итераторов в классе необходимо определить методы __iter__ и __next__. Типичные способы обхода итераторов включают использование цикла for и функции next. Итераторы работают по принципу ленивых вычислений, возвращая элементы по одному. Встроенные функции для работы с итераторами включают iter и next. Модуль itertools предоставляет дополнительные возможности для работы с итераторами, такие как генерация последовательностей, фильтрация и комбинирование элементов. Среди функций itertools наиболее полезны chain, cycle, repeat, combinations и permutations.

12. Функции генераторы и выражения генераторы: создание и применение в Python.
Генераторы создаются с помощью ключевого слова yield и позволяют возвращать значения по одному за раз, сохраняя состояние между вызовами. Это делает генераторы эффективными для обработки больших данных и потоков. Выражения генераторы создаются с помощью синтаксиса, похожего на списковые включения, но используют круглые скобки и создают итераторы. Они удобны для лаконичной записи и экономии памяти.

13. Специфика массивов, как структур данных. Динамические массивы – специфика работы, сложность операций. Специфика работа с array в Python.
Массивы — это структуры данных, представляющие собой коллекцию элементов, доступных по индексам. В отличие от статических массивов, динамические массивы могут изменять свой размер во время выполнения. Основные операции, такие как добавление или удаление элемента, могут иметь разные временные сложности. Вставка в конец динамического массива обычно выполняется за O(1), но в худшем случае может быть O(n), если требуется увеличение размера массива. В Python основным аналогом массивов является список (list), который реализован как динамический массив. Для работы с массивами фиксированного типа данных используется модуль array.

14. Абстрактная структура данных стек и очередь: базовые и расширенные операции, их сложность.
Стек (LIFO — Last In, First Out) поддерживает операции push (добавление элемента) и pop (удаление последнего добавленного элемента), обе с временной сложностью O(1). Очередь (FIFO — First In, First Out) поддерживает операции enqueue (добавление элемента) и dequeue (удаление первого добавленного элемента), также с временной сложностью O(1). Расширенные операции могут включать просмотр верхнего элемента стека или первого элемента очереди без удаления их, что тоже выполняется за O(1).

15. Специфика реализации и скорости основных операций в очереди на базе массива и связанного списка.
Очередь, реализованная на базе массива, часто использует кольцевой буфер для эффективного использования памяти и предотвращения сдвига элементов. Основные операции, такие как enqueue и dequeue, выполняются за O(1), но при заполнении массива требуется увеличение его размера, что выполняется за O(n). Очередь на основе связанного списка использует узлы, каждый из которых содержит элемент и ссылку на следующий узел. Основные операции в этом случае выполняются за O(1) и не требуют пересоздания структуры.

16. Связанные списки: однонаправленные и двунаправленные – принцип реализации. Сравнение скорости выполнения основных операций в связанных списках и в динамическом массиве.
Однонаправленные списки содержат узлы с элементом и ссылкой на следующий узел, а двунаправленные — ссылки на следующий и предыдущий узлы. Вставка и удаление элементов в начале или в середине списка выполняются за O(1) в обоих видах связанных списков. В динамических массивах вставка или удаление элемента в середине требует сдвига элементов и выполняется за O(n). Доступ по индексу в динамических массивах выполняется за O(1), тогда как в связанных списках требуется последовательный обход и выполняется за O(n).

17. Алгоритм обменной сортировки, сложность сортировки и возможности по ее улучшению.
Алгоритм обменной сортировки (или пузырьковой сортировки) работает путем многократного прохода по массиву и обмена соседних элементов, если они находятся в неправильном порядке. Основная сложность этого алгоритма заключается в его временной сложности O(n²) в худшем и среднем случаях. Возможности улучшения включают оптимизацию алгоритма путем добавления флага, который прекращает выполнение, если массив отсортирован на раннем этапе, что может снизить количество ненужных проходов.

18. Алгоритм сортировки выбором, сложность сортировки и возможности по ее улучшению.
Алгоритм сортировки выбором работает путем нахождения минимального (или максимального) элемента и его перемещения на начало (или конец) массива, затем этот процесс повторяется для оставшихся элементов. Временная сложность этого алгоритма также составляет O(n²) в худшем и среднем случаях. Возможности улучшения включают использование двоичной кучи (Binary Heap) для уменьшения сложности поиска минимального элемента, что может снизить общую сложность.

19. Алгоритм сортировки вставками, его сложность. Алгоритм быстрого поиска в отсортированном массиве. Сложность поиска в отсортированном и не отсортированном массиве.
Алгоритм сортировки вставками работает путем построения отсортированного массива один элемент за раз, вставляя каждый новый элемент в нужную позицию. Временная сложность этого алгоритма O(n²) в худшем случае и O(n) в лучшем случае (когда массив почти отсортирован). Быстрый поиск в отсортированном массиве осуществляется с помощью бинарного поиска, который имеет временную сложность O(log n). Поиск в неотсортированном массиве требует линейного прохода и имеет сложность O(n).

20. Алгоритм сортировки Шелла, сложность сортировки и возможности по ее улучшению.
Алгоритм сортировки Шелла является усовершенствованной версией сортировки вставками, где элементы перемещаются на несколько позиций за раз (расстояние между элементами уменьшается с каждым шагом). Временная сложность зависит от выбора промежутков (gap sequence) и варьируется от O(n^2) до O(n log^2 n) или лучше для некоторых оптимальных последовательностей промежутков. Возможности улучшения включают выбор оптимальных промежутков, таких как последовательности Кнута или Прэтта.

21. Алгоритм быстрой сортировки, сложность сортировки и возможности по ее улучшению.
Алгоритм быстрой сортировки (Quick Sort) работает путем выбора опорного элемента (pivot), разбиения массива на два подмассива (меньшие и большие опорного) и рекурсивной сортировки подмассивов. Средняя сложность O(n log n), но в худшем случае может быть O(n²), если опорный элемент выбирается неудачно. Возможности улучшения включают выбор лучшего опорного элемента (например, медианы из трех) и использование гибридных алгоритмов, таких как Quick Sort + Insertion Sort для небольших подмассивов.

22. Алгоритм сортировки слиянием, сложность сортировки.
Алгоритм сортировки слиянием (Merge Sort) работает путем рекурсивного разбиения массива на две половины, их сортировки и последующего слияния отсортированных половин. Временная сложность этого алгоритма составляет O(n log n) в худшем, среднем и лучшем случаях. Этот алгоритм стабилен и хорошо работает с большими объемами данных, но требует дополнительной памяти O(n) для временного хранения элементов во время слияния.

23. Реализация двоичных деревьев в виде связанных объектов. Различные реализации рекурсивного обхода двоичных деревьев.
Двоичное дерево реализуется как набор связанных объектов, где каждый узел содержит значение и ссылки на левое и правое поддерево. Основные типы рекурсивного обхода двоичных деревьев включают:

Прямой (preorder): посещение узла, затем левого и правого поддеревьев.
Симметричный (inorder): посещение левого поддерева, затем узла и правого поддерева.
Обратный (postorder): посещение левого и правого поддеревьев, затем узла.
Эти методы обхода используются для различных задач, таких как печать элементов в определенном порядке или выполнения вычислений над элементами дерева.

24. Двоичное дерево поиска – принципы реализации и логика реализации основных операций.
Двоичное дерево поиска (BST) — это структура данных, где для каждого узла все элементы в левом поддереве меньше, а все элементы в правом поддереве больше значения узла. Основные операции включают:

Вставка: поиск подходящей позиции для нового узла и его добавление.
Поиск: последовательное сравнение искомого значения с узлами, пока не найден нужный узел или не достигнут конец дерева.
Удаление: удаление узла с перестроением дерева для сохранения свойств BST. При удалении узла с двумя дочерними узлами заменяем его на наименьший узел в правом поддереве.
Все эти операции имеют среднюю временную сложность O(log n), но в худшем случае могут быть O(n).

25. Двоичная куча – принципы реализации и логика реализации основных операций.
Двоичная куча — это полное бинарное дерево, в котором каждый узел подчинен свойству кучи: для максимальной кучи каждый родительский узел больше или равен своим дочерним узлам, а для минимальной кучи — меньше или равен. Основные операции включают:

Вставка: добавление элемента в конец и восстановление свойства кучи путем подъема узла (swim).
Удаление максимального (или минимального) элемента: замена корневого узла последним элементом и восстановление свойства кучи путем спуска узла (sink).
Построение кучи: преобразование массива в кучу за время O(n).
Вставка и удаление имеют временную сложность O(log n).

26. Абстрактный тип данных - ассоциативный массив и принцип его реализации на основе хэш-таблиц и хэш-функций.
Ассоциативный массив (или словарь) — это структура данных, которая хранит пары ключ-значение и позволяет быстро находить значение по ключу. Основой реализации являются хэш-таблицы, которые используют хэш-функции для преобразования ключей в индексы массива. В Python ассоциативные массивы реализованы в виде словарей (dict), которые обеспечивают среднюю временную сложность O(1) для операций вставки, поиска и удаления.

27. Общая схема построения хэш-функции и возможная роль в этой схеме хэш-функции multiply-add-and-divide. Принцип работы хэш-функции multiply-add-and-divide.
Хэш-функция преобразует ключ в индекс массива. Хэш-функция multiply-add-and-divide (MAD) работает по формуле: h(k) = (a * k + b) % p % m, где k — ключ, a и b — случайные целые числа, p — большое простое число, а m — размер хэш-таблицы. MAD минимизирует коллизии и равномерно распределяет ключи по таблице.

28. Полиномиальная хэш-функция – принцип работы, специфика эффективной реализации и специфика применения хэш-функции.
Полиномиальная хэш-функция вычисляет хэш по формуле: h(k) = Σ(k_i * p^i) % m, где k_i — символы ключа, p — базовое число (обычно простое), m — модуль. Эта функция хорошо распределяет строки и эффективна для текстовых данных. Эффективная реализация достигается за счет использования свойства распределенности простых чисел и техники модульной арифметики.

29. Различные методы разрешения коллизий в хэш-таблицах.
Коллизии возникают, когда два ключа хэшируются в один и тот же индекс. Методы разрешения коллизий включают:

Открытая адресация: поиск следующего свободного места в таблице с использованием линейного пробирования, квадратичного пробирования или двойного хэширования.
Цепочки (chaining): хранение элементов с одинаковым хэш-значением в связном списке или другом контейнере.
Оба метода имеют свои преимущества и недостатки. Открытая адресация эффективнее по памяти, но цепочки проще в реализации и расширении.
"""

def car():
    return """
class Car:
    def __init__(self, brand, model, year, speed=0):
        self.brand = brand
        self.model = model
        self.year = year
        self.speed = speed

    def increase_speed(self, increment):
        self.speed += increment

    def decrease_speed(self, decrement):
        self.speed -= decrement
        if self.speed < 0:
            self.speed = 0

    def __eq__(self, other):
        if isinstance(other, Car):
            return self.speed == other.speed
        return False

    def __str__(self):
        return f"Автомобиль {self.brand} {self.model}, год выпуска - {self.year}, скорость - {self.speed}"

# Пример использования класса
car1 = Car("Toyota", "Corolla", 2020)
car2 = Car("Honda", "Civic", 2019)

car1.increase_speed(50)
car2.increase_speed(50)

print(car1)  # Автомобиль Toyota Corolla, год выпуска - 2020, скорость - 50
print(car2)  # Автомобиль Honda Civic, год выпуска - 2019, скорость - 50

# Сравнение скоростей
print(car1 == car2)  # True
"""

def nine():
    return """
import time

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения: {end_time - start_time:.6f} секунд")
        return result
    return wrapper

@time_decorator
def insertion_sort(products, ascending=True):
    for i in range(1, len(products)):
        key = products[i]
        j = i - 1
        while j >= 0 and ((key[1] < products[j][1]) if ascending else (key[1] > products[j][1])):
            products[j + 1] = products[j]
            j -= 1
        products[j + 1] = key
    return products

# Пример списка товаров и продаж до сортировки
products = [("Товар1", 53), ("Товар2", 72), ("Товар3", 30), ("Товар4", 85), ("Товар5", 47)]

# Сортировка по возрастанию
sorted_products_ascending = insertion_sort(products.copy(), ascending=True)
print("Сортировка по возрастанию:")
for product in sorted_products_ascending:
    print(product)

# Сортировка по убыванию
sorted_products_descending = insertion_sort(products.copy(), ascending=False)
print("\nСортировка по убыванию:")
for product in sorted_products_descending:
    print(product)


Специфика лямбда-функций в Python

Лямбда-функции в Python — это небольшие анонимные функции, которые определяются с помощью ключевого слова lambda. Они используются для создания простых функций на лету.
Ограничения лямбда-функций:

 1. Ограниченная функциональность:
Лямбда-функции могут содержать только одно выражение, что делает их менее мощными по сравнению с обычными функциями, которые могут содержать несколько операторов и более сложную логику.
 2. Отсутствие имени:
Лямбда-функции анонимны (не имеют имени), что может затруднить их отладку и чтение кода.

Типичные сценарии использования лямбда-функций:

 1. Кратковременные функции:
Использование лямбда-функций для создания временных, одноразовых функций, которые используются на месте и не требуются в других частях программы.
 2. Функции высшего порядка:
Передача лямбда-функций в функции высшего порядка, такие как map(), filter(), и sorted().
 3. Конструкции функционального программирования:
Применение лямбда-функций в функциональном программировании, где функции являются основными строительными блоками для обработки данных.
"""

def six():
    return """
 ##1Алгоритм обменной сортировки, сложность сортировки и возможности по ее улучшению.
Алгоритм обменной сортировки (или пузырьковой сортировки) работает путем многократного прохода по массиву и обмена соседних элементов, если они находятся в неправильном порядке. Основная сложность этого алгоритма заключается в его временной сложности O(n²) в худшем и среднем случаях. Возможности улучшения включают оптимизацию алгоритма путем добавления флага, который прекращает выполнение, если массив отсортирован на раннем этапе, что может снизить количество ненужных проходов.


##2
class Person:
    def __init__(self, name, country, date_of_birth):
        self.name = name
        self.country = country
        self.date_of_birth = date_of_birth

    def __str__(self):
        return f"{self.name}, {self.country}, {self.date_of_birth}"

# Пример использования
person = Person("Иван Иванов", "Россия", "1990-01-01")
print(person)


##3
import time
import string

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения {func.__name__}: {end_time - start_time:.6f} секунд")
        return result
    return wrapper

class WordSorter:
    def __init__(self, filepath):
        self.words = self.read_words_from_file(filepath)
    
    def read_words_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            # Удаляем пунктуацию и разбиваем текст на слова
            translator = str.maketrans('', '', string.punctuation)
            text = text.translate(translator)
            words = text.split()
        return words
    
    @time_decorator
    def insertion_sort(self, words, ascending=True):
        for i in range(1, len(words)):
            key = words[i]
            j = i - 1
            while j >= 0 and ((words[j] > key and ascending) or (words[j] < key and not ascending)):
                words[j + 1] = words[j]
                j -= 1
            words[j + 1] = key
        return words
    
    @time_decorator
    def selection_sort(self, words, ascending=True):
        for i in range(len(words)):
            min_idx = i
            for j in range(i + 1, len(words)):
                if (words[j] < words[min_idx] and ascending) or (words[j] > words[min_idx] and not ascending):
                    min_idx = j
            words[i], words[min_idx] = words[min_idx], words[i]
        return words

    def sort_words(self, method='insertion', ascending=True):
        if method == 'insertion':
            return self.insertion_sort(self.words[:], ascending)
        elif method == 'selection':
            return self.selection_sort(self.words[:], ascending)
        else:
            raise ValueError("Unsupported sorting method")

# Пример использования
filepath = 'text.txt'  # Укажите путь к вашему файлу с текстом
word_sorter = WordSorter(filepath)

# Сортировка вставками по возрастанию
sorted_words_insertion_asc = word_sorter.sort_words(method='insertion', ascending=True)
print("Сортировка вставками по возрастанию:", sorted_words_insertion_asc)

# Сортировка вставками по убыванию
sorted_words_insertion_desc = word_sorter.sort_words(method='insertion', ascending=False)
print("Сортировка вставками по убыванию:", sorted_words_insertion_desc)

# Сортировка выбором по возрастанию
sorted_words_selection_asc = word_sorter.sort_words(method='selection', ascending=True)
print("Сортировка выбором по возрастанию:", sorted_words_selection_asc)

# Сортировка выбором по убыванию
sorted_words_selection_desc = word_sorter.sort_words(method='selection', ascending=False)
print("Сортировка выбором по убыванию:", sorted_words_selection_desc)

"""