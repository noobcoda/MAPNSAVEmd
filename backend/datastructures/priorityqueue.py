#https://www.geeksforgeeks.org/binary-heap/

#if N denotes index of parent node then
#2N is left child node
#2N+1 is right child node
#where N=1,2,3...

#BINARY HEAP -- LEFT TO RIGHT, TOP TO BOTTOM

class MyMinHeap:
    def __init__(self):
        self.list = [0] #be aware, as index starts from 0, start saving inputs from index 1
        self.size = 0

    def up_heap(self,index):

        while index//2 > 0:
            #if element < parent, swap elements
            if self.list[index].priority < self.list[index//2].priority:
                self.list[index],self.list[index//2] = self.list[index//2],self.list[index]

            index = index//2

    def insert(self,element_obj):

        self.list.append(element_obj)
        self.size += 1

        self.up_heap(self.size) #up_heap when inserting, down_heap when removing. We bubble the worst to the top.

    def down_heap(self,index):

        while index*2 <= self.size:
            minChild_index = self.min_child(index)

            #swap if current element > min child
            if self.list[index].priority > self.list[minChild_index].priority:
                self.list[index],self.list[minChild_index] = self.list[minChild_index],self.list[index]

            index = minChild_index

    def min_child(self,index):
        #if node has one child, return index of that child
        if (index*2)+1 > self.size:
            return index*2
        else: #out of two children, return min child
            if self.list[index*2].priority < self.list[(index*2)+1].priority:
                return index*2
            else:
                return (index*2)+1

    def get_min(self):
        if len(self.list) == 1:
            return "Empty"

        root = self.list[1]

        #move last value of heap to be the root
        self.list[1] = self.list[self.size]
        #then pop last value off
        self.list.pop(-1)
        #size of heap -= 1
        self.size-=1
        #move down the root
        self.down_heap(1) #(value at index 1)
        #return min value of heap
        return root

class MyPriorityQueue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def insertWithPriority_obj(self,priority_obj):
        minHeap.insert(priority_obj)

    def pullHighestPriority_obj(self):
        min = minHeap.get_min()
        return min

    def get_queue(self,returned_val):
        if returned_val == "Empty":
            self.queue = self.queue[:-1] #last value would be "empty"
            return self.queue
        else:
            min_val = self.pullHighestPriority_obj()
            self.queue.append(min_val)
            return self.get_queue(min_val)
minHeap = MyMinHeap()
