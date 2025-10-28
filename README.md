# Collection Service - TakeYourTrade

Backend microservice per la gestione delle collezioni utente nella piattaforma TakeYourTrade.

## Panoramica

Collection Service è un microservizio FastAPI che gestisce l'inventario delle carte possedute dagli utenti. Fornisce operazioni CRUD complete con autenticazione JWT e isolamento completo dei dati per utente.

### Caratteristiche

- **API RESTful** completa con FastAPI
- **Autenticazione JWT** con verifica JWKS
- **Database MySQL** (MariaDB 11.8+)
- **Filtri dinamici** per language, foil status, source
- **Paginazione** integrata
- **Validazione** input/output con Pydantic
- **CORS** configurato per domini autorizzati
- **Test endpoint** per verifica sistema
- **Documentazione** Swagger/ReDoc
- **Docker** per deploy containerizzato

## Stack Tecnologico

- **Linguaggio**: Python 3.11+
- **Framework**: FastAPI 0.104+
- **Database**: MySQL 8.0+ / MariaDB 11.8+
- **ORM**: SQLAlchemy 2.x (async)
- **Driver**: asyncmy per MySQL async
- **Migrazioni**: Alembic
- **Validazione**: Pydantic 2.x
- **Containerizzazione**: Docker + Docker Compose
- **Testing**: pytest

## Struttura del Progetto

```
collection-service/
├── app/
│   ├── core/
│   │   ├── config.py           # Configurazione e variabili ambiente
│   │   └── security.py         # Verifica JWT e JWKS
│   ├── dependencies.py          # Dipendenze FastAPI
│   ├── main.py                 # Entry point e routing principale
│   ├── models/
│   │   ├── database.py         # Setup database e session factory
│   │   └── item.py             # Modello CollectionItem
│   ├── routers/
│   │   └── items.py            # Endpoint CRUD
│   ├── schemas/
│   │   └── item.py             # Schemi Pydantic
│   └── services/
│       └── item_service.py     # Business logic
├── migrations/                 # Alembic migrations
├── tests/                      # Test suite
├── Dockerfile                  # Immagine Docker
├── docker-compose.yml          # Configurazione deploy
├── requirements.txt            # Dipendenze Python
└── alembic.ini                 # Configurazione Alembic
```

## Installazione e Setup Locale

### Prerequisiti

- Python 3.11+
- MySQL 8.0+ (MariaDB 11.8+)
- Git

### Setup

1. Clone repository:
```bash
git clone https://github.com/LCDT20/collection-service.git
cd collection-service
```

2. Crea virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows
```

3. Installa dipendenze:
```bash
pip install -r requirements.txt
```

4. Configura variabili ambiente (copia da `env.example`):
```bash
cp env.example .env
# Modifica .env con le tue credenziali
```

5. Esegui migrazioni:
```bash
alembic upgrade head
```

6. Avvia server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deploy con Docker

### Deploy su Hostinger VPS

Il servizio è configurato per deploy automatico tramite Docker Compose su Hostinger VPS.

**URL per Componi da URL:**
```
https://raw.githubusercontent.com/LCDT20/collection-service/main/docker-compose.yml
```

1. Accedi a pPanel Hostinger
2. Vai su VPS → Componi da URL
3. Incolla l'URL sopra
4. Clicca Deploy

Le variabili d'ambiente sono già configurate nel docker-compose.yml.

### Build Locale

```bash
# Build immagine
docker-compose build

# Avvia container
docker-compose up -d

# Logs
docker-compose logs -f collection-service

# Stop
docker-compose down
```

## API Endpoints

### Health Check e Test

- `GET /` - Root endpoint
- `GET /health` - Health check semplice
- `GET /test/database` - Test connessione database
- `GET /test/config` - Test configurazione
- `GET /docs` - Documentazione Swagger UI
- `GET /redoc` - Documentazione ReDoc

### Collection Items

Tutti gli endpoint richiedono header JWT:
```
Authorization: Bearer <token>
```

#### Crea Item
```
POST /api/v1/collections/items/
Content-Type: application/json

{
  "card_id": "uuid",
  "quantity": 1,
  "condition": "NM",
  "language": "en",
  "is_foil": false,
  "is_signed": false,
  "is_altered": false,
  "notes": "Optional notes",
  "tags": ["tag1", "tag2"],
  "source": "manual"
}
```

#### Lista Items
```
GET /api/v1/collections/items/
Query params:
  - limit: int (default: 100, max: 500)
  - offset: int (default: 0)
  - language: string (optional)
  - is_foil: boolean (optional)
  - source: string (optional)
```

#### Get Item
```
GET /api/v1/collections/items/{item_id}
```

#### Update Item
```
PATCH /api/v1/collections/items/{item_id}
Content-Type: application/json

{
  "quantity": 2,
  "condition": "LP"
}
```

#### Delete Item
```
DELETE /api/v1/collections/items/{item_id}
```

## Autenticazione

Il servizio usa autenticazione JWT con verifica tramite JWKS.

### Configurazione JWT

Le seguenti variabili d'ambiente devono essere configurate:

- `AUTH_JWKS_URL`: URL del servizio che espone le chiavi JWKS
- `JWT_AUDIENCE`: Audience atteso nel token
- `JWT_ISSUER`: Issuer atteso nel token

### Estrazione User ID

Il servizio estrae automaticamente l'user_id dal claim `sub` del JWT token. Questo user_id viene poi usato per filtrare tutte le query, garantendo che ogni utente possa accedere solo ai propri items.

### Esempio Header

```bash
curl -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
     http://server:8000/api/v1/collections/items/
