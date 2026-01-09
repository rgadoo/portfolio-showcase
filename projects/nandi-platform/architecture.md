# Architecture

This document describes the multi-tenant SaaS architecture of the Nandi Platform.

## System Overview

The Nandi Platform is built as a single-application, multi-tenant SaaS system. All instances share the same infrastructure while maintaining complete data isolation.

## Architecture Principles

1. **Single Codebase**: One application serves all instances
2. **Runtime Tenant Resolution**: Tenant identification happens at request time
3. **Data Isolation**: Complete separation of data between tenants
4. **Shared Infrastructure**: Efficient resource utilization
5. **Scalable Design**: Auto-scaling based on traffic

## Multi-Tenant Architecture

### Tenant Resolution Flow

```
Request → Middleware → Extract Tenant ID → Set Header → Application
```

1. **Request arrives** with domain/subdomain
2. **Middleware** extracts instance ID from hostname
3. **Header set** (`x-instance-id`) for downstream use
4. **Application** uses tenant ID for all queries

### Data Isolation Pattern

All Firestore collections use an `instanceId` field for tenant isolation:

```typescript
// All queries automatically filter by instanceId
const tenantId = getTenantId(); // From middleware header
const query = db.collection('content')
  .where('instanceId', '==', tenantId)
  .where('published', '==', true);
```

### Tenant Context

The platform uses a tenant context system that:
- Extracts tenant ID from request headers
- Provides tenant ID to all downstream services
- Ensures all queries are tenant-scoped
- Handles fallback scenarios

## Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **React 18** - UI components
- **Tailwind CSS** - Styling
- **Zustand** - Client state management

### Backend
- **Next.js API Routes** - Serverless API endpoints
- **Firebase Admin SDK** - Server-side Firebase operations
- **Firebase Client SDK** - Client-side authentication

### Database
- **Firestore** - NoSQL database with multi-tenant support
- **Collections**: content, instances, users, pillars, categories, tags, widgets

### Storage
- **Google Cloud Storage** - Media file storage
- **Instance-based paths** - Organized by tenant

### Infrastructure
- **Google Cloud Run** - Containerized deployment
- **Cloud Build** - CI/CD pipeline
- **Container Registry** - Docker image storage

## Database Schema

### Core Collections

#### `instances`
Instance configuration and metadata:
- `id` - Instance identifier (document ID)
- `name` - Display name
- `domain` - Custom domain
- `subdomain` - Subdomain (if applicable)
- `isPlatformInstance` - Platform-owned flag
- `createdBy` - Creator user ID
- `config` - Instance-specific configuration

#### `content`
All content items (audio, video, articles, etc.):
- `instanceId` - Tenant identifier
- `type` - Content type (audio, video, page, etc.)
- `title`, `description` - Content metadata
- `pillar`, `category`, `tags` - Taxonomy
- `published` - Publication status
- `visibility` - Public or authenticated
- `mediaPath` - Storage path
- `createdAt`, `updatedAt` - Timestamps

#### `users`
Global user profiles:
- `id` - User ID (document ID)
- `email`, `displayName`, `photoURL` - Profile data
- `memberships/{instanceId}` - Subcollection for tenant memberships
  - `role` - Instance-specific role
  - `status` - Membership status
  - `joinedAt` - Join timestamp

#### `pillars`, `categories`, `tags`
Taxonomy master tables:
- Instance-scoped taxonomy
- Hierarchical relationships
- Active/inactive status
- Custom ordering

### Multi-Tenant Query Pattern

All queries follow this pattern:

```typescript
function getTenantId(): string {
  // Extract from middleware header
  const headersList = headers();
  return headersList.get('x-instance-id') || DEFAULT_TENANT_ID;
}

async function getContent() {
  const tenantId = getTenantId();
  return db.collection('content')
    .where('instanceId', '==', tenantId)
    .where('published', '==', true)
    .get();
}
```

## API Design

### RESTful Endpoints

- `/api/content` - Content operations
- `/api/taxonomy` - Taxonomy management
- `/api/admin/*` - Admin operations
- `/api/platform/*` - Platform operations
- `/api/auth/*` - Authentication

### Authentication

- Firebase Authentication for user auth
- JWT tokens for API authentication
- Role-based access control (RBAC)
- Instance-specific permissions

## Component Architecture

### Frontend Structure

```
app/
├── (routes)/          # Public routes
├── admin/             # Admin panel
├── api/               # API routes
└── ...

src/
├── components/         # Reusable components
├── features/          # Feature modules
├── hooks/             # Custom hooks
├── lib/               # Utilities and services
└── types/             # TypeScript types
```

### Service Layer

- **CMS Service** - Content management operations
- **Auth Service** - Authentication operations
- **Tenant Service** - Tenant context and configuration
- **Storage Service** - Media file operations

## Security Architecture

### Data Isolation
- Tenant-level query filtering
- Middleware-based tenant resolution
- No cross-tenant data access

### Authentication & Authorization
- Firebase Authentication
- Role-based access control
- Instance-specific roles
- Super admin for platform management

### Security Best Practices
- Input validation
- SQL injection prevention (NoSQL)
- XSS protection
- CSRF protection
- Secure headers
- Secret management

## Performance Optimizations

### Database
- Firestore indexes for efficient queries
- Query optimization
- Strategic caching

### Frontend
- Code splitting (Next.js automatic)
- Lazy loading
- Image optimization
- CDN for static assets

### Infrastructure
- Auto-scaling (Cloud Run)
- Efficient resource utilization
- Media CDN

## Scalability

### Horizontal Scaling
- Cloud Run auto-scales based on traffic
- Stateless application design
- Shared database (Firestore scales automatically)

### Vertical Scaling
- Configurable CPU and memory
- Optimized for serverless architecture

### Storage Scaling
- GCS handles large file storage
- Instance-based organization
- Efficient path structure

## Deployment Architecture

See [infrastructure.md](./infrastructure.md) for detailed deployment architecture.

## Design Patterns

### Multi-Tenant Patterns
- **Shared Database, Shared Schema** - All tenants in same database
- **Tenant ID in Every Record** - Data isolation via filtering
- **Middleware Tenant Resolution** - Runtime tenant identification

### Service Patterns
- **Service Layer** - Business logic separation
- **Repository Pattern** - Data access abstraction
- **Factory Pattern** - Dynamic component loading

## Future Architecture Considerations

- Multi-region deployment
- Read replicas for scaling
- Advanced caching strategies
- Microservices migration (if needed)
- Event-driven architecture

---

**Last Updated:** December 2024
