// index.js

document.addEventListener('DOMContentLoaded', function() {
    // Funciones auxiliares
    function cerrarMenuUsuario(e) {
        if (!userDropdown.contains(e.target)) {
            userMenu.classList.remove('active');
        }
    }

    function funcionEjecutar(side) {
        let parentTarget = document.getElementById('slider');
        let elements = parentTarget.getElementsByTagName('li');
        let curElement, siguienteElement;

        if (elements.length === 0) {
            console.log("No hay elementos en el slider");
            return;  // Salir de la función si no hay elementos
        }

        for (let i = 0; i < elements.length; i++) {
            if (elements[i].style.opacity == 1) {
                curElement = i;
                break;
            }
        }

        if (curElement === undefined) {
            curElement = 0;  // Si no se encontró un elemento activo, comenzar desde el primero
        }

        if (side == 'anterior' || side == 'siguiente') {
            siguienteElement = (side == "anterior") 
                ? (curElement == 0) ? elements.length - 1 : curElement - 1
                : (curElement == elements.length - 1) ? 0 : curElement + 1;
        } else {
            siguienteElement = side;
            side = (curElement > siguienteElement) ? 'anterior' : 'siguiente';
        }

        // PUNTOS INFERIORES
        let elementSelList = document.getElementsByClassName("listslider");
        if (elementSelList.length > 0) {
            let elementSel = elementSelList[0].getElementsByTagName("a");
            if (elementSel.length > curElement) {
                elementSel[curElement].classList.remove("item-select-slid");
            }
            if (elementSel.length > siguienteElement) {
                elementSel[siguienteElement].classList.add("item-select-slid");
            }
        }

        elements[curElement].style.opacity = 0;
        elements[curElement].style.zIndex = 0;
        elements[siguienteElement].style.opacity = 1;
        elements[siguienteElement].style.zIndex = 1;
    }

    // Menú desplegable para dispositivos móviles
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const navMenu = document.querySelector('nav ul');

    if (mobileMenuButton && navMenu) {
        mobileMenuButton.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }

    // Animación suave al hacer scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Lazy loading para imágenes
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.dataset.src;
                    image.classList.remove('lazy');
                    imageObserver.unobserve(image);
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Toggle para el menú de usuario
    const userDropdown = document.querySelector('.user-dropdown');
    const userMenu = userDropdown.querySelector('.user-menu');
    const userIcon = userDropdown.querySelector('.icon-btn');

    userIcon.addEventListener('click', function(e) {
        e.preventDefault();
        userMenu.classList.toggle('active');
    });

    // Cerrar el menú si se hace clic fuera de él
    document.addEventListener('click', cerrarMenuUsuario);

    // Configuración del slider
    if (document.querySelector('#container-slider')) {
        setInterval(() => funcionEjecutar("siguiente"), 5000);
    }

    // Configuración de la lista del slider y carga de imágenes
    if (document.querySelector('.listslider')) {
        let links = document.querySelectorAll(".listslider li a");
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                let item = this.getAttribute('itlist');
                let arrItem = item.split("_");
                funcionEjecutar(arrItem[1]);
            });
        });

        // Cargar imágenes del carrusel
        let sliderItems = document.querySelectorAll("#slider li");
        sliderItems.forEach(function(item) {
            let imgUrl = item.getAttribute('data-background');
            if (imgUrl) {
                item.style.backgroundImage = `url('${imgUrl}')`;
            }
        });
    }

    const header = document.querySelector('.header');
    const scrollThreshold = 100; // Ajusta este valor según necesites

    function updateHeaderStyle() {
        if (window.scrollY > scrollThreshold) {
            header.classList.remove('header-transparent');
            header.classList.add('header-solid');
        } else {
            header.classList.add('header-transparent');
            header.classList.remove('header-solid');
        }
    }

    // Aplicar estilo inicial
    updateHeaderStyle();

    // Actualizar en scroll
    window.addEventListener('scroll', updateHeaderStyle);

    function inicializarCarrusel() {
        let slider = document.getElementById('slider');
        if (slider && slider.children.length > 0) {
            // Oculta todos los elementos
            for (let i = 0; i < slider.children.length; i++) {
                slider.children[i].style.opacity = 0;
                slider.children[i].style.zIndex = 0;
            }
            // Muestra el primer elemento
            slider.children[0].style.opacity = 1;
            slider.children[0].style.zIndex = 1;

            let listslider = document.querySelector('.listslider');
            if (listslider && listslider.children.length > 0) {
                listslider.children[0].querySelector('a').classList.add('item-select-slid');
            }

            // Inicia el carrusel automático
            setInterval(() => funcionEjecutar("siguiente"), 5000);
        }
    }

    // Llama a la función de inicialización
    inicializarCarrusel();
});