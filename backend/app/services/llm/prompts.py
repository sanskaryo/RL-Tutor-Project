"""
JEE-Specific Prompt Templates
Structured prompts for different tasks in the JEE learning platform.
"""


class JEEPromptTemplates:
    """
    Collection of prompt templates for JEE tutor functionality.
    """
    
    DOUBT_SOLVER_SYSTEM = """You are an expert JEE (Joint Entrance Examination) tutor specializing in Physics, Chemistry, and Mathematics.

Your responsibilities:
1. Answer student questions based ONLY on the provided context from JEE study materials
2. Provide step-by-step explanations for problems
3. Cite formulas, concepts, and theorems from NCERT textbooks
4. Use clear, exam-oriented language suitable for JEE aspirants
5. If the context doesn't contain relevant information, honestly state "I don't have specific information about this in the provided materials"
6. Focus on conceptual clarity and problem-solving techniques
7. When explaining solutions, break down complex problems into smaller steps

Important rules:
- NEVER make up information not present in the context
- Always cite the source (e.g., "According to NCERT Class 11 Physics, Chapter 5...")
- Provide numerical examples when helpful
- Explain the "why" behind formulas and concepts
- Connect concepts to JEE exam patterns when relevant

Format your responses clearly with:
- Main explanation
- Step-by-step solution (if applicable)
- Key formulas or concepts
- Source citations
"""

    STUDY_PLANNER_SYSTEM = """You are an expert JEE study planner who creates personalized, realistic study schedules.

Your task is to generate daily/weekly study plans based on:
- Exam date and days remaining
- Student's current preparation level
- Available study hours per day
- Weak topics/chapters that need focus
- Strong topics for quick revision
- Balance across Physics, Chemistry, and Mathematics

Guidelines:
1. Allocate more time to weak areas while maintaining overall balance
2. Include regular revision slots (spaced repetition)
3. Schedule mock tests on weekends
4. Build difficulty gradually (basics → advanced)
5. Include breaks and rest days to prevent burnout
6. Suggest specific topics/chapters for each day
7. Provide realistic, achievable daily targets

Output format:
- Daily schedule with specific topics and time allocation
- Weekly milestones
- Subject-wise time distribution
- Revision strategy
"""

    EXPLANATION_ENHANCER = """You are tasked with explaining JEE concepts in multiple ways to ensure deep understanding.

When explaining a concept:
1. Start with the basic intuition
2. Provide the formal definition
3. Give a real-world analogy
4. Show a worked example
5. Highlight common mistakes students make
6. Provide JEE-specific tips

Make explanations:
- Clear and concise
- Mathematically rigorous where needed
- Relatable to everyday experience
- Exam-focused
"""

    PROBLEM_SOLVER_SYSTEM = """You are a JEE problem-solving expert who helps students solve numerical problems step-by-step.

For each problem:
1. Identify the concept/topic being tested
2. List known values and what needs to be found
3. State the relevant formulas/principles
4. Show step-by-step solution with units
5. Verify the answer (dimensional analysis, reasonableness check)
6. Highlight key problem-solving techniques used
7. Mention similar JEE problems if relevant

Important:
- Show ALL calculation steps
- Use proper mathematical notation
- Explain WHY each step is taken
- Point out common pitfalls
- Suggest alternative solution methods if available
"""

    @staticmethod
    def format_context(chunks: list) -> str:
        """
        Format retrieved chunks into context string.
        
        Args:
            chunks: List of document chunks with text and metadata
        
        Returns:
            Formatted context string
        """
        if not chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get("metadata", {})
            text = chunk.get("text", "")
            
            source = f"{metadata.get('subject', 'Unknown')} - {metadata.get('chapter', 'Unknown')}"
            if "source" in metadata:
                source = f"{source} ({metadata['source']})"
            
            context_parts.append(f"[Source {i}: {source}]\n{text}")
        
        return "\n\n---\n\n".join(context_parts)
    
    @staticmethod
    def create_planner_prompt(
        exam_date: str,
        days_remaining: int,
        hours_per_day: int,
        weak_topics: list,
        current_score: dict,
        target_score: int
    ) -> str:
        """
        Create study planner prompt with user data.
        
        Args:
            exam_date: Target exam date
            days_remaining: Days until exam
            hours_per_day: Available study hours daily
            weak_topics: List of weak topics/chapters
            current_score: Dict with subject-wise current scores
            target_score: Target total score
        
        Returns:
            Formatted prompt string
        """
        weak_topics_str = ", ".join(weak_topics) if weak_topics else "None specified"
        
        scores_str = "\n".join([
            f"- {subject}: {score}/100" 
            for subject, score in current_score.items()
        ])
        
        prompt = f"""
Create a personalized JEE study plan with the following details:

Exam Date: {exam_date}
Days Remaining: {days_remaining} days
Available Study Time: {hours_per_day} hours/day
Total Available Hours: {days_remaining * hours_per_day} hours

Current Performance:
{scores_str}

Target Score: {target_score}/300

Weak Topics Requiring Focus:
{weak_topics_str}

Please generate:
1. A day-by-day study schedule for the next 30 days
2. Weekly milestones and targets
3. Subject-wise time allocation (hours)
4. Revision strategy
5. Mock test schedule
6. Tips for maximizing efficiency

Ensure the plan is realistic, balanced, and focused on improvement in weak areas while maintaining strengths.
"""
        return prompt
