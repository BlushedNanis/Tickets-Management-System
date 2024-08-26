from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon
from sys import argv, exit

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Window config
        self.setWindowTitle("Desglosador de Casetas")
        icon = QIcon("Media\\icon.ico")
        self.setWindowIcon(icon)
        
        # Menu bar
        file_menu_item = self.menuBar().addMenu("&Archivo")
        records_menu_item = self.menuBar().addMenu("&Registros")
        help_menu_item = self.menuBar().addMenu("&Ayuda")
        
        
app = QApplication(argv)
main_window = MainWindow()
main_window.show()
exit(app.exec())