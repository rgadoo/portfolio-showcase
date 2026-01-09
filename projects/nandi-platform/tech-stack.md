# Tech Stack

Complete technology stack used in the Nandi Platform.

## Frontend

### Core Framework
- **Next.js 14** - React framework with App Router
  - Server-side rendering (SSR)
  - Static site generation (SSG)
  - API routes
  - Automatic code splitting
  - Image optimization

### UI & Styling
- **React 18** - UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **React Icons** - Icon library

### State Management
- **Zustand** - Lightweight state management
- **React Context** - Component-level state
- **Local Storage** - Client-side persistence

### UI Components
- **Custom Components** - Built-in component library
- **dnd-kit** - Drag and drop functionality
- **cmdk** - Command palette
- **driver.js** - User onboarding

### Media & File Handling
- **Uppy** - File upload library
  - Dashboard UI
  - Image editor
  - XHR upload

## Backend

### Runtime
- **Node.js 20** - JavaScript runtime
- **Next.js API Routes** - Serverless API endpoints

### Database & Services
- **Firebase Admin SDK** - Server-side Firebase operations
- **Firebase Client SDK** - Client-side Firebase operations
- **Firestore** - NoSQL database
- **Firebase Authentication** - User authentication

### Cloud Services
- **Google Cloud Storage** - Media file storage
- **Google Cloud Run** - Containerized deployment
- **Cloud Build** - CI/CD pipeline
- **Container Registry** - Docker image storage
- **Secret Manager** - Secure configuration

## Development Tools

### Language & Type Checking
- **TypeScript 5.8** - Type checking
- **ESLint** - Code linting
- **Prettier** - Code formatting

### Build Tools
- **npm** - Package management
- **Docker** - Containerization
- **Cloud Build** - CI/CD

### Code Quality
- **ESLint Config Next** - Next.js linting rules
- **TypeScript ESLint** - TypeScript linting
- **React Hooks ESLint** - React hooks linting

## Infrastructure

### Cloud Platform
- **Google Cloud Platform (GCP)**
  - Cloud Run
  - Cloud Storage
  - Cloud Build
  - Container Registry
  - Secret Manager

### Database
- **Firebase Firestore**
  - NoSQL database
  - Real-time updates
  - Offline support
  - Automatic scaling

### Authentication
- **Firebase Authentication**
  - Email/password
  - Google OAuth
  - Magic links
  - Custom tokens

### Storage
- **Google Cloud Storage**
  - Media files
  - CDN integration
  - Lifecycle policies

## DevOps

### Containerization
- **Docker** - Container platform
- **Alpine Linux** - Minimal base image

### CI/CD
- **Cloud Build** - Automated builds
- **Git** - Version control
- **GitHub** - Code repository (private)

### Deployment
- **Cloud Run** - Serverless containers
- **Custom Domains** - Domain mapping
- **HTTPS** - SSL/TLS certificates

## Third-Party Services

### Analytics (Optional)
- **Google Analytics** - Web analytics

### Content
- **React Markdown** - Markdown rendering
- **date-fns** - Date manipulation

## Development Environment

### Local Development
- **Node.js 18+** - Runtime
- **npm** - Package manager
- **VS Code** - Recommended IDE
- **Git** - Version control

### Environment Management
- **Environment Variables** - Configuration
- **.env.local** - Local development config
- **Secret Manager** - Production secrets

## Package Versions

### Core Dependencies
```json
{
  "next": "^14.2.33",
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "typescript": "~5.8.2",
  "firebase": "^11.0.2",
  "firebase-admin": "^12.0.0"
}
```

### Key Libraries
- **@dnd-kit/core**: ^6.3.1
- **@google-cloud/storage**: ^7.17.2
- **zustand**: ^5.0.8
- **tailwindcss**: ^3.4.17

## Architecture Patterns

### Frontend Patterns
- **Component-based** - Reusable components
- **Server Components** - Next.js 14 App Router
- **Client Components** - Interactive UI
- **Custom Hooks** - Reusable logic

### Backend Patterns
- **API Routes** - Serverless endpoints
- **Service Layer** - Business logic separation
- **Repository Pattern** - Data access abstraction

### Infrastructure Patterns
- **Serverless** - Cloud Run
- **Multi-tenant** - Shared infrastructure
- **Microservices-ready** - Modular design

## Performance Optimizations

### Frontend
- Code splitting (automatic)
- Image optimization
- Lazy loading
- CDN for static assets

### Backend
- Serverless scaling
- Database indexing
- Query optimization
- Caching strategies

### Infrastructure
- Auto-scaling
- CDN for media
- Efficient resource usage

## Security

### Authentication
- Firebase Authentication
- JWT tokens
- Secure session management

### Data Protection
- Tenant isolation
- Role-based access control
- Input validation
- Secret management

### Infrastructure Security
- HTTPS enforcement
- IAM roles
- Service accounts
- Network security

---

**Last Updated:** December 2024
