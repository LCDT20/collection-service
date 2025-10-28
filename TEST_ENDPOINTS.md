# 🧪 Endpoint di Test per Collection Service

Dopo il deploy su Hostinger, puoi testare il sistema con questi endpoint:

## 🌐 URL Base
Sostituisci `your-server-ip` con l'IP della tua VPS Hostinger.

## 📋 Endpoint di Test

### 1. Health Check Base
```
GET http://your-server-ip:8000/health
```
**Risposta:**
```json
{
  "status": "healthy",
  "service": "Collection Service",
  "version": "1.0.0"
}
```

### 2. Test Database Connection
```
GET http://your-server-ip:8000/test/database
```
**Testa:** Connessione al database MySQL

**Risposta Successo:**
```json
{
  "status": "success",
  "database": "connected",
  "mysql_version": "11.8.3-MariaDB-log",
  "message": "Database connection successful"
}
```

**Risposta Errore:**
```json
{
  "status": "error",
  "database": "disconnected",
  "error": "Connection error details...",
  "message": "Database connection failed"
}
```

### 3. Test Configuration
```
GET http://your-server-ip:8000/test/config
```
**Testa:** Variabili d'ambiente e configurazione

**Risposta:**
```json
{
  "status": "success",
  "config": {
    "app_name": "Collection Service",
    "app_version": "1.0.0",
    "debug": false,
    "has_database_url": true,
    "auth_jwks_url": "https://auth.takeyourtrade.com/.well-known/jwks.json",
    "jwt_audience": "collection-service",
    "jwt_issuer": "https://auth.takeyourtrade.com",
    "cors_origins": [
      "https://app.takeyourtrade.com",
      "https://takeyourtrade.com",
      "https://www.takeyourtrade.com",
      "http://localhost:3000"
    ]
  }
}
```

### 4. Test Completo Sistema
```
GET http://your-server-ip:8000/test/full
```
**Testa:** Database + Configurazione in un unico endpoint

**Risposta:**
```json
{
  "service": "Collection Service",
  "version": "1.0.0",
  "timestamp": "2025-01-28 10:30:00.123456",
  "tests": {
    "database": {
      "status": "success",
      "mysql_version": "11.8.3-MariaDB-log",
      "current_database": "u792485705_maintyt"
    },
    "configuration": {
      "status": "success",
      "has_database_url": true,
      "cors_configured": true,
      "jwt_configured": true
    }
  },
  "overall_status": "healthy"
}
```

## 🧪 Come Testare

### Via Browser
Apri direttamente nel browser:
```
http://your-server-ip:8000/health
http://your-server-ip:8000/test/database
http://your-server-ip:8000/test/config
http://your-server-ip:8000/test/full
```

### Via cURL (SSH sul server)
```bash
curl http://localhost:8000/health
curl http://localhost:8000/test/database
curl http://localhost:8000/test/config
curl http://localhost:8000/test/full
```

### Via Postman/Insomnia
- Imposta metodo: GET
- Inserisci l'URL completo
- Nessun header richiesto per questi endpoint

## ✅ Checklist Test

Dopo il deploy, testa in ordine:

1. ✅ **Health Check** - Verifica che il servizio sia up
   ```
   GET /health
   ```

2. ✅ **Config Test** - Verifica le variabili d'ambiente
   ```
   GET /test/config
   ```

3. ✅ **Database Test** - Verifica connessione database
   ```
   GET /test/database
   ```

4. ✅ **Full Test** - Test completo di tutto
   ```
   GET /test/full
   ```

## 🐛 Troubleshooting

### Errore Database
Se `/test/database` fallisce:
- Verifica che DATABASE_URL sia corretta nel docker-compose.yml
- Controlla che l'IP della VPS sia whitelisted per il database
- Verifica logs: `docker logs collection_service`

### Errore Config
Se `/test/config` mostra valori mancanti:
- Verifica che il container sia ripartito dopo modifiche
- Controlla le variabili nel docker-compose.yml
- Rebuild: `docker-compose up -d --build`

## 📚 Documentazione API Completa

Dopo il deploy, consulta anche:
- **Swagger UI**: `http://your-server-ip:8000/docs`
- **ReDoc**: `http://your-server-ip:8000/redoc`

Qui troverai tutti gli endpoint disponibili, inclusi quelli per la gestione dei collection items (richiedono JWT Bearer token).

## 🔒 Endpoint API Richiedono Auth

Gli endpoint di test sono **pubblici** (nessuna autenticazione richiesta).

Gli endpoint dell'API (`/api/v1/collections/items/*`) richiedono invece:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

