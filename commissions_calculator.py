import sys, os
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QMessageBox, QStackedWidget, QHeaderView, QDoubleSpinBox
from PyQt5.QtCore import Qt


class CommissionsCalculator(QDialog):
	def __init__(self):
		super(CommissionsCalculator, self).__init__()
		loadUi("All_Windows/Commissions_Calculator.ui", self)
		self.BackButton.clicked.connect(self.back)
		self.count_commissions_button.clicked.connect(self.count_commissions)
		self.OtherCommButt.clicked.connect(self.other_commission)
		self.comboBox.currentIndexChanged.connect(self.count_commissions)

	def get_vars_from_main_file(self, customers, calculator, commissions, widget, app):
		self.customers = customers
		self.calculator = calculator
		self.commissions = commissions
		self.widget = widget
		self.app = app

	def setData(self):
		items = os.listdir(f"MonthsBase/Banks")
		items = [item[:-4] for item in items]
		self.comboBox.clear()
		self.comboBox.addItem("Wybierz z listy...")
		self.comboBox.addItem("Wszystkie banki")
		for n in range(len(items)):
			self.comboBox.addItem(f"{items[n]}")

	def count_commissions(self):
		banks_name = self.comboBox.currentText()
		if banks_name == "Wybierz z listy..." or len(banks_name) == 0:
			self.tableWidget.setRowCount(0)
			return
		if banks_name != "Wszystkie banki": 
			commission_data = self.commissions.get_current_data(banks_name)
		elif banks_name == "Wszystkie banki":
			banks = os.listdir(f"MonthsBase/Banks")
			banks = [item[:-4] for item in banks]
			commission_data = []
			for bank in banks:
				banks_data = self.commissions.get_current_data(bank)
				for item in banks_data:
					item.append(bank)
				commission_data += banks_data
		comms = [float(provision[1]) for provision in commission_data]
		offer_names = [provision[0] for provision in commission_data]
		if banks_name == "Wszystkie banki":
			all_banks_names = [provision[2] for provision in commission_data]
		entered_data = self.lineEdit_2.text()
		check_credit = self.calculator.check_data(entered_data)
		if check_credit != 1:
			self.comboBox.setCurrentIndex(0)
			self.tableWidget.setRowCount(0)
			msg = QMessageBox()
			msg.setText("Błędna kwota kredytu!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		else:
			entered_data = float(entered_data)
		comms_and_offers = []
		for n in range(len(comms)):
			if banks_name != "Wszystkie banki":
				comms_and_offers.append([round((comms[n]/100) * entered_data, 2), offer_names[n]])
			else:
				comms_and_offers.append([round((comms[n]/100) * entered_data, 2), offer_names[n], all_banks_names[n]])
		comms_and_offers = sorted(comms_and_offers)[::-1]
		for n in range(len(comms_and_offers)):
			comms_and_offers[n][0] = str(comms_and_offers[n][0]).split(".")
			if len(comms_and_offers[n][0][1]) == 1:
				comms_and_offers[n][0][1] += "0"
			comms_and_offers[n][0] = ".".join(comms_and_offers[n][0])
		
		self.tableWidget.setRowCount(len(comms_and_offers))
		if banks_name != "Wszystkie banki": 
			self.tableWidget.setColumnCount(2)
			self.tableWidget.setHorizontalHeaderLabels(["Oferta Banku", "Wynagrodzenie"])
			header = self.tableWidget.horizontalHeader()
			header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
			header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
			for i in range(len(comms_and_offers)):
				self.tableWidget.setItem(i, 0, QTableWidgetItem(str(comms_and_offers[i][1])))
				self.tableWidget.setItem(i, 1, QTableWidgetItem(str(comms_and_offers[i][0])))
		elif banks_name == "Wszystkie banki":
			self.tableWidget.setColumnCount(3)
			self.tableWidget.setHorizontalHeaderLabels(["Bank","Oferta Banku", "Wynagrodzenie"])
			header = self.tableWidget.horizontalHeader()
			header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
			header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
			header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
			for i in range(len(comms_and_offers)):
				self.tableWidget.setItem(i, 0, QTableWidgetItem(str(comms_and_offers[i][2])))
				self.tableWidget.setItem(i, 1, QTableWidgetItem(str(comms_and_offers[i][1])))
				self.tableWidget.setItem(i, 2, QTableWidgetItem(str(comms_and_offers[i][0])))

	def other_commission(self):
		entered_total = self.lineEdit_2.text()
		check_credit = self.calculator.check_data(entered_total)
		if check_credit != 1:
			msg = QMessageBox()
			msg.setText("Błędna kwota kredytu!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		else:
			entered_total = float(entered_total)

		entered_comm = self.lineEdit_3.text()
		check_data = self.calculator.check_data(entered_comm)
		if check_data != 1:
			msg = QMessageBox()
			msg.setText("Błędna prowizja!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		else:
			entered_comm = float(entered_comm)

		calculated_offer = str(round(entered_total * (entered_comm/100), 2)).split(".")
		if len(calculated_offer[1]) == 1:
			calculated_offer[1] += "0"
		calculated_offer = ".".join(calculated_offer)
		self.label_4.setText(f"{calculated_offer}")

	def back(self):
		self.tableWidget.setRowCount(0)
		self.label_10.setText("")
		self.label_4.setText("")
		self.lineEdit_2.setText("")
		self.lineEdit_3.setText("")
		if self.customers.commission_window == False:
			self.widget.setCurrentIndex(0)
		else:
			self.widget.setCurrentIndex(5)
			self.customers.commission_window = False


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	commission_calculator = CommissionsCalculator() #7

	widget.addWidget(commission_calculator)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()
