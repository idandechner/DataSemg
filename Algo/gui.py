from tkinter import Tk, Label, Button , Toplevel ,Menu, LEFT, Entry, StringVar,OptionMenu,Message,RIDGE
from tkinter import  Scrollbar, RIGHT, Y,END, Listbox, BOTH, messagebox
import os # operation system package for standard operation system commands
import fnmatch # package for finding specific files
import numpy as np # numeric package for all math operation
import pickle # loading data object library (like mat in matlab)
import sys
import time


class MyFirstGUI:
    def __init__(self, master):
        self.key = 0
        self.color = "#4a4a48"
        self.result = ""
        self.date = ""
        self.muscle = ""
        self.user = ""
        self.master = master
        master.title("SEMG prediction application")

        self.user_label = Label(self.master,foreground="#ebebe3",background=self.color ,pady=10, font="Halvatica 12 bold", text="Enter user name:")
        self.user_label.grid(row=1,columnspan=2)
        self.user_entry = Entry(master)
        self.user_entry.grid(row=2,columnspan=2)

        self.path_label = Label(self.master, foreground="#ffc60b", background=self.color ,pady=10,font="Halvatica  12 bold",text="Enter a full path:")
        self.path_label.grid(row=3,columnspan=2)
        self.path_entry = Entry(master, width=50, background="#feffdb")
        self.path_entry.grid(row=4 , columnspan=2, padx=20, pady=(0,50))

        self.path_label2 = Label(self.master,foreground="#ffc60b", background=self.color ,font="Arial 10 bold",text="Which EX to check:")
        self.path_label2.grid(row=5,column=0)
        self.exercise = StringVar(master)
        self.exercise.set("EX1")  # default value
        w = OptionMenu(master, self.exercise, "EX1", "EX2")
        w.config(background="#feffdb" , font="Arial 8 bold", borderwidth=0)
        w.grid(row=6,column=0, pady=10)

        self.path_label3 = Label(self.master, foreground="#ffc60b",background=self.color,font="Arial 10 bold",text="Scalopa or Trapz:")
        self.path_label3.grid(row=5,column=1)
        self.tar = StringVar(master)
        self.tar.set("Scalopa")  # default value
        w = OptionMenu(master, self.tar, "Scalopa", "Trapz")
        w.config(background="#feffdb", font="Arial 8 bold" ,  borderwidth=0)

        w.grid(row=6,column=1, pady=10)

        self.greet_button = Button(master, borderwidth=0,bg = "#ff8b00", padx=10, pady=10,relief=RIDGE,text="Calculate", font="Arial 10", command=self.calculate)
        self.greet_button.grid(row=9, pady=(100, 10),columnspan=2)

        self.path_label4 = Label(self.master, background=self.color,font="Arial 8 bold",text="All @ rights reserved to Idan Dechner")
        self.path_label4.grid(row=10, columnspan=2)
    def save(self):
        print(self.result)
        print(self.date)
        print(self.muscle)
        print(self.user)
        if self.user != "":
            file_name = '{0}.txt'.format(self.user)
            with open(file_name, 'a') as f:
                data = '{0} {1} {2}\n'.format(self.date, self.result, self.muscle)
                f.write(data)
                messagebox.showinfo("Success", "The movement is saved")
        else:
            messagebox.showerror("Error", "Please enter a user")

    def load(self):
        file_name = '{0}.txt'.format( self.user_entry.get())
        top = Toplevel(background=self.color)
        w, h = top.winfo_screenwidth(), top.winfo_screenheight()
        top.geometry("%dx%d+0+0" % (w-10, h))

        top.title("User measurements")
        Label(top, foreground="#ffc60b",background=self.color, font=("Helvetica", 20, "bold italic"),
              text="Latest measurements").pack()
        try:
            with open(file_name, 'r') as f:
                line = f.readline()
                cnt = 1
                scrollbar = Scrollbar(top)
                scrollbar.pack(side=RIGHT, fill=Y)
                listbox = Listbox(top, width=100,font=("Helvetica", 14, "bold italic"), yscrollcommand=scrollbar.set)

                while line:
                    listbox.insert(END, "Measurement {}: {}".format(cnt, line.strip()))
                    #Label(top, pady=10,padx=10, background=self.color, font=("Helvetica", 14, "bold italic"), text=
                    print("Measurement {}: {}".format(cnt, line.strip()))
                    line = f.readline()
                    cnt += 1

                listbox.pack(side=LEFT, fill=BOTH)
                scrollbar.config(command=listbox.yview)
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            top.destroy()
            messagebox.showerror("Error", "No Measurements found!")
    def about(self):
        print("about")
        if self.key == 0:
            message = "This Application is a Graphical User Interface for the SEMG project.\n" \
                      "It's purpose is to replace the use of command line interface \n" \
                      "default for running python applications.\n" \
                      "All options are self explanatory and easy to interact with.\n"
            top = Toplevel(background=self.color)
            top.title("About SCMG app")
            label = Label(top,foreground="#ffc60b", background=self.color,font=("Helvetica", 14, "bold italic"),text="ABOUT:")
            label.pack()
            msg = Message(top, foreground="#ebebe3", background=self.color,text=message,font="Times 12")
            msg.pack()
            button = Button(top, borderwidth=0,bg = "#ff8b00", padx=10, pady=10,relief=RIDGE,text="Dismiss", font="Arial 10", command=top.destroy)
            button.pack()

    def calculate(self):
        models = []
        folder = self.exercise.get()
        main_folder = "C:\\Users\\yoav\\PycharmProjects\\untitled3\\DataSemg"
        action = ''
        input_file = self.path_entry.get()
        print(input_file)

        tar =  self.tar.get()
        self.muscle = tar
        try:

            if tar == "Scalopa": # value of second input
                print(folder)
                model1 = os.path.join(main_folder, folder, 'scapola_good.pkl')
                model2 = os.path.join(main_folder, folder, 'scapola_bad.pkl')
                with open(model1, "rb") as f:
                    models.append(pickle.load(f))
                with open(model2, "rb") as f:
                    models.append(pickle.load(f))
                action = 'scapola'

            else:
                model1 = os.path.join(main_folder, folder, 'trapz_good.pkl')
                model2 = os.path.join(main_folder, folder, 'trapz_bad.pkl')
                with open(model1, "rb") as f:
                    models.append(pickle.load(f))
                with open(model2, "rb") as f:
                    models.append(pickle.load(f))
                action = 'trapz'

            print("execise = %s, action = %s" % (folder, action))
            data = np.load(input_file) # the text input

            likelihood = []
            for gmm in models:
                likelihood.append(gmm.score(data))

            winner = np.argmax(likelihood)  # winner is the with the maximum likelihood

            if winner == 0:
                print("%s recognized as good with likelihood of %f" % (action, likelihood[int(winner)]))
                self.result = "good"
            else:
                print("%s recognized as bad with likelihood of %f" % (action, likelihood[int(winner)]))
                self.result = "bad"
            self.date = time.asctime( time.localtime(time.time()) )
            self.user = self.user_entry.get()
            messagebox.showinfo("Result" , "The movement is " + self.result)
        except FileNotFoundError:
            messagebox.showerror("Error", "No file in path: " + input_file + " found!")


root = Tk()

my_gui = MyFirstGUI(root)

menubar = Menu(root)
menubar.add_command(label="Save data", command=my_gui.save)
menubar.add_command(label="Load data", command=my_gui.load)
menubar.add_command(label="About", command=my_gui.about)
menubar.add_command(label="Quit", command=root.quit)

# display the menu

root.config(menu=menubar, background="#4a4a48")
root.mainloop()
