/**
 * OpenAI Service
 * 
 * Centralized service for OpenAI API integration.
 * Demonstrates API wrapper pattern with retry logic, error handling, and timeout management.
 */

import { OpenAI } from 'openai';

export class OpenAIService {
  private openai: OpenAI;
  private retryCount = 3;
  private retryDelay = 1000; // ms
  
  constructor() {
    // Check if we're in a test environment
    const isTestEnv = process.env.NODE_ENV === 'test';
    
    if (isTestEnv) {
      // In test environment, we don't need to create a real OpenAI instance
      this.openai = {} as OpenAI;
    } else {
      // In production, create a real OpenAI instance
      this.openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY,
      });
    }
  }
  
  /**
   * Call the OpenAI API with the provided messages
   * 
   * @param messages The messages to send to the OpenAI API
   * @param options Optional parameters for the API call
   * @returns The API response
   */
  async callOpenAI(messages: any[], options?: {
    model?: string;
    temperature?: number;
    maxTokens?: number;
    timeout?: number;
    top_p?: number;
    presence_penalty?: number;
    frequency_penalty?: number;
  }) {
    const {
      model = process.env.OPENAI_MODEL || 'gpt-4',
      temperature = 0.7,
      maxTokens = 1000,
      timeout = 15000, // 15 seconds default timeout
      top_p,
      presence_penalty,
      frequency_penalty,
    } = options || {};
    
    try {
      // Create a timeout promise
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('OpenAI API request timed out')), timeout);
      });
      
      // Create the API call promise with retry logic
      const apiCallPromise = this.callWithRetry(async () => {
        return await this.openai.chat.completions.create({
          model,
          messages,
          temperature,
          max_tokens: maxTokens,
          top_p: top_p,
          presence_penalty: presence_penalty,
          frequency_penalty: frequency_penalty,
        });
      });
      
      // Race between API call and timeout
      return await Promise.race([apiCallPromise, timeoutPromise]);
    } catch (error) {
      console.error('Error calling OpenAI API:', error);
      throw error;
    }
  }
  
  /**
   * Call a function with retry logic
   * 
   * @param fn The function to call
   * @returns The result of the function call
   */
  private async callWithRetry<T>(fn: () => Promise<T>): Promise<T> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt < this.retryCount; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;
        
        // Check if we should retry based on error type
        if (this.isRetryableError(error)) {
          // Wait before retrying (with exponential backoff)
          await new Promise(resolve => setTimeout(resolve, this.retryDelay * Math.pow(2, attempt)));
          continue;
        }
        
        // Non-retryable error, rethrow
        throw error;
      }
    }
    
    // All retries exhausted
    throw lastError || new Error('Failed after retries');
  }
  
  /**
   * Check if an error is retryable
   */
  private isRetryableError(error: any): boolean {
    // Retry on network errors, timeouts, and rate limits
    if (error?.code === 'ECONNRESET' || 
        error?.code === 'ETIMEDOUT' ||
        error?.status === 429 ||
        error?.message?.includes('timeout')) {
      return true;
    }
    
    return false;
  }
}
