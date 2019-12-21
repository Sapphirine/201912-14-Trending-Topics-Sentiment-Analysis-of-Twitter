import random


colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
def genRandomColor(n):
    res = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for i in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        res.append("#" + "".join([str(hex(x)[2:]) for x in [r,g,b]]))
    return res


def group_by_loc_topic(data):
    """
    [{loc: , topic: , sentiment: ,}]
    ->
    {loc: {topic: {pos_sentiment: , neg_sentiment: ,}}}
    """
    res = dict()
    for d in data:
        if d['location'] == 'NYC':
            d['location'] = 'New York'
        if d['location'] == 'LA':
            d['location'] = 'Los Angeles'
        if d['location'] not in res:
            res[d['location']] = dict()
        if d['topic'] not in res[d['location']]:
            res[d['location']][d['topic']] = {'count': 0, 'pos': 0., 'neg': 0.}
        res[d['location']][d['topic']]['count'] += 1
        if d['sentiment'] > 0.:
            res[d['location']][d['topic']]['pos'] += d['sentiment']
        else:
            res[d['location']][d['topic']]['neg'] += d['sentiment']
    tmp = dict()
    for key in res:
        tmp[key] = list()
        for topic in res[key]:
            t = dict()
            t['topic'] = topic
            t['sentiment'] = [res[key][topic]['count'], res[key][topic]['pos'], res[key][topic]['neg']]
            tmp[key].append(t)
        tmp[key] = sorted(tmp[key], key=lambda p: p['sentiment'][0], reverse=True)
    
    loc_data = {'nodes': list(), 'links': list()}
    loc_data['nodes'] = [ {'id': key, 'highlightFontSize': 20} for key in tmp ]
    for i in range(len(loc_data['nodes'])):
        loc_data['nodes'][i]['color'] = colors[i]

    keys = list(tmp.keys())
    for i, k1 in enumerate(keys):
        topics1 = set([ t['topic'] for t in tmp[k1] ][:5])
        for k2 in keys[i:]:
            topics2 = set([ t['topic'] for t in tmp[k2] ][:5])
            if len(topics1.intersection(topics2)) > 2:
                loc_data['links'].append({'source': k1, 'target': k2})
    loc_data['links'][0]['strokeWidth'] = 20
    
    topic_data = {'nodes': list(), 'links': list()};
    for key in tmp:
        for p in tmp[key]:
            if p['topic'] not in topic_data['nodes']:
                topic_data['nodes'].append({'id': p['topic'], 'highlightFontSize': 20})
    for i in range(len(topic_data['nodes'])):
        topic_data['nodes'][i]['color'] = colors[i % (len(colors))]
    count = { Id['id']: dict() for Id in topic_data['nodes'] }
    for key in tmp:
        for p in tmp[key]:
            if key not in count[p['topic']]:
                count[p['topic']][key] = 0
            count[p['topic']][key] += 1
    for p in count:
        count[p] = [ (key, count[p][key]) for key in count[p] ]
        count[p] = sorted(count[p], key=lambda p: p[1], reverse=True)

    keys = list(count.keys())
    for i, k1 in enumerate(keys):
        loc1 = set([ t[0] for t in count[k1] ][:9])
        for k2 in keys[i:]:
            loc2 = set([ t[0] for t in count[k2] ][:9])
            if len(loc1.intersection(loc2)) > 7:
                topic_data['links'].append({'source': k1, 'target': k2})
    return { 
        'plainData': tmp,
        'locGraph': loc_data,
        'topGraph': topic_data
    }



