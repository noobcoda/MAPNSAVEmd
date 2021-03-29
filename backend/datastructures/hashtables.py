from backend.datastructures.mylinkedlist import LinkedList
from backend.person_class import my_hash,PersonNode
import os

class HashTable:

    def __init__(self):
        self.hashList = [LinkedList()]*10 #(10)

    def insert(self,email,username,password):
        key,salt,index = my_hash(email,username,password,os.urandom(32))
        person = PersonNode(key,salt)
        self.hashList[index].append(person)
        return key,salt,person

    def search(self,email,username,password,salt):
        new_key,salt,search_index = my_hash(email,username,password,salt)
        #now traverse the linked list of person keys
        success,found_person = self.hashList[search_index].find(new_key)
        if success:
            return found_person
        return False