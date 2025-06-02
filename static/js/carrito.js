// Obtener cookie CSRF para Django
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

function mostrarMensajeEnProducto(contenedor, texto, duracion = 3000) {
  contenedor.textContent = texto;
  setTimeout(() => {
    contenedor.textContent = "";
  }, duracion);
}

function agregarAlCarrito(productoId, button) {
  const productoCard = button.closest('.producto-card');
  const mensajeContenedor = productoCard.querySelector('.mensaje-carrito');

  const cantidadInput = productoCard.querySelector('.cantidad-input');
  const cantidad = cantidadInput ? parseInt(cantidadInput.value) : 1;

  if (isNaN(cantidad) || cantidad < 1) {
    mostrarMensajeEnProducto(mensajeContenedor, "Ingrese una cantidad válida");
    return;
  }

  fetch("/agregar/", {  // Cambia por la URL correcta de tu API
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      producto_id: productoId,
      cantidad: cantidad,
    }),
    credentials: 'include'  // Para enviar cookies de sesión
  })
  .then(response => {
    if (!response.ok) {
      // Si el status no es 2xx
      return response.json().then(data => {
        throw new Error(data.error || 'Error desconocido');
      });
    }
    return response.json();
  })
  .then(data => {
    mostrarMensajeEnProducto(mensajeContenedor, "Producto agregado al carrito!");
    // Aquí puedes actualizar la UI si quieres
  })
  .catch(error => {
    mostrarMensajeEnProducto(mensajeContenedor, "Error: " + error.message);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-agregar-carrito').forEach(button => {
    button.addEventListener('click', () => {
      const productoId = button.dataset.id;
      agregarAlCarrito(productoId, button);
    });
  });
});
