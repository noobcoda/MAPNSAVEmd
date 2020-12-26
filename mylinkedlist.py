class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None

    def append(self,node):
        if self.head == None:
            self.head = node
            return

        current_node = self.head

        while current_node.next != None:
            current_node = current_node.next  # this just traverses

        # at the end of the linked list, we make a new node:
        current_node.next = node
        self.size += 1

    def delete_node(self,node):
        current_node = self.head

        if current_node == node: #if the data we want to delete is the head, we have to shift the head
            current_node = current_node.next
        else:
            while current_node.next != None:
                if current_node.next == node:
                    current_node.next = current_node.next.next

    def get_size(self):
        return self.size

    def find_hash(self,value):
        if self.head == None:
            return False
        else:
            current_node = self.head
            if current_node.hash == value:
                return True

            while current_node.next != None:
                if current_node.hash == value:
                    return True
                current_node = current_node.next
            return False