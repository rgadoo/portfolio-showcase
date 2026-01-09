# API Documentation

This document describes the API architecture, endpoints, and patterns used in the Nandi Mindfulness App.

## Overview

The Nandi Mindfulness App exposes a comprehensive REST API with **95+ documented endpoints** using OpenAPI/Swagger specification. All endpoints are built using Next.js API Routes and follow consistent patterns for authentication, authorization, request/response handling, and error management.

## API Architecture

### OpenAPI/Swagger Integration

The application uses OpenAPI 3.0 specification with Swagger JSDoc for API documentation.

**Specification Location:** `src/lib/core/openapi.server.ts`

**Documentation Endpoint:** `/api/docs`

**Key Features:**
- Auto-generated API documentation
- Interactive Swagger UI
- Type-safe API schemas
- Request/response validation

### API Route Organization

```
app/api/
├── admin/              # Admin endpoints (20+ routes)
│   ├── achievements/
│   ├── beta-feedback/
│   ├── beta-invite-codes/
│   ├── content/
│   ├── dashboard/
│   ├── geo-analytics/
│   ├── points/
│   ├── statistics/
│   └── users/
├── auth/               # Authentication (8+ routes)
│   ├── login/
│   ├── register/
│   ├── reset-password/
│   └── [...nextauth]/
├── activity/           # Activity tracking (6+ routes)
│   ├── achievements/
│   ├── path-balance/
│   ├── points-distribution/
│   ├── recent/
│   └── summary/
├── ask-nandi/          # Ask Nandi feature (4+ routes)
│   ├── conversations/
│   ├── generate/
│   └── reflections/
├── moral-play/         # Moral Play feature (6+ routes)
│   ├── progress/
│   ├── responses/
│   ├── stats/
│   └── stories/
├── nandi/              # AI Companion (6+ routes)
│   ├── chat/
│   ├── features/
│   ├── intents/
│   └── prompts/
├── journal/            # Journaling (3+ routes)
│   ├── entries/
│   └── silent/
├── insights/           # Insights/Quizzes (3+ routes)
│   ├── activity/
│   ├── quizzes/
│   └── stats/
└── ...                 # Additional endpoints
```

## API Patterns

### Request/Response Pattern

**Standard Response Format:**
```typescript
// Success response
{
  success: true,
  data: T,
  message?: string
}

// Error response
{
  success: false,
  error: string,
  message?: string
}
```

### HTTP Methods

- **GET**: Retrieve resources
- **POST**: Create resources or perform actions
- **PATCH**: Partial updates
- **PUT**: Full updates (less common)
- **DELETE**: Delete resources

### Status Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (not authenticated)
- **403**: Forbidden (not authorized)
- **404**: Not Found
- **500**: Internal Server Error

## Authentication & Authorization

### Authentication Methods

1. **NextAuth.js Sessions**
   - Session-based authentication
   - Secure HTTP-only cookies
   - CSRF protection

2. **API Token Authentication**
   - Bearer token authentication
   - For programmatic access

### Authorization Patterns

**Role-Based Access Control (RBAC):**
- `user`: Standard user
- `admin`: Administrative access
- `beta`: Beta tester access

**Authorization Middleware:**
```typescript
// Example: Admin-only endpoint
export async function GET(request: NextRequest) {
  const user = await getAuthUser(request);
  if (!user || user.role !== 'admin') {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    );
  }
  // ... endpoint logic
}
```

## API Endpoints by Category

### Admin Endpoints

**Base Path:** `/api/admin`

#### User Management
- `GET /api/admin/users` - List all users
- `PATCH /api/admin/users` - Update user role
- `GET /api/admin/users/[id]` - Get user details

#### Achievement Management
- `GET /api/admin/achievements` - List achievements
- `POST /api/admin/achievements` - Create achievement
- `PATCH /api/admin/achievements/[id]` - Update achievement
- `GET /api/admin/achievements/guide` - Get achievement guide

