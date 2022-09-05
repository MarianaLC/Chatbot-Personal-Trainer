from googleapiclient.discovery import build
from google.oauth2 import service_account
from unidecode import unidecode
import json


SERVICE_ACCOUNT_FILE = r'\Users\user\Desktop\MIEB_4\Semestre2\Ambientes_Inteligentes\TP2\rasa\client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1puG327IPMaC10-_4FAry1RtuuwIL5WQjrKTkJb36Wag'

def read():
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Teste!A2:B").execute()
    #result = sheet.values().set
    values = result.get('values', [])
    return values

def read_study():
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Summary!J2:K").execute()
    #result = sheet.values().set
    values = result.get('values', [])
    return values

def read_information():
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Teste!A2:G").execute()
    #result = sheet.values().set
    values = result.get('values', [])
    return values

def read_workouts():
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Treinos!A2:F").execute()
    #result = sheet.values().set
    values = result.get('values', [])
    return values

def read_period(page,cells):
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=f"{page}!{cells}").execute()
    #result = sheet.values().set
    values = result.get('values', [])
    return values

# --------------------- ISTO é PARA POR NA def run NO ficheiro actions.py-----------------------------------------
if __name__ == '__main__':
    
    nome = 'Lara'
    ultimo = 'Vaz'
    nome = unidecode(nome.upper())
    ultimo = unidecode(ultimo.upper())
    lista = read()
    '''for i in lista:
        first = unidecode(i[0].upper())
        last = unidecode(i[1].upper())
        #print(first,'----',nome)
        #print(last,'-----', ultimo)
        if first == nome and last == ultimo:
                #print(f'O Nome {first} {last} existe no excel')
                exit
    #print(f'Bem vindo {nome} {ultimo} !')'''
    
    ############################################

    ''' for i in read_study():
        #print(i)
        if unidecode(i[0].upper()) == nome:
            #print(i[1])
            #print(f'{nome} treinas melhor de {i[1]}')
            exit()
    #print("Não recolhi dados suficientes para te conseguir dizer isso!")'''

    '''for j in read_information():
        print(j)
        if unidecode(j[0].upper()) == nome and unidecode(j[1].upper()) == ultimo:
            idade=j[2]
            sexo=j[3]
            peso=j[4]
            altura=j[5]
            print(idade,sexo,peso,altura)'''


    '''imc_entrada='Baixo'
    escolha='pernas'
    for x in read_workouts():
            imc=x[0]
            #print(imc)
            treino = str(x[3])
            #print(treino)
            res = json.loads(treino)
            if imc == imc_entrada:
                for key,value in res.items():
                    print(key, ":", value)'''

    page='Summary'
    cells='A2:E'
    nome='Tiago'
    contador_manha = 0
    contador_tarde = 0
    HRR1_manha = 0
    HRR1_tarde = 0
    for x in read_period(page,cells):
        print(x)
        if x[0].upper() == nome.upper():
            if x[4] == 'Manhã':
                HRR1_manha += float(x[2])
                contador_manha += 1
            elif x[4] == 'Tarde':
                HRR1_tarde += float(x[2])
                contador_tarde += 1
    print(HRR1_tarde/contador_tarde)
    print(HRR1_manha/contador_manha)
    if (HRR1_tarde/contador_tarde) > (HRR1_manha/contador_manha):
        parte_dia = 'Tarde'
    elif (HRR1_tarde/contador_tarde) < (HRR1_manha/contador_manha):
        parte_dia = 'Manhã'
    print(parte_dia)
