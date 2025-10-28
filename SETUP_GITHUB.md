# 🚀 Setup Repository GitHub per Deploy

## ✅ Checklist Pre-Commit

Prima di fare commit e push su GitHub, verifica:

### ✅ File Da Committare

- [x] `app/` - Tutto il codice sorgente
- [x] `migrations/` - Script Alembic
- [x] `tests/` - Test suite
- [x] `docker-compose.yml` - Configurazione deploy (SENZA credenziali)
- [x] `Dockerfile` - Immagine Docker
- [x] `.dockerignore` - File da escludere nel build
- [x] `requirements.txt` - Dipendenze Python
- [x] `alembic.ini` - Configurazione Alembic
- [x] `env.example` - Template variabili ambiente
- [x] `README.md` - Documentazione tecnica
- [x] `README_REPO.md` - Guida repository
- [x] `README_DEPLOY.md` - Guida deploy Hostinger
- [x] `pytest.ini` - Configurazione test
- [x] `.gitignore` - File da ignorare

### ❌ File Da NON Committare

- [ ] `.env` - **VIETATO!** Contiene credenziali
- [ ] `__pycache__/` - Escluso da `.gitignore`
- [ ] `*.log` - Escluso da `.gitignore`
- [ ] `*.sql` - Non necessario (tabella già creata)
- [ ] File di test temporanei

## 📋 Procedura

### 1. Inizializza Repository Git

```bash
# Se non hai già git init
git init

# Aggiungi origin
git remote add origin https://github.com/your-username/collection-service.git
```

### 2. Aggiungi e Committa

```bash
# Aggiungi tutti i file
git add .

# Verifica cosa stai commitando (NON deve esserci .env!)
git status

# Commit iniziale
git commit -m "Initial commit: Collection Service ready for deploy"

# Push su GitHub
git branch -M main
git push -u origin main
```

### 3. Ottieni URL per Deploy

Dopo il push:

1. Vai su GitHub nel repository
2. Apri il file `docker-compose.yml`
3. Clicca su "Raw" (pulsante in alto a destra)
4. Copia l'URL completo dalla barra degli indirizzi

**URL sarà simile a:**
```
https://raw.githubusercontent.com/your-username/collection-service/main/docker-compose.yml
```

### 4. Deploy su Hostinger

1. Accedi al pPanel Hostinger
2. Vai su VPS > Componi da URL
3. Incolla l'URL del docker-compose.yml
4. Clicca "Deploy"

### 5. Configura Variabili Ambiente

**⚠️ CRITICO:** Dopo il deploy, connetti via SSH e configura `.env`:

```bash
# Connetti via SSH
ssh your-user@your-server-ip

# Trova la directory di deploy
cd /root  # oppure dove Hostinger ha deployato

# Crea .env
cat > .env << 'EOF'
DATABASE_URL=mysql+asyncmy://u792485705_tyts:oA5843eC@srv1502.hstgr.io:3306/u792485705_maintyt
AUTH_JWKS_URL=https://auth.takeyourtrade.com/.well-known/jwks.json
JWT_AUDIENCE=collection-service
JWT_ISSUER=https://auth.takeyourtrade.com
CORS_ORIGINS=["https://app.takeyourtrade.com","https://takeyourtrade.com","https://www.takeyourtrade.com"]
APP_NAME=Collection Service
APP_VERSION=1.0.0
DEBUG=false
EOF

# Restart container con le nuove variabili
docker-compose down
docker-compose up -d

# Applica migrazioni (se necessario)
docker-compose exec collection-service alembic upgrade head
```

## 🔍 Verifica Post-Deploy

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f collection-service

# Test endpoint
curl http://localhost:8000/health

# Verifica variabili ambiente
docker-compose exec collection-service env | grep -E '(DATABASE_URL|CORS|JWT)'
```

## 🌐 CORS Configuration

Il servizio è configurato per accettare richieste da:
- ✅ `https://app.takeyourtrade.com`
- ✅ `https://takeyourtrade.com`
- ✅ `https://www.takeyourtrade.com`

**Se hai altri domini frontend, aggiungili a `CORS_ORIGINS` nel file `.env` sul server.**

## 🐛 Troubleshooting

### Container non si avvia
```bash
docker-compose logs collection-service
```

### Errore database
- Verifica `DATABASE_URL` nel `.env`
- Controlla che IP VPS sia whitelisted per il DB remoto

### Errore CORS
- Verifica formato JSON in `CORS_ORIGINS`
- Aggiungi tutti i domini necessari

## 📝 Note Importanti

1. **NON** committare mai il file `.env` - è già nel `.gitignore`
2. Le credenziali devono essere configurate **sul server** via `.env`
3. Le migrazioni vanno eseguite **dopo** il deploy
4. Testa sempre il health check dopo il deploy
5. Se modifichi CORS, riavvia il container

## 🎯 Risultato Atteso

Dopo tutti i passaggi, dovresti avere:
- ✅ Container `collection_service` running
- ✅ API accessibile su `http://your-server-ip:8000`
- ✅ Documentazione su `http://your-server-ip:8000/docs`
- ✅ Health check OK su `http://your-server-ip:8000/health`

## 🔒 Sicurezza

- Tutti i segreti sono nel `.env` (non nel repo)
- Container esegue con user non-root
- Health checks attivi
- CORS configurato solo per domini autorizzati

