import sys
import base64
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt  # Qt 모듈 임포트 추가

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이미지 해석 애플리케이션")
        self.setGeometry(100, 100, 800, 600)

        # UI 구성
        self.image_label = QLabel("이미지를 선택하세요", self)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(600, 400)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("이미지 선택", self)
        self.select_button.clicked.connect(self.select_image)

        self.analyze_button = QPushButton("이미지 해석", self)
        self.analyze_button.clicked.connect(self.analyze_image)
        self.analyze_button.setEnabled(False)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.analyze_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 이미지 경로 저장 변수
        self.image_path = None

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height()))
            self.analyze_button.setEnabled(True)

    def analyze_image(self):
        if not self.image_path:
            return

        # 이미지 파일을 base64로 인코딩
        with open(self.image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # OpenAI API 호출
        api_key = "API Key"  # OpenAI API 키를 입력하세요
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",  # 적절한 모델을 선택하세요
            "messages": [
                {"role": "system", "content": "You are an assistant that interprets images."},
                {"role": "user", "content": f"이 이미지를 한글로 분석해줘: {encoded_image}"}
            ]
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            description = result['choices'][0]['message']['content']
            self.image_label.setText(description)
        except Exception as e:
            self.image_label.setText(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoForm()
    window.show()
    sys.exit(app.exec_())