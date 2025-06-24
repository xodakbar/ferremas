document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    if (!this.checkValidity()) {
        e.stopPropagation();
        this.classList.add('was-validated');
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const data = {
        first_name: this.first_name.value,
        last_name: this.last_name.value,
        email: this.email.value,
        password: this.password.value,
        // si quieres enviar rol, ponlo aquí, sino tu serializer puede asignar default
    };

    fetch(this.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
      console.log('Status de la respuesta:', response.status);
        if (response.ok) {
            document.getElementById('successMessage').style.display = 'block';
            this.reset();
            this.classList.remove('was-validated');
            setTimeout(() => {
                window.location.href = "{% url 'login' %}";
            }, 2000);
        } else {
            return response.json().then(errData => {
            console.error('Error de backend:', errData);
            throw new Error(JSON.stringify(errData));
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error durante el registro: ' + error.message);
    });
});
