class DirectionNode:
    def __init__(self,sLat,sLng):
        self.sLat = sLat
        self.sLng = sLng
        self.eLat = None #the end location for specific instruction
        self.eLon = None
        self.instructions = ""
        self.number = None
        self.next = None

    def get_rid_of_html_tags(self,instruction):
        #as these tags are bounded by < >, we just need to get rid of everything in between these tags
        instruction = list(instruction)

        in_tag = False
        for char in instruction:
            if char == "<":
                in_tag = True
            if in_tag == False:
                self.instructions += char
            if char == ">":
                in_tag = False

        return self.instructions