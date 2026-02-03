# Content Generator - Code Samples

Sanitized code examples demonstrating key implementation patterns.

## Directory Structure

```
code-samples/
├── README.md              # This file
├── services/
│   ├── openai_service.py      # OpenAI integration with structured outputs
│   ├── prompt_builder.py      # Layered prompt construction
│   └── validator_service.py   # Multi-layer validation
├── models/
│   └── schemas.py             # Pydantic models and JSON schemas
└── utils/
    └── retry_logic.py         # Exponential backoff implementation
```

## Key Patterns Demonstrated

### 1. Structured Outputs with OpenAI

The `openai_service.py` demonstrates:
- JSON schema enforcement via `response_format`
- Token usage tracking
- Cost estimation
- Retry with exponential backoff

### 2. Layered Prompt Engineering

The `prompt_builder.py` shows:
- Template-based prompt system
- Variable interpolation
- System/user prompt separation
- Context injection

### 3. Multi-Layer Validation

The `validator_service.py` illustrates:
- 5-layer validation chain
- Placeholder detection
- Minimum length enforcement
- Educational language validation

### 4. Retry Logic

The `retry_logic.py` demonstrates:
- Exponential backoff formula
- Jitter for distributed systems
- Max retry limits
- Retry-After header support

---

## Sample: OpenAI Service (Excerpt)

```python
class OpenAIService:
    """OpenAI integration with structured outputs and cost tracking."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.total_tokens_used = 0
        self.total_requests = 0
        self.failed_requests = 0
    
    def generate_structured_content(
        self,
        prompt: str,
        schema: dict,
        schema_name: str,
        max_tokens: int = 4000,
        temperature: float = 0.7
    ) -> dict:
        """Generate content with JSON schema enforcement."""
        
        for attempt in range(self.max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=settings.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": schema_name,
                            "schema": schema,
                            "strict": False
                        }
                    },
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                self._track_usage(response.usage)
                return json.loads(response.choices[0].message.content)
                
            except RateLimitError:
                delay = self._calculate_backoff(attempt)
                time.sleep(delay)
            except APITimeoutError:
                delay = self._calculate_backoff(attempt)
                time.sleep(delay)
        
        self.failed_requests += 1
        raise GenerationError("Max retries exceeded")
    
    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff with jitter."""
        delay = self.base_delay * (2 ** attempt)
        delay *= random.uniform(0.9, 1.1)  # ±10% jitter
        return min(delay, self.max_delay)
    
    def _track_usage(self, usage):
        """Track token usage for cost estimation."""
        self.total_tokens_used += usage.total_tokens
        self.total_requests += 1
    
    def get_usage_stats(self) -> dict:
        """Return usage statistics and cost estimate."""
        success_rate = (
            (self.total_requests - self.failed_requests) / self.total_requests
            if self.total_requests > 0 else 0
        )
        return {
            "total_tokens_used": self.total_tokens_used,
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "success_rate": success_rate,
            "estimated_cost": self._estimate_cost()
        }
```

---

## Sample: Validation Chain (Excerpt)

```python
class ContentValidatorService:
    """Multi-layer content validation."""
    
    PLACEHOLDER_PATTERNS = [
        r'\[placeholder\]',
        r'\[.*?\]',  # [any bracket content]
        r'TODO:',
        r'FIXME:',
        r'INSERT.*HERE',
    ]
    
    def validate_article(self, content: dict) -> ValidationResult:
        """Validate article content through all layers."""
        errors = []
        
        # Layer 1: Required fields
        required = ['title', 'description', 'sections']
        for field in required:
            if not content.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Layer 2: Placeholder detection
        text_content = self._extract_text(content)
        for pattern in self.PLACEHOLDER_PATTERNS:
            if re.search(pattern, text_content, re.IGNORECASE):
                errors.append(f"Contains placeholder pattern: {pattern}")
        
        # Layer 3: Minimum lengths
        if len(content.get('description', '')) < 1000:
            errors.append("Description must be at least 1000 characters")
        
        # Layer 4: Structure validation
        sections = content.get('sections', [])
        if len(sections) < 2:
            errors.append("Article must have at least 2 sections")
        
        for i, section in enumerate(sections):
            if not section.get('heading'):
                errors.append(f"Section {i+1} missing heading")
            if not section.get('content'):
                errors.append(f"Section {i+1} missing content")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
    
    def _extract_text(self, content: dict) -> str:
        """Extract all text content for validation."""
        texts = [
            content.get('title', ''),
            content.get('description', ''),
        ]
        for section in content.get('sections', []):
            texts.append(section.get('heading', ''))
            texts.append(section.get('content', ''))
        return ' '.join(texts)
```

---

## Sample: Retry Logic (Excerpt)

```python
def retry_with_exponential_backoff(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 300.0,
    retryable_exceptions: tuple = (RateLimitError, APITimeoutError)
) -> Any:
    """
    Execute function with exponential backoff retry.
    
    Formula: delay = base_delay * (2 ** attempt) * jitter
    Jitter: ±10% randomization
    """
    
    for attempt in range(max_attempts):
        try:
            return func()
        except retryable_exceptions as e:
            if attempt == max_attempts - 1:
                raise
            
            # Calculate delay with exponential backoff
            delay = base_delay * (2 ** attempt)
            
            # Add jitter (±10%)
            jitter = random.uniform(0.9, 1.1)
            delay *= jitter
            
            # Cap at max delay
            delay = min(delay, max_delay)
            
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {delay:.2f}s..."
            )
            time.sleep(delay)
    
    raise MaxRetriesExceeded(f"Failed after {max_attempts} attempts")


class TranscriptQueueRetry:
    """Queue-based retry with persistent scheduling."""
    
    def schedule_retry(self, queue_item: QueueItem, error: Exception):
        """Schedule retry with exponential backoff."""
        
        retry_count = queue_item.retry_count + 1
        
        if retry_count > self.max_retries:
            queue_item.status = 'failed'
            queue_item.error_message = str(error)
            return
        
        # Calculate next retry time
        delay = self.base_delay * (2 ** retry_count)
        delay *= random.uniform(0.9, 1.1)  # Jitter
        delay = min(delay, 300)  # Cap at 5 minutes
        
        queue_item.retry_count = retry_count
        queue_item.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)
        queue_item.status = 'pending'
```

---

**Note:** All code samples have been sanitized to remove sensitive information while preserving implementation patterns.
