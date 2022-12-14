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

function getRankingHTML(score = {Score: 0}) {
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