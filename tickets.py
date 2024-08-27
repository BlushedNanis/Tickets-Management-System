import pandas as pd

class Tickets():
    def __init__(self) -> None:
        self.data = pd.DataFrame(columns=["ID", "Toll", "Total", "Sub-Total", "IVA"])
        self.data["ID"] = self.data.index
        self.data = self.data.fillna("")
        
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
        
        
if __name__ == "__main__":
    t = Tickets()
    print(t.data)
    for index, row in t.data.iterrows():
        print(index)
        for column, data in enumerate(row):
            print(column, data)