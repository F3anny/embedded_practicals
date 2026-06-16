// ⚠️ IMPORTANT: must be WebSocket MQTT URL
const brokerUrl = "ws://157.173.101.159:9001/mqtt";
const topic = "temperature/readings";

console.log("Connecting to MQTT...");

const client = mqtt.connect(brokerUrl);

client.on("connect", () => {
    console.log("Connected to MQTT broker ✅");

    document.getElementById("status").innerText = "Connected ✅";

    client.subscribe(topic, (err) => {
        if (err) {
            console.error("Subscribe error:", err);
            document.getElementById("status").innerText = "Subscribe failed ❌";
        } else {
            console.log("Subscribed to:", topic);
        }
    });
});

client.on("message", (topic, message) => {
    console.log("Received:", message.toString());

    try {
        const data = JSON.parse(message.toString());

        // update UI
        document.getElementById("temp").innerText =
            data.temperature + "°C";

        document.getElementById("time").innerText =
            "Last update: " + data.timestamp;

    } catch (e) {
        console.error("JSON error:", e);
    }
});

client.on("error", (err) => {
    console.error("MQTT error:", err);
    document.getElementById("status").innerText = "Error ❌";
});

client.on("close", () => {
    console.log("Disconnected");
    document.getElementById("status").innerText = "Disconnected ❌";
});