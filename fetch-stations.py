from elasticsearch import Elasticsearch
import re

def buildVector(doc):
  dateExplodeWithoutYear = re.match('[0-9]{4}-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2})', doc['_source']['timestamp']).groups()
  dateVector = list(map(int, dateExplodeWithoutYear))

  return [
    doc['_source']['id'],
    1 if doc['_source']['status'] == 'EN SERVICE' else 0,
    doc['_source']['bikes'],
    doc['_source']['docks'],
  ] + dateVector

es = Elasticsearch(["giskard.aqelia.com"])

res = es.search(index="vlille-stations", size=10000, body={
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
              "gte": "2019-10-01",
              "lte": "2019-10-08",
            }
          }
        }
      ]
    }
  }
})

print("%d documents found" % res['hits']['total'])

globalSet = list(map(buildVector, res['hits']['hits']))

print(globalSet)
