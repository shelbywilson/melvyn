from itertools import combinations
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
    guest_combinations = {}

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

        names = [entry['name'] for entry in episode['experts']]

        # Generating all combinations of two names
        combinations_of_two = list(combinations(names, 2))
        for combo in combinations_of_two:
            key = combo[0] + '_' + combo[1]

            if (combo not in guest_combinations):
                guest_combinations[key] = {
                    "guests": combo,
                    "count": 1
                }
            else:
                guest_combinations[key]["count"] += 1
                print('repeat guest combo!', combo)

    keys_to_delete = [combo for combo in guest_combinations if guest_combinations[combo]["count"] == 1]
    for key in keys_to_delete:
        del guest_combinations[key]

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

    w = open('./../data/guest_combinations.json', 'w')
    json.dump(guest_combinations, w, indent=4, ensure_ascii=False)
    w.close()

    print('\n### end guest_analysis')

if __name__ == "__main__":
    guest_analysis()