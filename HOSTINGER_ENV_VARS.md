# 🔐 Variabili d'Ambiente per Hostinger "Componi da URL"

## ⚙️ Configurazione Variabili

Quando usi "Componi da URL" su Hostinger VPS, ti verrà chiesto di inserire le variabili d'ambiente. Ecco cosa inserire:

## 📋 Variabili Richieste

### 1. DATABASE_URL (OBBLIGATORIO)
```
DATABASE_URL=mysql+asyncmy://u792485705_tyts:oA5843eC@srv1502.hstgr.io:3306/u792485705_maintyt
```

### 2. AUTH_JWKS_URL (Opzionale - ha default)
```
AUTH_JWKS_URL=https://auth.takeyourtrade.com/.well-known/jwks.json
```

### 3. JWT_AUDIENCE (Opzionale - ha default)
```
JWT_AUDIENCE=collection-service
```

### 4. JWT_ISSUER (Opzionale - ha default)
```
JWT_ISSUER=https://auth.takeyourtrade.com
```

### 5. CORS_ORIGINS (Opzionale - ha default)
```
CORS_ORIGINS=["https://app.takeyourtrade.com","https://takeyourtrade.com","https://www.takeyourtrade.com"]
```

### 6. DEBUG (Opzionale - default: false)
```
DEBUG=false
```

## 🎯 Configurazione Minima Necessaria

Per far funzionare il servizio, è **OBBLIGATORIO** inserire solo:

```
DATABASE_URL=mysql+asyncmy://u792485705_tyts:oA5843eC@srv1502.hstgr.io:3306/u792485705_maintyt
```

Tutte le altre variabili hanno valori di default che funzioneranno.

## 📝 Come Inserire su Hostinger

Quando Hostinger ti chiede di aggiungere variabili d'ambiente:

1. **Nome Variabile**: `DATABASE_URL`
   **Valore**: `mysql+asyncmy://u792485705_tyts:oA5843eC@srv1502.hstgr.io:3306/u792485705_maintyt`

2. (Opzionale) Aggiungi altre variabili se vuoi sovrascrivere i default

3. Clicca "Deploy" o "Applica"

## ⚠️ Note Importanti

- **DATABASE_URL è l'unica obbligatoria** - senza questa non funziona nulla
- Le altre variabili hanno valori di default che vanno bene per la produzione
- CORS è già configurato per i domini takeyourtrade.com
- DEBUG=false in produzione (non mostra dettagli errori)

## 🔍 Verifica Post-Deploy

Dopo il deploy:

```bash
# Connetti via SSH
ssh your-user@your-server

# Verifica che il container sia running
docker ps | grep collection_service

# Controlla i logs
docker logs collection_service

# Test health check
curl http://localhost:8000/health
```

## 🌐 URL API

Dopo il deploy, l'API sarà disponibile su:
- Health: `http://your-server-ip:8000/health`
- Docs: `http://your-server-ip:8000/docs`
- API: `http://your-server-ip:8000/api/v1/collections/items/`

## 🔧 Modifiche Post-Deploy

Se devi modificare variabili dopo il deploy:

### Metodo 1: Tramite interfaccia Hostinger
- Vai nelle impostazioni del container
- Modifica le variabili d'ambiente
- Riavvia il container

### Metodo 2: Via SSH
```bash
# Connetti via SSH
ssh your-user@your-server

# Modifica il file .env nella directory di deploy
nano .env

# Riavvia
docker-compose down
docker-compose up -d
```

## 🔒 Sicurezza

- Le credenziali sono cifrate da Hostinger
- NON inserire mai variabili d'ambiente nel repository Git
- Il file `.env` è escluso dal repository (vedi `.gitignore`)

