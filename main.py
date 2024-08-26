from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidget, \
    QAbstractItemView, QToolBar
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize
from sys import argv, exit


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Window config
        self.setWindowTitle("Desglosador de Casetas")
        self.setWindowIcon(QIcon("Media\\window_icon\\icon.ico"))
        self.resize(600, 400)
        
        # Menu bar
        file_menu_item = self.menuBar().addMenu("&Archivo")
        records_menu_item = self.menuBar().addMenu("&Registros")
        help_menu_item = self.menuBar().addMenu("&Ayuda")
        
        # Menu bar actions
        # --> File menu actions
        add_record_action = QAction("Nuevo registro", self)
        file_menu_item.addAction(add_record_action)
        
        save_record_action = QAction(QIcon("Media\\action_icons\\save.png"), 
                                     "Guardar registro", self)
        file_menu_item.addAction(save_record_action)
        
        export_record_action = QAction(QIcon("Media\\action_icons\\export.png"), 
                                       "Exportar registro", self)
        file_menu_item.addAction(export_record_action)
        
        file_menu_item.addSeparator()
        
        add_ticket_action = QAction(QIcon("Media\\action_icons\\add.png"), 
                                    "Agregar caseta", self)
        file_menu_item.addAction(add_ticket_action)
        
        remove_ticket_action = QAction(QIcon("Media\\action_icons\\remove.png"), 
                                       "Eliminar caseta", self)
        file_menu_item.addAction(remove_ticket_action)
        
        edit_ticket_action = QAction(QIcon("Media\\action_icons\\edit.png"), 
                                     "Editar caseta", self)
        file_menu_item.addAction(edit_ticket_action)
        
        # --> Records menu actions
        view_records_action = QAction("Ver registros", self)
        records_menu_item.addAction(view_records_action)
        
        search_records_action = QAction(QIcon("Media\\action_icons\\search.png"), 
                                        "Buscar registros", self)
        records_menu_item.addAction(search_records_action)
        
        path_records_action = QAction("Ruta de guardado", self)
        records_menu_item.addAction(path_records_action)
        
        # --> Help menu actions
        guide_help_action = QAction("Guía de uso", self)
        help_menu_item.addAction(guide_help_action)
        
        repo_help_action = QAction("Repositorio (GitHub)", self)
        help_menu_item.addAction(repo_help_action)
        
        blushed_help_action = QAction("BlushedNanis", self)
        help_menu_item.addAction(blushed_help_action)

        # Tickets table
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("ID", "Caseta", "Total", 
                                              "Sub-Total", "IVA"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
        # Toolbar
        tool_bar = QToolBar()
        tool_bar.setMovable(True)
        tool_bar.setFloatable(False)
        self.addToolBar(Qt.BottomToolBarArea,tool_bar)
        tool_bar.addActions((add_ticket_action, remove_ticket_action, 
                             edit_ticket_action))
        tool_bar.addSeparator()
        tool_bar.addActions((save_record_action, export_record_action,
                             search_records_action))
        tool_bar.setStyleSheet("QToolBar{spacing: 5px; padding: 5px;}")
        
        
app = QApplication(argv)
main_window = MainWindow()
main_window.show()
exit(app.exec())