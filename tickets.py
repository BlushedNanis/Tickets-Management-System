import pandas as pd
import sqlite3 as db
from os import environ, path, mkdir

DIRECTORY = environ["USERPROFILE"] + "\\.tickets"
if not path.exists(DIRECTORY):
    mkdir(DIRECTORY)

class Tickets():
    def __init__(self) -> None:
        self.data = pd.DataFrame(columns=["ID", "Ticket", "Total", "Sub-Total", "IVA"])
        self.data["ID"] = self.data.index
        self.db_file = DIRECTORY + "\\records.db"
        
    def add_ticket(self, ticket_name:str, ticket_total:float):
        """
        Adds a new ticket to the dataframe, automatically calculates the
        Sub-Total and IVA columns.

        Args:
            ticket_name (str): Name of the ticket
            ticket_total (float): Total amount of the ticket
        """
        sub_total = round(ticket_total / 1.16, 2)
        iva = round(sub_total * 0.16, 2)
        self.data.loc[len(self.data)+1] = [len(self.data)+1, ticket_name,
                                           ticket_total, sub_total, iva]
        
    def remove_ticket(self, index:int):
        """Removes the row at the given index, and update the index and ID
        column for all the rows.

        Args:
            index (int): index to be removed from the dataframe
        """
        self.data = self.data.drop(index)
        self.data.index = range(1,len(self.data)+1)
        self.data["ID"] = self.data.index
        
    def edit_ticket(self, index:int, ticket_name:str, ticket_total:float):
        """Edits the row at the given index with the provided user data. Also
        updates the Sub-Total and IVA.

        Args:
            index (int): Index of the row to be edited
            ticket_name (str): Name of the ticket
            ticket_total (float): Total amount of the ticket
        """
        sub_total = round(ticket_total / 1.16, 2)
        iva = round(sub_total * 0.16, 2)
        self.data.loc[index] = (index, ticket_name, ticket_total, sub_total, iva)
        
    def calculate_summary(self):
        """
        Calculates the sum of the current tickets data, assigning it to the 
        "summary" variable of the object.
        And formats the values to fit the main window table.
        """
        self.summary = self.data.sum()
        self.summary["ID"] = ""
        self.summary["Ticket"] = "TOTAL"
        self.summary["Total"] = round(self.summary["Total"], 2)
        self.summary["Sub-Total"] = round(self.summary["Sub-Total"], 2)
        self.summary["IVA"] = round(self.summary["IVA"], 2)
        
    def save_record(self, record_name:str):
        """Save the record into the database.
        
        Args:
            record_name (str): Name of the record
        """
        conn = db.connect(self.db_file)
        self.data.to_sql(record_name, conn, index=False, if_exists="replace")
        conn.close()
        
    def clear_data(self) -> None:
        """
        Remove all the rows in the 'data' Data Frame
        """
        self.data = self.data.drop(range(1,len(self.data)+1))
        
    def fetch_record(self, record_name:str) -> None:
        """Fetch the record with the given name and assign it to the tickets
        data (DataFrame) variable

        Args:
            record_name (str):  Name of the record
        """
        conn = db.connect(self.db_file)
        self.data = pd.read_sql_query(f"SELECT * FROM {record_name}", conn)
        self.data.index = self.data["ID"].values
        conn.close()
        
        
if __name__ == "__main__":
    t = Tickets()
    print(t.data)
    for index, row in t.data.iterrows():
        print(index)
        for column, data in enumerate(row):
            print(column, data)