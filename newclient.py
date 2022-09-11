import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QStackedWidget, QDoubleSpinBox
from PyQt5.QtCore import Qt
from datetime import date, datetime
from encrypting import decryption, encryption

class NewClient(QDialog):
	def __init__(self):
		super(NewClient, self).__init__()
		loadUi("All_Windows/New_Client.ui", self)
		self.saveButton.clicked.connect(self.save)
		self.BackButton.clicked.connect(self.back)
		self.todayButton.clicked.connect(self.today)


	def get_vars_from_main_file(self, calculator, widget, app):
		self.calculator = calculator
		self.widget = widget
		self.app = app

	def save(self):
		name = self.lineEdit.text()
		date = self.lineEdit_2.text()
		credit = self.lineEdit_3.text()

		if len(name) < 3:
			msg = QMessageBox()
			msg.setText("Błędna nazwa klienta!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

		check_date = self.calculator.check_data(date, False)
		check_credit = self.calculator.check_data(credit)

		if check_date != 1:
			msg = QMessageBox()
			msg.setText("Błędna data! Upewnij się, że używasz dobrego formatu DD.MM.RRRR")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

		if check_credit != 1:
			msg = QMessageBox()
			msg.setText("Błędna kwota kredytu!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy napewno chcesz dodać klienta {name} ?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return

		decryption('MonthsBase/Customers.txt')
		f = open('MonthsBase/Customers.txt','a',encoding='utf-8')
		f.close()
		f = open('MonthsBase/Customers.txt','a',encoding='utf-8')
		f.write(f"{name},{date},{credit}\n")
		f.close()
		encryption('MonthsBase/Customers.txt')

		msg = QMessageBox()
		msg.setText(f"Klient {name} został zapisany w bazie klientów")
		x = msg.exec_()

		self.widget.setCurrentIndex(0)
		self.lineEdit.setText("")
		self.lineEdit_2.setText("")
		self.lineEdit_3.setText("")

	def today(self):
		today = (str(date.today())).split("-")
		today[0], today[1], today[2] = today[2], today[1], today[0]
		today = ".".join(today)
		self.lineEdit_2.setText(today)

	def back(self):
		self.lineEdit.setText("")
		self.lineEdit_2.setText("")
		self.lineEdit_3.setText("")
		self.widget.setCurrentIndex(0)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	new_client = NewClient() #4

	widget.addWidget(new_client)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()

