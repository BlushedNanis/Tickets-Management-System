import pandas as pd

class Tickets():
    def __init__(self) -> None:
        self.data = pd.DataFrame(index=range(1,6), 
                            columns=["ID", "Toll", "Total", "Sub-Total", "IVA"])
        self.data["ID"] = self.data.index
        self.data = self.data.fillna("")
        
    def add_ticket(self):
        self.data.loc[len(self.data)+1] = [len(self.data)+1, "", "", "", ""]
        
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