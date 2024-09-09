from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidget, \
    QAbstractItemView, QToolBar, QTableWidgetItem, QDialog, QLabel, \
    QGridLayout, QPushButton, QLineEdit, QSpacerItem, QMessageBox, \
    QFileDialog, QComboBox
from PySide6.QtGui import QIcon, QAction, QRegularExpressionValidator
from PySide6.QtCore import Qt
from tickets import Tickets
from export import Export
from records import Records
from sys import argv, exit


class MainWindow(QMainWindow):
    """
    QMainWindow, which displays a table as the main widget, the table contains
    the tickets information. It also contains a menubar and toolbar.
    """
    def __init__(self):
        super().__init__()
        
        # Create the objects instances
        self.export = Export()
        self.tickets = Tickets()
        self.records = Records()
        
        # Validator to decimal number inputs
        self.float_validator = QRegularExpressionValidator("^\\d+(\\.\\d+)?$")
        
        # Window config
        self.setWindowIcon(QIcon("Media\\window_icon\\icon.ico"))
        self.setMinimumSize(300, 200)
        
        # Menu bar
        self.file_menu_item = self.menuBar().addMenu("&Archivo")
        self.records_menu_item = self.menuBar().addMenu("&Registros")
        self.help_menu_item = self.menuBar().addMenu("&Ayuda")
        
        # Actions
        # --> Tickets actions
        self.add_tickets_action = QAction(QIcon("Media\\action_icons\\add.png"),
                                          "Agregar tickets", self)
        self.add_tickets_action.triggered.connect(self.add_tickets)
        
        self.remove_ticket_action = QAction(QIcon("Media\\action_icons\\remove.png"),
                                            "Eliminar ticket", self)
        self.remove_ticket_action.triggered.connect(self.remove_ticket)
        
        self.edit_ticket_action = QAction(QIcon("Media\\action_icons\\edit.png"),
                                          "Editar ticket", self)
        self.edit_ticket_action.triggered.connect(self.edit_ticket)
        
        self.export_tickets_action = QAction(QIcon("Media\\action_icons\\export.png"),
                                            "Exportar tickets", self)
        self.export_tickets_action.triggered.connect(self.export_tickets)
        
        self.path_records_action = QAction("Ruta de exportado", self)
        self.path_records_action.triggered.connect(self.change_export_path)
        
        # --> Records actions
        self.view_records_action = QAction(QIcon("Media\\action_icons\\view.png"),
                                           "Ver registros", self)
        self.view_records_action.triggered.connect(self.view_records)
        
        self.new_record_action = QAction(QIcon("Media\\action_icons\\add.png"),
                                               "Nuevo registro", self)
        self.new_record_action.triggered.connect(self.new_record)
        
        self.remove_record_action = QAction(QIcon("Media\\action_icons\\remove.png"),
                                            "Eliminar registro", self)
        self.remove_record_action.triggered.connect(self.remove_record)
        
        self.open_record_action = QAction(QIcon("Media\\action_icons\\open.png"),
                                          "Abrir registro", self)
        self.open_record_action.triggered.connect(self.open_record)
        
        self.save_record_action = QAction(QIcon("Media\\action_icons\\save.png"),
                                          "Guardar registro", self)
        self.save_record_action.triggered.connect(self.save_record)
        
        # --> Help actions
        self.guide_help_action = QAction("Guía de uso", self)
        
        self.repo_help_action = QAction("Repositorio (GitHub)", self)
        
        self.blushed_help_action = QAction("BlushedNanis", self)

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
        self.show_tickets_window() # Show the tickets window by default
        
    def show_tickets_window(self):
        """
        Shows the tickets on the table widget and also the related toolbar and 
        menubar
        """
        self.setWindowTitle("Tickets Management System")
        self.resize(600, 600)
        self.menuBar().show()
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("ID", "Ticket", "Total", 
                                              "Sub-Total", "IVA"))
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.disconnect()
        self.table.doubleClicked.connect(self.edit_ticket)
        # Set custom columns width
        col_widths = (30,300,70,70,70)
        for col, width in zip(range(0,5), col_widths):
            self.table.setColumnWidth(col,width)
        self.show_tickets_toolbar()
        self.show_tickets_menubar()
            
    def show_tickets_toolbar(self):
        """
        Shows the toolbar for the tickets window
        """
        self.tool_bar.clear()
        self.tool_bar.addActions((self.add_tickets_action,
                                  self.remove_ticket_action, 
                                  self.edit_ticket_action))
        self.tool_bar.addSeparator()
        self.tool_bar.addActions((self.save_record_action,
                                  self.export_tickets_action,
                                  self.view_records_action))
        
    def show_tickets_menubar(self):
        """
        Shows the menubar for the tickets window
        """
        self.file_menu_item.clear()
        # --> File actions
        self.file_menu_item.addAction(self.save_record_action)
        self.file_menu_item.addAction(self.export_tickets_action)
        self.file_menu_item.addSeparator()
        self.file_menu_item.addAction(self.add_tickets_action)
        self.file_menu_item.addAction(self.remove_ticket_action)
        self.file_menu_item.addAction(self.edit_ticket_action)
        # Hide icons in file menu
        for action in self.file_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
        self.menuBar().addAction(self.records_menu_item.menuAction())
        # --> Records actions
        self.records_menu_item.addAction(self.view_records_action)
        self.records_menu_item.addAction(self.path_records_action)
        # Hide icons in records menu
        for action in self.records_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
        self.menuBar().addAction(self.help_menu_item.menuAction())
        self.help_menu_item.clear()
        # --> Help actions
        self.help_menu_item.addAction(self.guide_help_action)
        self.help_menu_item.addAction(self.repo_help_action)
        self.help_menu_item.addAction(self.blushed_help_action)
        
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
        Shows the records on the table widget and also the related toolbar and
        menubar
        """
        self.setWindowTitle("Explorador de registros")
        self.resize(900,600)
        self.tickets.clear_data()
        self.table.doubleClicked.disconnect()
        self.table.doubleClicked.connect(self.open_record)
        self.table.clear()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(("ID", "Registro", "Fecha de guardado", 
                                              "Fecha de modificacion", "Tickets",
                                              "Total", "Sub-Total", "IVA"))
        self.table.verticalHeader().setVisible(False)
        #self.table.doubleClicked.connect(self.edit_ticket)
        self.load_records()
        # Set custom columns width
        col_widths = (30,250,120,130,70,70,70,70)
        for col, width in zip(range(0,8), col_widths):
            self.table.setColumnWidth(col,width)
        self.show_records_toolbar()
        self.show_records_menubar()
        
    def show_records_toolbar(self):
        """
        Shows the toolbar for the records table
        """
        self.tool_bar.clear()
        self.tool_bar.addActions((self.new_record_action,
                                  self.remove_record_action, 
                                  self.open_record_action))
        
    def show_records_menubar(self):
        """
        Shows the menubar for the records window
        """
        self.file_menu_item.clear()
        # --> File actions
        self.file_menu_item.addAction(self.new_record_action)
        self.file_menu_item.addSeparator()
        self.file_menu_item.addAction(self.remove_record_action)
        self.file_menu_item.addAction(self.open_record_action)
        # Hide icons in file menu
        for action in self.file_menu_item.actions():
            action.setIconVisibleInMenu(False)
        
        self.menuBar().removeAction(self.records_menu_item.menuAction())
        
        self.help_menu_item.clear()
        # --> Help actions
        self.help_menu_item.addAction(self.guide_help_action)
        self.help_menu_item.addAction(self.repo_help_action)
        self.help_menu_item.addAction(self.blushed_help_action)
        
    def load_records(self):
        """
        Loads the records data into the main window table
        """
        self.table.setRowCount(0)
        self.records.load_records()
        for index, row in self.records.data.iterrows():
            self.table.insertRow(index)
            for column_number, cell_data in enumerate(row):
                self.table.setItem(index, column_number,
                                   QTableWidgetItem(str(cell_data)))
        self.table.scrollToBottom()
        
    def view_records(self):
        """
        Executes the View Records Dialog if the user have already registered
        tickets. If the table is empty then will show the records window
        directly
        """
        if self.table.rowCount() == 0:
            self.show_records_window()
        else:
            self.dialog = ViewRecordsDialog()
            self.dialog.exec()
        
    def new_record(self):
        self.show_tickets_window()
        
    def remove_record(self):
        """
        Executes the Remove Record Dialog if the current item is not None
        """
        if self.table.currentItem() is not None:
            self.dialog = RemoveRecordDialog()
            self.dialog.exec()
            
    def open_record(self):
        """
        Loads the selected record on the table, into the tickets table. If the
        current item is not None
        """
        if self.table.currentItem() is not None:
            record_name = self.table.item(self.table.currentRow(), 1).text()
            self.tickets.fetch_record(record_name)
            self.show_tickets_window()
            self.load_tickets()
            
    def export_tickets(self):
        """
        Executes the Export Tickets Dialog if the table is not empty.
        """
        if self.table.rowCount() != 0:
            self.dialog = ExportTicketsDialog()
            self.dialog.exec()
            
    def change_export_path(self):
        """
        
        """
        self.dialog = ChangeExportPath()
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
        self.setWindowTitle("Agregar tickets")
        self.setFixedSize(200,200)
        layout = QGridLayout()
        
        # Dialog widgets
        self.ticket_id_label = QLabel("Ticket ID: "\
                                      f"{len(main_window.tickets.data) + 1}")
        layout.addWidget(self.ticket_id_label, 0, 0, 1, 2, 
                         Qt.AlignmentFlag.AlignHCenter)
        
        ticket_name_label = QLabel("Ticket:")
        layout.addWidget(ticket_name_label, 1, 0, 1, 2)
        
        self.ticket_name = QLineEdit(f"Ticket {len(main_window.tickets.data) + 1}")
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
            self.ticket_id_label.setText("Ticket ID: "\
                                        f"{len(main_window.tickets.data) + 1}")
            self.ticket_name.setText(f"Ticket {len(main_window.tickets.data) + 1}")
        
            
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
        self.ticket_name.setText(f"Ticket {len(main_window.tickets.data) + 1}")
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
        self.setWindowTitle("Eliminar ticket")
        self.setFixedSize(270,100)
        layout = QGridLayout()
        
        # Get the ticket ID, based on the selected row on the table
        self.ticket_id = int(main_window.table.item(main_window.table.currentRow(),
                                                    0).text())
        
        # Dialog widgets
        label = QLabel("¿Estás seguro que deseas eliminar esta ticket?")
        layout.addWidget(label, 0, 0, 1, 2)
        
        ticket_label = QLabel(f"Ticket ID: {self.ticket_id}")
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
        self.setWindowTitle("Editar ticket")
        self.setFixedSize(200,200)
        layout = QGridLayout()
        
        # Get the ticket ID, based on the selected row on the table
        self.ticket_id = int(main_window.table.item(main_window.table.currentRow(),
                                                    0).text())
        
        # Dialog widgets
        self.ticket_id_label = QLabel(f"Ticket ID: {self.ticket_id}")
        layout.addWidget(self.ticket_id_label, 0, 0, 1, 2, 
                         Qt.AlignmentFlag.AlignHCenter)
        
        ticket_name_label = QLabel("Ticket:")
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
        
        
class ViewRecordsDialog(QDialog):
    """
    QDialog to confirm that the user wants to change from the tickets to the
    records window, with a warning about loosing the tickets in the current
    window
    """
    def __init__(self):
        super().__init__()
        # Dialog config
        self.setWindowIcon(QIcon("Media\\action_icons\\view.png"))
        self.setWindowTitle("Ver registros")
        self.setFixedSize(250,130)
        layout = QGridLayout()
        
        # Dialog widgets
        ticket_name_label = QLabel("Al continuar los tickets registrados en \n"\
                                   "la tabla serán eliminados.\n\n"\
                                   "¿Estás seguro de que deseas continuar?")
        ticket_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ticket_name_label, 1, 0, 1, 2)
        
        save_button = QPushButton("Si")
        save_button.clicked.connect(self.show_records)
        layout.addWidget(save_button, 6, 0)
        
        cancel_button = QPushButton("No")
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button, 6, 1)
        
        self.setLayout(layout)
        
    def show_records(self):
        """
        Shows the records window in the main window.
        """
        main_window.show_records_window()
        self.close()
        
        
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
        main_window.records.add_record(main_window.tickets.data,
                                       self.record_name.text())
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
        main_window.records.remove_record(self.record_name)
        main_window.load_records()
        self.close()
        
    
class ExportTicketsDialog(QDialog):
    """
    QDialog to export the current list of tickets in the main window table.
    The user is be able to choose the name of the file, directory and 
    type of file to export.
    """
    def __init__(self):
        super().__init__()
        
        self.directory_path = main_window.export.path
        
        # Dialog config
        self.setWindowIcon(QIcon("Media\\action_icons\\export.png"))
        self.setWindowTitle("Exportar tickets")
        self.setFixedSize(300,270)
        layout = QGridLayout()
        
        # Dialog widgets
        file_name_label = QLabel("Nombre del archivo:")
        layout.addWidget(file_name_label, 0, 0, 1, 2)
        
        self.file_name = QLineEdit()
        layout.addWidget(self.file_name, 1, 0, 1, 2)
        
        file_type_label = QLabel("Tipo de archivo:")
        layout.addWidget(file_type_label, 2, 0, 1, 2)
        
        self.file_type_box = QComboBox()
        self.file_type_box.addItems(("CSV", "EXCEL", "PDF"))
        layout.addWidget(self.file_type_box, 3, 0, 1, 2)
        
        self.path_label = QLabel("Ruta de exportado:")
        layout.addWidget(self.path_label, 4, 0, 1, 2)
        
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        self.file_path.setText(self.directory_path)
        layout.addWidget(self.file_path, 5, 0, 1, 2)
        
        directory_button = QPushButton("Seleccionar ruta")
        directory_button.clicked.connect(self.select_path_dialog)
        layout.addWidget(directory_button, 6, 0, 1, 2)
        
        # Vertical spacing for buttons
        layout.addItem(QSpacerItem(20,20), 7, 0, 1, 2)
        
        yes_button = QPushButton("Exportar")
        yes_button.clicked.connect(self.export_tickets)
        layout.addWidget(yes_button, 8, 0)
        
        no_button = QPushButton("Cancelar")
        no_button.clicked.connect(self.close)
        layout.addWidget(no_button, 8, 1)
        
        self.setLayout(layout)
        
    def select_path_dialog(self):
        """
        Opens a QFileDialog for the user to choose a directory to export.
        """
        self.directory_path = QFileDialog().getExistingDirectory()
        self.file_path.setText(self.directory_path)
        
    def export_tickets(self):
        """
        Exports the list of tickets in the main window table in the selected 
        type of file and directory.
        """
        if self.file_name.text() == "":
            self.value_warning()
        else:
            file_type = self.file_type_box.currentIndex()
            file_name = self.file_name.text()
            
            if file_type == 0:
                main_window.export.to_csv(main_window.tickets.data, self.directory_path, file_name)
                self.close()
                self.succes_message()
            elif file_type == 1:
                main_window.export.to_excel(main_window.tickets.data, self.directory_path, file_name)
                self.close()
                self.succes_message()
            else:
                main_window.export.to_pdf(main_window.tickets.data, self.directory_path, file_name)
                self.close()
                self.succes_message()
            
    def value_warning(self):
        """
        QMessageBox to let the user know it's missing to input the name of the 
        file.
        """
        value_message = QMessageBox()
        value_message.setWindowIcon(QIcon("Media\\window_icon\\warning.png"))
        value_message.setWindowTitle("Advertencia")
        value_message.setText("Ooops, parece que te faltó ingresar el nombre")
        value_message.exec()

    def succes_message(self):
        """
        QMessageBox to let the user know that the export has been succesful.
        """
        value_message = QMessageBox()
        value_message.setWindowIcon(QIcon("Media\\window_icon\\success.png"))
        value_message.setWindowTitle("Exportación exitosa")
        value_message.setText("El archivo ha sido exportado exitosamente!")
        value_message.exec()
        
        
class ChangeExportPath(QDialog):
    """
    QDialog to change the export directory
    """
    def __init__(self):
        super().__init__()
        
        self.directory_path = main_window.export.path
        
        # Dialog config
        self.setWindowIcon(QIcon("Media\\window_icon\\folder.png"))
        self.setWindowTitle("Ruta de exportado")
        self.setFixedSize(300,150)
        layout = QGridLayout()
        
        # Dialog widgets
        self.path_label = QLabel("Ruta:")
        layout.addWidget(self.path_label, 1, 0, 1, 2)
        
        self.export_path = QLineEdit()
        self.export_path.setReadOnly(True)
        self.export_path.setText(self.directory_path)
        layout.addWidget(self.export_path, 2, 0, 1, 2)
        
        directory_button = QPushButton("Seleccionar ruta")
        directory_button.clicked.connect(self.select_path_dialog)
        layout.addWidget(directory_button, 3, 0, 1, 2)
        
        # Vertical spacing for buttons
        layout.addItem(QSpacerItem(20,20), 4, 0, 1, 2)
        
        yes_button = QPushButton("Aceptar")
        yes_button.clicked.connect(self.change_export_path)
        layout.addWidget(yes_button, 5, 0)
        
        no_button = QPushButton("Cancelar")
        no_button.clicked.connect(self.close)
        layout.addWidget(no_button, 5, 1)
        
        self.setLayout(layout)
        
    def select_path_dialog(self):
        """
        Opens a QFileDialog for the user to choose a directory to export.
        """
        self.directory_path = QFileDialog().getExistingDirectory()
        self.export_path.setText(self.directory_path)
        
    def change_export_path(self):
        """
        Exports the list of tickets in the main window table in the selected 
        type of file and directory.
        """
        main_window.export.change_export_path(self.export_path.text())
        self.close()
        self.succes_message()

    def succes_message(self):
        """
        QMessageBox to let the user know that the export path has been 
        succesfully changed.
        """
        value_message = QMessageBox()
        value_message.setWindowIcon(QIcon("Media\\window_icon\\success.png"))
        value_message.setWindowTitle("Modificación exitosa")
        value_message.setText("La ruta de exportado a cambiado a:\n"\
                              f"{self.export_path.text()}")
        value_message.exec()
        
if __name__ == "__main__":
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())