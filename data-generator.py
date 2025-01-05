import csv
import random
from random import randint
from faker import Faker
from datetime import date

# Configuración de Faker para español
fake = Faker('es_ES')

# Función para generar un DNI válido
def generar_dni():
    numeros = ''.join(random.choices('0123456789', k=8))
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    letra = letras[int(numeros) % 23]
    return numeros + '-' + letra

def generar_usuario(nombre_completo):
  nombres = nombre_completo.split(' ')
  iniciales = ''.join(nombre[0] for nombre in nombres)
  apellido = nombres[-1]
  usuario = iniciales + apellido
  return usuario.lower()

def generar_datos(DNI_check):
    if DNI_check == '0':
        email_check =  randint(80,100)
        telefono_check = randint(80,100)
        saoftware = ['Excel', 'Photoshop', 'Google Sheets']
        fecha_creacion_nomina = fake.date_between(start_date=fecha_registro - 4, end_date=fecha_registro)
    else:
        email_check = randint(0,40)
        telefono_check = randint(0,40)
        software = ['NominaNet', 'Excel', 'Access', 'SAP', 'Business Central', 'Sage', 'A3', 'Nominasol', 'Nominaplus']
        fecha_creacion_nomina = fake.date_between(start_date=fecha_inicio, end_date=fecha_registro)
    return email_check, telefono_check, software, fecha_creacion_nomina
# Datos a generar
num_registros = 5
fecha_inicio = date(2024, 12, 1)
fecha_fin = date(2024, 12, 31)
fecha_registro = fake.date_between(start_date=fecha_inicio, end_date=fecha_fin)
empresas = ['Inditex', 'Repsol', 'Telefónica', 'Iberdrola', 'BBVA', 'Santander', 'CaixaBank', 'Mapfre', 'Endesa', 'Naturgy','Mercadona']
DNI_check = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']



# Crear el archivo CSV
with open('datos_nomina.csv', 'w', newline='') as csvfile:
    fieldnames = ['Nombre', 'Apellidos', 'DNI','DNI check', 'email', 'email check','telefono', 'telefono check', 'Dirección postal', 'Nomina', 'Empresa', 'Autor nómina', 'Software', 'Fecha creacion nómina', 'Fecha registro']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for _ in range(num_registros):
        nombre_completo =  fake.name()
        row = {
            'Nombre': nombre_completo.split()[0],
            'Apellidos': nombre_completo.split()[1:][0],
            'DNI': generar_dni(),
            'DNI check': random.choice(DNI_check),
            'email': fake.email(),
            'email check': generar_datos(DNI_check)[0],
            'telefono': fake.phone_number(),
            'telefono check':  generar_datos(DNI_check)[1],
            'Dirección postal': fake.address(),
            'Nomina':'',
            'Empresa': random.choice(empresas),
            'Autor nómina': generar_usuario(nombre_completo),
            'Software': random.choice(generar_datos(DNI_check)[2]),
            'Fecha creacion nómina':  generar_datos(DNI_check)[3],
            'Fecha registro': fecha_registro,
        }
        writer.writerow(row)