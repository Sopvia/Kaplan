from tkinter import *
import customtkinter as ctk

lastnameText = "Lastname"

def open_createEntry():
    createEntry = ctk.CTkToplevel()
    createEntry.title("New Entry")
    createEntry.config(width=600, height=600)

    createEntry.lastname = ctk.CTkLabel(createEntry, text=lastnameText, height=12, width=12, text_color="white")
    createEntry.lastname.grid(row=1, column=1, padx=20, pady=20, sticky="ne")

# class createEntry(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs, fg_color="black", width=500, height=500)

#         self.grid_rowconfigure(1, weight=0)
#         self.grid_columnconfigure(1, weight=1)

#         self.lastname = ctk.CTkLabel(self, text=lastnameText, height=12, width=12, text_color="white")
#         self.lastname.grid(row=1, column=1, padx=20, pady=20, sticky="ne")