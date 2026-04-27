from PySide6.QtWidgets import QVBoxLayout, QFrame, QLabel

from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt


class CardImagem(QFrame):
    def __init__(self, imagem, on_click_callback):
        super().__init__()
        self.imagem = imagem
        self.on_click_callback = on_click_callback

        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)

        label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(imagem.photo)
        scaled_pixmap = pixmap.scaled(540, 540)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)

        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(imagem.alt))

        layout.addWidget(label)
        layout.addLayout(info_layout)
        layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_click_callback()
        super().mousePressEvent(event)
