# Quick Start Guide

## Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose (recommended)

## Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/sixfingerdev/sixfinger-shield.git
cd sixfinger-shield

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Access the applications
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Option 2: Manual Setup

### 1. Install Core Package

```bash
cd packages/core
npm install
npm run build
npm test
```

### 2. Setup Backend

```bash
cd ../../apps/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL database
createdb sixfinger

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Set API URL
export NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Visit http://localhost:3000

## Testing

### Core Library

```bash
cd packages/core
npm test
npm test -- --coverage
```

### Backend

```bash
cd apps/backend
pytest
pytest --cov=app
```

### E2E Tests

```bash
cd tests
npm install
npx playwright install
npm run test:e2e
```

## Using the Core Library

```typescript
import { getFingerprint } from '@sixfinger/core';

async function identify() {
  const result = await getFingerprint();
  console.log('Fingerprint:', result.hash);
  
  // Submit to API
  const response = await fetch('http://localhost:8000/api/fingerprint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(result)
  });
  
  const data = await response.json();
  console.log('Risk Score:', data.risk_score);
  console.log('Is Bot:', data.is_bot);
}
```

## API Endpoints

- `POST /api/fingerprint` - Submit fingerprint for analysis
- `GET /api/fingerprint/{hash}` - Get fingerprint info
- `GET /api/risk-score/{hash}` - Get detailed risk analysis
- `GET /health` - Health check
- `GET /docs` - API documentation

## Production Deployment

1. Update `.env` with production values
2. Build Docker images: `docker-compose build`
3. Start services: `docker-compose up -d`
4. Run migrations: `docker-compose exec backend alembic upgrade head`

## Troubleshooting

### Port already in use
```bash
# Change ports in docker-compose.yml or stop conflicting services
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:8000 | xargs kill -9  # Backend
```

### Database connection errors
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres
```

### Frontend build errors
```bash
# Clean and rebuild
cd apps/frontend
rm -rf .next node_modules
npm install
npm run build
```

## Support

- GitHub Issues: [Report a bug](https://github.com/sixfingerdev/sixfinger-shield/issues)
- Documentation: [Full README](../README.md)
