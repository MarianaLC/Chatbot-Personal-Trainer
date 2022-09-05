# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import json, re

#----------------------------------------------------------------------------------------------------------------------------
from googleapiclient.discovery import build
from google.oauth2 import service_account
from unidecode import unidecode

############################################################################################################################
SERVICE_ACCOUNT_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1puG327IPMaC10-_4FAry1RtuuwIL5WQjrKTkJb36Wag'

def write(lista):
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Teste!A:A", valueInputOption='USER_ENTERED', body={"values":lista}).execute()
    print(request)
    
########################################################################################################################################################################
def read(page,cols):
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=f"{page}!{cols}").execute()
    #result = sheet.values().set
    values = result.get('values', [])
    return values

############################################################################################################################
#----------------------------------------------------------------------------------------------------------------------------------------

class ValidateSimpleUserForm(FormValidationAction):
    def name(self) -> Text:
         return "validate_simple_user_form"

    def validate_first_name(self, slot_value: Any, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        first_name = tracker.get_slot("first_name")
        print("Apanhei este nome próprio: ",first_name)
        return []

    def validate_last_name(self, slot_value: Any, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        first_name = tracker.get_slot("first_name")  
        last_name = tracker.get_slot("last_name")
        print("Apanhei este apelido: ", last_name)
        nome = unidecode(first_name.upper())
        ultimo = unidecode(last_name.upper())

        page = 'Teste'
        cols = 'A2:B'
        page1 = 'Teste'
        cols1 = 'A2:G'

        lista = read(page,cols)
        for i in lista:
          first = unidecode(i[0].upper())
          last = unidecode(i[1].upper())
          print(first,last)
          print(nome,ultimo)
          if first == nome and last == ultimo:
            print("Ele já existe")
            dispatcher.utter_message(text="Já estás registado!")
            for j in read(page1,cols1):
               if unidecode(j[0].upper()) == nome and unidecode(j[1].upper()) == ultimo:
                    idade=j[2]
                    sexo=j[3]
                    peso=j[4]
                    altura=j[5]
                    print(idade,sexo,peso,altura)
                    return {"user_age":idade,"user_sex":sexo, "user_weight":peso, "user_height":altura, "requested_slot": None}
        print(i) # Os nomes que existem na base de dados
        return{"first_name":first_name,"last_name":last_name}

    def validate_user_age(self, slot_value: Any, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        idade = tracker.get_slot("user_age")
        if 5 > int(idade) or int(idade) > 100:
             dispatcher.utter_message(text="A tua idade não está dentro dos limites aceitáveis aqui do ginásio!")
             return {"user_age": None}
        else:
             return {"user_age":idade}


    def validate_user_weight(self, slot_value: Any, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        peso = tracker.get_slot("user_weight")
        if 20 > float(peso) or float(peso) > 200:
             dispatcher.utter_message(text="O teu peso é inválido!")
             return {"user_weight": None}
        else:
             return {"user_weight":peso}
    
    def validate_user_height(self, slot_value: Any, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        altura = tracker.get_slot("user_height")
        if 0.50 > float(altura) or float(altura) > 2.70:
             dispatcher.utter_message(text="A tua altura é inválido!")
             return {"user_height": None}
        else:
             return {"user_height":altura}

class AddUserInformation(Action):
    def name(self) -> Text:
         return "addition_simple_user_form"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        lista_user=[]
        sinal=0

        first_name = tracker.get_slot("first_name")
        last_name = tracker.get_slot("last_name")
        user_age = tracker.get_slot("user_age")
        user_sex = tracker.get_slot("user_sex")
        user_weight = tracker.get_slot("user_weight")
        user_height = tracker.get_slot("user_height")

        page = 'Teste'
        cols = 'A2:B'


        if (first_name == None or last_name == None or user_age == None or user_sex == None or user_weight == None or user_height == None):
             print("Lista Incompleta")
        else:
             first_name = tracker.get_slot("first_name")  
             last_name = tracker.get_slot("last_name")
             nome = unidecode(first_name.upper())
             ultimo = unidecode(last_name.upper())
             lista = read(page,cols)
             for i in lista:
               first = unidecode(i[0].upper())
               last = unidecode(i[1].upper())
               if first == nome and last == ultimo:
                    sinal = 1
             if sinal == 0:
               # Calculo do IMC
               IMC = float(user_weight)/(float(user_height)*float(user_height)) 
               # Escreve dados no excel     
               lista_user.append([first_name,last_name,user_age,user_sex,user_weight,user_height,IMC])



               if IMC < 18.5:
                   dispatcher.utter_message(text="Estou aqui a analisar e tens que ter cuidado. O teu Índice de Massa Corporal está muito baixo.")
               elif  25 > IMC > 18.5:
                   dispatcher.utter_message(text="Estou aqui a analisar e o teu Índice de Massa Corporal está bom!")
               elif  30 > IMC >= 25:
                   dispatcher.utter_message(text="Estou aqui a analisar e tens que ter cuidado. O teu Índice de Massa Corporal está um pouco elevado.") 
               elif  30 <= IMC:
                   dispatcher.utter_message(text="Estou aqui a analisar e tens que ter cuidado. O teu Índice de Massa Corporal está muito alto.")
               
               
               
               
               ValidateSimpleUserForm.validate_last_name
               print(lista_user)
               write(lista_user)
             else:
               print("Não acrescenta à base de dados")
        return []

class ListWorkoutDetails(Action):
    def name(self) -> Text:
         return "action_list_workout"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         page1 = 'Teste'
         cols1 = 'A2:G'

         # Retorna um array de entities
         entities = tracker.latest_message['entities']
         for e in entities:
              if e['entity'] == 'muscular_group':
                   entity_muscular = e['value']
         for x in read(page1,cols1):
              # Analisar o IMC
              dado=re.sub(r',',r'.',x[6])
              if float(dado) < 18.5:
                   imc='Baixo'
              elif  25 > float(dado) > 18.5:
                   imc='Normal'
              elif  30 > float(dado) >= 25:
                   imc='Sobrepeso' 
              elif  30 <= float(dado):
                   imc='Obeso'
         

         user_choice = tracker.get_slot("muscular_group")
         #dispatcher.utter_message(text=f"Tu escolheste {user_choice}")
         page = 'Treinos'
         cols = 'A2:F'
         if user_choice == "pernas":
              dispatcher.utter_message(text="Muito bem vamos lá treinar pernas")
              dispatcher.utter_message(text='Aqui tens o teu plano de treino:')
              for x in read(page,cols): 
                    col1=x[0]
                    treino = str(x[3])
                    res = json.loads(treino)
                    if imc == col1:
                         for key,value in res.items():
                              #print(i)
                              dispatcher.utter_message(text=f'{key} : {value}')
              dispatcher.utter_message(text='Avisa quando terminares! Qualquer dúvida é só perguntar que estou disponível.')
         elif user_choice == "braços":
              dispatcher.utter_message(text="Muito bem vamos lá treinar braços")
              dispatcher.utter_message(text='Aqui tens o teu plano de treino:')
              for x in read(page,cols): 
                    col1=x[0]
                    treino = str(x[2])
                    res = json.loads(treino)
                    if imc == col1:
                         for key,value in res.items():
                              #print(i)
                              dispatcher.utter_message(text=f'{key} : {value}')
              dispatcher.utter_message(text='Avisa quando terminares! Qualquer dúvida é só perguntar que estou disponível.')
         elif user_choice == "peito":
              dispatcher.utter_message(text="Muito bem vamos lá treinar peito")
              dispatcher.utter_message(text='Aqui tens o teu plano de treino:')
              for x in read(page,cols): 
                    col1=x[0]
                    treino = str(x[1])
                    res = json.loads(treino)
                    if imc == col1:
                         for key,value in res.items():
                              #print(i)
                              dispatcher.utter_message(text=f'{key} : {value}')
              dispatcher.utter_message(text='Avisa quando terminares! Qualquer dúvida é só perguntar que estou disponível.')
         elif user_choice == "ombros":
              dispatcher.utter_message(text="Muito bem vamos lá treinar ombros")
              dispatcher.utter_message(text='Aqui tens teu plano de treino:')
              for x in read(page,cols): 
                    col1=x[0]
                    treino = str(x[5])
                    res = json.loads(treino)
                    if imc == col1:
                         for key,value in res.items():
                              #print(i)
                              dispatcher.utter_message(text=f'{key} : {value}')
              dispatcher.utter_message(text='Avisa quando terminares! Qualquer dúvida é só perguntar que estou disponível.') 
         elif user_choice == "costas":
              dispatcher.utter_message(text="Muito bem vamos lá treinar costas")
              dispatcher.utter_message(text='Aqui tens o teu plano de treino:')
              for x in read(page,cols): 
                    col1=x[0]
                    treino = str(x[4])
                    res = json.loads(treino)
                    if imc == col1:
                         for key,value in res.items():
                              #print(i)
                              dispatcher.utter_message(text=f'{key} : {value}')
              dispatcher.utter_message(text='Avisa quando terminares! Qualquer dúvida é só perguntar que estou disponível.')
         else:
             dispatcher.utter_message(text="Essa opção não existe! Escolhe de novo.") 
         return []

class InformBetterTimeToWorkout(Action):
    def name(self) -> Text:
         return "inform_better_time_workout"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        page = 'Summary'
        cols = 'A2:E'
        contador_manha = 0
        contador_tarde = 0
        HRR1_manha = 0
        HRR1_tarde = 0
        sinalizador = 0
     
        if  (tracker.get_slot("first_name")) == None:
             #print('Entrei aqui')
             dispatcher.utter_message(response = "utter_what_is_your_name")
     
        nome = tracker.get_slot("first_name")
        if  nome == None:
             print("Algo correu mal")
        else:
          first_name1 = tracker.get_slot("first_name")
          first_name = unidecode(first_name1.upper())
          ############################# CALCULO DO MELHOR PERIODO DO DIA ######################################################
          for x in read(page,cols):
               print(x)
               if unidecode(x[0].upper()) == first_name:
                    sinalizador = 1
                    if x[4] == 'Manhã':
                         HRR1_manha += float(x[2])
                         contador_manha += 1
                    elif x[4] == 'Tarde':
                         HRR1_tarde += float(x[2])
                         contador_tarde += 1
          #print(HRR1_tarde/contador_tarde)
          #print(HRR1_manha/contador_manha)

          ######################################################################################################################
          if sinalizador == 1:
               if (HRR1_tarde/contador_tarde) > (HRR1_manha/contador_manha):
                    parte_dia = 'tarde'
               elif (HRR1_tarde/contador_tarde) < (HRR1_manha/contador_manha):
                    parte_dia = 'manhã'
               dispatcher.utter_message(text=f'Segundo a análise que fiz aos dados recolhidos \npelo teu smartwatch, tu treinas melhor de {parte_dia}, {first_name1}!')
          else:  
               dispatcher.utter_message(f"Desculpa {first_name1}, mas ainda não recolhi dados suficientes para te conseguir dizer isso! Mas não desanimes,\n traz o teu smartwatch e continua a treinar comigo que os resultados vão aparecer! ")
        return[]

class SayGoodBye(Action):
    def name(self) -> Text:
         return "action_goodbye_user"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

             if tracker.get_slot("first_name") == None and tracker.get_slot("last_name"): # Não se quis registar
                  dispatcher.utter_message(text='Então, até à próxima! Espero que entretanto mudes de ideias e venhas treinar comigo!')
             elif tracker.get_slot("first_name") != None: # Membro Registado
                  dispatcher.utter_message(text='Então, adeus! Foi um prazer e espero ver-te por cá com frequência.')


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"
    def run(self, dispatcher, tracker, domain):
        # output a message saying that the conversation will now be
        # continued by a human.
 
        message = "Não percebi bem o que quiseste dizer. Repete, por favor"
        dispatcher.utter_message(text=message)
             
          