import dotenv
import os
import requests

from simple_salesforce import Salesforce

dotenv.load_dotenv()


# Retrieving the data from .env file
client_id = os.getenv('SF_CONSUMER_KEY')
client_secret = os.getenv('SF_CONSUMER_SECRET')
instance_token_url = os.getenv('SF_TOKEN_URL')


payload = {"grant_type": "client_credentials"}

try:
    # Post credentials to get the token
    response = requests.post(instance_token_url, data=payload, auth=(client_id, client_secret))
    print(response)
    print(response.headers['content-type'])    
    print(response.json())
    
    if response.status_code == 200:
        sf_auth_data = response.json()
        sf_access_token = sf_auth_data['access_token']
        sf_instance_url = sf_auth_data['instance_url']


        sf_query_url = f"{sf_instance_url}/services/data/v64.0/query"
        sf_headers = {"Authorization" : f"Bearer {sf_access_token}"}
        sf_params = {"q" : "SELECT ID, Name FROM Account LIMIT 5"}
        sf_query_response = requests.get(sf_query_url, headers=sf_headers, params=sf_params)


        if sf_query_response.status_code == 200:
            sf_response_data = sf_query_response.json()
            sf_account_array = sf_response_data['records']
            sf_account_totalrecord = sf_response_data['totalSize']

            for tempaccount in sf_account_array:
                print(tempaccount['Id'])
                print(tempaccount['Name'])

    
except Exception as e:
    print(f"Error: {e}")
