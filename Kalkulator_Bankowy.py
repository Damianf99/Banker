import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt
from start import Start
from mainwindow import MainWindow
from calculator import Calculator
from database import Database
from newclient import NewClient
from customers import Customers
from commissions import Commissions
from commissions_calculator import CommissionsCalculator
from invoices import Invoices
from invoices_data import InvoicesData
from login import Login
from create_account import CreateAccount

def main():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    start = Start() #0
    mainwindow = MainWindow() #1
    calculator = Calculator() #2
    database = Database() #3
    new_client = NewClient() #4
    customers = Customers() #5
    commissions = Commissions() #6
    commission_calculator = CommissionsCalculator() #7
    invoices = Invoices() #8
    invoices_data = InvoicesData() #9
    login = Login() #10
    create_account = CreateAccount() #11

    start.get_vars_from_main_file(mainwindow, new_client, commissions, commission_calculator, invoices, login, widget, app)
    mainwindow.get_vars_from_main_file(calculator, customers, widget, app)
    calculator.get_vars_from_main_file(database, customers, invoices_data, widget, app, mainwindow, start)
    database.get_vars_from_main_file(calculator, invoices, widget, app, mainwindow, start)
    new_client.get_vars_from_main_file(calculator, widget, app)
    customers.get_vars_from_main_file(mainwindow, calculator, commission_calculator, widget, app)
    commissions.get_vars_from_main_file(widget, app)
    commission_calculator.get_vars_from_main_file(customers, calculator, commissions, widget, app)
    invoices.get_vars_from_main_file(start, invoices_data, widget, app)
    invoices_data.get_vars_from_main_file(invoices, widget, app)
    login.get_vars_from_main_file(start, widget, app)
    create_account.get_vars_from_main_file(widget, app)

    widget.addWidget(start)
    widget.addWidget(mainwindow)
    widget.addWidget(calculator)
    widget.addWidget(database)
    widget.addWidget(new_client)
    widget.addWidget(customers)
    widget.addWidget(commissions)
    widget.addWidget(commission_calculator)
    widget.addWidget(invoices)
    widget.addWidget(invoices_data)
    widget.addWidget(login)
    widget.addWidget(create_account)

    #widget.setCurrentIndex(10)
    widget.setFixedWidth(800)
    widget.setFixedHeight(550)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        pass

if __name__ == "__main__":
	main()


