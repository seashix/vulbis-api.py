from flask import Flask, request, jsonify
import cloudscraper
from bs4 import BeautifulSoup

app = Flask(__name__)

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

@app.route('/portals', methods=['GET'])
def get_all_portal_data():
    server = request.args.get('server', 'Draconiros')
    portals = ['Xélorium', 'Enutrosor', 'Ecaflipus', 'Srambad']
    
    all_data = []
    for portal in portals:
        data = fetch_portal_data(server, portal)
        all_data.append(data)
    
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=False, port=9952)
