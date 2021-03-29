#kivy modules
from kivymd.app import MDApp,App
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.list import ThreeLineListItem

#APIs
import urllib.request
from backend.GPSanddirections.secret_keys import DIRECTIONS_KEY
#for safety reasons, this file is not uploaded on github.

#other
import json
from functools import partial
import os.path

#files
from backend.utility import utility
if os.path.isfile("hashtablefile"):
    hashtable = utility.load_hashtable("hashtablefile",False)
else:
    hashtable = utility.load_hashtable("hashtablefile",True)

from backend.databases import database
from frontend.banners import ProductBanner
from backend.GPSanddirections.directions import DirectionNode
from backend.GPSanddirections.GPS import GPSHelper
from backend.datastructures.mylinkedlist import LinkedList
from backend.backend import MainInfo

###FRONTEND###

class SignUpScreen(Screen):
    def make_new_user(self):
        email = self.ids.email.text
        username = self.ids.username_new.text
        password = self.ids.password_new.text

        if email == "" or username=="" or password == "":
            popup = MDDialog(title="Error!", text="Please provide valid inputs.")
            popup.open()

        #check if email is in correct format
        elif email != "" and self.check_email(email) == True:

            #check if person exists
            result = database.check_already_exists(email, username)

            if result == 1:
                hash_key,salt,person = hashtable.insert(email,username,password)
                utility.save_hash_table(hashtable,"hashtablefile")
                #make a new user
                user = person.make_user(MainInfo.my_lat,MainInfo.my_lon)
                MainInfo.user = user
                #add to database
                database.insert_into_log_table(email,username,salt)
                MainInfo.person_id = database.get_person_ID(email,username)
                App.get_running_app().root.ids["screen_manager"].current = "login"

            elif result == 2:
                popup = MDDialog(title="Error!", text="Sorry, email is taken!")
                popup.open()

            elif result == True:
                App.get_running_app().root.ids["screen_manager"].current = "login"

    def check_email(self,email):
        if '@' not in email and '.com' or '@' not in email and '.co.uk' not in email:
            popup = MDDialog(title="Error!",text="Sorry, email is not valid!")
            popup.open()
            return False
        return True

class LoginScreen(Screen):

    def authenticate_person(self):
        email = self.ids.email.text
        username = self.ids.username.text
        given_password = self.ids.password.text

        #check if person is in database
        database.check_already_exists(email,username)
        database_salt = database.get_salt(email)

        person = hashtable.search(email,username,given_password,database_salt)
        if person != False:
            if person.user == None:
                person.make_user(MainInfo.my_lat,MainInfo.my_lon)
            MainInfo.user = person.user
            MainInfo.person_id = database.get_person_ID(email,username)
            return True
        elif person==False:
            popup = MDDialog(title="Error!",text="Sorry, you don't exist!")
            popup.open()
            App.get_running_app().root.ids["screen_manager"].current = "sign_up"

class HomeScreen(Screen):
    product_name = ObjectProperty(None)

    def on_enter(self):
        self.ids.product_name.text = ""
        MainInfo.finalists = []

        # reset all button images
        self.ids["supermarket"].background_normal = "images/supermarket_logo.jpg"
        self.ids["electronics_store"].background_normal = "images/electronics_logo.jpg"
        self.ids["pet_store"].background_normal = "images/pets_logo.jpg"
        self.ids["home_goods_store"].background_normal = "images/home_logo.jpg"

    def submit_all(self):
        name = self.ids.product_name.text
        MainInfo.user.productWish = name

class HistoryScreen(Screen):
    def on_enter(self,*args):
        self.ids["info_list"].clear_widgets()
        results = database.show_user_history(MainInfo.person_id)
        searchCount = database.count_search_history(MainInfo.person_id)

        for each in results:
            item = ThreeLineListItem(text="%s" % (str(each[0])), secondary_text="Product: %s, Total number of products: %s" % (str(each[2]),str(searchCount)),
                                     tertiary_text="%s" % (str(each[1])))
            self.ids["info_list"].add_widget(item)

class ShopScreen(Screen):
    pass

