/**
 * Tenant Context - Multi-Tenant Request Scoping
 * 
 * This module provides automatic tenant isolation for the entire request lifecycle.
 * It follows SaaS multi-tenant best practices by:
 * 
 * 1. Automatically detecting tenant from request (middleware sets headers)
 * 2. Providing a single source of truth for tenant ID
 * 3. Eliminating manual instanceId passing throughout the codebase
 * 4. Working seamlessly with Next.js App Router server components
 * 
 * Usage:
 *   // In any server component or API route:
 *   import { getTenantId } from '@/lib/tenant-context';
 *   const tenantId = getTenantId(); // Automatically resolved
 * 
 * Architecture:
 *   Request → Middleware (sets x-instance-id header) → Server Component/API
 *                                                       ↓
 *                                            getTenantId() reads header
 *                                                       ↓
 *                                            CMS queries auto-filtered
 */

import { headers } from 'next/headers';

// DEVELOPMENT-ONLY FALLBACK: This should only be used during local development
// In production, all requests MUST have a tenant ID from middleware
export const DEFAULT_TENANT_ID = 'example-instance';

// Header name set by middleware
const TENANT_HEADER = 'x-instance-id';
const PLATFORM_MODE_HEADER = 'x-platform-mode';

/**
 * Get the current tenant ID from request context
 * 
 * This is the primary function for multi-tenant isolation.
 * It reads from Next.js headers (set by middleware) and provides
 * automatic tenant scoping for all downstream queries.
 * 
 * @returns The current tenant ID
 */
export function getTenantId(): string {
  try {
    const headersList = headers();
    const instanceId = headersList.get(TENANT_HEADER);
    
    if (instanceId) {
      return instanceId;
    }
    
    // Fallback to environment variable for development
    if (process.env.NEXT_PUBLIC_INSTANCE_ID) {
      if (process.env.NODE_ENV === 'production') {
        console.warn('[MULTI-TENANT] No instance ID in headers, using env fallback. This should not happen in production.');
      }
      return process.env.NEXT_PUBLIC_INSTANCE_ID;
    }
    
    // Last resort fallback - should only happen in development
    if (process.env.NODE_ENV === 'production') {
      console.error('[MULTI-TENANT] No instance ID found in production! Using default fallback.');
    }
    return DEFAULT_TENANT_ID;
  } catch {
    // headers() throws when called outside request context (e.g., build time)
    // Return env variable or default for backwards compatibility
    const fallback = process.env.NEXT_PUBLIC_INSTANCE_ID || DEFAULT_TENANT_ID;
    if (process.env.NODE_ENV === 'production' && fallback === DEFAULT_TENANT_ID) {
      console.error('[MULTI-TENANT] Build-time tenant resolution in production! This indicates a configuration error.');
    }
    return fallback;
  }
}

/**
 * Check if current request is in platform mode
 * Platform mode has no specific tenant - it's the SaaS control plane
 */
export function isPlatformMode(): boolean {
  try {
    const headersList = headers();
    return headersList.get(PLATFORM_MODE_HEADER) === 'true';
  } catch {
    return false;
  }
}

/**
 * Get tenant ID or null for platform mode
 * Use this when you need to distinguish between instance mode and platform mode
 */
export function getTenantIdOrNull(): string | null {
  if (isPlatformMode()) {
    return null;
  }
  return getTenantId();
}

/**
 * Assert that we're in a tenant context (not platform mode)
 * Throws error if accessed from platform mode
 */
export function requireTenantId(): string {
  if (isPlatformMode()) {
    throw new Error('This resource requires a tenant context. Platform mode does not have tenant access.');
  }
  return getTenantId();
}

/**
 * Type guard to check if a tenant ID is valid
 */
export function isValidTenantId(id: string | null | undefined): id is string {
  return typeof id === 'string' && id.length > 0;
}

/**
 * Tenant-aware wrapper for database queries
 * 
 * This is a higher-order function that wraps any query function
 * and automatically injects the tenant ID.
 * 
 * @example
 * const getContent = withTenantScope(async (tenantId) => {
 *   return db.collection('content').where('instanceId', '==', tenantId).get();
 * });
 * 
 * // Usage - tenantId is automatically injected
 * const content = await getContent();
 */
export function withTenantScope<T>(
  queryFn: (tenantId: string) => Promise<T>
): () => Promise<T> {
  return async () => {
    const tenantId = getTenantId();
    return queryFn(tenantId);
  };
}

/**
 * Create a tenant-scoped Firestore query filter
 * Returns the filter condition for multi-tenant queries
 */
export function getTenantFilter() {
  const tenantId = getTenantId();
  return {
    field: 'instanceId',
    operator: '==' as const,
    value: tenantId,
  };
}
