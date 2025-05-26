document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        password: formData.get("password"),
        rol: "cliente"  // asigna rol automático
    };

    fetch("http://127.0.0.1:8000/api/usuarios/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {throw err;});
        }
        return response.json();
    })
    .then(data => {
        alert("Usuario registrado con éxito");
        console.log(data);
        // Aquí podrías redirigir a login o home
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error al registrar usuario: " + JSON.stringify(error));
    });
});
