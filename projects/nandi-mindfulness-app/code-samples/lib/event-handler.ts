/**
 * Universal Event Handler
 * 
 * Server-side event handler that processes events and triggers achievement/points systems.
 * Demonstrates event-driven architecture with pattern matching and rule-based processing.
 */

import { UserEvent } from '@prisma/client';
import { processEventForAchievements } from '../achievements/achievementProcessor.server';
import { awardPoints } from '../points/pointsProcessor.server';
import { loadRulesConfiguration } from './interpreters/configLoader';
import { EventPattern, EventRule } from './types';

/**
 * Process a user event through all applicable systems
 * This is called after an event is recorded in the database
 */
export async function processEvent(event: UserEvent): Promise<UserEvent | void> {
  try {
    console.log(`[EVENT PROCESSOR] Starting to process event: ${event.action} ${event.objectType} (${event.id})`);
    
    // 1. Process for achievements
    try {
      await processEventForAchievements(event);
      console.log(`[EVENT PROCESSOR] Successfully processed achievements for event ${event.id}`);
    } catch (achievementError) {
      console.error(`[EVENT PROCESSOR] Achievement processing failed for event ${event.id}:`, achievementError);
    }
    
    // 2. Process for points based on event rules
    try {
      await processEventForPoints(event);
      console.log(`[EVENT PROCESSOR] Successfully processed points for event ${event.id}`);
    } catch (pointsError) {
      console.error(`[EVENT PROCESSOR] Points processing failed for event ${event.id}:`, pointsError);
    }
    
    // 3. Log event processing completion
    console.log(`[EVENT PROCESSOR] Event fully processed: ${event.action} ${event.objectType} for user ${event.userId}`);
    
    return event;
  } catch (error) {
    console.error('[EVENT PROCESSOR] Error in main processEvent function:', error);
    // Do not throw - we don't want to interrupt the flow if processing fails
  }
}

/**
 * Check if an event matches conditions in a pattern
 * Demonstrates pattern matching for event-driven rules
 */
function eventMatchesConditions(event: UserEvent, pattern: EventPattern): boolean {
  // Basic matching - must match action and objectType
  if (pattern.action !== event.action || pattern.objectType !== event.objectType) {
    return false;
  }
  
  // Match objectId if specified
  if (pattern.objectId && pattern.objectId !== event.objectId) {
    return false;
  }
  
  // Check conditions if any exist
  if (pattern.conditions && pattern.conditions.length > 0) {
    const eventMetadata = event.metadata as Record<string, any>;
    
    // Each condition must be satisfied
    for (const condition of pattern.conditions) {
      const { property, operator, value } = condition;
      const metadataValue = eventMetadata[property];
      
      // If property doesn't exist in metadata, condition fails
      if (metadataValue === undefined) {
        return false;
      }
      
      // Check based on operator type
      switch (operator) {
        case 'equals':
          if (metadataValue !== value) return false;
          break;
        case 'greaterThan':
          if (typeof metadataValue !== 'number' || metadataValue <= value) return false;
          break;
        case 'lessThan':
          if (typeof metadataValue !== 'number' || metadataValue >= value) return false;
          break;
        case 'contains':
          if (typeof metadataValue !== 'string' || 
              typeof value !== 'string' || 
              !metadataValue.includes(value)) {
            return false;
          }
          break;
        default:
          return false;
      }
    }
  }
  
  // All conditions passed
  return true;
}

/**
 * Award points based on event rules defined in configuration
 * Demonstrates rule-based points system
 */
async function processEventForPoints(event: UserEvent): Promise<void> {
  try {
    // Load points rules from configuration
    const rules = await loadRulesConfiguration('spiritual') as EventRule[];
    
    // Find matching rules for this event
    const matchingRules = rules.filter(rule => {
      return eventMatchesConditions(event, rule.pattern);
    });
    
    if (matchingRules.length === 0) {
      // No matching rules, no points to award
      return;
    }
    
    // Process each matching rule
    for (const rule of matchingRules) {
      // Skip if not a points award or if no points specified
      if (!rule.outcome || 
          rule.outcome.type !== 'award_points' || 
          !rule.outcome.basePoints || 
          rule.outcome.basePoints <= 0) {
        continue;
      }
      
      // Calculate points to award
      let pointsToAward = rule.outcome.basePoints;
      const eventMetadata = event.metadata as Record<string, any>;
      
      // Apply multiplier if available in the metadata
      if (eventMetadata?.pointsMultiplier) {
        pointsToAward = Math.round(pointsToAward * eventMetadata.pointsMultiplier);
      }
      
      // Skip if no points to award after calculation
      if (pointsToAward <= 0) {
        continue;
      }
      
      // Award points
      await awardPoints({
        userId: event.userId,
        points: pointsToAward,
        source: rule.outcome.category || event.objectType,
        description: rule.description || `${event.action} ${event.objectType}`,
        eventId: event.id,
        metadata: {
          action: event.action,
          objectType: event.objectType,
          category: rule.outcome.category,
          eventMetadata: event.metadata
        }
      });
      
      console.log(`Awarded ${pointsToAward} points to user ${event.userId} for ${event.action} ${event.objectType}`);
    }
  } catch (error) {
    console.error('Error processing event for points:', error);
  }
}
