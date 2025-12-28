document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario-producto');
    const mensajeDiv = document.getElementById('mensaje');

    formulario.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(formulario); // Esto incluye todos los inputs y archivos

        fetch('http://127.0.0.1:8000/api/productos/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // CSRF para Django
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            mostrarMensaje('¡Producto agregado correctamente!', 'success', mensajeDiv);
            formulario.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            let errorMsg = 'Error al agregar el producto';
            if (error.imagen) {
                errorMsg = error.imagen.join(', ');
            } else if (error.detail) {
                errorMsg = error.detail;
            } else if (typeof error === 'object') {
                errorMsg = Object.values(error).flat().join(', ');
            }
            mostrarMensaje(errorMsg, 'danger', mensajeDiv);
        });
    });

    function mostrarMensaje(texto, tipo, elemento) {
        elemento.textContent = texto;
        elemento.className = `alert alert-${tipo} d-block`;
        setTimeout(() => {
            elemento.className = 'alert d-none';
        }, 5000);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
