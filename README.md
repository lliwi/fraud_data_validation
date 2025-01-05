# Fraud data validation
Este es un formulario de ejemplo para la verificación de datos.
Para el DNI hace uso de una función básica que realiza el cálculo para documentos españoles.
Para el email y el teléfono hace uso de la API de IPQS, obteniendo únicamente el score de cada uno de ellos.
Al subir un fichero obtiene los metadatos, en el ejemplo se registran únicamente el autor y la fecha de creación.

Todos los datos se almacenan en una Google sheet y consumida desde looker studio para la presentación de los datos.

## requisitos
API de IPQS
cuenta de google + service account

## ejecución en local 
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
streamlit run registration.py
