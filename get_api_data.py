import requests


api = "https://api.nationalize.io/?name=johnson"

val_from = "EUR" 
val_to="USD"
EXCHANGE_TOKEN = ""
api_exchange = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_TOKEN}/pair/{val_from}/{val_to}"

def get_data(api: str) -> dict:
    response = requests.get(api)
    if response.status_code == 200:
        return response.json()
   
def get_nationalize(user_name: str) -> dict:
    api = "https://api.nationalize.io/"
    
    response = requests.get(api, params={"name":user_name})
    if response.status_code == 200:
        return response.json() 

if __name__ == "__main__":
    # name: str = input("Name: ")  
    # api: str = f"https://api.nationalize.io/?name={name}"    
    # print(get_nationalize(name))
    
    print(get_data(api_exchange))