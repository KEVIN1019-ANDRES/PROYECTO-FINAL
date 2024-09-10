let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-item');
const totalSlides = slides.length;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.display = (i === index) ? 'block' : 'none';
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

setInterval(nextSlide, 2400); // Change image every 3 seconds

// Initialize the carousel by showing the first slide
showSlide(currentSlide);

//---------------------

document.addEventListener('DOMContentLoaded', function () {
    const track = document.querySelector('.theme_brands');
    let isMouseDown = false;
    let startX;
    let scrollLeft;

    track.addEventListener('mousedown', (e) => {
        isMouseDown = true;
        startX = e.pageX - track.offsetLeft;
        scrollLeft = track.scrollLeft;
    });

    track.addEventListener('mouseleave', () => {
        isMouseDown = false;
    });

    track.addEventListener('mouseup', () => {
        isMouseDown = false;
    });

    track.addEventListener('mousemove', (e) => {
        if (!isMouseDown) return;
        e.preventDefault();
        const x = e.pageX - track.offsetLeft;
        const walk = (x - startX) * 2; // Ajusta la velocidad del desplazamiento
        track.scrollLeft = scrollLeft - walk;

        if (track.scrollLeft === 0) {
            track.scrollLeft = track.scrollWidth / 2;
        } else if (track.scrollLeft >= track.scrollWidth / 2) {
            track.scrollLeft = track.scrollWidth / 4;
        }
    });
});
