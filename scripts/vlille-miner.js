require('dotenv').config();

const request = require("request");
const elasticsearch = require('elasticsearch');

const esClient = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'info'
});

const VLILLE_URL = `${process.env.VLILLE_API_BASE}&rows=-1&apikey=${process.env.VLILLE_API_KEY}`;
const ELASTIC_INDEX = process.env.ES_INDEX;
// const ELASTIC_INDEX = 'demo';

request(VLILLE_URL, { json: true }, (error, response, body) => {
  if (error) {
    throw error;
  }

  if (!body.records) {
    throw "No data";
  }

  // formats entries
  const data = prepareData(body);

  // manage data insertion
  storeDataToES(data);
});

/**
 * Removes useless data from dataset
 *
 * @param {Array} data
 */
function prepareData(data) {
  // console.debug(data.records[0])

  return data.records.map(record => {
    return {
      timestamp: record.record_timestamp,
      id: record.fields.libelle,
      bikes: record.fields.nbvelosdispo,
      docks: record.fields.nbplacesdispo,
      status: record.fields.etat,
      connexionStatus: record.fields.etatconnexion
    };
  });
}

/**
 * Perform ES indexation bulk request
 *
 * @param {Array} data
 */
async function storeDataToES(data) {
  try {
    const response = await esClient.bulk({
      body: prepareEsBodyRequest(data)
    });

    // console.debug(response.items)
  } catch (error) {
    console.trace(error.message)
  }
}

/**
 * Prepare data to indexation format for ES
 * @param {Array} data
 */
function prepareEsBodyRequest(data) {
  const body = [];

  data.forEach(element => {
    body.push({
      index:  {
        _index: ELASTIC_INDEX,
        _type: '_doc'
      }
    });
    body.push(element);
  });

  return body;
}