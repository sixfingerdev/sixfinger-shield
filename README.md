# 🖐️ SixFinger Shield

**Open-source bot detection & device recognition.** Collects 15+ browser signals (canvas, WebGL, audio, fonts, hardware...) to generate a unique 32-char hash.

[![CI/CD Pipeline](https://github.com/sixfingerdev/sixfinger-shield/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/sixfingerdev/sixfinger-shield/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🚀 Features

- **`@sixfinger/core`**: Single `getFingerprint()` function, client-side only
- **15+ Browser Signals**: Canvas, WebGL, Audio, Fonts, Hardware, Screen, Browser info, Timezone, Plugins, Touch, Battery, Network, Media devices, Color depth, DNT
- **Risk Scoring API**: FastAPI backend with PostgreSQL for bot detection
- **Rate Limiting**: Built-in protection with slowapi and Redis
- **Live Demo UI**: Next.js + Tailwind CSS + shadcn/ui components
- **Full Test Coverage**: Jest, pytest, and Playwright E2E tests
- **Production Ready**: Docker + Docker Compose + Database migrations
- **CI/CD Ready**: GitHub Actions workflow included

## 🏗️ Architecture

**Stack:**
- **Core**: TypeScript library
- **Backend**: FastAPI (Python) + PostgreSQL + Redis
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Infrastructure**: Docker + Docker Compose + Alembic migrations

## 📦 Installation

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/sixfingerdev/sixfinger-shield.git
cd sixfinger-shield

# Start all services
docker-compose up -d

# Access the demo
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Installation

#### 1. Install Core Package

```bash
cd packages/core
npm install
npm run build
npm test
```

#### 2. Setup Backend

```bash
cd apps/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb sixfinger
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### 3. Setup Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

## 🔧 Usage

### Core Library

```typescript
import { getFingerprint } from '@sixfinger/core';

async function identify() {
  const result = await getFingerprint();
  
  console.log('Hash:', result.hash); // 32-character unique hash
  console.log('Components:', result.components);
  
  // Submit to API for risk scoring
  const response = await fetch('http://localhost:8000/api/fingerprint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(result)
  });
  
  const data = await response.json();
  console.log('Risk Score:', data.risk_score);
  console.log('Is Bot:', data.is_bot);
}

identify();
```

### API Endpoints

#### POST `/api/fingerprint`
Submit a fingerprint for analysis

**Request:**
```json
{
  "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "components": {
    "canvas": "data:image/png;base64...",
    "webgl": "Intel Inc.~ANGLE",
    "audio": "48000_2048",
    "fonts": "Arial,Verdana",
    "hardware": "cores:8_mem:8_gpu:Intel",
    "screen": "1920x1080_1920x1040_24",
    "browser": "Mozilla/5.0...",
    "timezone": "America/New_York_300",
    "plugins": "Chrome PDF Plugin",
    "touch": "0_false",
    "battery": "true_100",
    "network": "4g_10_50",
    "media": "audioinput,videoinput",
    "colorDepth": "24_2",
    "doNotTrack": "unknown"
  }
}
```

**Response:**
```json
{
  "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "risk_score": 25.5,
  "is_bot": false,
  "visit_count": 1,
  "first_seen": "2026-01-05T13:00:00Z"
}
```

#### GET `/api/fingerprint/{hash}`
Get fingerprint information by hash

#### GET `/api/risk-score/{hash}`
Get detailed risk analysis with factors

**Response:**
```json
{
  "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "risk_score": 75.0,
  "is_bot": true,
  "confidence": 0.75,
  "factors": {
    "webgl_missing": true,
    "canvas_missing": true,
    "audio_missing": true,
    "hardware_unknown": true,
    "no_plugins": true
  }
}
```

## 🧪 Testing

### Core Library Tests

```bash
cd packages/core
npm test
npm test -- --coverage
```

### Backend Tests

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

## 📊 Browser Signals Collected

| Signal | Description | Bot Indicator |
|--------|-------------|---------------|
| Canvas | Canvas fingerprinting data | Unsupported/Error |
| WebGL | WebGL renderer and vendor | Unsupported/Error |
| Audio | Audio context fingerprint | Unsupported/Error |
| Fonts | Available system fonts | Empty/Missing |
| Hardware | CPU cores, memory, GPU | Unknown values |
| Screen | Screen resolution & color | Common bot resolutions |
| Browser | User agent & platform | Headless indicators |
| Timezone | Timezone & offset | Inconsistencies |
| Plugins | Browser plugins | None/Missing |
| Touch | Touch support | Desktop without touch |
| Battery | Battery status | Unsupported |
| Network | Network information | Unsupported |
| Media | Media devices | Missing |
| Color Depth | Color depth & pixel ratio | - |
| DNT | Do Not Track setting | Enabled |

## 🔒 Security & Privacy

- All fingerprinting is done **client-side only**
- No personal information is collected
- Hashes are one-way and cannot be reversed
- Rate limiting prevents abuse
- PostgreSQL for secure data storage
- Environment variables for sensitive configuration

## 🚢 Deployment

### Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/sixfinger
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
RATE_LIMIT=100/minute

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production Deployment

1. Update `.env` with production values
2. Build Docker images: `docker-compose build`
3. Start services: `docker-compose up -d`
4. Run migrations: `docker-compose exec backend alembic upgrade head`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FingerprintJS](https://github.com/fingerprintjs/fingerprintjs) for fingerprinting inspiration
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [shadcn/ui](https://ui.shadcn.com/) for UI components

## 📧 Contact

- GitHub: [@sixfingerdev](https://github.com/sixfingerdev)
- Project Link: [https://github.com/sixfingerdev/sixfinger-shield](https://github.com/sixfingerdev/sixfinger-shield)

---

**Production-ready with Docker & migrations** | **MIT License** | **Made with ❤️ by sixfingerdev**
