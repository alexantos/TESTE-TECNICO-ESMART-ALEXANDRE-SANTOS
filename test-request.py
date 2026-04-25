from service import Service

service = Service()
request = service.get_requisicao()

print("Minha requisição: ", request["photos"])