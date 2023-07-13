function checkPassword(form) {
    const password = form.password.value;
    const confirmPassword = form.confirm_password.value;

    if (confirmPassword) {
        if (password != confirmPassword) {
            $('#2').addClass('d-block');
            $('#2').removeClass('d-none');
            $('#confirm_password').addClass('is-valid');


            return false;
        } else {
            $('#2').addClass('d-none');
            $('#2').removeClass('d-block');
            $('#2').addClass('is-valid');
            return true;
        }
    } else { }

}

(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()


            }

            form.classList.add('was-validated')
        }, false)
    })
})()