from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon, QAction
from sys import argv, exit


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Window config
        self.setWindowTitle("Desglosador de Casetas")
        self.setWindowIcon(QIcon("Media\\window_icon\\icon.ico"))
        
        # Menu bar
        file_menu_item = self.menuBar().addMenu("&Archivo")
        records_menu_item = self.menuBar().addMenu("&Registros")
        help_menu_item = self.menuBar().addMenu("&Ayuda")
        
        # Menu bar actions
        add_ticket_action = QAction("Agregar caseta", self)
        file_menu_item.addAction(add_ticket_action)
        
        remove_ticket_action = QAction("Eliminar caseta", self)
        file_menu_item.addAction(remove_ticket_action)
        
        edit_ticket_action = QAction("Editar caseta", self)
        file_menu_item.addAction(edit_ticket_action)
        
app = QApplication(argv)
main_window = MainWindow()
main_window.show()
exit(app.exec())