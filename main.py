from tkinter import messagebox
import customtkinter as ctk
from createEntry import *
from variables import *
import sqlite3
from PIL import Image

# ctk.set_default_color_theme("light-pink.json")
# ctk.set_appearance_mode("light")

connection = sqlite3.connect("addressBook.db")
cursor = connection.cursor()

createTable = """CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, category TEXT,lastname TEXT,firstname TEXT,email TEXT,phone INTEGER,address TEXT,date TEXT);"""
cursor.execute(createTable)

getLang = """SELECT language FROM settings;"""
cursor.execute(getLang)
language = cursor.fetchone()

if language == None:
    cursor.execute("INSERT INTO settings (language) VALUES (?)", ("english",))
    connection.commit()

if language[0] == "german":
    var = 1
else:
    var = 0


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
        for widgets in self.winfo_children():
            widgets.destroy()

        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.newEntry = ctk.CTkButton(self, text="+", height=12, width=12, command=open_createEntry)
        self.newEntry.grid(row=1, column=1, padx=(20,10), pady=20, sticky="ne")

        self.settings = ctk.CTkButton(self, text=settingsText[var], height=12, width=12, command=open_settings)
        self.settings.grid(row=1, column=2, padx=(10,20), pady=20, sticky="ne")

        self.test = ctk.CTkLabel(self, text=testText[var], text_color="white")
        self.test.grid(row=1, column=0, padx=20, pady=20)
        
        self.table_frame = table(master=self, height=500, width=500)
        self.table_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")


class table(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        self.grid_columnconfigure((7,8), weight=0)
        self.grid_rowconfigure((1,2,3,4,5,6), weight=1)
        self.grid_rowconfigure(0, weight=0)

        def getOverview(choice):
            for widgets in self.winfo_children():
                widgets.destroy()

            if choice == categorySortAll[0] or choice == categorySortAll[1]:
                overviewAll = """SELECT * FROM contacts;"""
                cursor.execute(overviewAll)
            else:
                if choice == categoryGeneral[0] or choice == categoryGeneral[1]:
                    cat = categoryGeneral[0]
                elif choice == categoryWork[0] or choice == categoryWork[1]:
                    cat = categoryWork[0]
                elif choice == categoryPrivate[0] or choice == categoryPrivate[1]:
                    cat = categoryPrivate[0]

                overviewSort = """SELECT * FROM contacts WHERE category = ?;"""
                cursor.execute(overviewSort, (cat,))

            contacts = cursor.fetchall()

            header = [categoryText[var], lastnameText[var], firstnameText[var], emailText, phoneText[var], addressText[var], dateText[var]]

            c = 0

            for index, value in enumerate(header):
                self.header  = ctk.CTkLabel(self, text= value, text_color="white")
                self.header.grid(row=1, column=0 + c, sticky="w")

                c = c + 1

            labels = {}
            r = 0

            for contact in contacts:
                id = contact[0]
                category = contact[1]
                lastname = contact[2]
                firstname = contact[3]
                email = contact[4]
                phone = contact[5]
                address = contact[6]
                date = contact[7]

                if var == 1:
                    if category == categoryGeneral[0]:
                        category = categoryGeneral[1]
                    elif category == categoryGeneral[0]:
                        category = categoryWork[1]
                    elif category == categoryPrivate[0]:
                        category = categoryPrivate[1]

                labels[contact] = ctk.CTkLabel(self, text= f"{category}")
                labels[contact].grid(row=3 + r, column=0, sticky="w")
                labels[contact] = ctk.CTkLabel(self, text= f"{lastname}")
                labels[contact].grid(row=3 + r, column=1, sticky="w")
                labels[contact] = ctk.CTkLabel(self, text= f"{firstname}")
                labels[contact].grid(row=3 + r, column=2, sticky="w")
                labels[contact] = ctk.CTkLabel(self, text= f"{email}")
                labels[contact].grid(row=3 + r, column=3, sticky="w")
                labels[contact] = ctk.CTkLabel(self, text= f"{phone}")
                labels[contact].grid(row=3 + r, column=4, sticky="w")
                labels[contact] = ctk.CTkLabel(self, text= f"{address}")
                labels[contact].grid(row=3 + r, column=5, sticky="w")
                labels[contact] = ctk.CTkLabel(self, text= f"{date}")
                labels[contact].grid(row=3 + r, column=6, sticky="w")

                # edit = ctk.CTkButton(self, text="E", height=12, width=12)
                # edit.grid(row=3 + r, column=7, padx=10, sticky="w")

                deleteIcon = ctk.CTkImage(light_image=Image.open("icons/delete.png"), dark_image=Image.open("icons/delete.png"), size=(16, 16))

                deleteButton = ctk.CTkButton(self, image=deleteIcon, text="", height=12, width=12, command=lambda: delete(id))
                deleteButton.grid(row=3 + r, column=8, padx=10, sticky="w")

                r = r + 1


            refreshIcon = ctk.CTkImage(light_image=Image.open("icons/retry.png"), dark_image=Image.open("icons/retry.png"), size=(16, 16))

            self.refresh = ctk.CTkButton(self, image=refreshIcon, text="", command=lambda: getOverview(categorySortAll[0]), height=12, width=12)
            self.refresh.grid(row=0, column=7, padx=10, pady=20, sticky="e")

            self.sort = ctk.CTkOptionMenu(self, values=[categorySortAll[var], categoryGeneral[var], categoryWork[var], categoryPrivate[var]], command=getOverview, width=40)
            self.sort.grid(row=0, column=8, padx=10, pady=20, sticky="w")
            self.sort.set(categorySortAll[var])
        
        getOverview(categorySortAll[var])


class settings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="black", width=500, height=500)
        
        self.grid_columnconfigure(1, weight=0)

        self.language = ctk.CTkButton(self, text="De/En", height=12, width=12, command=switchLanguage)
        self.language.grid(row=1, column=1, padx=20, pady=(20,10), sticky="nesw")

        self.mode = ctk.CTkButton(self, text="Dark/Light Mode", height=12, width=12)
        self.mode.grid(row=2, column=1, padx=20, pady=10, sticky="nesw")

        self.theme = ctk.CTkOptionMenu(self, values=["Default", "Pink"], height=12, width=12)
        self.theme.grid(row=3, column=1, padx=20, pady=10, sticky="nesw")

        self.backButton = ctk.CTkButton(self, text=closeText[var], height=12, width=12, command=self.destroy)
        self.backButton.grid(row=4, column=1, padx=20, pady=(10,20))


def open_settings():
    root.settings_frame = settings(master=root)
    root.settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

def open_restart():
    restart_win = ctk.CTkToplevel()
    restart_win.title("Info")
    restart_win.geometry("200x100")
    restart_win.attributes('-topmost', 'true')
    restart_win.focus()
    restart_win.grab_set() 

    restart_win.info = ctk.CTkLabel(restart_win, text=restartInfo[var], height=12, width=12)
    restart_win.info.grid(row=0, column=1, padx=20, pady=20, sticky="nesw")

    restart_win.ok = ctk.CTkButton(restart_win, text="Ok", height=12, width=12, command=root.destroy)
    restart_win.ok.grid(row=1, column=1, padx=20, pady=20, sticky="nesw")


def switchLanguage():
    if language[0] == "german":
        lang = "english"
    else:
        lang = "german"

    cursor.execute("UPDATE settings SET language = ?", (lang,))
    connection.commit()

    open_restart()


def delete(x):
    cursor.execute("DELETE FROM contacts WHERE id= ?", (x,))
    connection.commit()    

root = root()
root.mainloop()