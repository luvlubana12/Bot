const login = require("fca-unofficial");
const fs = require("fs");
const config = require("./config.json");

const appState = JSON.parse(fs.readFileSync("appstate.json", "utf-8"));

login({ appState }, (err, api) => {
    if (err) return console.error("Login Failed:", err);

    api.setOptions({ listenEvents: true, selfListen: false });

    console.log("🤖 Bot is now running...");

    const commandPrefix = config.prefix;
    const adminID = config.adminID;

    const commands = {
        lock: require("./commands/lock"),
        uid: require("./commands/uid"),
        mention: require("./commands/mention"),
        help: require("./commands/help")
    };

    api.listenMqtt((err, event) => {
        if (err) return console.error(err);

        if (event.type !== "message" && event.type !== "message_reply") return;

        const senderID = event.senderID;
        const threadID = event.threadID;
        const message = event.body;

        // Auto-Reply when mentioned
        if (event.mentions && Object.keys(event.mentions).includes(api.getCurrentUserID())) {
            return api.sendMessage(`📌 I'm owned by ${config.ownerName}`, threadID);
        }

        if (!message || !message.startsWith(commandPrefix)) return;

        const args = message.slice(commandPrefix.length).trim().split(/ +/);
        const cmd = args.shift().toLowerCase();

        if (commands[cmd]) {
            if (senderID === adminID) {
                commands[cmd](api, event, args);
            } else {
                api.sendMessage("🚫 You are not authorized to use this command.", threadID);
            }
        }
    });
});
