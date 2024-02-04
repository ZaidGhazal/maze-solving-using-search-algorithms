"""This file contains the data structures used in the project."""

class Stack:
    """Stack data structure."""

    def __init__(self):
        """Initialize the stack."""
        self.stack = []

    def push(self, item):
        """Push an item to the stack."""
        self.stack.append(item)

    def pop(self):
        """Pop an item from the stack."""
        return self.stack.pop()

    def peek(self):
        """Peek at the top item in the stack."""
        return self.stack[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.stack) == 0

    def size(self):
        """Get the size of the stack."""
        return len(self.stack)
    
    def __str__(self):
        """Return the string representation of the stack."""
        return str(self.stack)
    

class Queue:
    """Queue data structure."""

    def __init__(self):
        """Initialize the queue."""
        self.queue = []

    def enqueue(self, item):
        """Enqueue an item to the queue."""
        self.queue.append(item)

    def dequeue(self):
        """Dequeue an item from the queue."""
        return self.queue.pop(0)

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.queue) == 0

    def size(self):
        """Get the size of the queue."""
        return len(self.queue)
    
    def __str__(self):
        """Return the string representation of the queue."""
        return str(self.queue)
    
class PriorityQueue:
    """Priority Queue data structure."""
    
    def __init__(self):
        """Initialize the priority queue."""
        self.queue = []

    def enqueue(self, item, priority):
        """Enqueue an item to the priority queue."""
        self.queue.append((item, priority))
        self.queue = sorted(self.queue, key=lambda x: x[1])

    def dequeue(self):
        """Dequeue an item from the priority queue."""
        return self.queue.pop(0)[0] ## Return the item only

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self.queue) == 0

    def size(self):
        """Get the size of the priority queue."""
        return len(self.queue)
    
    def __str__(self):
        """Return the string representation of the priority queue."""
        return str(self.queue)