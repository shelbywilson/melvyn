from bs4 import BeautifulSoup
import urllib.request
import json
# from util import parse_page

# f = open('../data/recommendations.json')

# data = json.load(f)
# f.close()

html_page = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_In_Our_Time_programmes')
soup = BeautifulSoup(html_page, "html.parser")
rows = soup.findAll('tr')
episodes = []
for row in rows:
    i = 0
    date = ''
    episode_link = ''
    topic = ''
    wiki_link = ''
    experts = []
    for col in row.findAll('td'):
        if (i == 0):
            date = col.get_text().strip()
            if (col.find('a')):
                episode_link = col.find('a').get('href')
        if (i == 1):
            topic = col.get_text().strip()
            if (col.find('a')):
                wiki_link = 'https://en.wikipedia.org' + col.find('a').get('href')
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
        i += 1
    if topic != "" and episode_link != "":
        episodes.insert(0, { 'date': date, 'episode_link': episode_link, 'topic': topic, 'wiki_link': wiki_link, 'experts': experts })

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

w = open('./data/episodes.json', 'w')
json.dump(episodes, w, indent=4, ensure_ascii=False)
w.close()