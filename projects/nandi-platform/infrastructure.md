# Infrastructure

This document describes the infrastructure architecture, deployment pipeline, and DevOps setup for the Nandi Platform.

## Infrastructure Overview

The platform runs entirely on Google Cloud Platform (GCP) with Firebase services, providing a serverless, scalable architecture.

## Google Cloud Platform (GCP)

### Cloud Run

**Purpose:** Containerized deployment of the Next.js application

**Configuration:**
- **Region:** us-central1
- **Platform:** Managed
- **Memory:** 1Gi
- **CPU:** 2
- **Timeout:** 300 seconds
- **Max Instances:** 10
- **Port:** 3000

**Features:**
- Auto-scaling based on traffic
- Scales to zero when idle
- Pay-per-use pricing
- HTTPS by default
- Custom domain support

**Multi-Tenant Architecture:**
- Single Cloud Run service serves all instances
- Runtime tenant resolution via middleware
- Instance-specific configuration from Firestore
- Shared infrastructure with tenant isolation

### Google Cloud Storage (GCS)

**Purpose:** Media file storage (audio, video, images)

**Architecture:**
- Instance-based path structure
- Organized by tenant ID
- Public read access for media files
- CDN-enabled for fast delivery

**Path Structure:**
```
{bucket-name}/
  {instance-id}/
    {content-type}/
      {file-name}
```

**Features:**
- Automatic CDN distribution
- CORS configuration
- Lifecycle policies
- Access control

### Cloud Build

**Purpose:** CI/CD pipeline for automated deployments

**Pipeline Steps:**
1. Build Docker image
2. Push to Container Registry
3. Deploy to Cloud Run
4. Update service configuration

**Configuration:**
- Build config: `cloudbuild.yaml`
- Environment-specific configs (dev/prod)
- Build-time environment variables
- Secret management integration

### Container Registry

**Purpose:** Docker image storage

**Features:**
- Private image registry
- Version tagging
- Image scanning
- Access control

### Secret Manager

**Purpose:** Secure storage of sensitive configuration

**Secrets:**
- Bootstrap tokens
- API keys (if needed)
- Service account keys (references)

**Integration:**
- Cloud Run secret references
- Runtime secret injection
- No secrets in code or config files

### Service Accounts

**Purpose:** Identity for Cloud Run service

**Roles:**
- Cloud Run service account
- Firestore access
- GCS access
- Secret Manager access

## Firebase Services

### Firestore

**Purpose:** Multi-tenant NoSQL database

**Configuration:**
- **Database ID:** `prod-db` (production), `dev-db` (development)
- **Region:** us-central1
- **Mode:** Native mode

**Collections:**
- `instances` - Instance configurations
- `content` - Content items
- `users` - User profiles
- `pillars`, `categories`, `tags` - Taxonomy
- `widgets` - UI configuration
- `contentSubmissions` - Submission workflow
- `tenantContent` - Tenant-specific UI config
- `pageTemplates` - Page content

**Multi-Tenant Pattern:**
- All collections use `instanceId` field
- Queries filter by `instanceId`
- Complete data isolation

**Indexes:**
- Custom indexes for complex queries
- Composite indexes for filtering
- Optimized for common query patterns

### Firebase Authentication

**Purpose:** User authentication

**Providers:**
- Email/password
- Google OAuth
- Magic links

**Features:**
- JWT token generation
- Custom claims for roles
- Multi-tenant user support
- Password reset flow

### Firebase Storage (Optional)

**Purpose:** Alternative storage option (currently using GCS)

**Note:** Platform primarily uses GCS, but Firebase Storage is available if needed.

## Deployment Pipeline

### CI/CD Flow

```
Code Push → Cloud Build Trigger → Build Image → Push to Registry → Deploy to Cloud Run
```

### Build Process

1. **Docker Build**
   - Multi-stage build
   - Install dependencies
   - Build Next.js application
   - Create production image

2. **Image Push**
   - Tag with latest
   - Push to Container Registry
   - Version tracking

