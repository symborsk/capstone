#############################################################################
# Wizard.py
#
# By: Joey-Michael Fallone
#
# This is the main file for the setup wizard on the Raspberry Pi.
#
# ie run "python3 Wizard.py" to run the GUI 
#
# This is a GUI wizard which a user can run to interface with all types of 
# sensors once they have been physically interfaced to the sensor hub. 
# 
# The goal of this is to create a completely "generic" sensor driver that 
# will allow (in conjunction with our hardware converters) interfacing 
# with virtually any existing server. 
#
# This entire module should be compiled to C using Cython to 
# obscure source code before deploying to customers. 
#############################################################################

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens import *

presentation = Builder.load_file("wizard.kv")


class WizardApp(App):

	def build(self):
		return presentation

if __name__ == "__main__":
	WizardApp().run()
