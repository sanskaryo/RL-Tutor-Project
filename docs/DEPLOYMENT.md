# Deployment Guide - RL Educational Tutor

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Database Migration](#database-migration)
5. [Environment Variables](#environment-variables)
6. [Production Checklist](#production-checklist)

---

## Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_db.py

# Start server
uvicorn main:app --reload
```

Backend will run on: http://localhost:8000
API Docs: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to project root
cd mini_project

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# Start development server
npm run dev
```

Frontend will run on: http://localhost:3000

---

## Backend Deployment

### Option 1: Railway (Recommended)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   ```

3. **Configure Environment Variables**
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-super-secret-key-min-32-chars
   BACKEND_CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Add Procfile**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### Option 2: Render

1. **Create Render Account**
   - Go to https://render.com

2. **Create Web Service**
   - Connect your GitHub repository
   - Select backend directory as root

3. **Configure Build**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**
   - Go to Environment tab
   - Add all required variables (see below)

5. **Add PostgreSQL Database**
   - Create new PostgreSQL database
   - Copy DATABASE_URL to environment variables

### Option 3: AWS EC2

1. **Launch EC2 Instance**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv nginx -y
   
   # Clone repository
   git clone your-repo-url
   cd your-repo/backend
   
   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Install Gunicorn
   pip install gunicorn
   ```

2. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/rl-tutor.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=RL Tutor FastAPI Application
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/your-repo/backend
   Environment="PATH=/home/ubuntu/your-repo/backend/venv/bin"
   ExecStart=/home/ubuntu/your-repo/backend/venv/bin/gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Start Service**
   ```bash
   sudo systemctl start rl-tutor
   sudo systemctl enable rl-tutor
   ```

4. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/rl-tutor
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   
   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/rl-tutor /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## Frontend Deployment

### Vercel (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd mini_project
   vercel
   ```

4. **Configure Environment Variables**
   - Go to Vercel Dashboard
   - Project Settings → Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1
     ```

5. **Redeploy**
   ```bash
   vercel --prod
   ```

### Alternative: Netlify

1. **Build Settings**
   ```
   Build Command: npm run build
   Publish Directory: .next
   ```

2. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url/api/v1
   ```

---

## Database Migration

### From SQLite to PostgreSQL

1. **Backup SQLite Data**
   ```bash
   python export_data.py > data_backup.json
   ```

2. **Update config.py**
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@host:5432/dbname")
   ```

3. **Create Tables**
   ```bash
   python -c "from app.core.database import init_db; init_db()"
   ```

4. **Import Data**
   ```bash
   python import_data.py data_backup.json
   ```

---

## Environment Variables

### Backend (.env)

```bash
# App Config
PROJECT_NAME="RL Educational Tutor"
API_V1_STR="/api/v1"

# Security
SECRET_KEY="your-super-secret-key-must-be-at-least-32-characters-long"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="postgresql://user:password@host:5432/database"
# Or for SQLite (development):
# DATABASE_URL="sqlite:///./tutor.db"

# CORS
BACKEND_CORS_ORIGINS=["https://your-frontend.vercel.app", "http://localhost:3000"]

# RL Agent
RL_EXPLORATION_RATE=0.1
RL_LEARNING_RATE=0.1
RL_DISCOUNT_FACTOR=0.9
```

### Frontend (.env.local)

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1
NEXT_PUBLIC_API_BASE=https://your-backend.railway.app

# Optional: Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

---

## Production Checklist

### Backend

- [ ] Use PostgreSQL instead of SQLite
- [ ] Set strong SECRET_KEY (32+ characters)
- [ ] Enable HTTPS/SSL
- [ ] Configure proper CORS origins
- [ ] Set up database backups
- [ ] Enable logging and monitoring
- [ ] Rate limiting configured
- [ ] Error tracking (Sentry)
- [ ] Health check endpoint working
- [ ] Load testing completed

### Frontend

- [ ] Environment variables set
- [ ] Build optimized for production
- [ ] Static assets cached
- [ ] Error boundaries implemented
- [ ] Loading states added
- [ ] SEO metadata configured
- [ ] Analytics integrated
- [ ] Performance testing done
- [ ] Cross-browser tested
- [ ] Mobile responsive

### Security

- [ ] All secrets in environment variables
- [ ] No hardcoded credentials
- [ ] HTTPS enforced
- [ ] Rate limiting active
- [ ] SQL injection protection (SQLAlchemy ORM)
- [ ] XSS protection (React/Next.js default)
- [ ] CSRF tokens if needed
- [ ] Dependency vulnerabilities checked

### Monitoring

- [ ] Application logs configured
- [ ] Error tracking (Sentry/Rollbar)
- [ ] Performance monitoring (New Relic/Datadog)
- [ ] Uptime monitoring (UptimeRobot/Pingdom)
- [ ] Database monitoring
- [ ] API response time tracking

---

## Docker Deployment

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/rl_tutor
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    command: uvicorn main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./mini_project
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=rl_tutor
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Troubleshooting

### Backend Issues

**Database connection error**
```bash
# Check DATABASE_URL format
# PostgreSQL: postgresql://user:pass@host:5432/db
# SQLite: sqlite:///./database.db
```

**Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Port already in use**
```bash
# Kill process on port 8000
# Windows: netsh interface ipv4 show excludedportrange protocol=tcp
# Linux: lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**API connection error**
- Check NEXT_PUBLIC_API_URL is correct
- Verify backend CORS settings include frontend URL
- Check browser console for errors

**Build failures**
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

---

## Support

For issues or questions:
- Check TODO.txt for project status
- Review INTEGRATION.md for API examples
- See backend/README.md for API documentation
- Check logs: `docker-compose logs` or `tail -f logs/app.log`

---

## Quick Start Commands

```bash
# Development
cd backend && uvicorn main:app --reload  # Terminal 1
cd mini_project && npm run dev            # Terminal 2

# Production Docker
docker-compose up -d

# Deploy
vercel --prod              # Frontend
railway up                 # Backend
```

---

*Last Updated: October 22, 2025*
