# -*- coding: utf-8.
"""
Created on Sat Oct 28 11:13:32 2023

@author: Sanchez-Cisneros
"""

import sqlite3
#THIS is a (RDBMS) Relational database management system.
DB_PATH = 'sample.db'

import sqlite3

def check_connection():
    """
    Check if there is a connection to the SQLite database.
    If there is a connection, print the version of SQLite.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        db_version = cur.fetchone()
        print("Connected to SQLite version:", db_version[0])
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        return False

import sqlite3

def create_table():
    """
    Creates a new table called 'sample_table' in the SQLite database located at DB_PATH.
    The table has three columns: 'id' (integer, primary key), 'name' (text, not null), and 'age' (integer, not null).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS sample_table (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL)''')
        print("Table created successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

import sqlite3

def insert_data():
    """
    Inserts a new record into the sample_table in the database.
    Prompts the user to enter a name and age, and inserts the values into the
    sample_table. If the insertion is successful, prints the number of records
    inserted. If an error occurs, prints the error message.
    """
    try:
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO sample_table (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        print(f"Inserted {cur.rowcount} record(s) successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

import sqlite3

def display_data():
    """
    Connects to a SQLite database and retrieves all rows from the 'sample_table' table.
    Prints each row to the console.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM sample_table")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

import sqlite3

def delete_data():
    """
    Deletes a record from the 'sample_table' table in the SQLite database located at DB_PATH.
    The user is prompted to enter the id of the record they want to delete.
    """
    try:
        display_data()  # First, display the data to help the user decide which record to delete.
        record_id = int(input("Enter the id of the record you want to delete: "))
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM sample_table WHERE id=?", (record_id,))
        conn.commit()
        
        if cur.rowcount:
            print(f"Deleted {cur.rowcount} record(s) successfully.")
        else:
            print("No records found with the provided id.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

def main():
    """
    This function displays a menu of options for managing an SQLite database.
    The user can choose to check the connection, create a table, insert data,
    display data, delete data, or exit the manager.
    """
    while True:
        print("\n=== SQLite Database Manager ===")
        print("1. Check connection")
        print("2. Create table")
        print("3. Insert data")
        print("4. Display data")
        print("5. Delete data")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            if check_connection():
                print("Database is running smoothly.")
            else:
                print("Unable to connect to the database!")
        elif choice == '2':
            create_table()
        elif choice == '3':
            insert_data()
        elif choice == '4':
            display_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            print("Exiting the manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
