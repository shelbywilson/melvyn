# Explore episodes of In Our Time

[https://shelby.cool/melvyn](https://shelby.cool/melvyn/)

This is an index of episodes of In Our Time, a BBC radio show. Episodes are linked to their associated Wikipedia articles when available. Episodes are categorized by five top-level categories ([science](https://shelby.cool/melvyn/category/Science.html), [philosophy](https://shelby.cool/melvyn/category/Philosophy.html), [history](https://shelby.cool/melvyn/category/History.html), [culture](https://shelby.cool/melvyn/category/Culture.html), and [religion](https://shelby.cool/melvyn/category/Religion.html)), and many subcategories (tagged in their associated Wikipedia articles). 

Browse by title, category, description, and guests in a searchable [list](https://shelby.cool/melvyn/index.html) or [3D visualization](https://shelby.cool/melvyn/world.html). 

[<img width="1470" alt="in our time world" src="https://github.com/user-attachments/assets/dcdb27f6-85ee-41cd-b54b-3d7fbad323e1">](https://shelby.cool/melvyn/world.html)

## scripts
Using python scripts, episodes are scraped from [Wikipedia's List of In Our Time Programmes](https://en.wikipedia.org/wiki/List_of_In_Our_Time_programmes) and their descriptions are scraped from [BBC](https://www.bbc.co.uk/sounds/brand/b006qykl) and html pages are generated from this data. 

If there is an associated Wikipedia article, that is followed and its categories are compiled. Any categories to which multiple episodes' articles are associated will be displayed (this is to reduce noise since any categories that only apply to a single episode are not a useful/interesting grouping), and these link to a category page:

<img width="1150" alt="Symmetry; a line drawing of a symmetric tree and an asymmetric tree" src="https://user-images.githubusercontent.com/5523024/193950974-8e85a23f-29f9-4a00-8488-409022d50b38.png">

e.g. Aesthetics and Theoretical Physics

In the cases where categories share an identical set of episodes, they are collapsed into a single category (e.g. ["Ancient Greek metaphilosophers, Ancient Greek metaphysicians, Ancient Greek ethicists"](https://shelby.cool/melvyn/category/Ancient_Greek_ethicists,_Ancient_Greek_epistemologists.html) is a single category since both categories are associated to the episodes: "Heraclitus", "Plato's Gorgias", and "Socrates").

Each guest has their own page as well:
<img width="1171" alt="Emma Smith" src="https://user-images.githubusercontent.com/5523024/193951523-740f7194-ea5c-46b1-acfe-cf19cf39b110.png">(https://shelby.cool/melvyn/guest/Emma_Smith.html), and a link to that guest's own Wikipedia page (when available).

A Google sheet supplies ranking and comments.

## to update
#### from `/scripts`
##### install dependencies
`pip3 install -r requirements.txt`
##### update content
`python update_all.py`

## local server
`python3 -m http.server 5142` (or any port)

## TODO 
- [ ] network diagram of guests
- [ ] add bookmarking
- [ ] arrange world in a meaningful way rather than randomly (PCA? UMAP?)
- [ ] allow anyone to score or comment on episodes (local storage? link own google sheet?)
