class Calculation:
    toBeSortedListPrices = []

    @classmethod
    def getFinalList(cls):
        return cls.toBeSortedListPrices

    @classmethod
    def add_to_be_sorted(cls,aDict,store_obj):
        for product,price in aDict.items():
            cls.toBeSortedListPrices.append((product,float(eval(price)),store_obj))  # so it looks like (('tesco biscuit',1.00),((tesco biscuit 2',1.50))

    #WHOLE MERGESORT ALGORITHM:

    @classmethod
    def merge(cls, left, right):
        sortedList = []

        while len(left) != 0 and len(right) != 0:
            if left[0][1] < right[0][1]:
                sortedList.append(left[0])
                left.remove(left[0])
            else:
                sortedList.append(right[0])
                right.remove(right[0])

        if len(left) == 0:
            sortedList += right

        else:
            sortedList += left

        return sortedList

    @classmethod
    def mergesort(cls,randomList):
        mid = len(randomList) // 2

        if len(randomList) <=1:
            return randomList

        else:

            #does left side of array
            left = Calculation.mergesort(randomList[:mid])

            #does right side of array
            right = Calculation.mergesort(randomList[mid:])

            #merge
            return Calculation.merge(left,right)