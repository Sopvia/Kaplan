from tkinter import messagebox
import customtkinter as ctk
from variables import *
import sqlite3
from datetime import datetime

connection = sqlite3.connect("addressBook.db")
cursor = connection.cursor()


def open_createEntry():
    
    createEntry = ctk.CTkToplevel(fg_color="black")
    createEntry.title("New Entry")
    createEntry.geometry("600x600")
    createEntry.attributes('-topmost', 'true')
    createEntry.focus()

    for widgets in createEntry.winfo_children():
        widgets.destroy()

    createEntry.grid_rowconfigure(6, weight=1)
    createEntry.grid_columnconfigure(1, weight=1)
    createEntry.grid_columnconfigure(2, weight=2)


    createEntry.category = ctk.CTkLabel(createEntry, text=categoryText, height=12, width=12, text_color="white")
    createEntry.category.grid(row=0, column=1, padx=20, pady=20, sticky="nesw")

    createEntry.categoryEntry = ctk.CTkComboBox(createEntry, values=[categoryGeneral, categoryWork, categoryPrivate], state="readonly")
    createEntry.categoryEntry.grid(row=0, column=2, columnspan=2, padx=20, pady=20, sticky="ne")

    createEntry.lastname = ctk.CTkLabel(createEntry, text=lastnameText, height=12, width=12, text_color="white")
    createEntry.lastname.grid(row=1, column=1, padx=20, pady=20, sticky="nesw")

    createEntry.lastnameEntry = ctk.CTkEntry(createEntry)
    createEntry.lastnameEntry.grid(row=1, column=2, columnspan=2, padx=20, pady=20, sticky="ne")

    createEntry.firstname = ctk.CTkLabel(createEntry, text=firstnameText, height=12, width=12, text_color="white")
    createEntry.firstname.grid(row=2, column=1, padx=20, pady=20, sticky="nesw")

    createEntry.firstnameEntry = ctk.CTkEntry(createEntry)
    createEntry.firstnameEntry.grid(row=2, column=2, columnspan=2, padx=20, pady=20, sticky="ne")

    createEntry.email = ctk.CTkLabel(createEntry, text=emailText, height=12, width=12, text_color="white")
    createEntry.email.grid(row=3, column=1, padx=20, pady=20, sticky="nesw")

    createEntry.emailEntry = ctk.CTkEntry(createEntry)
    createEntry.emailEntry.grid(row=3, column=2, columnspan=2, padx=20, pady=20, sticky="ne")

    createEntry.phone = ctk.CTkLabel(createEntry, text=phoneText, height=12, width=12, text_color="white")
    createEntry.phone.grid(row=4, column=1, padx=20, pady=20, sticky="nesw")

    createEntry.phoneEntry = ctk.CTkEntry(createEntry)
    createEntry.phoneEntry.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="ne")

    createEntry.address = ctk.CTkLabel(createEntry, text=addressText, height=12, width=12, text_color="white")
    createEntry.address.grid(row=5, column=1, padx=20, pady=20, sticky="nesw")

    createEntry.addressEntry = ctk.CTkEntry(createEntry)
    createEntry.addressEntry.grid(row=5, column=2, columnspan=2, padx=20, pady=20, sticky="ne")


    def save():
        if not (createEntry.categoryEntry.get() and createEntry.lastnameEntry.get() and createEntry.firstnameEntry.get()):
            messagebox.showerror('Error', errorText + "!", parent=createEntry)
        else:
            categoryInput = createEntry.categoryEntry.get()
            lastnameInput = createEntry.lastnameEntry.get()
            firstnameInput = createEntry.firstnameEntry.get()
            emailInput = createEntry.emailEntry.get()
            phoneInput = createEntry.phoneEntry.get()
            addressInput = createEntry.addressEntry.get()

            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")

            cursor.execute("INSERT INTO contacts (category, lastname, firstname, email, phone, address, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (categoryInput,lastnameInput,firstnameInput,emailInput,phoneInput,addressInput,date))
            connection.commit()
            connection.close()

            createEntry.destroy()
                

    createEntry.closeButton = ctk.CTkButton(createEntry, text=closeText, height=12, width=12, text_color="white", command=createEntry.destroy)
    createEntry.closeButton.grid(row=6, column=2, padx=20, pady=20, sticky="ne")

    createEntry.saveButton = ctk.CTkButton(createEntry, text=saveText, height=12, width=12, text_color="white", command=save)
    createEntry.saveButton.grid(row=6, column=3, padx=20, pady=20, sticky="ne")