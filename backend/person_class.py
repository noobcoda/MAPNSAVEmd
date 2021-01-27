import googlemaps
from backend.my_keys import KEY
import hashlib
gmaps = googlemaps.Client(key=KEY)


def my_hash(email,username,password,salt):
    to_be_password = email+username+password
    new_password = ''.join(list(map(str,map(ord,to_be_password))))
    index_returned = 0
    for x in new_password:
        index_returned += ord(x)
    index_returned = index_returned % 10
    key = hashlib.pbkdf2_hmac(
        'sha256',
        new_password.encode('utf-8'),
        salt,
        100000,
        dklen=128
    )
    return key,salt,index_returned

class PersonNode:
    def __init__(self,key,salt):
        self.salt = salt
        self.key = key
        self.next = None
        self.email = ''
        self.password = ''
        self.username = ''
        self.user = None

    def make_user(self,lat,long):
        self.user = User(lat,long) #composition
        return self.user

    def get_user(self):
        self.user.uLat=None
        self.user.uLong=None
        self.user.productWish=None
        self.user.productType=None
        return self.user

class User:
    def __init__(self,uLat,uLong):
        self.uLat = uLat
        self.uLong = uLong
        self.productWish = None
        self.productType = None

    def getObs(self):
        places_result = gmaps.places_nearby(location="%s,%s" % (self.uLat, self.uLong), radius=500)

        placeDict = {'Latitude': [], 'Longitude': [], 'Radius': [], 'Categories': [], 'Name': []}

        for place in places_result["results"]:
            latitude = place['geometry']['location']['lat']
            longitude = place['geometry']['location']['lng']
            categories = place['types']
            name = place['name']

            placeDict['Latitude'].append(latitude)
            placeDict['Longitude'].append(longitude)
            placeDict['Categories'].append(categories)
            placeDict['Name'].append(name)

        return placeDict
