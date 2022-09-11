import sys, os
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QWidget, QMessageBox, QStackedWidget, QHeaderView, QInputDialog, QLineEdit, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt
from encrypting import decryption, encryption


class Calculator(QDialog):
	def __init__(self):
		super(Calculator, self).__init__()
		loadUi("All_Windows/New_calc_window.ui", self)
		self.full_base = 0
		self.nextButton.clicked.connect(self.next)
		self.Inny.clicked.connect(self.inny)
		self.chooseOfferButton.clicked.connect(self.finalize_offer)
		self.BackButton.clicked.connect(self.back)
		self.comboBox.currentIndexChanged.connect(self.load_bank_offers)
		self.current_banks_name = ""
		self.bank_data = []
		self.setData()

	def get_vars_from_main_file(self, database, customers, invoices_data, widget, app, mainwindow, start):
		self.database = database
		self.customers = customers
		self.invoices_data = invoices_data
		self.widget = widget
		self.app = app
		self.mainwindow = mainwindow
		self.start = start


	def save_data(self, name_, date_, credit_, pay_, bank_, provision_):
		decryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))
		f = open('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year),'a',encoding='utf-8')
		f.write("{name},{date},{credit},{pay},{bank},{entry},{provision}\n".format(name = name_, date = date_, credit = credit_, pay = pay_, bank = bank_, entry = self.customers.entry_date, provision = provision_))
		f.close()
		encryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))
		self.customers.remove(True)

	def check_data(self, var, switch = True):
		numbers = ["1","2","3","4","5","6","7","8","9","0","."]
		check = 0
		if switch == False:
			if len(var) != 10:
				return check
			if var[2] != '.' and var[5] != '.':
				return check
			var = var.split(".")
			if int(var[0]) > 31 or int(var[0]) < 1:
				return check
			if int(var[1]) > 12 or int(var[1]) < 1:
				return check
			var = ".".join(var)
		for n in range(len(var)):
			if var[n] in numbers:
				check = 1
			else:
				check = 0
				break
		return check

	def calculate(self, datas, credit):
		outcome = float(datas)/100 * float(credit)
		outcome = round(outcome,2)
		result = str(outcome).split(".")
		if len(result[1]) < 2:
				result[1] += "0"
		result = ".".join(result)
		return result

	def back(self):
		self.label_32.setText("")
		self.lineEdit.setText("")
		self.lineEdit_2.setText("")
		self.lineEdit_3.setText("")
		self.widget.setCurrentIndex(1)

	def next(self, month_data = None, indexes = None, temp = None, combo = None):
		if_searched = False
		if month_data == False or month_data == None:
			if self.full_base == 0:
				decryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))
				f = open('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year),'r',encoding='utf-8')
				line = f.readline()
				month_data = []
				while line != '':
					month_data.append(line.replace('\n', ''))
					line = f.readline()
				f.close()
				encryption('MonthsBase/{c_y}/{m}.txt'.format(m = self.mainwindow.month, c_y = self.start.current_year))
			elif self.full_base == 1:
				month_data = []
				for n in range(1,13):
					decryption('MonthsBase/{c_y}/{m}.txt'.format(m = n, c_y = self.start.current_year))
					f = open('MonthsBase/{c_y}/{m}.txt'.format(m = n, c_y = self.start.current_year),'r',encoding='utf-8')
					line = f.readline()
					while line != '':
						month_data.append(line.replace('\n', ''))
						line = f.readline()
					f.close()
					encryption('MonthsBase/{c_y}/{m}.txt'.format(m = n, c_y = self.start.current_year))
			for n in range(len(month_data)):
				month_data[n] = month_data[n].split(",")
			if len(month_data) != 0:
				self.database.tableWidget.setColumnCount(len(month_data[0]))
			self.database.current_data = month_data.copy()
		else:
			if_searched = True
			self.database.tableWidget.setColumnCount(len(month_data[0]))

		if len(month_data) == 0:
			msg = QMessageBox()
			msg.setText("Baza danych jest pusta!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

		if combo == True and self.database.bankComboBox.currentText() != "Wybierz z listy...":
			month_data = [month_data[i] for i in range(len(month_data)) if month_data[i][4] == self.database.bankComboBox.currentText()]
		if combo == True:
			self.database.sort_data = month_data.copy()

		self.database.tableWidget.setColumnCount(8)
		self.database.tableWidget.setHorizontalHeaderLabels(['','Nazwisko i Imie','Data wprowadzenia', 'Data sfinalizowania','Kwota Kredytu','Wynagrodzenie','Bank','Prowizje'])
		self.database.tableWidget.setRowCount(len(month_data))
		header = self.database.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

		self.database.check_states.clear()
		self.database.check_boxes.clear()
		self.database.comboBox.clear()
		if combo != True:
			self.database.bankComboBox.clear()
			self.database.bankComboBox.addItem("Wybierz z listy...")
		self.database.comboBox.addItem("Wybierz z listy...")
		for n in range(len(month_data)):
			self.database.comboBox.addItem(f"{month_data[n][0]} ({month_data[n][1]})")

		for n in range(len(month_data)):
			Widget = QWidget()
			self.CheckBox = QCheckBox()
			self.database.check_states.append(self.CheckBox)
			Layout = QHBoxLayout(Widget)
			Layout.addWidget(self.CheckBox)
			Layout.setAlignment(Qt.AlignCenter)
			Layout.setContentsMargins(0,0,0,0)
			Widget.setLayout(Layout)
			self.database.check_boxes.append(Widget)

		bank_names = []
		for i in range(len(month_data)):
			if month_data[i][4] not in bank_names and combo != True:
				bank_names.append(str(month_data[i][4]))
			if temp == None:
				self.database.tableWidget.setCellWidget(i, 0, self.database.check_boxes[i])
				self.database.tableWidget.setItem(i, 0, QTableWidgetItem(""))
				self.database.tableWidget.setItem(i, 1, QTableWidgetItem(str(month_data[i][0])))
				self.database.tableWidget.setItem(i, 2, QTableWidgetItem(str(month_data[i][1])))
				self.database.tableWidget.setItem(i, 3, QTableWidgetItem(str(month_data[i][5])))
				self.database.tableWidget.setItem(i, 4, QTableWidgetItem(str(month_data[i][2])))
				self.database.tableWidget.setItem(i, 5, QTableWidgetItem(str(month_data[i][3])))
				self.database.tableWidget.setItem(i, 6, QTableWidgetItem(str(month_data[i][4])))
				self.database.tableWidget.setItem(i, 7, QTableWidgetItem(str(month_data[i][6])))
			else:
				self.database.tableWidget.setCellWidget(i, 0, self.database.check_boxes[temp[i][1]])
				self.database.tableWidget.setItem(i, 0, QTableWidgetItem(""))
				self.database.tableWidget.setItem(i, 1, QTableWidgetItem(str(month_data[temp[i][1]][0])))
				self.database.tableWidget.setItem(i, 2, QTableWidgetItem(str(month_data[temp[i][1]][1])))
				self.database.tableWidget.setItem(i, 3, QTableWidgetItem(str(month_data[temp[i][1]][5])))
				self.database.tableWidget.setItem(i, 4, QTableWidgetItem(str(month_data[temp[i][1]][2])))
				self.database.tableWidget.setItem(i, 5, QTableWidgetItem(str(month_data[temp[i][1]][3])))
				self.database.tableWidget.setItem(i, 6, QTableWidgetItem(str(month_data[temp[i][1]][4])))
				self.database.tableWidget.setItem(i, 7, QTableWidgetItem(str(month_data[temp[i][1]][6])))
			if if_searched == True:
				if temp == None:
					self.database.tableWidget.setItem(i, 8, QTableWidgetItem(str(indexes[i])))
				else:
					self.database.tableWidget.setItem(i, 8, QTableWidgetItem(str(indexes[temp[i][1]])))
		for i in range(len(bank_names)):
			self.database.bankComboBox.addItem(bank_names[i])
		self.label_32.setText("")
		self.lineEdit.setText("")
		self.lineEdit_2.setText("")
		self.lineEdit_3.setText("")
		total_credit = 0
		total_result = 0
		for i in range(len(month_data)):
			total_credit += float(month_data[i][2])
			total_result += float(month_data[i][3])
		total_credit = round(total_credit, 2)
		total_result = round(total_result, 2)
		if self.full_base == 0:
			months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
			self.database.label.setText(months[self.mainwindow.month-1])
		else:
			self.database.label.setText("Razem")

		total_credit = str(total_credit).split(".")
		if len(total_credit[1]) < 2:
			total_credit[1] += "0"
		if len(total_credit[0]) > 3:
			total_credit[0] = list(total_credit[0])
			total_credit[0][-4] += " "
			total_credit[0] = "".join(total_credit[0])
		if len(total_credit[0]) > 7:
			total_credit[0] = list(total_credit[0])
			total_credit[0][-8] += " "
			total_credit[0] = "".join(total_credit[0])
		total_credit = ".".join(total_credit)

		total_result = str(total_result).split(".")
		if len(total_result[1]) < 2:
			total_result[1] += "0"
		if len(total_result[0]) > 3:
			total_result[0] = list(total_result[0])
			total_result[0][-4] += " "
			total_result[0] = "".join(total_result[0])
		if len(total_result[0]) > 7:
			total_result[0] = list(total_result[0])
			total_result[0][-8] += " "
			total_result[0] = "".join(total_result[0])
		total_result = ".".join(total_result)

		self.database.label_4.setText(str(total_credit))
		self.database.label_5.setText(str(total_result))
		self.widget.setCurrentIndex(3)

	def setData(self):
		items = os.listdir(f"MonthsBase/Banks")
		items = [item[:-4] for item in items]
		self.comboBox.clear()
		self.comboBox.addItem("Wybierz z listy...")
		for n in range(len(items)):
			self.comboBox.addItem(f"{items[n]}")

	def load_bank_offers(self):
		self.current_banks_name = self.comboBox.currentText()
		self.bank_data.clear()
		self.offerComboBox.clear()
		self.offerComboBox.addItem("Wybierz z listy...")
		if self.current_banks_name == "Wybierz z listy..." or len(self.current_banks_name) == 0:
			self.current_banks_name = ""
			return
		decryption(f'MonthsBase/Banks/{self.current_banks_name}.txt')
		with open(f'MonthsBase/Banks/{self.current_banks_name}.txt', 'r',encoding='utf-8') as f:
			line = f.readline()
			while line != '':
				self.bank_data.append((line.replace('\n', '')).split("~`"))
				line = f.readline()
		encryption(f'MonthsBase/Banks/{self.current_banks_name}.txt')
		for n in range(len(self.bank_data)):
			self.offerComboBox.addItem(f"{self.bank_data[n][0]}")

	def finalize_offer(self):
		name = self.lineEdit.text()
		date = self.lineEdit_2.text()
		credit = self.lineEdit_3.text()
		offer_name = self.offerComboBox.currentText()
		if offer_name == "Wybierz z listy...":
			return
		offers = [offer[0] for offer in self.bank_data]
		check_date = self.check_data(date, False)
		check = self.check_data(credit)
		if check_date == 0:
			self.label_32.setText("Podano nieprawidłową datę!")
			return
		if check == 1:
			box = QMessageBox()
			box.setIcon(QMessageBox.Question)
			box.setWindowTitle('Kalkulator Bankowy')
			box.setText(f"Czy napewno chcesz dodać klienta {name} sfinalizowanego w banku {self.current_banks_name} z ofertą {offer_name}?")
			box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			buttonY = box.button(QMessageBox.Yes)
			buttonY.setText('Tak')
			buttonN = box.button(QMessageBox.No)
			buttonN.setText('Nie')
			box.exec_()
			if box.clickedButton() == buttonN:
				return
			result = self.calculate(self.bank_data[offers.index(offer_name)][1], credit)
			commission = self.invoices_data.separate_numbers(self.bank_data[offers.index(offer_name)][1])
			self.save_data(name, date, credit, result, self.current_banks_name, commission)
			self.next()
		else:
			self.label_32.setText("Podano nieprawidłową kwotę kredytu!")
			return

	def inny(self):
		name = self.lineEdit.text()
		date = self.lineEdit_2.text()
		credit = self.lineEdit_3.text()
		check_date = self.check_data(date, False)
		check = self.check_data(credit)
		if check_date == 0:
			self.label_32.setText("Podano nieprawidłową datę!")
			return
		if check == 1:
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
			commision, okPressed = QInputDialog.getText(self, "Kalkulator Bankowy", "Wprowadź wartość prowizji (np. 1.23):", QLineEdit.Normal, "")
			if okPressed and commision != '':
				check_credit = self.check_data(commision)
				if check_credit == 0:
					msg = QMessageBox()
					msg.setText("Niepoprawny format liczb! Czy napewno używasz kropki zamiast przecinka? np. 1.23")
					msg.setIcon(QMessageBox.Critical)
					x = msg.exec_()
					return
			if len(commision) == 0:
				msg = QMessageBox()
				msg.setText("Brak prowizji!")
				msg.setIcon(QMessageBox.Critical)
				x = msg.exec_()
				return
			bank_name, okPressed = QInputDialog.getText(self, "Kalkulator Bankowy", "Wprowadź nazwę banku:", QLineEdit.Normal, "")
			if okPressed and bank_name != '':
				box = QMessageBox()
				box.setIcon(QMessageBox.Question)
				box.setWindowTitle('Kalkulator Bankowy')
				box.setText(f"Czy napewno chcesz dodać klienta {name} sfinalizowanego w banku {bank_name}?")
				box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
				buttonY = box.button(QMessageBox.Yes)
				buttonY.setText('Tak')
				buttonN = box.button(QMessageBox.No)
				buttonN.setText('Nie')
				box.exec_()
				if box.clickedButton() == buttonN:
					return
				result = self.calculate(commision, credit)
				commision = self.invoices_data.separate_numbers(commision)
				self.save_data(name, date, credit, result, bank_name, commision)
				self.next()
			else:
				msg = QMessageBox()
				msg.setText("Brak nazwy banku!")
				msg.setIcon(QMessageBox.Critical)
				x = msg.exec_()
				return
		else:
			self.label_32.setText("Podano nieprawidłową kwotę kredytu!")
			return

def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	calculator = Calculator() #2

	widget.addWidget(calculator)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()



