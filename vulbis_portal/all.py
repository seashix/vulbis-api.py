import threading
import time
from web import run_flask_server
from webhooks import run_discord_webhook

def start_flask():
    run_flask_server()

def start_webhook():
    time.sleep(2)  # Attendre un court instant avant de démarrer le webhook Discord
    run_discord_webhook()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask)
    webhook_thread = threading.Thread(target=start_webhook)

    flask_thread.start()
    webhook_thread.start()

    flask_thread.join()
    webhook_thread.join()
