document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.querySelector('#id_email');
    const form = document.querySelector('#signup-form');
    
    form.addEventListener('submit', function(event) {
        const email = emailInput.value;
        if (!email.endsWith('@gmail.com')) {
            event.preventDefault();
            alert('Only @gmail.com email addresses are accepted.');
        }
    });
});