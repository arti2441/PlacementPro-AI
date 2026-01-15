<!-- Add this JavaScript -->
<script>
document.getElementById('studentRegisterForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        email: document.getElementById('email').value,
        full_name: document.getElementById('firstName').value + ' ' + document.getElementById('lastName').value,
        password: document.getElementById('password').value,
        university: document.getElementById('college').value,
        batch: document.getElementById('batch').value,
        department: document.getElementById('course').value,
        phone: ''  // Add phone field if needed
    };
    
    try {
        const response = await fetch('http://localhost:5000/api/student/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token and user data
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            alert('Registration successful! Redirecting to dashboard...');
            window.location.href = 'student_dashboard.html';
        } else {
            alert('Registration failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please check backend server.');
    }
});
</script>
