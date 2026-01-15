import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pickle
import os

class SkillAnalyzer:
    def __init__(self):
        self.model_path = 'skill_model.pkl'
        self.scaler_path = 'skill_scaler.pkl'
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load or train ML model for skill gap analysis"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
        else:
            self.train_default_model()
    
    def train_default_model(self):
        """Train default model with industry data"""
        # Sample industry data for Data Science roles
        industry_data = [
            # [Python, ML, SQL, Statistics, DeepLearning, Cloud, Communication]
            [90, 85, 85, 90, 80, 70, 85],  # Google Data Scientist
            [85, 90, 80, 85, 85, 75, 80],  # Amazon ML Engineer
            [80, 75, 90, 80, 70, 65, 90],  # Microsoft Data Analyst
            [95, 80, 75, 85, 90, 85, 75],  # Netflix Research Scientist
        ]
        
        X = np.array(industry_data)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = NearestNeighbors(n_neighbors=2, metric='euclidean')
        self.model.fit(X_scaled)
        
        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def analyze_skill_gaps(self, student_skills, target_role='Data Scientist'):
        """Analyze skill gaps using ML"""
        # Map skill names to standardized indices
        skill_mapping = {
            'Python': 0, 'Python Programming': 0,
            'Machine Learning': 1, 'ML': 1,
            'SQL': 2, 'Database': 2,
            'Statistics': 3, 'Probability': 3,
            'Deep Learning': 4, 'Neural Networks': 4,
            'Cloud Computing': 5, 'AWS': 5, 'Azure': 5,
            'Communication': 6, 'Soft Skills': 6
        }
        
        # Prepare student vector (initialize with zeros)
        student_vector = np.zeros(len(skill_mapping))
        
        for skill in student_skills:
            skill_name = skill['skill_name']
            if skill_name in skill_mapping:
                idx = skill_mapping[skill_name]
                student_vector[idx] = skill['proficiency']
        
        # Scale student vector
        student_scaled = self.scaler.transform([student_vector])
        
        # Find nearest industry standard
        distances, indices = self.model.kneighbors(student_scaled)
        
        # Get industry standard vector
        industry_vectors = [
            [90, 85, 85, 90, 80, 70, 85],  # Data Scientist
            [85, 90, 80, 85, 85, 75, 80],  # ML Engineer
            [80, 75, 90, 80, 70, 65, 90],  # Data Analyst
        ]
        
        closest_standard = industry_vectors[indices[0][0]]
        
        # Calculate gaps
        skill_gaps = []
        for i, (student_val, industry_val) in enumerate(zip(student_vector, closest_standard)):
            if student_val < industry_val:
                skill_gaps.append({
                    'skill': list(skill_mapping.keys())[i],
                    'student_level': int(student_val),
                    'industry_standard': int(industry_val),
                    'gap': int(industry_val - student_val),
                    'priority': 'High' if (industry_val - student_val) > 20 else 'Medium'
                })
        
        return sorted(skill_gaps, key=lambda x: x['gap'], reverse=True)
    
    def generate_recommendations(self, skill_gaps, student_level='intermediate'):
        """Generate personalized recommendations based on skill gaps"""
        recommendations = []
        
        course_resources = {
            'Python': [
                {'name': 'Python for Data Science', 'url': 'https://coursera.org/python-data-science', 'level': 'beginner'},
                {'name': 'Advanced Python Programming', 'url': 'https://udemy.com/advanced-python', 'level': 'advanced'}
            ],
            'Machine Learning': [
                {'name': 'Machine Learning Specialization', 'url': 'https://coursera.org/ml-specialization', 'level': 'intermediate'},
                {'name': 'Hands-On ML with Scikit-Learn', 'url': 'https://amazon.com/hands-on-ml', 'level': 'intermediate'}
            ],
            'SQL': [
                {'name': 'SQL for Data Analysis', 'url': 'https://datacamp.com/sql-data-analysis', 'level': 'beginner'},
                {'name': 'Advanced SQL Queries', 'url': 'https://udemy.com/advanced-sql', 'level': 'advanced'}
            ]
        }
        
        for gap in skill_gaps[:3]:  # Top 3 gaps
            skill = gap['skill']
            if skill in course_resources:
                # Find appropriate course based on student level
                for course in course_resources[skill]:
                    if course['level'] == student_level:
                        recommendations.append({
                            'type': 'course_recommendation',
                            'skill': skill,
                            'gap': gap['gap'],
                            'recommendation': f"Take '{course['name']}' to improve {skill}",
                            'resource_url': course['url'],
                            'priority': gap['priority']
                        })
                        break
        
        # Add generic recommendations if needed
        if len(recommendations) < 3:
            recommendations.append({
                'type': 'general_recommendation',
                'recommendation': 'Practice mock interviews focusing on your weak areas',
                'priority': 'Medium'
            })
        
        return recommendations
