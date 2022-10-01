from bs4 import BeautifulSoup
import urllib.request
import json

def get_episodes():
    print('\n### start get_episodes')
    html_page = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_In_Our_Time_programmes')
    soup = BeautifulSoup(html_page, "html.parser")
    rows = soup.findAll('tr')
    episodes = []
    episodes_min = []
    episodes_dictionary = {}
    for row in rows:
        i = 0
        date = ''
        episode_link = ''
        topic = ''
        wiki_link = ''
        experts = []
        experts_min = []
        for col in row.findAll('td'):
            if (i == 0):
                date = col.get_text().strip()
                if (col.find('a')):
                    episode_link = col.find('a').get('href')
            if (i == 1):
                topic = col.get_text().strip()
                if (col.find('a')):
                    partial = col.find('a').get('href')
                    if (partial.startswith('/')):
                        wiki_link = 'https://en.wikipedia.org' + col.find('a').get('href')
                else: 
                    wiki_link = ''
                    print('\t--- no wiki link', topic)
            if (i == 2):
                for li in col.findAll('li'):
                    name = li.get_text().split(',')[0]
                    links = []
                    try: 
                        title = li.get_text().replace(name + ',', '', 1).strip()
                    except:
                        title = ''
                    for a in li.find_all('a'):
                        links.append({ 'text': a.get_text(), 'wiki': 'https://en.wikipedia.org' + a.get('href') })
                    experts.append({ 'name': name, 'title': title, 'links': links })
                    experts_min.append({ 'name': name, 'title': title })
            i += 1
        if topic != "" and episode_link != "":
            ep = { 'date': date, 'episode_link': episode_link, 'topic': topic, 'wiki_link': wiki_link, 'experts': experts }
            episodes.insert(0, ep)
            episodes_min.insert(0, { 'date': date, 'episode_link': episode_link, 'topic': topic, 'wiki_link': wiki_link, 'experts': experts_min })
            episodes_dictionary[topic] = ep

    #     url = link.get('href')
    #     found = False
    #     print(url)
        # for item in data:
        #     if (item['url'] == url):
        #         found = True
        #         break
        # if not found:
        #     if (link.get('href').startswith('/people')):
        #         info = parse_page(url, link)

        #         data.insert(0, info)

    w = open('./../data/episodes.json', 'w')
    json.dump(episodes, w, indent=4, ensure_ascii=False)
    w.close()

    w = open('./../data/episodes_min.json', 'w')
    json.dump(episodes_min, w)
    w.close()

    w = open('./../data/episodes_dictionary.json', 'w')
    json.dump(episodes_dictionary, w)
    w.close()

    print('\n### end get_episodes')