import sqlite3 as db
from os import environ, path, mkdir
from time import strftime
import pandas as pd


DIRECTORY = environ["USERPROFILE"] + "\\.tickets"
if not path.exists(DIRECTORY):
    mkdir(DIRECTORY)
    
    
class Records():
    def __init__(self) -> None:
        self.db_file = DIRECTORY + "\\records.db"
        
    def create_table(self) -> None:
        """
        Creates the records table. With the following columns:
        - ID (primary key -> Int)
        - Name (-> Text)
        - DateC (Creation date-> Text)
        - DateM (Modification date -> Text)
        - Tickets (Number of tickets -> Integer)
        - Total (Sum of the totals -> Real)
        - SubTotal (Sum of the Sub-Totals -> Real)
        - IVA (Sum of the taxes -> Real)
        """
        conn = db.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE name=='records'")
        if cur.fetchone() is None:
            cur.execute("CREATE TABLE records(ID INTEGER PRIMARY KEY,"\
                                                "Name TEXT,"\
                                                "DateC TEXT,"\
                                                "DateM TEXT,"\
                                                "Tickets INTEGER,"\
                                                "Total REAL,"\
                                                "SubTotal REAL,"\
                                                "IVA REAL)")
        cur.close()
        conn.close()
        
    def add_record(self, data:pd.DataFrame, name:str) -> None:
        """Adds the given record of ticket to the table 'records', adding the 
        Creation and Modification date (Depends if the record already exists)

        Args:
            data (DataFrame): Tickets data
            name (str): Name of the record
        """
        now_date = strftime("%d/%m/%Y")
        tickets = len(data)
        total = round(data["Total"].sum(), 2)
        sub_total = round(data["Sub-Total"].sum(), 2)
        iva = round(data["IVA"].sum(), 2)
        
        conn = db.connect(self.db_file)
        cur = conn.cursor()
        
        if self.record_exists(name):
            cur.execute("UPDATE records SET DateM=?, Tickets=?, Total=?, SubTotal=?, IVA=?" \
                        "WHERE Name=?", (now_date, tickets, total, sub_total, iva, name))
            conn.commit()
            cur.close()
            conn.close()
        else:
            cur.execute("INSERT INTO records(Name, DateC, DateM, Tickets, Total, SubTotal, IVA)" \
                        "VALUES (?,?,?,?,?,?,?)", (name, now_date, "", 
                                                   tickets, total, sub_total, iva))
            conn.commit()
            cur.close()
            conn.close()
    
    def record_exists(self, name:str):
        """Checks if the given record name exists in the 'records' table

        Args:
            name (str): Name of the record

        Returns:
            bool: True if the records exists, False if it doesn't
        """
        conn = db.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT Name from records WHERE Name==(?)", (name,))
        if cur.fetchone() is None:
            return False
        else:
            return True
        
    def load_records(self) -> None:
        """
        Loads the records table into the variable data.
        """
        conn = db.connect(self.db_file)
        self.data = pd.read_sql_query("SELECT * FROM records", conn)
        conn.close()
