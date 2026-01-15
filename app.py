from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hackathon-secret-2024')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placementpro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ================== DATABASE MODELS ==================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role
        }

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    university = db.Column(db.String(200))
    batch = db.Column(db.String(20))
    cgpa = db.Column(db.Float)
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    target_role = db.Column(db.String(100), default='Data Scientist')
    
    user = db.relationship('User', backref='student_profile', uselist=False)
    
    def to_dict(self):
        return {
            'university': self.university,
            'batch': self.batch,
            'cgpa': self.cgpa,
            'department': self.department,
            'phone': self.phone,
            'target_role': self.target_role
        }

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'proficiency': self.proficiency,
            'category': self.category
        }

# ================== CREATE DATABASE TABLES ==================

def create_database():
    """Create all database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
            print(f"📁 Database file: {os.path.abspath('placementpro.db')}")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Tables created: {tables}")
            
        except Exception as e:
            print(f"❌ Error creating database: {str(e)}")
            import traceback
            traceback.print_exc()

# ================== ROUTES ==================

@app.route('/')
def home():
    return jsonify({
        "message": "🚀 PlacementPro AI API is running!",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "register_student": "/api/student/register (POST)",
            "login_student": "/api/student/login (POST)",
            "health": "/api/health (GET)"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "PlacementPro AI Backend",
        "database": "SQLite",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/student/register', methods=['POST'])
def student_register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user = User(
            email=data['email'],
            full_name=data['full_name'],
            role='student'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create student profile
        profile = StudentProfile(
            user_id=user.id,
            university=data.get('university', ''),
            batch=data.get('batch', ''),
            department=data.get('department', ''),
            target_role=data.get('target_role', 'Data Scientist')
        )
        db.session.add(profile)
        db.session.commit()
        
        return jsonify({
            'message': 'Student registered successfully!',
            'user': user.to_dict(),
            'profile': profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/login', methods=['POST'])
def student_login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email'], role='student').first()
        
        if not user:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check password
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid password'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Login successful!',
            'user': user.to_dict(),
            'token': 'jwt-token-placeholder'  # You can add JWT later
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/skills', methods=['POST'])
def add_skills():
    try:
        data = request.get_json()
        
        if 'user_id' not in data or 'skills' not in data:
            return jsonify({'error': 'user_id and skills required'}), 400
        
        # Add skills
        for skill_data in data['skills']:
            skill = Skill(
                user_id=data['user_id'],
                skill_name=skill_data['skill_name'],
                proficiency=skill_data['proficiency'],
                category=skill_data.get('category', 'technical')
            )
            db.session.add(skill)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Skills added successfully!',
            'count': len(data['skills'])
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/<int:user_id>/skills', methods=['GET'])
def get_skills(user_id):
    try:
        skills = Skill.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'skills': [skill.to_dict() for skill in skills],
            'count': len(skills)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================== RUN APPLICATION ==================

if __name__ == '__main__':
    print("🚀 Starting PlacementPro AI Backend...")
    
    # Create database tables
    create_database()
    
    # Run the app
    print("🌐 Server starting at: http://localhost:5000")
    print("📚 API Documentation at: http://localhost:5000/")
    
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000,
        use_reloader=False  # Disable reloader for database stability
    )