class ShopMapScreen(Screen):
    def on_enter(self, *args):

        #ACCESSING DATABASE
        loci = database.get_all_locations(MainInfo.person_id)

        startx = float(loci[0][0])
        starty = float(loci[0][1])
        endx = float(loci[0][2])
        endy = float(loci[0][3])

        self.map = MapView(zoom=11,lat=startx,lon=starty)
        self.add_widget(self.map)

        self.get_directions_using_api(startx,starty,endx,endy)
        self.draw()

    def get_directions_using_api(self,startx,starty,endx,endy):

        end_point = "https://maps.googleapis.com/maps/api/directions/json?"

        userLocation = '%s,%s' % (startx,starty)

        endLocation = '%s,%s' % (endx,endy)

        nav_request = 'origin={}&destination={}&mode=walking&key={}'.format(userLocation, endLocation, DIRECTIONS_KEY)
        request = end_point + nav_request
        response = urllib.request.urlopen(request).read()  # response as a string
        directions = json.loads(response)

        ##upload to linked list

        self.directions_linkedList = LinkedList()

        # going through directions

        number = 1
        for step in directions['routes'][0]['legs'][0]['steps']:
            node_from_lat = step['start_location']['lat']
            node_from_lon = step['start_location']['lng']
            node_to_lat = step['end_location']['lat']
            node_to_lon = step['end_location']['lng']
            node_instructions = step['html_instructions']

            dir_node = DirectionNode(node_from_lat, node_from_lon)
            dir_node.eLat = node_to_lat
            dir_node.eLon = node_to_lon
            dir_node.instructions = dir_node.get_rid_of_html_tags(node_instructions)

            dir_node.number = number
            number += 1

            self.directions_linkedList.append(dir_node)

    def draw(self):
        current_node = self.directions_linkedList.head
        count = 0
        markers = []
        while current_node.next != None:
            count +=1
            marker = MapMarker(lat=current_node.sLat,lon=current_node.sLng,source="images/marker.png")
            marker.get_node(current_node)
            markers.append(marker)
            current_node = current_node.next

        for m in markers:
            self.map.add_widget(m)

        btn = MDRoundFlatIconButton(text="Go to Home") #next time change to sign out
        btn.bind(on_press=lambda x:self.change_screen("home"))
        self.map.add_widget(btn)

        return self.map

    def change_screen(self,name):
        App.get_running_app().root.ids["screen_manager"].current = name


class MapMarker(MapMarkerPopup):
    def get_node(self,current_node):
        self.current_node = current_node

    def on_release(self):
        self.popup = MDDialog(title="%d"%(self.current_node.number),text="%s"%(self.current_node.instructions))
        self.popup.open()

class MyButtons(Button):
    count = 0
    buttons = []

    def inside_count(self, img1, img2):
        self.count += 1
        if self.count % 2 == 0:
            self.hold_down(img1)
        else:
            self.hold_down(img2)

    def overwrite_id(self, the_id):
        MainInfo.user.productType = the_id

    def hold_down(self, image):
        self.background_normal = image


class MainApp(MDApp):

    buttons = []
    finalists = []

    def build(self):
        self.GUI = Builder.load_file("main.kv")
        return self.GUI

    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def change_to_home(self,*args):
        self.change_screen("home")

    def on_start(self):
        #MainInfo.my_lat,MainInfo.my_lon = GPSHelper.run()
        MainInfo.my_lat = 51.553538
        MainInfo.my_lon = -0.259801

    def load_shop_screen(self):

        ##clearing all the grids before
        banner_grid = self.root.ids["shop_screen"].ids["ProductGrid"]
        banner_grid.clear_widgets()

        self.finalists = MainInfo.start()

        #if self.finalists is empty:
        if self.finalists == False:
            popup = Popup(title="Error!",content=Label(text="We couldn't find any results near you :("),size_hint=[.5,.3])
            popup.bind(on_dismiss=self.change_to_home)
            popup.open()
            return False
        elif self.finalists == 3:
            popup = Popup(title="Error!",content=Label(text="Empty field. Please retype."),size_hint=[.5,.3])
            popup.bind(on_dismiss=self.change_to_home)
            popup.open()
            return False

        hex_colours = ["#BEC6C3", "#FCDFCE", "#E0D7D3", "#8A7D80", "#626670"]

        for count in range(len(self.finalists)):
            btn = Button(text="Choose me!", size_hint=(1, 1), pos_hint={"top": .5, "right": 1})
            btn.bind(on_press=partial(self.load_map_screen, count))

            #populate grid in shopscreen

            PBanner = ProductBanner(shop=str(self.finalists[count][0]), product=str(self.finalists[count][1]),
                                    price=str(self.finalists[count][2]),distance=str(self.finalists[count][3]),time=str(self.finalists[count][4]),
                                    colour=hex_colours[count],my_button=btn)

            banner_grid.add_widget(PBanner)

        self.change_screen("shop_screen")

    def load_map_screen(self,index,instance):
        #now update the databases

        bLat = self.finalists[index][7]
        bLon = self.finalists[index][8]
        storeName = self.finalists[index][0]

        productName = self.finalists[index][1]
        productPrice = self.finalists[index][2]

        #check if store already exists in database (we don't want any repeats)

        if database.is_store(bLat, bLon, storeName) == False:
            database.insert_to_store(bLat, bLon, storeName)

        storeID = database.get_store_ID(bLat, bLon, storeName)

        database.insert_to_product(storeID, productName, productPrice)

        ###ADD EVERYTHING TO A DATABASE###
        database.insert_user_table(MainInfo.person_id, storeID, MainInfo.my_lat, MainInfo.my_lon, MainInfo.user.productWish)

        #switch screens
        self.change_screen("shop_map_screen")

MainInfo.clear()
MainApp().run()