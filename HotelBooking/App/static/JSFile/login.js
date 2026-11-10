document.addEventListener('DOMContentLoaded', () => {
    const loginTabBtn = document.getElementById('loginTabBtn');
    const registerTabBtn = document.getElementById('registerTabBtn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const authSubtitle = document.getElementById('authSubtitle');

    // Switch to Sign In view
    loginTabBtn.addEventListener('click', () => {
        loginTabBtn.classList.add('active');
        registerTabBtn.classList.remove('active');
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
        authSubtitle.textContent = 'Access your membership profile & bookings';
    });

    // Switch to Create Account view
    registerTabBtn.addEventListener('click', () => {
        registerTabBtn.classList.add('active');
        loginTabBtn.classList.remove('active');
        registerForm.classList.add('active');
        loginForm.classList.remove('active');
        authSubtitle.textContent = 'Join the Aura Privilege Circle';
    });

    // Handle Login Submit Simulation
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Successfully signed in to Aura Grand.');
        window.location.href = 'index.html';
    });

    // Handle Register Submit Simulation
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Account successfully created! Welcome to Aura Grand.');
        window.location.href = 'index.html';
    });
});