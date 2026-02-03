# Case Study: Retry Logic with Exponential Backoff

## Overview

This case study examines the implementation of robust retry logic with exponential backoff in Content Generator, handling rate limits from both OpenAI and YouTube APIs.

## The Problem

Content Generator integrates with multiple external APIs that have rate limits:

1. **OpenAI API**: Token-per-minute and request-per-minute limits
2. **YouTube Data API**: Daily quota limits and per-second rate limits
3. **Network Issues**: Transient failures, timeouts, connection resets

**Without proper retry logic:**
- Single failures could halt entire batch processing
- Rate limit errors would cascade into complete failure
- No visibility into failure patterns

## The Solution: Multi-Strategy Retry System

### Core Retry Logic

#### Exponential Backoff Formula

```
delay = base_delay × 2^attempt × jitter
```

Where:
- `base_delay`: Starting delay (default 1 second)
- `attempt`: Current attempt number (0-indexed)
- `jitter`: Random factor between 0.9 and 1.1 (±10%)

#### Implementation

```python
def calculate_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 300.0) -> float:
    """
    Calculate delay with exponential backoff and jitter.
    
    Examples:
        attempt 0: 1s × 1 × jitter = ~1s
        attempt 1: 1s × 2 × jitter = ~2s
        attempt 2: 1s × 4 × jitter = ~4s
        attempt 3: 1s × 8 × jitter = ~8s
        ...capped at max_delay
    """
    # Exponential growth
    delay = base_delay * (2 ** attempt)
    
    # Add jitter (±10%) to prevent thundering herd
    jitter = random.uniform(0.9, 1.1)
    delay *= jitter
    
    # Cap at maximum delay
    return min(delay, max_delay)
```

### OpenAI Service Retry

**Retry Configuration:**
- Max attempts: 3 (configurable via `OPENAI_RETRY_ATTEMPTS`)
- Base delay: 1 second
- Max delay: 60 seconds
- Retryable errors: `RateLimitError`, `APITimeoutError`, `APIConnectionError`

**Implementation:**

```python
class OpenAIService:
    def __init__(self):
        self.max_attempts = settings.openai_retry_attempts
        self.base_delay = 1.0
        self.max_delay = 60.0
    
    def generate_structured_content(self, prompt: str, schema: dict) -> dict:
        last_error = None
        
        for attempt in range(self.max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=settings.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_schema", "json_schema": {...}}
                )
                return json.loads(response.choices[0].message.content)
                
            except RateLimitError as e:
                last_error = e
                delay = self._get_retry_delay(e, attempt)
                logger.warning(f"Rate limited. Retrying in {delay:.2f}s...")
                time.sleep(delay)
                
            except APITimeoutError as e:
                last_error = e
                delay = calculate_backoff(attempt, self.base_delay, self.max_delay)
                logger.warning(f"Timeout. Retrying in {delay:.2f}s...")
                time.sleep(delay)
                
            except APIConnectionError as e:
                last_error = e
                delay = calculate_backoff(attempt, self.base_delay, self.max_delay)
                logger.warning(f"Connection error. Retrying in {delay:.2f}s...")
                time.sleep(delay)
        
        # All retries exhausted
        self.failed_requests += 1
        raise GenerationError(f"Failed after {self.max_attempts} attempts: {last_error}")
    
    def _get_retry_delay(self, error: RateLimitError, attempt: int) -> float:
        """Extract Retry-After header or use exponential backoff."""
        if hasattr(error, 'response') and error.response:
            retry_after = error.response.headers.get('Retry-After')
            if retry_after:
                return float(retry_after)
        return calculate_backoff(attempt, self.base_delay, self.max_delay)
```

### YouTube Transcript Queue Retry

**Different Strategy:** Queue-based retry with persistent scheduling.

**Retry Configuration:**
- Max retries: 10 (configurable)
- Base delay: 60 seconds (YouTube quotas reset slowly)
- Max delay: 300 seconds (5 minutes)
- Persistent: Stored in database, survives restarts

**Implementation:**

