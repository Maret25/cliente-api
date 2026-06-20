# API de Cadastro e Gestão de Clientes

Trabalho final da disciplina **CAC3024-09754 — Integração de Sistemas para Automação (2026/1)**.

API REST desenvolvida em **FastAPI** + **MongoDB**, com integração ao webservice externo **ViaCEP**.

---

## 📋 Requisitos atendidos

| Requisito | Endpoint(s) | Status |
|---|---|---|
| 2 — Envio de dados/comando + status | `POST/PUT/DELETE /api/v1/clientes` | ✅ |
| 3 — Busca por chave | `GET /api/v1/clientes/{id}` | ✅ |
| 4 — Webservice de terceiro | `GET /api/v1/cep/{cep}` (ViaCEP) | ✅ |
| 5 — Lista com filtro | `GET /api/v1/clientes?nome=&cidade=&estado=&ativo=` | ✅ |
| 6 — Banco de dados NoSQL | MongoDB | ✅ |

---

## 🗂️ Estrutura do projeto

```
cliente-api/
├── app/
│   ├── main.py              # ponto de entrada da aplicação
│   ├── config.py            # leitura das variáveis de ambiente
│   ├── database.py          # conexão com MongoDB
│   ├── models/
│   │   └── cliente.py       # modelos Pydantic (validação)
│   ├── routes/
│   │   ├── clientes.py      # CRUD de clientes (req. 2, 3, 5)
│   │   └── cep.py           # integração ViaCEP (req. 4)
│   └── services/
│       └── viacep_service.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Passo a passo — Rodando localmente

### 1. Verifique se o Python está instalado

Abra o terminal (Prompt de Comando / PowerShell no Windows, ou Terminal no Mac/Linux) e rode:

```bash
python3 --version
```

Se não tiver Python instalado, baixe em **https://www.python.org/downloads/** (marque a opção "Add Python to PATH" na instalação do Windows).

### 2. Crie um ambiente virtual (recomendado)

```bash
cd cliente-api
python3 -m venv venv

# Ativar o ambiente virtual:
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Crie sua conta no MongoDB Atlas (gratuito)

1. Acesse **https://www.mongodb.com/cloud/atlas/register** e crie uma conta gratuita.
2. Crie um novo **Cluster gratuito (M0)**.
3. Em "Database Access", crie um usuário e senha (anote-os).
4. Em "Network Access", clique em "Add IP Address" → "Allow Access from Anywhere" (`0.0.0.0/0`) — necessário para o deploy funcionar.
5. Clique em "Connect" → "Drivers" → copie a **Connection String**, algo como:
   ```
   mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite com seus dados:

```bash
cp .env.example .env
```

Abra o `.env` e cole sua connection string do Atlas:

```
MONGODB_URI=mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=cadastro_clientes
```

⚠️ **Substitua `usuario` e `senha`** pelos dados reais criados no passo 4. Se a senha tiver caracteres especiais (@, #, etc.), use a versão "URL encoded" que o próprio Atlas oferece no botão "Connect".

### 6. Rode a aplicação

```bash
uvicorn app.main:app --reload
```

Acesse no navegador:
- **http://localhost:8000** → mensagem de status
- **http://localhost:8000/docs** → documentação interativa (Swagger UI) — aqui você testa todos os endpoints clicando em "Try it out"

---

## 🧪 Testando os endpoints

### Cadastrar cliente (Requisito 2)
```bash
curl -X POST http://localhost:8000/api/v1/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Silva","email":"maria@email.com","telefone":"47999990000","cidade":"Blumenau","estado":"SC"}'
```

### Buscar cliente por ID (Requisito 3)
```bash
curl http://localhost:8000/api/v1/clientes/SEU_ID_AQUI
```

### Consultar CEP via ViaCEP (Requisito 4)
```bash
curl http://localhost:8000/api/v1/cep/01310-100
```

### Listar clientes com filtro (Requisito 5)
```bash
curl "http://localhost:8000/api/v1/clientes?estado=SC&ativo=true"
```

### Atualizar cliente
```bash
curl -X PUT http://localhost:8000/api/v1/clientes/SEU_ID_AQUI \
  -H "Content-Type: application/json" \
  -d '{"cidade":"Gaspar"}'
```

### Remover cliente
```bash
curl -X DELETE http://localhost:8000/api/v1/clientes/SEU_ID_AQUI
```

---

## ☁️ Deploy (URL pública) — Render.com

1. Suba este projeto para um repositório no **GitHub** (sem o arquivo `.env`!).
2. Crie uma conta em **https://render.com**.
3. Clique em "New +" → "Web Service" → conecte seu repositório do GitHub.
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Em "Environment Variables", adicione:
   - `MONGODB_URI` → sua connection string do Atlas
   - `DATABASE_NAME` → `cadastro_clientes`
6. Clique em "Create Web Service" e aguarde o deploy.
7. Sua API ficará disponível em algo como `https://seu-projeto.onrender.com`, com a documentação em `https://seu-projeto.onrender.com/docs`.

---

## 🛠️ Tecnologias utilizadas

- **Python 3.12** + **FastAPI** — framework web
- **Motor** — driver assíncrono do MongoDB
- **Pydantic** — validação de dados
- **httpx** — cliente HTTP para consumir o ViaCEP
- **MongoDB Atlas** — banco de dados NoSQL em nuvem
- **ViaCEP** — webservice de terceiro para consulta de endereços
