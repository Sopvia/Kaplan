from tkinter import messagebox
import customtkinter as ctk
from init import *
from createEntry import *
from variables import *
import sqlite3
from PIL import Image

connection = sqlite3.connect("addressBook.db")
cursor = connection.cursor()

getLang = """SELECT language FROM settings;"""
cursor.execute(getLang)
language = cursor.fetchone()

if language[0] == None:
    cursor.execute("INSERT INTO settings (language) VALUES (?)", ("english",))
    connection.commit()

if language[0] == "german":
    var = 1
else:
    var = 0

getMode = """SELECT mode FROM settings;"""
cursor.execute(getMode)
mode = cursor.fetchone()

if mode[0] == "dark":
    ctk.set_appearance_mode("dark")
else:
    ctk.set_appearance_mode("light")

getTheme = """SELECT theme FROM settings;"""
cursor.execute(getTheme)
theme = cursor.fetchone()

if theme[0] == "blue":
    ctk.set_default_color_theme("blue.json")
else:
    ctk.set_default_color_theme("light-pink.json")


class root(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kaplan - Your Address Book")
        self.geometry("800x600") 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.iconbitmap('icons/address_book.ico')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.overview_frame = overview(master=self)
        self.overview_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


class overview(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color=["#ffecf2", "#23292c"], width=500, height=500)
        for widgets in self.winfo_children():
            widgets.destroy()

        getName = """SELECT name FROM settings;"""
        cursor.execute(getName)
        username = cursor.fetchone()

        self.grid_rowconfigure((1,3), weight=3)
        self.grid_rowconfigure((2,3), weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)

        self.intro = ctk.CTkLabel(self, text= f"{introText[var]}!")
        self.intro.grid(row=1, column=1, padx=(20,10), pady=(20, 10), sticky="nesw")

        if username[0]:
            self.intro.configure(text= f"{introText[var]}, {username[0]}!")

        self.table_frame = table(master=self, height=500, width=500)
        self.table_frame.grid(row=1, rowspan=3, column=2, padx=(10,20), pady=20, sticky="nesw")

        self.newEntry = ctk.CTkButton(self, text="+", height=12, command=open_createEntry)
        self.newEntry.grid(row=2, column=1, padx=(20,10), pady=(10,10), ipadx=10, ipady=2, sticky="new")

        self.settings = ctk.CTkButton(self, text=settingsText[var], height=12, command=open_settings)
        self.settings.grid(row=3, column=1, padx=(20,10), pady=(10,20), ipadx=10, ipady=2, sticky="new")


class table(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add(categorySortAll[var])
        self.add(categoryGeneral[var])
        self.add(categoryWork[var])
        self.add(categoryPrivate[var])

        self.tab(categorySortAll[var]).grid_columnconfigure(0, weight=2)
        self.tab(categorySortAll[var]).grid_rowconfigure(0, weight=2)

        self.tab(categoryGeneral[var]).grid_columnconfigure(0, weight=2)
        self.tab(categoryGeneral[var]).grid_rowconfigure(0, weight=2)
        
        self.tab(categoryWork[var]).grid_columnconfigure(0, weight=2)
        self.tab(categoryWork[var]).grid_rowconfigure(0, weight=2)

        self.tab(categoryPrivate[var]).grid_columnconfigure(0, weight=2)
        self.tab(categoryPrivate[var]).grid_rowconfigure(0, weight=2)

        self.tableAll = createTableAll(master=self.tab(categorySortAll[var]))
        self.tableAll.grid(row=0, column=0, padx=20, pady=20, sticky="nesw")

        self.tableGeneral = createTableGeneral(master=self.tab(categoryGeneral[var]))
        self.tableGeneral.grid(row=0, column=0, padx=20, pady=20, sticky="nesw")

        self.tableWork = createTableWork(master=self.tab(categoryWork[var]))
        self.tableWork.grid(row=0, column=0, padx=20, pady=20, sticky="nesw")

        self.tablePrivate = createTablePrivate(master=self.tab(categoryPrivate[var]))
        self.tablePrivate.grid(row=0, column=0, padx=20, pady=20, sticky="nesw")

        # self.order = ctk.CTkOptionMenu(self, values=[orderDateDESC[var], orderDateASC[var], orderLastnameDESC[var], orderLastnameASC[var]], command=getOverview, width=40)
        # self.order.grid(row=0, column=10, padx=10, pady=20, sticky="w")
        # self.order.set(orderDateDESC[var])


class createTableAll(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, border_width=0)
        for widgets in self.winfo_children():
            widgets.destroy()
        getOverview(self, categorySortAll[0])


class createTableGeneral(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, border_width=0)
        for widgets in self.winfo_children():
            widgets.destroy()
        getOverview(self, categoryGeneral[var])


class createTableWork(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, border_width=0)
        for widgets in self.winfo_children():
            widgets.destroy()
        getOverview(self, categoryWork[var])


class createTablePrivate(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, border_width=0)
        for widgets in self.winfo_children():
            widgets.destroy()
        getOverview(self, categoryPrivate[var])


def getOverview(master, choice):
    master.grid_columnconfigure((0,1,2,3), weight=2)
    master.grid_columnconfigure(4, weight=1)

    if choice == categorySortAll[0] or choice == categorySortAll[1]:
        overviewAll = """SELECT * FROM contacts ORDER BY date DESC;"""
        cursor.execute(overviewAll)
    else:
        if choice == categoryGeneral[0] or choice == categoryGeneral[1]:
            cat = categoryGeneral[0]
        elif choice == categoryWork[0] or choice == categoryWork[1]:
            cat = categoryWork[0]
        elif choice == categoryPrivate[0] or choice == categoryPrivate[1]:
            cat = categoryPrivate[0]

        overviewSort = """SELECT * FROM contacts WHERE category = ? ORDER BY date DESC;"""
        cursor.execute(overviewSort, (cat,))

    contacts = cursor.fetchall()

    header = [categoryText[var], lastnameText[var], firstnameText[var], dateText[var]]

    c = 0

    for index, value in enumerate(header):
        master.header  = ctk.CTkLabel(master, text= value)
        master.header.grid(row=0, column=0 + c, padx=10, pady=20, sticky="nw")

        c = c + 1

    labels = {}
    r = 0

    for contact in contacts:
        entry_id = contact[0]
        category = contact[1]
        lastname = contact[2]
        firstname = contact[3]
        date = contact[7]

        if var == 1:
            if category == categoryGeneral[0]:
                category = categoryGeneral[1]
            elif category == categoryWork[0]:
                category = categoryWork[1]
            elif category == categoryPrivate[0]:
                category = categoryPrivate[1]

        labels[contact] = ctk.CTkLabel(master, text= f"{category}")
        labels[contact].grid(row=3 + r, column=0, padx=10, pady=5, sticky="nsw")
        labels[contact] = ctk.CTkLabel(master, text= f"{lastname}")
        labels[contact].grid(row=3 + r, column=1, padx=10, pady=5, sticky="nsw")
        labels[contact] = ctk.CTkLabel(master, text= f"{firstname}")
        labels[contact].grid(row=3 + r, column=2, padx=10, pady=5, sticky="nsw")
        labels[contact] = ctk.CTkLabel(master, text= f"{date}")
        labels[contact].grid(row=3 + r, column=3, padx=10, pady=5, sticky="nsw")

        showEntry = ctk.CTkButton(master, text=moreText[var], height=12, width=12, command=lambda id=entry_id: openDetails(id))
        showEntry.grid(row=3 + r, column=4, padx=10, pady=10, ipadx=10, ipady=2, sticky="nsw")

        r = r + 1



class settings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=500, height=500)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure((2,3,4), weight=1)

        getName = """SELECT name FROM settings;"""
        cursor.execute(getName)
        username = cursor.fetchone()

        self.name = ctk.CTkLabel(self, text="Name", height=12, width=12)
        self.name.grid(row=0, column=1, padx=(20, 10), pady=20, sticky="nesw")

        if username[0] is not None:
            current_name = username[0]

        self.nameEntry = ctk.CTkEntry(self, placeholder_text=current_name)
        self.nameEntry.grid(row=0, column=2, padx=10, pady=20, sticky="nsw")

        self.saveNameEntry = ctk.CTkButton(self, text=saveText[var], height=12, width=12, command=saveName)
        self.saveNameEntry.grid(row=0, column=4, padx=(10,20), pady=20, ipadx=10, ipady=2, sticky="nes")

        self.language = ctk.CTkButton(self, text="De/En", height=12, width=12, command=switchLanguage)
        self.language.grid(row=1, column=1, padx=20, pady=(20,10), ipadx=10, ipady=2, sticky="nesw")

        # infoIcon = ctk.CTkImage(light_image=Image.open("icons/info.png"), dark_image=Image.open("icons/info.png"), size=(16, 16))

        # self.langInfoIcon = ctk.CTkLabel(self, image=infoIcon, text="", height=12, width=12)
        # self.langInfoIcon.grid(row=1, column=2, padx=(20, 10), pady=20, sticky="nsw")

        # self.langInfo = ctk.CTkLabel(self, text=languageInfo[var], height=12, width=12)
        # self.langInfo.grid(row=1, column=2, padx=(10,20), pady=20, sticky="nes")

        self.mode = ctk.CTkButton(self, text="Dark/Light Mode", height=12, width=12, command=switchMode)
        self.mode.grid(row=2, column=1, padx=20, pady=10, ipadx=10, ipady=2, sticky="nesw")

        self.theme = ctk.CTkOptionMenu(self, values=["Pink", "Blue"], height=12, width=12, command=changeTheme, state="disabled")
        self.theme.grid(row=3, column=1, padx=20, pady=10, ipadx=10, ipady=2, sticky="nesw")

        self.backButton = ctk.CTkButton(self, text=closeText[var], height=12, width=12, command=self.destroy)
        self.backButton.grid(row=4, column=1, padx=20, ipadx=10, ipady=2, pady=(10,20))


def open_settings():
    root.settings_frame = settings(master=root)
    root.settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


def open_restart():
    restart_win = ctk.CTkToplevel()
    restart_win.title("Info")
    restart_win.geometry("300x100")
    restart_win.attributes('-topmost', 'true')
    restart_win.focus()
    restart_win.grab_set() 

    restart_win.grid_columnconfigure(1, weight=1)

    restart_win.info = ctk.CTkLabel(restart_win, text=restartInfo[var], height=12, width=12)
    restart_win.info.grid(row=0, column=1, padx=20, pady=20, sticky="nesw")

    restart_win.ok = ctk.CTkButton(restart_win, text="Ok", height=12, width=12, command=root.destroy)
    restart_win.ok.grid(row=1, column=1, padx=20, pady=20, ipadx=10, ipady=2, sticky="nesw")


def switchLanguage():
    if language[0] == "german":
        lang = "english"
    else:
        lang = "german"

    cursor.execute("UPDATE settings SET language = ?", (lang,))
    connection.commit()

    open_restart()


def saveName():
        y = root.settings_frame.nameEntry.get()
        cursor.execute("""UPDATE settings SET name = ?""", (y,))
        connection.commit()

        root.settings_frame.destroy()


def switchMode():
    getMode = """SELECT mode FROM settings;"""
    cursor.execute(getMode)
    mode = cursor.fetchone()

    if mode[0] == "dark":
        mde = "light"
        ctk.set_appearance_mode("light")
    else:
        mde = "dark"
        ctk.set_appearance_mode("dark")

    cursor.execute("UPDATE settings SET mode = ?", (mde,))
    connection.commit()


def changeTheme(choice):
    match choice:
        case "Blue":
            thm = "blue"
        case "Pink":
            thm = "pink"

    cursor.execute("UPDATE settings SET theme = ?", (thm,))
    connection.commit()


def openDetails(x):
    openEntry = ctk.CTkToplevel()
    openEntry.geometry("300x400")
    openEntry.attributes('-topmost', 'true')
    openEntry.focus()

    openEntry.grid_rowconfigure((1,2,3,4,5), weight=0)
    openEntry.grid_columnconfigure(1, weight=1)
    openEntry.grid_columnconfigure(2, weight=2)
    
    for widgets in openEntry.winfo_children():
        widgets.destroy()

    getEntry = """SELECT * FROM contacts WHERE id = ?;"""
    cursor.execute(getEntry, (x,))
    entries = cursor.fetchall()

    for entry in entries:
        category = entry[1]
        lastname = entry[2]
        firstname = entry[3]
        email = entry[4]
        phone = entry[5]
        address = entry[6]
        date = entry[7]

    openEntry.title(f"{lastname}, {firstname}")

    openEntry.categoryLabel = ctk.CTkLabel(openEntry, text=categoryText[var])
    openEntry.categoryLabel.grid(row=1, column=1, padx=(20,10), pady=(20,10), sticky="nw")

    openEntry.lastnameLabel = ctk.CTkLabel(openEntry, text=lastnameText[var])
    openEntry.lastnameLabel.grid(row=2, column=1, padx=(20,10), pady=(10,10), sticky="nw")

    openEntry.phoneLabel = ctk.CTkLabel(openEntry, text=phoneText[var])
    openEntry.phoneLabel.grid(row=3, column=1, padx=(20,10), pady=(10,10), sticky="nw")

    openEntry.addressLabel = ctk.CTkLabel(openEntry, text=addressText[var])
    openEntry.addressLabel.grid(row=4, column=1, padx=(20,10), pady=(10,10), sticky="nw")

    openEntry.dateLabel = ctk.CTkLabel(openEntry, text=dateText[var])
    openEntry.dateLabel.grid(row=5, column=1, padx=(20,10), pady=(10,20), sticky="nw")

    openEntry.categoryEntry = ctk.CTkLabel(openEntry, text= f"{category}")
    openEntry.categoryEntry.grid(row=1, column=2, padx=(10,20), pady=(20,10), sticky="nw")

    openEntry.categoryEntry = ctk.CTkLabel(openEntry, text= f"{email}")
    openEntry.categoryEntry.grid(row=2, column=2, padx=(10,20), pady=(10,10), sticky="nw")

    openEntry.categoryEntry = ctk.CTkLabel(openEntry, text= f"{phone}")
    openEntry.categoryEntry.grid(row=3, column=2, padx=(10,20), pady=(10,10), sticky="nw")

    openEntry.categoryEntry = ctk.CTkLabel(openEntry, text= f"{address}")
    openEntry.categoryEntry.grid(row=4, column=2, padx=(10,20), pady=(10,10), sticky="nw")

    openEntry.categoryEntry = ctk.CTkLabel(openEntry, text= f"{date}")
    openEntry.categoryEntry.grid(row=5, column=2, padx=(10,20), pady=(10,10), sticky="nw")

    openEntry.backButton = ctk.CTkButton(openEntry, text=closeText[var], height=12, width=12, command=openEntry.destroy)
    openEntry.backButton.grid(row=6, column=1, padx=(20,10), pady=(10,20), ipadx=10, ipady=2, sticky="nesw")

    def delete(x):
        cursor.execute("DELETE FROM contacts WHERE id= ?", (x,))
        connection.commit()

        openEntry.destroy

    deleteIcon = ctk.CTkImage(light_image=Image.open("icons/delete.png"), dark_image=Image.open("icons/delete.png"), size=(16, 16))

    openEntry.deleteButton = ctk.CTkButton(openEntry, image=deleteIcon, text="", height=12, width=12, command=lambda: delete(x))
    openEntry.deleteButton.grid(row=6, column=2, padx=(10,20), pady=(10,20), ipadx=10, ipady=2, sticky="nsw")

    # edit = ctk.CTkButton(self, text="E", height=12, width=12)
    # edit.grid(row=3 + r, column=7, padx=10, sticky="w")


root = root()
root.mainloop()