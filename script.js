// ===========================
// FORM HANDLING
// ===========================

function handleSubscribe(event) {
    event.preventDefault();
    const email = event.target.querySelector('input[type="email"]').value;
    
    if (email) {
        alert(`Thank you for subscribing! We'll send updates to ${email}`);
        event.target.reset();
    }
}

function handleContact(event) {
    event.preventDefault();
    const formData = {
        name: event.target.querySelector('input[type="text"]').value,
        email: event.target.querySelector('input[type="email"]').value,
        message: event.target.querySelector('textarea').value
    };
    
    if (formData.name && formData.email && formData.message) {
        alert(`Thank you ${formData.name}! Your message has been received. We'll get back to you soon.`);
        event.target.reset();
    }
}

function handleAccountCreation(event) {
    event.preventDefault();
    
    const firstName = event.target.querySelector('#firstName').value;
    const lastName = event.target.querySelector('#lastName').value;
    const email = event.target.querySelector('#email').value;
    const password = event.target.querySelector('#password').value;
    const confirmPassword = event.target.querySelector('#confirmPassword').value;
    const terms = event.target.querySelector('#terms').checked;
    
    // Basic validation
    if (!firstName || !lastName || !email || !password) {
        alert('Please fill in all required fields.');
        return;
    }
    
    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return;
    }
    
    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }
    
    if (!terms) {
        alert('You must agree to the Terms and Conditions.');
        return;
    }
    
    // Simulate account creation
    alert(`Welcome ${firstName}! Your account has been successfully created. You can now start exploring Lens&Luxe.`);
    event.target.reset();
    window.location.href = 'index.html';
}

function handleLogin(event) {
    event.preventDefault();
    const email = event.target.querySelector('#email').value;
    const password = event.target.querySelector('#password').value;

    if (!email || !password) {
        alert('Please fill in all required fields.');
        return;
    }

    alert('Welcome back! You have successfully logged in.');
    event.target.reset();
    window.location.href = 'index.html';
}

// ===========================
// SMOOTH SCROLLING
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    // Add scroll event listener for navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.boxShadow = '0 4px 15px rgba(128, 0, 32, 0.15)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(128, 0, 32, 0.1)';
        }
    });

    // Add animation to post cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all post cards
    document.querySelectorAll('.post-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Observe gallery items
    document.querySelectorAll('.gallery-item').forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'scale(0.95)';
        item.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(item);
    });
});

// ===========================
// GALLERY LIGHTBOX (Optional Enhancement)
// ===========================

document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', function() {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
            cursor: pointer;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            width: 80%;
            height: 80%;
            max-width: 600px;
            background: ${this.style.background};
            border-radius: 8px;
            animation: zoomIn 0.3s ease;
        `;
        
        modal.appendChild(content);
        document.body.appendChild(modal);
        
        modal.addEventListener('click', function() {
            modal.remove();
        });
    });
});

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
`;
document.head.appendChild(style);

// ===========================
// SCROLL TO TOP BUTTON
// ===========================

function createScrollToTopButton() {
    const button = document.createElement('button');
    button.innerHTML = '↑';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background-color: #800020;
        color: #fffef9;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 24px;
        display: none;
        z-index: 999;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(128, 0, 32, 0.3);
    `;
    
    document.body.appendChild(button);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            button.style.display = 'flex';
            button.style.alignItems = 'center';
            button.style.justifyContent = 'center';
        } else {
            button.style.display = 'none';
        }
    });
    
    button.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    button.addEventListener('mouseenter', function() {
        this.style.backgroundColor = '#400010';
        this.style.transform = 'scale(1.1)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.backgroundColor = '#800020';
        this.style.transform = 'scale(1)';
    });
}

// Initialize scroll to top button
document.addEventListener('DOMContentLoaded', createScrollToTopButton);
