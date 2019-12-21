# import json
# import random

# topics = []

# with open('sample-topics.csv', 'r') as f:
#     for line in f:
#         topics.append(line.strip())

# with open('world-topo-min.json', 'r') as f, open('example-tweet-toptic.json', 'w') as w:
#     data = json.load(f)
#     geometries = data['objects']['countries']['geometries']
#     countries = {}
#     topics_len = len(topics)
#     for geo in geometries:
#         topic_ids = [random.randrange(0, topics_len) for i in range(3)]
#         countries[geo['properties']['name']] = [{'topic':topics[topic_ids[0]], 'sentiment':'neutral'}, {'topic':topics[topic_ids[1]], 'sentiment':'negitive'}, {'topic':topics[topic_ids[2]], 'sentiment':'positive'}]
    
#     json.dump(countries, w)

    
import json
import random

topics = []

# with open('sample-topics.csv', 'r') as f:
#     for line in f:
#         topics.append(line.strip())

# with open('world-topo-min.json', 'r') as f, open('example-tweet-toptic-big-query.json', 'w') as w:
#     data = json.load(f)
#     geometries = data['objects']['countries']['geometries']
#     countries = []
#     topics_len = len(topics)
#     for geo in geometries:
#         topic_ids = [random.randrange(0, topics_len) for i in range(3)]
#         tmp = {}
#         tmp['country_name'] = geo['properties']['name']
#         tmp['topic_1'] = topics[topic_ids[0]]
#         tmp['topic_2'] = topics[topic_ids[1]]
#         tmp['topic_3'] = topics[topic_ids[2]]
#         tmp['sentiment_1'] = 'neutral'
#         tmp['sentiment_2'] = 'positive'
#         tmp['sentiment_3'] = 'negitive'

#         countries.append(tmp)

#         #countries[geo['properties']['name']] = [{'topic':topics[topic_ids[0]], 'sentiment':'neutral'}, {'topic':topics[topic_ids[1]], 'sentiment':'negitive'}, {'topic':topics[topic_ids[2]], 'sentiment':'positive'}]
    
#     json.dump(countries, w)



with open('world-topo-min.json', 'r') as f, open('country_list.json', 'w') as w:
    data = json.load(f)
    geometries = data['objects']['countries']['geometries']
    countries = []
    for geo in geometries:
        countries.append(geo['properties']['name'])
    json.dump(countries, w)