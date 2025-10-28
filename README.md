# Collection Service - TakeYourTrade

Microservizio backend per la gestione dell'inventario delle carte possedute dagli utenti nella piattaforma TakeYourTrade.

## 📋 Descrizione

Il **Collection Service** è responsabile della gestione completa delle carte nella collezione degli utenti. Questo servizio opera in modo indipendente dagli altri microservizi (Auth, Sync, ecc.) e utilizza **MySQL 8.0+** come database.

## 🛠️ Stack Tecnologico

- **Linguaggio:** Python 3.11+
- **Framework:** FastAPI
- **Database:** MySQL 8.0+ (locale e Docker)
- **ORM:** SQLAlchemy 2.x (async con `asyncmy`)
- **Migrazioni:** Alembic (configurato per MySQL async)
- **Validazione:** Pydantic 2.x
- **Autenticazione:** JWT con verifica JWKS
- **Containerizzazione:** Docker + Docker Compose
- **Testing:** pytest con httpx (async)

## 📁 Struttura del Progetto

```
collection-service/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Entry point FastAPI
│   ├── core/
│   │   ├── config.py                # Settings e configurazione
│   │   └── security.py              # JWT verification
│   ├── dependencies.py               # Dependenze FastAPI
│   ├── models/
│   │   ├── database.py              # Engine e session setup
│   │   └── item.py                  # Model CollectionItem
│   ├── schemas/
│   │   └── item.py                  # Schemi Pydantic
│   ├── services/
│   │   └── item_service.py          # Business logic
│   └── routers/
│       └── items.py                 # Endpoints CRUD
├── migrations/                       # Alembic migrations
│   ├── env.py
│   └── versions/
├── tests/
│   └── test_collection_api.py       # Test suite
├── .env.example                     # Template variabili ambiente
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## 🚀 Setup Locale

### Prerequisiti

- Python 3.11+
- MySQL 8.0+ (locale o Docker)
- pip

### 1. Clone e Setup Ambiente Virtuale

```bash
# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente virtuale
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Configurazione Database

Crea un file `.env` nella root del progetto:

```env
# Database Configuration
DATABASE_URL=mysql+asyncmy://collection_user:collection_password@localhost:3306/collection_db

# JWT Authentication
AUTH_JWKS_URL=https://auth.takeyourtrade.com/.well-known/jwks.json
JWT_AUDIENCE=collection-service
JWT_ISSUER=https://auth.takeyourtrade.com

# CORS Configuration
CORS_ORIGINS=["https://app.takeyourtrade.com","http://localhost:3000"]

# Application
APP_NAME=Collection Service
APP_VERSION=1.0.0
DEBUG=True
```

### 3. Setup Database MySQL

Crea il database e l'utente:

```sql
-- Connetti come root
mysql -u root -p

-- Crea database
CREATE DATABASE collection_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crea utente
CREATE USER 'collection_user'@'localhost' IDENTIFIED BY 'collection_password';

-- Concedi privilegi
GRANT ALL PRIVILEGES ON collection_db.* TO 'collection_user'@'localhost';

-- Applica modifiche
FLUSH PRIVILEGES;
```

### 4. Esegui Migrazioni

```bash
# Inizializza Alembic (solo la prima volta)
# NOTA: Se la directory migrations non esiste ancora
alembic init migrations

# Genera prima migrazione (solo dopo setup completo)
# NOTA: Questo creerà lo script di migrazione
alembic revision --autogenerate -m "Initial migration for collection items"

# Applica migrazioni
alembic upgrade head
```

### 5. Avvia Applicazione

```bash
# Avvio sviluppo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Oppure direttamente con Python
python -m app.main
```

L'applicazione sarà disponibile su `http://localhost:8000`

## 🐳 Setup con Docker

### Quick Start

```bash
# Costruisci e avvia servizi (app + MySQL)
docker-compose up --build

# In background
docker-compose up -d

# Visualizza logs
docker-compose logs -f app
```

### Setup Database in Docker

```bash
# Esegui migrazioni nel container
docker exec -it collection_service alembic upgrade head

# Oppure esegui localmente (se .env punta al DB Docker)
alembic upgrade head
```

### Comandi Utili

```bash
# Stop servizi
docker-compose down

# Stop e rimuovi volumi
docker-compose down -v

# Rebuild app (mantiene dati DB)
docker-compose up --build

# Accesso shell al container
docker exec -it collection_service /bin/bash

# Accesso MySQL
docker exec -it collection_db mysql -u collection_user -pcollection_password collection_db
```

## 🧪 Testing

### Esegui Test

```bash
# Tutti i test
pytest

# Con verbose
pytest -v

# Specifico file
pytest tests/test_collection_api.py

# Con coverage
pytest --cov=app tests/

# In Docker
docker-compose exec app pytest
```

## 📡 API Endpoints

### Base URL

- **Local:** `http://localhost:8000`
- **Docker:** `http://localhost:8000`
- **Produzione:** (configurabile)

### Authentication

Tutti gli endpoint (eccetto `/health`) richiedono autenticazione JWT:

```
Authorization: Bearer <token>
```

### Endpoints

#### Health Check

```http
GET /health
GET /
```

#### Collection Items

**Lista Items** (con filtri e paginazione)
```http
GET /api/v1/collections/items/
  ?limit=100
  &offset=0
  &language=en
  &is_foil=true
  &source=cardtrader
```

