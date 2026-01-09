# Nandi Platform

A production-ready white-label SaaS platform for content management and playback, enabling organizations to launch their own branded content platforms.

**🔗 Quick Links:** [Architecture](./architecture.md) | [Infrastructure](./infrastructure.md) | [Features](./features.md) | [Code Samples](./code-samples/) | [Case Studies](./case-studies/)

## Overview

Nandi Platform is a multi-tenant SaaS solution that transforms content management and delivery. Built from the ground up with a focus on scalability, flexibility, and white-label customization, the platform supports multiple content types, comprehensive taxonomy management, and a robust user authentication system.

## Production Status

**Status:** Production Beta  
**Live Instance:** Closer to Self (production)  
**User Signup:** Currently disabled for beta phase

The platform has completed Phases 1-5 of development, with core multi-tenant architecture, CMS, authentication, and content management fully operational.

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Commits** | 260+ |
| **Source Files** | 667+ |
| **Lines of Code** | ~50,000+ (TypeScript/JavaScript) |
| **Development Period** | Oct 2025 - Jan 2026 |
| **Total Changes** | 3,264 files changed, 216,419+ insertions, 63,185+ deletions |
| **TypeScript/JavaScript Files** | 495+ |
| **Components** | 100+ React components |
| **API Routes** | 50+ serverless endpoints |
| **Database Collections** | 20+ Firestore collections |

## Key Achievements

- ✅ **Multi-Tenant Architecture**: Complete instance isolation with shared infrastructure
- ✅ **Production Deployment**: Live instance running on Google Cloud Platform
- ✅ **Full-Stack Development**: End-to-end implementation from frontend to infrastructure
- ✅ **Scalable Design**: Supports unlimited instances with tenant isolation
- ✅ **Modern Tech Stack**: Next.js 14, TypeScript, Firebase, GCP

## Technologies Used

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **Zustand** - State management

### Backend & Services
- **Firebase Firestore** - Multi-tenant database
- **Firebase Authentication** - User authentication (email, Google, magic links)
- **Google Cloud Storage** - Media file storage
- **Next.js API Routes** - Serverless API endpoints

### Infrastructure & DevOps
- **Google Cloud Run** - Containerized deployment
- **Cloud Build** - CI/CD pipeline
- **Container Registry** - Docker image storage
- **Secret Manager** - Secure configuration management
- **Docker** - Containerization

## Architecture Highlights

### Multi-Tenant Design
- Single Cloud Run service serving all instances
- Runtime tenant resolution via middleware
- Instance-specific configuration from Firestore
- Complete data isolation between tenants
- Shared infrastructure with tenant-level security

### Content Management
- Multiple content types: audio, video, page (articles), embed
- Rich taxonomy system: pillars, categories, tags
- Content submission workflow with review process
- Admin panel for content management
- Public contribution system

### User Management
- Role-based access control (RBAC)
- Multi-tenant user memberships
- Firebase Authentication integration
- Instance-specific roles and permissions

## Features

### Fully Implemented ✅
- Multi-tenant instance management
- Content Management System (CMS)
- User authentication & RBAC
- Content types: audio, video, page, embed
- Taxonomy management
- Session builder & playback engine
- Admin panels
- Content submission workflow

### In Progress ⚠️
- Collection (course) content type - UI exists, functionality being enhanced
- Quiz content type - UI exists, interactive features in development

## Documentation

- [Architecture](./architecture.md) - System design and architecture
- [Infrastructure](./infrastructure.md) - GCP, Firebase, deployment setup
- [Features](./features.md) - Detailed feature breakdown
- [Implementation Status](./implementation-status.md) - What's built vs planned
- [Tech Stack](./tech-stack.md) - Technology details

## Case Studies

See [case-studies/](./case-studies/) for detailed deep-dives on:
- Multi-tenant architecture implementation
- White-label platform transformation
- CMS implementation
- Infrastructure & deployment
- Authentication & RBAC system

## Code Samples

Sanitized code examples available in:
- [code-samples/](./code-samples/) - React components, hooks, services, utilities
- [Infrastructure examples](./code-samples/infrastructure/) - Deployment configs (sanitized)

## My Role & Contributions

As the lead developer on this project, I was responsible for:

- **Architecture Design**: Designed and implemented the multi-tenant SaaS architecture
- **Full-Stack Development**: Built frontend, backend, and infrastructure components
- **DevOps**: Set up CI/CD pipelines, deployment automation, and infrastructure
- **Database Design**: Designed Firestore schema for multi-tenant data isolation
- **Security**: Implemented RBAC, tenant isolation, and security best practices
- **Platform Transformation**: Led the transformation from single-tenant to multi-tenant SaaS

## Technical Challenges Solved

1. **Multi-Tenant Data Isolation**: Implemented middleware-based tenant resolution with Firestore query filtering
2. **Instance Provisioning**: Built automated instance creation workflow with Cloud Run domain mapping
3. **Content Type System**: Created pluggable content type registry with dynamic player components
4. **Storage Architecture**: Designed instance-based GCS path structure for multi-tenant media storage
5. **Authentication Flow**: Integrated Firebase Auth with multi-tenant membership system

## Performance & Scalability

- **Serverless Architecture**: Cloud Run auto-scales based on traffic
- **Database Optimization**: Firestore indexes for efficient queries
- **Media Delivery**: GCS with CDN for fast media file delivery
- **Code Splitting**: Next.js automatic code splitting for optimal bundle sizes
- **Caching**: Strategic caching at multiple layers (Firestore, API routes, client)

## Security

- Role-based access control (RBAC)
- Tenant-level data isolation
- Firebase Authentication with secure token management
- Secret Manager for sensitive configuration
- Environment-based configuration separation
- Input validation and sanitization

## Future Roadmap

- Phase 6: Platform setup (marketing site, customer signup)
- Phase 7: Runtime theming
- Phase 8: Billing integration
- Enhanced collection and quiz functionality
- Additional content types

---

**Note:** This is a showcase of my work. The actual production codebase remains private. All code samples and documentation have been sanitized to remove sensitive information.
