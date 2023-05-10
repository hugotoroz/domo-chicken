var nombre = document.getElementById("nombre");
var contra1 = document.getElementById("clave");
var contra2 = document.getElementById("clave2");
var comuna = document.getElementById("comuna");
var email = document.getElementById("email");



const form = document.getElementById("form");
var mensaje = document.getElementById("warnings");

form.addEventListener("submit", function(event){
    let mensajesMostrar = "";
    let entrar = false;
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/
    mensaje.innerHTML = "";

    if (!regexEmail.test(email.value)) {
        mensajesMostrar += 'El correo electrónico ingresado no es válido. <br>'
        e.preventDefault();
    }
    if (comuna.value == 0){
        mensajesMostrar += 'Seleccione una Comuna. <br>'
        e.preventDefault();
      }

    if (contra1.value.length < 4 || contra1.value.length > 16) {
        mensajesMostrar += 'La contraseña no tiene el largo necesario. <br>';
        e.preventDefault();
    }
    if (contra1.value != contra2.value) {
        mensajesMostrar += 'Las contraseña no coinciden <br>';
        e.preventDefault();

    }
    if (entrar) {
        mensaje.innerHTML = mensajesMostrar;
        e.preventDefault();
    } else {
        mensaje.innerHTML = "Enviado";
    }
})