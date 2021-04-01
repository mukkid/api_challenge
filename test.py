import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api', methods=['GET', 'POST', 'DELETE'])
def hello_world():
    con = sqlite3.connect('api.db')
    con.execute('CREATE TABLE IF NOT EXISTS site (domain TEXT)')
    if request.method == 'POST':
        '''
        {'domain': the_domain}
        '''
        domain = request.form.get('domain')
        with con:
            con.execute('INSERT INTO site VALUES (?)', (domain,))
        return domain
    elif request.method == 'DELETE':
        domain = request.form.get('domain')
        try:
            with con:
                con.execute('DELETE FROM site WHERE domain=?', (domain,))
        except TypeError:
            return '400'
        else:
            return '200'
    else:
        with con:
            sites = []
            for d in con.execute('SELECT * FROM site').fetchall():
                sites.append(d)
        return jsonify(sites)

if __name__ == '__main__':
    app.run(debug=True)
