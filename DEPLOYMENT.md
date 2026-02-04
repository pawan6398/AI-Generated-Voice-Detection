# 🚀 Deployment Guide - AI Voice Detection API

This guide covers deploying your AI Voice Detection API to various cloud platforms.

---

## 📋 Pre-Deployment Checklist

- [ ] Code tested locally
- [ ] Model trained and saved (`models/classifier.pkl`)
- [ ] Environment variables configured
- [ ] Dependencies up to date (`requirements.txt`)
- [ ] Docker image builds successfully (if using Docker)
- [ ] API key secured (never commit to git)

---

## 🌐 Deployment Options

### Option 1: Railway.app (Recommended - Easiest)

**Pros:** Free tier, automatic deployments, easy setup
**Best for:** Quick deployment, prototypes, small projects

#### Steps:

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize Project**
```bash
cd AI-Generated-Voice-Detection-Multi-Language-
railway init
```

4. **Set Environment Variables**
```bash
railway variables set API_KEY="your-production-api-key"
```

5. **Deploy**
```bash
railway up
```

6. **Get URL**
```bash
railway domain
```

Your API will be available at: `https://your-app.railway.app`

---

### Option 2: Render.com

**Pros:** Free tier, simple interface, auto-deploy from Git
**Best for:** Production apps, continuous deployment

#### Steps:

1. **Push code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Create `render.yaml`** (Already included in project)

