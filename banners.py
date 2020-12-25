from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
import kivy.utils
from kivy.uix.image import Image

class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

class ProductBanner(GridLayout):
    rows = 1

    def __init__(self,**kwargs):
        super(ProductBanner,self).__init__()

        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex(str(kwargs['colour']))))
            self.rect = Rectangle(size=self.size,pos=self.pos)

        self.bind(pos=self.update_rect,size=self.update_rect)

        #leftest
        top = FloatLayout()
        top_text = WrappedLabel(text=kwargs['product'],font_size=15,size_hint=(1,1),pos_hint={"top":1}) #width,height for size
        top.add_widget(top_text)
        self.add_widget(top)

        #left
        left = FloatLayout()
        left_img = Image(source="images/store_logo.png",size_hint=(1,0.8),pos_hint={"top":1,"right":1})
        left_text = WrappedLabel(text=kwargs['shop'],size_hint=(1,.2),pos_hint={"top":.2,"right":1})
        left.add_widget(left_img)
        left.add_widget(left_text)
        self.add_widget(left)

        #mid
        mid = FloatLayout()
        mid_text1 = WrappedLabel(text="Avg Dist: "+str(kwargs['distance'])+'m',size_hint=(1,0.8),pos_hint={"top":1,"right":1})
        mid_text2 = WrappedLabel(text="Avg Walk Time: "+str(kwargs['time'])+"mins",size_hint=(1,.2),pos_hint={"top":.2,"right":1})
        mid.add_widget(mid_text1)
        mid.add_widget(mid_text2)
        self.add_widget(mid)

        #right
        right = FloatLayout()
        right_img = Image(source="images/pound.png",size_hint=(1,0.8),pos_hint={"top":1,"right":1})
        right_text = WrappedLabel(text="Price: £"+str(kwargs['price']),size_hint=(1,.2),pos_hint={"top":.2,"right":1})
        right.add_widget(right_img)
        right.add_widget(right_text)
        self.add_widget(right)

        self.add_widget(kwargs['my_button'])

    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size= self.size
