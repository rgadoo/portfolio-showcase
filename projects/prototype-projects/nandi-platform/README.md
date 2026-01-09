# Nandi Spiritual Platform

A multi-module spiritual platform built with Domain-Driven Design principles, featuring three interactive modules for Vedic wisdom exploration.

## Overview

Nandi is an integrated platform that brings together multiple modules focused on Vedic wisdom and spiritual exploration. The platform provides a unified interface to access all available modules through a single application.

## Project Status

**Status:** Prototype

**Development Period:** March 2025

## Key Features

### Three Core Modules

1. **KarmaCafe (🧘)** - AI-Powered Vedic Wisdom Chatbot
   - Three unique AI avatars (Karma, Dharma, Atma)
   - Real-time conversational AI based on OpenAI
   - Session-based conversation history
   - Philosophical guidance on Vedic concepts

2. **SoulQuest (🔮)** - Interactive Spiritual Adventure Game
   - Multiple themed quests (Self-Discovery, Mindfulness, Compassion)
   - Guided reflective questions
   - Progressive difficulty
   - Progress tracking and visualization

3. **WisdomPets (🐘)** - Virtual Spiritual Animal Companions
   - Multiple spiritual animal companions
   - Various interaction types with different effects
   - Interaction history tracking
   - Spiritual guidance through pet interactions

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Architecture**: Domain-Driven Design (DDD)
- **AI Integration**: OpenAI GPT models
- **Session Management**: Flask-Session
- **Database**: PostgreSQL (configured for dev, test, prod)
- **Search**: Elasticsearch

### Frontend
- **Framework**: React
- **Routing**: React Router
- **HTTP Client**: Axios
- **Styling**: CSS with modern responsive design
- **State Management**: React Hooks

### Development
- **Testing**: Pytest, Jest, React Testing Library
- **E2E Testing**: Selenium
- **Code Quality**: ESLint, Prettier

## Architecture

The platform follows **Domain-Driven Design (DDD)** principles with a layered architecture:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External services and technical concerns
- **Presentation Layer**: API endpoints and UI

Each module is self-contained with clear boundaries and follows the same architectural pattern.

## Project Statistics

| Metric | Value |
|--------|-------|
| **Modules** | 3 (KarmaCafe, SoulQuest, WisdomPets) |
| **Python Files** | 100+ |
| **React Components** | 20+ |
| **API Endpoints** | 20+ |
| **Architecture Pattern** | Domain-Driven Design |

## Documentation

- [Architecture](./architecture.md) - System architecture and DDD patterns
- [Modules](./modules.md) - Detailed module breakdown

## Code Samples

See the [code-samples](./code-samples/) directory for examples of:
- Domain-Driven Design patterns
- Flask blueprint registration
- React component patterns
- OpenAI integration
- Session management

## Case Studies

- [Domain-Driven Design Implementation](./case-studies/domain-driven-design.md)

---

**Note:** This is a showcase repository. The actual production codebase remains private.
