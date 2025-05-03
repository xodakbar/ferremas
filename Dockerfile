FROM python:3.11-slim

# Evita prompts interactivos al instalar
ENV DEBIAN_FRONTEND=noninteractive

# Instala paquetes necesarios del sistema para compilar mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    zlib1g-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el proyecto
COPY . /app/

# Actualiza pip y luego instala requerimientos
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará Django
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