#### Content Generation
- `POST /api/admin/content/quiz/generate` - Generate quiz
- `POST /api/admin/content/story/generate` - Generate story
- `GET /api/admin/content/quiz/index` - List quizzes
- `GET /api/admin/content/story/index` - List stories

#### Beta Management
- `GET /api/admin/beta-overview` - Beta overview
- `GET /api/admin/beta-users` - List beta users
- `GET /api/admin/beta-feedback` - List feedback
- `POST /api/admin/beta-invite-codes` - Create invite code
- `PATCH /api/admin/beta-invite-codes/[id]` - Update invite code

#### Analytics
- `GET /api/admin/dashboard` - Dashboard metrics
- `GET /api/admin/dashboard/metrics` - Detailed metrics
- `GET /api/admin/geo-analytics` - Geographic analytics
- `GET /api/admin/statistics/points` - Points statistics
- `GET /api/admin/statistics/achievements` - Achievement statistics

### Authentication Endpoints

**Base Path:** `/api/auth`

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/progressive-register` - Progressive registration
- `POST /api/auth/reset-password` - Reset password
- `POST /api/auth/verify-security` - Verify security question
- `GET /api/auth/[...nextauth]` - NextAuth.js endpoints

### Activity Endpoints

**Base Path:** `/api/activity`

- `GET /api/activity/recent` - Recent activities
- `GET /api/activity/summary` - Activity summary
- `GET /api/activity/points-distribution` - Points by category
- `GET /api/activity/path-balance` - Yoga path balance
- `GET /api/activity/yoga-path-balance` - Detailed path balance
- `GET /api/activity/achievements` - User achievements

### Ask Nandi Endpoints

**Base Path:** `/api/ask-nandi`

- `POST /api/ask-nandi/generate` - Generate conversation
- `GET /api/ask-nandi/conversations` - List conversations
- `GET /api/ask-nandi/conversations/[id]` - Get conversation
- `POST /api/ask-nandi/reflections` - Create reflection

### Moral Play Endpoints

**Base Path:** `/api/moral-play`

- `GET /api/moral-play/stories` - List stories
- `GET /api/moral-play/story/[id]` - Get story
- `POST /api/moral-play/submit` - Submit response
- `GET /api/moral-play/responses` - Get responses
- `GET /api/moral-play/progress` - User progress
- `GET /api/moral-play/stats` - Statistics

### AI Companion (Nandi) Endpoints

**Base Path:** `/api/nandi`

- `POST /api/nandi/chat` - Chat with AI companion
- `GET /api/nandi/chat/sessions` - List chat sessions
- `GET /api/nandi/chat/sessions/[id]` - Get session
- `GET /api/nandi/intents` - List intents
- `GET /api/nandi/features` - List features
- `GET /api/nandi/prompts` - Quick prompts

### Journal Endpoints

**Base Path:** `/api/journal`

- `POST /api/journal/entries` - Create journal entry
- `GET /api/journal/entries` - List entries
- `POST /api/journal/silent` - Create silent journal entry
- `GET /api/journal/silent` - List silent journal entries

### Insights/Quizzes Endpoints

**Base Path:** `/api/insights`

- `GET /api/insights/quizzes` - List quizzes
- `GET /api/insights/activity` - Quiz activity
- `GET /api/insights/stats` - Quiz statistics

### User Endpoints

**Base Path:** `/api/user` and `/api/profile`

- `GET /api/profile` - Get user profile
- `PATCH /api/profile` - Update profile
- `GET /api/user/beta-info` - Beta user info

### Additional Endpoints

- `GET /api/health` - Health check
- `GET /api/docs` - API documentation
- `POST /api/events` - Record event
- `GET /api/favorites` - List favorites
- `POST /api/favorites` - Add favorite
- `DELETE /api/favorites/[id]` - Remove favorite
- `GET /api/mood-logs` - List mood logs
- `POST /api/mood-logs` - Create mood log
- `GET /api/journey/summary` - Journey summary

## Request/Response Schemas

### User Schema

```typescript
interface User {
  id: string;
  userId: string;
  email?: string;
  name?: string;
  role: 'user' | 'admin' | 'beta';
  createdAt: string;
  updatedAt: string;
}
```

### Error Schema

```typescript
interface Error {
  success: false;
  error: string;
  message?: string;
}
```

### Pagination Schema

```typescript
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    offset: number;
    limit: number;
    hasMore: boolean;
  };
}
```

## API Conventions

### Naming Conventions

- **Routes**: kebab-case (e.g., `/api/ask-nandi`)
- **Parameters**: camelCase (e.g., `userId`)
- **Query Parameters**: camelCase (e.g., `?limit=10&offset=0`)

### Error Handling

**Consistent Error Format:**
```typescript
{
  success: false,
  error: 'Error type',
  message: 'Human-readable error message'
}
```

**Error Types:**
- `ValidationError`: Input validation failed
- `UnauthorizedError`: Authentication required
- `ForbiddenError`: Insufficient permissions
- `NotFoundError`: Resource not found
- `InternalError`: Server error

### Input Validation

**Zod Schemas:**
```typescript
import { z } from 'zod';

