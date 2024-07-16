import tkinter as tk
import customtkinter as ctk
from createEntry import *
from variables import *
import sqlite3

# ctk.set_default_color_theme("light-pink.json")
# ctk.set_appearance_mode("light")

connection = sqlite3.connect("addressBook.db")
cursor = connection.cursor()

createTable = """CREATE TABLE IF NOT EXISTS contacts (category TEXT,lastname TEXT,firstname TEXT,email TEXT,phone INTEGER,address TEXT,date TEXT);"""
cursor.execute(createTable)

language = "english"

class root(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="white")
        
        self.title("Kaplan - Your Address Book")
        self.geometry("900x600")
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
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.newEntry = ctk.CTkButton(self, text="+", height=12, width=12, command=open_createEntry)
        self.newEntry.grid(row=1, column=1, padx=(20,10), pady=20, sticky="ne")

        self.settings = ctk.CTkButton(self, text="Settings", height=12, width=12, command=open_settings)
        self.settings.grid(row=1, column=2, padx=(10,20), pady=20, sticky="ne")

        self.test = ctk.CTkLabel(self, text=testText, text_color="white")
        self.test.grid(row=1, column=0, padx=20, pady=20)

        
        self.table_frame = table(master=self, height=500, width=500)
        self.table_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")


class table(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()

        self.header  = ctk.CTkLabel(self, text= categoryText + "\t\t" + lastnameText + "\t\t" + firstnameText + "\t\t" + emailText + "\t\t" + phoneText + "\t\t" + addressText + "\t\t" + dateText, text_color="white")
        self.header.grid(row=0, column=0, sticky="nsew")

        # self.table = ctk.CTkTextbox(self, height=400, wrap="none")
        # self.table.insert("0.0", categoryText + "\t\t" + lastnameText + "\t\t" + firstnameText + "\t\t" + emailText + "\t\t" + phoneText + "\t\t" + addressText + "\t\t" + dateText + "\n")

        labels = {}
        r = 0

        for contact in contacts:
            category = contact[0]
            lastname = contact[1]
            firstname = contact[2]
            email = contact[3]
            phone = contact[4]
            address = contact[5]
            date = contact[6]
            labels[contact] = ctk.CTkLabel(self, text= f"{category}\t\t{lastname}\t\t{firstname}\t\t{email}\t\t{phone}\t\t{address}\t\t{date}\n")
            labels[contact].grid(row=3 + r, column=0)

            r = r + 1
            # self.table.insert("0.0", f"{category}\t\t{lastname}\t\t{firstname}\t\t{email}\t\t{phone}\t\t{address}\t\t{date}\n")

        # self.table.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        # self.table.configure(state="disabled")

        connection.close()

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