# ChefGenie - Deployment Guide

## Overview

ChefGenie is a containerized full-stack application that can be deployed to any cloud provider that supports Docker containers. This guide covers popular deployment options.

## Prerequisites for All Deployments

1. **Git Repository**: Push your code to GitHub/GitLab
2. **Container Registry** (for cloud deployments):
   - AWS ECR
   - DigitalOcean Registry
   - Google Container Registry
   - Azure Container Registry
3. **Environment Variables**: Prepare `.env` with:
   - `OPENAI_API_KEY`
   - Database credentials
   - Any provider-specific settings

---

## Deployment Options

### 1. Basic Docker Compose (Single Server)

**Best for**: Small projects, prototyping, learning

**Requirements**: A server with Docker & Docker Compose

**Steps:**

```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/yourusername/Better-Half.git
cd Better-Half

# Setup environment
cp .env.example .env
# Edit .env with your credentials and OpenAI key

# Start services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f
```

**Cost**: ~$5-20/month (depending on server size)

---

### 2. AWS Deployment

#### Option A: Using AWS Elastic Beanstalk (Easiest for Docker)

**Requirements**:
- AWS Account
- AWS CLI installed
- Docker images pushed to ECR

**Steps:**

```bash
# 1. Create ECR repositories
aws ecr create-repository --repository-name chefgenie-backend --region us-east-1
aws ecr create-repository --repository-name chefgenie-frontend --region us-east-1

# 2. Build images locally
docker build -t chefgenie-backend:latest .
docker build -t chefgenie-frontend:latest ./frontend

# 3. Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com

# 4. Tag images
docker tag chefgenie-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/chefgenie-backend:latest
docker tag chefgenie-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/chefgenie-frontend:latest

# 5. Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/chefgenie-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/chefgenie-frontend:latest

# 6. Create Dockerrun.aws.json
cat > Dockerrun.aws.json << EOF
{
  "AWSEBDockerrunVersion": 3,
  "containerDefinitions": [
    {
      "name": "chefgenie-backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/chefgenie-backend:latest",
      "essential": true,
      "portMappings": [{
        "containerPort": 8000,
        "hostPort": 8000
      }],
      "environment": [
        {"name": "OPENAI_API_KEY", "value": "your-key-here"}
      ]
    },
    {
      "name": "chefgenie-frontend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/chefgenie-frontend:latest",
      "essential": true,
      "portMappings": [{
        "containerPort": 3000,
        "hostPort": 3000
      }]
    }
  ]
}
EOF

# 7. Deploy with EB CLI
eb init -p docker chefgenie
eb create chefgenie-env
eb deploy
```

#### Option B: AWS ECS (More Control)

1. Create ECS cluster
2. Create task definitions (backend and frontend)
3. Create services
4. Configure load balancer
5. Setup RDS for PostgreSQL
6. Deploy services

(See AWS documentation for detailed steps)

#### Option C: AWS Lambda + API Gateway (Serverless)

Works for backend, but frontend still needs web hosting:
- Deploy backend to Lambda
- Use API Gateway for HTTP
- Deploy frontend to S3 + CloudFront

**Cost**: ~$20-100/month (depending on usage)

---

### 3. DigitalOcean Deployment

#### Option A: Using App Platform (Easiest)

**Steps:**

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to DigitalOcean Console:
# - Click "Create" → "App"
# - Connect GitHub repository
# - Select Dockerfile in root and frontend/Dockerfile
# - Set environment variables
# - Click "Deploy"

# 3. Add PostgreSQL database in App Platform
# - Within the app, add Component → Database → PostgreSQL
# - DigitalOcean will create and connect it automatically
```

#### Option B: Using Docker on Droplet

```bash
# 1. Create Droplet with Docker one-click app
# 2. SSH into droplet
# 3. Follow Docker Compose steps above

# 4. Setup SSL with Let's Encrypt
docker run --rm -it -p 80:80 -p 443:443 \
  -v /root/certbot:/etc/letsencrypt \
  certbot/certbot certonly --standalone -d your-domain.com
```

**Cost**: ~$5-40/month (depending on Droplet size)

---

### 4. Google Cloud Deployment

#### Using Cloud Run (Easiest)

**Steps:**

```bash
# 1. Authenticate
gcloud auth login
gcloud config set project your-project-id

# 2. Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/chefgenie-backend .
gcloud builds submit --tag gcr.io/your-project/chefgenie-frontend frontend/

# 3. Deploy backend
gcloud run deploy chefgenie-backend \
  --image gcr.io/your-project/chefgenie-backend \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --set-env-vars OPENAI_API_KEY=your-key

