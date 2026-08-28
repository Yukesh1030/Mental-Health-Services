document.addEventListener('DOMContentLoaded', () => {
    // --- Login Form Logic ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            const loginAs = document.getElementById('loginAs'); // Dropdown: 'Admin' or 'Client'
            
            let isValid = true;
            
            // Basic Email Validation
            if (!email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                showError(email, "Please enter a valid email address.");
                isValid = false;
            } else {
                clearError(email);
            }
            
            // Basic Password Validation
            if (password.value.length < 6) {
                showError(password, "Password must be at least 6 characters.");
                isValid = false;
            } else {
                clearError(password);
            }
            
            if (isValid) {
                // Mock Authentication Routing
                if (loginAs && loginAs.value === 'Admin') {
                    window.location.href = 'admin-dashboard.html';
                } else {
                    window.location.href = 'client-dashboard.html';
                }
            }
        });
    }

    // --- Signup Form Logic ---
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const fullName = document.getElementById('fullName');
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            
            let isValid = true;
            
            if (fullName.value.trim().length < 2) {
                showError(fullName, "Please enter your full name.");
                isValid = false;
            } else {
                clearError(fullName);
            }
            
            if (!email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                showError(email, "Please enter a valid email address.");
                isValid = false;
            } else {
                clearError(email);
            }
            
            if (password.value.length < 6) {
                showError(password, "Password must be at least 6 characters.");
                isValid = false;
            } else {
                clearError(password);
            }
            
            if (isValid) {
                // Route to Login on successful signup
                window.location.href = 'Login.html';
            }
        });
    }

    // --- Contact/Booking Form Logic ---
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // For this project, any form on pages (Contact, Booking, etc) validates simply and redirects to 404
            let isValid = true;
            const requiredFields = contactForm.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    showError(field, "This field is required.");
                    isValid = false;
                } else {
                    clearError(field);
                }
            });
            
            if (isValid) {
                // As per requirements, successful form submissions redirect to 404
                window.location.href = '404.html';
            }
        });
    }

    // Helper functions
    function showError(input, message) {
        input.classList.add('is-invalid');
        let feedback = input.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            input.parentNode.insertBefore(feedback, input.nextSibling);
        }
        feedback.textContent = message;
    }
    
    function clearError(input) {
        input.classList.remove('is-invalid');
        const feedback = input.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.remove();
        }
    }
});
