from backend.datastructures.mylinkedlist import LinkedList
from backend.person_class import PersonNode,my_hash
import os

class HashTable:

    def __init__(self):
        self.hashList = [LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList(),
                         LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList()] #(10)

    def insert(self,email,username,password):
        key,salt,index = my_hash(email,username,password,os.urandom(32))
        self.hashList[index].append(PersonNode(key,salt)) #adds the hash value to the linkedlist
        return key,salt

    def search(self,email,username,password,salt):
        new_key,salt,search_index = my_hash(email,username,password,salt)
        #now traverse the linked list
        return self.hashList[search_index].find_hash(new_key)