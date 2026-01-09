# Nandi Platform Modules

This document provides a detailed breakdown of the three core modules in the Nandi Spiritual Platform.

## Module Overview

The Nandi platform consists of three distinct modules, each following Domain-Driven Design principles:

1. **KarmaCafe** - AI-powered conversational chatbot
2. **SoulQuest** - Interactive spiritual adventure game
3. **WisdomPets** - Virtual spiritual animal companions

## KarmaCafe Module

### Description

KarmaCafe is an AI-powered conversational chatbot system that introduces users to Vedic philosophical concepts through three distinct avatar personalities.

### Features

- **Three AI Avatars**:
  - **Karma (⚖️)**: Explains cause-and-effect relationships in life events
  - **Dharma (🧭)**: Helps users understand life decisions and personal meaning
  - **Atma (🧘)**: Guides users toward mindfulness, inner peace, and self-awareness

- **Conversation Features**:
  - Real-time AI conversations
  - Session-based conversation history
  - Avatar-specific system prompts
  - Conversation limits and management

### Architecture

```
karma_cafe/
├── domain/
│   ├── entities/
│   │   └── avatar.py          # Avatar definitions
│   └── services/
│       └── avatar_service.py # Avatar business logic
├── application/
│   └── services/
│       └── chat_service.py    # Conversation orchestration
├── infrastructure/
│   └── external/
│       └── ai_service.py       # OpenAI integration
└── presentation/
    └── routes.py               # API endpoints
```

### API Endpoints

- `GET /api/karma/avatars` - Get all avatars
- `GET /api/karma/avatar/<avatar_id>` - Get avatar details
- `GET /api/karma/chat/<avatar_id>` - Get chat interface
- `POST /api/karma/send_message` - Send message to avatar
- `POST /api/karma/new_conversation` - Start new conversation
- `GET /api/karma/messages/<avatar_id>` - Get message history

### Technical Implementation

- **OpenAI Integration**: Uses GPT models for responses
- **Session Management**: Conversation history in Flask session
- **Avatar System**: Three distinct personalities with custom prompts
- **Error Handling**: Comprehensive error handling and recovery

## SoulQuest Module

### Description

SoulQuest is an interactive spiritual journey that guides users through reflective quests designed to promote self-discovery, mindfulness, and inner growth.

### Features

- **Multiple Quests**:
  - Self-Discovery: Explores personal identity and authenticity
  - Mindfulness Mastery: Focuses on present-moment awareness
  - Cultivating Compassion: Develops empathy and understanding

- **Quest Features**:
  - Progressive difficulty
  - Guided reflective questions
  - Progress tracking
  - Completion states
  - Reset capabilities

### Architecture

```
soul_quest/
├── domain/
│   ├── entities/
│   │   └── quest.py            # Quest definitions
│   └── services/
│       └── quest_service.py    # Quest business logic
├── application/
│   └── services/
│       └── progress_service.py # Progress management
├── infrastructure/
│   └── external/
│       └── session_service.py  # Session management
└── presentation/
    └── routes.py               # API endpoints
```

### API Endpoints

- `GET /api/soul/quests` - Get all quests
- `GET /api/soul/quest/<quest_id>` - Get quest details
- `POST /api/soul/start/<quest_id>` - Start quest
- `POST /api/soul/answer` - Answer question
- `POST /api/soul/reset` - Reset progress
- `GET /api/soul/progress` - Get progress

### Technical Implementation

- **Quest System**: Structured quest definitions with questions
- **Progress Tracking**: Session-based progress storage
- **Question Flow**: Sequential question progression
- **Completion Logic**: Automatic completion detection

## WisdomPets Module

### Description

WisdomPets provides interactive virtual spiritual animal companions based on Vedic traditions and symbolism, offering users a way to interact with and learn from spiritual animals.

### Features

- **Spiritual Animal Companions**:
  - **Ganesha (Elephant)**: Wisdom and obstacle removal
  - **Durga (Tiger)**: Courage and protection
  - **Kamadhenu (Cow)**: Abundance and nurturing
  - **Mayura (Peacock)**: Beauty and transformation
  - **Hanuman (Monkey)**: Devotion and strength

- **Interaction Features**:
  - Multiple interaction types per companion
  - Interaction history tracking
  - Effect durations
  - Interaction summaries

### Architecture

```
wisdom_pets/
├── domain/
│   ├── entities/
│   │   └── companion.py        # Companion definitions
│   └── services/
│       └── companion_service.py # Companion business logic
├── application/
│   └── services/
│       └── interaction_service.py # Interaction management
├── infrastructure/
│   └── external/
│       └── session_service.py  # Session management
└── presentation/
    └── routes.py               # API endpoints
```

### API Endpoints

- `GET /api/pets/companions` - Get all companions
- `GET /api/pets/companion/<companion_id>` - Get companion details
- `POST /api/pets/interact` - Create interaction
- `POST /api/pets/reset` - Reset interactions
- `GET /api/pets/interactions/<companion_id>` - Get interaction history
- `GET /api/pets/interaction-types/<companion_id>` - Get interaction types

### Technical Implementation

- **Companion System**: Spiritual animal definitions with traits
- **Interaction System**: Multiple interaction types with effects
- **History Tracking**: Session-based interaction history
- **Spiritual Guidance**: Companion-specific wisdom

## Module Integration

### Unified Platform

All modules are integrated through the main Flask application:

```python
# Register module blueprints
app.register_blueprint(karma_blueprint, url_prefix='/api/karma')
app.register_blueprint(soul_blueprint, url_prefix='/api/soul')
app.register_blueprint(pets_blueprint, url_prefix='/api/pets')
```

### Shared Infrastructure

- **Session Management**: Flask-Session for all modules
- **Error Handling**: Centralized error handling
- **Logging**: Unified logging system
- **Configuration**: Environment-based configuration

### React Frontend

The React frontend provides a unified interface:
- Module navigation
- Consistent UI patterns
- Shared components
- Unified state management

## Module Comparison

| Feature | KarmaCafe | SoulQuest | WisdomPets |
|---------|-----------|-----------|------------|
| **Primary Function** | AI Conversations | Quest Progression | Pet Interactions |
| **External API** | OpenAI | None | None |
| **Data Storage** | Session | Session | Session |
| **User Interaction** | Chat messages | Quest answers | Pet interactions |
| **Progress Tracking** | Conversation history | Quest completion | Interaction history |

## Development Patterns

All modules follow the same patterns:

1. **Domain-Driven Design**: Consistent layer structure
2. **Blueprint Registration**: Flask blueprints for routes
3. **Service Layer**: Application services for orchestration
4. **Error Handling**: Standardized error responses
5. **Testing**: Unit, integration, and E2E tests

## Future Enhancements

Potential improvements:
- Database persistence (beyond sessions)
- User authentication
- Cross-module features
- Advanced analytics
- Mobile app versions
