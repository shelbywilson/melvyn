import json
import html as _html

PAGE_SIZE = 50

def create_index_page():
    print('\n### start create_index_page')

    with open('./../data/episodes_min.json') as f:
        episodes = json.load(f)
    with open('./../data/bbc_descriptions_short.json') as f:
        bbc_descriptions = json.load(f)
    with open('./../data/episode_thumbnails.json') as f:
        thumbnails = json.load(f)
    try:
        with open('./../data/episode_thumbnails_manual.json') as f:
            thumbnails = {**thumbnails, **json.load(f)}
    except FileNotFoundError:
        pass
    with open('./../data/guest_frequency_min.json') as f:
        guest_frequency = json.load(f)
    with open('./../data/categories_by_episode.json') as f:
        categories_by_episode = json.load(f)
    with open('./../data/top_level_categories_by_episode.json') as f:
        top_level_categories_by_episode = json.load(f)
    try:
        with open('./../data/custom_tags_by_episode.json') as f:
            custom_tags_by_episode = json.load(f)
    except FileNotFoundError:
        custom_tags_by_episode = {}
    with open('./../config/config.json') as f:
        config = json.load(f)

    v = config['FILE_VERSION']
    max_url = config['MAX_LENGTH_URL']
    episode_count = len(episodes)

    def get_url(name):
        return name.replace(' ', '_')[:max_url]

    def render_episode(ep):
        topic = ep['topic']
        date = ep['date']
        wiki_link = ep.get('wiki_link', '')
        episode_link = ep.get('episode_link', '')
        bbc_id = episode_link.split('/')[-1] if episode_link else ''
        description = bbc_descriptions.get(date + '_' + topic, '')
        thumb = thumbnails.get(topic)
        thumb_url = thumb.get('url', '') if isinstance(thumb, dict) else (thumb or '')
        thumb_w = thumb.get('width') if isinstance(thumb, dict) else None
        thumb_h = thumb.get('height') if isinstance(thumb, dict) else None

        experts = ep.get('experts', [])
        experts_html = ''
        for expert in experts:
            name = expert['name']
            title = expert.get('title', '')
            count = guest_frequency.get(name, 1)
            ep_label = 'episode' if count == 1 else 'episodes'
            experts_html += (
                f'<div class="expert">'
                f'<div class="flex-row">'
                f'<a href="./guest/{get_url(name)}.html">{name} ({count} {ep_label})</a>'
                f'</div>'
                f'<div><em>{title}</em></div>'
                f'</div>'
            )

        if wiki_link:
            if thumb_url:
                dims = f' width="{thumb_w}" height="{thumb_h}"' if thumb_w and thumb_h else ''
                thumb_html = f'<div><img src="{thumb_url}"{dims} /></div>'
            else:
                thumb_html = ''
            wiki_col = (
                f'<div><a href="{wiki_link}" target="_blank">'
                f'{thumb_html}'
                f'<div>wikipedia article &#8599;</div>'
                f'</a></div>'
            )
        else:
            wiki_col = ''

        top_cats = top_level_categories_by_episode.get(topic, [])
        ep_cats = categories_by_episode.get(topic, [])
        cats_html = ''
        for cat in top_cats:
            cats_html += f'<a href="./category/{get_url(cat)}.html">{cat}</a>'
        for cat in ep_cats:
            cats_html += f'<a href="./category/{get_url(cat)}.html">{cat}</a>'

        for tag in custom_tags_by_episode.get(topic, []):
            cats_html += f'<a href="./category/{get_url(tag)}.html">{tag[0].upper() + tag[1:]}</a>'

        return (
            f'<div class="episode flex-column">'
            f'<div class="episode-title"><h3>{topic}</h3></div>'
            f'<div class="episode-about">'
            f'<div class="content-col">'
            f'<p>{description}</p>'
            f'<div class="date">{date}</div>'
            f'<p><a href="https://www.bbc.co.uk/sounds/play/{bbc_id}" target="_blank">listen &#8599;</a></p>'
            f'</div>'
            f'<div class="wiki-col">{wiki_col}</div>'
            f'<div class="meta-col">{experts_html}</div>'
            f'</div>'
            f'<p class="categories">{cats_html}</p>'
            f'<div class="episode-ranking" data-topic="{_html.escape(topic, quote=True)}"></div>'
            f'</div>'
        )

    # Pre-render only the first page (most recent PAGE_SIZE episodes, assumed date-sorted)
    prerendered = '\n'.join(render_episode(ep) for ep in episodes[:PAGE_SIZE])

    html = f'''<html lang="en">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="index,follow,noai,noimageai">
    <meta name="googlebot" content="index,follow">
    <meta name="description" content="An index of In Our Time episodes and their associated Wikipedia pages.">
    <meta property="og:url" content="">
    <meta property="og:title" content="in our time">
    <meta property="og:description" content="An index of In Our Time episodes and their associated Wikipedia pages.">
    <meta name="theme-color" content="#000">
    <title>in our time</title>
    <link rel="stylesheet" type="text/css" href="./client/css/common.{v}.css">
    <link rel="stylesheet" type="text/css" href="./client/css/index.{v}.css">
    <link rel="icon" href="./client/lord-bragg.jpg">
    <script src="./client/util.{v}.js"></script>
    <script src="./client/index.{v}.js"></script>
</head>

<body>
    <main>
        <div>
            <header>
                <div class="flex-row space-between">
                    <h1><a href="./" class="home-link"><img src="./client/lord-bragg.jpg" alt="Melvyn Bragg">Hello,</a></h1>
                    <div class="flex-row" style="gap: 2rem">
                        <a href="./world.html">world</a>
                        <a href="https://github.com/shelbywilson/melvyn" target="_blank">about</a>
                    </div>
                </div>
                <div class="filters flex-row justify-end">
                    <div class="flex-column">
                        <label class="mb-1">
                            <input id="scored-only" type="checkbox">
                            scored only
                        </label>
                        <input class="mb-1" id="search" type="text" placeholder="search" spellcheck="false">
                        <select id="sort-by" value="date" class="mb-1">
                            <option disabled="">sort by</option>
                            <option value="date">date</option>
                            <option value="name">name</option>
                            <option value="score">score</option>
                        </select>
                        <div class="mb-1 buttons--bottom">
                            <button class="first-page" disabled="" onclick="changePage('first')">⇤</button>
                            <button class="prev-page" disabled="" onclick="changePage(-1)">←</button>
                            <button class="next-page" onclick="changePage(1)">→</button>
                            <button class="last-page" onclick="changePage('last')">⇥</button>
                        </div>
                        <div class="mb-1 flex-row space-between">
                            <span id="start-to-end">1 to {PAGE_SIZE}</span>
                            <span id="count">{episode_count} episodes</span>
                        </div>
                    </div>
                </div>
            </header>
            <div id="episodes">
{prerendered}
            </div>
            <div class="mb-1 buttons--bottom">
                <button class="first-page" disabled="" onclick="changePage('first')">⇤</button>
                <button class="prev-page" disabled="" onclick="changePage(-1)">←</button>
                <button class="next-page" onclick="changePage(1)">→</button>
                <button class="last-page" onclick="changePage('last')">⇥</button>
            </div>
        </div>
        <footer class="attribution">
            <p><a href="https://commons.wikimedia.org/wiki/File:Official_portrait_of_Lord_Bragg_crop_2.jpg" target="_blank">Portrait of Lord Bragg</a> by <a href="https://www.parliament.uk/" target="_blank">UK Parliament</a> / Chris McAndrew, <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank">CC BY 3.0</a></p>
        </footer>
    </main>
</body>

</html>'''

    with open('./../index.html', 'w') as w:
        w.write(html)

    print(f'\t{episode_count} episodes ({PAGE_SIZE} prerendered)')
    print('### end create_index_page')

if __name__ == "__main__":
    create_index_page()
