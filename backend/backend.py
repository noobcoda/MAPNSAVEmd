#####BACKEND#####
from backend.datastructures.priorityqueue import MyPriorityQueue
from backend.obstacles_class import Store, Product
from backend.calculations_class import Calculation
from backend.person_class import User

from math import radians, cos, sin, sqrt, atan2

class MainInfo:
    def __init__(self):
        self.my_lat = None
        self.my_lon = None
        self.p_category = None
        self.p_name = None
        self.finalists = []
        self.person_id = None

    def start(self):
        if self.person_id is not None and self.my_lat is not None and self.my_lon is not None and self.p_category is not None and self.p_name is not None:
            self.main_body()
            return self.finalists
        else:
            print("Failed to run any operations.")
            return False

    def main_body(self):
        # initialise user
        user = User(self.my_lat, self.my_lon)
        user.productType = self.p_category
        user.productWish = self.p_name

        self.get_info_near_you(user)

        # now that we have the finished priceandproductdict, we must collect the list & begin mergesort

        top = self.find_top_stores()

        # getting top five to show onto screen
        queue = MyPriorityQueue()

        possible_options = self.get_top_five_options(self.my_lat, self.my_lon, top, queue)

        return possible_options

    def journey(self, startLat, startLon, endLat, endLon):
        startLat = radians(startLat)
        startLon = radians(startLon)
        endLat = radians(endLat)
        endLon = radians(endLon)

        # using formula (Haversine)
        diff_lat = endLat - startLat
        diff_lon = endLon - startLon

        calc_var = sin(diff_lat / 2) ** 2 + cos(startLat) * cos(endLat) * sin(diff_lon / 2) ** 2
        calc_two = 2 * atan2(sqrt(calc_var), sqrt(1 - calc_var))

        # radius of earth: (km)
        r = 6371

        ans_m = r * calc_two * 1000

        return ans_m

    def calculate_priority(self, price, distance): #distance should not be weighted as much as price, as made sure all stores are in a 500m radius anyway
        return price + distance/1000

    def get_info_near_you(self, user):
        priceAndProductDict = {}
        from_shopList = []

        # getting things near user
        places = user.getObs()

        # making instances of obstacles
        obstacle_index = 0
        success_count = 0
        for index in range(len(places['Latitude'])):  # remember that categories is a list
            obstacle_index += 1

            # whichever stores has the same category will go to store class and insert into database
            if user.productType in places['Categories'][index]:
                success_count += 1  # id of each store
                store = Store(places['Latitude'][index], places['Longitude'][index], places['Categories'][index],
                              places['Name'][index])

                new_priceAndProductDict, new_from_shopList = store.get_product_price(user.productWish)  # == shop name, not product name
                priceAndProductDict.update(new_priceAndProductDict)
                from_shopList += new_from_shopList
                Calculation.toBeSortedListPrices = []
                Calculation.add_to_be_sorted(priceAndProductDict, store)

            elif obstacle_index > len(places['Latitude']) and success_count == 0:
                print("Unable to find any products near you.")
                return False


    def find_top_stores(self):
        toBeSortedList = Calculation.getFinalList()  # (('tesco biscuit',1.00,<store obj>))
        top = Calculation.mergesort(toBeSortedList)  # [('innocent apple juice',0.12,<store obj>)]

        return top

    def get_top_five_options(self, uLat, uLong, top, queue):
        possible_options = []  # contains all possible buttons

        for rank in range(len(top)):
            store_ins = top[rank][2]
            store_ins.dist = self.journey(uLat, uLong, store_ins.lat, store_ins.long)
            store_ins.walk_time = round(store_ins.dist / 100, 3)
            product_bought = top[rank][0]
            product_price = top[rank][1]
            priority = self.calculate_priority(product_price, store_ins.dist)
            product = Product(store_ins.lat, store_ins.long, store_ins.category, store_ins.store_name, priority,
                              product_bought, product_price, store_ins.walk_time, store_ins.dist)

            queue.insertWithPriority_obj(product)

        options = queue.get_queue(0)

        # now getting all the stores
        for p in options:
            possible_options.append(
                [p.store_name, p.product_name, p.price, round(p.dist / 3), p.walk_time, uLat, uLong, float(p.lat),
                 float(p.long)])
            # basically contains store name, product name, product price, distance, amount to walk time

        # now get top five possible options
        self.finalists = possible_options[:5]

    def clear(self):
        self.my_lat = None
        self.my_lon = None
        self.p_category = None
        self.p_name = None
        self.finalists = []
        self.person_id = None

MainInfo = MainInfo()