const createQuizSchema = z.object({
  prompt: z.string().min(1),
  category: z.string(),
  count: z.number().min(1).max(10)
});
```

### Rate Limiting

- API endpoints may implement rate limiting
- Admin endpoints have stricter limits
- Authentication endpoints have special limits

## API Documentation

### Swagger UI

Access the interactive API documentation at:
- **Development**: `http://localhost:3000/api/docs`
- **Production**: `https://your-domain.com/api/docs`

### OpenAPI Specification

The OpenAPI specification is available at:
- `/api/docs` - JSON format
- Swagger UI for interactive exploration

### Documentation Features

- **Interactive Testing**: Test endpoints directly from Swagger UI
- **Schema Validation**: Request/response schemas
- **Authentication**: Test with authentication tokens
- **Examples**: Request/response examples

## API Security

### Security Measures

1. **Authentication**: NextAuth.js sessions or bearer tokens
2. **Authorization**: Role-based access control
3. **Input Validation**: Zod schemas for all inputs
4. **SQL Injection Prevention**: Prisma parameterized queries
5. **XSS Protection**: Input sanitization
6. **CSRF Protection**: NextAuth.js CSRF tokens
7. **Rate Limiting**: Protection against abuse

### Security Best Practices

- All sensitive endpoints require authentication
- Admin endpoints require admin role
- Input validation on all user inputs
- Error messages don't expose sensitive information
- Secure password hashing (bcrypt)
- HTTPS in production

## API Performance

### Optimization Strategies

1. **Database Queries**: Optimized with Prisma
2. **Caching**: Response caching where appropriate
3. **Pagination**: All list endpoints support pagination
4. **Indexing**: Database indexes for common queries
5. **Connection Pooling**: Prisma connection pooling

### Performance Metrics

- **Response Time**: < 200ms for most endpoints
- **Database Queries**: Optimized with indexes
- **Concurrent Requests**: Handled efficiently

## API Versioning

Currently using version 1.0.0 of the API. Future versions will be handled through:
- URL versioning: `/api/v2/...`
- Header versioning: `Accept: application/vnd.nandi.v2+json`

## Testing

### API Testing

- Unit tests for service functions
- Integration tests for API routes
- E2E tests for critical flows

### Test Coverage

- Authentication flows
- Authorization checks
- Input validation
- Error handling
- Success responses

## Summary

The Nandi Mindfulness App API provides:

- **95+ documented endpoints** across all features
- **OpenAPI/Swagger** integration for comprehensive documentation
- **Consistent patterns** for authentication, authorization, and error handling
- **Type-safe** request/response schemas
- **Secure** by default with authentication and authorization
- **Well-documented** with interactive Swagger UI
- **Performant** with optimized queries and caching

This API architecture supports a complex application with multiple features, admin capabilities, and AI integration while maintaining consistency, security, and developer experience.
