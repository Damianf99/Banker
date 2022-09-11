import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QWidget, QMessageBox, QHeaderView, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt
from encrypting import decryption, encryption


class Database(QDialog):
	def __init__(self):
		super(Database, self).__init__()
		loadUi("All_Windows/Month_database.ui", self)
		self.name_sort = 0
		self.searched = 0
		self.sorted_ascending = 0
		self.check_boxes = []
		self.check_states = []
		self.current_data = []
		self.sort_data = []
		self.checkBox.clicked.connect(self.change_all_states)
		self.BackButton.clicked.connect(self.back)
		self.pushButton.clicked.connect(self.remove)
		self.pushButton_3.clicked.connect(self.search)
		self.saveToInvoiceButton.clicked.connect(self.save_to_invoice)
		self.bankComboBox.activated.connect(lambda x: self.calculator.next(combo=True))
		self.tableWidget.horizontalHeader().sectionClicked.connect(self.set_filters)

	def get_vars_from_main_file(self, calculator, invoices, widget, app, mainwindow, start):
		self.calculator = calculator
		self.invoices = invoices
		self.widget = widget
		self.app = app
		self.mainwindow = mainwindow
		self.start = start

	def set_filters(self, index):
		if self.tableWidget.horizontalHeaderItem(index).text() == "Data wprowadzenia":
			return self.sort_by_date()
		if self.tableWidget.horizontalHeaderItem(index).text() == "Nazwisko i Imie":
			return self.sort_by_name()

	def change_all_states(self):
		if self.checkBox.isChecked():
			for n in range(len(self.check_states)):
				self.check_states[n].setChecked(True)
		else:
			for n in range(len(self.check_states)):
				self.check_states[n].setChecked(False)

	def save_to_invoice(self):
		if self.calculator.full_base == 1:
			msg = QMessageBox()
			msg.setText("Nie można dodawać do faktury z listy przeznaczonej wyłącznie do podglądu!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy napewno chcesz dodać zaznaczonych klientów do faktury?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		already_in_list = False
		for n in range(len(self.check_states)):
			if self.check_states[n].isChecked() == True:
				temp_person = [self.tableWidget.item(n, i).text() for i in range(1,8)]
				if temp_person not in self.invoices.invoice_list:
					self.invoices.invoice_list.append(temp_person)
				else:
					already_in_list = True
		if already_in_list:
			msg = QMessageBox()
			msg.setText(f"Niektórzy klienci znajdowali się już na fakturze. Pozostali zostali dodani poprawnie")
			x = msg.exec_()
		else:
			msg = QMessageBox()
			msg.setText(f"Wszyscy klienci zostali poprawnie dodani do faktury")
			x = msg.exec_()

	def back(self):
		self.checkBox.setChecked(False)
		self.lineEdit_2.setText("")
		self.searched = 0
		self.sorted_ascending = 0
		self.widget.setCurrentIndex(1)

	def check_data(self, var):
		numbers = ["1","2","3","4","5","6","7","8","9","0"]
		check = 0
		for n in range(len(var)):
			if var[n] in numbers:
				check = 1
			else:
				check = 0
				break
		return check

	def remove(self):
		if self.calculator.full_base == 1:
			msg = QMessageBox()
			msg.setText("Nie można usuwać z listy przeznaczonej wyłącznie do podglądu!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		to_remove = self.comboBox.currentText()
		decryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))
		f = open('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year),'r',encoding='utf-8')
		line = f.readline()
		month_data = []
		while line != '':
			month_data.append(line)
			line = f.readline()
		f.close()
		encryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))

		to_remove = to_remove.split(" ")
		name = ""
		for n in range(len(to_remove) - 2):
			name += to_remove[n] + " "
		else:
			name += to_remove[n+1]
		date = to_remove[-1]
		date = date[1:-1]
		idx_to_remove = 99999
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

		decryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))
		f = open('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year),'w',encoding='utf-8')
		for n in range(len(month_data)):
			f.write(month_data[n])
		f.close()
		encryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))

		msg = QMessageBox()
		msg.setText(f"Klient {temp_name} został usunięty")
		x = msg.exec_()

		self.lineEdit_2.setText("")
		self.widget.setCurrentIndex(1)

	def sort_by_name(self):
		self.sort_by_date(True)

	def sort_by_date(self, name_sort = False):
		indexes = None
		if self.searched == 0:
			if len(self.sort_data) != 0: 
				month_data = self.sort_data.copy()
			else:
				month_data = self.current_data.copy()
		else:
			try:
				month_data, indexes = self.search(True)
			except:
				return

		if name_sort == False:
			lista = []
			temp = []
			result = []
			for n in range(len(month_data)):
				lista.append([month_data[n][1], n])

			for n in range(len(lista)):
				lista[n][0] = lista[n][0].split(".")

			years = [int(lista[j][0][2]) for j in range(len(lista))]
			years = sorted(list(set(years)))

			for k in range(len(years)):
				for i in range(1,13):
					for j in range(len(lista)):
						if int(lista[j][0][1]) == i and int(lista[j][0][2]) == years[k]:
							temp.append([lista[j][0], lista[j][1]])
					if len(temp) != 0:
						temp.sort()
						result.append(temp[:])
						temp.clear()

			for i in range(len(result)):
				for j in range(len(result[i])):
					temp.append([".".join(result[i][j][0]),result[i][j][1]])

			if self.sorted_ascending == 0:
				self.sorted_ascending = 1
			elif self.sorted_ascending == 1:
				temp = temp[::-1]
				self.sorted_ascending = 0

			if self.searched == 1:
				self.calculator.next(month_data, indexes, temp)
				return
		
		if name_sort == True:
			for n in range(len(month_data)):
				if indexes != None:
					month_data[n].append(indexes[n])
				else:
					month_data[n].append(n+1)

			month_data.sort()
			if self.sorted_ascending == 0:
				self.sorted_ascending = 1
			elif self.sorted_ascending == 1:
				month_data = month_data[::-1]
				self.sorted_ascending = 0

		self.tableWidget.setColumnCount(8)
		self.tableWidget.setHorizontalHeaderLabels(['','Nazwisko i Imie','Data wprowadzenia', 'Data sfinalizowania','Kwota Kredytu','Wynagrodzenie','Bank','Prowizje'])
		header = self.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

		self.check_states.clear()
		self.check_boxes.clear()
		self.comboBox.clear()
		self.comboBox.addItem("Wybierz z listy...")
		for n in range(len(month_data)):
			self.comboBox.addItem(f"{month_data[n][0]} ({month_data[n][1]})")

		for n in range(len(month_data)):
			Widget = QWidget()
			self.CheckBox = QCheckBox()
			self.check_states.append(self.CheckBox)
			Layout = QHBoxLayout(Widget)
			Layout.addWidget(self.CheckBox)
			Layout.setAlignment(Qt.AlignCenter)
			Layout.setContentsMargins(0,0,0,0)
			Widget.setLayout(Layout)
			self.check_boxes.append(Widget)

		for i in range(len(month_data)):
			if name_sort == False:
				self.tableWidget.setCellWidget(i, 0, self.check_boxes[temp[i][1]])
				self.tableWidget.setItem(i, 0, QTableWidgetItem(""))
				self.tableWidget.setItem(i, 1, QTableWidgetItem(str(month_data[temp[i][1]][0])))
				self.tableWidget.setItem(i, 2, QTableWidgetItem(str(month_data[temp[i][1]][1])))
				self.tableWidget.setItem(i, 3, QTableWidgetItem(str(month_data[temp[i][1]][5])))
				self.tableWidget.setItem(i, 4, QTableWidgetItem(str(month_data[temp[i][1]][2])))
				self.tableWidget.setItem(i, 5, QTableWidgetItem(str(month_data[temp[i][1]][3])))
				self.tableWidget.setItem(i, 6, QTableWidgetItem(str(month_data[temp[i][1]][4])))
				self.tableWidget.setItem(i, 7, QTableWidgetItem(str(month_data[temp[i][1]][6])))
				self.tableWidget.setItem(i, 8, QTableWidgetItem(str(temp[i][1] + 1)))
			else:
				self.tableWidget.setCellWidget(i, 0, self.check_boxes[i])
				self.tableWidget.setItem(i, 0, QTableWidgetItem(""))
				self.tableWidget.setItem(i, 1, QTableWidgetItem(str(month_data[i][0])))
				self.tableWidget.setItem(i, 2, QTableWidgetItem(str(month_data[i][1])))
				self.tableWidget.setItem(i, 3, QTableWidgetItem(str(month_data[i][5])))
				self.tableWidget.setItem(i, 4, QTableWidgetItem(str(month_data[i][2])))
				self.tableWidget.setItem(i, 5, QTableWidgetItem(str(month_data[i][3])))
				self.tableWidget.setItem(i, 6, QTableWidgetItem(str(month_data[i][4])))
				self.tableWidget.setItem(i, 7, QTableWidgetItem(str(month_data[i][6])))
				self.tableWidget.setItem(i, 8, QTableWidgetItem(str(month_data[i][7])))

	def search(self, if_sorted = False):
		entered_data = self.lineEdit_2.text()
		month_data = self.current_data.copy()
		indexes = []
		idx_to_del = []
		for n in range(len(month_data)):
			if (month_data[n][0].lower()).find(entered_data.lower()) == -1:
				idx_to_del.append(n)
			else:
				indexes.append(n+1)
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
		if if_sorted == True:
			return month_data, indexes
		self.searched = 1
		self.calculator.next(month_data, indexes)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	database = Database() #3

	widget.addWidget(database)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()


