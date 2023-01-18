import json
import psycopg2

username = 'postgres'
password = 'A_m0N66'
database = 'beer_DB'
host = 'localhost'
port = '5432'

TABLES = [
    'place',
    'info',
    'beers'
]

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:

    cur = conn.cursor()
    
    for tablename in TABLES:
        cur.execute('SELECT * FROM ' + tablename)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[tablename] = rows

with open('all_data.json', 'w', encoding="ISO-8859-1") as outf:
    json.dump(data, outf, default=str)
