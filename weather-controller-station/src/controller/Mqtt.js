const mqtt = require('mqtt');
const client = mqtt.connect(process.env.MQTT_URL, {
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD
});
const apiController = require('./ApiAgriDataBox');

client.on("connect", function () {
  client.subscribe("agristation/#", function (err) {
    if (!err) {
      client.publish("agristation/chat", "Initializing");
    }
  })
})

client.on("message", function (topic, message) {
  const msgString = message.toString();

  const [_, subTopic] = topic.split('/');
  if (subTopic === "chat") {
    switch (msgString) {
      case "shutdown":
        client.end();
        break;
      default:
        console.log("Apenas um teste para controlar este dispositivo ;)");
    }
  }
  else {
    apiController.create(subTopic, msgString);
  }
})
