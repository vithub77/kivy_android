from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    src = '/Users/one/Dev/samolet/back.png'

    def register_user(self):
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        email = self.ids.email_input.text

        print(f"Регистрация пользователя: {name}, {phone}, {email}")
        self.clear_field()

        self.manager.current = 'pregame'

    def clear_field(self):
        self.ids.name_input.text = ""
        self.ids.phone_input.text = ""
        self.ids.email_input.text = ""


class Welcome(Screen):
    def back_login(self):
        self.manager.current = 'register'

    def go_to_game(self):
        self.manager.current = 'game'


class Game(Screen):
    Builder.load_file('./game.kv')
    positive = 0
    negative = 0

    def __init__(self, **kw):
        self.list_img = ['1.png', '2.png', '3.png']
        super().__init__(**kw)
        self.img_generator = self.get_img()
        self.press()

    def press(self, resonate=None):
        if resonate:
            print('resonate!!!!')
        else:
            print('Not resonate!')
        try:
            p = next(self.img_generator)
            self.ids.img.source = f'/Users/one/Dev/samolet/questions/{p}'
        except:
            print('game over')

    def get_img(self):
        for i in self.list_img:
            yield f'{i}'


class MyApp(App):
    def build(self):
        # return LoginScreen()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='register'))
        sm.add_widget(Welcome(name='pregame'))
        sm.add_widget(Game(name='game'))
        return sm


Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
# Config.set('kivy', 'keyboard_mode', 'systemanddock')
# Config.set('kivy', 'keyboard_mode', 'keyboard_height', '100')

# Config.set('graphics', 'fullscreen', 'auto')
Builder.load_file('./start.kv')
MyApp().run()
