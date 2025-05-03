document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Evita que el formulario se envíe de la manera tradicional

    const formData = new FormData(this);
    const data = {
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        password: formData.get("password"),
    };

    // Hacer la solicitud a la API usando Fetch
    fetch("http://127.0.0.1:8000/usuarios/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        alert("Usuario registrado con éxito");
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Hubo un error al registrar el usuario");
    });
});
