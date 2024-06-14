# Projeto de Arquitetura

## Engenharia de Software - SENAI - 7º Período

<hr/>

# Rodando o projeto

#### Para rodar o projeto, é preciso instalar o gerenciador de ambiente virtual PipEnv

```bash
$ pip install pipenv
```

#### Após isso, instalar as dependências do arquivo Pipfile com:

```bash
$ pipenv install
```

#### Para rodar o projeto, é só rodar:

```bash
$ pipenv run python manage.py runserver
```

#### Se houver necessidade de realizar migrations:

```bash
$ pipenv run python manage.py makemigrations
```

#### e

```bash
$ pipenv run python manage.py migrate
```

<hr>

# Configurações

#### Para a criação de funcionários, deve-se utilizar o admin do django, portanto, deve-se ter um super-usuário. A aplicação conta com a criação automática do mesmo, baseado em variáveis de ambiente. Para isso, deve ser criado um arquivo .env na raiz do projeto, contendo as variáveis de .env.example

```bash
ADMIN_USERNAME=usuario
ADMIN_PASSWORD=senha
```

#### Um grupo para funcionários já é criado automaticamente, denomidado "employee", porém, é necessário entrar no admin do django para definir as permissões conforme a necessidade

<hr>

# Rodando com Docker Compose

#### Para rodar com docker compose:

```bash
$ docker compose up -d --build
```
