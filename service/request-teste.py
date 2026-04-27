from service import Service

service = Service()
request = service.lista_fotos()

print("Minha requisição: ", request["photos"])