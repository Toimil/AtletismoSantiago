var tooltip_en_pantalla = false;

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var eventos = null;

    // Fetch events from the JSON file
    fetch('https://toimil.github.io/AtletismoSantiago/data/calendario_fga.json')
        .then(response => response.json())
        .then(data => {
            eventos = data;

            // Create the FullCalendar instance after fetching the data
            var calendar = new FullCalendar.Calendar(calendarEl, {
                height: 'auto',
                defaultView: 'dayGridMonth',
                locale: 'es',
                eventLimit: true,
                dayMaxEvents: 3,
                views: {
                    week: {
                        dayMaxEvents: 15
                    }
                },

                buttonText: {
                    today: 'Hoy',
                    month: 'Mes',
                    week: 'Semana',
                    day: 'Día',
                    list: 'Lista'
                },
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,listMonth'
                },

                events: eventos,
                eventClick: function (info) {
                    info.jsEvent.preventDefault();

                    // Cerrar tooltip existente si está en pantalla
                    if (tooltip_en_pantalla) {
                        $('.tooltip.bs-tooltip-auto.fade.show').remove();
                        tooltip_en_pantalla = false;
                    }

                    $(info.el).tooltip({
                        title: function () {
                            var tooltipContent = '<strong>' + info.event.title + '</strong>';

                            if (info.event.extendedProps.place) {
                                tooltipContent += '<br>Lugar: ' + info.event.extendedProps.place;
                            }

                            if (info.event.url) {
                                tooltipContent += '<br><a href="' + info.event.url + '" target="_blank">Más información</a>';
                            }

                            return tooltipContent;
                        },
                        placement: 'top',
                        trigger: 'manual',  // Desactivar el cierre automático
                        container: 'body',
                        html: true,
                        template: '<div id="tooltip_abierto" style="display: block !important" class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
                    });

                    $(info.el).tooltip('show');
                    tooltip_en_pantalla = true;
                },

                eventMouseEnter: function (info) {
                    $(info.el).tooltip({
                        title: function () {
                            var tooltipContent = '<strong>' + info.event.title + '</strong>';

                            if (info.event.extendedProps.place) {
                                tooltipContent += '<br>Lugar: ' + info.event.extendedProps.place;
                            }

                            if (info.event.url) {
                                tooltipContent += '<br><a href="' + info.event.url + '" target="_blank">Más información</a>';
                            }

                            return tooltipContent;
                        },
                        placement: 'top',
                        trigger: 'manual',  // Desactivar el cierre automático
                        container: 'body',
                        html: true,
                        template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'

                    });

                    $(info.el).tooltip('show');


                    // Evento para ocultar el tooltip cuando el mouse sale del evento
                    $(info.el).on('mouseleave', function () {
                        setTimeout(function () {
                            if (!$('.tooltip:hover').length) {
                                $(info.el).tooltip('hide');
                            }
                        }, 100);
                    });

                    // Evento para mantener el tooltip visible cuando el mouse está sobre él
                    $('.tooltip').on('mouseleave', function () {
                        $(info.el).tooltip('hide');
                    });
                },
            });

            // Render the calendar
            calendar.render();

           

        })
        .catch(error => {
            console.error('Error fetching events:', error);
        });
});


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



 // URL del JSON de datos
 var url = 'https://ruta-de-tu-json.com/archivo.json';

 // Función para cargar los datos en la tabla
 function cargarDatosEnTabla(datos) {
     var tabla = document.getElementById('tabla-marcas').getElementsByTagName('tbody')[0];

     for (var tipoPrueba in datos) {
         for (var nombrePrueba in datos[tipoPrueba]) {
             for (var genero in datos[tipoPrueba][nombrePrueba]) {
                 var marcaData = datos[tipoPrueba][nombrePrueba][genero]["H"];
                 var mejorMarca = marcaData["Mejor Marca"];
                 var atleta = marcaData["Atleta"];
                 var lugar = marcaData["Lugar"];
                 var fecha = marcaData["Fecha"];

                 var fila = tabla.insertRow();
                 var celdaTipoPrueba = fila.insertCell(0);
                 var celdaNombrePrueba = fila.insertCell(1);
                 var celdaGenero = fila.insertCell(2);
                 var celdaMejorMarca = fila.insertCell(3);
                 var celdaAtleta = fila.insertCell(4);
                 var celdaLugar = fila.insertCell(5);
                 var celdaFecha = fila.insertCell(6);

                 celdaTipoPrueba.innerHTML = tipoPrueba;
                 celdaNombrePrueba.innerHTML = nombrePrueba;
                 celdaGenero.innerHTML = genero;
                 celdaMejorMarca.innerHTML = mejorMarca;
                 celdaAtleta.innerHTML = atleta;
                 celdaLugar.innerHTML = lugar;
                 celdaFecha.innerHTML = fecha;
             }
         }
     }
 }

 // Cargar datos desde la URL
 fetch(url)
     .then(response => response.json())
     .then(data => cargarDatosEnTabla(data))
     .catch(error => console.error('Error al cargar los datos:', error));
