# -*- coding: utf-8.
"""
Created on Wed Oct 25 12:07:43 2023

@author: Sanchez-Cisneros
"""
#Program automatically checks SQL database to make sure running smoothly
# can be adjusted to send errors to email or text message when they occur
import sqlite3
from time import sleep

DB_PATH = 'sample.db'

import sqlite3

def check_connection():
    """
    Check if the connection to the SQLite database is successful.
    :return: True if the connection is successful, False otherwise.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute('SELECT SQLITE_VERSION()')
        db_version = cur.fetchone()
        print("Connected to SQLite version:", db_version[0])

        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)
        return False
    return True

def main():
    """
    Continuously checks the connection to the database every minute.
    If the connection is successful, it prints "Database is running smoothly."
    If the connection is unsuccessful, it prints "Unable to connect to the database!"
    """
    while True:
        if check_connection():
            print("Database is running smoothly.")
        else:
            print("Unable to connect to the database!")
        
        sleep(60)  # Check every minute ; can be modified

if __name__ == '__main__':
    main()
