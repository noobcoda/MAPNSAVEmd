class DirectionNode:
    def __init__(self,sLat,sLng):
        self.sLat = sLat
        self.sLng = sLng
        self.eLat = None #the end location for specific instruction
        self.eLon = None
        self.instructions = None
        self.number = None
        self.next = None