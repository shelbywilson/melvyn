import json
from html_util import get_html_page, get_url, div, li, p, a, get_episode_row
import os
import glob

files = glob.glob('./category/*')
for f in files:
    os.remove(f)

def create_topic_category_page():
    print('\n### start create_topic_category_page')
    f = open('./../data/topics_by_category_non_unique.json')
    topics_by_category = json.load(f)
    f.close()

    f = open('./../data/categories_by_episode.json')
    categories_by_episode = json.load(f)
    f.close()

    f = open('./../data/category_summaries.json')
    category_summaries = json.load(f)
    f.close()

    f = open('./../data/episodes_dictionary.json')
    episodes_dictionary = json.load(f)
    f.close()

    index_html = '<header>'
    index_html += p(a('home', "/", '', False) + a('world', "/world.html", '', False) + a('all guests', "/guest/", '', False) + a('about', 'https://github.com/shelbywilson/melvyn', '', True), 'header__home-links')
    index_html += p(a('&larr; back', "javascript:history.back()", '', False), 'header__back-link')
    index_html += '<h1>All categories</h1>'
    index_html += '</header>'

    def sort_by_len(key):
        return len(topics_by_category[key])

    for key in sorted(topics_by_category.keys(), key=sort_by_len, reverse=True):
        category_html = '<header>' 
        # category_html += a('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Official_portrait_of_Lord_Bragg_crop_2.jpg/440px-Official_portrait_of_Lord_Bragg_crop_2.jpg" alt="Portrait of Lord Melvyn Bragg, host of In Our Time" />', '/', 'home-link', False)
        category_html += p(a('home', "/", '', False) + a('world', "/world.html", '', False) + a('all guests', "/guest/", '', False) + a('about', 'https://github.com/shelbywilson/melvyn', '', True), 'header__home-links')
        category_html += p(a('&larr; back', "javascript:history.back()", '', False), 'header__back-link')
        category_html += '<h1>' + key + '</h1>'
    
        try:
            category_html += div(p(category_summaries[key]), "category-summary")
        except:
            pass

        category_html += p(str(len(topics_by_category[key])) + ' episodes')

        episode_list = ''
        index_page_detail = ''
        related_categories = set()
        for topic in sorted(topics_by_category[key]):
            episode_list += get_episode_row(topic)
            links = ''
            if (episodes_dictionary[topic]["wiki_link"]):
                links += a("wikipedia", episodes_dictionary[topic]["wiki_link"], False)
            if (episodes_dictionary[topic]["episode_link"]): 
                links += a("listen", episodes_dictionary[topic]["episode_link"], False)
            index_page_detail += li(topic + links)
            for cat in categories_by_episode[topic]:
                if cat != key:
                    related_categories.add(cat)

        related_html = ''
        for cat in sorted(related_categories, key=sort_by_len, reverse=True):
            related_html += a(cat, './../category/' + get_url(cat) + '.html', '', False)

        if (len(related_categories) > 0):
            category_html += '<p style="margin-bottom: -1rem">Episodes in this category also belong to the following categories:</p>'
        category_html += div(related_html, 'categories')
        category_html += '</header>' 

        category_html += '<ol id="episodes">' + episode_list + '</ol>'

        index_html += '<details><summary>' + key + ' (' + str(len(topics_by_category[key])) + ')</summary>' 
        index_html += '<h2>' + (a(key, './../category/' + get_url(key) + '.html', '', False)) + '</h2><ol>' + index_page_detail + '</ol></details>'

        w = open('./../category/' + get_url(key) + '.html', 'w')
        w.write(get_html_page(category_html, key, ['guest', 'category'], ['util', 'add-episode-scores']))
        w.close()
    
    print('\t', len(topics_by_category.keys()), 'category pages written')

    w = open('./../category/index.html', 'w')
    w.write(get_html_page(index_html, 'episode categories', ['category']))
    w.close()

    print('### end create_topic_category_page')

if __name__=="__main__":
    create_topic_category_page()