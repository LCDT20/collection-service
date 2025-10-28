# Guida Deploy Collection Service

## Stato Attuale

✅ **Completato**:
- Modello SQLAlchemy CollectionItem
- API endpoints FastAPI complete
- Sistema di autenticazione JWT
- Script SQL CREATE TABLE
- Configurazione Docker pronta

⚠️ **In Attesa**: 
- Risoluzione problema connessione database MySQL

## Configurazione Database

### File Creati

1. **collection_items_table.sql** - Comando SQL per creare la tabella
2. **test_db_connection_fixed.py** - Script per testare la connessione
3. **setup_database.py** - Script per creare le tabelle via SQLAlchemy

### File .env

Crea un file `.env` nella root del progetto con:

```env
DATABASE_URL=mysql+asyncmy://u792485705_tyts:[PASSWORD_ENCODED]@srv1502.hstgr.io:3306/u792485705_maintyt
AUTH_JWKS_URL=https://auth.takeyourtrade.com/.well-known/jwks.json
JWT_AUDIENCE=collection-service
JWT_ISSUER=https://auth.takeyourtrade.com
CORS_ORIGINS=["https://app.takeyourtrade.com","http://localhost:3000"]
APP_NAME=Collection Service
APP_VERSION=1.0.0
DEBUG=False
```

**Nota**: Per la password `Na+xE|E12`, usa la versione URL-encoded:
```
Na%2BxE%7CE12
```

## Setup Database

### Opzione 1: Tramite SQL Direct (Raccomandato)

1. Accedi al database tramite phpMyAdmin o client MySQL
2. Esegui il contenuto di `collection_items_table.sql`

### Opzione 2: Tramite Script Python

```bash
python setup_database.py
```

## Test Connessione

```bash
python test_db_connection_fixed.py
```

## Test Applicazione

```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia il server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints Disponibili

- `GET /` - Health check
- `POST /api/v1/collections/items/` - Crea item
- `GET /api/v1/collections/items/` - Lista items
- `GET /api/v1/collections/items/{id}` - Dettaglio item
- `PATCH /api/v1/collections/items/{id}` - Aggiorna item
- `DELETE /api/v1/collections/items/{id}` - Elimina item

**Tutti gli endpoints richiedono autenticazione JWT Bearer token**

## Docker Deployment

### Build Docker Image

```bash
docker build -t collection-service:latest .
```

### Run con Docker Compose

```bash
docker-compose up -d
```

### Monitor Logs

```bash
docker-compose logs -f collection-service
```

## Autenticazione

Il servizio usa JWT token con:
- **JWKS URL**: https://auth.takeyourtrade.com/.well-known/jwks.json
- **Audience**: collection-service
- **Issuer**: https://auth.takeyourtrade.com
- **User ID**: Estratto dal claim `sub` del JWT

Ogni utente può accedere solo ai propri items grazie al filtro su `user_id`.

## Verifica Funzionamento

### Test con curl

```bash
# Health check (no auth richiesta)
curl http://localhost:8000/

# Lista items (richiede JWT)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/v1/collections/items/
```

## Troubleshooting

Vedi `TEST_CONNECTION.md` per problemi di connessione database.

