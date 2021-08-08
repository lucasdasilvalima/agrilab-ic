const axios = require('axios');

const api = axios.create({
  baseURL: "http://agdatabox.md.utfpr.edu.br/apidata/v2",
  timeout: 1000,
  headers: {
    "accept": "*/*",
    "Content-Type": "application/json"
  }
});

module.exports = api;