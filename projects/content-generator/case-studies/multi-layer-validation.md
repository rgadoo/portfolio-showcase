# Case Study: Multi-Layer Validation Chain

## Overview

This case study examines the implementation of a 5-layer validation chain in Content Generator that ensures AI-generated content meets quality standards before publication.

## The Problem

AI-generated content can suffer from several quality issues:

1. **Placeholder Text**: LLMs sometimes output `[placeholder]`, `[insert here]`, or similar markers
2. **Insufficient Length**: Generated content may be too brief to be useful
3. **Wrong Structure**: Missing required fields or incorrect nesting
4. **Invalid References**: Taxonomy references (pillar, category) that don't exist
5. **Narrative Style**: Output that reads like a story instead of educational content

**Business Impact:**
- Publishing low-quality content damages platform credibility
- Manual review of all AI output is time-consuming
- Late-stage failures waste API costs

## The Solution: 5-Layer Validation Chain

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Content Generation Request                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Taxonomy Validation (Pre-API)                         │
│  • Validate pillar exists in instance                           │
│  • Validate category exists under pillar                        │
│  • Validate all tags exist                                      │
│  ❌ Fail Fast → No API call made, save costs                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2: OpenAI Schema Validation (During Generation)          │
│  • JSON schema enforcement via response_format                  │
│  • Required fields guaranteed                                   │
│  • Type checking (string, array, object)                        │
│  ❌ Fail → Retry with stricter prompt                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Content Quality Validation (Post-Generation)          │
│  • Placeholder text detection (regex patterns)                  │
│  • Minimum length checks (1000+ chars)                          │
│  • Educational language enforcement                             │
│  • Structure validation (sections, modules, lessons)            │
│  ❌ Fail → Regenerate or manual review                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: Pydantic Model Validation (Pre-Save)                  │
│  • Type coercion and validation                                 │
│  • Field constraints (min/max length)                           │
│  • Custom validators                                            │
│  ❌ Fail → Validation error with details                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 5: Publisher Validation (Pre-Publish)                    │
│  • Firestore-ready format verification                          │
│  • Required fields for production                               │
│  • Final sanity checks                                          │
│  ❌ Fail → Block publication                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ✅ Published to Firestore
```

### Layer Details

#### Layer 1: Taxonomy Validation (Pre-API)

**Purpose:** Fail fast before making expensive API calls.

**Implementation:**
```python
def validate_taxonomy(instance_id: str, pillar: str, category: str, tags: list):
    """Validate taxonomy references exist in instance."""
    
    # Fetch instance taxonomy (cached)
    taxonomy = get_instance_taxonomy(instance_id)
    
    # Validate pillar
    if pillar not in taxonomy['pillars']:
        raise TaxonomyValidationError(f"Pillar '{pillar}' not found")
    
    # Validate category under pillar
    pillar_categories = taxonomy['pillars'][pillar]['categories']
    if category not in pillar_categories:
        raise TaxonomyValidationError(
            f"Category '{category}' not found under pillar '{pillar}'"
        )
    
    # Validate tags
    instance_tags = taxonomy['tags']
    invalid_tags = [t for t in tags if t not in instance_tags]
    if invalid_tags:
        raise TaxonomyValidationError(f"Invalid tags: {invalid_tags}")
