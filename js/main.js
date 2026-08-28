document.addEventListener('DOMContentLoaded', () => {
    // --- Mobile Menu Toggle ---
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileBtn && navMenu) {
        const navbar = document.querySelector('.navbar');
        mobileBtn.addEventListener('click', () => {
            navMenu.classList.toggle('is-open');
            if(navbar) navbar.classList.toggle('menu-open');
            const icon = mobileBtn.querySelector('i');
            if (navMenu.classList.contains('is-open')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Relocate Login Button on Mobile
        const relocateLoginBtn = () => {
            const loginBtn = document.querySelector('.nav-actions .btn-primary, .nav-menu .btn-primary.mobile-login');
            if (!loginBtn) return;

            if (window.innerWidth <= 768) {
                if (!loginBtn.classList.contains('mobile-login')) {
                    loginBtn.classList.add('mobile-login');
                    loginBtn.style.marginTop = '24px';
                    navMenu.appendChild(loginBtn);
                }
            } else {
                if (loginBtn.classList.contains('mobile-login')) {
                    loginBtn.classList.remove('mobile-login');
                    loginBtn.style.marginTop = '0';
                    const navActions = document.querySelector('.nav-actions');
                    if (navActions) navActions.insertBefore(loginBtn, mobileBtn);
                }
            }
        };

        window.addEventListener('resize', relocateLoginBtn);
        relocateLoginBtn();
    }

    // --- Sticky Navbar ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // --- Active Menu Indicator ---
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });

    // --- Basic GSAP Setup (if GSAP is loaded) ---
    if (typeof gsap !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
        
        // Navbar entrance animation
        gsap.from('.navbar', {
            y: -100,
            opacity: 0,
            duration: 1,
            ease: "power3.out"
        });
    }
});
