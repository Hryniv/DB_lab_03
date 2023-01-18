import psycopg2
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np


username = 'postgres'
password = 'A_m0N66'
database = 'beer_DB'
host = 'localhost'
port = '5432'


query_0 = """
DELETE FROM Beers;
DELETE FROM Place;
DELETE FROM Info;
"""

query_place = """
INSERT INTO Place(place_id, place_country, place_state) VALUES ('%s', '%s', '%s')
"""

query_info = """
INSERT INTO Info(info_id, info_style, info_availability, info_abv, info_notes) VALUES ('%s', '%s', '%s', '%s', '%s')
"""


query_beers = """
INSERT INTO Beers(beer_id, beer_name, place_id, info_id) VALUES ('%s', '%s', 
(SELECT place_id FROM place WHERE place_country = '%s' AND place_state = '%s'),
(SELECT info_id FROM info WHERE info_style = '%s' AND info_availability = '%s' AND info_abv = '%s' AND info_notes = '%s'))
"""


data = pd.read_csv(r'beers.csv', encoding="ISO-8859-1")

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_0)

    df = pd.DataFrame(data, columns=['name', 'state', 'country', 'style', 'availability', 'abv', 'notes'])
    df = df.astype(object).replace(np.nan, 'NULL')  # заміняємо всі значення nan на 'None'

    cur1 = conn.cursor()
    place_country = df['country'].tolist()
    place_state = df['state'].tolist()

    place_unique = []  # [place_country, place_state]

    for i in range(len(place_country)):
        x = [place_country[i], place_state[i]]
        if x not in place_unique:
            place_unique.append(x)


    for i in range(len(place_unique)):
        query = query_place % (i, place_unique[i][0], place_unique[i][1])
        cur1.execute(query)
    conn.commit()


    cur2 = conn.cursor()

    info_style = df['style'].tolist()
    info_availability = df['availability'].tolist()
    info_abv = df['abv'].tolist()
    info_notes = df['notes'].tolist()

    unique = []   # [info_style, info_availability, info_abv, info_notes]

    for i in range(len(info_style)):
        x = [info_style[i], info_availability[i], info_abv[i], info_notes[i]]
        if x not in unique:
            unique.append(x)


    for i in range(len(unique)):
        unique[i][3] = unique[i][3].replace('\'', '')
        query = query_info % (i, unique[i][0], unique[i][1], unique[i][2], unique[i][3])
        cur2.execute(query)
    conn.commit()


    cur3 = conn.cursor()
    beer_name = df['name'].tolist()

    u_beer_name = []
    for el in beer_name:
        if el not in u_beer_name:
            u_beer_name.append(el)

    i = 0
    for i in range(len(u_beer_name)):
        u_beer_name[i] = u_beer_name[i].replace('\'', '')  # апострофи призводять до помилки
        info_notes[i] = info_notes[i].replace('\'', '')
        query = query_beers % (i, u_beer_name[i],
                               place_country[i], place_state[i],
                               info_style[i], info_availability[i], info_abv[i], info_notes[i],
                               )
        cur3.execute(query)
    conn.commit()
