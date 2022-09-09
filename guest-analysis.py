from bs4 import BeautifulSoup
import urllib.request
import json

f = open('./data/episodes.json')
data = json.load(f)
f.close()

f = open('./data/bbc_descriptions_short.json')
descriptions = json.load(f)
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

        if (guest['name'] not in topics_by_guest):
            topics_by_guest[guest['name']] = [ {'topic': episode['topic'], 'date': episode['date'], 'episode_link': episode['episode_link'] }]
        else:
            topics_by_guest[guest['name']].append({'topic': episode['topic'], 'date': episode['date'], 'episode_link': episode['episode_link'] })

for guest in frequency.keys():
    el = frequency[guest].copy()
    el['name'] = guest
    frequency_min[guest] = el['count']
    guest_html = ''
    try:
        if el['links'][0]['text'] == guest:
            print('wiki link ')
            guest_html += '<h1><a href="' + el['links'][0]['wiki'] + '" target="_blank">' + guest + ' &nearr;</a></h1>'
        else:
            guest_html += '<h1>' + guest + '</h1>'
    except: 
        guest_html += '<h1>' + guest + '</h1>'

    guest_html += '<em>' + frequency[guest]['title'][0] + '</em>'
    guest_html += '<h2>Episodes</h2><ol>'
    for topic in topics_by_guest[guest]:
        desc = descriptions[topic['date'] + '_' + topic['topic']]
        guest_html += '<li><a href="https://www.bbc.co.uk/sounds/play/' + topic['episode_link'].split('/').pop() + '" target="_blank">' + topic['topic'] + '&nearr;</a><p>' + desc + '</p></li>'
    guest_html += '</ol>'

    ranked_frequency.append(el)
    
    w = open('./guests/' + guest.replace(' ', '_') + '.html', 'w')
    w.write('<!DOCTYPE html><html lang="en"><head><meta http-equiv="Content-Type"content="text/html; charset=UTF-8" /><link rel="stylesheet" type="text/css" href="./../main.css" /><meta http-equiv="X-UA-Compatible" content="IE=edge" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="robots" content="index,follow" /><meta name="googlebot" content="index,follow" /><meta property="og:title" content="' + guest +'" /><meta property="og:description" content="" /><meta name="theme-color" content="#000"><title>' + guest + '</title><link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Official_portrait_of_Lord_Bragg_crop_2.jpg/440px-Official_portrait_of_Lord_Bragg_crop_2.jpg" /></head><body><main>' + guest_html + '</main></body></html>')
    w.close()
    

def get_count(element):
    return element['count']

ranked_frequency.sort(reverse=True, key=get_count)

w = open('./data/guest_frequency.json', 'w')
json.dump(frequency, w, indent=4, ensure_ascii=False)
w.close()

w = open('./data/guest_frequency_min.json', 'w')
json.dump(frequency_min, w, indent=4, ensure_ascii=False)
w.close()

w = open('./data/ranked_guest_frequency.json', 'w')
json.dump(ranked_frequency, w, indent=4, ensure_ascii=False)
w.close()

w = open('./data/topics_by_guest.json', 'w')
json.dump(topics_by_guest, w, indent=4, ensure_ascii=False)
w.close()