import streamlit as st
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import re
import json
import requests
from typing import Union
from wtforms.validators import Email
import os
from dotenv import load_dotenv
from datetime import datetime
import tempfile
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from dateutil import parser
import base64

# Button disable
st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    .stMainMenu {   
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True
)
# API
IPQS_API_KEY = os.getenv("IPQS_API_KEY")

# Credenciales de Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'hello-world-d0794-bb8a32250c8d.json'
creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
# ID de tu hoja de cálculo
spreadsheet_id = '1-cucBIOOsQEz98IgvysC-eGtfDp69c4xdBHRH1WYbmM'

# Validación de DNI
class ValidaDNI:
    REGEXP = "[0-9]{8}[A-Z]"
    DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
    INVALIDOS = {"00000000T", "00000001R", "99999999R"}

    def __init__(self):
        pass

    def validar_dni(self, dni: str) -> bool:
        return dni not in self.INVALIDOS \
            and re.match(self.REGEXP, dni) is not None \
            and dni[8] == self.DIGITO_CONTROL[int(dni[0:8]) % 23]

# Valida email
class ValidaEMAIL(object):
    """
    Class for interacting with the IPQualityScore API.

    Attributes:
        key (str): Your IPQS API key.
        format (str): The format of the response. Default is 'json', but you can also use 'xml'.
        base_url (str): The base URL for the IPQS API.

    Methods:
        email_validation_api(email: str, timeout: int = 1, fast: str = 'false', abuse_strictness: int = 0) -> str:
            Returns the response from the IPQS Email Validation API.
    """

    key = None
    format = None
    base_url = None

    def __init__(self, key, format="json") -> None:
        self.key = key
        self.format = format
        self.base_url = f"https://www.ipqualityscore.com/api/{self.format}/"


    def email_validation_api(self, email: str, timeout: int = 7, fast: str = 'false', abuse_strictness: int = 0) -> str:
        """
        Returns the response from the IPQS Email Validation API.

        Args:
            email (str):
                The email you wish to validate.
            timeout (int):
                Set the maximum number of seconds to wait for a reply from an email service provider.
                If speed is not a concern or you want higher accuracy we recommend setting this in the 20 - 40 second range in some cases.
                Any results which experience a connection timeout will return the "timed_out" variable as true. Default value is 7 seconds.
            fast (str):
                If speed is your major concern set this to true, but results will be less accurate.
            abuse_strictness (int):
                Adjusts abusive email patterns and detection rates higher levels may cause false-positives (0 - 2).

        Returns:
            str: The response from the IPQS Email Validation API.
        """

        url = f"{self.base_url}email/{self.key}/{email}"

        params = {
            "timeout": timeout,
            "fast": fast,
            "abuse_strictness": abuse_strictness
        }

        response = requests.get(url, params=params)
        return response.text

# Validar teléfono
class IPQS:
    key =  IPQS_API_KEY
    def phone_number_api(self, phonenumber: str, vars: dict = {}) -> dict:
        url = 'https://www.ipqualityscore.com/api/json/phone/%s/%s' %(self.key, phonenumber)
        x = requests.get(url, params = vars)
        return (json.loads(x.text))
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()
line = len(df) + 2

st.title("Silictud de finnaciación")

with st.form(key='personal_data'):
    nombre = st.text_input("Nombre")
    apelidos = st.text_input("Apellidos")
    DNI = st.text_input("DNI")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")
    direccion = st.text_input("Dirección postal")
    empresa = st.text_input("Empresa")
    uploaded_file = st.file_uploader("File upload", type="pdf")
    if uploaded_file:
        with st.spinner('Cargando datos ...'):
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)

            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
            fp = open(path, 'rb')
            parsed_file = PDFParser(fp)
            doc = PDFDocument(parsed_file)

            nomina = uploaded_file.name
            try:
                author = doc.info[0]['Author'].decode('utf-8')
            except:
                author = ""
            try:
                producer = doc.info[0]['Producer'].decode('utf-16')
            except:
                producer = ""
                
            CreationDate = parser.parse(doc.info[0]['CreationDate'].decode('utf-8')[2:14])


    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        DNI_check = ValidaDNI().validar_dni(DNI)
        try:
            EMAIL_check = ValidaEMAIL(IPQS_API_KEY).email_validation_api(email)
            EMAIL_fraud = json.loads(EMAIL_check)["fraud_score"]

            ipqs = IPQS()
            countries = {'ES'}
            additional_params = {
                'country' : countries
            }
            PHONE_check  = ipqs.phone_number_api(telefono, additional_params)
            PHONE_fraud = PHONE_check["fraud_score"]
        except:
            EMAIL_fraud = ""
            PHONE_fraud = ""

        fecha_registro = datetime.today().strftime('%Y-%d-%m %H:%M:%S')

        conn = st.connection("gsheets", type=GSheetsConnection)
        new_record = [str(nombre), str(apelidos), str(DNI), bool(DNI_check), str(email), EMAIL_fraud, str(telefono), PHONE_fraud, str(direccion), str(nomina), str(empresa), str(author), str(producer), str(CreationDate), str(fecha_registro)]
        range_ = f'Data!A{line}:O{line}'
        body = {'values': [new_record]}
        result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
           range=range_,
           valueInputOption='RAW',
           body=body).execute()
        st.write('{0} cells updated.'.format(result.get('updatedCells')))
        st.cache_data.clear()
        st.rerun()
        
# Create a connection object.
#conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()
#st.write(df)

