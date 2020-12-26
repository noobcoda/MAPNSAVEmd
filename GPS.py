from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

class P(FloatLayout):
    pass

class GpsHelper():
    count = 0
    has_centered_map = False

    def run(self):
        #on android, we must request some permissions

        if platform == 'android':
            from android.permissions import Permission,request_permissions
            def callback(permission,results):
                if all([res for res in results]):
                    print("All permissions given.")
                else:
                    print("Not all permissions given.")

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION],callback)

        #Configure GPS - first check if on mobile
        if platform == "android" or platform =="ios":
            from plyer import gps
            gps.configure(on_location=self.on_gps_location,
                          on_status=self.on_auth_status) #whenever new location is received
            gps.start(minTime=100000000000000000000,minDistance=10000000000000000) #I'm only getting new location after a very long period of time, as there's no need to keep calling this function. We mainly just want the start location.


    def on_gps_location(self,*args,**kwargs): #kwargs gets you all the key stuff -- lat and long
        self.count += 1
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']

        my_lat = 51.553538
        my_lon = -0.259801

        print("GPS POS:",my_lat,my_lon)
        if self.count == 1: #if this is the first time
            return my_lat,my_lon

    def on_auth_status(self,general_status,status_message):
        if general_status == "provider-enabled":
            pass
        else:
            self.show_popup()

    def show_popup(self):
        show = P()
        popupWindow = Popup(title="GPS error", content=show, size_hint=(None, None), size=(400, 400))
        popupWindow.open()

GPSHelper = GpsHelper()