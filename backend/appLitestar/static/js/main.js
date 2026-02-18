$(document).ready(function() {
    let table = $('#usuarios-table').DataTable();

    // 1. MANEJO DEL LOGIN
    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        const data = {
            username: $('#username').val(),
            password: $('#password').val()
        };

        $.ajax({
            url: '/auth/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                $('#user-display').text(response.nombre);
                $('#user-rol').text(response.rol.toUpperCase()); // En mayúsculas para que luzca mejor
                $('#login-container').hide();
                $('#dashboard-container').show();
                cargarDatosTabla(); // Llamamos a la API de datos
            },
            error: function() {
                $('#error-msg').show();
            }
        });
    });

    // 2. CARGAR DATOS SEGÚN ROL
    function cargarDatosTabla() {
        $.ajax({
            url: '/auth/data',
            method: 'GET',
            success: function(data) {
                table.clear();
                data.forEach(user => {
                    table.row.add([
                        user.nombre,
                        user.rol,
                        user.renta
                    ]);
                });
                table.draw();
            }
        });
    }

    $('#logout-btn').on('click', function() {
        $.ajax({
            url: '/auth/logout',
            method: 'POST',
            success: function(response) {
                // Una vez confirmada la salida en el servidor, limpiamos el cliente
                alert("Has cerrado sesión");
                window.location.href = "/auth/login-page"; // O el div que corresponda
            },
            error: function() {
                console.error("Error al cerrar sesión");
                // Forzamos recarga si algo falla
                location.reload();
            }
        });
    });
});