```

## Modello Dati

### CollectionItem

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | UUID | Identificatore univoco |
| user_id | UUID | Proprietario dell'item |
| card_id | UUID | Riferimento alla carta |
| quantity | int | Numero di copie (min 1) |
| condition | string(10) | Condizione (M, NM, LP, MP, HP) |
| language | string(5) | Codice lingua (en, it, jp) |
| is_foil | boolean | Carta foil |
| is_signed | boolean | Carta firmata |
| is_altered | boolean | Carta alterata |
| notes | text | Note aggiuntive |
| tags | JSON | Array di tag personalizzati |
| source | string(50) | Origine (cardtrader, manual) |
| cardtrader_id | bigint | ID esterno CardTrader |
| last_synced_at | datetime | Ultima sincronizzazione |
| added_at | datetime | Data creazione (auto) |
| updated_at | datetime | Data ultimo aggiornamento (auto) |

### Indici

- Primary Key: `id`
- Unique: `cardtrader_id`
- Index: `user_id`, `card_id`, `condition`, `language`, `source`
- Composite Index: `(user_id, card_id)`

### Constraints

- CHECK: `quantity > 0`
- FOREIGN KEY: `user_id`, `card_id` (riferimenti esterni)

## Filtri e Paginazione

### Filtri Disponibili

- **language**: Filtra per lingua (es: "en", "it")
- **is_foil**: Filtra per carte foil (true/false)
- **source**: Filtra per origine (es: "cardtrader", "manual")

### Paginazione

- **limit**: Numero massimo di risultati (default: 100, max: 500)
- **offset**: Numero di risultati da saltare (default: 0)

### Ordinamento

I risultati sono ordinati per data di creazione (più recenti prima).

## Migrazioni Database

### Crea Nuova Migration

```bash
alembic revision --autogenerate -m "description"
```

### Applica Migrazioni

```bash
# Ultima versione
alembic upgrade head

# Versione specifica
alembic upgrade <revision>

# Rollback
alembic downgrade -1
```

### Stato Migrazioni

```bash
alembic current
alembic history
```

## Testing

### Esegui Test

```bash
# Tutti i test
pytest

# Test specifici
pytest tests/test_collection_api.py

# Con coverage
pytest --cov=app tests/
```

### Test Coverage

I test coprono:
- Endpoint CRUD
- Autenticazione JWT
- Filtri e paginazione
- Validazione input
- Isolamento dati per utente

## Variabili d'Ambiente

### Obbligatorie

- `DATABASE_URL`: Connection string MySQL (mysql+asyncmy://user:pass@host:port/db)

### Opzionali (con default)

- `AUTH_JWKS_URL`: https://auth.takeyourtrade.com/.well-known/jwks.json
- `JWT_AUDIENCE`: collection-service
- `JWT_ISSUER`: https://auth.takeyourtrade.com
- `CORS_ORIGINS`: JSON array di domini autorizzati
- `DEBUG`: false (production)

Vedi `env.example` per template completo.

## CORS Configuration

Il servizio è configurato per accettare richieste da:

- https://app.takeyourtrade.com
- https://takeyourtrade.com
- https://www.takeyourtrade.com
- http://localhost:3000 (dev)

Per modificare i domini autorizzati, aggiorna `CORS_ORIGINS` nelle variabili d'ambiente.

## Monitoring e Health Checks

### Health Endpoints

- `/health`: Basic health check
- `/test/database`: Test connessione database
- `/test/config`: Verifica configurazione
- `/test/full`: Test sistema completo

### Docker Health Check

Il Dockerfile include un health check che verifica `/health` ogni 30 secondi.

## Troubleshooting

### Container non si avvia

```bash
docker-compose logs collection-service
```

Verifica errori nelle variabili d'ambiente o nel database.

### Errore connessione database

- Verifica `DATABASE_URL` nel docker-compose.yml
- Controlla che IP VPS sia whitelisted nel pannello hosting
- Verifica che database esista e utente abbia permessi

### Errore CORS

- Verifica formato JSON in `CORS_ORIGINS`
- Assicurati che il dominio frontend sia nell'array

### Errore JWT

- Verifica che `AUTH_JWKS_URL` sia raggiungibile
- Controlla che `JWT_AUDIENCE` e `JWT_ISSUER` matchino

## Performance

### Ottimizzazioni Implementate

- Pool di connessioni database
- Indici su campi filtrati frequentemente
- Paginazione per limitare risultati
- Query async per non bloccare I/O
- Connection pooling con pool_pre_ping

### Limiti

- Massimo 500 items per richiesta lista
- Timeout connessione database: 5 secondi
- Pool size: configurabile in `database.py`

## Sicurezza

### Best Practices Implementate

- Autenticazione JWT obbligatoria per endpoint API
- Isolamento dati per utente (user_id filtering)
- Validazione input con Pydantic
- SQL injection prevention con SQLAlchemy ORM
- HTTPS in production (da configurare nel reverse proxy)
- Non-root user nel container Docker
- Health checks attivi
- CORS limitato a domini autorizzati

### Raccomandazioni

- Usa reverse proxy (nginx/traefik) per HTTPS
- Ruota periodicamente le credenziali database
- Monitora i log per accessi sospetti
- Implementa rate limiting
- Usa secret management per ambiente production

## Development

### Struttura Codice

- **routers/**: Endpoint HTTP e dependency injection
- **services/**: Business logic e logica applicativa
- **models/**: Strutture dati e database
- **schemas/**: Validazione input/output
- **core/**: Configurazione e utility

### Code Style

- Follow PEP 8
- Type hints per tutte le funzioni
- Docstrings per classi e funzioni pubbliche
- Async/await per operazioni I/O

## License

Proprietario - TakeYourTrade

## Support

Per domande o problemi:
- Documentazione: http://server:8000/docs
- Repository: https://github.com/LCDT20/collection-service
