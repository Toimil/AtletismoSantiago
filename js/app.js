

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

    const instagramIframe = document.getElementById('instagram-embed-0');
    if (instagramIframe) {
        instagramIframe.title = 'Título del Iframe para Instagram'; // Reemplaza con tu propio título
    }

    const owlDotButtons = document.querySelectorAll('.owl-dots button');
    console.log("prueba:" + owlDotButtons.length);

    owlDotButtons.forEach(function(button, index) {
        console.log("pueba2" + button);
        const buttonLabel = 'Slide ' + (index + 1); // Puedes personalizar el texto según tus necesidades
        button.setAttribute('aria-label', buttonLabel);
        console.log(buttonLabel);
    });
};



