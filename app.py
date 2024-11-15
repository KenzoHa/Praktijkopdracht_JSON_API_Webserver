'''
Sources: 
- https://canvas.kdg.be/courses/49874/pages/hoorcollege-api-clients?module_item_id=1057896 
- https://canvas.kdg.be/courses/49874/pages/wekcollge-zelf-een-api-aanmaken?module_item_id=1107129 
- https://canvas.kdg.be/courses/49874/assignments/208046 
- Anthropic AI (2024) - Claude 3.5 Sonnet - https://claude.ai

DATA Sources:
--> via website "My Json Server": https://my-json-server.typicode.com/ on my GitHub repo --> https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver
https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/locations
https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/devices
https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/db
'''

import requests
from flask import Flask, render_template, abort

app = Flask(__name__)

#gebruik de request.get() bij elke route, zo kan je filteren (haal enkel op wat nodig is) --> good practice

@app.route("/")
def home():
    return homepage() 

@app.route("/homepage")
def homepage():
    # Stuur een GET-verzoek om ALLE data op te halen
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/db')
    json_response = response.json()
    # Maak 2 lijsten om de data (zijnde 2 lijsten) in op te slaan
    locations = json_response['locations']
    devices = json_response['devices']
    
    return render_template("homepage.html", devices=devices, locations=locations)

@app.route("/devices")
def devices():
    # Stuur een GET-verzoek om DEVICES data op te halen
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/devices')
    # Maak devices variabele om de data in op te slaan (hier een lijst aanmaken is niet nodig, want het response is al een lijst)
    devices = response.json()
    
    return render_template("devices.html", devices=devices)

@app.route("/devices/<int:device_id>")
def device_detail(device_id):
    # Haal alle devices op
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/devices')
    devices = response.json()
    
    # Zoek het specifieke device
    device = next((device for device in devices if device['id'] == device_id), None)
    
    # Als het device niet gevonden is, toon een 404 error
    if device is None:
        abort(404)
    
    return render_template("device_detail.html", device=device)

@app.route("/locations")
def locations():
    # Stuur een GET-verzoek om LOCATIONS data op te halen
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/locations')
    locations = response.json()
    # Maak locations variabele om de data in op te slaan (hier een lijst aanmaken is niet nodig, want het response is al een lijst)
    
    return render_template("locations.html", locations=locations)

@app.route("/locations/<string:location_name>")
def location_detail(location_name):
    # Haal alle data op om zowel locaties als devices te kunnen checken
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/db')
    data = response.json()
    
    # Controleer of de locatie bestaat
    if location_name not in data['locations']:
        abort(404)
    
    # Filter devices voor deze locatie
    location_devices = [device for device in data['devices'] if device['location'] == location_name]
    
    return render_template("location_detail.html", location=location_name, devices=location_devices)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 