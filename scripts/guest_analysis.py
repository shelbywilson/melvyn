from bs4 import BeautifulSoup
import urllib.request
import json

def guest_analysis():
    print('\n### start guest_analysis')
    f = open('./../data/episodes.json')
    data = json.load(f)
    f.close()

    frequency = {}
    frequency_min = {}
    ranked_frequency = []
    topics_by_guest = {}

    for episode in data:
        for guest in episode['experts']:
            if (guest['name'] not in frequency):
                # print(guest['name'])
                frequency[guest['name']] = { 'count': 1, 'first': episode['date'], 'last': episode['date'], 'links': guest['links'], 'title': [guest['title']] }
            else: 
                frequency[guest['name']]['count'] += 1
                frequency[guest['name']]['first'] = episode['date']
                if (guest['title'] not in frequency[guest['name']]['title']):
                    frequency[guest['name']]['title'].append(guest['title'])
                    # print('different title', guest['name'], guest['title'], frequency[guest['name']]['title'])

            entry = {'topic': episode['topic'], 'wiki_link': episode['wiki_link'], 'title': guest['title'], 'date': episode['date'], 'episode_link': episode['episode_link'] }
            if (guest['name'] not in topics_by_guest):
                topics_by_guest[guest['name']] = [entry]
            else:
                topics_by_guest[guest['name']].append(entry)

    for guest in frequency.keys():
        frequency_min[guest] = frequency[guest]['count']

    def get_count(element):
        return element['count']

    ranked_frequency.sort(reverse=True, key=get_count)

    w = open('./../data/guest_frequency.json', 'w')
    json.dump(frequency, w, indent=4, ensure_ascii=False)
    w.close()

    w = open('./../data/guest_frequency_min.json', 'w')
    json.dump(frequency_min, w, ensure_ascii=False)
    w.close()

    w = open('./../data/ranked_guest_frequency.json', 'w')
    json.dump(ranked_frequency, w, indent=4, ensure_ascii=False)
    w.close()

    w = open('./../data/topics_by_guest.json', 'w')
    json.dump(topics_by_guest, w, indent=4, ensure_ascii=False)
    w.close()

    print('\n### end guest_analysis')