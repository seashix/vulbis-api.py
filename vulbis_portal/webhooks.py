import requests
import json
import time

WEBHOOK_URL = 'https://discord.com/api/webhooks/1255906181248188497/eA1RFrQG68T5vH80HkLbB9hWsfXTOwqlK_JQR04kChbS-GDKnzZVSCnfjhfCsP8CbCIf'
DOFUS_SERVER = "Draconiros"
LAST_MESSAGE_ID = "1255906462337601576"  # Stocker l'ID du dernier message envoyé


def fetch_portal_data():
    response = requests.get('http://127.0.0.1:9952/portals?server='+DOFUS_SERVER)  # Utilisez localhost ou l'IP locale
    return response.json() if response.status_code == 200 else []

def send_discord_message(portal_data):
    global LAST_MESSAGE_ID

    embeds = [{
        "title": "Informations",
        "color": 3447003,
        "fields": [
            {"name": "Server", "value": DOFUS_SERVER, "inline": False},
            {"name": "Copyright", "value": "Based on Vulbis.com \"API\" \n Dev by [@Initialisation](https://github.com/initialisation)", "inline": False}
        ]
    }]
    
    for data in portal_data:
        embed = {
            "title": f"{data['portal']}",
            "color": 3447003,
            "fields": [
                {"name": "Position", "value": f"/travel [{data['position']}]", "inline": False},
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

    if LAST_MESSAGE_ID:
        response = requests.patch(f'{WEBHOOK_URL}/messages/{LAST_MESSAGE_ID}', headers=headers, data=json.dumps(payload))
    else:
        response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload))
        if response.status_code in [200, 204]:
            LAST_MESSAGE_ID = response.json().get('id')
    
    if response.status_code not in [200, 204]:
        print(f"[Webhooks Thread] Vulbis Portal: Failed to send message: {response.status_code} - {response.text}")

def run_discord_webhook():
    while True:
        portal_data = fetch_portal_data()
        send_discord_message(portal_data)
        print(f"[Webhooks Thread] Vulbis Portal: Success to send message: {response.status_code} - Data refreshed")
        time.sleep(300)  # Attendre 5 minutes avant de vérifier à nouveau

if __name__ == '__main__':
    run_discord_webhook()
