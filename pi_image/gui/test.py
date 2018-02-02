from tkinter import *

# http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
# fullscreen: https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
# button orientation: https://stackoverflow.com/questions/31128780/tkinter-how-to-make-a-button-center-itself
# wizard: https://stackoverflow.com/questions/41332955/creating-a-wizard-in-tkinter
class WelcomeScreen:
    welcome_message = "Welcome to AI Sensor Hub setup! Let's guide you through a few steps to get your hub connected to the server."
    def __init__(self, master):
        self.master = master
        master.title("Setup Wizard")

        self.welcome = Label(master, text = self.welcome_message)
        self.welcome.pack()

        self.next_button = Button(master, text = "Next", command = self.next)
        # self.next_button.pack()
        self.next_button.place(relx=1.0, rely=1.0, anchor=SE)

        # self.back_button = Button(master, text= "Back", command = None)
        # self.back_button['state'] = 'disabled'
        # self.back_button.pack()
        # self.back_button.place(relx=0.0, rely=0.0, anchor=SE)

        self.close_button = Button(master, text = "Close", command = master.quit)


    def next(self):
        print("Call next data")

root = Tk()
root.attributes("-fullscreen", True);
my_gui = WelcomeScreen(root)
root.mainloop()