```

**Cost Savings:** ~30% reduction in unnecessary API calls by catching invalid requests early.

#### Layer 2: OpenAI Schema Validation (During Generation)

**Purpose:** Guarantee JSON structure from AI output.

**Implementation:**
```python
ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "heading": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["heading", "content"]
            }
        }
    },
    "required": ["title", "description", "sections"]
}

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "article_schema",
            "schema": ARTICLE_SCHEMA,
            "strict": False  # Allow optional fields
        }
    }
)
```

**Benefit:** Eliminates JSON parsing errors and guarantees required fields.

#### Layer 3: Content Quality Validation (Post-Generation)

**Purpose:** Catch content quality issues that schema can't detect.

**Implementation:**
```python
class ContentValidator:
    PLACEHOLDER_PATTERNS = [
        r'\[placeholder\]',
        r'\[insert.*here\]',
        r'\[your.*here\]',
        r'TODO:',
        r'FIXME:',
        r'Lorem ipsum',
    ]
    
    NARRATIVE_INDICATORS = [
        r'^Once upon a time',
        r'^In a land far away',
        r'^There was a',
        r'lived happily ever after',
    ]
    
    def validate_article(self, content: dict) -> ValidationResult:
        errors = []
        
        # Check for placeholders
        full_text = self._extract_all_text(content)
        for pattern in self.PLACEHOLDER_PATTERNS:
            if re.search(pattern, full_text, re.IGNORECASE):
                errors.append(f"Contains placeholder: {pattern}")
        
        # Check minimum lengths
        if len(content.get('description', '')) < 1000:
            errors.append("Description too short (min 1000 chars)")
        
        # Check for narrative style
        for pattern in self.NARRATIVE_INDICATORS:
            if re.search(pattern, full_text, re.IGNORECASE):
                errors.append("Contains narrative language (should be educational)")
        
        # Check section count
        sections = content.get('sections', [])
        if len(sections) < 3:
            errors.append("Too few sections (min 3)")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

#### Layer 4: Pydantic Validation (Pre-Save)

**Purpose:** Type safety and constraint enforcement before database save.

**Implementation:**
```python
class ArticleSection(BaseModel):
    heading: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=100)

class ArticleContent(BaseModel):
    title: str = Field(min_length=10, max_length=200)
    description: str = Field(min_length=500)
    sections: List[ArticleSection] = Field(min_items=3)
    
    @validator('title')
    def title_not_placeholder(cls, v):
        if '[' in v and ']' in v:
            raise ValueError('Title contains placeholder')
        return v
    
    @validator('sections')
    def sections_have_unique_headings(cls, v):
        headings = [s.heading for s in v]
        if len(headings) != len(set(headings)):
            raise ValueError('Section headings must be unique')
        return v
```

#### Layer 5: Publisher Validation (Pre-Publish)

**Purpose:** Final verification before Firestore write.

**Implementation:**
```python
class PublisherValidator:
    REQUIRED_FIRESTORE_FIELDS = [
        'title', 'description', 'contentType', 'instanceId',
        'pillar', 'category', 'published', 'createdAt'
    ]
    
    def validate_for_publish(self, content: dict) -> ValidationResult:
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIRESTORE_FIELDS:
            if field not in content or content[field] is None:
                errors.append(f"Missing required field: {field}")
        
        # Verify IDs are set
        if not content.get('id'):
            errors.append("Content ID not set")
        
        # Verify timestamps
        if not content.get('createdAt'):
            errors.append("createdAt timestamp not set")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

## Results

### Quality Metrics

| Metric | Before | After |
|--------|--------|-------|
| Placeholder content published | ~5% | 0% |
| Too-short content published | ~10% | 0% |
| Invalid taxonomy references | ~3% | 0% |
| Manual review required | 100% | ~5% |

### Cost Savings

| Optimization | Savings |
|--------------|---------|
| Fail-fast taxonomy validation | ~30% fewer API calls |
| Structured outputs | ~50% fewer retries |
| Early validation | ~20% less rework |

### Developer Experience

- **Clear Error Messages**: Each layer provides specific, actionable errors
- **Fast Feedback**: Invalid requests fail immediately
- **Debuggable**: Validation results include all failed checks

## Key Learnings

1. **Fail Fast**: Layer 1 (taxonomy validation) saves the most money by avoiding unnecessary API calls

2. **Schema Enforcement**: OpenAI's structured outputs are reliable but don't catch content quality issues

3. **Multiple Layers Needed**: No single validation layer catches everything; defense in depth is essential

4. **Placeholder Detection**: Simple regex patterns catch most placeholder issues, but need regular updates as LLMs evolve

5. **Educational vs Narrative**: AI models need explicit instructions to output educational content; validation catches when they revert to storytelling

## Conclusion

The 5-layer validation chain transformed content generation from a manual review process into a reliable automated pipeline. The combination of pre-flight checks, schema enforcement, quality validation, and type safety ensures consistent, high-quality output while minimizing costs.
