# Desafio ESMART

Desenvolvido com PySide6

### Configurando o projeto

Para configurar o projeto primeiramente devemos configurar algumas variáveis de ambiente obrigatórias no .env:

```
# Itens obrigatórios
API_KEY="SUA API KEY AQUI"
```

Para isso crie o arquivo .env na raiz do projeto e copie essas variáveis ou utilize o .env.exemplo também disposto na
raiz do projeto

### Criação da venv

Primeiro devemos ter uma venv configurada na raiz do projeto

```bash
python -m venv .venv
```

Para ativar essa venv:

```bash
source .venv/bin/activate
```


### Instalação de dependências

```bash
pip install -r requirements.txt
```

O projeto conta com as "ferramentas permitidas" e a adição extra da lib python-dotenv apenas para lidar corretamente
com as variáveis de ambiente.

### Rodando o projeto

Para rodar o projeto podemos rodar o seguinte comando:

```bash
python run.py
```
