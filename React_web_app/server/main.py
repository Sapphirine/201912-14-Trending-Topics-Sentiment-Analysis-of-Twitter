import json
from random import shuffle

from flask import Flask, Response, make_response, jsonify, request
from google.cloud import bigquery

import utils

client = bigquery.Client()
query = "SELECT * FROM BigData_Final.tweetTopicSent;"

app = Flask(__name__)

@app.route("/")
def home():
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    rp = list()
    for index, row in results.iterrows():
        res = dict()
        for col in results.columns:
            if col == 'sentiment':
                res[col] = float(row[col])
            else:
                res[col] = row[col]
        rp.append(res)
    shuffle(rp)
    print(rp[0])
    resp = jsonify(utils.group_by_loc_topic(rp[:300]))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/search", methods=['POST'])
def search():
    data = json.loads(request.get_data().decode('utf-8'))
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    app.run(debug=True)
