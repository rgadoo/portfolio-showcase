# Case Study: Domain-Driven Design in Nandi Platform

## Problem

The Nandi platform needed to support multiple distinct modules (KarmaCafe, SoulQuest, WisdomPets) while maintaining:
- Clear separation of concerns
- Modularity and maintainability
- Testability
- Scalability for future modules

The initial codebase had mixed concerns, making it difficult to:
- Understand business logic
- Test components in isolation
- Add new modules
- Maintain and refactor code

## Solution

Implemented **Domain-Driven Design (DDD)** with a layered architecture for each module.

### Architecture Layers

Each module follows a consistent 4-layer structure:

```
module/
├── domain/          # Core business logic (no dependencies)
├── application/     # Use case orchestration
├── infrastructure/  # External services & technical concerns
└── presentation/    # API endpoints
```

### Implementation Details

#### 1. Domain Layer
- **Entities**: Core business objects (Avatar, Quest, Companion)
- **Services**: Business rules and domain logic
- **Independence**: No framework dependencies

**Example - Avatar Entity:**
```python
# domain/entities/avatar.py
AVATARS = {
    "karma": {
        "name": "Karma",
        "system_prompt": "...",
        # Business logic encapsulated
    }
}
```

#### 2. Application Layer
- **Services**: Orchestrate use cases
- **Responsibilities**: Coordinate domain and infrastructure
- **No Business Rules**: Only orchestration logic

**Example - Chat Service:**
```python
# application/services/chat_service.py
class ChatService:
    def generate_response(self, avatar_id, user_message, history):
        # Orchestrates: Avatar lookup + AI service + history management
        avatar = self.avatar_service.get_avatar(avatar_id)
        messages = self._prepare_messages(avatar, history, user_message)
        return self.ai_service.generate_response(messages)
```

#### 3. Infrastructure Layer
- **External Services**: OpenAI API, Session management
- **Abstractions**: Implements interfaces from domain/application
- **Technical Concerns**: API calls, data persistence

**Example - AI Service:**
```python
# infrastructure/external/ai_service.py
class AIService:
    def generate_response(self, messages):
        # Technical implementation of AI integration
        response = openai.ChatCompletion.create(...)
        return response.choices[0].message.content
```

#### 4. Presentation Layer
- **Routes**: Flask blueprint endpoints
- **Input/Output**: Request/response handling
- **Validation**: Input validation and error handling

**Example - Routes:**
```python
# presentation/routes.py
@karma_blueprint.route('/send_message', methods=['POST'])
def send_message():
    # Handles HTTP, delegates to application service
    response = chat_service.generate_response(...)
    return jsonify(response)
```

## Benefits

### 1. Modularity
- Each module is self-contained
- Clear boundaries between modules
- Easy to understand module responsibilities

### 2. Testability
- Domain logic can be tested in isolation
- Infrastructure can be mocked
- Application services testable with mocked dependencies

### 3. Maintainability
- Changes isolated to specific layers
- Business logic separated from technical concerns
- Easy to locate and modify code

### 4. Scalability
- New modules follow same pattern
- Consistent structure across modules
- Easy to add new features

### 5. Clarity
- Clear separation of concerns
- Business logic visible and accessible
- Technical details abstracted away

## Results

- **3 Modules**: Successfully structured using DDD
- **Consistent Architecture**: All modules follow same pattern
- **Improved Testability**: Unit tests for each layer
- **Better Maintainability**: Clear code organization
- **Easier Onboarding**: New developers understand structure quickly

## Lessons Learned

1. **Start with Domain**: Define business entities first
2. **Layer Independence**: Keep layers independent where possible
3. **Consistent Patterns**: Apply same patterns across modules
4. **Clear Boundaries**: Maintain strict boundaries between layers
5. **Testability First**: Design for testability from the start

## Future Enhancements

- Database persistence layer (currently using sessions)
- Event-driven architecture for cross-module communication
- CQRS pattern for read/write separation
- Domain events for better decoupling
