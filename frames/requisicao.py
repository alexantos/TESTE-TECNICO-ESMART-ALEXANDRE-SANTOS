import requests

from PySide6.QtCore import Slot, QObject, Signal

from models.imagem import Imagem
from service.service import Service


class Requisicao(QObject):
    finalizado = Signal()
    atualizar = Signal(object)

    def __init__(self, pagina):
        super().__init__()
        self.pagina = pagina

    @Slot()
    def requisicao_lenta(self):
        self.carrega_imagens()
        self.finalizado.emit()

    def carrega_imagens(self):  # TODO: Fazer novos métodos com novas camadas para chamadas
        service = Service(pagina=self.pagina)
        request = service.get_requisicao()

        for photo in request['photos']:
            response = requests.get(photo['src']['large'])

            imagem = Imagem(
                id=photo['id'],
                photo=response.content,
                alt=photo['alt'],
                width=photo['width'],
                height=photo['height'],
                photographer=photo['photographer'],
                photographer_url=photo['photographer_url'],
            )

            self.atualizar.emit(imagem)
