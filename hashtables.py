from mylinkedlist import LinkedList
from person_class import PersonNode

import pickle #without this, hashtable gets instantiated whenever app restarts, and we lose all previous data

class HashTable:

    def __init__(self):
        self.hashList = [LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList(),LinkedList()] #(10)

    def insert(self,obj):
        hash_result = hash(obj)
        index = self.get_index_pos(hash_result)
        person = PersonNode(hash_result)
        self.hashList[index].append(person) #adds the hash value to the linkedlist
        print(self.hashList[index])

    def get_index_pos(self,hash_result):
        return hash_result % 10

    def search(self,search_obj):
        new_hash_result = hash(search_obj)
        search_index = self.get_index_pos(new_hash_result)
        #now traverse the linked list
        return self.hashList[search_index].find_hash(new_hash_result)

'''
def first_time_run():
    new_hashtable = HashTable()
    pickle_out = open("hashtable.pickle", "wb")
    pickle.dump(new_hashtable, pickle_out)
    pickle_out.close()
    return new_hashtable

def other_time_run():
    pickle_in = open("hashtable.pickle", "rb")
    hashtable = pickle.load(pickle_in)
    return hashtable

def update_hashtable(hashtable):
    pickle_out = open("hashtable.pickle", "wb")
    pickle.dump(hashtable, pickle_out)
    pickle_out.close()
'''

hashtable = HashTable()