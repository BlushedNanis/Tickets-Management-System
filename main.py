from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon
from sys import argv, exit

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desglosador de Casetas")

        
        
app = QApplication(argv)
main_window = MainWindow()
main_window.show()
exit(app.exec())