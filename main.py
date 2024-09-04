from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidget, \
    QAbstractItemView, QToolBar, QTableWidgetItem, QDialog, QLabel, \
    QGridLayout, QPushButton, QLineEdit, QSpacerItem, QMessageBox
from PySide6.QtGui import QIcon, QAction, QRegularExpressionValidator
from PySide6.QtCore import Qt
from tickets import Tickets
from sys import argv, exit


class MainWindow(QMainWindow):
    """
    QMainWindow, which displays a table as the main widget, the table contains
    the tickets information. It also contains a menubar and toolbar.
    """
    def __init__(self):
        super().__init__()
        
        # Create the tickets instance
        self.create_tickets()
        
        # Validator to decimal number inputs
        self.float_validator = QRegularExpressionValidator("^\\d+(\\.\\d+)?$")
        
        # Window config
        self.setWindowIcon(QIcon("Media\\window_icon\\icon.ico"))
        
        # Menu bar
        file_menu_item = self.menuBar().addMenu("&Archivo")
        records_menu_item = self.menuBar().addMenu("&Registros")
        help_menu_item = self.menuBar().addMenu("&Ayuda")
        
        # Actions
        # --> Tickets actions
        self.add_tickets_action = QAction(QIcon("Media\\action_icons\\add.png"),
                                          "Agregar casetas", self)
        self.add_tickets_action.triggered.connect(self.add_tickets)
        
        self.remove_ticket_action = QAction(QIcon("Media\\action_icons\\remove.png"),
                                            "Eliminar caseta", self)
        self.remove_ticket_action.triggered.connect(self.remove_ticket)
        
        self.edit_ticket_action = QAction(QIcon("Media\\action_icons\\edit.png"),
                                          "Editar caseta", self)
        self.edit_ticket_action.triggered.connect(self.edit_ticket)
        
        # --> Records actions
        self.view_records_action = QAction(QIcon("Media\\action_icons\\view.png"),
                                           "Ver registros", self)
        self.view_records_action.triggered.connect(self.show_records_window)
        
        self.new_record_action = QAction(QIcon("Media\\action_icons\\add.png"),
                                               "Nuevo registro", self)
        self.new_record_action.triggered.connect(self.new_record)
        
        self.remove_record_action = QAction(QIcon("Media\\action_icons\\remove.png"),
                                            "Eliminar registro", self)
        self.remove_record_action.triggered.connect(self.remove_record)
        
        self.edit_record_action = QAction(QIcon("Media\\action_icons\\edit.png"),
                                          "Editar registro", self)
        
        self.save_record_action = QAction(QIcon("Media\\action_icons\\save.png"),
                                          "Guardar registro", self)
        self.save_record_action.triggered.connect(self.save_record)
        
        self.export_record_action = QAction(QIcon("Media\\action_icons\\export.png"),
                                            "Exportar registro", self)
        
        self.path_records_action = QAction("Ruta de guardado", self)
        
        # --> Help actions
        self.guide_help_action = QAction("Guía de uso", self)
        
        self.repo_help_action = QAction("Repositorio (GitHub)", self)
        
        self.blushed_help_action = QAction("BlushedNanis", self)
        
        
        
        # Menu bar actions
        # --> File actions
        file_menu_item.addAction(self.new_record_action)
        file_menu_item.addAction(self.save_record_action)
        file_menu_item.addAction(self.export_record_action)
        file_menu_item.addSeparator()
        file_menu_item.addAction(self.add_tickets_action)
        file_menu_item.addAction(self.remove_ticket_action)
        file_menu_item.addAction(self.edit_ticket_action)
        # Hide icons in file menu
        for action in file_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
        # --> Records actions
        records_menu_item.addAction(self.view_records_action)
        records_menu_item.addAction(self.path_records_action)
        # Hide icons in records menu
        for action in records_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
        # --> Help actions
        help_menu_item.addAction(self.guide_help_action)
        help_menu_item.addAction(self.repo_help_action)
        help_menu_item.addAction(self.blushed_help_action)
        
        # Toolbar
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(True)
        self.tool_bar.setFloatable(False)
        self.tool_bar.setStyleSheet("QToolBar{spacing: 5px; padding: 5px;}")
        self.addToolBar(Qt.BottomToolBarArea,self.tool_bar)
        
        # Table (Central Widget) config
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setCentralWidget(self.table)
        self.show_tickets_window() # Show tickets table by default
        
    def show_tickets_window(self):
        """
        Shows the tickets on the table widget and also the related toolbar
        """
        self.setWindowTitle("Desglosador de Casetas")
        self.resize(600, 600)
        self.menuBar().show()
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("ID", "Caseta", "Total", 
                                              "Sub-Total", "IVA"))
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(self.edit_ticket)
        # Set custom columns width
        col_widths = (30,300,70,70,70)
        for col, width in zip(range(0,5), col_widths):
            self.table.setColumnWidth(col,width)
        self.show_tickets_toolbar()
            
    def show_tickets_toolbar(self):
        """
        Shows the toolbar for the tickets table
        """
        self.tool_bar.clear()
        self.tool_bar.addActions((self.add_tickets_action,
                                  self.remove_ticket_action, 
                                  self.edit_ticket_action))
        self.tool_bar.addSeparator()
        self.tool_bar.addActions((self.save_record_action,
                                  self.export_record_action,
                                  self.view_records_action))
        
    def load_tickets(self):
        """
        Loads the tickets data into the main window table and 
        also loads the summary row at the end.
        """
        self.table.setRowCount(0)
        for index, row in self.tickets.data.iterrows():
            self.table.insertRow(index-1)
            for column_number, cell_data in enumerate(row):
                self.table.setItem(index-1, column_number,
                                   QTableWidgetItem(str(cell_data)))
        self.load_summary()
        self.table.scrollToBottom()
        
    def load_summary(self):
        """
        Loads the summary row at the end of the main window table and set the
        row as uneditable by the user.
        """
        self.tickets.calculate_summary()
        self.summary_row = self.table.rowCount()
        self.table.insertRow(self.summary_row)
        for col, cell_data in enumerate(self.tickets.summary):
            self.table.setItem(self.summary_row, col, 
                               QTableWidgetItem(str(cell_data)))
        for col in range(self.table.columnCount()):
            self.table.item(self.summary_row, col).setFlags(Qt.ItemFlag.ItemIsEnabled)
    
    def create_tickets(self):
        """
        Creates a tickets instance
        """
        self.tickets = Tickets()
        
    def add_tickets(self):
        """
        Executes the dialog to add tickets
        """
        self.dialog = AddTicketDialog()
        self.dialog.exec()
        
    def remove_ticket(self):
        """
        Executes the dialog to remove tickets, it pass if the table is empty
        """
        try:
            if self.is_not_summary():
                self.dialog = RemoveTicketDialog()
                self.dialog.exec()
        except AttributeError:
            pass
        
    def edit_ticket(self):
        """
        Executes the dialog to edit tickets, it pass if the table is empty
        """
        try:
            if self.is_not_summary():
                self.dialog = EditTicketDialog()
                self.dialog.exec()
        except AttributeError:
            pass
        
    def is_not_summary(self) -> bool:
        """Checks if the selected row by the user is not the summary row.

        Returns:
            bool: True if the selected row is not the summary row
        """
        row = self.table.currentRow()
        if row != self.summary_row:
            return True
        
    def save_record(self):
        """
        Executes the save record dialog, pass if the table is empty.
        """
        if self.table.rowCount() == 0:
            pass
        else:
            self.dialog = SaveRecordDialog()
            self.dialog.exec()
        
    def show_records_window(self):
        """
        Shows the records on the table widget and also the related toolbar.
        """
        self.setWindowTitle("Explorador de registros")
        self.resize(900,600)
        self.table.clear()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(("ID", "Registro", "Fecha de guardado", 
                                              "Fecha de modificacion", "Casetas",
                                              "Total", "Sub-Total", "IVA"))
        self.table.verticalHeader().setVisible(False)
        #self.table.doubleClicked.connect(self.edit_ticket)
        self.load_records()
        # Set custom columns width
        col_widths = (30,250,120,130,70,70,70,70)
        for col, width in zip(range(0,8), col_widths):
            self.table.setColumnWidth(col,width)
        self.menuBar().hide()
        self.show_records_toolbar()
        
    def show_records_toolbar(self):
        """
        Shows the toolbar for the records table
        """
        self.tool_bar.clear()
        self.tool_bar.addActions((self.new_record_action,
                                  self.remove_record_action, 
                                  self.edit_record_action,
                                  self.export_record_action))
        
    def load_records(self):
        """
        Loads the records data into the main window table
        """
        self.table.setRowCount(0)
        self.tickets.records.load_records()
        for index, row in self.tickets.records.data.iterrows():
            self.table.insertRow(index)
            for column_number, cell_data in enumerate(row):
                self.table.setItem(index, column_number,
                                   QTableWidgetItem(str(cell_data)))
        self.table.scrollToBottom()
        
    def new_record(self):
        self.show_tickets_window()
        
    def remove_record(self):
        """
        Executes the Remove Record Dialog if the current item is not None
        """
        if self.table.currentItem() is not None:
            self.dialog = RemoveRecordDialog()
            self.dialog.exec()
        
          
