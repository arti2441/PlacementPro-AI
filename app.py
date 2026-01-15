from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import jwt
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon-secret-key-2024'

# Database connection helper
def get_db():
    conn = sqlite3.connect('placementpro.db')
    conn.row_factory = sqlite3.Row  # To get dict-like rows
    return conn

# 🔐 REGISTRATION API
@app.route('/api/register/student', methods=['POST'])
def register_student():
    """Register a student - store in database"""
    data = request.json
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 1. Hash password
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 2. Insert into users table
        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', (data['email'], password_hash, data['full_name'], 'student'))
        
        user_id = cursor.lastrowid
        
        # 3. Insert into student_profiles table
        cursor.execute('''
            INSERT INTO student_profiles 
            (user_id, university, batch, department, phone, target_role)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data.get('university', ''),
            data.get('batch', ''),
            data.get('department', ''),
            data.get('phone', ''),
            data.get('target_role', 'Data Scientist')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Student registered successfully",
            "user_id": user_id
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/register/tpo', methods=['POST'])
def register_tpo():
    """Register a TPO - store in database"""
    data = request.json
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', (data['email'], password_hash, data['full_name'], 'tpo'))
        
        user_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO tpo_profiles 
            (user_id, college, department, phone, position)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            data.get('college', ''),
            data.get('department', ''),
            data.get('phone', ''),
            data.get('position', '')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "TPO registered successfully",
            "user_id": user_id
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/register/faculty', methods=['POST'])
def register_faculty():
    """Register a faculty - store in database"""
    data = request.json
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', (data['email'], password_hash, data['full_name'], 'faculty'))
        
        user_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO faculty_profiles 
            (user_id, college, department, phone, designation, expertise)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data.get('college', ''),
            data.get('department', ''),
            data.get('phone', ''),
            data.get('designation', ''),
            data.get('expertise', '')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Faculty registered successfully",
            "user_id": user_id
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔑 LOGIN API
@app.route('/api/login', methods=['POST'])
def login():
    """Login user - verify credentials"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user from database
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({"error": "Invalid password"}), 401
        
        # Create JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "full_name": user['full_name'],
                "role": user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 👤 PROFILE API
@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user's complete profile from database"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get basic user info
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        profile_data = {
            "user": {
                "id": user['id'],
                "email": user['email'],
                "full_name": user['full_name'],
                "role": user['role'],
                "created_at": user['created_at']
            }
        }
        
        # Get role-specific profile
        if user['role'] == 'student':
            cursor.execute('SELECT * FROM student_profiles WHERE user_id = ?', (user_id,))
            profile = cursor.fetchone()
            if profile:
                profile_data['profile'] = {
                    "university": profile['university'],
                    "batch": profile['batch'],
                    "cgpa": profile['cgpa'],
                    "department": profile['department'],
                    "phone": profile['phone'],
                    "target_role": profile['target_role'],
                    "skills": json.loads(profile['skills']) if profile['skills'] else []
                }
        
        elif user['role'] == 'tpo':
            cursor.execute('SELECT * FROM tpo_profiles WHERE user_id = ?', (user_id,))
            profile = cursor.fetchone()
            if profile:
                profile_data['profile'] = {
                    "college": profile['college'],
                    "department": profile['department'],
                    "phone": profile['phone'],
                    "position": profile['position']
                }
        
        elif user['role'] == 'faculty':
            cursor.execute('SELECT * FROM faculty_profiles WHERE user_id = ?', (user_id,))
            profile = cursor.fetchone()
            if profile:
                profile_data['profile'] = {
                    "college": profile['college'],
                    "department": profile['department'],
                    "phone": profile['phone'],
                    "designation": profile['designation'],
                    "expertise": profile['expertise']
                }
        
        conn.close()
        return jsonify(profile_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "database": "placementpro.db"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)