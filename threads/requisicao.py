from PySide6.QtCore import Slot, QObject, Signal

from frames.dialog import DialogAlerta
from models.imagem import Imagem
from service.service import Service


class RequisicaoThread(QObject):
    finalizado = Signal()
    atualizar = Signal(object)

    def __init__(self, pagina):
        super().__init__()
        self.pagina = pagina

    @Slot()
    def requisicao_lenta(self):
        self.carrega_imagens()
        self.finalizado.emit()

    def carrega_imagens(self):
        service = Service(pagina=self.pagina)
        request = service.lista_fotos()
        if request.status_code == 200:
            for photo in request.json()['photos']:
                foto = service.recupera_foto(url=photo['src']['large'])
                imagem = Imagem(
                    id=photo['id'],
                    photo=foto.content,
                    alt=photo['alt'],
                    width=photo['width'],
                    height=photo['height'],
                    photographer=photo['photographer'],
                    photographer_url=photo['photographer_url'],
                )
                self.atualizar.emit(imagem)
        else:
            dialog = DialogAlerta(
                titulo='Erro ao carregar imagens',
                mensagem="Falha ao recuperar imagens, tente novamente mais tarde"
            )
            dialog.exec()
            self.atualizar.emit(None)
            self.atualizar.disconnect()
