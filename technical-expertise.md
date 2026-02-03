# Technical Expertise: Skills Mapped to Implementations

This document maps professional skills to concrete implementations across production systems.

**Production Systems:**
- **[Nandi Platform](./projects/nandi-platform/)** — Multi-tenant SaaS content platform (Next.js 14, Firebase, GCP) - **Primary Production System**
- **[Content Generator](./projects/content-generator/)** — AI content pipeline supporting Nandi Platform (Python, FastAPI)

---

## Platform Engineering (Nandi Platform)

### Multi-Tenant SaaS Architecture

**Skill:** Designing and implementing production multi-tenant systems with complete isolation

**Evidence:**

#### Middleware Layer Isolation (`middleware.ts`)

```typescript
// Domain-based tenant resolution
export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host');
  
  // Platform domain → Platform mode (marketing, signup, admin)
  if (hostname === 'satjana.com') {
    return platformRouting(request);
  }
  
  // Subdomain → Extract instanceId
  if (hostname?.endsWith('.satjana.com')) {
    const instanceId = hostname.split('.')[0];
    return instanceRouting(request, instanceId);
  }
  
  // Custom domain → Firestore lookup
  const instanceId = await lookupCustomDomain(hostname);
  return instanceRouting(request, instanceId);
}
```

| Domain Type | Routing | Example |
|-------------|---------|---------|
| Platform domain | Platform mode | `satjana.com` → marketing/signup |
| Subdomain | Instance mode | `lightofvedanta.satjana.com` → instanceId |
| Custom domain | Instance mode | Firestore lookup |

**Fail-Fast Pattern:** No default tenant fallback in production - invalid tenant context terminates immediately.

#### Database Layer Isolation (Firestore)

**All collections scoped by `instanceId`:**

| Collection | Tenant Isolation |
|------------|------------------|
| `content` | `where('instanceId', '==', tenantId)` on every query |
| `pillars` | `instances/{instanceId}/pillars/{pillarId}` |
| `categories` | `instances/{instanceId}/categories/{categoryId}` |
| `tags` | `instances/{instanceId}/tags/{tagId}` |
| `transcripts` | `instanceId` field |
| `contentSubmissions` | `instanceId` field |

```typescript
// Automatic tenant scoping - no manual passing
export function getTenantId(): string {
  const tenantId = headers().get('x-instance-id');
  if (!tenantId && process.env.NODE_ENV === 'production') {
    throw new Error('Tenant context required');
  }
  return tenantId;
}
```

#### Storage Layer Isolation (GCS)

```
{bucket}/
└── {instanceId}/
    ├── content/{filename}
    ├── transcripts/{filename}
    └── thumbnails/{filename}
```

📖 [Multi-Tenant Architecture Case Study](./projects/nandi-platform/case-studies/multi-tenant-architecture.md)

---

### Authentication & Role-Based Access Control

**Skill:** Implementing enterprise-grade authentication with granular permissions

**Evidence:**

#### Multi-Method Authentication (Firebase Auth)

| Method | Implementation |
|--------|----------------|
| Email/Password | Standard signup/login flow |
| Google OAuth | Social login integration |
| Magic Links | Passwordless email authentication |
| Session Cookies | Server-side session management |

#### 4-Tier Role Hierarchy

```typescript
// src/lib/permissions.ts
export const ROLES = {
  user: ['content:read'],
  creator: ['content:read', 'content:submit'],
  admin: ['content:read', 'content:write', 'content:publish', 
          'taxonomy:write', 'submissions:approve'],
  super_admin: ['*']  // All permissions
};
```

| Role | Capabilities |
|------|-------------|
| `user` | Browse content, save favorites, view history |
| `creator` | Submit content for review |
| `admin` | Manage content, review submissions, manage taxonomy |
| `super_admin` | Full platform access, manage instances, manage users |

#### Granular Permission System

```typescript
// Permission checking
hasPermission(user, 'content:publish')
hasRoleOrHigher(user, 'admin')

// API route protection
withAuth({ requiredRole: 'admin' })
withAuth({ requiredPermission: 'content:publish' })
```

#### Multi-Tenant Auth Model

