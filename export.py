import pandas as pd
from os import environ, path, mkdir

DIRECTORY = environ["USERPROFILE"] + "\\.tickets\\exports"
if not path.exists(DIRECTORY):
    mkdir(DIRECTORY)
    

class EXPORT():
    def __init__(self):
        self.path = DIRECTORY
        
    def to_csv(self, data:pd.DataFrame, path:str, file_name:str) -> None:
        """Exports the given data (tickets) with the given name into the given
        directory as a csv file. Also adds a a row at the end with the summary
        of the data.

        Args:
            data (pd.DataFrame): Data to be exported
            path (str): Directory where the file will be saved
            file_name (str): Name of the file to export
        """
        data_to_export = self.prepare_data(data)
        data_to_export.to_csv(path + "\\" + file_name + ".csv", index=False)
        
    def to_excel(self, data:pd.DataFrame, path:str, file_name:str) -> None:
        """Exports the given data (tickets) with the given name into the given
        directory as a xlsx file. Also adds a a row at the end with the summary
        of the data.

        Args:
            data (pd.DataFrame): Data to be exported
            path (str): Directory where the file will be saved
            file_name (str): Name of the file to export
        """
        data_to_export = self.prepare_data(data)
        data_to_export.to_excel(path + "\\" + file_name + ".xlsx", index=False)
        
    def prepare_data(self, data:pd.DataFrame) -> pd.DataFrame:
        """Prepares the data (tickets) to be exported, adding a new row with 
        the summary of the tickets.

        Args:
            data (pd.DataFrame): Data to be prepared

        Returns:
            pd.DataFrame: Prepared Data
        """
        summary = data.sum()
        summary["ID"] = ""
        summary["Toll"] = "TOTAL"
        summary["Total"] = round(summary["Total"], 2)
        summary["Sub-Total"] = round(summary["Sub-Total"], 2)
        summary["IVA"] = round(summary["IVA"], 2)
        summary = summary.to_frame().T
        prepared_data = pd.concat([data, summary])
        return prepared_data