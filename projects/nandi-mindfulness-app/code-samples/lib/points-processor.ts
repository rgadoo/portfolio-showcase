/**
 * Points Processor Service
 * 
 * Server-side service for awarding and tracking points in the event-driven system.
 * Demonstrates Prisma ORM usage, aggregations, and type-safe database operations.
 */

import { prisma } from '../core/db.server';

/**
 * Parameters for awarding points
 */
export interface AwardPointsParams {
  userId: string;
  points: number;
  source: string;  // e.g., 'meditation', 'journal', 'achievement'
  description?: string;
  eventId?: string; // Link to the triggering event
  metadata?: Record<string, any>;
}

/**
 * Award points to a user and record in points history
 */
export async function awardPoints(params: AwardPointsParams): Promise<void> {
  const { userId, points, source, description, eventId, metadata } = params;
  
  try {
    // Create points history record using Prisma
    await prisma.pointsHistory.create({
      data: {
        userId,
        pointsEarned: points,
        source,
        description: description || `Points from ${source}`,
        eventId,
        metadata: metadata || {}
      }
    });
    
    console.log(`Awarded ${points} points to user ${userId} from ${source}`);
  } catch (error) {
    console.error('Error awarding points:', error);
    throw error;
  }
}

/**
 * Get total points for a user using Prisma aggregation
 */
export async function getUserTotalPoints(userId: string): Promise<number> {
  try {
    // Sum all points from points history using Prisma aggregate
    const result = await prisma.pointsHistory.aggregate({
      where: {
        userId
      },
      _sum: {
        pointsEarned: true
      }
    });
    
    return result._sum.pointsEarned || 0;
  } catch (error) {
    console.error('Error getting user points:', error);
    return 0;
  }
}

/**
 * Get points breakdown by source for a user
 * Demonstrates grouping and aggregation in application code
 */
export async function getUserPointsBySource(userId: string): Promise<Record<string, number>> {
  try {
    // Get all points history records for user
    const pointsRecords = await prisma.pointsHistory.findMany({
      where: {
        userId
      },
      select: {
        source: true,
        pointsEarned: true
      }
    });
    
    // Group by source
    const pointsBySource: Record<string, number> = {};
    
    for (const record of pointsRecords) {
      if (!pointsBySource[record.source]) {
        pointsBySource[record.source] = 0;
      }
      pointsBySource[record.source] += record.pointsEarned;
    }
    
    return pointsBySource;
  } catch (error) {
    console.error('Error getting user points by source:', error);
    return {};
  }
}

/**
 * Get recent points history with relationship includes
 */
export async function getUserRecentPoints(
  userId: string,
  limit: number = 10
): Promise<any[]> {
  try {
    return await prisma.pointsHistory.findMany({
      where: {
        userId
      },
      orderBy: {
        awardedAt: 'desc'
      },
      take: limit,
      include: {
        event: true  // Include related event data
      }
    });
  } catch (error) {
    console.error('Error getting recent points history:', error);
    return [];
  }
}
