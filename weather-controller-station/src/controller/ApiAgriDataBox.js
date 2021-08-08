const api = require('../services/API');
const LocalStorage = require('node-localstorage').LocalStorage;
const errorLog = require('../utils/logger').errorlog;
const successlog = require('../utils/logger').successlog;

const CONSTSAPI = require('../consts.json');

const localStorage = new LocalStorage('/tmp/.scrath');

module.exports = {
  authenticate: async () => {
    const keyAPI = localStorage.getItem('api-agdatabox');

    if (!keyAPI) {
      const login = process.env.API_LOGIN;
      const password = process.env.API_PASSWORD;
      const user = { login, password };

      try {
        const response = await api.post('/auth/login', user);
        const { data } = response;
        localStorage.setItem('api-agdatabox', data);
        successlog.info("Authenticate sucess!");
      } catch (error) {
        const { status } = error.response;
        switch (status) {
          case 500:
            errorLog.error("Internal server error!\nCheck: data types, parameter names, parameters passed through the URL and all the data being sent");
          case 401:
            localStorage.clear();
            errorLog.error("Time for your token is expired!");
          default:
            errorLog.error(`Error => status code ${status}`);
        }
      }

    }

  },

  create: async (sensor, data) => {
    const keyAPI = localStorage.getItem('api-agdatabox');
    const { deviceId, dataTypeId, unitOfMeasurement} = CONSTSAPI[sensor];
    const dataJson = JSON.parse(data);

    const value = dataJson[sensor]
    const description = sensor
    const dateTime = `${(new Date().toISOString()).split('.')[0]}-0000` // "2019-01-01T00:00:00-0300"

    const dataPost = {
      value,
      description,
      "geometry": "SRID=4326;POINT(-45.98 -19.56)",
      dateTime,
      sensor: { id: deviceId },
      unitMeasurement: { id: unitOfMeasurement }
    }
    try {
      const response = await api.post("/measurement", dataPost, {headers: { Authorization: keyAPI }});
    } catch (error) {
      const { status } = error.response;
      console.log(error.data);
      switch (status) {
        case 500:
          errorLog.error("Internal server error!\nCheck: data types, parameter names, parameters passed \
                          through the URL and all the data being sent");
          break;
        case 400:
          errorLog.error("Invalid reference ... ");
          break;
        case 401:
          localStorage.clear();
          errorLog.error("Authentication faild");
          break;
        case 403:
          errorLog.error("you cannot acess this references!");
          break;
        default:
          errorLog.error(`HTTP error ${status}`);
      }
    }
  }
}
