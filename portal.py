import cloudscraper

url = 'https://www.vulbis.com/portal.php'  # URL de destination de la requête
data = {
    'server': 'Draconiros',
    'portal': 'Enutrosor'
}

# Créer un scraper qui contourne Cloudflare
scraper = cloudscraper.create_scraper()

# Envoyer une requête POST
response = scraper.post(url, data=data)

# Afficher la réponse
print(response.status_code)  # Code de statut HTTP
print(response.text)         # Corps de la réponse en texte
