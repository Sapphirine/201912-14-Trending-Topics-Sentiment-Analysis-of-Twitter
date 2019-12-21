from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account



from collections import defaultdict
import json

credentials = service_account.Credentials.from_service_account_file('website2\\hw1-jl5255-7e5b2ee95a9d.json')

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()

def my_schedule(task):
    print("link to bigquery")
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "hw1-jl5255"

    #SQL = "SELECT location, topic, count(*) as count FROM `hw1-jl5255.BigData_Final.tweetTopicSent_country` group by location, topic LIMIT 5"
    SQL = "SELECT * FROM `hw1-jl5255.BigData_Final.tweetTopicSent_country`"

    df = pandas_gbq.read_gbq(SQL)
    print(df)
    countries = defaultdict(dict)
    count_topic = defaultdict(dict)
    for i, row in df.iterrows():
            if row['country'] not in countries or row['topic'] not in countries[row['country']]:
                pos, neu, neg = 0, 0, 0
                count = 1
                if row['sentiment'] > 0:
                    pos += 1
                elif row['sentiment'] == 0:
                    neu += 1
                else: 
                    neg += 1
                tmp = {}
                tmp['sentiment'] = (pos, neu, neg)
                sum_sen = pos + neu + neg
                tmp['sentiment_percent'] = [pos/sum_sen*100, neu/sum_sen*100, neg/sum_sen*100]
                tmp['count'] = count
                countries[row['country']][row['topic']] = tmp
                count_topic[row['country']][row['topic']] = count
            else:
                pos, neu, neg = countries[row['country']][row['topic']]['sentiment']
                if row['sentiment'] > 0:
                    pos += 1
                elif row['sentiment'] == 0:
                    neu += 1
                else: 
                    neg += 1
                countries[row['country']][row['topic']]['sentiment'] = (pos, neu, neg)
                sum_sen = pos + neu + neg
                countries[row['country']][row['topic']]['sentiment_percent'] = [pos/sum_sen*100, neu/sum_sen*100, neg/sum_sen*100]
                countries[row['country']][row['topic']]['count'] += 1
                count_topic[row['country']][row['topic']] =  countries[row['country']][row['topic']]['count']
    
    with open('static\data\country-tweet.json', 'w') as w:
        json.dump(countries, w)

    # #TODO
    country_top_5 = {}
    for country, topics in count_topic.items():
        top_5_topics = sorted(list(topics.items()), reverse=True, key=lambda x:x[1])[:5]
        country_top_5[country] = [topic[0] for topic in top_5_topics]
    with open('static\data\country-top-topic.json', 'w') as w:
        json.dump(country_top_5, w)

scheduler.add_job(my_schedule,"interval", seconds=5, args=(5,)) 
register_events(scheduler)

def map(request):
    context = {}
    return render(request, 'world_map.html', context)