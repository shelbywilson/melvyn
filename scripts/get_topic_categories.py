from bs4 import BeautifulSoup
import urllib.request
import json
import re
import wikipedia
# from create_topic_category_page import create_topic_category_page 
# from create_guest_pages import create_guest_pages 

def split_century_phrase(phrase):
    # Define the regular expression pattern for matching "n-century something"
    pattern = r'^(\d{1,2}[-\s]century)\s(.+)$'

    # Use re.match to check if the phrase matches the pattern
    match = re.match(pattern, phrase)
    
    if match:
        # Extract and return the two parts
        century_part = match.group(1)
        something_part = match.group(2)
        return (century_part, something_part)
    else:
        # Return None if the pattern doesn't match
        return None

def get_topic_categories():
    print('\n### start get_topic_categories')
    f = open('./../data/episodes.json')
    episodes = json.load(f)
    f.close()

    f = open('./../data/topics_by_category.json')
    dictionary = json.load(f)
    f.close()

    f = open('./../data/categories_by_episode.json')
    categories_by_episode = json.load(f)
    f.close()

    try:
        f = open('./../data/category_summaries.json')
        category_summaries = json.load(f)
        f.close()
    except:
        category_summaries = {}


    # dictionary = {}
    # categories_by_episode = {}
    i = 0

    for episode in episodes:
        # if (i < 10):
        if (episode['topic'] not in categories_by_episode):
            categories_by_episode[episode['topic']] = []
            if (episode['wiki_link'] != ""):
                # if episode['topic'] not in categories_by_episode:
                #     print('new episode', episodes['topic'])
                try:
                    html_page = urllib.request.urlopen(episode['wiki_link'])
                    soup = BeautifulSoup(html_page, "html.parser")
                    categories = soup.find('div', {'id': "mw-normal-catlinks"}).find_all('li')
                    for category in categories:
                        cat_name = category.get_text() 
                        century_phrase = split_century_phrase(cat_name)
                        
                        if (century_phrase):
                            if (century_phrase[0] not in dictionary):
                                dictionary[century_phrase[0]] = []
                            if (century_phrase[1] not in dictionary):
                                dictionary[century_phrase[1]] = []
                            dictionary[century_phrase[0]].append(episode['topic'])
                            dictionary[century_phrase[1]].append(episode['topic'])
                        else:
                            if (cat_name not in dictionary):
                                dictionary[cat_name] = []
                            dictionary[cat_name].append(episode['topic'])

                    print('\tcategories for', episode['topic'])
                except:
                    print('\tno categories', episode['topic'])
        i += 1
        # else:
            # print('\t--', 'no wiki link', episode['topic'])
    print('\t', len(dictionary.keys()), 'categories')

    for topic in dictionary:
        dictionary[topic] = list(set(dictionary[topic]))
        
    w = open('./../data/topics_by_category.json', 'w')
    json.dump(dictionary, w, indent=4, ensure_ascii=False)
    w.close()

    print('\twrite topics_by_category.json')

    # frequency distribution
    # distribution = {}
    # for key in sorted(dictionary.keys(), key=sort_by_frequency, reverse=True):
        # length = len(dictionary[key])
        # if length not in distribution:
        #     distribution[length] = []
        # distribution[length].append(key)

    # print(sorted(distribution.keys(), reverse=True), distribution)

    # get meaningful categories
    def sort_by_frequency(key):
        return len(dictionary[key])
    non_unique_categories = {}
    for key in sorted(dictionary.keys(), key=sort_by_frequency, reverse=True):
        if len(dictionary[key]) >= 2 and (not re.search('[0-9]+ deaths', key)) and (not re.search('[0-9]+ births', key)):
            non_unique_categories[key] = dictionary[key]

            # get wikipedia summaries
            if key not in category_summaries:
                print('\t new category', key)
                try:
                    summary = wikipedia.summary(key, sentences=2)
                    if not summary.startswith("This is a list"):
                        category_summaries[key] = summary
                        print('\n\t', len(category_summaries.keys()), key, '\n\t\t', summary)
                    else:
                        print('\n\t', len(category_summaries.keys()), key, '\n\t\t list --skip')
                except:
                    category_summaries[key] = ''
                    print('\n\t', len(category_summaries.keys()), key, '\n\t\t', category_summaries[key])

    # combine topics with same sets of episodes
    combine = []
    i = 0
    for key1 in non_unique_categories.keys():
        j = 0
        new_set = {key1}
        for key2 in non_unique_categories.keys():
            if (key1 != key2) and j > i:
                if set(non_unique_categories[key1]) == set(non_unique_categories[key2]):
                    # print('equal', key1, key2)  
                    new_set.add(key2)
            j += 1
        if len(new_set) > 1:
            is_not_super_set = True
            for super_set in combine:
                if (super_set.issuperset(new_set)):
                    is_not_super_set = False
                    break
            if is_not_super_set:
                combine.append(new_set)
        i += 1
    for equal_set in combine:
        i = 0
        new_key = ''
        for topic in equal_set:
            new_key += topic + ', '
            if (i == 0):
                episodes = non_unique_categories[topic]
            # remove redundant category
            non_unique_categories.pop(topic)
        
        new_key = new_key[:len(new_key) - 2]
        print('\tcombined category', new_key)
        non_unique_categories[new_key] = episodes

    for key in non_unique_categories:
        for episode in non_unique_categories[key]:
            if episode not in categories_by_episode:
                categories_by_episode[episode] = []
            categories_by_episode[episode].append(key)

    print('\t', len(combine), 'combined categories')
    print('\t', len(non_unique_categories.keys()), 'non-unique categories')

    w = open('./../data/category_summaries.json', 'w')
    json.dump(category_summaries, w, indent=4, ensure_ascii=False)
    w.close()

    w = open('./../data/topics_by_category_non_unique.json', 'w')
    json.dump(non_unique_categories, w, indent=4, ensure_ascii=False)
    w.close()
      
    for ep in categories_by_episode:
        categories_by_episode[ep] = list(set(categories_by_episode[ep]))

    w = open('./../data/categories_by_episode.json', 'w')
    json.dump(categories_by_episode, w, indent=4, ensure_ascii=False)
    w.close()

    # create_guest_pages()
    # create_topic_category_page()

    print('### end get_topic_categories')

if __name__=="__main__":
    get_topic_categories()
