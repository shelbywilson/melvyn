from get_episodes import get_episodes
from get_bbc_descriptions import get_bbc_descriptions
from get_thumbnails import get_thumbnails
from guest_analysis import guest_analysis
from get_topic_categories import get_topic_categories
from get_top_level_categories import get_top_level_categories
from create_topic_category_page import create_topic_category_page 
from create_guest_pages import create_guest_pages 

print('# get episodes')
get_episodes()

print('\n# get thumbnails')
get_thumbnails()

print('\n# get bbc descriptions')
get_bbc_descriptions()

print('\n# guest analysis')
guest_analysis()

print('\n# top level categories')
get_top_level_categories()

print('\n# get topic categories \n# create guest pages \n# create topic pages')
get_topic_categories()

create_topic_category_page()
create_guest_pages()