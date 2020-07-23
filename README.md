# tourism

## Objetivo

Foi criado um API com alguns recursos, possibilitando usuários consumirem e registrarem algumas informações, explorando pontos turísticos.

No desenvolvimento foi utilizado Python e FastAPI, pelo fato de possuir algumas entregas de valores e agilidade, como o Swagger e as dependências que foram aproveitadas.

## Instruções para executar ambiente

Criar um ambiente virtual para o isolamento da versão do python e suas dependências

```sh
python3.8 -m venv .env
```

```sh
# ativar o ambiente virtual
python3.8 -m venv .env

# e para desativar
deactivate
```

Instalar as dependências através do pip

```sh
make install
```

Para gerenciamento dos dados foi utilizado o PostgreSQL, então importante que você tenha uma base criada e aponte as configurações do seu banco de dados, no arquivo `.environment`.

Após isso, é necessário atualizar o versionamento da sua base com a criação das tabelas.

```sh
alembic upgrade head
```

Agora apenas iniciar a API.

```sh
make run
```