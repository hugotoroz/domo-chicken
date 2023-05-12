var nombre = document.getElementById("nombre");
var direccion = document.getElementById("direccion");
var celular = document.getElementById("celular");
var apellido = document.getElementById("apellido");
var contra1 = document.getElementById("clave");
var contra2 = document.getElementById("clave2");
var comuna = document.getElementById("comuna");
var email = document.getElementById("email");
var mensajes = document.getElementById("mensajes1");

const form = document.getElementById("form");
var mensajes = document.getElementById("mensajes");

form.addEventListener("submit", e => {
    e.preventDefault();
    let mensajesMostrar = "";
    let entrar = false;
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/
    let validar_no_numerico = /^[a-zA-Z]$/
    let validar_numerico = /^[0-9]$/
    let validar_direccion = /^[a-zA-Z0-9\#\-]/
    mensajes.innerHTML = "";

    if (!regexEmail.test(email.value)) {
        mensajesMostrar += 'El correo electrónico ingresado no es válido. <br>'
        entrar = true;
    }
    if (contra1.value.length < 4 || contra1.value.length > 16) {
        mensajesMostrar += 'La contraseña no tiene el largo necesario. <br>';
        entrar = true;
    }
    if (contra1.value != contra2.value) {
        mensajesMostrar += 'Las contraseña no coinciden <br>';
        entrar = true;

    }
    if (nombre.value == '') {
        mensajesMostrar += 'Por favor, escriba un nombre. <br>'
        entrar = true;
    }
    else if (!validar_no_numerico.test(nombre.value)) {
        mensajesMostrar += 'Escriba un nombre válido. <br>'
        entrar = true;
    }
    if (apellido.value == '') {
        mensajesMostrar += 'Por favor, escriba un apellido. <br>'
        entrar = true;
    }
    else if (!validar_no_numerico.test(apellido.value)) {
        mensajesMostrar += 'Escriba un apellido válido. <br>'
        entrar = true;
    }
    if (celular.value == '') {
        mensajesMostrar += 'Por favor, ingrese su celular. <br>'
        entrar = true;
    }
    else if (celular.value.length <= 1 || celular.value.length > 9) {
        mensajesMostrar += 'El celular debe tener como máximo 9 números. <br>'
        entrar = true;
    }
    if (comuna.value == '') {
        mensajesMostrar += 'Seleccione una Comuna. <br>'
        entrar = true;
    }
    if (direccion.value == '') {
        mensajesMostrar += 'Por favor, ingrese su dirección. <br>'
        entrar = true;
    }
    else if (!validar_direccion.test(direccion.value)) {
        mensajesMostrar += 'Escriba una dirección válida. <br>'
        entrar = true;
    }
    else if (!validar_numerico.test(celular.value)) {
        mensajesMostrar += 'Escriba un celular válido. <br>'
        entrar = true;
    }
    if (entrar) {
        mensajes.classList.remove("d-none");
        mensajes.classList.add("d-block");
        mensajes.innerHTML = mensajesMostrar;
        e.preventDefault();
    } else {
        mensajes.innerHTML = "Enviado";
    }
})