document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario-producto');
    if (!formulario) return;

    let mensajeDiv = document.getElementById('mensaje');
    if (!mensajeDiv) {
        mensajeDiv = document.createElement('div');
        mensajeDiv.id = 'mensaje';
        mensajeDiv.className = 'alert d-none';
        formulario.parentNode.insertBefore(mensajeDiv, formulario.nextSibling);
    }

    formulario.addEventListener('submit', function(e) {
        e.preventDefault();
        const codigo_producto = formulario.querySelector('input[name="codigo_producto"]').value;
        const nombre = formulario.querySelector('input[name="nombre"]').value.trim();
        const descripcion = formulario.querySelector('textarea[name="descripcion"]').value.trim();
        const codigo_fabricante = formulario.querySelector('input[name="codigo_fabricante"]').value.trim();
        const marca = parseInt(formulario.querySelector('select[name="marca"]').value);
        const categoria = parseInt(formulario.querySelector('select[name="categoria"]').value);
        const stock = parseInt(formulario.querySelector('input[name="stock"]').value);
        const activo = formulario.querySelector('input[name="activo"]').checked;
        const precio = parseFloat(formulario.querySelector('input[name="precio"]').value);

        if (!nombre || !precio || !marca || !categoria || !codigo_fabricante) {
            mostrarMensaje('Por favor complete todos los campos obligatorios', 'danger', mensajeDiv);
            return;
        }

        const formData = {
            codigo_producto,
            nombre,
            descripcion,
            precio,
            stock,
            codigo_fabricante,
            marca_id: marca,
            categoria_id: categoria,
            activo
        };

        fetch('http://127.0.0.1:8000/api/productos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
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
            if (error.detail) {
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
