# 🚀 URL per Deploy Hostinger

## ✅ Repository Pubblicato

Il codice è stato pushato con successo su GitHub:
**https://github.com/LCDT20/collection-service**

## 📋 URL da Usare su Hostinger "Componi da URL"

**Copia questo URL completo:**

```
https://raw.githubusercontent.com/LCDT20/collection-service/main/docker-compose.yml
```

## 🔐 Variabile d'Ambiente da Inserire

Quando Hostinger ti chiede di aggiungere variabili d'ambiente, inserisci:

**Nome Variabile:**
```
DATABASE_URL
```

**Valore:**
```
mysql+asyncmy://u792485705_tyts:oA5843eC@srv1502.hstgr.io:3306/u792485705_maintyt
```

## 📝 Procedura Completa Hostinger

1. Vai su **pPanel Hostinger**
2. Vai su **VPS** → **Componi da URL**
3. Incolla l'URL: `https://raw.githubusercontent.com/LCDT20/collection-service/main/docker-compose.yml`
4. Clicca **"Avanti"** o **"Continua"**
5. Inserisci la variabile `DATABASE_URL` con il valore sopra
6. Clicca **"Deploy"** o **"Applica"**
7. Aspetta che il build completi

## ✅ Verifica Post-Deploy

Dopo il deploy, verifica:

```bash
# Via SSH sul server
ssh your-user@your-server-ip

# Check container
docker ps | grep collection_service

# Test health
curl http://localhost:8000/health

# Controlla logs
docker logs collection_service
```

## 🌐 URLs Disponibili

Dopo il deploy:
- Health: `http://your-server-ip:8000/health`
- Docs: `http://your-server-ip:8000/docs`
- API: `http://your-server-ip:8000/api/v1/collections/items/`

## 📌 Checklist

- [x] Repository creato su GitHub
- [x] Codice pushato
- [x] Repository PUBLIC
- [ ] URL copiato per Hostinger
- [ ] Deploy eseguito su Hostinger
- [ ] Variabile DATABASE_URL inserita
- [ ] Container running
- [ ] Health check OK

## 🎉 Prossimo Step

Vai su Hostinger pPanel e usa "Componi da URL" con l'URL sopra!

