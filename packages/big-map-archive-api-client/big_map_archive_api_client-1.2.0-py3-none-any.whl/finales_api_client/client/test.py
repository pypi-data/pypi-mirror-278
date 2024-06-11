import requests

# get token
url = "https://api.finales.osl-sandbox.big-map.eu:443/user_management/authenticate"

response = requests.post(url, 
                         data={'username': 'user', 'password': 'user'}, 
                         headers={'Accept': 'application/json', 'Content-type': 'application/x-www-form-urlencoded'}
                        )

result = response.json()
token = result["access_token"]
print(token)

# get finales
# url_finales = "https://api.finales.osl-sandbox.big-map.eu:443/capabilities/?currently_available=false"
# url_finales = "https://api.finales.osl-sandbox.big-map.eu/all_requests/" 
url_finales = "https://api.finales.osl-sandbox.big-map.eu/results_requested/" 

response = requests.get(url_finales, 
                        headers={
                                'Accept': 'application/json', 
                                'Content-type': 'application/json', 
                                'Authorization': f'Bearer {token}'
                                },
                        stream=False
                        )

print(response.json())