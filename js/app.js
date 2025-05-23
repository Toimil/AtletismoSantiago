$(document).ready(function () {
    //HERO SLIDER
    $('#hero-slider').owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        items: 1,
        dots: false,
        autoplay: true,
        autoplayTimeout: 4000,
        smartSpeed: 1000,
        navText: ['<', '>'],
        responsive: {
            0: {
                responsiveClass: true,
                center: true,
                items: 1,
                nav: false,
                dots: true
            },
            768: {
                responsiveClass: true,
                items: 1,
                nav: true,
                dots: false,
                center: true
            },
            992: {
                items: 1,
                nav: true,
                dots: false,
                center: true
            }
        }
    })
    //Projcet-slider
    $('#project-slider').owlCarousel({
        loop: true,
        margin: 0,
        nav: false,
        dots: true,
        smartSpeed: 1000,
        autoplay: true,
        autoplayTimeout: 4000,
        margin: 24,
        responsive: {
            0: {
                items: 1,
                margin: 0,
            },
            768: {
                items: 2
            },
            1140: {
                items: 2,
                center: true
            }


        }
    })

    $('.owl-carousel').owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        dots: true,
        items: 1,
        autoplay: true,
        autoplayTimeout: 4000,
        smartSpeed: 2000,
        responsive: {
            0: {
                dots: false,
            },
            768: {
                dots: true,
            },
            1140: {

            }
        }
    })
})


function sendEmail() {
    // Obtener los valores de los campos
    var email = document.getElementById('email').value;
    var subject = document.getElementById('subject').value;
    var message = document.getElementById('message').value;

    // Construir el enlace de correo electrónico
    var mailtoLink = 'mailto:atletismosantiago@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(message);

    // Redirigir al usuario al enlace de correo electrónico
    window.location.href = mailtoLink;
}


window.onload = function () {

    const owlDotButtons = document.querySelectorAll('.owl-dots button');

    owlDotButtons.forEach(function (button, index) {
        const buttonLabel = 'Slide ' + (index + 1);
        button.setAttribute('aria-label', buttonLabel);
    });
};


function handleWindowResize() {

    if ((screen.width < 1000 || window.innerWidth < 1000) && (screen.width > 500 || window.innerWidth > 500)) {
        document.getElementsByClassName('navbar-brand')[0].style.maxWidth = '25%';
    }
    else{
        document.getElementsByClassName('navbar-brand')[0].style.maxWidth = '40%';
    }
}
// Verificar el estado inicial del dispositivo y aplicar los cambios necesarios
handleWindowResize();

// Escuchar el evento de cambio de tamaño de la ventana
window.addEventListener('resize', handleWindowResize);
window.addEventListener('load', handleWindowResize);




