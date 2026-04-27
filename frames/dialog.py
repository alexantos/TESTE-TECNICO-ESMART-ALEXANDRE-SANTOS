from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog


class DialogDetalhe(QDialog):
    def __init__(self, imagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalhe da foto")
        layout = QVBoxLayout()

        # Descrição
        label_descricao = QLabel("Descrição:")
        label_descricao.setMinimumHeight(10)
        label_descricao.setMaximumHeight(10)
        alt = QLabel(imagem.alt)
        alt.setMinimumHeight(20)
        alt.setMaximumHeight(20)

        # Tamanho
        label_width = QLabel("Tamanho:")
        label_width.setMinimumHeight(10)
        label_width.setMaximumHeight(10)
        width = QLabel(str(imagem.width))
        width.setMinimumHeight(20)
        width.setMaximumHeight(20)

        # Altura
        label_height = QLabel("Altura:")
        label_height.setMinimumHeight(10)
        label_height.setMaximumHeight(10)
        height = QLabel(str(imagem.height))
        height.setMinimumHeight(20)
        height.setMaximumHeight(20)

        # Fotógrafo
        label_photographer = QLabel("Altura:")
        label_photographer.setMinimumHeight(10)
        label_photographer.setMaximumHeight(10)
        photographer = QLabel(str(imagem.photographer))
        photographer.setMinimumHeight(20)
        photographer.setMaximumHeight(20)

        # Portifólio
        label_photographer_url = QLabel("Portifólio:")
        label_photographer_url.setMinimumHeight(10)
        label_photographer_url.setMaximumHeight(10)
        photographer_url = QLabel(imagem.photographer_url)
        photographer_url.setMinimumHeight(20)
        photographer_url.setMaximumHeight(20)

        layout.addWidget(label_descricao)
        layout.addWidget(alt)
        layout.addWidget(label_width)
        layout.addWidget(width)
        layout.addWidget(label_height)
        layout.addWidget(height)
        layout.addWidget(label_photographer)
        layout.addWidget(photographer)
        layout.addWidget(label_photographer_url)
        layout.addWidget(photographer_url)
        self.setLayout(layout)


class DialogAlerta(QDialog):
    def __init__(self, titulo, mensagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        layout = QVBoxLayout()
        mensagem = QLabel(mensagem)
        layout.addWidget(mensagem)
        self.setLayout(layout)
