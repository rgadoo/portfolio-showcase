# Nandi Mindfulness App

A comprehensive AI-powered spiritual wellness platform that combines mindfulness practices, AI conversation, gamification, and personal growth tracking.

**🔗 Quick Links:** [Architecture](./architecture.md) | [Features](./features.md) | [API Documentation](./api-documentation.md) | [Data Model](./data-model.md) | [Code Samples](./code-samples/) | [Case Studies](./case-studies/)

## Overview

Nandi Mindfulness App is a full-stack Next.js application that provides users with a holistic approach to spiritual wellness. The platform features an intelligent AI companion, multiple wellness activities, gamification systems, and comprehensive analytics.

## Project Status

**Status:** Production Beta

**Development Period:** April 2025 - June 2025

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Commits** | 415+ |
| **TypeScript/TSX Files** | 773+ |
| **Lines of Code** | ~24,000+ (TypeScript/JavaScript) |
| **Development Period** | April 2025 - June 2025 |
| **Total Changes** | 4,645 files changed, 478,618+ insertions, 205,176+ deletions |
| **API Routes** | 95+ documented routes |
| **Database Models** | 20+ Prisma models |
| **Features** | 25+ features across AI, wellness, user, and admin domains |

## Key Features

### Core AI Features

1. **AI Companion** - Conversational interface with intent detection (20+ intent types) that guides users to appropriate features
2. **Ask Nandi** - Philosophical inquiry and dialogue with AI, including conversations, reflections, and bookmarks
3. **Moral Play** - Vikram-Vetal moral dilemma engine with stories, responses, and progress tracking
4. **Silent Journal** - Guided journaling with reflection, mood logs, intention tags, and AI-generated reflections

### Wellness Features

5. **Insights/Quizzes** - Mindfulness assessments and insights with quiz responses and activity tracking
6. **Core Calm** - Meditation and breathwork sessions
7. **Activity Sessions** - Multiple session types (meditation, journal, lifebuilder, sync)
8. **Activity Dashboard** - User activity tracking and analytics (recent activity, path balance, points distribution, achievements)
9. **Journey** - Personal growth and progress tracking with summary and milestones

### User Features

10. **Profile** - Account management with security (password, security questions, progressive registration support)
11. **Favorites** - Save and manage favorite content
12. **Feedback** - User feedback system
13. **Beta Testing** - Invite-based beta testing system with feedback management

### Admin Features

14. **Admin Dashboard** - Analytics, user management, content management
15. **Achievement Management** - Create and manage achievements with criteria builder
16. **Points System** - Points distribution and management
17. **Beta Management** - Invite codes, user management, feedback review
18. **User Management** - User CRUD, role management, analytics
19. **Geographic Analytics** - Privacy-first user distribution insights
20. **AI Content Generation** - Generate quizzes and moral stories using OpenAI prompts, populate database

### Additional Features

21. **Home** - Personalized home dashboard
22. **Create Menu** - Quick access to activity creation
23. **Games** - Game sessions and management
24. **Mood Logs** - Mood tracking and analytics
25. **Agent Insights** - AI-generated insights
26. **Events** - Event tracking and logging system

## Technology Stack

- **Frontend:** Next.js 14 (App Router), TypeScript, React
- **Styling:** Tailwind CSS, Shadcn UI
- **State Management:** Zustand
- **Backend:** Next.js API Routes, Server Actions
- **Database:** PostgreSQL with Prisma ORM
- **Authentication:** NextAuth.js
- **AI Integration:** OpenAI API, Claude (Anthropic)
- **API Documentation:** OpenAPI/Swagger
- **Architecture:** Feature-based, event-driven

## Key Highlights

- **AI Integration:** Multiple AI features (companion, Ask Nandi, moral play, journal reflections, admin content generation)
- **OpenAPI API Architecture:** 95+ documented API routes with Swagger integration
- **Feature-Based Architecture:** 25+ features, scalable, maintainable codebase
- **Gamification:** Event-driven achievement system, rule-based points/rewards, levels
- **Full-Stack Development:** Next.js, PostgreSQL, Prisma ORM (Hibernate-like), NextAuth
- **Data Modeling:** Prisma ORM with 20+ models, complex relationships, type-safe queries
- **Event-Driven System:** Rule-based points and achievement processing
- **User Experience:** Thoughtful UX for mindfulness/spiritual context
- **Analytics:** Activity tracking, user sessions, events, geographic analytics
- **Admin Systems:** Comprehensive admin panel with AI content generation

## Architecture

The application follows a feature-based architecture pattern with:

- **Feature Isolation:** Each feature is self-contained with its own components, services, and types
- **Service Layer:** Server-side services for business logic
- **Event-Driven Architecture:** Decoupled event system for points and achievements
- **Type Safety:** Full TypeScript coverage with Prisma-generated types
- **API-First Design:** OpenAPI/Swagger documentation for all endpoints

## Documentation

- [Architecture](./architecture.md) - System architecture and design patterns
- [Features](./features.md) - Detailed feature breakdown
- [Tech Stack](./tech-stack.md) - Technology details and choices
- [API Documentation](./api-documentation.md) - API architecture and endpoints
- [Data Model](./data-model.md) - Database schema and Prisma ORM patterns

## Case Studies

- [AI Companion Implementation](./case-studies/ai-companion.md)
- [OpenAPI API Architecture](./case-studies/openapi-api-architecture.md)
- [Achievement System](./case-studies/achievement-system.md)
- [Feature-Based Architecture](./case-studies/feature-architecture.md)
- [Activity Tracking System](./case-studies/activity-tracking.md)
- [Prisma ORM Data Model](./case-studies/prisma-orm-data-model.md)
- [Event-Driven Points/Reward System](./case-studies/event-driven-rewards.md)
- [Admin AI Content Generation](./case-studies/admin-ai-content-generation.md)

## Code Samples

See the [code-samples](./code-samples/) directory for sanitized examples of:

- Feature implementations
- Core libraries and services
- Database patterns and Prisma usage
- API route implementations
- Event-driven system patterns

## Development Practices

- **Type Safety:** Full TypeScript coverage
- **Code Organization:** Feature-based directory structure
- **Testing:** Unit and integration tests
- **Documentation:** Inline code documentation and feature READMEs
- **Security:** Authentication, authorization, input validation
- **Performance:** Optimized queries, caching strategies

---

**Note:** This is a showcase repository. The actual production codebase remains private.
