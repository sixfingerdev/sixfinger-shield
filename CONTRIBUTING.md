# SixFinger Shield

Simple browser fingerprinting demonstration.

## Quick Start

```bash
# With Docker
docker-compose up -d

# Without Docker
cd packages/core && npm install && npm run build
cd apps/backend && pip install -r requirements.txt && uvicorn app.main:app
cd apps/frontend && npm install && npm run dev
```

Visit http://localhost:3000
