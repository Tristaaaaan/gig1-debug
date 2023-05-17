from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime
from kivymd.uix.textfield import MDTextField
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import webbrowser



class ClickableLabel(ButtonBehavior, MDLabel):
    pass


class TextField(MDTextField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_text(self, char):
        self.text += char + '/'

    def keyboard_on_key_up(self, keycode, text):
        if text[1][-1:].isdigit():
            if len(self.text) == 2:
                self.update_text('')
            elif len(self.text) + 1 == 5:
                self.update_text(text[1][-1:])
            else:
                if len(self.text) > 2:
                    self.text += text[1][-1:]
        if text[0] == 'backspace':
            self.do_backspace()


class IntroScreen(Screen):
    pass


class CustomDrop(MDDropdownMenu):
    pass


class VolScreen(Screen):
    pass


class XBoxScreen(Screen):
    pass


class PlaystationScreen(Screen):
    pass


class FortnightScreen(Screen):
    pass


class MaddenScreen(Screen):
    pass


class RejectScreen(Screen):
    pass


class Madden2Screen(Screen):

    def open_link(self):
        webbrowser.open("http://google.com/")


class HomeScreen(Screen):
    birthday_value = None

    def save_birthday_value(self, value):
        self.birthday_value = value

    def get_age(self):
        try:
            date_str = self.birthday_value
            date = datetime.strptime(date_str, f"%m/%d/%Y")
            if date < datetime(1912, 1, 1) or date > datetime.now():
                self.ids.birthday_field.error = True
                self.ids.birthday_field.text = ""
            else:
                self.ids.birthday_field.error = False
                today = datetime.today()
                age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
                app = MDApp.get_running_app()
                return age

        except ValueError:
            self.ids.birthday_field.error = True
            self.ids.birthday_field.text = ""
            print('error')

    def validate(self, dob):
        self.birthday_value = dob
        age = self.get_age()
        if age is not None:
            self.manager.current = "vol"
            app = MDApp.get_running_app()
            app.set_age(age)
        else:
            self.manager.current = "home"


sm = ScreenManager()
sm.add_widget(IntroScreen(name='intro'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(VolScreen(name='vol'))
sm.add_widget(Madden2Screen(name='madden2'))

from kivymd.uix.button import MDRaisedButton


class Vaxlect(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_age = 0
        self.screen = Builder.load_file('screenmanager.kv')
        '''
        all the screens are already added to the screenmanager in the screenmanager.kv file, so
        there's actually no need to create one here and add the screens to it
        '''
        # self.screen = Builder.load_file('graphics.kv')
        # self.screen_manager=ScreenManager()
        # RejectScreen=Screen(name='reject')
        # self.screen_manager.add_widget(RejectScreen)
        # FortnightScreen=Screen(name='fortnight')
        # self.screen_manager.add_widget(FortnightScreen)
        # MaddenScreen=Screen(name='madden')
        # self.screen_manager.add_widget(MaddenScreen)
        # menu items for the main dropown
        self.menu_items = [
            {
                "text": "XBOX",
                "viewclass": "OneLineListItem",  ## here I can whatever widget I want
                "height": dp(56),
                "on_release": lambda x='xbox': self.menu_callback(x, 1),
            },
            {
                "text": "Playstation",
                "viewclass": "OneLineListItem",  ## here I can whatever widget I want
                "height": dp(56),
                "on_release": lambda x="playstation": self.menu_callback(x, 2),
            },

        ]

        # main dropdown
        self.vol_menu = MDDropdownMenu(
            caller=self.screen.screens[2].ids.dropdown_button,
            items=self.menu_items,
            position="center",
            width_mult=4,
        )
        # items for the sub dropdown (to have different sub dropdowns, copy this code)
        self.sub_menu_items = [
            {
                "text": "Madden",
                "viewclass": "OneLineListItem",  ## here I can whatever widget I want
                "height": dp(56),
                "on_release": lambda x='madden': self.sub_menu_callback(x),
            },
            {
                "text": "Fortnight",
                "viewclass": "OneLineListItem",  ## here I can whatever widget I want
                "height": dp(56),
                "on_release": lambda x="fortnight": self.sub_menu_callback(x),
            },

        ]
        # sub dropdown
        self.sub_vol_menu = MDDropdownMenu(
            caller=self.screen.screens[2].ids.dropdown_button,
            items=self.sub_menu_items,
            position="center",
            width_mult=4,
        )

    # sub dropdown callback
    # eventually the code will be self.root.current=text_text item.
    #   the other self.root.current will be eliminated after testing
    def sub_menu_callback(self, text_item):
        print(text_item)
        if text_item == 'madden' and self.user_age < 18:
            self.root.current = 'reject'
        else:
            self.root.current = text_item
        self.sub_vol_menu.dismiss()

    # main dropdown callback
    def menu_callback(self, text_item, num):
        print(text_item)
        if num == 1 or num == 7:
            self.vol_menu.dismiss()
            try:
                self.sub_vol_menu.open()
            except:
                print('menu already opened')
            print('num', num)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        # screen = Builder.load_string(kv.screen_helper)
        # return screen
        return self.screen

    def set_age(self, age):
        self.user_age = age
        next_screens = [screen for screen in self.root.screens if
                        screen.name == 'vol' or screen.name == 'madden' or screen.name == 'madden2' or screen.name == 'reject']
        for screen in next_screens:
            if screen.name == 'reject':
                screen.ids.age.text = f"Sorry as your age is {age} your are ineligbile to play"
            else:
                screen.ids.age.text = f'User age: {age}'

    def reset_data(self):
        home = [screen for screen in self.root.screens if screen.name == "home"][0]
        home.ids.birthday_field.text = ""
        print('hello')

Vaxlect().run()
