# Stack Flask + Redis — CRUD

Template minimale per avviare un'applicazione **Flask** (Python 3.12) con **Redis** (key-value store), e una piccola CRUD su una risorsa `items`.

Gli item vengono salvati come chiavi Redis `item:<id>` con valore JSON; un contatore `items:counter` genera gli id.

## Struttura

```
flask-redis/
├── README.md
├── docker-compose.yml   # servizi app + redis
├── Dockerfile           # immagine Python + Flask
├── app.py               # route web e API
├── db.py                # accesso a Redis (chiavi item:*) 
├── requirements.txt     # flask, redis
└── templates/
    └── index.html       # pagina HTML che usa l'API via JS
```

## docker-compose.yml

```yaml
services:
  app:
    build: .
    container_name: flask-redis-app
    ports:
      - "5020:5000"
    environment:
      REDIS_HOST: redis
      REDIS_PORT: 6379
    depends_on:
      redis:
        condition: service_healthy

  redis:
    image: redis:7-alpine
    container_name: flask-redis-db
    ports:
      - "6380:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  redis-data:
```

## Concetti toccati

- **Build** — `build: .` esegue il `Dockerfile` che installa Flask e il client `redis`.
- **Port mapping** — `"5020:5000"` espone l'app; `"6380:6379"` espone Redis.
- **Variabili d'ambiente** — `REDIS_HOST` e `REDIS_PORT` vengono lette da `db.py`.
- **Volume nominato** — `redis-data` (montato in `/data`) rende i dati persistenti.
- **Healthcheck** — l'app attende che `redis-cli ping` risponda prima di partire.

## API CRUD (items)

| Metodo | Endpoint | Descrizione |
|---|---|---|
| `GET` | `/api/items` | Lista |
| `POST` | `/api/items` | Crea (`{"title", "note"}`) |
| `GET` | `/api/items/:id` | Singolo |
| `PUT` | `/api/items/:id` | Modifica (`{"title", "note"}`) |
| `DELETE` | `/api/items/:id` | Elimina |

Al primo avvio viene inserito un item di esempio (se `items:counter` non esiste).

## Comandi

```bash
# avviare (compila l'immagine la prima volta)
docker compose up --build

# aprire l'interfaccia web
# http://localhost:5020

# esempi con curl
curl http://localhost:5020/api/items
curl -X POST -H "Content-Type: application/json" -d '{"title":"Ciao","note":"da curl"}' http://localhost:5020/api/items
curl http://localhost:5020/api/items/1
curl -X PUT -H "Content-Type: application/json" -d '{"title":"Aggiornato","note":"ok"}' http://localhost:5020/api/items/1
curl -X DELETE http://localhost:5020/api/items/1

# ispezionare Redis dall'host (porta 6380)
docker compose exec redis redis-cli keys 'item:*'

# stato e log
docker compose ps
docker compose logs -f

# fermare tutto
docker compose down

# fermare ed eliminare anche i volumi (perde i dati)
docker compose down -v
```