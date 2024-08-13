from bs4 import BeautifulSoup
import urllib.request
import json

# some titles on the BBC site differ from the Wikipedia articles 
#  [key: BBC title]: [value: Wikipedia title]
normalized_titles = {
    "Al-Biruni": "al-Biruni",
    "The Safavid Dynasty": "Safavid Dynasty",
    "The Seventh Seal": "The Seventh Seal\n(1000th program)",
    "Beethoven": "Ludwig van Beethoven",
    "Germaine de Stael - Animal Farm": "Animal Farm",
    "Rabindranath Tagore": "Tagore",
    "Truth, Lies and Fiction": "Truth, Lies and fiction",
    "Cultural rights in the 20th Century": "Cultural Rights in the 20th Century",
    "The Plague of Justinian": "Plague of Justinian",
    "Zong Massacre": "The Zong Massacre",
    "The Valladolid Debate": "Valladolid Debate",
    "The Siege of Paris 1870-71": "The Siege of Paris (1870-71)",
    "Owain Glyndwr": "Owain Glyndŵr",
    "Matteo Ricci and the Ming Dynasty": "Matteo Ricci and the Ming dynasty",
    "Ice Ages": "Ice ages",
    "Aristotle's Biology": "Aristotle's biology",
    "Zeno's Paradoxes": "Zeno's paradoxes",
    "Ordinary Language Philosophy": "Ordinary language philosophy",
    "Free Will": "Free Will(500th programme)",
    "William James's 'The Varieties of Religious Experience'": "William James's The Varieties of Religious Experience",
    "Godel's Incompleteness Theorems": "Gödel's Incompleteness Theorems",
    "The Challenger Expedition 1872-1876 is now first on BBC Sounds": "The Challenger Expedition 1872–1876",
    "Feathered Dinosaurs": "Feathered dinosaurs",
    "Bird Migration": "Bird migration",
    "Pauli's Exclusion Principle": "Pauli's exclusion principle",
    "The Kuiper Belt": "The Kuiper belt",
    "Circadian Rhythms": "Circadian rhythms",
    "Perpetual Motion": "Perpetual motion",
    "The Earth's Core": "The Earth's core",
    "Dark Matter": "Dark matter",
    "Behavioural Ecology": "Behavioural ecology",
    "Cosmic Rays": "Cosmic rays",
    "Pitt-Rivers": "Pitt Rivers",
    "The Scientific Method": "The Scientific method",
    "Imaginary Numbers": "Imaginary numbers",
    "Mathematics' Unintended Consequences": "The Unintended Consequences of Mathematics",
    "The Royal Society and British Science: Episode 4—In Our Time: The Royal Society and British Science": "The Royal Society and British Science: Episode 4",
    "The Royal Society and British Science: Episode 3—In Our Time: The Royal Society and British Science": "The Royal Society and British Science: Episode 3",
    "The Royal Society and British Science: Episode 2—In Our Time: The Royal Society and British Science": "The Royal Society and British Science: Episode 2",
    "The Royal Society and British Science: Episode 1—In Our Time: The Royal Society and British Science": "The Royal Society and British Science: Episode 1",
    "The Measurement Problem in Physics": "The Measurement problem in Physics",
    "Darwin: Life After Origins—Darwin: In Our Time": "Darwin: Life After Origins",
    "Darwin: On the Origin of Species—Darwin: In Our Time": "Darwin: On the Origin of Species",
    "Darwin: The Voyage of the Beagle—Darwin: In Our Time": "Darwin: The Voyage of the Beagle",
    "Darwin: On the Origins of Charles Darwin—Darwin: In Our Time": "Darwin: On the Origins of Charles Darwin",
    "The Poincaré Conjecture": "The Poincaré conjecture",
    "Negative Numbers": "Negative numbers",
    "Psychoanalysis and Democracy": "Psychoanalysis and democracy",
    "Chemical Elements": "Chemical elements",
    "Climate Change": "Climate change",
    "Neuroscience in the 20th century": "Neuroscience in the 20th Century"
}

def get_top_level_categories():
    print('\n### start get_top_level_categories')
    f = open('./../data/episodes.json')
    episodes = json.load(f)
    f.close()

    bbc = {
        "Culture": "https://www.bbc.co.uk/programmes/p01drwny/episodes/downloads",
        "History": "https://www.bbc.co.uk/programmes/p01dh5yg/episodes/downloads",
        "Philosophy": "https://www.bbc.co.uk/programmes/p01f0vzr/episodes/downloads",
        "Religion": "https://www.bbc.co.uk/programmes/p01gvqlg/episodes/downloads",
        "Science": "https://www.bbc.co.uk/programmes/p01gyd7j/episodes/downloads"
    }

    top_level_categories = {}
    top_level_categories_by_episode = {}

    def add_to_dictionary(type, page):
        html_page = urllib.request.urlopen(bbc[type] + "?page=" + str(page))
        soup = BeautifulSoup(html_page, "html.parser")
        episodes = soup.find_all('a', {'class': "br-blocklink__link"})

        for ep in episodes:
            title = ep.get_text()
            if (title in normalized_titles):
                title = normalized_titles[title]
            if (title not in top_level_categories[type]):
                top_level_categories[type].append(title)

    for type in bbc:
        top_level_categories[type] = []

        page = 1
        while (page < 15):
            try:
                add_to_dictionary(type, page)
                page += 1
            except:
                continue

    for cat in top_level_categories:
        for ep in top_level_categories[cat]:
            if (ep not in top_level_categories_by_episode):
                top_level_categories_by_episode[ep] = []
                if (cat not in top_level_categories_by_episode[ep]):
                    top_level_categories_by_episode[ep].append(cat)

    w = open('./../data/top_level_categories.json', 'w')
    json.dump(top_level_categories, w, indent=4, ensure_ascii=False)
    w.close()

    print('\twrite top_level_categories.json')

    w = open('./../data/top_level_categories_by_episode.json', 'w')
    json.dump(top_level_categories_by_episode, w, indent=4, ensure_ascii=False)
    w.close()

    print('\twrite top_level_categories_by_episode.json')

    print('### end get_top_level_categories')

if __name__=="__main__":
    get_top_level_categories()