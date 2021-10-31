import json
import os
from dotenv import load_dotenv
from requests.sessions import Session, session

from DataBase.database import GetCoinIdByName

load_dotenv()

def BuildHeader(api_token):

    header = {
        'x-access-token': api_token
    }

    return header


def GetCoinPrice(name):
    id = GetCoinIdByName(name)

    if(not id):
        print('An error ocurred')
    
    header = BuildHeader(os.environ.get('COIN_API_TOKEN'))
    session = Session()
    session.headers.update(header)

    endpoint = (os.environ.get('URL_COIN') + 'coin/{}/price').format(id[0])
    
    response = session.get(endpoint)

    if(response.status_code != 200):
        print('Error ocurred in API request')

    data = json.loads(response.text)

    return float(data["data"]["price"])

def GetDolarValue():

    endpoint = os.environ.get('URL_DOLAR_VALUE')
    session = Session()
    response = session.get(endpoint)

    data = json.loads(response.text)

    value = (float(data["USDBRL"]["high"]) + float(data["USDBRL"]["low"]))/2

    return value