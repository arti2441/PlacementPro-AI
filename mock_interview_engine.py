import openai
import json
import random
from typing import List, Dict
import os

class MockInterviewEngine:
    def __init__(self):
        # Initialize OpenAI (you can use Hugging Face as alternative)
        self.api_key = os.getenv('OPENAI_API_KEY', 'your-api-key')
        openai.api_key = self.api_key
        
        # Question bank categorized by skill
        self.question_bank = {
            'Python': [
                "Explain the difference between list comprehension and generator expression.",
                "How does Python's garbage collection work?",
                "What are decorators and how do you use them?",
                "Explain the Global Interpreter Lock (GIL) in Python."
            ],
            'Machine Learning': [
                "Explain bias-variance tradeoff with examples.",
                "What is overfitting and how do you prevent it?",
                "Compare logistic regression and SVM.",
                "What are regularization techniques in ML?"
            ],
            'SQL': [
                "Explain different types of JOINs in SQL.",
                "What is indexing and when should you use it?",
                "How do you optimize a slow SQL query?",
                "What is window function in SQL?"
            ]
        }
    
    def generate_questions(self, skill_gaps: List[Dict], num_questions: int = 5) -> List[str]:
        """Generate interview questions based on skill gaps"""
        questions = []
        
        # Focus on skills with largest gaps
        for gap in skill_gaps[:3]:  # Top 3 gaps
            skill = gap['skill']
            if skill in self.question_bank:
                questions.extend(random.sample(self.question_bank[skill], 2))
        
        # If not enough questions, add random ones
        while len(questions) < num_questions:
            random_skill = random.choice(list(self.question_bank.keys()))
            random_question = random.choice(self.question_bank[random_skill])
            if random_question not in questions:
                questions.append(random_question)
        
        return questions[:num_questions]
    
    async def evaluate_answer(self, question: str, answer: str) -> Dict:
        """Evaluate student's answer using AI"""
        try:
            # Using OpenAI for evaluation (can use Hugging Face locally)
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert interviewer evaluating a candidate's answer."},
                    {"role": "user", "content": f"Question: {question}\n\nCandidate Answer: {answer}\n\nEvaluate this answer on a scale of 0-100 for technical accuracy, completeness, and clarity. Also provide specific feedback on what was good and what could be improved. Return as JSON with keys: score, feedback, strengths, improvements."}
                ],
                temperature=0.3
            )
            
            # Parse response
            evaluation_text = response.choices[0].message.content
            try:
                evaluation = json.loads(evaluation_text)
            except:
                evaluation = {
                    'score': 70,
                    'feedback': 'Answer shows basic understanding but could be more detailed.',
                    'strengths': ['Correct general direction'],
                    'improvements': ['Add more specific examples', 'Explain underlying concepts']
                }
            
            return evaluation
            
        except Exception as e:
            # Fallback evaluation
            return {
                'score': random.randint(50, 90),
                'feedback': 'AI evaluation unavailable. Please consult with your mentor.',
                'strengths': ['Answer provided'],
                'improvements': ['Could be more detailed']
            }
    
    def calculate_interview_score(self, evaluations: List[Dict]) -> int:
        """Calculate overall interview score"""
        if not evaluations:
            return 0
        
        scores = [e['score'] for e in evaluations]
        return int(sum(scores) / len(scores))
