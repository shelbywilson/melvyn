from bs4 import BeautifulSoup
import urllib.request
import json
# from util import parse_page

f = open('./data/episodes.json')

data = json.load(f)
f.close()

descriptions = {}

for episode in data:
    html_page = urllib.request.urlopen('https://www.bbc.co.uk/programmes/' + episode['episode_link'].split('/').pop())
    soup = BeautifulSoup(html_page, "html.parser")
    short_desc = ''
    long_desc = ''

    print(episode['topic'])
    try:
        short_desc = soup.find('div', {'class': "synopsis-toggle__short"}).find('p').get_text()
    except:
        print('\tcannot find short description', episode['episode_link'])

    try:
        long_desc = soup.find('div', {'class': "synopsis-toggle__long"}).get_text()
    except:
        print('\tcannot find long description', episode['episode_link'])


    descriptions[episode['date'] + '_' + episode['topic']] = { 'short_desc': short_desc, 'long_desc': long_desc}

w = open('./data/bbc_descriptions.json', 'w')
json.dump(descriptions, w, indent=4, ensure_ascii=False)
w.close()

short_descriptions = {}
for key in descriptions.keys():
    short_descriptions[key] = descriptions[key]['short_desc']

w = open('./data/bbc_descriptions_short.json', 'w')
json.dump(short_descriptions, w, indent=4, ensure_ascii=False)
w.close()