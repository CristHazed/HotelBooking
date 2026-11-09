document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            if (navMenu.style.display === 'flex') {
                navMenu.style.display = 'none';
            } else {
                navMenu.style.display = 'flex';
                navMenu.style.flexDirection = 'column';
                navMenu.style.position = 'absolute';
                navMenu.style.top = '80px';
                navMenu.style.left = '0';
                navMenu.style.width = '100%';
                navMenu.style.background = '#FFFFFF';
                navMenu.style.padding = '1.5rem 2rem';
                navMenu.style.boxShadow = 'var(--shadow-md)';
                navMenu.style.borderBottom = '1px solid var(--border-color)';
            }
        });
    }

    // Room Category Filter Tabs
    const filterBtns = document.querySelectorAll('.filter-btn');
    const roomCards = document.querySelectorAll('.room-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            roomCards.forEach(card => {
                const categories = card.getAttribute('data-category');
                if (filter === 'all' || categories.includes(filter)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Amenities Showcase Tabs
    const amenityTabs = document.querySelectorAll('.amenity-tab');
    const amenityPanels = document.querySelectorAll('.amenity-panel');

    amenityTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            amenityTabs.forEach(t => t.classList.remove('active'));
            amenityPanels.forEach(p => p.classList.remove('active'));

            tab.classList.add('active');
            const targetId = tab.getAttribute('data-target');
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });

    // Reserve Modal Interactivity
    const reserveBtns = document.querySelectorAll('.reserve-btn');
    const reserveModal = document.getElementById('reserveModal');
    const modalClose = document.getElementById('modalClose');
    const modalRoomTitle = document.getElementById('modalRoomTitle');
    const modalRoomPrice = document.getElementById('modalRoomPrice');

    reserveBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const roomName = btn.getAttribute('data-room');
            const roomPrice = btn.getAttribute('data-price');
            
            modalRoomTitle.textContent = roomName;
            modalRoomPrice.textContent = `${roomPrice} / night`;
            reserveModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    const closeModalFunc = () => {
        reserveModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    };

    if (modalClose) {
        modalClose.addEventListener('click', closeModalFunc);
    }

    if (reserveModal) {
        reserveModal.addEventListener('click', (e) => {
            if (e.target === reserveModal) {
                closeModalFunc();
            }
        });
    }

    // Reservation Form Submit Handler
    const reservationForm = document.getElementById('reservationForm');
    if (reservationForm) {
        reservationForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Thank you! Your reservation request has been successfully submitted. Our concierge team will reach out shortly.');
            closeModalFunc();
            reservationForm.reset();
        });
    }

    // Booking Bar Search Submit
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const suitesSection = document.getElementById('suites');
            if (suitesSection) {
                suitesSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
});

// Copy Promo Code Function
function copyPromo(code, btnElement) {
    navigator.clipboard.writeText(code).then(() => {
        const originalHTML = btnElement.innerHTML;
        btnElement.innerHTML = '<i class="fa-solid fa-check"></i> Copied';
        btnElement.style.color = '#10B981';
        setTimeout(() => {
            btnElement.innerHTML = originalHTML;
            btnElement.style.color = 'inherit';
        }, 2000);
    });
}