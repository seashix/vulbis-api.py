from flask import Flask, request, render_template_string
import cloudscraper

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
    
    return render_template_string('''
        <h1>Response</h1>
        <p>Status Code: {{ status_code }}</p>
        <pre>{{ response_text }}</pre>
        <a href="/portal">Go Back</a>
    ''', status_code=response.status_code, response_text=response.text)

if __name__ == '__main__':
    app.run(debug=True)
