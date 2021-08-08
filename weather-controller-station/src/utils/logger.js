const winston = require('winston');

const fileErrorConfig = [
  new winston.transports.File({
	  filename: '.log/error.log', level: 'error'
  })
];

const fileInfoConfig = [
  new winston.transports.File({
	  filename: '.log/info.log', level: 'info'
  })
];

const successLogger = winston.createLogger({
  'name': 'access-file',
  'level': 'info',
  'filename': '../logs/access.log',
  //'format': winston.format.json(),
  'datePattern': 'dd=MM-yyyy-',
  'prepend': true,
   transports: fileInfoConfig,
});

const errorLogger = winston.createLogger({
  'name': 'error-file',
  'level': 'error',
  'filename': '../logs/error.log',
  //'format': winston.format.json(),
  'datePattern': 'dd-MM-yyyy-',
  'prepend': true,
   transports: fileErrorConfig,
});

module.exports = {
  'successlog': successLogger,
  'errorlog': errorLogger
};
