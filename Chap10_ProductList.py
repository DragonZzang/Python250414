import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic 
import sqlite3
import os.path 

class DatabaseManager:
    def __init__(self, db_name="ProductList.db"):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self._initialize_database()

    def _initialize_database(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Price INTEGER NOT NULL
            );
        """)
        self.con.commit()

    def add_product(self, name, price):
        self.cur.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (name, price))
        self.con.commit()

    def update_product(self, product_id, name, price):
        self.cur.execute("UPDATE Products SET Name = ?, Price = ? WHERE id = ?;", (name, price, product_id))
        self.con.commit()

    def delete_product(self, product_id):
        self.cur.execute("DELETE FROM Products WHERE id = ?;", (product_id,))
        self.con.commit()

    def get_all_products(self):
        self.cur.execute("SELECT * FROM Products;")
        return self.cur.fetchall()

form_class = uic.loadUiType("ProductList.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # DB 매니저 인스턴스
        self.db = DatabaseManager()

        # 테이블 설정
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        self.tableWidget.setTabKeyNavigation(False)

        # 엔터키 입력 시 포커스 이동
        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())

        # 더블클릭 이벤트 연결
        self.tableWidget.doubleClicked.connect(self.doubleClick)

    def addProduct(self):
        name = self.prodName.text().strip()
        price = self.prodPrice.text().strip()

        if name and price.isdigit():
            self.db.add_product(name, int(price))
            self.getProduct()
        else:
            QMessageBox.warning(self, "입력 오류", "제품명과 가격(숫자)을 올바르게 입력하세요.")

    def updateProduct(self):
        product_id = self.prodID.text().strip()
        name = self.prodName.text().strip()
        price = self.prodPrice.text().strip()

        if product_id.isdigit() and name and price.isdigit():
            self.db.update_product(int(product_id), name, int(price))
            self.getProduct()
        else:
            QMessageBox.warning(self, "수정 오류", "모든 필드를 올바르게 입력하세요.")

    def removeProduct(self):
        product_id = self.prodID.text().strip()
        if product_id.isdigit():
            self.db.delete_product(int(product_id))
            self.getProduct()
        else:
            QMessageBox.warning(self, "삭제 오류", "제품 ID를 올바르게 입력하세요.")

    def getProduct(self):
        self.tableWidget.clearContents()
        products = self.db.get_all_products()

        for row_idx, (prod_id, name, price) in enumerate(products):
            item_id = QTableWidgetItem(str(prod_id))
            item_id.setTextAlignment(Qt.AlignRight)
            item_name = QTableWidgetItem(name)
            item_price = QTableWidgetItem(str(price))
            item_price.setTextAlignment(Qt.AlignRight)

            self.tableWidget.setItem(row_idx, 0, item_id)
            self.tableWidget.setItem(row_idx, 1, item_name)
            self.tableWidget.setItem(row_idx, 2, item_price)

    def doubleClick(self):
        current_row = self.tableWidget.currentRow()
        self.prodID.setText(self.tableWidget.item(current_row, 0).text())
        self.prodName.setText(self.tableWidget.item(current_row, 1).text())
        self.prodPrice.setText(self.tableWidget.item(current_row, 2).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoForm()
    window.show()
    window.getProduct()  # 앱 시작 시 자동 로딩
    app.exec_()
