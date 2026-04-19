# 🎓 API Escola

API REST para gerenciamento de alunos, cursos e matrículas, desenvolvida com **Python (Flask)** e **MySQL**.

---

## 📁 Estrutura do Projeto

```
api_escola/
├── app.py                  # Ponto de entrada da aplicação
├── requirements.txt        # Dependências Python
├── .env.example            # Modelo de variáveis de ambiente
├── config/
│   └── database.py         # Conexão e inicialização do banco
├── controllers/
│   ├── alunos_controller.py
│   ├── cursos_controller.py
│   └── matriculas_controller.py
├── services/
│   ├── alunos_service.py
│   ├── cursos_service.py
│   └── matriculas_service.py
├── routes/
│   ├── alunos.py
│   ├── cursos.py
│   └── matriculas.py
└── static/
    └── swagger.json        # Documentação da API
```

---

## ⚙️ Como configurar o banco de dados

1. Crie o banco no MySQL:

```sql
CREATE DATABASE escola_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. As tabelas são criadas **automaticamente** ao iniciar a aplicação.

### Tabelas criadas:

**alunos**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT AUTO_INCREMENT | Chave primária |
| nome | VARCHAR(100) | Obrigatório |
| email | VARCHAR(150) UNIQUE | Obrigatório |
| created_at | TIMESTAMP | Criado em |

**cursos**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT AUTO_INCREMENT | Chave primária |
| titulo | VARCHAR(150) | Obrigatório |
| descricao | TEXT | Opcional |
| created_at | TIMESTAMP | Criado em |

**matriculas**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT AUTO_INCREMENT | Chave primária |
| aluno_id | INT (FK) | Referência ao aluno |
| curso_id | INT (FK) | Referência ao curso |
| status | ENUM | `ativa`, `cancelada`, `concluida` |
| created_at | TIMESTAMP | Criado em |

---

## 🚀 Como rodar o projeto

### Pré-requisitos
- Python 3.10+
- MySQL 8.0+

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/api-escola.git
cd api-escola

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com seus dados do MySQL

# 5. Inicie a aplicação
python app.py
```

A API estará disponível em: `http://localhost:5000`  
A documentação Swagger estará em: `http://localhost:5000/docs`

---

## 📋 Endpoints disponíveis

### 👤 Alunos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/alunos/` | Listar todos os alunos |
| GET | `/alunos/<id>` | Buscar aluno por ID |
| POST | `/alunos/` | Criar aluno |
| PUT | `/alunos/<id>` | Atualizar aluno |
| DELETE | `/alunos/<id>` | Deletar aluno |

**Criar/Atualizar aluno — Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com"
}
```

---

### 📚 Cursos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/cursos/` | Listar todos os cursos |
| GET | `/cursos/<id>` | Buscar curso por ID |
| POST | `/cursos/` | Criar curso |
| PUT | `/cursos/<id>` | Atualizar curso |
| DELETE | `/cursos/<id>` | Deletar curso |
| GET | `/cursos/<id>/alunos` | Listar alunos de um curso |

**Criar/Atualizar curso — Body:**
```json
{
  "titulo": "Python para Iniciantes",
  "descricao": "Curso introdutório de Python"
}
```

---

### 🎓 Matrículas

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/matriculas/` | Matricular aluno em curso |
| GET | `/matriculas/aluno/<id>/cursos` | Listar cursos de um aluno |
| PATCH | `/matriculas/aluno/<aluno_id>/curso/<curso_id>/cancelar` | Cancelar matrícula |
| PATCH | `/matriculas/aluno/<aluno_id>/curso/<curso_id>/concluir` | Concluir curso |

**Matricular — Body:**
```json
{
  "aluno_id": 1,
  "curso_id": 2
}
```

---

### ⚠️ Formato de erros

```json
{
  "error": "Mensagem descritiva do erro",
  "statusCode": 400
}
```

| Código | Significado |
|--------|-------------|
| 400 | Requisição inválida / regra de negócio |
| 404 | Recurso não encontrado |

---

## 🔒 Regras de negócio

- Email do aluno deve ser **único**
- Campos `nome` e `email` (aluno) e `titulo` (curso) são **obrigatórios**
- Um aluno **não pode se matricular duas vezes** no mesmo curso
- Não é permitido matricular aluno ou curso **inexistente**
- Um aluno pode ter no máximo **5 matrículas ativas**
- Status da matrícula: `ativa` → `cancelada` ou `concluida`

---

## 🌐 Deploy

### Variáveis de ambiente necessárias

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DB_HOST` | Host do banco de dados | `localhost` |
| `DB_USER` | Usuário do MySQL | `root` |
| `DB_PASSWORD` | Senha do MySQL | `senha123` |
| `DB_NAME` | Nome do banco | `escola_db` |
| `DB_PORT` | Porta do MySQL | `3306` |

### Deploy no Railway (recomendado para iniciantes)

1. Acesse [railway.app](https://railway.app) e crie uma conta
2. Crie um novo projeto e adicione um banco **MySQL**
3. Conecte seu repositório GitHub
4. Configure as variáveis de ambiente no painel do Railway (copie os valores do MySQL gerado)
5. Adicione a variável `PORT` e certifique-se de que o app usa `os.getenv('PORT', 5000)`
6. O Railway detecta automaticamente o `requirements.txt` e faz o deploy

**Comando de start para produção (Procfile):**
```
web: gunicorn app:app
```

### Deploy no Render

1. Acesse [render.com](https://render.com) e crie uma conta
2. Crie um **Web Service** conectado ao seu repositório
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Adicione as variáveis de ambiente no painel
6. Crie um banco MySQL externo (ex: [PlanetScale](https://planetscale.com) ou [Aiven](https://aiven.io)) e use as credenciais

---

## 📖 Documentação interativa

Com a API rodando, acesse `/docs` para visualizar e testar todos os endpoints via **Swagger UI**.
