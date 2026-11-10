document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');

    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Account successfully created! Welcome to the Aura Grand Privilege Circle.');
            window.location.href = 'index.html';
        });
    }
});