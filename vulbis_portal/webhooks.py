import requests
import json
import time

# URL de votre webhook Discord
WEBHOOK_URL = 'https://discord.com/api/webhooks/1255906181248188497/eA1RFrQG68T5vH80HkLbB9hWsfXTOwqlK_JQR04kChbS-GDKnzZVSCnfjhfCsP8CbCIf'

# URL du serveur Flask pour récupérer les données
FLASK_SERVER_URL = 'http://127.0.0.1:5000/portals?server=Draconiros'

# Dernier message envoyé pour mettre à jour plutôt qu'envoyer un nouveau
last_message_id = "1255906462337601576"

def send_discord_message(portal_data):
    global last_message_id

    embeds = []
    for data in portal_data:
        embed = {
            "title": f"Portal: {data['portal']}",
            "color": 3447003,
            "fields": [
                {"name": "Server", "value": data['server'], "inline": False},
                {"name": "Position", "value": data['position'], "inline": False},
                {"name": "Updated", "value": data['updated'], "inline": False}
            ]
        }
        embeds.append(embed)
    
    payload = {
        "embeds": embeds
    }

    headers = {
        "Content-Type": "application/json"
    }

    if last_message_id:
        response = requests.patch(f'{WEBHOOK_URL}/messages/{last_message_id}', headers=headers, data=json.dumps(payload))
    else:
        response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200 or response.status_code == 204:
            last_message_id = response.json().get('id')
    
    if response.status_code not in [200, 204]:
        print(f"Failed to send message: {response.status_code} - {response.text}")

while True:
    response = requests.get(FLASK_SERVER_URL)
    if response.status_code == 200:
        portal_data = response.json()
        send_discord_message(portal_data)
        print("Data refreshed!")
    else:
        print(f"Failed to retrieve portal data: {response.status_code} - {response.text}")
    
    time.sleep(2)  # Attendre 5 minutes avant de vérifier à nouveau
