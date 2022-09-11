import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QStackedWidget
from PyQt5.QtCore import Qt
from six import u
from encrypting import decryption, encryption


class InvoicesData(QDialog):
	def __init__(self):
		super(InvoicesData, self).__init__()
		loadUi("All_Windows/Invoices_Data.ui", self)
		self.BackButton.clicked.connect(self.go_back)
		self.saveButton.clicked.connect(self.save_to_file)
		self.multipleClientBox.clicked.connect(self.change_state_multiple)
		self.singleClientBox.clicked.connect(self.change_state_single)
		self.read_from_file()

	def get_vars_from_main_file(self, invoices, widget, app):
		self.invoices = invoices
		self.widget = widget
		self.app = app

	def go_back(self):
		self.widget.setCurrentIndex(8)

	def change_state_multiple(self):
		self.singleClientBox.setChecked(False)

	def change_state_single(self):
		self.multipleClientBox.setChecked(False)

	def read_from_file(self):
		fields = [self.invoiceNumberEdit, self.sellersEdit, self.buyersEdit,
			self.paymentFormEdit, self.notesEdit, self.productNameEdit, self.notesBottomEdit]
		try:
			decryption('MonthsBase/InvoiceData.txt')
			with open('MonthsBase/InvoiceData.txt', 'r',encoding='utf-8') as f:
				for i in range(len(fields)):
					if i == 1 or i == 2:
						fields[i].setPlainText((str(f.readline()).replace("\n","")).replace("~`","\n"))
					else:
						fields[i].setText((str(f.readline()).replace("\n","")).replace("~`","\n"))
			encryption('MonthsBase/InvoiceData.txt')
		except:
			return

	def get_price_in_words(self, value):
		JEDNOSTKI = [u(""), u("jeden"), u("dwa"), u("trzy"), u("cztery"), u("pięć"),
				u("sześć"), u("siedem"), u("osiem"), u("dziewięć")]
		DZIESIATKI = [u(""), u("dziesięć"), u("dwadzieścia"), u("trzydzieści"),
				u("czterdzieści"), u("pięćdziesiąt"), u("sześćdziesiąt"),
				u("siedemdziesiąt"), u("osiemdziesiąt"), u("dziewięćdziesiąt")]
		NASTKI = [u("dziesięć"), u("jedenaście"), u("dwanaście"), u("trzynaście"),
				u("czternaście"), u("piętnaście"), u("szesnaście"), u("siedemnaście"),
				u("osiemnaście"), u("dziewiętnaście")]
		SETKI = [u(""), u("sto"), u("dwieście"), u("trzysta"), u("czterysta"),
				u("pięćset"), u("sześćset"), u("siedemset"), u("osiemset"),
				u("dziewięćset")]

		WIELKIE = [
				[u("x"), u("x"), u("x")],
				[u("tysiąc"), u("tysiące"), u("tysięcy")],
				[u("milion"), u("miliony"), u("milionów")],
				[u("miliard"), u("miliardy"), u("miliardów")],
				[u("bilion"), u("biliony"), u("bilionów")],
			]

		ZLOTOWKI = [u("złoty"), u("złote"), u("złotych")]
		GROSZE = [u("grosz"), u("grosze"), u("groszy")]

		def _slownie3cyfry(liczba):
			je = liczba % 10
			dz = (liczba // 10) % 10
			se = (liczba // 100) % 10
			slowa = []

			if se > 0:
				slowa.append(SETKI[se])
			if dz == 1:
				slowa.append(NASTKI[je])
			else:
				if dz > 0:
					slowa.append(DZIESIATKI[dz])
				if je > 0:
					slowa.append(JEDNOSTKI[je])
			retval = u(" ").join(slowa)
			return retval

		def _przypadek(liczba):
			je = liczba % 10
			dz = (liczba // 10) % 10

			if liczba == 1:
				typ = 0  # jeden tysiąc"
			elif dz == 1 and je > 1:  # naście tysięcy
				typ = 2
			elif 2 <= je <= 4:
				typ = 1  # [k-dziesiąt/set] [dwa/trzy/czery] tysiące
			else:
				typ = 2  # x tysięcy

			return typ

		def lslownie(liczba):
			"""Liczba całkowita słownie"""
			trojki = []
			if liczba == 0:
				return u("zero")
			while liczba > 0:
				trojki.append(liczba % 1000)
				liczba = liczba // 1000
			slowa = []
			for i, n in enumerate(trojki):
				if n > 0:
					if i > 0:
						p = _przypadek(n)
						w = WIELKIE[i][p]
						slowa.append(_slownie3cyfry(n) + u(" ") + w)
					else:
						slowa.append(_slownie3cyfry(n))
			slowa.reverse()
			return u(" ").join(slowa)

		def cosslownie(liczba, cos):
			"""Słownie "ileś cosiów"
			liczba - int
			cos - tablica przypadków [coś, cosie, cosiów]"""

			return lslownie(liczba) + u(" ") + cos[_przypadek(liczba)]

		def kwotaslownie(liczba, fmt=0):
			"""Słownie złotych, groszy.
			liczba - float, liczba złotych z groszami po przecinku
			fmt - (format) jesli 0, to grosze w postaci xx/100, słownie w p. przypadku
			"""
			lzlotych = int(liczba)
			lgroszy = int(liczba * 100 + 0.5) % 100
			if fmt != 0:
				groszslownie = cosslownie(lgroszy, GROSZE)
			else:
				groszslownie = u("%d/100") % lgroszy
			return cosslownie(lzlotych, ZLOTOWKI) + u(" ") + groszslownie

		return kwotaslownie(value)

	def set_values(self):
		self.total_payment = [["0.00","0.00","0.00"] for i in range(4)]
		self.seller = str(self.sellersEdit.toPlainText()).replace("\n", "<br>")
		self.buyer = str(self.buyersEdit.toPlainText()).replace("\n", "<br>")
		self.sales_date = ".".join((str(self.dateEdit.date().toPyDate())).split("-")[::-1])
		self.issuance_date = ".".join((str(self.dateEdit_2.date().toPyDate())).split("-")[::-1])
		self.payment_due_by = ".".join((str(self.dateEdit_3.date().toPyDate())).split("-")[::-1])
		self.new_services = self.add_new_services()

	def separate_numbers(self, total_to_pay):
		try:
			total_to_pay = round(total_to_pay, 2)
		except:
			pass
		total_to_pay = str(total_to_pay).split(".")
		if len(total_to_pay[1]) < 2:
			total_to_pay[1] += "0"
		if len(total_to_pay[0]) > 3:
			total_to_pay[0] = list(total_to_pay[0])
			total_to_pay[0][-4] += " "
			total_to_pay[0] = "".join(total_to_pay[0])
		if len(total_to_pay[0]) > 7:
			total_to_pay[0] = list(total_to_pay[0])
			total_to_pay[0][-8] += " "
			total_to_pay[0] = "".join(total_to_pay[0])
		total_to_pay = ".".join(total_to_pay)
		return total_to_pay

	def add_new_services(self):
		taxes = [0.23, 0.08, 0.05, 0.00]
		taxes_numeric = ["23%", "8%", "5%", "zw"]
		buttons = [self.radioButton0, self.radioButton1, self.radioButton2, self.radioButton3]
		self.current_tax = 0
		for n in range(len(taxes)):
			if buttons[n].isChecked():
				self.current_tax = taxes[n]
				break
		self.total_payment[n] = [0,0,0]
		new_service = ""
		if self.multipleClientBox.isChecked():
			for i in range(len(self.invoices.invoice_list)):
				counted_tax = round(float(self.invoices.invoice_list[i][4]) * self.current_tax, 2)
				total_for_curr_product = float(self.invoices.invoice_list[i][4]) + counted_tax
				self.total_payment[n][0] += float(self.invoices.invoice_list[i][4])
				self.total_payment[n][1] += counted_tax
				self.total_payment[n][2] += total_for_curr_product
				new_service += \
				f""" 
				<tr>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="74" align="center" valign=middle bgcolor="#FFFFFF">{i+1}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;@">{self.productNameEdit.text()}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;@"><br></td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;@">usługa</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=middle sdnum="1033;0;0%">{taxes_numeric[n]}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00">{self.separate_numbers(self.invoices.invoice_list[i][4])}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=middle bgcolor="#FFFFFF">1</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00">{self.separate_numbers(self.invoices.invoice_list[i][4])}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=middle bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.separate_numbers(counted_tax)}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=middle bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.separate_numbers(total_for_curr_product)}</td>
					<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
				</tr>
				"""
		else:
			for i in range(len(self.invoices.invoice_list)):
				counted_tax = round(float(self.invoices.invoice_list[i][4]) * self.current_tax, 2)
				total_for_curr_product = float(self.invoices.invoice_list[i][4]) + counted_tax
				self.total_payment[n][0] += float(self.invoices.invoice_list[i][4])
				self.total_payment[n][1] += counted_tax
				self.total_payment[n][2] += total_for_curr_product
			new_service += \
				f""" 
				<tr>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="74" align="center" valign=middle bgcolor="#FFFFFF">1</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;@">{self.productNameEdit.text()}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;@"><br></td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;@">usługa</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=middle sdnum="1033;0;0%">{taxes_numeric[n]}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00">{self.separate_numbers(self.total_payment[n][0])}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=middle bgcolor="#FFFFFF">1</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00">{self.separate_numbers(self.total_payment[n][0])}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=middle bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.separate_numbers(self.total_payment[n][1])}</td>
					<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=middle bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.separate_numbers(self.total_payment[n][2])}</td>
					<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
				</tr>
				"""
		self.price_in_words = self.get_price_in_words(self.total_payment[n][2])
		for j in range(len(self.total_payment[n])):
			self.total_payment[n][j] = self.separate_numbers(self.total_payment[n][j])
		self.total_to_pay_for_all = self.total_payment[n][2]
		return new_service

	def save_to_file(self):
		fields = [self.invoiceNumberEdit.text(), self.sellersEdit.toPlainText(), self.buyersEdit.toPlainText(),
				  self.paymentFormEdit.text(), self.notesEdit.text(), self.productNameEdit.text(), self.notesBottomEdit.text()]
		decryption('MonthsBase/InvoiceData.txt')
		with open('MonthsBase/InvoiceData.txt', 'w',encoding='utf-8') as f:
			for n in fields:
				word = str(n).replace("\n", "~`") + "\n"
				f.write(word)
		encryption('MonthsBase/InvoiceData.txt')
		msg = QMessageBox()
		msg.setText("Dane zostały zapisane do systemu.\nPrzy ponownym uruchomieniu aplikacji dane zostaną automatycznie wpisane")
		x = msg.exec_()

def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	invoices_data = InvoicesData() #9

	widget.addWidget(invoices_data)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()


