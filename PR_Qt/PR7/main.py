import sys
import os
import mysql.connector as mc
from PyQt5 import uic, QtWidgets

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(current_dir, 'main1.ui')
        uic.loadUi(ui_file_path, self)
        self.connect.clicked.connect(self.connect_to_db)
        self.databases.currentIndexChanged.connect(self.show_tables)
        self.tables.currentIndexChanged.connect(self.show_info)
        self.select.clicked.connect(self.select_query)
        self.insert.clicked.connect(self.add_value)

    def add_value(self):
        array = []
        try:
            with mc.connect(
                    host="localhost",
                    user="roman",
                    password="...",
                    database=f'{self.databases.currentText()}'
            ) as connection:
                insert_query = str(self.query.toPlainText())
                select_query = f'select * from {self.tables.currentText()}'
                with connection.cursor() as cursor:
                    cursor.execute(insert_query)
                    connection.commit()
                    cursor.execute(select_query)
                    self.result_query.setRowCount(0)
                    for lineIndex, lineData in enumerate(cursor):
                        if lineIndex == 0:
                            self.result_query.setColumnCount(len(lineData))
                            self.result_query.insertRow(lineIndex)
                        for columnIndex, columnData in enumerate(lineData):
                            self.result_query.setItem(lineIndex, columnIndex,
                                                      QtWidgets.QTableWidgetItem(str(columnData)))
                            if cursor.description[columnIndex][0] not in array:
                                array.append(cursor.description[columnIndex][0])
                    self.result_query.setHorizontalHeaderLabels(array)
        except mc.Error as e:
            print(e)

    def select_query(self):
        array = []
        try:
            with mc.connect(
                    host="localhost",
                    user="roman",
                    password="...",
                    database=f'{self.databases.currentText()}'
            ) as connection:
                query = str(self.query.toPlainText())
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    self.result_query.setRowCount(0)
                    for lineIndex, lineData in enumerate(cursor):
                        if lineIndex == 0:
                            self.result_query.setColumnCount(len(lineData))
                            self.result_query.insertRow(lineIndex)
                        for columnIndex, columnData in enumerate(lineData):
                            self.result_query.setItem(lineIndex, columnIndex,
                                                      QtWidgets.QTableWidgetItem(str(columnData)))
                            if cursor.description[columnIndex][0] not in array:
                                array.append(cursor.description[columnIndex][0])
                    self.result_query.setHorizontalHeaderLabels(array)
        except mc.Error as e:
            print(e)

    def show_info(self):
        array = []
        try:
            with mc.connect(
                    host="localhost",
                    user="roman",
                    password="...",
                    database=f'{self.databases.currentText()}'
            ) as connection:
                show_info_query = f"select * from {self.tables.currentText()} limit 10;"
                with connection.cursor() as cursor:
                    cursor.execute(show_info_query)
                    self.table_info.setRowCount(0)
                    for lineIndex, lineData in enumerate(cursor):
                        if lineIndex == 0:
                            self.table_info.setColumnCount(len(lineData))
                            self.table_info.insertRow(lineIndex)
                        for columnIndex, columnData in enumerate(lineData):
                            self.table_info.setItem(lineIndex, columnIndex,
                                                     QtWidgets.QTableWidgetItem(str(columnData)))
                            if cursor.description[columnIndex][0] not in array:
                                array.append(cursor.description[columnIndex][0])
                    self.table_info.setHorizontalHeaderLabels(array)
        except mc.Error as e:
            print(e)

    def show_tables(self):
        try:
            with mc.connect(
                    host="localhost",
                    user="roman",
                    password="...",
                    database=f'{self.databases.currentText()}'
            ) as connection:
                show_tables_query = "show tables;"
                with connection.cursor() as cursor:
                    cursor.execute(show_tables_query)
                    self.tables.clear()
                    for table in cursor:
                        self.tables.addItem(str(table[0]))
        except mc.Error as e:
            print(e)

    def connect_to_db(self):
        try:
            with mc.connect(
                    host="localhost",
                    user="roman",
                    password="..."
            ) as connection:
                show_db_query = "show databases;"
                with connection.cursor() as cursor:
                    cursor.execute(show_db_query)
                    self.databases.clear()
                    for db in cursor:
                        self.databases.addItem(str(db[0]))
        except mc.Error as e:
            print(e)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
