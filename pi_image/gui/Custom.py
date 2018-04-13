#############################################################################
# Custom.py
#
# By: Joey-Michael Fallone
#
# Custom dropdown class for the GUI
# 
#
#############################################################################

from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
presentation = Builder.load_file("custom.kv")

# https://kivy.org/docs/api-kivy.uix.dropdown.html
class CustomDropDown(DropDown):
    pass

dropdown = CustomDropDown()
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))