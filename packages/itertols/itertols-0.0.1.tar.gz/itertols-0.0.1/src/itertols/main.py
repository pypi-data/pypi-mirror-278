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
 pp
