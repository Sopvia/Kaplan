import tkinter as tk
import customtkinter as ctk
from createEntry import *
from variables import *
import sqlite3

language = "english"

class root(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="white")
        
        self.title("Address Book")
        self.geometry("600x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.iconbitmap('icon.ico')

        self.font = ctk.CTkFont(family="Georgia", size=12)

        self.overview_frame = overview(master=self)
        self.overview_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


class overview(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="black", width=500, height=500)

        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.newEntry = ctk.CTkButton(self, text="+", height=12, width=12, command=open_createEntry)
        self.newEntry.grid(row=1, column=1, padx=20, pady=20, sticky="ne")

        self.test = ctk.CTkLabel(self, text=testText, text_color="white")
        self.test.grid(row=2, column=1, padx=20, pady=20)

        self.settings = ctk.CTkButton(self, text="Settings", height=12, width=12, command=open_settings)
        self.settings.grid(row=1, column=3, padx=20, pady=20, sticky="ne")


class settings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="black", width=500, height=500)

        self.language = ctk.CTkButton(self, text="De/En", height=12, width=12, command=switchLanguage)
        self.language.grid(row=1, column=1, padx=20, pady=20, sticky="ne")

        self.backButton = ctk.CTkButton(self, text="Close", height=12, width=12, command=self.destroy)
        self.backButton.grid(row=2, column=1)


def open_settings():
    root.settings_frame = settings(master=root)
    root.settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


def switchLanguage():
    global language
    global testText
    global lastnameText

    if language == "german":
        language = "english"
    else:
        language = "german"

    if language == "german":
        testText = "willkommen"
        lastnameText = "Nachname"
    elif language == "english":
        testText = "welcome"
        lastnameText = "Lastname"
    
    update()


def update():
    root.overview_frame.test.configure(text=testText)
    root.createEntry_frame.lastname.configure(text=lastnameText)


root = root()
root.mainloop()