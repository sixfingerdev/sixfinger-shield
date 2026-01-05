# 🖐️ SixFinger Shield

**Open-source bot detection & device recognition with full authentication and payment system.** Collects 15+ browser signals (canvas, WebGL, audio, fonts, hardware...) to generate a unique 32-char hash.

[![CI/CD Pipeline](https://github.com/sixfingerdev/sixfinger-shield/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/sixfingerdev/sixfinger-shield/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🚀 Features

- **`@sixfinger/core`**: Single `getFingerprint()` function, client-side only
- **15+ Browser Signals**: Canvas, WebGL, Audio, Fonts, Hardware, Screen, Browser info, Timezone, Plugins, Touch, Battery, Network, Media devices, Color depth, DNT
- **Flask API Backend**: Full-featured Flask application with PostgreSQL for bot detection
- **User Authentication**: Complete signup/login system with password hashing
- **Admin Panel**: Flask-Admin dashboard for managing users, credits, and fingerprints
- **Credit System**: Pay-per-use API with credit balance tracking
- **Stripe Integration**: Secure payment processing for credit purchases
- **API Key Management**: Create and manage multiple API keys per user
- **Rate Limiting**: Built-in protection with Flask-Limiter and Redis
- **Live Demo UI**: Next.js 14 + TypeScript + Tailwind CSS
- **Production Ready**: Docker + Docker Compose + Database migrations
- **CI/CD Ready**: GitHub Actions workflow included

## 🏗️ Architecture

**Stack:**
- **Core**: TypeScript library
- **Backend**: Flask (Python) + PostgreSQL + Redis + Stripe
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Infrastructure**: Docker + Docker Compose + Alembic migrations

## 📦 Installation

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)
- Stripe Account (for payment processing)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/sixfingerdev/sixfinger-shield.git
cd sixfinger-shield

# Setup environment variables
cp .env.example .env
# Edit .env with your database, Redis, and Stripe credentials

# Start all services
docker-compose up -d

# Create admin user
docker-compose exec backend python create_admin.py

# Access the application
# Backend: http://localhost:5000
# Admin Panel: http://localhost:5000/admin
# Frontend: http://localhost:3000
```

### Manual Installation

#### 1. Install Core Package

```bash
cd packages/core
npm install
npm run build
npm test
```

#### 2. Setup Backend (Flask)

```bash
cd apps/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp ../../.env.example ../../.env
# Edit .env with your configuration

# Setup database
createdb sixfinger
alembic upgrade head

# Create admin user
python create_admin.py

# Start Flask server
python run.py
# Or use Gunicorn for production:
# gunicorn -w 4 -b 0.0.0.0:5000 "app.main:app"
```

#### 3. Setup Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

## 🔧 Usage

### Getting Started

1. **Sign Up**: Visit http://localhost:5000/auth/signup
   - Create an account (receives 100 free credits)
   
2. **Create API Key**: Visit http://localhost:5000/dashboard/api-keys
   - Generate an API key for your application
   
3. **Purchase Credits**: Visit http://localhost:5000/payment/credits
   - Buy credit packages via Stripe
   
4. **Use the API**: Submit fingerprints with your API key

### Core Library

```typescript
import { getFingerprint } from '@sixfinger/core';

async function identify() {
  const result = await getFingerprint();
  
  console.log('Hash:', result.hash); // 32-character unique hash
  console.log('Components:', result.components);
  
  // Submit to API for risk scoring with API key
  const response = await fetch('http://localhost:5000/api/fingerprint', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key-here'
    },
    body: JSON.stringify(result)
  });
  
  const data = await response.json();
  console.log('Risk Score:', data.risk_score);
  console.log('Is Bot:', data.is_bot);
  console.log('Credits Remaining:', data.credits_remaining);
}

identify();
```

### API Endpoints

All API endpoints (except authentication) require an API key in the `X-API-Key` header.

#### Authentication Endpoints

**POST `/auth/signup`**
Register a new user (receives 100 free credits)

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**POST `/auth/login`**
User login

```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### API Endpoints (Require API Key)

**POST `/api/fingerprint`** (Costs 1 credit)
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
  "first_seen": "2026-01-05T13:00:00Z",
  "credits_used": 1,
  "credits_remaining": 99
}
```

**GET `/api/fingerprint/{hash}`** (Free)
Get fingerprint information by hash

**GET `/api/risk-score/{hash}`** (Free)
Get detailed risk analysis with factors

#### Payment Endpoints

**GET `/payment/credits`**
View credit balance and purchase options

**POST `/payment/purchase`**
Create Stripe checkout session for credit purchase

**GET `/payment/history`**
View transaction history

### Credit Packages

- **Starter**: 1,000 credits - $10
- **Pro**: 5,000 credits - $40
- **Business**: 20,000 credits - $150

### Admin Panel

Access the admin panel at http://localhost:5000/admin

- Manage users
- View all fingerprints
- Monitor credit usage
- View transactions
- Manage API keys

Default admin credentials (change after first login):
- Email: admin@sixfinger.dev
- Password: admin123

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
# Backend (Flask)
DATABASE_URL=postgresql://user:pass@localhost:5432/sixfinger
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Stripe Payment
STRIPE_PUBLIC_KEY=pk_live_your_publishable_key
STRIPE_SECRET_KEY=sk_live_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Application URLs
BASE_URL=https://yourdomain.com
STRIPE_SUCCESS_URL=https://yourdomain.com/payment/success?session_id={CHECKOUT_SESSION_ID}
STRIPE_CANCEL_URL=https://yourdomain.com/payment/cancel

# Frontend
NEXT_PUBLIC_API_URL=https://yourdomain.com
```

### Production Deployment

1. Update `.env` with production values
2. Build Docker images: `docker-compose build`
3. Start services: `docker-compose up -d`
4. Run migrations: `docker-compose exec backend alembic upgrade head`
5. Create admin user: `docker-compose exec backend python create_admin.py`
6. Configure Stripe webhook:
   - Go to Stripe Dashboard → Webhooks
   - Add endpoint: `https://yourdomain.com/payment/webhook`
   - Select events: `checkout.session.completed`
   - Copy webhook secret to `.env`

### Production Server with Gunicorn

```bash
# In apps/backend directory
gunicorn -w 4 -b 0.0.0.0:5000 "app.main:app"
```

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