```python
class TranscriptQueueService:
    def __init__(self):
        self.max_retries = 10
        self.base_delay = 60  # YouTube needs longer delays
        self.max_delay = 300
    
    def process_queue(self):
        """Process pending items in the transcript queue."""
        while True:
            item = self._get_next_pending_item()
            if not item:
                break
            
            try:
                self._mark_processing(item)
                transcript = self._fetch_transcript(item.video_id)
                self._save_transcript(item, transcript)
                self._mark_completed(item)
                
            except TranscriptNotAvailable as e:
                # Permanent failure - no retry
                self._mark_failed(item, str(e))
                
            except QuotaExceeded as e:
                # Schedule retry with backoff
                self._schedule_retry(item, e)
                
            except TransientError as e:
                # Schedule retry with backoff
                self._schedule_retry(item, e)
    
    def _schedule_retry(self, item: QueueItem, error: Exception):
        """Schedule retry with exponential backoff."""
        retry_count = item.retry_count + 1
        
        if retry_count > self.max_retries:
            self._mark_failed(item, f"Max retries exceeded: {error}")
            return
        
        # Calculate next retry time
        delay = calculate_backoff(
            attempt=retry_count,
            base_delay=self.base_delay,
            max_delay=self.max_delay
        )
        
        # Check for Retry-After header
        if hasattr(error, 'retry_after') and error.retry_after:
            delay = max(delay, error.retry_after)
        
        item.retry_count = retry_count
        item.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)
        item.status = 'pending'
        item.last_error = str(error)
        
        self.db.commit()
        
        logger.info(
            f"Scheduled retry {retry_count}/{self.max_retries} for video "
            f"{item.video_id} in {delay:.0f}s"
        )
    
    def _get_next_pending_item(self) -> Optional[QueueItem]:
        """Get next item ready for processing."""
        return self.db.query(QueueItem).filter(
            QueueItem.status == 'pending',
            QueueItem.next_retry_at <= datetime.utcnow()
        ).order_by(QueueItem.next_retry_at).first()
```

### Jitter: Preventing Thundering Herd

**Problem:** Without jitter, all failed requests retry at the same time, causing another rate limit spike.

**Solution:** Add ±10% random variation to retry delays.

```
Without jitter:
  Request 1 retries at: T+4s
  Request 2 retries at: T+4s
  Request 3 retries at: T+4s
  → All hit API simultaneously → Rate limited again

With jitter:
  Request 1 retries at: T+3.8s
  Request 2 retries at: T+4.2s
  Request 3 retries at: T+4.0s
  → Spread across 0.4s window → Better success rate
```

### Error Classification

Not all errors should be retried:

```python
class ErrorClassifier:
    """Classify errors as retryable or permanent."""
    
    RETRYABLE_ERRORS = (
        RateLimitError,      # Too many requests
        APITimeoutError,     # Request timed out
        APIConnectionError,  # Network issue
        ServiceUnavailable,  # 503 errors
    )
    
    PERMANENT_ERRORS = (
        AuthenticationError,  # Invalid API key
        InvalidRequestError,  # Bad request
        NotFoundError,        # Resource doesn't exist
        PermissionDenied,     # Access denied
    )
    
    @classmethod
    def is_retryable(cls, error: Exception) -> bool:
        return isinstance(error, cls.RETRYABLE_ERRORS)
```

## Monitoring & Observability

### Retry Metrics

```python
class RetryMetrics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_retries = 0
        self.retry_distribution = defaultdict(int)  # retries -> count
    
    def record_success(self, retries_needed: int):
        self.total_requests += 1
        self.successful_requests += 1
        self.total_retries += retries_needed
        self.retry_distribution[retries_needed] += 1
    
    def record_failure(self, retries_attempted: int):
        self.total_requests += 1
        self.failed_requests += 1
        self.total_retries += retries_attempted
    
    def get_stats(self) -> dict:
        return {
            "success_rate": self.successful_requests / max(self.total_requests, 1),
            "avg_retries": self.total_retries / max(self.total_requests, 1),
            "retry_distribution": dict(self.retry_distribution),
        }
```

### Logging

```python
def log_retry(attempt: int, max_attempts: int, error: Exception, delay: float):
    logger.warning(
        f"Retry {attempt + 1}/{max_attempts} after {type(error).__name__}. "
        f"Waiting {delay:.2f}s. Error: {error}"
    )

def log_final_failure(max_attempts: int, error: Exception):
    logger.error(
        f"Request failed after {max_attempts} attempts. "
        f"Final error: {type(error).__name__}: {error}"
    )
```

## Results

### Before Retry Implementation

| Metric | Value |
|--------|-------|
| Success rate (with rate limits) | ~70% |
| Batch processing completion | ~60% |
| Manual intervention required | Frequent |

### After Retry Implementation

| Metric | Value |
|--------|-------|
| Success rate (with rate limits) | ~99% |
| Batch processing completion | ~98% |
| Manual intervention required | Rare |

### Retry Distribution (Typical)

| Retries Needed | Percentage |
|----------------|------------|
| 0 (first try) | 85% |
| 1 | 10% |
| 2 | 4% |
| 3+ | 1% |

## Key Learnings

1. **Jitter is Essential**: Without jitter, retry storms can make rate limiting worse

2. **Different APIs Need Different Strategies**:
   - OpenAI: Short delays, few retries (rate limits reset quickly)
   - YouTube: Longer delays, more retries (daily quota)

3. **Respect Retry-After Headers**: APIs that provide them know best

4. **Classify Errors**: Don't retry permanent failures

5. **Persistent Queues for Long Operations**: Database-backed queues survive process restarts

6. **Monitor Retry Patterns**: High retry rates indicate capacity issues

## Conclusion

Robust retry logic with exponential backoff transformed batch processing from fragile to reliable. The combination of immediate retries for transient errors and queue-based retries for quota issues ensures maximum throughput while respecting API limits.
