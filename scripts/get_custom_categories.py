import json
import re

CENTURY_RE = re.compile(r'\b(\d+)(?:st|nd|rd|th)[\s-]century\b(?:\s+BC)?', re.IGNORECASE)
BC_RE = re.compile(r'\b(\d+)(?:st|nd|rd|th)[\s-]century\s+BC\b', re.IGNORECASE)

def century_label(n, bc=False):
    n = int(n)
    suffix = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suffix} century BC' if bc else f'{n}{suffix} century'

def get_custom_categories():
    print('\n### start get_custom_categories')

    with open('./../data/episodes_min.json') as f:
        episodes = json.load(f)
    with open('./../data/categories_by_episode.json') as f:
        categories_by_episode = json.load(f)
    with open('./../config/custom_category_patterns.json') as f:
        patterns = json.load(f)
    try:
        with open('./../data/custom_tags_manual.json') as f:
            manual = json.load(f)
    except FileNotFoundError:
        manual = {}

    result = {}
    for ep in episodes:
        topic = ep['topic']
        topic_lower = topic.lower()
        ep_cats = categories_by_episode.get(topic, [])
        cats_text = ' '.join(ep_cats)

        tags = set()

        # Pattern-based tags
        cats_lower = cats_text.lower()
        for tag, matchers in patterns.items():
            if any(kw in cats_lower for kw in matchers.get('category', [])):
                tags.add(tag)
            if any(re.search(r'\b' + re.escape(kw) + r'(?:es|s)?\b', topic_lower) for kw in matchers.get('topic', [])):
                tags.add(tag)

        # Century extraction from Wikipedia categories and episode title
        search_text = cats_text + ' ' + topic
        bc_centuries = {int(m.group(1)) for m in BC_RE.finditer(search_text)}
        all_centuries = {int(m.group(1)) for m in CENTURY_RE.finditer(search_text)}
        ad_centuries = all_centuries - bc_centuries
        for n in bc_centuries:
            tags.add(century_label(n, bc=True))
        for n in ad_centuries:
            tags.add(century_label(n))

        # Manual overrides
        for tag in manual.get(topic, []):
            tags.add(tag)

        if tags:
            result[topic] = sorted(tags)

    with open('./../data/custom_tags_by_episode.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f'\t{len(result)} episodes tagged')
    print('### end get_custom_categories')

if __name__ == '__main__':
    get_custom_categories()
