from datetime import datetime
from flask_bcrypt import Bcrypt

# Initialize bcrypt
bcrypt = Bcrypt()

# Import db from app
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, tpo, faculty
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
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
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
    
    user = db.relationship('User', backref='student_profile')
    
    def to_dict(self):
        return {
            'university': self.university,
            'batch': self.batch,
            'cgpa': self.cgpa,
            'department': self.department,
            'phone': self.phone,
            'target_role': self.target_role
        }

class TPOProfile(db.Model):
    __tablename__ = 'tpo_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    college = db.Column(db.String(200))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(100))
    
    user = db.relationship('User', backref='tpo_profile')
    
    def to_dict(self):
        return {
            'college': self.college,
            'department': self.department,
            'phone': self.phone,
            'position': self.position
        }

class FacultyProfile(db.Model):
    __tablename__ = 'faculty_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    college = db.Column(db.String(200))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    designation = db.Column(db.String(100))
    expertise = db.Column(db.String(200))
    
    user = db.relationship('User', backref='faculty_profile')
    
    def to_dict(self):
        return {
            'college': self.college,
            'department': self.department,
            'phone': self.phone,
            'designation': self.designation,
            'expertise': self.expertise
        }
