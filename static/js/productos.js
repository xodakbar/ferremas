document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario-producto');
    
    // Verifica si el formulario existe en la página
    if (!formulario) return;

    // Crea el elemento de mensaje dinámicamente si no existe
    let mensajeDiv = document.getElementById('mensaje');
    if (!mensajeDiv) {
        mensajeDiv = document.createElement('div');
        mensajeDiv.id = 'mensaje';
        mensajeDiv.className = 'alert d-none';
        formulario.parentNode.insertBefore(mensajeDiv, formulario.nextSibling);
    }

    formulario.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const formData = {
            nombre: formulario.nombre.value,
            descripcion: formulario.descripcion.value,
            precio: parseFloat(formulario.precio.value),
            stock: parseInt(formulario.stock.value),
            categoria: formulario.categoria.value,
            activo: true  // Asegurando que el producto se cree como activo
        };

        // Validación básica
        if (!formData.nombre || !formData.precio || !formData.categoria) {
            mostrarMensaje('Por favor complete los campos requeridos', 'danger', mensajeDiv);
            return;
        }

        // Enviar datos a la API
        fetch('/api/productos/', {
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
                errorMsg = Object.values(error).join(', ');
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

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.csrfmiddlewaretoken.value,
                'Accept': 'application/json',
            },
            body: new FormData(this)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Stock actualizado');
            }
        });
    });
});