# Collection Service - Deploy con Docker Compose

## 🚀 Deploy Veloce su Hostinger VPS

## Descrizione

Collection Service è un microservizio FastAPI per la gestione delle collezioni utente. Supporta operazioni CRUD complete con autenticazione JWT e filtri avanzati.

## 📋 Prerequisiti

- Hosting con Docker support (Hostinger VPS)
- Database MySQL remoto configurato
- Accesso SSH alla VPS
- File `.env` configurato sul server

## 🔧 Setup

### 1. Variabili d'Ambiente

Prima di procedere al deploy, configura le variabili d'ambiente sul server:

```bash
# Copia il template
cp env.example .env

# Modifica con i tuoi valori (VIETATO includere nel repository!)
nano .env
```

**Variabili richieste:**
- `DATABASE_URL`: Connessione al database MySQL (mysql+asyncmy://user:pass@host:port/db)
- `AUTH_JWKS_URL`: URL del servizio di autenticazione JWKS
- `JWT_AUDIENCE`: Audience del token JWT
- `JWT_ISSUER`: Issuer del token JWT
- `CORS_ORIGINS`: Domini autorizzati (array JSON)

### 2. Deploy via Componi da URL

1. Ottieni l'URL del file `docker-compose.yml`:
   - Vai sul repository GitHub/GitLab
   - Apri il file `docker-compose.yml`
   - Clicca su "Raw"
   - Copia l'URL completo (es: `https://raw.githubusercontent.com/user/repo/main/docker-compose.yml`)

2. Su Hostinger VPS:
   - Vai alla sezione "Componi da URL"
   - Incolla l'URL del `docker-compose.yml`
   - Conferma il deploy

3. **Configura le variabili d'ambiente:**
   ```bash
   # Connetti via SSH
   ssh user@your-server.com
   
   # Naviga nella directory di deploy (di solito /root o /home/user)
   cd /path/to/deployed/app
   
   # Crea e configura .env
   nano .env
   # Inserisci tutti i valori come nel file env.example
   
   # Applica le variabili al container
   docker-compose down
   docker-compose up -d
   ```

### 3. Migrazioni Database

Dopo il deploy, esegui le migrazioni:

```bash
docker-compose exec collection-service alembic upgrade head
```

Oppure se le migrazioni sono state eseguite manualmente prima:

```bash
# Verifica lo stato
docker-compose exec collection-service alembic current

# Se necessario, upgrade
docker-compose exec collection-service alembic upgrade head
```

## 🌐 Configurazione CORS

Assicurati che `CORS_ORIGINS` includa tutti i domini che chiameranno l'API:

```env
CORS_ORIGINS=["https://app.takeyourtrade.com","https://takeyourtrade.com","https://www.takeyourtrade.com"]
```

## 📡 Endpoints API

### Base URL
`http://your-server-ip:8000`

### Endpoints Disponibili
- `GET /` - Health check
- `GET /health` - Health check dettagliato
- `GET /docs` - Documentazione Swagger UI
- `GET /redoc` - Documentazione ReDoc
- `POST /api/v1/collections/items/` - Crea item
- `GET /api/v1/collections/items/` - Lista items
- `GET /api/v1/collections/items/{id}` - Dettaglio item
- `PATCH /api/v1/collections/items/{id}` - Aggiorna item
- `DELETE /api/v1/collections/items/{id}` - Elimina item

**Tutti gli endpoint `/api/v1/*` richiedono JWT Bearer token.**

## 🔒 Autenticazione

Ogni richiesta all'API deve includere un header:
```
Authorization: Bearer <JWT_TOKEN>
```

Il servizio:
1. Valida il token JWT tramite JWKS
2. Estrae l'user_id dal claim `sub`
3. Filtra automaticamente i dati per utente

## 🛠️ Gestione Container

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart collection-service

# Logs
docker-compose logs -f collection-service

# Shell nel container
docker-compose exec collection-service sh
```

## 🔍 Troubleshooting

### Container non si avvia
```bash
# Verifica logs
docker-compose logs collection-service

# Verifica variabili ambiente
docker-compose exec collection-service env
```

### Errore di connessione database
- Verifica `DATABASE_URL` nel file `.env`
- Controlla che l'IP del server sia whitelisted per il database remoto
- Verifica porta e credenziali

### Errore CORS
- Verifica che il dominio frontend sia in `CORS_ORIGINS`
- Il formato deve essere un array JSON valido

### Problemi JWT
- Verifica che `AUTH_JWKS_URL` sia raggiungibile
- Controlla che `JWT_AUDIENCE` e `JWT_ISSUER` matchino con l'issuer

## 📝 Note Importanti

⚠️ **NON committare mai file `.env` nel repository!**

✅ Il file `.dockerignore` esclude automaticamente `.env`

🔐 I segreti devono essere gestiti via variabili d'ambiente sul server

🌐 Configura HTTPS tramite reverse proxy (nginx/traefik) in production

## 📚 Documentazione API

Dopo il deploy, consulta la documentazione interattiva:
- Swagger UI: `http://your-server:8000/docs`
- ReDoc: `http://your-server:8000/redoc`

## 🤝 Support

Per problemi o domande:
1. Verifica i logs del container
2. Controlla le variabili d'ambiente
3. Consulta la documentazione Swagger
4. Controlla la connessione al database

