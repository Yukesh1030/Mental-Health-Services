// Global Animation Controller
const Animations = {
    initFAQ: () => {
        if (typeof gsap === 'undefined') return;
        const faqItems = document.querySelectorAll('.faq-item');
        faqItems.forEach(item => {
            const head = item.querySelector('.faq-head');
            const body = item.querySelector('.faq-body');
            const icon = item.querySelector('.faq-icon');
            
            if (head) {
                head.addEventListener('click', () => {
                    const isOpen = item.classList.contains('open');
                    
                    // Close all others
                    faqItems.forEach(otherItem => {
                        otherItem.classList.remove('open');
                        const otherBody = otherItem.querySelector('.faq-body');
                        const otherIcon = otherItem.querySelector('.faq-icon');
                        if(otherBody) gsap.to(otherBody, { height: 0, opacity: 0, duration: 0.3 });
                        if(otherIcon) gsap.to(otherIcon, { rotation: 0, duration: 0.3 });
                    });

                    if (!isOpen) {
                        item.classList.add('open');
                        if(body) gsap.to(body, { height: 'auto', opacity: 1, duration: 0.4, ease: "power2.out" });
                        if(icon) gsap.to(icon, { rotation: 45, duration: 0.3 });
                    }
                });
            }
        });
    },
    initHomeAnimations: () => {
        if (typeof gsap === 'undefined') return;
        
        // --- Hero Timeline ---
        const heroTl = gsap.timeline();
        
        heroTl.from('.page-hero-bg', { 
                  scale: 1.1, 
                  opacity: 0, 
                  duration: 1.5, 
                  ease: "power3.out" 
              })
              .from('.hero-eyebrow', { y: 20, opacity: 0, duration: 0.8, ease: "power2.out" }, "-=1.0")
              .from('.hero-text', { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, "-=0.6")
              .from('.page-hero p', { y: 20, opacity: 0, duration: 0.8, ease: "power2.out" }, "-=0.6")
              .from('.hero-cta', { y: 20, opacity: 0, duration: 0.8, ease: "power2.out" }, "-=0.6");

        // --- Section 01: A Place to Begin ---
        gsap.utils.toArray('.stagger-card').forEach((card, i) => {
            gsap.from(card, {
                scrollTrigger: {
                    trigger: '.section-01',
                    start: "top 75%",
                },
                y: 50,
                opacity: 0,
                scale: 0.95,
                duration: 0.8,
                delay: i * 0.2,
                ease: "power2.out"
            });
        });

        // --- Section 02: Areas We Support (Horizontal Scroll) ---
        const areasWrapper = document.querySelector('.areas-scroll-wrapper');
        if (areasWrapper) {
            gsap.to('.areas-scroll-content', {
                x: () => -(document.querySelector('.areas-scroll-content').scrollWidth - window.innerWidth + 80),
                ease: "none",
                scrollTrigger: {
                    trigger: '.section-02',
                    pin: true,
                    scrub: 1,
                    end: () => "+=" + document.querySelector('.areas-scroll-content').scrollWidth
                }
            });
        }

        // --- Section 03: Our Approach ---
        const approachItems = gsap.utils.toArray('.approach-item');
        approachItems.forEach((item, i) => {
            ScrollTrigger.create({
                trigger: item,
                start: "top center",
                end: "bottom center",
                toggleClass: "active-approach",
                onEnter: () => gsap.to(item, { opacity: 1 }),
                onLeave: () => gsap.to(item, { opacity: 0.4 }),
                onEnterBack: () => gsap.to(item, { opacity: 1 }),
                onLeaveBack: () => gsap.to(item, { opacity: 0.4 })
            });
        });

        // Parallax image
        gsap.to('.approach-parallax-img', {
            y: 100,
            ease: "none",
            scrollTrigger: {
                trigger: '.section-03',
                start: "top bottom",
                end: "bottom top",
                scrub: true
            }
        });

        // --- Section 04: Meet Our Therapists ---
        gsap.from('.therapist-card', {
            scrollTrigger: {
                trigger: '.section-04',
                start: "top 75%",
            },
            y: 50,
            opacity: 0,
            scale: 0.95,
            duration: 0.8,
            stagger: 0.2,
            ease: "back.out(1.2)"
        });

        // --- Section 05: How It Works (Timeline) ---
        gsap.to('.timeline-progress-line', {
            height: '100%',
            ease: "none",
            scrollTrigger: {
                trigger: '.timeline-container',
                start: "top center",
                end: "bottom center",
                scrub: true
            }
        });

        const timelineItems = gsap.utils.toArray('.timeline-item');
        timelineItems.forEach((item) => {
            gsap.from(item, {
                opacity: 0.3,
                scrollTrigger: {
                    trigger: item,
                    start: "top center",
                    end: "bottom center",
                    toggleClass: "active"
                }
            });
        });



        // --- Generic Section Text Animations ---
        const sectionTextElements = gsap.utils.toArray('.section h2, .section > .container > p, .section > .container > div > p, .section > .container > div > h2');
        
        sectionTextElements.forEach((elem) => {
            // Skip elements that are inside specific animated components to avoid conflicting animations
            if (elem.closest('.therapist-card') || 
                elem.closest('.stagger-card') || 
                elem.closest('.approach-item') || 
                elem.closest('.timeline-item') ||
                elem.closest('.area-card') ||
                elem.closest('.resource-card') ||
                elem.closest('.faq-item') ||
                elem.closest('.final-cta-content') ||
                elem.closest('.hero-text') ||
                elem.closest('.page-hero')) {
                return;
            }
            
            gsap.from(elem, {
                scrollTrigger: {
                    trigger: elem,
                    start: "top 85%",
                },
                y: 30,
                opacity: 0,
                duration: 0.8,
                ease: "power2.out"
            });
        });

        // --- Section 10: Final CTA ---
        gsap.from('.final-cta-bg', {
            scale: 1.1,
            scrollTrigger: {
                trigger: '.section-10',
                start: "top bottom",
                end: "bottom top",
                scrub: true
            }
        });

        gsap.from('.final-cta-content > *', {
            y: 40,
            opacity: 0,
            stagger: 0.2,
            duration: 1,
            ease: "power3.out",
            scrollTrigger: {
                trigger: '.section-10',
                start: "top 70%"
            }
        });
    }
};

// Auto-init based on page
document.addEventListener('DOMContentLoaded', () => {
    Animations.initFAQ();
    if (document.querySelector('.home-page-marker')) {
        Animations.initHomeAnimations();
    }
});
