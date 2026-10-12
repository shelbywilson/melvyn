window.onload = () => {
    getScores().then(scores => {
        const episodes = document.getElementsByClassName('episode-ranking')

        for (let i = 0; i < episodes.length; i += 1) {
            episodes[i].innerHTML = getRankingHTML(scores[episodes[i].getAttribute('data-topic')])
        }
    })
}