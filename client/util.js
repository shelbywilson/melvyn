const scoresUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQrVEZP1eRgmuwslWhDmmm0RUB5JHSBKYqLbpG--dJO3ewZbiLsCGDv1rsZ2mLq08gLQbuOiCbj3qSd/pub?gid=2006021976&single=true&output=tsv';

function tsvToScoresDictionary(str, delimiter = "	") {
    const headers = str.slice(0, str.indexOf("\n")).split(delimiter).map(val => val.trim());
    const rows = str.slice(str.indexOf("\n") + 1).split("\n");
    const arr = rows.map(function (row) {
        const values = row.split(delimiter);
        const el = headers.reduce(function (object, header, index) {
            object[header] = values[index].trim();
            return object;
        }, {});
        return el;
    });

    const dict = {}
    arr.forEach(row => {
        dict[row.Topic] = row
    })

    return dict;
}

function getProgressBarHTML(score) {
    score = Math.min(5, parseFloat(score) || 0)
    if (!score) {
        return ''
    }
    return `
    <div class="progress-bar">
        <div style="width: ${score * 20}%" class="score-${Math.round(score) * 20}"></div>
    </div>
    `
}

function getRankingHTML(score = { Score: 0 }) {
    return `<div class="ranking">
        <div class="flex-row">
            <div>
                ${getProgressBarHTML(score.Score)}
            </div>
            <div class="ranking-label">
                ${score.Score ? `${score.Score}/5` : '<em>no score yet</em>'}
            </div>
        </div>
        ${score.Comments ?
            `<div>
                <p>
                    ${score.Comments}
                </p>
            </div>
            ` :
            ''
        }
    </div>
    `
}

async function getScores() {
    return fetch(scoresUrl)
        .then(response => {
            return response.blob()
        })
        .then((blob) => {
            return blob.text()
        })
        .then((tsv) => {
            return tsvToScoresDictionary(tsv)
        })
        .catch((err) => console.error(err));

}

function getCategoriesHTML(topic, categoriesByEpisode, topLevelCategoriesByEpisode, config) {
    let html = '';

    if ((topLevelCategoriesByEpisode[topic] || []).length > 0) {
        topLevelCategoriesByEpisode[topic].forEach(cat => {
            html += '<a href="./category/' + cat.replace(/\s/g, '_').substring(0, config.MAX_LENGTH_URL) + '.html">' + cat + '</a>'
        })
    }

    if ((categoriesByEpisode[topic] || []).length > 0) {
        categoriesByEpisode[topic].forEach(cat => {
            html += '<a href="./category/' + cat.replace(/\s/g, '_').substring(0, config.MAX_LENGTH_URL) + '.html">' + cat + '</a>'
        })
    }
    return html
}

function isSearchMatch(episode, categoriesByEpisode, topLevelCategoriesByEpisode, bbcDescriptions, scores, checkInit, searchTerm = "") {
    const normalizedSearch = searchTerm.toLowerCase().trim()

    if (normalizedSearch.length === 0) {
        return true;
    }

    if (checkInit) {
        if (!episode.init || !episode.topic) {
            return false;
        }
    }
    try {

        return episode.topic.toLowerCase().indexOf(normalizedSearch) > -1 ||
            (categoriesByEpisode[episode.topic] || []).find(cat => cat.toLowerCase().indexOf(normalizedSearch) > -1) ||
            (topLevelCategoriesByEpisode[episode.topic] || []).find(cat => cat.toLowerCase().indexOf(normalizedSearch) > -1) ||
            (bbcDescriptions[episode.date + '_' + episode.topic] || '').toLowerCase().indexOf(normalizedSearch) > -1 ||
            episode.experts.find(expert => expert.name.toLowerCase().indexOf(normalizedSearch) > -1) ||
            (scores[episode.topic] || {
                Comments: ''
            }).Comments.toLowerCase().indexOf(normalizedSearch) > -1
    } catch {
        return false
    }
}