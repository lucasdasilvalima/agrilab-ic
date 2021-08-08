const dotenv = require("dotenv");
const apiagdatabox = require("./controller/ApiAgriDataBox");

dotenv.config();

console.log("Inicializando...");
apiagdatabox.authenticate();

require('./controller/Mqtt');
console.log(`Seus logs estãoe em: ${process.cwd()}/.log`);
