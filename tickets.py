import pandas as pd

class Tickets():
    def __init__(self) -> None:
        self.data = pd.DataFrame(index=range(1,6), 
                            columns=["ID", "Toll", "Total", "Sub-Total", "IVA"])
        self.data["ID"] = self.data.index
        self.data = self.data.fillna("")
        
    def add_ticket(self):
        self.data.loc[len(self.data)+1] = [len(self.data)+1, "", "", "", ""]
        
        
if __name__ == "__main__":
    t = Tickets()
    print(t.data)
    for index, row in t.data.iterrows():
        print(index)
        for column, data in enumerate(row):
            print(column, data)