class AddTicketDialog(QDialog):
    """
    QDialog, to add new tickets to the main window table. The dialog will
    remain open until the user close it manually, so multiple tickets can be
    added at once.
    """
    def __init__(self):
        super().__init__()
        # Dialog config
        self.setWindowIcon(QIcon("Media\\action_icons\\add.png"))
        self.setWindowTitle("Agregar casetas")
        self.setFixedSize(200,200)
        layout = QGridLayout()
        
        # Dialog widgets
        self.ticket_id_label = QLabel("Caseta ID: "\
                                      f"{len(main_window.tickets.data) + 1}")
        layout.addWidget(self.ticket_id_label, 0, 0, 1, 2, 
                         Qt.AlignmentFlag.AlignHCenter)
        
        ticket_name_label = QLabel("Caseta:")
        layout.addWidget(ticket_name_label, 1, 0, 1, 2)
        
        self.ticket_name = QLineEdit(f"Caseta {len(main_window.tickets.data) + 1}")
        layout.addWidget(self.ticket_name, 2, 0, 1, 2)
        
        ticket_total_label = QLabel("Total:")
        layout.addWidget(ticket_total_label, 3, 0, 1, 2)
        
        self.ticket_total = QLineEdit()
        self.ticket_total.setPlaceholderText("$")
        self.ticket_total.setValidator(main_window.float_validator) # Decimal number validator
        layout.addWidget(self.ticket_total, 4, 0, 1, 2)
        
        # Vertical spacing for buttons
        layout.addItem(QSpacerItem(20,20), 5, 0, 1, 2)
        
        add_button = QPushButton("Agregar")
        add_button.clicked.connect(self.add_ticket)
        layout.addWidget(add_button, 6, 0)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button, 6, 1)
        
        self.setLayout(layout)
        
        # Set focus on total, for user convenience
        self.ticket_total.setFocus()
        
    def add_ticket(self):
        """
        Adds a new ticket to the tickets dataframe, with the information 
        provided by the user. Ift the user leaves blank inputs a warning
        message will appear.
        """
        if self.ticket_total.text() == "" or self.ticket_name.text() == "":
            self.value_warning()
        else:
            main_window.tickets.add_ticket(self.ticket_name.text(),
                                        float(self.ticket_total.text()))
            main_window.load_tickets()
            self.ticket_total.clear()
            self.ticket_total.setFocus()
            self.ticket_id_label.setText("Caseta ID: "\
                                        f"{len(main_window.tickets.data) + 1}")
            self.ticket_name.setText(f"Caseta {len(main_window.tickets.data) + 1}")
        
            
    def value_warning(self):
        """
        QMessageBox to let the user know it has missing data. It also resets
        the input lines to the default values.
        """
        value_message = QMessageBox()
        value_message.setWindowIcon(QIcon("Media\\window_icon\\warning.png"))
        value_message.setWindowTitle("Advertencia")
        value_message.setText("Ooops, parece que te faltó llenar un campo")
        value_message.exec()
        self.ticket_total.clear()
        self.ticket_name.setText(f"Caseta {len(main_window.tickets.data) + 1}")
        self.ticket_total.setFocus()
        
        
