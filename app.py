'''
Sources: 
- https://canvas.kdg.be/courses/49874/pages/hoorcollege-api-clients?module_item_id=1057896 
- https://canvas.kdg.be/courses/49874/pages/wekcollge-zelf-een-api-aanmaken?module_item_id=1107129 
- https://canvas.kdg.be/courses/49874/assignments/208046 
- Anthropic AI (2024) - Claude 3.5 Sonnet - https://claude.ai

DATA Sources:
--> via website "My Json Server": https://my-json-server.typicode.com/ on my GitHub repo --> https://github.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver
https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/locations
https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/devices
https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/db

IMAGES: 
hoofdkantoor --> https://www.pfizer.be/nl/over-ons/pfizer-in-belgie/hoofdkantoor-brussel 
productiehal --> https://www.nbd-online.nl/nieuws/187913-Op-deze-manier-behaal-je-maximale-productiviteit-in-een-productiehal 
distrubutiecentrum --> https://wanscale.com/klantcases/distributiecentrum/ 
R&D laboratorium --> https://www.pmgroup-global.com/our-work/biopharma-rd-lab-emd-sero/ 
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
    # Maak een mapping van locatie-id naar locatie-naam
    locations_dict = {location['id']: location['name'] for location in json_response['locations']}
    devices = json_response['devices']
    
    # Voeg de locatie-naam toe aan elk device
    for device in devices:
        device['location_name'] = locations_dict[device['location_id']]
    
    return render_template("homepage.html", devices=devices, locations=json_response['locations'])

@app.route("/devices")
def devices():
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/db')
    data = response.json()

    # Maak een mapping van locatie-id naar locatie-naam
    locations_dict = {location['id']: location['name'] for location in data['locations']}
    devices = data['devices']

    # Voeg de locatie-naam toe aan elk device
    for device in devices:
        device['location_name'] = locations_dict[device['location_id']]

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

@app.route("/locations/<int:location_id>")
def location_detail(location_id):
    response = requests.get('https://my-json-server.typicode.com/KenzoHa/Praktijkopdracht_JSON_API_Webserver/db')
    data = response.json()

    # Zoek de locatie
    location = next((loc for loc in data['locations'] if loc['id'] == location_id), None)
    if location is None:
        abort(404)

    # Filter devices voor deze locatie
    location_devices = [device for device in data['devices'] if device['location_id'] == location_id]

    return render_template("location_detail.html", location=location['name'], devices=location_devices)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 