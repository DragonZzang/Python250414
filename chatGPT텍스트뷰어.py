import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QMessageBox


class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle("텍스트 뷰어")
        self.setGeometry(100, 100, 800, 600)

        # 텍스트 편집기 위젯 추가
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        # 메뉴바 생성
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("파일")

        # "열기" 액션 추가
        openAction = QAction("열기", self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        # "종료" 액션 추가
        exitAction = QAction("종료", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

    def openFile(self):
        # 파일 열기 대화상자 표시
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "텍스트 파일 열기", "", "텍스트 파일 (*.txt);;모든 파일 (*)", options=options)

        if filePath:
            try:
                with open(filePath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.textEdit.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 열 수 없습니다:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TextViewer()
    viewer.show()
    sys.exit(app.exec_())