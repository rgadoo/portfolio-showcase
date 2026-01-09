# Case Study: Multi-Tenant Architecture Implementation

## Challenge

Build a SaaS platform that can serve multiple isolated instances (tenants) on shared infrastructure while maintaining complete data isolation and allowing each instance to have custom branding, configuration, and content.

## Solution

Implemented a middleware-based multi-tenant architecture with runtime tenant resolution and database-level isolation.

## Architecture Design

### Core Principles

1. **Single Codebase**: One application serves all instances
2. **Runtime Tenant Resolution**: Tenant ID extracted from request at runtime
3. **Data Isolation**: All queries filtered by `instanceId` field
4. **Shared Infrastructure**: Efficient resource utilization

### Implementation

#### 1. Middleware-Based Tenant Resolution

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || '';
  const instanceId = extractInstanceId(hostname);
  
  // Set tenant ID in header for downstream use
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-instance-id', instanceId);
  
  return NextResponse.next({
    request: { headers: requestHeaders }
  });
}
```

#### 2. Tenant Context Utility

Created a tenant context system that automatically provides tenant ID to all server components and API routes:

```typescript
// src/lib/tenant-context.ts
export function getTenantId(): string {
  const headersList = headers();
  const instanceId = headersList.get('x-instance-id');
  return instanceId || DEFAULT_TENANT_ID;
}
```

#### 3. Database Query Pattern

All Firestore queries automatically filter by tenant:

```typescript
async function getContent() {
  const tenantId = getTenantId();
  return db.collection('content')
    .where('instanceId', '==', tenantId)
    .where('published', '==', true)
    .get();
}
```

## Key Components

### 1. Instance Configuration

Each instance has its own configuration stored in Firestore:

- Branding (name, logo, colors)
- Feature flags
- Enabled content types
- Taxonomy structure
- Navigation configuration

### 2. Domain Mapping

- Custom domains map to instances
- Subdomains automatically resolve to instances
- Middleware extracts instance ID from hostname

### 3. Storage Architecture

Media files organized by instance:

```
{bucket}/
  {instance-id}/
    {content-type}/
      {file-name}
```

## Benefits

1. **Cost Efficiency**: Shared infrastructure reduces costs
2. **Scalability**: Auto-scaling works for all instances
3. **Maintainability**: Single codebase to maintain
4. **Isolation**: Complete data separation between tenants
5. **Flexibility**: Each instance fully customizable

## Challenges Solved

### Challenge 1: Tenant Resolution at Build Time

**Problem**: Next.js static generation happens at build time, but tenant ID is only known at request time.

**Solution**: Used Next.js App Router with server components that run at request time, allowing runtime tenant resolution.

### Challenge 2: Data Isolation

**Problem**: Ensuring no cross-tenant data access.

**Solution**: 
- All queries require `instanceId` filter
- Tenant context utility ensures tenant ID is always available
- Middleware enforces tenant resolution
- Database rules enforce tenant isolation

### Challenge 3: Instance-Specific Configuration

**Problem**: Each instance needs different branding and features.

**Solution**: 
- Configuration stored in Firestore `instances` collection
- Fetched at runtime based on tenant ID
- Cached for performance
- Supports feature flags and content type enablement

## Performance Optimizations

1. **Caching**: Instance configuration cached in memory
2. **Query Optimization**: Firestore indexes for tenant-scoped queries
3. **CDN**: Media files served via CDN
4. **Code Splitting**: Next.js automatic code splitting

## Security

1. **Data Isolation**: Query-level filtering ensures no cross-tenant access
2. **Authentication**: Firebase Auth with tenant-aware memberships
3. **Authorization**: Role-based access control per tenant
4. **Middleware**: Tenant resolution happens before any data access

## Results

- ✅ Multiple instances running on shared infrastructure
- ✅ Complete data isolation verified
- ✅ Zero cross-tenant data leaks
- ✅ Efficient resource utilization
- ✅ Scalable architecture

## Lessons Learned

1. **Middleware is Key**: Early tenant resolution simplifies downstream code
2. **Type Safety**: TypeScript helps catch tenant-related bugs
3. **Testing**: Important to test multi-tenant scenarios thoroughly
4. **Documentation**: Clear patterns help prevent mistakes

---

**Status**: Production-ready  
**Impact**: Enables platform to serve unlimited instances efficiently