```typescript
// Global identity + tenant-specific roles
users/{userId}/memberships/{instanceId}
  ├── role: 'admin' | 'creator' | 'user'
  ├── status: 'active' | 'suspended'
  └── joinedAt: timestamp
```

---

### Full-Stack Implementation

**Skill:** End-to-end development from frontend to infrastructure

**Evidence:**

#### Frontend (Next.js 14 App Router)

| Metric | Value |
|--------|-------|
| React Components | 100+ |
| TypeScript Files | 495+ |
| Lines of Code | ~50,000+ |

**Component Architecture:**
```
app/
├── (instance)/           # Tenant-scoped routes
│   ├── explore/          # Content discovery
│   ├── content/[id]/     # Content player
│   └── session-builder/  # Session management
├── admin/                # Admin dashboard
│   ├── content/          # Content management
│   ├── users/            # User management
│   └── taxonomy/         # Pillar/category/tag management
└── platform/             # Platform marketing/signup
```

**Key Features:**
- Server Components for SEO and performance
- Streaming with Suspense boundaries
- Optimistic UI updates
- Real-time content updates

#### Backend (Next.js API Routes)

| Metric | Value |
|--------|-------|
| API Routes | 50+ |
| Serverless Endpoints | All routes |

**API Architecture:**
```
app/api/
├── admin/
│   ├── content/          # CRUD operations
│   ├── users/            # User management
│   ├── instances/        # Instance management
│   └── taxonomy/         # Taxonomy CRUD
├── auth/
│   ├── session/          # Session management
│   └── membership/       # Role management
├── content/              # Public content API
└── platform/             # Platform-level APIs
```

#### Database (Firestore)

| Collection | Purpose |
|------------|---------|
| `instances` | Tenant configuration, branding, settings |
| `content` | All content items (audio, video, page, quiz, course) |
| `pillars` | Top-level taxonomy |
| `categories` | Second-level taxonomy |
| `tags` | Content tags |
| `users` | User profiles |
| `memberships` | Tenant-specific roles |
| `contentSubmissions` | User submissions |

---

### Admin Dashboard & Tooling

**Skill:** Building comprehensive admin systems

**Evidence:**

#### Content Management

```typescript
// app/api/admin/content/route.ts
export async function POST(request: Request) {
  await withAdmin(request);  // Role check
  const tenantId = getTenantId();
  
  const content = await createContent({
    ...body,
    instanceId: tenantId,
    createdBy: user.uid,
    createdAt: serverTimestamp()
  });
  
  return Response.json({ id: content.id });
}
```

**Admin Features:**
- Content CRUD with version tracking
- Bulk operations (publish, unpublish, delete)
- Content scheduling
- Media management

#### User Management

- User listing with role filtering
- Role assignment per instance
- Membership management
- User suspension/reactivation

#### Instance Management (Super Admin)

- Create new instances
- Configure branding (name, logo, colors)
- Enable/disable content types
- Domain mapping

#### Taxonomy Management

- Pillar CRUD with ordering
- Category management under pillars
- Tag management
- Bulk import/export

---

### Cloud Infrastructure (GCP)

**Skill:** Production cloud deployment with CI/CD

**Evidence:**

#### Infrastructure Stack

| Component | Service |
|-----------|---------|
| Compute | Google Cloud Run |
| Database | Firestore |
| Storage | Google Cloud Storage |
| Auth | Firebase Authentication |
| CI/CD | Cloud Build |
| Secrets | Secret Manager |

#### Cloud Build Pipeline (`cloudbuild.yaml`)

```yaml
steps:
  # Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/nandi', '.']
  
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/nandi']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args:
      - 'run'
      - 'deploy'
      - 'nandi'
      - '--image=gcr.io/$PROJECT_ID/nandi'
      - '--region=us-central1'
      - '--memory=1Gi'
      - '--cpu=2'
```

#### Dockerfile (Multi-Stage Build)

