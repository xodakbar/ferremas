// static/js/carrito.js

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

const csrftoken = getCookie('csrftoken');

function agregarAlCarrito(productoId) {
  fetch("/agregar/", {  // O la URL que tengas configurada
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      producto_id: productoId,
      cantidad: 1
    }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert("Error: " + data.error);
    } else {
      alert("Producto agregado al carrito!");
    }
  })
  .catch(error => {
    alert("Error al agregar el producto: " + error);
  });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-toggle-dolar').forEach(button => {
      button.addEventListener('click', () => {
        const precioDolares = button.previousElementSibling;
        if (!precioDolares) return;
        if (precioDolares.style.display === 'none' || precioDolares.style.display === '') {
          precioDolares.style.display = 'block';
          button.textContent = 'Ocultar precio en USD';
        } else {
          precioDolares.style.display = 'none';
          button.textContent = 'Mostrar precio en USD';
        }
      });
    });
  });