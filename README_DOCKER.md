# 🐳 Collection Service - Docker Quick Start

## Pronto per il Deploy!

Il servizio è completamente configurato e pronto per essere deployato con Docker.

## Setup Completo

### 1. File `.env` Configurato ✅
```env
DATABASE_URL=mysql+asyncmy://u792485705_tyts:oA5843eC@srv1502.hstgr.io:3306/u792485705_maintyt
AUTH_JWKS_URL=https://auth.takeyourtrade.com/.well-known/jwks.json
JWT_AUDIENCE=collection-service
JWT_ISSUER=https://auth.takeyourtrade.com
CORS_ORIGINS=["https://app.takeyourtrade.com","http://localhost:3000","http://localhost:8000"]
APP_NAME=Collection Service
APP_VERSION=1.0.0
DEBUG=False
```

### 2. Database MySQL Remoto ✅
- ✅ Connessione testata
- ✅ Tabella `collection_items` creata
- ✅ IP autorizzato: 78.213.73.13

### 3. Docker Configurazione ✅
- ✅ Dockerfile ottimizzato
- ✅ docker-compose.yml con database remoto
- ✅ .dockerignore configurato
- ✅ Health check attivo

## Avvio Rapido

```bash
# Build e avvia
docker-compose up -d --build

# Verifica logs
docker-compose logs -f collection-service

# Test
curl http://localhost:8000/health
```

## Struttura Progetto

```
.
├── app/                    # Codice applicazione
│   ├── main.py            # Entry point FastAPI
│   ├── core/              # Configurazione e sicurezza
│   ├── models/            # Modelli SQLAlchemy
│   ├── routers/           # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── tests/                 # Test unitari
├── Dockerfile             # Immagine Docker
├── docker-compose.yml     # Orchestrazione
├── .env                   # Variabili ambiente
├── requirements.txt       # Dipendenze Python
└── README_DOCKER.md       # Questo file
```

## API Endpoints

Tutti gli endpoints richiedono JWT Bearer token:

- `POST /api/v1/collections/items/` - Crea item
- `GET /api/v1/collections/items/` - Lista items  
- `GET /api/v1/collections/items/{id}` - Dettaglio
- `PATCH /api/v1/collections/items/{id}` - Aggiorna
- `DELETE /api/v1/collections/items/{id}` - Elimina

Documentazione: http://localhost:8000/docs

## Caratteristiche

- ✅ JWT Authentication
- ✅ Filtro automatico per user_id
- ✅ Validazione input/output
- ✅ Paginazione e filtri
- ✅ Health checks
- ✅ CORS configurato
- ✅ Logging strutturato

## Comandi Utili

```bash
# Avvia
docker-compose up -d

# Ferma
docker-compose down

# Restart
docker-compose restart

# Logs in tempo reale
docker-compose logs -f

# Shell nel container
docker exec -it collection_service bash

# Rebuild
docker-compose build --no-cache
```

## Troubleshooting

Se il container non si avvia:
```bash
docker-compose logs collection-service
```

Se ci sono problemi con il database:
- Verifica che l'IP sia whitelisted: 78.213.73.13
- Controlla le credenziali in `.env`

## Production Checklist

- [x] Database remoto configurato
- [x] JWT authentication attiva
- [x] Health checks attivi
- [x] Non-root user nel container
- [ ] HTTPS/TLS (configura reverse proxy)
- [ ] Rate limiting
- [ ] Monitoring e alerting

## Supporto

Per domande o problemi, consulta:
- Swagger UI: http://localhost:8000/docs
- DEPLOY.md per dettagli deploy
- README.md per documentazione tecnica

