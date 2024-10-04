from itertools import combinations
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
            guest_name = guest['name']
            guest_title = guest['title']
            
            if guest_name not in frequency:
                frequency[guest_name] = {
                    'count': 1,
                    'first': episode['date'],
                    'last': episode['date'],
                    'links': guest['links'],
                    'title': [guest_title]
                }
            else:
                frequency[guest_name]['count'] += 1
                frequency[guest_name]['last'] = episode['date']
                if guest_title not in frequency[guest_name]['title']:
                    frequency[guest_name]['title'].append(guest_title)

            entry = {
                'topic': episode['topic'],
                'wiki_link': episode['wiki_link'],
                'title': guest_title,
                'date': episode['date'],
                'episode_link': episode['episode_link']
            }
            if guest_name not in topics_by_guest:
                topics_by_guest[guest_name] = [entry]
            else:
                topics_by_guest[guest_name].append(entry)

        names = [guest['name'] for guest in episode['experts']]
        combinations_of_two = list(combinations(names, 2))

        for combo in combinations_of_two:
            key = '_'.join(combo)  # use join for better key management

            if key not in guest_combinations:
                guest_combinations[key] = {
                    "guests": combo,
                    "count": 1
                }
            else:
                guest_combinations[key]["count"] += 1
                print('repeat guest combo!', combo)
            
    # remove combinations that occurred only once
    guest_combinations = {k: v for k, v in guest_combinations.items() if v["count"] > 1}

    frequency_min = {guest: freq['count'] for guest, freq in frequency.items()}

    ranked_frequency = sorted(frequency.values(), key=lambda x: x['count'], reverse=True)
    
    with open('./../data/guest_frequency.json', 'w', encoding='utf-8') as w:
        json.dump(frequency, w, indent=4, ensure_ascii=False)

    with open('./../data/guest_frequency_min.json', 'w', encoding='utf-8') as w:
        json.dump(frequency_min, w, ensure_ascii=False)

    with open('./../data/ranked_guest_frequency.json', 'w', encoding='utf-8') as w:
        json.dump(ranked_frequency, w, indent=4, ensure_ascii=False)

    with open('./../data/topics_by_guest.json', 'w', encoding='utf-8') as w:
        json.dump(topics_by_guest, w, indent=4, ensure_ascii=False)

    with open('./../data/guest_combinations.json', 'w', encoding='utf-8') as w:
        json.dump(guest_combinations, w, indent=4, ensure_ascii=False)

    print('\n### end guest_analysis')

if __name__ == "__main__":
    guest_analysis()
