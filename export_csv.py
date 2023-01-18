import csv
import psycopg2

username = 'postgres'
password = 'A_m0N66'
database = 'beer_DB'
host = 'localhost'
port = '5432'

OUTPUT_FILE_T = 'beers_{}.csv'

TABLES = [
    'place',
    'info',
    'beers'
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for tablename in TABLES:
        cur.execute('SELECT * FROM ' + tablename)
        fields = [x[0] for x in cur.description]
        with open(OUTPUT_FILE_T.format(tablename), 'w', encoding="ISO-8859-1") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])