3. **Cloud Run Deploy**
   - Update service with new image
   - Set environment variables
   - Configure secrets
   - Update traffic allocation

### Environment Configuration

**Build-Time Variables:**
- Site URL
- Media base URL
- Firebase config (public)
- Content types enabled

**Runtime Variables:**
- Database IDs
- GCS bucket names
- Service account references
- Secret references

**Secret Management:**
- Bootstrap tokens from Secret Manager
- No secrets in environment variables
- Secure secret injection

### Multi-Stage Dockerfile

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
# Install dependencies

# Stage 2: Builder
FROM node:20-alpine AS builder
# Build application

# Stage 3: Runner
FROM node:20-alpine AS runner
# Production image
```

**Optimizations:**
- Minimal base image (Alpine)
- Layer caching
- Standalone Next.js output
- Security best practices

## Multi-Tenant Infrastructure

### Single Service Architecture

- One Cloud Run service for all instances
- Runtime tenant resolution
- Instance-specific configuration from database
- Shared infrastructure resources

### Domain Mapping

**Pattern:**
- Custom domains → Instance mapping
- Subdomains → Automatic instance resolution
- Middleware extracts instance ID from hostname

**Implementation:**
- Cloud Run domain mappings
- DNS configuration
- Middleware-based routing

### Storage Architecture

**Multi-Tenant Storage:**
- Instance-based GCS paths
- Tenant isolation at storage level
- Shared bucket with path separation
- Efficient organization

## Security

### Infrastructure Security

- **Network:** Private networking where possible
- **Access Control:** IAM roles and service accounts
- **Secrets:** Secret Manager (no hardcoded secrets)
- **HTTPS:** Enforced for all traffic
- **CORS:** Configured for media access

### Application Security

- **Authentication:** Firebase Auth
- **Authorization:** RBAC with tenant isolation
- **Data Isolation:** Query-level filtering
- **Input Validation:** All inputs validated
- **Secure Headers:** Security headers configured

## Monitoring & Logging

### Cloud Logging

- Application logs
- Cloud Run logs
- Build logs
- Error tracking

### Monitoring

- Cloud Run metrics
- Request tracking
- Error rates
- Performance metrics

## Cost Optimization

### Strategies

- **Serverless:** Pay only for usage
- **Auto-scaling:** Scale to zero when idle
- **Efficient Storage:** Lifecycle policies
- **CDN:** Reduced bandwidth costs
- **Optimized Builds:** Smaller images

### Cost Structure

- Cloud Run: Pay per request and compute time
- Firestore: Pay per read/write operation
- GCS: Pay per storage and egress
- Cloud Build: Pay per build minute

## Development vs Production

### Development Environment

- Separate Cloud Run service
- Dev Firestore database
- Dev GCS bucket
- Separate build config

### Production Environment

- Production Cloud Run service
- Production Firestore database
- Production GCS bucket
- Production build config

### Environment Separation

- Complete isolation
- Separate credentials
- Independent scaling
- Isolated testing

## Deployment Scripts

### Production Deployment

```bash
./deploy.sh
```

**Process:**
1. Set GCP project
2. Enable required APIs
3. Submit Cloud Build
4. Deploy to Cloud Run

### Development Deployment

```bash
./deploy-dev.sh
```

**Process:**
1. Use dev configuration
2. Deploy to dev service
3. Use dev database and storage

## Infrastructure as Code

### Configuration Files

- `cloudbuild.yaml` - Production build config
- `cloudbuild-dev.yaml` - Development build config
- `Dockerfile` - Container definition
- `app.yaml` - App Engine config (if used)

### Version Control

- All infrastructure configs in Git
- Environment-specific configs
- Secret references (not actual secrets)
- Deployment scripts versioned

## Future Infrastructure Enhancements

- Multi-region deployment
- Advanced monitoring and alerting
- Automated backup strategies
- Disaster recovery planning
- Performance optimization
- Cost monitoring and optimization

---

**Last Updated:** December 2024
