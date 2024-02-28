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
    content = message.content;
    attachment = message.attachments.first().url;
    await sendToWebhook(message.guild.name, message.channel.name, author_name, content, attachment);
  }
})

//create a function to send the message to the slack webhook
async function sendToWebhook(server, channel, author_name, message_content, message_attachment) {
  const axios = require('axios');
  newDate = new Date().toLocaleString();;
  try {
    const data = {
      'text': newDate + ": New message on Discord in " + server + ": #" + channel + " by " + author_name + ": " + message_content + "\n" + message_attachment
    };
    await axios.post(webhook, data);
    console.log("Message sent successfully!");
  } catch (error) {
    console.error("Failed to send message:", error);
    throw error;
  }
}

client.login(token);