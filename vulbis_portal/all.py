import subprocess
import time

def run_flask_server():
    subprocess.Popen(['python3', 'web.py'])

def run_discord_webhook():
    subprocess.Popen(['python3', 'webhooks.py'])

if __name__ == '__main__':
    run_flask_server()
    time.sleep(2)  # Attendre un court instant avant de démarrer le webhook Discord
    run_discord_webhook()
