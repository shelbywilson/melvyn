from bs4 import BeautifulSoup
import urllib.request
import json
# import datefinder
# from geotext import GeoText
import re

f = open('./../data/bbc_descriptions.json')
descriptions = json.load(f)
f.close()

f = open('./../data/episodes.json')
episodes = json.load(f)
f.close()

# for key in descriptions.keys():
#     places = GeoText(descriptions[key]['short_desc'])
#     cities = list(places.country_mentions)
#     print(descriptions[key]['short_desc'])
#     print('\t', cities)
#     desc = descriptions[key]['long_desc']
#     matches = datefinder.find_dates(desc, True)
#     for match in matches:
#         print(key, match, desc)


dictionary = {}

for episode in episodes:
    for guest in episode['experts']:
        # try: 
            # print(guest['title'], '\n\t', re.search(r'(.*?) of (.+)(,| at| in)?', guest['title']).group(2))
            # print(guest['title'], '\n\t', re.search(r' at (the)? (.*?) for (.*)(,| at| in)?', guest['title']))
        # except:
        #     continue
        try:
            # print(guest['name'], '\n\t', guest['title'], '\n\t', re.search(r' of (.*?)( at|,)', guest['title']).group(1))
            key = re.search(r' of (.*?)( at|,)', guest['title']).group(1)
            name_title = guest['name'] + '___' + guest['title']
            try:
                if not name_title in dictionary[key]:
                    dictionary[key].append(name_title)
            except:
                dictionary[key] = [name_title]
        except:
            print('-- not found --', guest['name'], ': ', guest['title'])

        # for word in guest['title'].split(' '):
        #     if word != 'and' and word != 'the' and word != 'a' and word != 'an' and word != 'of' and word != 'in' and word != 'at' and word != 'for':
        #         try:
        #             dictionary[word] += 1
        #         except:
        #             dictionary[word] = 1

w = open('./../data/guest_areas_of_expertise.json', 'w')
json.dump(dictionary, w, indent=4, ensure_ascii=False)
w.close()
        # if ('at' in guest['title'] or ', ' in guest['title']):
        #     print(guest['name'])
        #     if ('Professor of' in guest['title']):
        #         print('\t', re.search(r'Professor of (.*?)( at|,)', guest['title']).group(1))
        #     elif ('Professor and' in guest['title']):
        #         print('\t', re.search(r'Professor and (.*?) of (.*?)( at|,)', guest['title']).group(2))