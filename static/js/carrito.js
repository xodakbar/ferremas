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

    fetch("/agregar/", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      producto_id: productoId,
      cantidad: cantidad,
    }),
    credentials: 'include',  // Esto asegura que las cookies de sesión se envíen
  })
  .then(response => {
    console.log(response.status);  // Revisa el código de estado HTTP
    if (response.status === 302) {  // Esto es lo que ocurre cuando hay una redirección
      alert("Debes iniciar sesión primero.");
      window.location.href = "{% url 'login' %}";  // Redirige al login si no está autenticado
    }
    return response.json();
  })
  .then(data => {
    mostrarMensajeEnProducto(mensajeContenedor, "Producto agregado al carrito!");
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