# 4. Deploy frontend
gcloud run deploy chefgenie-frontend \
  --image gcr.io/your-project/chefgenie-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 5. Setup Cloud SQL PostgreSQL
gcloud sql instances create chefgenie-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1
```

**Cost**: ~$10-50/month

---

### 5. Azure Deployment

#### Using Container Instances

```bash
# 1. Authenticate
az login

# 2. Create resource group
az group create --name chefgenie --location eastus

# 3. Create Azure Container Registry
az acr create --resource-group chefgenie \
  --name chefgenieregistry --sku Basic

# 4. Build and push images
az acr build --registry chefgenieregistry \
  --image chefgenie-backend:latest .

az acr build --registry chefgenieregistry \
  --image chefgenie-frontend:latest frontend/

# 5. Deploy using Container Instances
az container create \
  --resource-group chefgenie \
  --name chefgenie-backend \
  --image chefgenieregistry.azurecr.io/chefgenie-backend:latest \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your-key \
  --registry-login-server chefgenieregistry.azurecr.io
```

**Cost**: ~$15-60/month

---

## GitHub Pages for Frontend Only

**If you only want to host the frontend:**

```bash
# 1. Update frontend/vite.config.ts
# Add base path for GitHub Pages:
export default {
  base: '/Better-Half/',
  // ... rest of config
}

# 2. Update package.json
{
  "homepage": "https://yourusername.github.io/Better-Half",
  "scripts": {
    "deploy": "npm run build && gh-pages -d dist"
  }
}

# 3. Install gh-pages
npm install --save-dev gh-pages

# 4. Deploy
npm run deploy

# 5. Enable GitHub Pages in repository settings
# Select "Deploy from a branch" and choose gh-pages
```

**Limitation**: Frontend will need to call your backend API from somewhere else (not free)

---

## Production Checklist

Before deploying to production:

- [ ] Set `APP_ENV=production` in `.env`
- [ ] Use a strong database password
- [ ] Enable HTTPS/SSL certificate
- [ ] Set up backups for PostgreSQL
- [ ] Configure logging and monitoring
- [ ] Set resource limits (CPU, memory)
- [ ] Enable auto-scaling (if available)
- [ ] Configure firewall rules
- [ ] Set up CI/CD pipeline for automated deployments
- [ ] Test database restore procedures
- [ ] Set up health checks
- [ ] Configure environment-specific settings

## Security Considerations

1. **Secrets Management**:
   - Never commit `.env` files
   - Use cloud provider secrets manager
   - Rotate keys regularly

2. **Database**:
   - Use strong passwords
   - Enable SSL for database connections
   - Restrict database access to application only
   - Regular backups

3. **API**:
   - Enable CORS only for your domain
   - Rate limiting
   - Authentication/authorization
   - Input validation

4. **Frontend**:
   - Content Security Policy headers
   - HTTPS only
   - Secure cookies

## Monitoring & Logging

Set up monitoring for:
- Application logs
- Error tracking
- Performance metrics
- Database metrics
- Cost tracking

Popular tools:
- CloudWatch (AWS)
- Stack Driver (Google Cloud)
- Application Insights (Azure)
- Datadog (multi-cloud)
- New Relic (multi-cloud)

## Scaling

For higher traffic:
- Use load balancers
- Auto-scaling groups
- CDN for frontend
- Read replicas for database
- Caching layer (Redis)
- Horizontal pod autoscaling (Kubernetes)

## CI/CD Pipeline

Example GitHub Actions workflow:

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push to registry
        run: |
          docker build -t chefgenie-backend .
          docker push registry.example.com/chefgenie-backend
      
      - name: Deploy to cloud
        run: |
          # Your deployment script here
```

## Cost Estimates

| Platform | Size | Estimated Monthly Cost |
|----------|------|------------------------|
| Single Droplet | Small | $5-10 |
| Docker Compose | Medium | $20-50 |
| AWS Elastic Beanstalk | Small-Medium | $30-100 |
| DigitalOcean App Platform | Small | $12-50 |
| Google Cloud Run | Small-Medium | $10-50 |
| Azure Container Instances | Small | $15-60 |

*(Prices are approximate and vary by region/usage)*

---

## Support & Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [DigitalOcean Docs](https://docs.digitalocean.com/)
- [Google Cloud Docs](https://cloud.google.com/docs)

---

## Need Help?

1. Check logs: `docker-compose logs -f`
2. Test API: `curl http://localhost:8000/docs`
3. Verify environment variables are set
4. Check cloud provider console for errors
5. Open a GitHub issue for support

---

Happy deploying! 🚀
