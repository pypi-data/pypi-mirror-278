def sort():
    """
def comb_sort(arr):
    n = len(arr)
    shrink = 1.3
    gap = n
    swap = True
    while swap:
        gap = int(gap /shrink)
        if gap < 1:
            gap = 1
        i = 0
        swap = False
        while gap + i < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swap = True
            i += 1
    return arr

------------------------------------------

def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return arr

------------------------------------------

def insert_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break
    return arr

--------------------------------------------

def coctail_sort(arr):
    n = len(arr)
    start = 0
    end = n - 1
    swap = True
    while swap:
        swap = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swap = True
        if not swap:
            break

        swap = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swap = True
        start += 1
    return arr

---------------------------

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

def merge(left, right):
    res = []
    i = j = 0
    while len(left) > i and len(right) > j:
        if left[i] < right[j]:
            res.append(left[i])
            i+=1
        else:
            res.append(right[j])
            j+=1
    res += left[i:]
    res += right[j:]
    return res

-------------------------------------------

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    n = len(arr)
    piv = arr[n//2]
    left = [x for x in arr if x < piv]
    mid = [x for x in arr if x == piv]
    right = [x for x in arr if x > piv]
    return quicksort(left) + mid + quicksort(right)

----------------------
    """

def lst():
    """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node


    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next


doubly_linked_list = DoublyLinkedList()
doubly_linked_list.append(1)
doubly_linked_list.append(2)
doubly_linked_list.append(3)
doubly_linked_list.print_list()

---------------------------------------

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
        print()


queue = Queue()

queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)

print("Очередь:")
queue.print_queue()

print("Извлечение элемента из очереди:", queue.dequeue())
print("Очередь после извлечения:")
queue.print_queue()

print("Проверка на пустоту", queue.is_empty())

-----------------------------------------------------

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

    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next


llist = LinkedList()
llist.append("A")
llist.append("B")
llist.append("C")
llist.print_list()

--------------------------

class Stack:
    def __init__(self, max_size):
        self.stack = []
        self.max_size = max_size

    def push(self, element):
        if len(self.stack) >= self.max_size:
            raise Exception("Стек переполнен")
        self.stack.append(element)

    def pop(self):
        if self.is_empty():
            raise Exception("Стек пуст")
        return self.stack.pop()

    def top(self):
        if self.is_empty():
            raise Exception("Стек пуст")
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)



stack = Stack(5)
print(stack.is_empty())
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.top())
print(len(stack))
stack.pop()
print(stack.top())
stack.push(4)
stack.push(5)
print(len(stack))

    """