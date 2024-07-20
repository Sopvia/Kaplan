import sqlite3

connection = sqlite3.connect("addressBook.db")
cursor = connection.cursor()

createTable = """CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, category TEXT,lastname TEXT,firstname TEXT,email TEXT,phone INTEGER,address TEXT,date TEXT);"""
cursor.execute(createTable)
connection.commit()

createSettingsTable = """CREATE TABLE IF NOT EXISTS settings (language TEXT, name TEXT);"""
cursor.execute(createSettingsTable)
connection.commit()