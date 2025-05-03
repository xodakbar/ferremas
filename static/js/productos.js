document.addEventListener('DOMContentLoaded', () => {
    const lista = document.getElementById('lista-productos');
    const form = document.getElementById('formulario-producto');
  
    function cargarProductos() {
      fetch('/api/productos/')
        .then(res => res.json())
        .then(data => {
          lista.innerHTML = '';
          data.forEach(p => {
            const li = document.createElement('li');
            li.textContent = `${p.nombre} - $${p.precio}`;
            lista.appendChild(li);
          });
        });
    }
  
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const datos = {
        nombre: form.nombre.value,
        descripcion: form.descripcion.value,
        precio: form.precio.value,
        stock: form.stock.value,
        categoria: form.categoria.value
      };
  
      fetch('/api/productos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      })
      .then(res => {
        if (res.ok) {
          form.reset();
          cargarProductos();
        } else {
          alert("Error al crear el producto");
        }
      });
    });
  
    cargarProductos();
  });
  