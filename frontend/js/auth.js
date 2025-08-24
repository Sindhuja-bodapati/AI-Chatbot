document.addEventListener('DOMContentLoaded', function() {
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    
    // Switch between login and signup tabs
    loginTab.addEventListener('click', function() {
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
        loginForm.classList.add('active');
        signupForm.classList.remove('active');
    });
    
    signupTab.addEventListener('click', function() {
        signupTab.classList.add('active');
        loginTab.classList.remove('active');
        signupForm.classList.add('active');
        loginForm.classList.remove('active');
    });
    
    // Handle login form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Store token and redirect to chat
                localStorage.setItem('token', data.token);
                window.location.href = 'chat.html';
            } else {
                alert(data.message || 'Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during login');
        }
    });
    
    // Handle signup form submission
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        
        try {
            const response = await fetch('/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                alert('Account created successfully! Please login.');
                loginTab.click();
            } else {
                alert(data.message || 'Signup failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during signup');
        }
    });
    
    // Check if user is already logged in
    if (localStorage.getItem('token')) {
        window.location.href = 'chat.html';
    }
});