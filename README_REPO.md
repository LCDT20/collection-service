# Collection Service - Repository per Deploy

## 📦 Scopo del Repository

Questo repository contiene la configurazione Docker per il deploy automatico del **Collection Service** tramite Docker Compose.

## 🚀 Deploy con "Componi da URL"

### Per Hostinger VPS

1. **Ottieni l'URL del docker-compose.yml:**
   - Clicca su "Raw" per il file `docker-compose.yml` in questo repository
   - Copia l'URL completo dalla barra degli indirizzi

2. **Su Hostinger:**
   - Usa la funzione "Componi da URL"
   - Incolla l'URL del docker-compose.yml
   - Avvia il deploy

3. **⚠️ IMPORTANTE - Configurazione Post-Deploy:**
   
   ```bash
   # Connetti via SSH
   ssh user@your-server.com
   
   # Naviga nella directory di deploy
   cd /path/to/deployed/app
   
   # Crea file .env
   cp env.example .env
   nano .env
   
   # Inserisci TUTTE le variabili d'ambiente necessarie:
   # - DATABASE_URL (con credenziali database)
   # - AUTH_JWKS_URL
   # - JWT_AUDIENCE
   # - JWT_ISSUER
   # - CORS_ORIGINS (verifica i domini!)
   ```

4. **Restart con le nuove variabili:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

5. **Esegui le migrazioni del database:**
   ```bash
   docker-compose exec collection-service alembic upgrade head
   ```

## 🔒 Variabili d'Ambiente Richieste

Consulta `env.example` per il template completo.

**Campi obbligatori:**
- `DATABASE_URL`: Connessione MySQL completa
- `AUTH_JWKS_URL`: URL servizio autenticazione
- `JWT_AUDIENCE`: Audience JWT
- `JWT_ISSUER`: Issuer JWT

## 🌐 CORS Configuration

Il servizio è configurato per accettare richieste da:
- `https://app.takeyourtrade.com`
- `https://takeyourtrade.com`
- `https://www.takeyourtrade.com`

**Se devi aggiungere altri domini, modifica `CORS_ORIGINS` nel file `.env` sul server.**

## 📝 Note Sicurezza

⚠️ **Questo repository è pubblico. NON include:**
- File `.env` con credenziali
- Password o token
- Database credentials
- Informazioni sensibili

✅ **Tutti i segreti devono essere configurati sul server via variabili d'ambiente.**

## 📚 Documentazione

- **Setup dettagliato:** Vedi `README_DEPLOY.md`
- **Documentazione API:** Dopo deploy su `http://server:8000/docs`
- **Docker:** Vedi `Dockerfile` e `docker-compose.yml`

## 🔧 Struttura

```
.
├── app/                # Codice applicazione
├── migrations/         # Migrazioni database
├── Dockerfile          # Immagine Docker
├── docker-compose.yml  # Configurazione deploy
├── env.example         # Template variabili ambiente
└── requirements.txt    # Dipendenze Python
```

## 🆘 Troubleshooting

Vedi `README_DEPLOY.md` per problemi comuni e soluzioni.

## 📞 Support

Dopo il deploy, tutti gli endpoint sono disponibili su:
- API: `http://your-server:8000/api/v1/collections/items/`
- Docs: `http://your-server:8000/docs`

**Tutti gli endpoint richiedono JWT Bearer token nell'header Authorization.**

