import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config

import configparser

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '400')

config = configparser.ConfigParser()
config.read('config.ini')

class IniForm(BoxLayout):

    def __init__(self, **kwargs):
        super(IniForm, self).__init__(**kwargs)
        self.orientation = 'vertical'

    def get_k(self):
        return config.get('Prop', 'k')

    def get_name(self):
        return config.get('Prop', 'name')

    def get_MW(self):
        return config.get('Prop', 'MW')

    def get_Re(self):
        return config.get('Nozzle', 'Re')

    def get_Rt(self):
        return config.get('Nozzle', 'Rt')

    def get_alpha(self):
        return config.get('Nozzle', 'alpha')

    def get_Tc(self):
        return config.get('Chamber', 'Tc')

    def get_Pc(self):
        return config.get('Chamber', 'Pc')

    def write(self, name, k, MW, Re, Rt, alpha, Tc, Pc):
        config.set('Prop', 'name', name.text)
        config.set('Prop', 'k', k.text)
        config.set('Prop', 'MW', MW.text)
        config.set('Nozzle', 'Re', Re.text)
        config.set('Nozzle', 'Rt', Rt.text)
        config.set('Nozzle', 'alpha', alpha.text)
        config.set('Chamber', 'Tc', Tc.text)
        config.set('Chamber', 'Pc', Pc.text)

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            

class TDUApp(App):
    def build(self):
        return IniForm()

    def get_k(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        return config.get('Prop', 'k')

if __name__ == '__main__':
    TDUApp().run()
