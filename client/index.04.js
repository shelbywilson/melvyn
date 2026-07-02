const PAGE_SIZE = 50;

const initialPage = parseInt(window.location.hash.split('page=').pop()) || 0;
const state = {
    start: initialPage * PAGE_SIZE,
    end: (initialPage + 1) * PAGE_SIZE - 1,
    scoredOnly: false,
    sortBy: 'date',
    search: '',
};

let episodes = [], bbcDescriptions = {}, guestFrequency = {}, categoriesByEpisode = {},
    topLevelCategoriesByEpisode = {}, customTagsByEpisode = {}, thumbnails = {}, config = {}, scores = {};

window.onload = () => {
    state.scoredOnly = document.getElementById('scored-only').checked;
    document.getElementById('search').addEventListener('input', filter);
    document.getElementById('scored-only').addEventListener('input', filter);
    document.getElementById('sort-by').addEventListener('change', filter);
    window.onhashchange = display;

    Promise.all([
        fetch('./data/episodes_min.json').then(r => r.json()),
        fetch('./data/bbc_descriptions_short.json').then(r => r.json()),
        fetch('./data/guest_frequency_min.json').then(r => r.json()),
        fetch('./data/categories_by_episode.json').then(r => r.json()),
        fetch('./data/top_level_categories_by_episode.json').then(r => r.json()),
        fetch('./data/custom_tags_by_episode.json').then(r => r.json()),
        fetch('./data/episode_thumbnails.json').then(r => r.json()),
        fetch('./data/episode_thumbnails_manual.json').then(r => r.json()),
        fetch('./config/config.json').then(r => r.json()),
    ]).then(([eps, desc, freq, cats, topCats, customTags, thumbs, manualThumbs, cfg]) => {
        episodes = eps;
        bbcDescriptions = desc;
        guestFrequency = freq;
        categoriesByEpisode = cats;
        topLevelCategoriesByEpisode = topCats;
        customTagsByEpisode = customTags;
        thumbnails = {...thumbs, ...manualThumbs};
        config = cfg;
        state.end = Math.min(state.end, episodes.length - 1);
        display();
    }).catch(console.error);

    // Scores load independently — only populates score divs, never redraws episodes
    getScores().then(s => {
        scores = s;
        populateScores();
        if (state.scoredOnly || state.sortBy === 'score') display();
    }).catch(console.error);
};

function getUrl(name) {
    return name.replace(/\s/g, '_').substring(0, config.MAX_LENGTH_URL || 100);
}

function renderEpisode(ep) {
    const { topic, date, wiki_link: wikiLink = '', episode_link: episodeLink = '', experts = [] } = ep;
    const bbcId = episodeLink.split('/').pop();
    const description = bbcDescriptions[`${date}_${topic}`] || '';
    const thumb = thumbnails[topic];
    const thumbUrl = thumb?.url || '';
    const thumbW = thumb?.width;
    const thumbH = thumb?.height;

    const expertsHtml = experts.map(({ name, title = '' }) => {
        const count = guestFrequency[name] || 1;
        return `<div class="expert"><div class="flex-row"><a href="./guest/${getUrl(name)}.html">${name} (${count} ${count === 1 ? 'episode' : 'episodes'})</a></div><div><em>${title}</em></div></div>`;
    }).join('');

    let wikiCol = '';
    if (wikiLink) {
        const dims = thumbW && thumbH ? ` width="${thumbW}" height="${thumbH}"` : '';
        const thumbHtml = thumbUrl ? `<div><img src="${thumbUrl}"${dims} /></div>` : '';
        wikiCol = `<div><a href="${wikiLink}" target="_blank">${thumbHtml}<div>wikipedia article &#8599;</div></a></div>`;
    }

    const catsHtml = [
        ...(topLevelCategoriesByEpisode[topic] || []),
        ...(categoriesByEpisode[topic] || []),
    ].map(cat => `<a href="./category/${getUrl(cat)}.html">${cat}</a>`).join('');

    const customCatsHtml = (customTagsByEpisode[topic] || [])
        .map(tag => `<a href="./category/${getUrl(tag)}.html">${tag.charAt(0).toUpperCase() + tag.slice(1)}</a>`).join('');

    return `<div class="episode flex-column">
        <div class="episode-title"><h3>${topic}</h3></div>
        <div class="episode-about">
            <div class="content-col"><p>${description}</p><div class="date">${date}</div><p><a href="https://www.bbc.co.uk/sounds/play/${bbcId}" target="_blank">listen &#8599;</a></p></div>
            <div class="wiki-col">${wikiCol}</div>
            <div class="meta-col">${expertsHtml}</div>
        </div>
        <p class="categories">${catsHtml}${customCatsHtml}</p>
        <div class="episode-ranking" data-topic="${topic}"></div>
    </div>`;
}

function populateScores() {
    document.querySelectorAll('.episode-ranking').forEach(div => {
        const score = scores[div.dataset.topic];
        if (score) div.innerHTML = getRankingHTML(score);
    });
}

function display() {
    const filtered = episodes
        .filter(ep => {
            if (state.scoredOnly && !scores[ep.topic]?.Score) return false;
            return isSearchMatch(ep, categoriesByEpisode, topLevelCategoriesByEpisode, bbcDescriptions, scores, false, state.search, customTagsByEpisode);
        })
        .sort((a, b) => {
            switch (state.sortBy) {
                case 'name': return a.topic.localeCompare(b.topic);
                case 'score': return (scores[b.topic]?.Score || 0) - (scores[a.topic]?.Score || 0);
                default: return new Date(b.date) - new Date(a.date);
            }
        });

    const n = filtered.length;
    if (n > 0) {
        state.start = Math.min(state.start, n - 1);
        state.end = Math.min(state.end, n - 1);
    }

    document.getElementById('episodes').innerHTML = n === 0
        ? '<p class="no-results">No episodes found.</p>'
        : filtered.slice(state.start, state.end + 1).map(renderEpisode).join('');

    populateScores();

    document.querySelectorAll('.first-page, .prev-page').forEach(el => { el.disabled = state.start === 0; });
    document.querySelectorAll('.last-page, .next-page').forEach(el => { el.disabled = n === 0 || state.end >= n - 1; });

    window.location.hash = state.start > 0 ? `page=${Math.floor(state.start / PAGE_SIZE)}` : '';

    document.getElementById('count').innerText = `${n} ${n === 1 ? 'episode' : 'episodes'}`;
    document.getElementById('start-to-end').innerText = `${1 + state.start} to ${1 + Math.min(state.end, Math.max(0, n - 1))}`;
}

function changePage(direction) {
    const n = episodes.filter(ep => isSearchMatch(ep, categoriesByEpisode, topLevelCategoriesByEpisode, bbcDescriptions, scores, false, state.search, customTagsByEpisode)).length;
    if (direction === -1) state.start = Math.max(0, state.start - PAGE_SIZE);
    else if (direction === 1) state.start = Math.min(n - 1, state.start + PAGE_SIZE);
    else if (direction === 'first') state.start = 0;
    else if (direction === 'last') state.start = Math.floor(n / PAGE_SIZE) * PAGE_SIZE;
    state.end = state.start + PAGE_SIZE - 1;
    display();
}

function filter() {
    state.scoredOnly = document.getElementById('scored-only').checked;
    state.search = document.getElementById('search').value.toLowerCase().trim();
    state.sortBy = document.getElementById('sort-by').value;
    state.start = 0;
    state.end = PAGE_SIZE - 1;
    display();
}
