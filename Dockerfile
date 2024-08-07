FROM python:3.12


# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar todo el código fuente del proyecto
COPY . .

# Instalar las dependencias del proyecto
RUN pip install -r requirements_linux.txt

# Ejecutar el servidor web Streamlit
CMD ["streamlit", "run", "1_🏠_Inicio.py", "--server.port", "5555"]