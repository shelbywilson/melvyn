## used to update Google Sheet used for scoring episodes
import json
import csv

f = open('./../data/episodes.json')
data = json.load(f)
f.close()

w = open('./../data/episodes.csv', 'w')
writer = csv.writer(w, delimiter=",")
writer.writerow(['Topic', 'Date', 'Score', 'Comments'])

for episode in data:
    writer.writerow([episode['topic'], episode['date'], '', ''])

w.close()