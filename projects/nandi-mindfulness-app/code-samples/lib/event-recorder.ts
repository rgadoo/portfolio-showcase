/**
 * Event Recorder Service
 * 
 * Core service for recording user events in the event-driven system.
 * Demonstrates event recording, filtering, and pagination with Prisma.
 */

import { prisma } from "../core/db.server";
import { processEvent } from "./eventHandler.server";
import type { CreateEventParams } from "./types";

/**
 * Records a user event in the database and triggers event processing
 * 
 * @param params Event parameters including userId, action, objectType, etc.
 * @returns The created event record
 */
export async function recordEvent(params: CreateEventParams) {
  const { userId, action, objectType, objectId, sessionId, metadata } = params;
  
  try {
    // Create the event record using Prisma
    const event = await prisma.userEvent.create({
      data: {
        userId,
        action,
        objectType,
        objectId,
        sessionId,
        metadata: metadata || {}, // Ensure we always have an object
      },
    });

    // Process the event through event handler (achievements, points)
    await processEvent(event);

    return event;
  } catch (error) {
    console.error("Failed to record event:", error);
    throw new Error(`Failed to record event: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * Retrieves events for a specific user with optional filtering
 * Demonstrates Prisma query building, filtering, and pagination
 * 
 * @param userId The user ID to retrieve events for
 * @param filter Optional filtering parameters
 * @returns List of user events matching the criteria
 */
export async function getUserEvents(userId: string, filter?: {
  action?: string;
  objectType?: string;
  startDate?: Date;
  endDate?: Date;
  limit?: number;
  offset?: number;
}) {
  const { action, objectType, startDate, endDate, limit = 20, offset = 0 } = filter || {};
  
  // Build the where clause based on filter parameters
  const where: any = { userId };
  
  if (action) where.action = action;
  if (objectType) where.objectType = objectType;
  
  // Add date range filter if provided
  if (startDate || endDate) {
    where.createdAt = {};
    if (startDate) where.createdAt.gte = startDate;
    if (endDate) where.createdAt.lte = endDate;
  }
  
  try {
    // Query events with pagination
    const events = await prisma.userEvent.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: limit,
      skip: offset,
    });
    
    // Get total count for pagination metadata
    const total = await prisma.userEvent.count({ where });
    
    return {
      events,
      pagination: {
        total,
        offset,
        limit,
        hasMore: offset + events.length < total,
      },
    };
  } catch (error) {
    console.error("Failed to retrieve user events:", error);
    throw new Error(`Failed to retrieve user events: ${error instanceof Error ? error.message : String(error)}`);
  }
}
