import requests
import bs4
import sqlite3
import re

db = sqlite3.connect('anecdotes.db')
cur = db.cursor()
cur.executescript('''create table anecdotes(
                     id integer primary key, topic integer, anecdote longtext);''')
topics = {1: 'anekdoti_aforizmi', 2: 'anekdoti_starie-i-borodatie',
          3: 'anekdoti_sovetskie', 4: 'anekdoti_skazochnie',
          5: 'anekdoti_pro-shtirlitsa', 6: 'anekdoti_pro-programmistov',
          7: 'anekdoti_dorognie-pro-dorogu', 8: 'anekdoti_pro-druzey',
          9: 'anekdoti_pro-studentov', 10: 'anekdoti_pro-militsiyu',
          11: 'anekdoti_shkolnie-i-pro-shkolu', 12: 'anekdoti_meditsinskie',
          13: 'anekdoti_pro-detey', 14: 'anekdoti_pro-semyu',
          15: 'anekdoti_pro-sport-pro-futbol', 16: 'anekdoti_Pro-reklamu',
          17: 'anekdoti_pro-givotnih', 18: 'anekdoti_pro-armiu',
          19: 'anekdoti_po-shou-biznes', 20: 'anekdoti_kriminalnie',
          21: 'anekdoti_pro-kino', 22: 'anekdoti_pro-kompyuteri',
          23: 'anekdoti_pro-alkogolikov', 24: 'anekdoti_pro-narkomanov',
          25: 'anekdoti_pro-sudey', 26: 'anekdoti_pro-buhgalterov',
          27: 'anekdoti_pro-billa-geytsa', 28: 'anekdoti_raznie'}


def add_topic(topic):
    request = requests.get('http://anekdotme.ru/' + topics[topic])
    texts = (bs4.BeautifulSoup(request.text,
                               'html.parser')).select('.anekdot_text')
    for anec in texts:
        text = anec.getText().strip()
        text = (re.compile('a-zA-Zа-яА-я .,$@!%:;()*-"]')).sub(' ', text)
        insert_query = '''INSERT INTO anecdotes (topic, anecdote) 
                                VALUES (?,?) '''
        record = (topic, text)
        cur.execute(insert_query, record)
        db.commit()


for i in range(1, 29):
    add_topic(i)

db.close()
