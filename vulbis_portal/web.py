from flask import Flask, request, jsonify
import cloudscraper
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

def fetch_portal_data(server, portal):
    url = 'https://www.vulbis.com/portal.php'
    data = {
        'server': server,
        'portal': portal
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, data=data)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    server_info = soup.find('span', style="float:left;")
    portal_info = soup.find('span', style="float:right;")
    
    if server_info:
        server_info = server_info.contents[1].strip()
    else:
        server_info = "N/A"
    
    position = "N/A"
    if portal_info:
        portal_text = portal_info.text.strip()
        if ': ' in portal_text:
            portal_parts = portal_text.split(': ')
            if len(portal_parts) > 1:
                position_part = portal_parts[1]
                if '[' in position_part and ']' in position_part:
                    position = position_part[position_part.find('[') + 1:position_part.find(']')]
    
    time_info = "N/A"
    time_info_tag = soup.find('b', text="Actualisé : ")
    if time_info_tag:
        time_info = time_info_tag.next_sibling.strip()
    
    return {
        'server': server_info,
        'portal': portal,
        'position': position,
        'updated': time_info
    }

@app.route('/')


@app.route('/portals', methods=['GET'])
def get_all_portal_data():
    server = request.args.get('server', 'Draconiros')
    portals = ['Xélorium', 'Enutrosor', 'Ecaflipus', 'Srambad']
    
    all_data = []
    for portal in portals:
        data = fetch_portal_data(server, portal)
        all_data.append(data)
    
    return jsonify(all_data)

def run_flask_server():
    app.run(debug=False, port=9952, use_reloader=False)  # Remplacez 5001 par le port de votre choix et désactivez le reloader

if __name__ == '__main__':
    run_flask_server()
