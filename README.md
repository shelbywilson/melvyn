# Explore episodes of In Our Time

[https://shelby.cool/melvyn/](https://shelby.cool/melvyn/)

## scripts
Using python scripts, episodes are scraped from [Wikipedia's List of In Our Time Programmes](https://en.wikipedia.org/wiki/List_of_In_Our_Time_programmes) and their descriptions are scraped from [BBC](https://www.bbc.co.uk/sounds/brand/b006qykl) and html pages are generated from this data. 

If there is an associated Wikipedia article, that is followed and its categories are compiled. Any categories to which multiple episodes' articles are associated will be displayed (this is to reduce noise since any categories that only apply to a single episode are not a useful/interesting grouping), and these link to a category page:

<img width="1150" alt="Symmetry; a line drawing of a symmetric tree and an asymmetric tree" src="https://user-images.githubusercontent.com/5523024/193950974-8e85a23f-29f9-4a00-8488-409022d50b38.png">

e.g. Aesthetics and Theoretical Physics

In the cases where categories share an identical set of episodes, they are collapsed into a single category (e.g. ["Ancient Greek metaphysicians, Ancient Greek ethicists, Ancient Greek metaphilosophers"](https://shelby.cool/melvyn/category/Ancient_Greek_metaphilosophers,_Ancient_Greek_metaphysicians,_Ancient_Greek_ethicists.html) is a single category since all three are associated to the episodes: "Plato's Gorgias", "Heraclitus", "Pythagoras", and "Socrates").

Each guest has their own page as well:
<img width="1171" alt="Emma Smith" src="https://user-images.githubusercontent.com/5523024/193951523-740f7194-ea5c-46b1-acfe-cf19cf39b110.png">

A Google sheet supplies ranking and comments.

## to update
##### from `/scripts`
`python update_all.py`

## local server
`python3 -m http.server 5142`