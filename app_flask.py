from flask import Flask, request, render_template_string
import cloudscraper
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/portal')
def home():
    return '''
        <form action="/portal/data" method="post">
            <label for="portal">Portal:</label><br>
            <select name="portal" id="portal" class="form-select">
                <option value="Xélorium" selected>Xélorium</option>
                <option value="Enutrosor">Enutrosor</option>
                <option value="Ecaflipus">Ecaflipus</option>
                <option value="Srambad">Srambad</option>
            </select> <br>
            
            <label for="server">Server:</label><br>
            <select name="server" id="server" class="form-select">
                <option value="Draconiros" selected>Draconiros</option>
                <option value="Orukam">Orukam</option>
                <option value="Tylezia">Tylezia</option>
                <option value="Hell Mina">Hell Mina</option>
                <option value="Imagiro">Imagiro</option>
                <option value="Tal Kasha">Tal Kasha</option>
                <option value="Ombre">Ombre</option>
            </select> <br><br>
            
            <input type="submit" value="Submit">
        </form>
        <hr>
        <p>Response based on Vulbis.com</p>
    '''

@app.route('/portal/data', methods=['POST'])
def get_data():
    server = request.form['server']
    portal = request.form['portal']
    
    url = 'https://www.vulbis.com/portal.php'
    data = {
        'server': server,
        'portal': portal
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, data=data)
    
    # Analyse de la réponse HTML pour extraire les informations nécessaires
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Imprimer le HTML pour le débogage
    print(response.text)
    
    # Extraire le serveur et le portail
    server_info = soup.find('span', style="float:left;")
    portal_info = soup.find('span', style="float:right;")
    
    if server_info:
        server_info = server_info.contents[1].strip()
    else:
        server_info = "N/A"
    
    # Extraire la position
    position = "N/A"
    if portal_info:
        portal_text = portal_info.text.strip()
        if ': ' in portal_text:
            portal_parts = portal_text.split(': ')
            if len(portal_parts) > 1:
                position_part = portal_parts[1]
                if '[' in position_part and ']' in position_part:
                    position = position_part[position_part.find('[') + 1:position_part.find(']')]
    
    # Extraire le temps écoulé
    time_info = "N/A"
    time_info_tag = soup.find('b', text="Actualisé : ")
    if time_info_tag:
        time_info = time_info_tag.next_sibling.strip()
    
    return render_template_string('''
        <h1>Response</h1>
        <p>Status Code: {{ status_code }}</p>
        <p>Server: {{ server }} <br>
        Portal: {{ portal }} <br>
        Position: /travel [{{ position }}] <br>
        Updated: {{ time_info }}</p>
        <hr>
        <p>Original response</p>
        <pre>{{ response_text }}</pre>
        <hr>
        <a href="/portal">Go Back</a>
    ''', status_code=response.status_code, server=server_info, portal=portal, position=position, time_info=time_info, response_text=response.text)



if __name__ == '__main__':
    app.run(debug=True)
