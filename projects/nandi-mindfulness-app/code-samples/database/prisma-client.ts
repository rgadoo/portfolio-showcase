/**
 * Prisma Database Client Setup
 * 
 * Demonstrates Prisma ORM client initialization with connection management,
 * error handling, and development logging.
 */

import { PrismaClient } from '@prisma/client';

// Type declaration for global context (Next.js hot reload support)
declare global {
  var prisma: PrismaClient | undefined;
}

/**
 * Creates a Prisma client with connection tracking and error handling
 */
const createPrismaClient = () => {
  try {
    console.log('[DB] Initializing Prisma client...');
    
    // Initialize with query logging in development
    const client = new PrismaClient({
      log: process.env.NODE_ENV === 'development' 
        ? ['query', 'error', 'warn'] 
        : ['error'],
    });
    
    // Add connection state tracking
    const clientWithState = Object.assign(client, {
      isConnected: false,
      isConnecting: false,
      connectionError: null
    });
    
    // Mark client as connecting
    clientWithState.isConnecting = true;
    
    // Test connection to ensure DB is accessible
    client.$connect().then(() => {
      console.log('[DB] Successfully connected to database');
      clientWithState.isConnected = true;
      clientWithState.isConnecting = false;
    }).catch(error => {
      console.error('[DB] Database connection failed:', error);
      clientWithState.connectionError = error;
      clientWithState.isConnecting = false;
    });
    
    console.log('[DB] Prisma client initialized successfully');
    return clientWithState;
  } catch (error) {
    console.error('[DB] Failed to initialize Prisma client:', error);
    
    // Create a stub client that logs errors for any operation
    // This prevents the application from crashing completely
    const stubClient: Record<string, (...args: any[]) => Promise<never>> = new Proxy({}, {
      get: (target, prop) => {
        if (prop === 'then' || prop === 'catch') return undefined;
        
        return () => {
          console.error(`[DB] Attempted to use Prisma client method '${String(prop)}' but client failed to initialize.`);
          return Promise.reject(new Error('PrismaClient failed to initialize'));
        };
      }
    });
    
    return stubClient as unknown as PrismaClient;
  }
};

// Use existing client or create a new one (Next.js hot reload support)
const prismaClient = global.prisma ?? createPrismaClient();

// Only save to global in non-production for hot reloading
if (process.env.NODE_ENV !== 'production') {
  global.prisma = prismaClient;
}

export const prisma = prismaClient;
