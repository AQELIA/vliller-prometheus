require('dotenv').config();

const request = require("request");

const url = `${process.env.VLILLE_API_BASE}&rows=-1&apikey=${process.env.VLILLE_API_KEY}`;

request(url, { json: true }, (error, response, body) => {
  if (error) {
    throw error;
  }

  if (!body.records) {
    throw "No data";
  }

  // formats entries
  const data = prepareData(body);

  // manage data insertion
  // storeDataToDb(data, db);
  console.debug(data);
});

// TODO refactor with ES
function storeDataToDb(data, db) {

  // count data insertion
  leftInsertCount = data.length;

  // insert entries into database
  data.forEach(element => {
    db.collection("station-" + element.id).insert(element, error => {
      if (error) {
        throw error;
      }

      // all data stored
      if (--leftInsertCount === 0) {
        db.close();
        process.exit(0);
      }
    });
  });
}

/**
 * Removes useless data from dataset
 *
 * @param {Array} data
 */
function prepareData(data) {
  return data.records.map(record => {
    return {
      id: record.fields.libelle,
      date: new Date(record.record_timestamp),
      bikes: record.fields.nbVelosDispo,
      docks: record.fields.nbPlacesDispo,
      status: record.fields.etat,
      connexionStatus: record.fields.etatConnexion
    };
  });
}