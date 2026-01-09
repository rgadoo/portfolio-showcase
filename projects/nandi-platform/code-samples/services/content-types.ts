/**
 * Content Type Registry
 * Defines all available content types and their configurations
 * Each instance can enable/disable types via environment variables
 */

export interface ContentField {
  id: string;
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array' | 'object' | 'file';
  required: boolean;
  description?: string;
}

export interface UploadRules {
  maxSize: number; // in MB
  allowedFormats: string[];
  multiple?: boolean;
}

export interface ContentTypeDefinition {
  id: string;
  name: string;
  description: string;
  icon: string;
  enabled: boolean;
  fields: ContentField[];
  playerComponent: string;
  uploadRules: UploadRules;
  requiresMedia: boolean;
}

/**
 * Get list of enabled content types from environment
 */
function getEnabledContentTypes(): string[] {
  const envValue = process.env.NEXT_PUBLIC_ENABLED_CONTENT_TYPES || 'audio;video;page;collection;quiz';
  // Support both comma and semicolon separators for backwards compatibility
  const separator = envValue.includes(';') ? ';' : ',';
  return envValue.split(separator).map(type => type.trim()).filter(Boolean);
}

/**
 * Content type registry - defines all available content types
 */
const CONTENT_TYPE_DEFINITIONS: ContentTypeDefinition[] = [
  {
    id: 'audio',
    name: 'Audio',
    description: 'Audio content (podcasts, music, audiobooks, talks, meditations, etc.)',
    icon: '🎵',
    enabled: true,
    requiresMedia: true,
    playerComponent: 'AudioPlayer',
    fields: [
      { id: 'audioFile', name: 'Audio File', type: 'file', required: true },
      { id: 'duration', name: 'Duration', type: 'number', required: true, description: 'Duration in seconds' },
      { id: 'transcript', name: 'Transcript', type: 'string', required: false },
    ],
    uploadRules: {
      maxSize: 100,
      allowedFormats: ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'],
    },
  },
  {
    id: 'video',
    name: 'Video',
    description: 'Video content (tutorials, presentations, guided sessions, etc.)',
    icon: '🎥',
    enabled: true,
    requiresMedia: true,
    playerComponent: 'VideoPlayer',
    fields: [
      { id: 'videoFile', name: 'Video File', type: 'file', required: true },
      { id: 'duration', name: 'Duration', type: 'number', required: true, description: 'Duration in seconds' },
      { id: 'subtitles', name: 'Subtitles', type: 'file', required: false },
    ],
    uploadRules: {
      maxSize: 500,
      allowedFormats: ['.mp4', '.webm', '.mov', '.avi', '.mkv'],
    },
  },
  {
    id: 'collection',
    name: 'Collection',
    description: 'Multi-part grouped content (courses, series, journeys, pathways, etc.)',
    icon: '📚',
    enabled: true,
    requiresMedia: false,
    playerComponent: 'CollectionPlayer',
    fields: [
      { id: 'lessons', name: 'Lessons', type: 'array', required: true, description: 'Array of lesson IDs' },
      { id: 'modules', name: 'Modules', type: 'array', required: false, description: 'Course modules' },
      { id: 'certificate', name: 'Certificate Enabled', type: 'boolean', required: false },
      { id: 'estimatedTime', name: 'Estimated Completion Time', type: 'number', required: false, description: 'In hours' },
    ],
    uploadRules: {
      maxSize: 1000,
      allowedFormats: ['.zip'],
    },
  },
  {
    id: 'quiz',
    name: 'Quiz',
    description: 'Interactive quiz or assessment',
    icon: '📝',
    enabled: true,
    requiresMedia: false,
    playerComponent: 'QuizPlayer',
    fields: [
      { id: 'questions', name: 'Questions', type: 'array', required: true, description: 'Quiz questions' },
      { id: 'passingScore', name: 'Passing Score', type: 'number', required: false, description: 'Percentage required to pass' },
      { id: 'timeLimit', name: 'Time Limit', type: 'number', required: false, description: 'Time limit in minutes' },
      { id: 'showResults', name: 'Show Results Immediately', type: 'boolean', required: false },
    ],
    uploadRules: {
      maxSize: 10,
      allowedFormats: ['.json'],
    },
  },
  {
    id: 'page',
    name: 'Page',
    description: 'Rich content page with customizable sections (articles, landing pages, guides, etc.)',
    icon: '📄',
    enabled: true,
    requiresMedia: false,
    playerComponent: 'PageViewer',
    fields: [
      { id: 'richText', name: 'Content', type: 'string', required: true, description: 'Rich text content' },
      { id: 'images', name: 'Images', type: 'array', required: false, description: 'Article images' },
      { id: 'author', name: 'Author', type: 'string', required: false },
      { id: 'readingTime', name: 'Reading Time', type: 'number', required: false, description: 'Estimated reading time in minutes' },
    ],
    uploadRules: {
      maxSize: 50,
      allowedFormats: ['.md', '.html', '.txt'],
    },
  },
];

/**
 * Get all content type definitions
 */
export function getAllContentTypes(): ContentTypeDefinition[] {
  return CONTENT_TYPE_DEFINITIONS;
}

/**
 * Get only enabled content types based on environment configuration
 */
export function getEnabledContentTypeDefinitions(): ContentTypeDefinition[] {
  const enabledTypes = getEnabledContentTypes();
  return CONTENT_TYPE_DEFINITIONS.map(type => ({
    ...type,
    enabled: enabledTypes.includes(type.id),
  })).filter(type => type.enabled);
}

/**
 * Get a specific content type by ID
 */
export function getContentTypeById(id: string): ContentTypeDefinition | undefined {
  return CONTENT_TYPE_DEFINITIONS.find(type => type.id === id);
}

/**
 * Check if a content type is enabled
 */
export function isContentTypeEnabled(id: string): boolean {
  const enabledTypes = getEnabledContentTypes();
  return enabledTypes.includes(id);
}

/**
 * Get the player component name for a content type
 */
export function getPlayerComponentForType(contentType: string): string {
  const type = getContentTypeById(contentType);
  return type?.playerComponent || 'AudioPlayer'; // Default to AudioPlayer for backwards compatibility
}

/**
 * Validate that a content type is enabled and valid
 */
export function validateContentType(contentType: string): { valid: boolean; error?: string } {
  const type = getContentTypeById(contentType);
  
  if (!type) {
    return { valid: false, error: `Unknown content type: ${contentType}` };
  }
  
  if (!isContentTypeEnabled(contentType)) {
    return { valid: false, error: `Content type '${contentType}' is not enabled for this instance` };
  }
  
  return { valid: true };
}