class RemoveTicketDialog(QDialog):
    """
    QDialog to remove an specific ticket from the main window table.
    The ticket to be removed will be the one selected from the user on the table.
    If the user does not select a ticket, by default ID = 1 is selected. 
    """
    def __init__(self):
        super().__init__()
        # Dialog config
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
        
        
class EditTicketDialog(QDialog):
    """
    QDialog, to edit an specific ticket from the main window table. 
    The ticket to be removed will be the one selected from the user on the table.
    If the user does not select a ticket, by default ID = 1 is selected.
    """
    def __init__(self):
        super().__init__()
        # Dialog config
        self.setWindowIcon(QIcon("Media\\action_icons\\edit.png"))
        self.setWindowTitle("Editar caseta")
        self.setFixedSize(200,200)
        layout = QGridLayout()
        
        # Get the ticket ID, based on the selected row on the table
        self.ticket_id = int(main_window.table.item(main_window.table.currentRow(),
                                                    0).text())
        
        # Dialog widgets
        self.ticket_id_label = QLabel(f"Caseta ID: {self.ticket_id}")
        layout.addWidget(self.ticket_id_label, 0, 0, 1, 2, 
                         Qt.AlignmentFlag.AlignHCenter)
        
        ticket_name_label = QLabel("Caseta:")
        layout.addWidget(ticket_name_label, 1, 0, 1, 2)
        
        self.ticket_name = QLineEdit(main_window.table.item(
            main_window.table.currentRow(), 1).text())
        layout.addWidget(self.ticket_name, 2, 0, 1, 2)
        
        ticket_total_label = QLabel("Total:")
        layout.addWidget(ticket_total_label, 3, 0, 1, 2)
        
        self.ticket_total = QLineEdit(main_window.table.item(
            main_window.table.currentRow(),2).text())
        self.ticket_total.setPlaceholderText("$")
        self.ticket_total.setValidator(main_window.float_validator) # Decimal number validator
        layout.addWidget(self.ticket_total, 4, 0, 1, 2)
        
        # Vertical spacing for buttons
        layout.addItem(QSpacerItem(20,20), 5, 0, 1, 2)
        
        add_button = QPushButton("Terminar")
        add_button.clicked.connect(self.edit_ticket)
        layout.addWidget(add_button, 6, 0)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button, 6, 1)
        
        self.setLayout(layout)
        
        # Set focus on total, for user convenience
        self.ticket_total.setFocus()
        
    def edit_ticket(self):
        """
        Updates the selected ticket with the given information by the user and
        re-loads the main window table.
        """
        if self.ticket_total.text() == "" or self.ticket_name.text() == "":
            self.value_warning()
        else:
            main_window.tickets.edit_ticket(self.ticket_id, self.ticket_name.text(), 
                                            float(self.ticket_total.text()))
            main_window.load_tickets()
            self.close()
            
    def value_warning(self):
        """
        QMessageBox to let the user know it has missing data. It also resets
        the input lines to the default values.
        """
        value_message = QMessageBox()
        value_message.setWindowIcon(QIcon("Media\\window_icon\\warning.png"))
        value_message.setWindowTitle("Advertencia")
        value_message.setText("Ooops, parece que te faltó llenar un campo")
        value_message.exec()
        
        
