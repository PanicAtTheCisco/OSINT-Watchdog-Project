//server name, channel name instead of id, add timestamps, and newline url

const { Client } = require('discord.js-selfbot-v13');
const client = new Client();

const {token} = require('./config.json');
const {channelId} = require('./config.json');
const { webhook } = require('./config.json');

client.on('ready', async () => {
  console.log(`${client.user.username} is ready!`);
})

client.on('messageCreate', async (message) => {
  if (message.channel.channelId === channelId && message.attachments.size > 0) {
    author_name = message.author.username;
    content = message.attachments.first().url;
    await sendToWebhook(channelId, author_name, content);
  }
})

//create a function to send the message to the slack webhook
async function sendToWebhook(channel_id, author_name, message_content) {
  const axios = require('axios');
  try {
    const data = {
      'text': "New message on Discord in #" + channel_id + " by " + author_name + ": " + message_content
    };
    await axios.post(webhook, data);
    console.log("Message sent successfully!");
  } catch (error) {
    console.error("Failed to send message:", error);
    throw error;
  }
}

client.login(token);