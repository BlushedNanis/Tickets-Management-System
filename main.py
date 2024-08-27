from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidget, \
    QAbstractItemView, QToolBar, QTableWidgetItem, QDialog, QLabel, \
    QGridLayout, QPushButton
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from tickets import Tickets
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
        add_ticket_action.triggered.connect(self.add_ticket)
        file_menu_item.addAction(add_ticket_action)
        
        remove_ticket_action = QAction(QIcon("Media\\action_icons\\remove.png"), 
                                       "Eliminar caseta", self)
        remove_ticket_action.triggered.connect(self.remove_ticket)
        file_menu_item.addAction(remove_ticket_action)
        
        edit_ticket_action = QAction(QIcon("Media\\action_icons\\edit.png"), 
                                     "Editar caseta", self)
        file_menu_item.addAction(edit_ticket_action)
        
        for action in file_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
        # --> Records menu actions
        view_records_action = QAction("Ver registros", self)
        records_menu_item.addAction(view_records_action)
        
        search_records_action = QAction(QIcon("Media\\action_icons\\search.png"), 
                                        "Buscar registros", self)
        records_menu_item.addAction(search_records_action)
        
        path_records_action = QAction("Ruta de guardado", self)
        records_menu_item.addAction(path_records_action)
        
        for action in records_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
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
        
        self.load_empty_tickets()
        
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
        
    def load_tickets(self):
        self.table.setRowCount(0)
        for index, row in self.tickets.data.iterrows():
            self.table.insertRow(index-1)
            for column_number, cell_data in enumerate(row):
                self.table.setItem(index-1, column_number,
                                   QTableWidgetItem(str(cell_data)))
    
    def load_empty_tickets(self):
        self.tickets = Tickets()
        self.load_tickets()
        
    def add_ticket(self):
        self.tickets.add_ticket()
        self.load_tickets()
        
    def remove_ticket(self):
        self.dialog = RemoveDialog()
        self.dialog.exec()
        
class RemoveDialog(QDialog):
    """
    QDialog to remove an specific ticket from the main window table.
    The ticket to be removed will be the one selected from the user on the table.
    If the user does not select a ticket, by default ID = 1 is selected. 
    """
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("Media\\action_icons\\remove.png"))
        self.setWindowTitle("Eliminar caseta")
        self.setFixedSize(270,100)
        layout = QGridLayout()
        
        # Get the ticket ID, based on the selected row on the table
        self.ticket_id = int(main_window.table.item(main_window.table.currentRow(),
                                                    0).text())
        
        # Dialog widgets
        label = QLabel("¿Estás seguro que deseas eliminar esta caseta?")
        layout.addWidget(label, 0, 0, 1, 2)
        
        ticket_label = QLabel(f"Caseta ID: {self.ticket_id}")
        layout.addWidget(ticket_label, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        
        yes_button = QPushButton("Si")
        yes_button.clicked.connect(self.remove_ticket)
        layout.addWidget(yes_button, 2, 0)
        
        no_button = QPushButton("No")
        no_button.clicked.connect(self.close)
        layout.addWidget(no_button, 2, 1)
        
        self.setLayout(layout)
        
    def remove_ticket(self):
        """
        Removes the selected ticket from the main window table and update it
        """
        main_window.tickets.remove_ticket(self.ticket_id)
        main_window.load_tickets()
        self.close()
        

if __name__ == "__main__":
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())