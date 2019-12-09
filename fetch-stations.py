import re
from elasticsearch import Elasticsearch
from datetime import datetime

def buildVector(doc):
  data = doc['_source']

  dateExplodeWithoutYear = re.match('[0-9]{4}-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2})', data['timestamp']).groups()
  dateVector = list(map(int, dateExplodeWithoutYear))

  # compute percent usage of the station
  total = data['bikes'] + data['docks']
  usage = round(data['bikes'] / total, 3) if total > 0 else 0 # should we remove offline stations ?

  return [
    data['id'],
    1 if data['status'] == 'EN SERVICE' else 0,
    usage,
    datetime.fromisoformat(data['timestamp']).weekday(),
  ] + dateVector

es = Elasticsearch(["giskard.aqelia.com"])
res = es.search(index="vlille-stations", size=10000, body={
  "query": {
    "bool": {
      "minimum_should_match" : 1,
      "should": [
        {
          "match": {
            "id": 1
          }
        },
        {
          "match": {
            "id": 2
          }
        },
      ],
      "filter": [
        {
          "range": {
            "timestamp": {
              "gte": "2019-09-25",
              "lte": "2019-10-10",
            }
          }
        }
      ]
    }
  }
})

def writeToCsv(filename, data):
  with open(filename, 'w') as fp:
    # headers
    fp.write('id,status,usage,weekday,month,day,hours,minutes' + '\n')

    # data
    for vector in data:
      fp.write(','.join(map(str, vector)) + '\n')


# Main

print("%d documents found" % res['hits']['total'])

globalSet = list(map(buildVector, res['hits']['hits']))

# print(globalSet)
writeToCsv('dataset/station-1-2_2019-09-25_to_2019-10-10.csv', globalSet)
