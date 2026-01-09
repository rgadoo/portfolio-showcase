/**
 * Quiz Generator Service
 * 
 * Handles generating quiz questions using AI and persisting them to the database.
 * Demonstrates AI integration, Prisma ORM usage, and service layer patterns.
 */

import { prisma } from '@/lib/core/db.server';
import { QuizAIService } from '@/lib/ai/features/quiz';
import { GenerateQuizOptions, QuizGenerationResult } from '../types';

export class QuizGeneratorService {
  private aiService: QuizAIService;
  
  constructor() {
    this.aiService = new QuizAIService();
  }
  
  /**
   * Generate quizzes using AI and persist them to the database
   * 
   * @param options Options for generating quiz questions
   * @returns Result of the generation process
   */
  async generateAndPersistQuiz(options: GenerateQuizOptions): Promise<QuizGenerationResult> {
    const { prompt, category, count, createdById } = options;
    
    // Track generation stats
    let successCount = 0;
    
    try {
      // 1. Generate the quiz questions using the AI service
      const questions = await this.aiService.generateMultipleQuizQuestions(prompt, count);
      
      // 2. Create a quiz container in the database using Prisma
      const quiz = await prisma.quiz.create({
        data: {
          title: `Quiz: ${prompt.slice(0, 50)}${prompt.length > 50 ? '...' : ''}`,
          prompt, // Required field in the Quiz model 
          source: 'AI_GENERATED', // Required field in the Quiz model
          type: 'INSIGHT_LOOP',
          category: category.toUpperCase(),
          createdById, // Optional field for the creator's user ID
        },
      });
      
      // 3. For each generated question, create a DB record
      for (const question of questions) {
        await prisma.quizQuestion.create({
          data: {
            quizId: quiz.id,
            question: question.question,
            options: question.options, // This is JSON in the DB
            correctOption: question.correctOption,
            metadata: question.metadata, // This is JSON in the DB
          }
        });
        successCount++;
      }
      
      // 4. Return the result
      return {
        success: true,
        quizId: quiz.id,
        questionsGenerated: successCount,
        message: `Successfully generated ${successCount} questions`
      };
    } catch (error) {
      console.error('[QUIZ GENERATOR] Error generating questions:', error);
      return {
        success: false,
        questionsGenerated: 0,
        error: error instanceof Error ? error.message : 'Failed to generate quiz questions'
      };
    }
  }
}
