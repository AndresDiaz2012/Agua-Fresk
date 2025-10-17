# WaterCRM

Sistema inteligente para gestión de clientes en empresa de purificación y distribución de agua.

## Backend
- Django + DRF + JWT
- Apps: `accounts`, `customers`, `dispatches`, `messaging`
- OpenAPI: `/api/docs/`

### Desarrollo local
```bash
# Variables
cp backend/.env backend/.env.local

# Migraciones
PYTHONPATH=backend python3 backend/manage.py migrate
PYTHONPATH=backend python3 backend/manage.py runserver 0.0.0.0:8000
```

## Frontend
- React + Vite + TS
- Configurado con React Router y React Query

### Desarrollo
```bash
cd frontend
npm install
npm run dev
```

## Docker Compose
```bash
cd deploy
docker compose up --build
```
Servicios:
- db: Postgres
- redis: Redis
- backend: Gunicorn en :8000
- worker/beat: Celery
- frontend: build estático
- nginx: sirve frontend y proxy `/api/`

## WhatsApp Business API
- Configurar en `backend/.env`:
  - `WHATSAPP_PHONE_NUMBER_ID`
  - `WHATSAPP_TOKEN`
  - `WHATSAPP_VERIFY_TOKEN`

## Pruebas
- Backend: `pytest` o `python manage.py test` (pendiente añadir casos)
- Frontend: `vitest` (pendiente)