class SaveRecordDialog(QDialog):
    """
    QDialog, to save the current tickets in the table as a record in the database.
    
    """
    def __init__(self):
        super().__init__()
        # Dialog config
        self.setWindowIcon(QIcon("Media\\action_icons\\save.png"))
        self.setWindowTitle("Guardar registro")
        self.setFixedSize(200,120)
        layout = QGridLayout()
        
        # Dialog widgets
        ticket_name_label = QLabel("Nombre del registro:")
        layout.addWidget(ticket_name_label, 1, 0, 1, 2)
        
        self.record_name = QLineEdit()
        layout.addWidget(self.record_name, 2, 0, 1, 2)
        
        # Vertical spacing for buttons
        layout.addItem(QSpacerItem(20,20), 5, 0, 1, 2)
        
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_record)
        layout.addWidget(save_button, 6, 0)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button, 6, 1)
        
        self.setLayout(layout)
        
    def save_record(self):
        """
        Saves the list of tickets into the database.
        """
        main_window.tickets.save_record(self.record_name.text())
        self.clear_tickets()
        self.close() 
        
    def clear_tickets(self):
        """
        Clear the tickets.data DataFrame and reset the rows on the main window
        table.
        """
        main_window.table.setRowCount(0)
        main_window.tickets.clear_data()
        
        
class RemoveRecordDialog(QDialog):
    """
    QDialog to remove an specific record from the database.
    The record to be removed will be the one selected from the user on the table.
    """
    def __init__(self):
        super().__init__()
        # Dialog config
        self.setWindowIcon(QIcon("Media\\action_icons\\remove.png"))
        self.setWindowTitle("Eliminar registro")
        self.setFixedSize(270,100)
        layout = QGridLayout()
        
        # Get the ticket ID, based on the selected row on the table
        self.record_name = main_window.table.item(main_window.table.currentRow(),
                                                  1).text()
        
        # Dialog widgets
        label = QLabel("¿Estás seguro que deseas eliminar este registro?")
        layout.addWidget(label, 0, 0, 1, 2)
        
        ticket_label = QLabel(f"Registro: {self.record_name}")
        layout.addWidget(ticket_label, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        
        yes_button = QPushButton("Si")
        yes_button.clicked.connect(self.remove_record)
        layout.addWidget(yes_button, 2, 0)
        
        no_button = QPushButton("No")
        no_button.clicked.connect(self.close)
        layout.addWidget(no_button, 2, 1)
        
        self.setLayout(layout)
        
    def remove_record(self):
        """
        Removes the selected record from the database and updates the table.
        """
        main_window.tickets.records.remove_record(self.record_name)
        main_window.load_records()
        self.close()
        

if __name__ == "__main__":
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())