# To run:
# pip3 install sentence-transformers

from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('bbc_descriptions.json', 'r') as file:
    data = json.load(file)
    for name, episode in data.items():
        print(name)
        embedding = model.encode([episode['short_desc'] if episode['long_desc'] == '' else episode['long_desc']])
        data[name]['embedding'] = embedding[0].tolist()
    # write out data
    with open('bbc_descriptions_with_embeddings.json', 'w') as out_file:
        json.dump(data, out_file)
    