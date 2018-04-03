#############################################################################
# screens.py
#
# By: Joey-Michael Fallone
#
# This contains class declarations for screen types used in Wizard.py
# as well as some internal operations
#
#############################################################################
from kivy.uix.screenmanager import Screen
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.uix.progressbar import ProgressBar

from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner


class WelcomeScreen(Screen):
    welcome_label_text = "Wireless Sensor Hub Setup"

    def on_exit(self):
        pass # shutdown code will go here eventually 

    def on_next(self):
        pass

class InputScreen(Screen):
    input_label_text = "Please enter Connection String"

    def on_back(self):
        pass

    def on_next(self):
        connect_string = self.ids['input_1']
        f = open(".connection_string.dat", "w+")
        f.write(str(connect_string))
        f.close()

    def activate_cellular(self):
        pass


class SensorScreen(Screen):
    input_label_text = "Please enter Sensor Information"
    sensors = list()

    def on_back(self):
        pass

    def on_next(self):
        pass # create sensor objs

    def save_sensor(self):
        # https://github.com/kivy/kivy/wiki/Styling-a-Spinner-and-SpinnerOption-in-KV
        pass


class ProgressScreen(Screen):
    pb = ProgressBar(max=1000)
    pb.value = 500
    def on_back(self):
        pass

    def on_next(self):
        pass

class TextScreen(Screen):
    text_label_text = "This wizard will allow you to configure numerous sensors and server information for your wireless hub"

    def on_back(self):
        pass

    def on_next(self):
        pass

class FinalScreen(Screen):
    final_label_text = "Finsihed!"

    def on_back(self):
        pass

    def on_exit(self):
        pass

