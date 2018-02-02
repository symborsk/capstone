import tkinter as tk
class Step1(tk.Frame):
    welcome_message = "Welcome to AI Sensor Hub setup! Let's guide you through a few steps to get your hub connected to the server."
    def __init__(self, master):
        self.master = master

        self.welcome = Label(master, text = self.welcome_message)
        self.welcome.pack()

class Step2(tk.Frame):
    def __init__(self, parent):
        print("step2")

class Step3(tk.Frame):
    def __init__(self, parent):
        print("step3")

class Wizard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.current_step = None
        self.steps = [Step1(self), Step2(self), Step3(self)]

        self.button_frame = tk.Frame(self, bd=1, relief="raised")
        self.content_frame = tk.Frame(self)

        self.back_button = tk.Button(self.button_frame, text="<< Back", command=self.back)
        self.next_button = tk.Button(self.button_frame, text="Next >>", command=self.next)
        self.finish_button = tk.Button(self.button_frame, text="Finish", command=self.finish)

        self.button_frame.pack(side="bottom", fill="x")
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.show_step(0)

    def show_step(self, step):

        if self.current_step is not None:
            # remove current step
            current_step = self.steps[self.current_step]
            current_step.pack_forget()

        self.current_step = step

        # new_step = self.steps[step]
        # new_step.pack(fill="both", expand=True)

        if step == 0:
            # first step
            self.back_button.pack_forget()
            self.next_button.pack(side="right")
            self.finish_button.pack_forget()

        elif step == len(self.steps)-1:
            # last step
            self.back_button.pack(side="left")
            self.next_button.pack_forget()
            self.finish_button.pack(side="right")

        else:
            # all other steps
            self.back_button.pack(side="left")
            self.next_button.pack(side="right")
            self.finish_button.pack_forget()

    def back():
        print("go back")

    def next():
        print("next")

    def finish():
        print("finish")

root = tk.Tk()
# root.attributes("-fullscreen", True);
my_gui = Wizard(root)
root.mainloop()