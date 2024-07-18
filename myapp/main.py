from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from os.path import join
from jnius import autoclass

import json
import csv


class LoginScreen(Screen):
    src = './back.png'

    def register_user(self):
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        email = self.ids.email_input.text
        company = self.ids.company.text
        rang = self.ids.rang.text

        if name == 'admin' and phone == '666':
            self.clear_field()
            self.manager.current = 'adminpage'

        if name and phone and email and company and rang:
            store.put(phone, name=name, email=email, phone=phone, company=company, profession=rang)
            self.clear_field()
            self.manager.transition.direction = 'left'
            self.manager.current = 'pregame'

    def clear_field(self):
        self.ids.name_input.text = ""
        self.ids.phone_input.text = ""
        self.ids.email_input.text = ""
        self.ids.company.text = ""
        self.ids.rang.text = ""


class Welcome(Screen):
    def back_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'register'

    def go_to_game(self):
        self.manager.transition.direction = 'left'
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
            self.ids.img.source = f'./{p}'  # f'/Users/one/Dev/samolet/questions/{p}'
        except:
            print('game over')

    def get_img(self):
        for i in self.list_img:
            yield f'{i}'


class AdminPage(Screen):

    def load_bd(self):
        environment = autoclass('android.os.Environment')
        documents_path = join(environment.getExternalStorageDirectory().getAbsolutePath(), 'Documents', 'users.csv')

        with open(documents_path, mode='w', newline='') as fc:
            wc = csv.DictWriter(fc, fieldnames=['name', 'phone', 'email', 'company', 'profession'])
            wc.writeheader()
            with open('./users.json', mode='r') as f:
                data = json.load(f)
                for item in data.values():
                    wc.writerow(item)

        self.manager.transition.direction = 'right'
        self.manager.current = 'register'

    def clear_bd(self):
        store.clear()
        self.manager.transition.direction = 'right'
        self.manager.current = 'register'


class MyApp(App):
    def build(self):
        # return LoginScreen()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='register'))
        sm.add_widget(Welcome(name='pregame'))
        sm.add_widget(Game(name='game'))
        sm.add_widget(AdminPage(name='adminpage'))
        return sm


Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
# Config.set('kivy', 'keyboard_mode', 'systemanddock')
# Config.set('kivy', 'keyboard_mode', 'keyboard_height', '100')

# Config.set('graphics', 'fullscreen', 'auto')
store = JsonStore('users.json')
Builder.load_file('./start.kv')
MyApp().run()
