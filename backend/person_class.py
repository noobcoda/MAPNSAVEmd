import googlemaps
from backend.my_keys import KEY
gmaps = googlemaps.Client(key=KEY)


class PersonHashSymbol: #takes in an object, e.g. a set
    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password

    def __hash__(self): #every hash value is different. Makes sure that if one is the same as the other, ignores the latter
        return hash(self.email) ^ hash(self.username) ^ hash(self.password)

    def __eq__(self,other):
        if isinstance(self,other.__class__): #check if both values are of the same type (e.g. both are HashSymbols)
            if self.email == other.email and self.username == other.username and self.password == other.password:
                return True
        else:
            return NotImplemented

class PersonNode:
    def __init__(self,hash):
        self.next = None
        self.hash = hash

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
