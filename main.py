import psycopg2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

username = 'postgres'
password = 'A_m0N66'
database = 'beer_DB'
host = 'localhost'
port = '5432'

query_1 = '''
CREATE VIEW ByInfoAbv AS
SELECT TRIM(beer_name), info_abv
FROM beers, info
WHERE beers.info_id = info.info_id
AND info_abv IS NOT NULL
ORDER BY info_abv DESC
'''
query_2 = '''
CREATE VIEW CountByCountry AS
SELECT TRIM(place_country), COUNT(*)
FROM beers, place
WHERE beers.place_id = place.place_id
GROUP BY place_country
'''
query_3 = '''
CREATE VIEW Average AS
SELECT TRIM(place_country), SUM(info_abv) / COUNT(*)
FROM place, info, beers
WHERE beers.info_id = info.info_id 
AND beers.place_id = place.place_id
AND info_abv IS NOT NULL
GROUP BY place_country
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
with conn:
    cur = conn.cursor()

    cur.execute('DROP VIEW IF EXISTS ByInfoAbv')
    cur.execute(query_1)
    cur.execute('SELECT * FROM ByInfoAbv')
    b_name = []
    i_abv = []

    for row in cur:
        b_name.append(row[0])
        i_abv.append(row[1])

    fig, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)

    bar_ax.set_title('Статистика за міцністю пива')
    bar = bar_ax.bar(b_name, i_abv)
    bar_ax.set_xticks([])                            # без назв бо їх дуже багато
    bar_ax.yaxis.set_major_locator(ticker.MultipleLocator(1))


    cur.execute('DROP VIEW IF EXISTS CountByCountry')
    cur.execute(query_2)
    cur.execute('SELECT * FROM CountByCountry')
    p_country = []
    count = []

    for row in cur:
        p_country.append(row[0])
        count.append(row[1])

    top_5 = []
    for i in range(len(p_country)):
        if i < 5:   # заповнимо список першими 5 значеннями (шостим будуть сума всіх інших)
            top_5.append([p_country[i], count[i]])

        else:
            if i == 5:
                top_5.append(["Other", 0])  # додаємо останній елемент

            if count[i] > min([el[1] for el in top_5[0:-1]]):  # перевіряємо чи кількість більша за вже записані
                index_el = [el[1] for el in top_5[0:-1]].index( min([el[1] for el in top_5[0:-1]]) )  # визначаємо індекс мінімального елементу
                top_5[-1][1] += top_5[index_el][1]  # додаємо до Other елемент що забираємо з списку
                top_5[index_el] = [p_country[i], count[i]]  # замінюємо елемент

            else:
                top_5[-1][1] += count[i]  # додаємо до Other елемент що менший за всі в списку


    pie_ax.pie([el[1] for el in top_5], labels=[el[0] for el in top_5], autopct='%1.1f%%')
    pie_ax.set_title('Кількість різних пив у кожній країні (топ 5)')  # там малі числа, тому якщо більше буде нерозбірливо


    cur.execute('DROP VIEW IF EXISTS Average')
    cur.execute(query_3)
    cur.execute('SELECT * FROM Average')
    p_country = []
    average = []

    for row in cur:
        p_country.append(row[0])
        average.append(row[1])

    graph_ax.plot(p_country, average, marker='o')
    graph_ax.set_title('Cередня міцність пива в кожній країні')
    graph_ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    graph_ax.set_xticklabels(p_country, rotation=90, size=8)

plt.show()