3. **Go to** [render.com](https://render.com)

4. **Click "New +" → "Web Service"**

5. **Connect GitHub repository**

6. **Configure:**
   - Environment: Docker
   - Build Command: (auto-detected from Dockerfile)
   - Start Command: (auto-detected)

7. **Add Environment Variables:**
   - `API_KEY`: your-production-api-key

8. **Click "Create Web Service"**

Your API will be at: `https://your-service.onrender.com`

---

### Option 3: Google Cloud Run

**Pros:** Scalable, pay-per-use, Google infrastructure
**Best for:** Production, high traffic, enterprise

#### Steps:

1. **Install Google Cloud SDK**
```bash
# Download from: https://cloud.google.com/sdk/docs/install
```

2. **Login and Set Project**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

3. **Enable APIs**
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

4. **Build and Push Image**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/voice-detection-api
```

5. **Deploy**
```bash
gcloud run deploy voice-detection-api \
  --image gcr.io/YOUR_PROJECT_ID/voice-detection-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY="your-production-api-key" \
  --memory 2Gi \
  --cpu 2
```

6. **Get URL**
```bash
gcloud run services describe voice-detection-api --region us-central1
```

---

### Option 4: AWS Elastic Beanstalk

**Pros:** Auto-scaling, load balancing, AWS ecosystem
**Best for:** Enterprise, AWS infrastructure

#### Steps:

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB**
```bash
eb init -p docker voice-detection-api
```

3. **Create Environment**
```bash
eb create voice-detection-env
```

4. **Set Environment Variables**
```bash
eb setenv API_KEY="your-production-api-key"
```

5. **Deploy**
```bash
eb deploy
```

6. **Open Application**
```bash
eb open
```

---

### Option 5: Heroku

**Pros:** Easy deployment, add-ons ecosystem
**Best for:** Quick deployment, startups

#### Steps:

1. **Install Heroku CLI**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login**
```bash
heroku login
```

3. **Create App**
```bash
heroku create voice-detection-api
```

4. **Set Environment Variables**
```bash
heroku config:set API_KEY="your-production-api-key"
```

5. **Deploy**
```bash
git push heroku main
```

6. **Open App**
```bash
heroku open
```

---

### Option 6: DigitalOcean App Platform

**Pros:** Simple, predictable pricing, good docs
**Best for:** Small to medium apps

#### Steps:

1. **Go to** [cloud.digitalocean.com](https://cloud.digitalocean.com)

2. **Create → Apps → GitHub Repository**

3. **Select Repository:** AI-Generated-Voice-Detection-Multi-Language-

4. **Configure:**
   - Type: Web Service
   - Environment: Docker
   - HTTP Port: 8000

5. **Add Environment Variables:**
   - `API_KEY`: your-production-api-key

6. **Click "Create Resources"**

---

### Option 7: Azure Container Instances

**Pros:** Quick container deployment, Azure ecosystem
**Best for:** Azure users, containerized apps

#### Steps:

1. **Install Azure CLI**
```bash
# Download from: https://docs.microsoft.com/cli/azure/install-azure-cli
```

2. **Login**
```bash
az login
```

3. **Create Resource Group**
```bash
az group create --name voice-detection-rg --location eastus
```

4. **Create Container Registry**
```bash
az acr create --resource-group voice-detection-rg \
  --name voicedetectionacr --sku Basic
```

5. **Build Image**
```bash
az acr build --registry voicedetectionacr \
  --image voice-detection-api:latest .
```

6. **Deploy Container**
```bash
az container create --resource-group voice-detection-rg \
  --name voice-detection-api \
  --image voicedetectionacr.azurecr.io/voice-detection-api:latest \
  --cpu 2 --memory 4 \
  --ports 8000 \
  --dns-name-label voice-detection-api \
  --environment-variables API_KEY="your-production-api-key"
```

---

## 🐳 Docker Deployment

### Local Docker

```bash
# Build image
docker build -t voice-detection-api .

# Run container
docker run -d -p 8000:8000 \
  -e API_KEY="your-api-key" \
  --name voice-api \
  voice-detection-api

# Check logs
docker logs voice-api

# Stop container
docker stop voice-api
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## 🔐 Security Best Practices

### 1. API Key Management

**Never hardcode API keys!**

Use environment variables:
```bash
# Development
export API_KEY="dev-key-12345"

# Production (set in cloud platform)
# Use secrets management service
```

### 2. HTTPS Only
Configure your cloud platform to enforce HTTPS.

### 3. Rate Limiting
Add rate limiting to prevent abuse:
```python
# Already shown in the main guide
```

### 4. CORS Configuration
Update `app/main.py` CORS settings for production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### 5. Input Validation
- File size limits (already implemented)
- Audio format validation
- Request rate limiting

---

## 📊 Monitoring & Logging

### Health Check Endpoint
```bash
curl https://your-api.com/health
```

### Application Logs

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Google Cloud:**
```bash
gcloud run services logs read voice-detection-api
```

### Monitoring Services

1. **Sentry** - Error tracking
2. **DataDog** - Application monitoring
3. **New Relic** - Performance monitoring
4. **Prometheus & Grafana** - Custom metrics

---

## 🚀 Performance Optimization

### 1. Caching
Implement Redis caching for frequently requested predictions.

### 2. Load Balancing
Use cloud platform's built-in load balancing.

### 3. Auto-Scaling
Configure auto-scaling based on traffic:
- Railway: Automatic
- Google Cloud Run: Configure in deployment
- AWS: Use Auto Scaling Groups

### 4. CDN
Use CloudFlare or AWS CloudFront for static assets.

### 5. Database
For storing results:
- PostgreSQL (Render, Railway)
- Cloud SQL (Google Cloud)
- RDS (AWS)

---

## 🧪 Testing Deployed API

### Test Health
```bash
curl https://your-api.com/health
```

### Test Authentication
```bash
curl -X POST https://your-api.com/detect \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"audio_data": "...", "language": "English"}'
```

### Load Testing
```bash
# Install Apache Bench
apt-get install apache2-utils

# Run load test
ab -n 1000 -c 10 https://your-api.com/health
```

---

## 📈 Cost Estimates

### Free Tiers (Monthly)

| Platform | Free Tier | Limits |
|----------|-----------|--------|
| Railway | $5 credit | 500 hours |
| Render | Free | 750 hours |
| Heroku | Free (deprecated) | - |
| Google Cloud Run | Free | 2M requests |
| AWS Lambda | Free | 1M requests |

### Paid Plans (Monthly)

| Platform | Starter | Pro |
|----------|---------|-----|
| Railway | $5 | Variable |
| Render | $7 | $25+ |
| Heroku | $7 | $25+ |
| Google Cloud Run | ~$10 | Variable |
| AWS | ~$10 | Variable |

---

## 🔄 CI/CD Setup

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up
```

---

## 🆘 Troubleshooting

### Issue: Deployment Failed
- Check logs in cloud platform dashboard
- Verify Dockerfile builds locally
- Check environment variables

### Issue: API Not Responding
- Check health endpoint
- Verify port configuration (8000)
- Check firewall rules

### Issue: High Latency
- Check server location (closer to users)
- Implement caching
- Optimize model inference

### Issue: Out of Memory
- Increase container memory limits
- Optimize model size
- Implement request queueing

---

## 📞 Support

For deployment issues:
1. Check platform documentation
2. Review application logs
3. Test locally first
4. Contact platform support

---

**Remember:** Always test in a staging environment before deploying to production!
