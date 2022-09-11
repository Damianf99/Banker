import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QStackedWidget, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt
from encrypting import decryption, encryption


class Customers(QDialog):
	def __init__(self):
		super(Customers, self).__init__()
		loadUi("All_Windows/Customers.ui", self)
		self.searched = False
		self.if_sorted = False
		self.commission_window = False
		self.entry_date = ''
		self.BackButton.clicked.connect(self.back)
		self.pushButton.clicked.connect(self.remove)
		self.pushButton_3.clicked.connect(self.search)
		self.pushButton_2.clicked.connect(self.finalize)
		self.pushButton_5.clicked.connect(self.count_commission)
		self.tableWidget.horizontalHeader().sectionClicked.connect(self.set_filters)

	def get_vars_from_main_file(self, mainwindow, calculator, commission_calculator, widget, app):
		self.mainwindow = mainwindow
		self.calculator = calculator
		self.commission_calculator = commission_calculator
		self.widget = widget
		self.app = app

	def set_filters(self, index):
		if self.tableWidget.horizontalHeaderItem(index).text() == "Nazwisko i Imie":
			return self.sorting()

	def get_data(self):
		decryption('MonthsBase/Customers.txt')
		f = open('MonthsBase/Customers.txt','r',encoding='utf-8')
		line = f.readline()
		month_data = []
		while line != '':
			month_data.append(line)
			line = f.readline()
		f.close()
		encryption('MonthsBase/Customers.txt')
		return month_data

	def remove(self, final = False):
		if final == False:
			to_remove = self.comboBox.currentText()
		else:
			to_remove = self.comboBox_2.currentText()
		to_remove = to_remove.split(" ")
		name = ""
		for n in range(len(to_remove) - 2):
			name += to_remove[n] + " "
		else:
			name += to_remove[n+1]
		date = to_remove[-1]
		date = date[1:-1]
		idx_to_remove = 99999
		month_data = self.get_data()
		for n in range(len(month_data)):
			month_data[n] = month_data[n].split(",")
			if name == month_data[n][0] and date == month_data[n][1]:
				idx_to_remove = n

		if idx_to_remove > len(month_data):
			msg = QMessageBox()
			msg.setText("Brak klienta w bazie!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

		if final == False:
			box = QMessageBox()
			box.setIcon(QMessageBox.Question)
			box.setWindowTitle('Kalkulator Bankowy')
			box.setText(f"Czy chcesz usunąć klienta {month_data[idx_to_remove][0]} ?")
			box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			buttonY = box.button(QMessageBox.Yes)
			buttonY.setText('Tak')
			buttonN = box.button(QMessageBox.No)
			buttonN.setText('Nie')
			box.exec_()
			if box.clickedButton() == buttonN:
				return

		temp_name = month_data[idx_to_remove][0]
		del month_data[idx_to_remove]

		for n in range(len(month_data)):
			month_data[n] = ",".join(month_data[n])

		decryption('MonthsBase/Customers.txt')
		f = open('MonthsBase/Customers.txt','w',encoding='utf-8')
		for n in range(len(month_data)):
			f.write(month_data[n])
		f.close()
		encryption('MonthsBase/Customers.txt')

		if final == False:
			msg = QMessageBox()
			msg.setText(f"Klient {temp_name} został usunięty")
			x = msg.exec_()
			self.mainwindow.to_customers()

	def search(self, sorted_search = False):
		entered_data = self.lineEdit_2.text()
		indexes = []
		if self.if_sorted == False:
			month_data = self.get_data()
		elif self.if_sorted == True and self.searched == True:
			month_data = self.get_data()
			month_data.sort()
			self.if_sorted = False
		else:
			month_data = self.get_data()
			month_data.sort()
		idx_to_del = []
		for n in range(len(month_data)):
			month_data[n] = month_data[n].split(",")
			if (month_data[n][0].lower()).find(entered_data.lower()) == -1:
				idx_to_del.append(n)
			else:
				indexes.append(n+1)
			month_data[n] = ",".join(month_data[n])
		it = 0
		for n in range(len(idx_to_del)):
			del month_data[idx_to_del[n] - it]
			it += 1
		if len(indexes) == 0:
			msg = QMessageBox()
			msg.setText("Nie można znaleźć takiej osoby w bazie!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		if sorted_search == True:
			return month_data, indexes
		self.searched = True
		self.mainwindow.to_customers(month_data, indexes)

	def sorting(self):
		if self.searched == False:
			month_data = self.get_data()
			indexes = []

			for n in range(len(month_data)):
				month_data[n] = month_data[n].split(",")

			month_data.sort()

			for n in range(len(month_data)):
				indexes.append(n+1)
				month_data[n] = ",".join(month_data[n])
		else:
			try:
				month_data, indexes = self.search(True)
			except:
				return
			for n in range(len(month_data)):
				month_data[n] = month_data[n].split(",")

			month_data.sort()

			for n in range(len(month_data)):
				indexes[n] = n+1
				month_data[n] = ",".join(month_data[n])
		self.if_sorted = True
		self.mainwindow.to_customers(month_data, indexes)

	def finalize(self):
		month_list = [self.mainwindow.January, self.mainwindow.February, self.mainwindow.March, self.mainwindow.April, self.mainwindow.May,
			   self.mainwindow.June, self.mainwindow.July, self.mainwindow.August, self.mainwindow.September, self.mainwindow.October,
			  self.mainwindow.November, self.mainwindow.December]
		credit = ""
		person = self.comboBox_2.currentText()
		person = person.split(" ")
		name = ""
		for n in range(len(person) - 2):
			name += person[n] + " "
		else:
			name += person[n+1]
		date = person[-1]
		date = date[1:-1]
		custom_data = self.get_data()
		check_name = False
		for n in range(len(custom_data)):
			custom_data[n] = custom_data[n].split(",")
			if custom_data[n][0] == name:
				check_name = True
				break
		if check_name == False:
			msg = QMessageBox()
			msg.setText("Nie można znaleźć takiej osoby w bazie!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		self.entry_date, okPressed = QInputDialog.getText(self, "Kalkulator Bankowy", f"Aby sfinalizować klienta {name} podaj date finalizacji:", QLineEdit.Normal, "")
		if okPressed and self.entry_date != '':
			check_date = self.calculator.check_data(self.entry_date, False)
			if check_date == 0:
				msg = QMessageBox()
				msg.setText("Niepoprawna data! Upewnij się, że używasz format DD.MM.RRRR")
				msg.setIcon(QMessageBox.Critical)
				x = msg.exec_()
				return
			self.entry_date = self.entry_date.split(".")
			self.mainwindow.month = int(self.entry_date[1])
			self.entry_date = ".".join(self.entry_date)
			for n in range(len(custom_data)):
				if name == custom_data[n][0] and date == custom_data[n][1]:
					credit = custom_data[n][2]
					credit = credit[:-1]
			self.calculator.lineEdit.setText(name)
			self.calculator.lineEdit_2.setText(date)
			self.calculator.lineEdit_3.setText(credit)
			month_list[self.mainwindow.month-1](True)

	def count_commission(self):
		month_data = self.get_data()
		person = self.comboBox_3.currentText()
		if person == "Wybierz z listy...":
			return
		person = person.split("(")
		person[0] = person[0][:-1]
		person[1] = person[1][:-1]
		person = ",".join(person)
		idx = -1
		for i in range(len(month_data)):
			if month_data[i].find(person) != -1:
				idx = i
				break
		credit_amount = month_data[idx].split(",")[-1][:-1]
		self.commission_calculator.lineEdit_2.setText(f"{credit_amount}")
		self.commission_calculator.setData()
		self.commission_calculator.label_10.setText(f"Klient:\n{month_data[idx].split(',')[0]}")
		self.lineEdit_2.setText("")
		self.widget.setCurrentIndex(7)
		self.commission_window = True

	def back(self):
		self.lineEdit_2.setText("")
		self.if_sorted = False
		self.widget.setCurrentIndex(1)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	customers = Customers() #5

	widget.addWidget(customers)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()

