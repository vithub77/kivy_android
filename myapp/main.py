from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    def register_user(self):
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        email = self.ids.email_input.text

        print(f"Регистрация пользователя: {name}, {phone}, {email}")
        self.clear_field()

    def clear_field(self):
        self.ids.name_input.text = ""
        self.ids.phone_input.text = ""
        self.ids.email_input.text = ""


class Container(FloatLayout):
    pass


class MyApp(App):
    def build(self):
        # return Container()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='register'))
        return sm


Config.set('graphics', 'width', '1800')
Config.set('graphics', 'height', '1000')
# Config.set('graphics', 'fullscreen', 'auto')
MyApp().run()