```dockerfile
# Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runner
FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup --system nextjs && adduser --system nextjs
COPY --from=builder /app/.next/standalone ./
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

#### Cloud Run Configuration

| Setting | Production | Development |
|---------|------------|-------------|
| Memory | 1Gi | 512Mi |
| CPU | 2 | 1 |
| Max Instances | 10 | 5 |
| Timeout | 300s | 300s |

---

### Defense-in-Depth Security

**Skill:** Implementing multiple security layers

**Evidence:**

| Layer | Implementation |
|-------|----------------|
| Middleware | Tenant routing, header injection |
| Firestore Rules | Tenant boundary enforcement |
| API Validation | `validateInstanceAccess()` |
| Auth Middleware | `withAuth()`, `withAdmin()` |
| Bootstrap Protection | `BOOTSTRAP_SECRET_TOKEN` for super admin |
| Security Headers | CSP, HSTS, X-Frame-Options |
| Rate Limiting | On public endpoints |

**Firestore Security Rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Content - tenant isolated
    match /content/{contentId} {
      allow read: if request.auth != null 
        && resource.data.instanceId == request.auth.token.instanceId;
      allow write: if hasPermission('content:write');
    }
  }
}
```

---

## AI Engineering (Content Generator)

### Multi-Step LLM Pipeline

**Skill:** Orchestrating LLMs with external services

**Evidence:**

```
User Prompt → Prompt Builder → OpenAI API → Validation → Draft
                                   ↓
YouTube Sync → Transcript → Analysis → Content Generation
                                   ↓
Audio Script → Voice Service (OpenAI TTS / ElevenLabs) → Audio File
                                   ↓
Video Generator (librosa + MoviePy) → Subtitles → Video File
                                   ↓
GCS Upload → Firestore Publish → Live on Nandi Platform
```

### Key AI Capabilities

| Capability | Implementation |
|------------|----------------|
| Structured Outputs | OpenAI JSON schema enforcement |
| 5-Layer Validation | Taxonomy → Schema → Content → Pydantic → Publisher |
| Retry Logic | Exponential backoff with jitter |
| Cost Tracking | Token usage, model pricing, estimates |
| TTS Pipeline | OpenAI TTS (6 voices), ElevenLabs |
| Video Pipeline | Waveform visualization, burned-in subtitles |

📖 [Content Generator Architecture](./projects/content-generator/architecture.md)

---

## Summary Table

| Capability | Nandi Platform | Content Generator |
|------------|----------------|-------------------|
| **Production Status** | Live, serving users | Supporting tool |
| Multi-tenant SaaS | ✅ Primary feature | — |
| Authentication & RBAC | ✅ 4-tier roles | — |
| Admin Dashboard | ✅ Full CRUD | — |
| 50+ API Routes | ✅ | — |
| 100+ React Components | ✅ | — |
| Cloud Deployment (GCP) | ✅ Cloud Run | — |
| CI/CD Pipeline | ✅ Cloud Build | — |
| Firestore Database | ✅ 8+ collections | ✅ Publishing target |
| GCS Storage | ✅ Multi-tenant paths | ✅ Media uploads |
| Defense-in-Depth Security | ✅ | — |
| AI/LLM Pipelines | — | ✅ |
| Structured Outputs | — | ✅ |
| Multi-layer Validation | — | ✅ |
| TTS (OpenAI, ElevenLabs) | — | ✅ |
| Video Generation | — | ✅ |

---

## Project Statistics

### Nandi Platform (Primary)

| Metric | Value |
|--------|-------|
| **Status** | Production Beta, Live |
| **Total Commits** | 260+ |
| **Source Files** | 667+ |
| **Lines of Code** | ~50,000+ |
| **React Components** | 100+ |
| **API Routes** | 50+ |
| **Database Collections** | 8+ |
| **Development Period** | Oct 2025 - Feb 2026 |

### Content Generator (Supporting)

| Metric | Value |
|--------|-------|
| **Status** | Production-ready |
| **Python Files** | 198+ |
| **Lines of Code** | ~15,000+ |
| **Content Types** | 5 |
| **TTS Providers** | 2 |

---

## Related Documentation

- [Nandi Platform Architecture](./projects/nandi-platform/architecture.md)
- [Multi-Tenant Architecture Case Study](./projects/nandi-platform/case-studies/multi-tenant-architecture.md)
- [Infrastructure Documentation](./projects/nandi-platform/infrastructure.md)
- [Content Generator Architecture](./projects/content-generator/architecture.md)

---

*Last updated: February 2026*
