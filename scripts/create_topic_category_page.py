import json
import re
from html_util import get_html_page, get_url, div, li, p, a, get_episode_row, get_wiki_img
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

    f = open('./../data/top_level_categories_by_episode.json')
    top_level_categories_by_episode = json.load(f)
    f.close()

    f = open('./../data/top_level_categories.json')
    top_level_categories = json.load(f)
    f.close()

    f = open('./../data/category_summaries.json')
    category_summaries = json.load(f)
    f.close()

    try:
        f = open('./../data/category_summaries_manual.json')
        category_summaries = {**category_summaries, **json.load(f)}
        f.close()
    except FileNotFoundError:
        pass

    f = open('./../data/episodes_dictionary.json')
    episodes_dictionary = json.load(f)
    f.close()

    index_html = get_header_html('All categories')

    def sort_by_len(key):
        if key in top_level_categories:
            # Sort top-level categories to the beginning
            return (-10000, key)  # Use 0 for top-level categories to ensure they come first
        try:
            return (-len(topics_by_category[key]), key)  # Negative length for descending sort, key for alphabetical
        except KeyError:
            # If the key is not found, we still want to prioritize top-level categories
            return (1, key)  # Use 1 for non-top-level categories
    
    # create top level category pages
    for key in top_level_categories:
        links_to_other_top_levels = ''
        for other in top_level_categories:
            if (other != key):
                links_to_other_top_levels += a(other, './../category/' + get_url(other) + '.html',  '', False)
        
        tl_cat_html = get_header_html(key, p("This is a top level category. The other top level categories are:" + div(links_to_other_top_levels, 'categories')))

        tl_cat_html += p(str(len(top_level_categories[key])) + ' episodes')
        episode_list = ''

        for episode in top_level_categories[key]:
            try: 
                episode_list += get_episode_row(episode)
            except:
                print("difference in bbc/wikipedia title, bbc title to be normalized:", episode)

        tl_cat_html +=  '<ol id="episodes">' + episode_list + '</ol>'

        w = open('./../category/' + get_url(key) + '.html', 'w')
        w.write(get_html_page(tl_cat_html, key, ['guest', 'category'], ['util', 'add-episode-scores']))
        w.close()

    # create other category pages
    for key in sorted(topics_by_category, key=sort_by_len):
        if (key in top_level_categories):
            continue
        category_inner = ''
    
        try:
            if category_summaries[key]:
                category_inner += div(p(category_summaries[key]), "category-summary")
        except:
            pass

        category_inner += p(str(len(topics_by_category[key])) + ' episodes')
        
        category_inner += '<div class="header__all-imgs">\n'
        for topic in sorted(topics_by_category[key]):
            try:
                episode = episodes_dictionary[topic]
                category_inner += a(get_wiki_img(episode['topic']), episode['wiki_link'])
            except:
                print('\tno episode found -', topic)
        category_inner += '\n</div>'

        episode_list = ''
        index_page_detail = ''
        related_categories = set()
        related_html = ''

        for episode in sorted(topics_by_category[key]):
            episode_list += get_episode_row(episode)
            links = ''
            try:
                if (episodes_dictionary[episode]["wiki_link"]):
                    links += a("wikipedia", episodes_dictionary[episode]["wiki_link"], False)
                if (episodes_dictionary[episode]["episode_link"]): 
                    links += a("listen", episodes_dictionary[episode]["episode_link"], False)
                index_page_detail += li(episode + links)
            except:
                print('\tno episode found -', episode)

            # add categories of each episode to set
            for cat in categories_by_episode[episode]:
                if cat != key:
                    related_categories.add(cat)

            #  add top level categories as well
            try:
                for cat in top_level_categories_by_episode[episode]:
                    related_categories.add(cat)
            except: 
                # print("can't find", episode)
                pass
       
        for cat in sorted(related_categories, key=sort_by_len):
            related_html += a(cat, './../category/' + get_url(cat) + '.html', '', False)

        if (len(related_categories) > 0):
            category_inner += '<p style="margin-bottom: -1rem">Episodes in this category also belong to the following categories:</p>\n'
        category_inner += div(related_html, 'categories')

        category_html = get_header_html(key, category_inner)

        category_html += '<ol id="episodes">\n' + episode_list + '\n</ol>'

        index_html += '<details>\n<summary>\n' + key + ' (' + str(len(topics_by_category[key])) + ')\n</summary>' 
        index_html += '<h2>' + (a(key, './../category/' + get_url(key) + '.html', '', False)) + '</h2><ol>' + index_page_detail + '</ol></details>'

        w = open('./../category/' + get_url(key) + '.html', 'w')
        w.write(get_html_page(category_html, key, ['guest', 'category'], ['util', 'add-episode-scores']))
        w.close()
    
    print('\t', len(topics_by_category.keys()), 'category pages written')

    w = open('./../category/index.html', 'w')
    w.write(get_html_page(index_html, 'episode categories', ['category']))
    w.close()

    # create custom tag pages
    try:
        with open('./../data/custom_tags_by_episode.json') as f:
            custom_tags_by_episode = json.load(f)
    except FileNotFoundError:
        custom_tags_by_episode = {}

    topics_by_tag = {}
    for topic, tags in custom_tags_by_episode.items():
        for tag in tags:
            topics_by_tag.setdefault(tag, []).append(topic)

    # Build full ordered century list: BC centuries in data + all AD 1st–21st
    century_re = re.compile(r'^(\d+)(?:st|nd|rd|th) century( BC)?$')
    def century_sort_key(tag):
        m = century_re.match(tag)
        n, bc = int(m.group(1)), bool(m.group(2))
        return -n if bc else n + 1000
    bc_centuries = sorted([t for t in topics_by_tag if century_re.match(t) and 'BC' in t], key=century_sort_key)

    def ordinal(n):
        suffix = 'th' if 10 <= n % 100 <= 20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')
        return f'{n}{suffix}'
    ad_centuries = [f'{ordinal(n)} century' for n in range(1, 22)]
    all_centuries = bc_centuries + ad_centuries

    def short_century_label(tag):
        m = century_re.match(tag)
        n, bc = m.group(1), bool(m.group(2))
        return f'{n}BC' if bc else f'{n}AD'

    def get_century_timeline(active_tag):
        html = '<nav class="century-timeline">'
        for i, tag in enumerate(all_centuries):
            count = len(topics_by_tag.get(tag, []))
            classes = 'tl-dot'
            if tag == active_tag:
                classes += ' tl-dot--active'
            if count == 0:
                classes += ' tl-dot--empty'
            count_html = f'<span class="tl-count">{count}</span>'
            circle_html = '<span class="tl-dot-circle"></span>'
            lbl_html = f'<span class="tl-label">{short_century_label(tag)}</span>'
            inner = count_html + circle_html + lbl_html
            if tag == active_tag:
                html += f'<span class="{classes}" title="{tag}">{inner}</span>'
            else:
                html += f'<a href="./../category/{get_url(tag)}.html" class="{classes}" title="{tag}">{inner}</a>'
            if i < len(all_centuries) - 1:
                html += '<span class="tl-line"></span>'
        html += '</nav>'
        return html

    pages_written = 0
    all_tags = set(topics_by_tag.keys()) | set(all_centuries)
    for tag in sorted(all_tags):
        topics = topics_by_tag.get(tag, [])
        is_century = bool(century_re.match(tag))

        episode_list = ''
        for topic in sorted(topics):
            episode_list += get_episode_row(topic)

        tag_label = tag[0].upper() + tag[1:] if not is_century else tag
        tag_html = get_header_html(tag_label)
        if is_century:
            tag_html += get_century_timeline(tag)
        tag_html += p(str(len(topics)) + ' episodes')
        if episode_list:
            tag_html += '<ol id="episodes">\n' + episode_list + '\n</ol>'

        w = open('./../category/' + get_url(tag) + '.html', 'w')
        w.write(get_html_page(tag_html, tag_label, ['guest', 'category'], ['util', 'add-episode-scores']))
        w.close()
        pages_written += 1

    print('\t', pages_written, 'custom tag pages written')
    print('### end create_topic_category_page')

def get_header_html(title, inner = ''):
    html = '<header>'
    html += '''
        <a href="./../" class="header__home-icon">
            <img src="./../client/lord-bragg.jpg"
                alt="Portrait of Lord Melvyn Bragg, host of In Our Time" />
        </a>
    '''
    html += p(a('list', "./../", '', False) + a('world', "./../world.html", '', False) + a('about', 'https://github.com/shelbywilson/melvyn', '', True), 'header__home-links')
    html += p(a('&larr; back', "javascript:history.back()", '', False), 'header__back-link')
    html += '<h1>' + title + '</h1>\n'
    html += inner
    html += '\n</header>'
    return html

if __name__=="__main__":
    create_topic_category_page()
