from bs4 import BeautifulSoup
import urllib.request
import json
from datetime import datetime
    
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d %b %Y')
    except:
        return datetime.strptime(date_str, '%d %B %Y')

# some titles on the BBC site differ from the Wikipedia articles 
#  [key: BBC title]: [value: Wikipedia title]
normalized_titles = {
    "al-Biruni": "Al-Biruni",
    "Safavid Dynasty": "The Safavid dynasty",
    "The Safavid Dynasty": "The Safavid dynasty",
    "The Seventh Seal": "The Seventh Seal\n(1000th program)",
    "Beethoven": "Ludwig van Beethoven",
    "In Our Time - Animal Farm": "Animal Farm",
    "Tagore": "Rabindranath Tagore",
    "Truth, Lies and Fiction": "Truth, Lies and fiction",
    "Cultural Rights in the 20th Century": "Cultural rights in the 20th Century",
    "The Plague of Justinian": "Plague of Justinian",
    "The Zong Massacre": "Zong Massacre",
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
    "The Challenger Expedition 1872-1876": "The Challenger Expedition 1872–1876",
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
    "Neuroscience in the 20th century": "Neuroscience in the 20th Century",
    "Germaine de Stael": "Germaine de Staël",
    "Comenius": "Jan Amos Komenský",
}

def get_top_level_categories():
    print('\n### start get_top_level_categories')
    f = open('./../data/episodes_dictionary.json')
    episodes_dictionary = json.load(f)
    f.close()

    bbc = {
        "Culture": "https://www.bbc.co.uk/programmes/p01drwny/episodes/downloads",
        "History": "https://www.bbc.co.uk/programmes/p01dh5yg/episodes/downloads",
        "Philosophy": "https://www.bbc.co.uk/programmes/p01f0vzr/episodes/downloads",
        "Religion": "https://www.bbc.co.uk/programmes/p01gvqlg/episodes/downloads",
        "Science": "https://www.bbc.co.uk/programmes/p01gyd7j/episodes/downloads"
    }

    top_level_categories = {
        "Culture": [
            "Lyrical Ballads",
            "Boudica",
            "Delacroix's Liberty Leading the People",
            "Vitruvius and De Architectura",
            "The Etruscan Civilisation",
            "The Great Wall of China",
            "The Rise and Fall of the Zulu Nation",
            "Romulus and Remus",
            "The Silk Road",
            "Japan's Sakoku Period",
            "The Death of Elizabeth I",
            "Sparta",
            "Akhenaten",
            "The Augustan Age",
            "The Magna Carta",
            "The Building of St Petersburg",
            "The Statue of Liberty",
            "Tacitus and the Decadence of Rome",
            "Bismarck",
            "The Roman Republic",
            "Washington and the American Revolution",
            "Babylon",
            "Byzantium",
            "Tea",
            "The Alphabet",
            "Roman Britain",
            "The Enclosures of the 18th Century",
            "Heritage",
            "The Trojan War",
            "The American West",
            "Bohemia",
            "The Norman Yoke",
            "The Aztecs",
            "The Celts",
            "Rome and European Civilization",
            "The British Empire",
            "The Enlightenment in Britain",
            "The Tudor State",
            "Africa",
            "Money",
            "The Aristocracy"
        ],
        "History": [
            "Plague of Justinian",
            "History as Science",
            "The Wars of the Roses",
            "History and Understanding the Past",
            "New Wars",
            "Hitler in History",
            "The French Revolution's Legacy",
            "The Enlightenment in Britain",
            "The Restoration",
            "The Roman Empire's Collapse in the 5th century",
            "The Glorious Revolution",
            "Napoleon and Wellington",
            "The British Empire",
            "The Haymarket Affair",
            "Benjamin Disraeli",
            "Voyages of James Cook",
            "Marco Polo",
            "The Battle of Bosworth Field",
            "The Siege of Tenochtitlan",
            "The Spanish Armada",
            "Athelstan",
            "The City - a history, part 2",
            "The City - a history, part 1",
            "The Indian Mutiny",
            "The Glencoe Massacre",
            "The Dreyfus Affair",
            "The Trial of Charles I",
            "The Boxer Rebellion",
            "Carthage's Destruction",
            "History of History",
            "The Fire of London",
            "The Great Reform Act",
            "Bolivar",
            "The Black Death",
            "The Enclosures of the 18th Century",
            "The Charge of the Light Brigade",
            "The Sassanid Empire",
            "The Siege of Orléans",
            "The Opium Wars",
            "Genghis Khan",
            "Constantinople Siege and Fall",
            "The Peasants' Revolt",
            "The Great Exhibition of 1851",
            "The Abbasid Caliphs",
            "The Peterloo Massacre",
            "The Field of the Cloth of Gold",
            "The French Revolution's Reign of Terror",
            "Alfred and the Battle of Edington",
            "Tsar Alexander II's assassination",
            "The Roman Republic",
            "Agincourt",
            "Washington and the American Revolution",
            "Babylon",
            "Byzantium",
            "China's Warring States period",
            "The Mughal Empire",
            "Thermopylae",
            "The Alphabet",
            "The East India Company",
            "The Jacobite Rebellion",
            "Atrocity in the 20th Century",
            "Roman Britain",
            "The British Empire's Legacy",
            "History's relevance in the 20th century",
            "The Spanish Civil War",
            "Catherine the Great"
        ],
        "Philosophy": [
            "Clausewitz and On War",
            "War in the 20th Century",
            "Ptolemy and Ancient Astronomy",
            "Archaeology and Imperialism",
            "Suffragism",
            "Architecture and Power",
            "Slavery and Empire",
            "Chinese Legalism",
            "The Nation State",
            "Lenin",
            "Politics in the 20th Century",
            "History's relevance in the 20th century",
            "Republicanism",
            "Education"
        ],
        "Religion": [
            "The Divine Right of Kings",
            "Wilberforce"
        ],
        "Science": [
            "Wormholes",
            "Ptolemy and Ancient Astronomy",
            "Childhood",
            "The Moon",
            "History as Science"
        ]
    }
    top_level_categories_by_episode = {}
    
    r = open('./../data/top_level_categories_by_episode.json', 'r')
    cat_by_ep = json.load(r)
    r.close()
    
    # any missing episodes?
    # tend to be earlier ones
    for ep in episodes_dictionary.keys():
        if ep in cat_by_ep:
            pass
        else:
            print(ep, episodes_dictionary[ep]['date'])

    def add_to_dictionary(type, page):
        html_page = urllib.request.urlopen(bbc[type] + "?page=" + str(page))
        soup = BeautifulSoup(html_page, "html.parser")
        episodes = soup.find_all('a', {'class': "br-blocklink__link"})

        for ep in episodes:
            title = ep.get_text()
            if (title.startswith("In Our Time") or title.startswith("Introducing")):
                continue
            if (title in normalized_titles):
                title = normalized_titles[title]
            if (title not in top_level_categories[type]):
                top_level_categories[type].append(title)

    for type in bbc:
        page = 1
        while (page < 15):
            try:
                add_to_dictionary(type, page)
                page += 1
            except:
                continue
            
    def get_date(topic):
        try:
            return parse_date(episodes_dictionary[topic]['date'])
        except:
            return datetime.min
        
    for key in top_level_categories:
        top_level_categories[key] = sorted(top_level_categories[key], key=get_date, reverse=True)        

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