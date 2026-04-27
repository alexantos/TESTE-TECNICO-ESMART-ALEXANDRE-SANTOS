from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog


class DialogDetalhe(QDialog):
    def __init__(self, imagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalhe da foto")
        layout = QVBoxLayout()
        self.alt = QLabel(imagem.alt)
        self.width = QLabel(str(imagem.width))
        self.height = QLabel(str(imagem.height))
        self.photographer = QLabel(imagem.photographer)
        self.photographer_url = QLabel(imagem.photographer_url)
        layout.addWidget(self.alt)
        layout.addWidget(self.width)
        layout.addWidget(self.height)
        layout.addWidget(self.photographer)
        layout.addWidget(self.photographer_url)
        self.setLayout(layout)


class DialogAlerta(QDialog):
    def __init__(self, titulo, mensagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        layout = QVBoxLayout()
        mensagem = QLabel(mensagem)
        layout.addWidget(mensagem)
        self.setLayout(layout)
