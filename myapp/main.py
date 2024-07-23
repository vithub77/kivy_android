from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from os.path import join
from kivy.animation import Animation

from jnius import autoclass
from kivy.core.window import Window

from questions import question

import json
import csv

check = 0


class LoginScreen(Screen):
    src = './back.png'
    agreement = False

    def register_user(self):
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        email = self.ids.email_input.text
        company = self.ids.company.text
        rang = self.ids.rang.text

        if name == 'admin' and phone == '777':
            self.clear_field()
            self.manager.current = 'adminpage'

        if name and phone and email and company and rang and self.agreement:
            store.put(phone, name=name, email=email, phone=phone, company=company, profession=rang)
            self.clear_field()
            self.manager.transition.direction = 'left'
            self.manager.current = 'pregame'

    def checkbox_click(self, instance, value):
        if value:
            self.agreement = True

    def clear_field(self):
        self.agreement = False
        self.ids.checkbox.active = False
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
    resonate = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.list_img = question.keys()
        self.img_generator = self.get_img()
        self.anim_ftb = Animation(opacity=0.8, duration=0.07)
        self.anim_up = Animation(opacity=1, duration=0.1)
        self.q = ''
        self.press()

    def restart_gen(self):
        self.ids.progress_bar.value = 0
        self.resonate = None
        self.q = ''
        self.img_generator = self.get_img()
        self.press()

    def ftb_press(self, resonate):
        self.ids.progress_bar.value += 0.1
        self.resonate = int(resonate)
        self.press()
        # self.anim_ftb.bind(on_complete=self.press)
        # self.anim_ftb.start(self.ids.img)

    def _up_img(self):
        self.anim_up.start(self.ids.img)

    def press(self, animation=None, widget=None):
        global check
        if question.get(self.q) == 0:
            check += 10
        elif self.resonate == 1:
            if question.get(self.q) == 1:
                check += 10
        else:
            if question.get(self.q) == -1:
                check += 10

        try:
            self.q = next(self.img_generator)
            self.ids.q.text = self.q
            # self.ids.img.source = f'./{p}'  # f'/Users/one/Dev/samolet/questions/{p}'
            # self._up_img()
        except:
            self.manager.transition.direction = 'left'
            self.manager.current = 'result'
            self.restart_gen()

    def back_login_page(self):
        global check
        check = 0
        self.restart_gen()
        self.manager.transition.direction = 'right'
        self.manager.current = 'register'

    def get_img(self):
        for i in self.list_img:
            yield f'{i}'


class ResultPage(Screen):
    Builder.load_file('./result.kv')

    def index_(self):
        global check

        self.ids.counts.text = f'Вы резанируете на {check} %'
        if check > 50:
            self.ids.gif.text = 'Получите приз!'
        else:
            self.ids.gif.text = 'Увы, но Вы ничего не получите'

    def back_login_page(self):
        global check
        check = 0
        self.ids.gif.text = ''
        self.manager.transition.direction = 'left'
        self.manager.current = 'register'


class AdminPage(Screen):

    def load_bd(self):
        environment = autoclass('android.os.Environment')
        documents_path = join(environment.getExternalStorageDirectory().getAbsolutePath(), 'Documents', 'users.csv')

        # with open(documents_path, 'w') as file:
        #     file.write("Hello world!!!")

        with open(documents_path, mode='w', newline='') as fc:
            wc = csv.DictWriter(fc, fieldnames=['id', 'name', 'phone', 'email', 'company', 'profession'])
            wc.writeheader()
            with open('./users.json', mode='r') as f:
                data = json.load(f)
                for num, item in enumerate(data.values(), start=1):
                    item['id'] = str(num)
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
        sm.add_widget(ResultPage(name='result'))
        return sm

# Window.size = 1280, 800
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
# Config.set('kivy', 'keyboard_mode', 'systemanddock')
# Config.set('kivy', 'keyboard_mode', 'keyboard_height', '100')

# Config.set('graphics', 'fullscreen', 'auto')
# Window.softinput_mode = 'resize'
store = JsonStore('users.json')
Builder.load_file('./start.kv')
MyApp().run()
