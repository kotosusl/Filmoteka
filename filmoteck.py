from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtSql import QSqlQuery, QSqlTableModel, QSqlDatabase
import sys
import os
import sqlite3

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

FLAG = False

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(489, 402)
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 50, 471, 331))
        self.tableView.setObjectName("tableView")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(3)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))


class AddFrom(QMainWindow):
    def setupUi(self, MainWindow):
        super(AddFrom, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(325, 175)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(10, 10, 51, 18))
        self.label_name.setObjectName("label_name")
        self.label_year = QtWidgets.QLabel(self.centralwidget)
        self.label_year.setGeometry(QtCore.QRect(10, 40, 66, 18))
        self.label_year.setObjectName("label_year")
        self.label_genre = QtWidgets.QLabel(self.centralwidget)
        self.label_genre.setGeometry(QtCore.QRect(10, 80, 35, 12))
        self.label_genre.setObjectName("label_genre")
        self.label_duration = QtWidgets.QLabel(self.centralwidget)
        self.label_duration.setGeometry(QtCore.QRect(10, 110, 35, 12))
        self.label_duration.setObjectName("label_duration")
        self.add = QtWidgets.QPushButton(self.centralwidget)
        self.add.setGeometry(QtCore.QRect(210, 130, 91, 21))
        self.add.setObjectName("add")
        self.error = QtWidgets.QLabel(self.centralwidget)
        self.error.setGeometry(QtCore.QRect(10, 130, 191, 21))
        self.error.setText("")
        self.error.setObjectName("error")
        self.name = QtWidgets.QTextEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(80, 10, 231, 24))
        self.name.setObjectName("name")
        self.year = QtWidgets.QTextEdit(self.centralwidget)
        self.year.setGeometry(QtCore.QRect(80, 40, 231, 24))
        self.year.setObjectName("year")
        self.duration = QtWidgets.QTextEdit(self.centralwidget)
        self.duration.setGeometry(QtCore.QRect(80, 100, 231, 24))
        self.duration.setObjectName("duration")
        self.genre = QtWidgets.QComboBox(self.centralwidget)
        self.genre.setGeometry(QtCore.QRect(80, 72, 231, 20))
        self.genre.setObjectName("genre")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить элемент"))
        self.label_name.setText(_translate("MainWindow", "Название"))
        self.label_year.setText(_translate("MainWindow", "Год выпуска"))
        self.label_genre.setText(_translate("MainWindow", "Жанр"))
        self.label_duration.setText(_translate("MainWindow", "Длина"))
        self.add.setText(_translate("MainWindow", "Добавить"))


class Filmotecka(Ui_MainWindow):
    def __init__(self):
        super(Filmotecka, self).setupUi(self)
        self.setFixedSize(489, 402)
        self.setWindowTitle('Фильмотека')
        if os.path.isfile('films_db.sqlite'):
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName('films_db.sqlite')
        else:
            app = QApplication(sys.argv)
            bad_exit = DatabaseNotFound()
            bad_exit.show()
            sys.exit(app.exec_())

        self.model = QSqlTableModel(self)
        self.model.select()

        self.update_table()

        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.pushButton.clicked.connect(self.adding)

    def adding(self):
        global FLAG
        if not FLAG:
            self.form = AddFilm()
            self.form.show()
            FLAG = True
            self.update_table()

    def update_table(self):
        sql = QSqlQuery('''select films.id as "ID", films.title as "Название", films.year as "Год выпуска", 
                genres.title as "Жанр", films.duration as "Продолжительность" from films 
                join genres on genres.id = films.genre''', self.db)
        self.model.setQuery(sql)


class AddFilm(AddFrom):
    def __init__(self):
        super(AddFilm, self).setupUi(self)
        self.setFixedSize(325, 175)
        con = sqlite3.connect('films_db.sqlite')
        self.cur = con.cursor()
        self.genre.addItems([p[0] for p in self.cur.execute('''select title from genres''').fetchall()])
        self.add.clicked.connect(self.adding)

    def adding(self):
        if self.name.toPlainText() and self.year.toPlainText().isdigit() and self.duration.toPlainText().isdigit():
            self.add_table = QSqlQuery()
            self.add_table.exec(f'''INSERT INTO films(title, year, genre, duration) 
            VALUES ("{self.name.toPlainText()}", {self.year.toPlainText()}, 
            (select id from genres where title = "{self.genre.currentText()}"), {self.duration.toPlainText()})''')
            self.close()
        else:
            self.error.setText('Неверно заполнена форма')

    def closeEvent(self, event) -> None:
        global FLAG
        FLAG = False
        global form
        form.update_table()




class DatabaseNotFound(QMainWindow, QWidget):
    def __init__(self):
        super(DatabaseNotFound, self).__init__()
        # Создание окна ошибки
        self.setGeometry(500, 500, 250, 50)
        self.setWindowTitle('Ошибка!')
        self.error_layout = QVBoxLayout()
        self.error_label = QLabel('База данных не найдена!', self)
        self.error_label.resize(self.sizeHint())
        self.error_layout.addWidget(self.error_label)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.error_layout)
        self.setCentralWidget(self.centralWidget)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:  # Закрытие окна
        app.quit()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    form = Filmotecka()
    form.show()
    sys.exit(app.exec())