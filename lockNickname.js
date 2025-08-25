module.exports = async (api, event, args) => {
  // implement locking via group settings
  api.sendMessage("Nickname lock applied!", event.threadID);
};
