from flask import jsonify
from flask_jwt_extended import create_access_token
from models import User, StudentProfile, TPOProfile, FacultyProfile, bcrypt
from app import db
from datetime import datetime

def register_user(data):
    """Register a new user with role-specific profile"""
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Create user
        user = User(
            email=data['email'],
            full_name=data['full_name'],
            role=data['role']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        
        # Create role-specific profile
        if data['role'] == 'student':
            profile = StudentProfile(
                user_id=user.id,
                university=data.get('university', ''),
                batch=data.get('batch', ''),
                department=data.get('department', ''),
                phone=data.get('phone', '')
            )
        elif data['role'] == 'tpo':
            profile = TPOProfile(
                user_id=user.id,
                college=data.get('college', ''),
                department=data.get('department', ''),
                phone=data.get('phone', ''),
                position=data.get('position', '')
            )
        elif data['role'] == 'faculty':
            profile = FacultyProfile(
                user_id=user.id,
                college=data.get('college', ''),
                department=data.get('department', ''),
                phone=data.get('phone', ''),
                designation=data.get('designation', ''),
                expertise=data.get('expertise', '')
            )
        else:
            return {'error': 'Invalid role'}, 400
        
        db.session.add(profile)
        db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(
            identity={'id': user.id, 'email': user.email, 'role': user.role}
        )
        
        return {
            'message': 'Registration successful',
            'user': user.to_dict(),
            'token': access_token
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

def login_user(data):
    """Login user and return JWT token"""
    try:
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid email or password'}, 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(
            identity={'id': user.id, 'email': user.email, 'role': user.role}
        )
        
        return {
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': access_token
        }, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

def get_user_profile(user_id):
    """Get user profile based on role"""
    try:
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        response = {'user': user.to_dict()}
        
        # Add role-specific profile data
        if user.role == 'student' and user.student_profile:
            response['profile'] = user.student_profile.to_dict()
        elif user.role == 'tpo' and user.tpo_profile:
            response['profile'] = user.tpo_profile.to_dict()
        elif user.role == 'faculty' and user.faculty_profile:
            response['profile'] = user.faculty_profile.to_dict()
        
        return response, 200
        
    except Exception as e:
        return {'error': str(e)}, 500
