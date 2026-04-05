import dotenv
import os
import requests
import json

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
    print("------------------------------------------------------------")
    print("******We received the access token*********")    
    print(response.json())
    print("------------------------------------------------------------")
    
    #Post response to fetch the access token and intance url
    if response.status_code == 200:
        sf_auth_data = response.json()
        sf_access_token = sf_auth_data['access_token']
        sf_instance_url = sf_auth_data['instance_url']


        # HTTP Get Request to get the Order details from APEX Class exposed as REST API
        sf_query_url = f"{sf_instance_url}/services/apexrest/OrderManagement/replace_with_an_orderid"
        sf_headers = {"Authorization" : f"Bearer {sf_access_token}"}
        sf_query_response = requests.get(sf_query_url, headers=sf_headers)


        # Response of Get Request contains Order Details
        if sf_query_response.status_code == 200:
            sf_response_data = sf_query_response.json()
            print("------------------------------------------------------------")
            print("******We received the response of get method below*********")            
            print(sf_response_data)
            print("------------------------------------------------------------")
        
        # HTTP POST Request to create an Account using an APEX Class exposed as REST API
        sf_query_url = f"{sf_instance_url}/services/apexrest/OrderManagement/"
        sf_headers = {"Authorization" : f"Bearer {sf_access_token}", "Content-Type": "application/json"}
        sf_data = {"name" : "PythonRestAPITest", "phone" : "1234567890", "website" : "pythonenv@test.com"}
        sf_query_response = requests.post(sf_query_url, headers=sf_headers, json=sf_data)

        # Response of POST Request
        if sf_query_response.status_code == 200:
            sf_response_data = sf_query_response.json()
            print("------------------------------------------------------------")
            print("******We received the response of post method below*********")            
            print(sf_response_data)
            print("------------------------------------------------------------")
        
        # HTTP PUT Request to update OrderItem using an APEX Class exposed as REST API
        sf_query_url = f"{sf_instance_url}/services/apexrest/OrderManagement/"
        sf_headers = {"Authorization" : f"Bearer {sf_access_token}", "Content-Type": "application/json"}
        sf_data = {"orderItemId" : "replace_with_an_orderid", "unitPrice" : 75000, "quantity" : 1}
        sf_query_response = requests.put(sf_query_url, headers=sf_headers, data=json.dumps(sf_data))

        # Response of PUT Request
        if sf_query_response.status_code == 200:
            sf_response_data = sf_query_response.json()
            print("------------------------------------------------------------")
            print("******We received the response of put method below*********")            
            print(sf_response_data)
            print("------------------------------------------------------------")
    
except Exception as e:
    print(f"Error: {e}")
