document.addEventListener('DOMContentLoaded', () => {
    console.log('La Metta Hood landing page loaded.');

    // Example of adding a simple interaction:
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default anchor behavior
            alert('Explore our projects!');
            // In a real application, you might navigate the user or trigger another action.
        });
    }

    // Smooth scrolling for internal links (optional)
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});