from elasticsearch import Elasticsearch
import re

es = Elasticsearch(["giskard.aqelia.com"])

res = es.search(index="vlille-stations", body={
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "id": 1
          }
        },
      ],
      "filter": [
        {
          "range": {
            "timestamp": {
              "gte": "2019-12-08T22:20:00",
            }
          }
        }
      ]
    }
  }
})

print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
  dateExplodeWithoutYear = re.match('[0-9]{4}-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2}).*', doc['_source']['timestamp']).groups()
  dateVector = list(map(int, dateExplodeWithoutYear))

  vector = [
    doc['_source']['id'],
    doc['_source']['bikes'],
    doc['_source']['docks'],
  ] + dateVector

  print("%s) %s" % (doc['_id'], vector))
