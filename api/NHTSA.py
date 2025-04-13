import requests

def vinUS(vin):
    response = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json')
    if response.status_code == 200:
        data = [item for item in response.json()['Results'] if item['Value']]
        return data
    else:
        return ["❌ Failed to fetch vehicle details."]