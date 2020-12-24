#kivy modules
from kivymd.app import MDApp,App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.list import ThreeLineListItem
from kivy.uix.floatlayout import FloatLayout

#APIs
import urllib.request
from my_keys import DIRECTIONS_KEY

#files
from hashtables import hashtable
import database
from person_class import PersonHashSymbol
from banners import ProductBanner
from directions import DirectionNode
from mylinkedlist import LinkedList
from backend import MainInfo
from GPS import GPSHelper

#other
import json
from functools import partial


####RUN CODE THE VERY FIRST TIME YOU DOWNLOAD THIS CODE!!###
#hashtable=first_time_run()

##otherwise:##
#hashtable = other_time_run()
#print("HASHTABLE: ",hashtable)

###FRONTEND###

class SignUpScreen(Screen):
    def make_new_user(self):
        email = self.ids.email.text
        username = self.ids.username_new.text
        password = self.ids.password_new.text

        #check if person exists
        result = database.check_already_exists(email,username)

        if result == 1:
            hashtable.insert(PersonHashSymbol(email,username,password))
            #add to database
            database.insert_into_log_table(email, username)
            print("Added to database successfully!")
            MainInfo.person_id = database.get_person_ID(email, username)
            App.get_running_app().root.ids["screen_manager"].current = "home"

        elif result == 2:
            print("Email already taken!")
            print("DATABASES", database.see_all_tables())
            self.ids.email.text = ""
            self.ids.username_new.text=""
            self.ids.password_new.text=""

        elif result == True:
            hashtable.search(PersonHashSymbol(email,username,password))
            print("You already exist!")
            App.get_running_app().root.ids["screen_manager"].current = "home"



class LoginScreen(Screen):
    def authenticate_person(self):
        print(database.see_all_tables())
        email = self.ids.email.text
        username = self.ids.username.text
        given_password = self.ids.password.text

        if hashtable.search(PersonHashSymbol(email,username,given_password)) is True:
            MainInfo.person_id = database.get_person_ID(email, username)
            print("SUCCESS!")
            return True
        else:
            print("Sorry, you don't exist!")
            App.get_running_app().root.ids["screen_manager"].current = "sign_up"
            MainApp.get_running_app().stop()

class HomeScreen(Screen):
    product_name = ObjectProperty(None)

    def on_enter(self):
        self.ids.product_name.text = ""
        MainInfo.p_category = None
        MainInfo.p_name = None

        # reset all button images
        self.ids["supermarket"].background_normal = "images/supermarket_logo.jpg"
        self.ids["electronics_store"].background_normal = "images/electronics_logo.jpg"
        self.ids["pet_store"].background_normal = "images/pets_logo.jpg"
        self.ids["home_goods_store"].background_normal = "images/home_logo.jpg"

    def submit_all(self):
        name = self.ids.product_name.text
        MainInfo.p_name = name

class HistoryScreen(Screen):
    def on_enter(self,*args):
        results = database.show_user_history(MainInfo.person_id)
        for each in results:
            items = ThreeLineListItem(text="%s"%(str(each[0])),secondary_text="Product: %s"%(str(each[1])),tertiary_text="%s"%(str(each[3])))
            self.add_widget(items)

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
            dir_node.instructions = node_instructions

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
        btn.bind(on_press=lambda x:self.change_to_home())
        self.map.add_widget(btn)

        return self.map

    def change_to_home(self):
        App.get_running_app().root.ids["screen_manager"].current = "home"

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
        MainInfo.p_category = the_id

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

    def on_start(self):
        #my_lat,my_lon = GPSHelper.run()
        my_lat = 51.553538
        my_lon = -0.259801
        MainInfo.my_lat = my_lat
        MainInfo.my_lon = my_lon

    def load_shop_screen(self):

        self.finalists = MainInfo.start()

        hex_colours = ["#BEC6C3", "#FCDFCE", "#E0D7D3", "#8A7D80", "#626670"]

        banner_grid = self.root.ids["shop_screen"].ids["ProductGrid"]

        for count in range(5):
            #populate grid in shopscreen

            PBanner = ProductBanner(shop=str(self.finalists[count][0]), product=str(self.finalists[count][1]),
                                    price=str(self.finalists[count][2]),distance=str(self.finalists[count][3]),time=str(self.finalists[count][4]),
                                    colour=hex_colours[count])

            self.buttons.append(Button(text="Choose me!",size_hint=(1,1),pos_hint={"top":.5,"right":1}))

            PBanner.add_widget(self.buttons[count])
            self.buttons[count].bind(on_press=partial(self.load_map_screen, count))

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
        if database.if_is_store_send_id(bLat, bLon, storeName) == False:
            database.insert_to_store(bLat, bLon, storeName)
            storeID = database.get_latest_store_ID()
        else:
            storeID = database.if_is_store_send_id(bLat, bLon, storeName)

        database.insert_to_product(storeID, productName, productPrice)

        ###ADD EVERYTHING TO A DATABASE###
        database.insert_user_table(MainInfo.person_id, storeID, MainInfo.my_lat, MainInfo.my_lon, MainInfo.p_name)

        #switch screens
        self.change_screen("shop_map_screen")

        ######CHECK#####
        print("DATABASES", database.see_all_tables())

MainApp().run()

# update hashtable
#update_hashtable(hashtable)
MainInfo.clear()
#database.reset()