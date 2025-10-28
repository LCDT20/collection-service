# ✅ Pronto per Deploy su Hostinger!

## 🚀 Variabili Incluse nel docker-compose.yml

Il file `docker-compose.yml` è stato aggiornato e include **TUTTE** le variabili d'ambiente necessarie direttamente nel file. Non devi inserire nulla manualmente su Hostinger!

## 📋 URL per Deploy

**Copia e usa questo URL su Hostinger:**

```
https://raw.githubusercontent.com/LCDT20/collection-service/main/docker-compose.yml
```

## ⚙️ Variabili Incluse

✅ **DATABASE_URL** - Database MySQL con credenziali  
✅ **AUTH_JWKS_URL** - URL servizio autenticazione JWT  
✅ **JWT_AUDIENCE** - Audience token  
✅ **JWT_ISSUER** - Issuer token  
✅ **CORS_ORIGINS** - Domini autorizzati (takeyourtrade.com, localhost)  
✅ **APP_NAME** - Nome servizio  
✅ **APP_VERSION** - Versione  
✅ **DEBUG** - Modalità produzione (false)  

## 🎯 Procedura Hostinger

1. Vai su **pPanel Hostinger**
2. Vai su **VPS** → **Componi da URL**
3. Incolla: `https://raw.githubusercontent.com/LCDT20/collection-service/main/docker-compose.yml`
4. Clicca **"Deploy"** o **"Applica"**
5. **NON è necessario inserire variabili d'ambiente!**
6. Aspetta che il build completi

## ✅ Verifica Post-Deploy

```bash
# Connetti via SSH
ssh your-user@your-server

# Controlla container
docker ps | grep collection_service

# Test health check
curl http://localhost:8000/health
```

## 🌐 URLs Disponibili

- Health: `http://your-server-ip:8000/health`
- Docs: `http://your-server-ip:8000/docs`
- ReDoc: `http://your-server-ip:8000/redoc`
- API: `http://your-server-ip:8000/api/v1/collections/items/`

## 🔒 Sicurezza Note

- Le credenziali sono ora nel docker-compose.yml pubblico
- Il repository è pubblico (richiesto per Componi da URL)
- In produzione considera di:
  - Rendere il repository privato dopo il primo deploy
  - Usare variabili d'ambiente sul server invece di hard-coded values
  - Ruotare le password periodicamente

## 🎉 Tutto Pronto!

Vai su Hostinger e usa "Componi da URL" con l'URL sopra. Non serve configurazione aggiuntiva!