**Crea Item**
```http
POST /api/v1/collections/items/
Content-Type: application/json

{
  "card_id": "uuid",
  "quantity": 2,
  "condition": "NM",
  "language": "en",
  "is_foil": false,
  "is_signed": false,
  "is_altered": false,
  "notes": "Limited edition",
  "tags": ["foil", "special"],
  "source": "cardtrader",
  "cardtrader_id": 12345
}
```

**Ottieni Item Specifico**
```http
GET /api/v1/collections/items/{item_id}
```

**Aggiorna Item**
```http
PATCH /api/v1/collections/items/{item_id}
Content-Type: application/json

{
  "quantity": 3,
  "condition": "LP"
}
```

**Elimina Item**
```http
DELETE /api/v1/collections/items/{item_id}
```

### Documentazione API

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 📊 Modello Dati

### CollectionItem

| Campo | Tipo | Obbligatorio | Descrizione |
|-------|------|--------------|-------------|
| `id` | UUID | ✅ | Primary Key |
| `user_id` | UUID | ✅ | Owner |
| `card_id` | UUID | ✅ | Card reference |
| `quantity` | Integer | ✅ | Numero copie (>= 1) |
| `condition` | String(10) | ✅ | Condizione carta |
| `language` | String(5) | ✅ | Codice lingua |
| `is_foil` | Boolean | ✅ | Carta foil |
| `is_signed` | Boolean | ❌ | Carta firmata |
| `is_altered` | Boolean | ❌ | Carta alterata |
| `notes` | Text | ❌ | Note aggiuntive |
| `tags` | JSON | ❌ | Tag personalizzati |
| `source` | String(50) | ❌ | Sorgente (es. "cardtrader") |
| `cardtrader_id` | BigInteger | ❌ | ID CardTrader (UNIQUE) |
| `last_synced_at` | DateTime | ❌ | Ultima sync |
| `added_at` | DateTime | ✅ | Data creazione |
| `updated_at` | DateTime | ✅ | Data ultimo aggiornamento |

## 🔐 Sicurezza

### JWT Authentication

Il servizio verifica i token JWT utilizzando:
- **JWKS URL** (`AUTH_JWKS_URL`)
- **Audience** (`JWT_AUDIENCE`)
- **Issuer** (`JWT_ISSUER`)

I token devono contenere il claim `sub` con il `user_id` dell'utente.

### Ownership Check

Tutte le operazioni su item specifici verificano l'ownership:
- Solo il proprietario può vedere/modificare/eliminare i propri item
- La lista filtra automaticamente per `user_id`

## 🔄 Migrazioni Database

### Genera Nuova Migrazione

```bash
# Dopo modifiche ai modelli
alembic revision --autogenerate -m "Description"

# Crea migrazione vuota
alembic revision -m "Description"
```

### Applica Migrazioni

```bash
# Applica tutte
alembic upgrade head

# Versione specifica
alembic upgrade <revision>

# Downgrade
alembic downgrade -1

# In Docker
docker exec -it collection_service alembic upgrade head
```

### Rollback

```bash
# Indietro di 1 versione
alembic downgrade -1

# Versione specifica
alembic downgrade <revision>

# Rimuovi tutto (ATTENZIONE!)
alembic downgrade base
```

## 📦 Deploy su VPS Hostinger

### 1. Preparazione Server

```bash
# Aggiorna sistema
sudo apt update && sudo apt upgrade -y

# Installa Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installa Docker Compose
sudo apt install docker-compose -y

# Aggiungi utente a gruppo docker
sudo usermod -aG docker $USER
```

### 2. Deploy Applicazione

```bash
# Clona repository
git clone <repository-url> collection-service
cd collection-service

# Crea .env
cp .env.example .env
nano .env  # Modifica con valori produzione

# Build e avvia
docker-compose up -d

# Esegui migrazioni
docker exec -it collection_service alembic upgrade head

# Verifica logs
docker-compose logs -f
```

### 3. Configurazione Nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name collection-api.takeyourtrade.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. SSL con Let's Encrypt

```bash
# Installa Certbot
sudo apt install certbot python3-certbot-nginx -y

# Configura certificato
sudo certbot --nginx -d collection-api.takeyourtrade.com
```

## 🐛 Troubleshooting

### Problema connessione MySQL

```bash
# Verifica MySQL è attivo
docker-compose ps

# Controlla logs DB
docker-compose logs db

# Testa connessione
docker exec -it collection_service python -c "import asyncio; from app.models.database import engine; asyncio.run(engine.connect())"
```

### Migrazioni fallite

```bash
# Resetta migrazioni (ATTENZIONE: perdi dati!)
alembic downgrade base
alembic upgrade head
```

### Test falliti

```bash
# Pulisci cache
pytest --cache-clear

# Reinstalla dipendenze
pip install --force-reinstall -r requirements.txt
```

## 📝 Note Sviluppo

- Usa `async/await` ovunque per operazioni I/O
- Tutte le query DB sono async con SQLAlchemy 2.x
- I tipi UUID sono gestiti con `as_uuid=True`
- Il campo `tags` usa `JSON` MySQL (non JSONB PostgreSQL)
- Le migrazioni Alembic sono configurate per async MySQL
- Gli endpoint rispettano i principi REST

## 📄 Licenza

Proprietario - TakeYourTrade

## 👥 Contributori

- Team TakeYourTrade

## 📞 Supporto

Per supporto o domande:
- Email: dev@takeyourtrade.com
- Issue Tracker: [GitHub Issues]

