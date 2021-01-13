from backend.datastructures.hashtables import HashTable
import pickle

class Utility:
    def save_hash_table(self,obj,filename):
        target_file = open(filename,'wb')
        pickle.dump(obj,target_file)

    def load_hashtable(self,filename,firstTime):
        if firstTime: #if it's the first time the app's ever loaded, make a new instance of hashtable
            hashTable = HashTable()
        else:
            loadfile = open(filename,"rb")
            hashTable = pickle.load(loadfile)

        return hashTable

utility = Utility()