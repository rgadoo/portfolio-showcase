/**
 * Admin Quiz Generation API Route
 * 
 * Demonstrates Next.js API route pattern with authentication, authorization,
 * input validation, and service layer integration.
 */

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/features/admin/core/utils/auth';
import { QuizGeneratorService } from '@/features/admin/content-generation/services/quiz-generator';

/**
 * POST /api/admin/content/quiz/generate
 * 
 * Generates quiz questions using AI and persists them to the database
 * Only accessible to admin users
 */
export async function POST(request: NextRequest) {
  try {
    // 1. Authenticate admin user
    const user = await getAuthUser(request);
    if (!user || user.role !== 'admin') {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // 2. Parse and validate request body
    const body = await request.json();
    const { prompt, category = 'GENERAL', count = 1, source = 'AI' } = body;

    // Validate based on the source
    if (source === 'AI' && !prompt) {
      return NextResponse.json(
        { error: 'Prompt is required for AI-generated quizzes' },
        { status: 400 }
      );
    }

    if (source === 'GOLDEN' && !category) {
      return NextResponse.json(
        { error: 'Category is required for golden source quizzes' },
        { status: 400 }
      );
    }

    // 3. Create service and generate content
    const service = new QuizGeneratorService();
    let result;
    
    if (source === 'GOLDEN') {
      // Load from golden source
      result = await service.loadAndPersistGoldenQuiz({
        category,
        createdById: user.id
      });
    } else {
      // Generate using AI
      result = await service.generateAndPersistQuiz({
        prompt,
        category,
        count,
        createdById: user.id
      });
    }

    // 4. Return the result
    return NextResponse.json(result);
  } catch (error: any) {
    console.error('[QUIZ GENERATOR] Error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to generate quiz' },
      { status: 500 }
    );
  }
}
