import os
import requests

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


class Service:
    def __init__(self, itens_por_pagina=20, pagina=1):
        self.itens_por_pagina = itens_por_pagina
        self.pagina = pagina
        self.url = 'https://api.pexels.com/v1/search'

    def get_requisicao(self):
        headers = {
            "Authorization": api_key
        }
        params = {
            "query": "nature",
            "per_page": self.itens_por_pagina,
            "page": self.pagina
        }
        r = requests.get(
            url=self.url,
            headers=headers,
            params=params
        )
        return r.json()
