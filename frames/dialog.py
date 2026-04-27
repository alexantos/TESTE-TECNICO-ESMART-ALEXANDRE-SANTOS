from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog


class Dialog(QDialog):
    def __init__(self, imagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalhe da foto")
        layout = QVBoxLayout()
        self.alt = QLabel(imagem.alt)
        self.width = QLabel(str(imagem.width))
        self.height = QLabel(str(imagem.height))
        self.photographer = QLabel(imagem.photographer)
        self.photographer_url = QLabel(imagem.photographer_url)
        # self.alt.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.alt)
        layout.addWidget(self.width)
        layout.addWidget(self.height)
        layout.addWidget(self.photographer)
        layout.addWidget(self.photographer_url)
        self.setLayout(layout)
