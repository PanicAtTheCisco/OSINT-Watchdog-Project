const { Client } = require('discord.js-selfbot-v13');
const client = new Client();

const {token} = require('./config.json');
const { webhook } = require('./config.json');
const {channelId} = require('./config.json');

client.on('ready', async () => {
  console.log(`${client.user.username} is ready!`);
})

client.on('messageCreate', async (message) => {
  if (message.channel.channelId === channelId) {
    author_name = message.author.username;
    content = message.content;

    if (message.attachments.first()) {
      attachments = message.attachments.map(attachment => "```" + attachment.name + " - " + attachment.contentType + ":\n" + attachment.url + "```").join('\n');
      await sendToWebhook(message.guild.name, message.channel.name, author_name, content, attachments);
    } else {
      attachments = "";
      await sendToWebhook(message.guild.name, message.channel.name, author_name, content, attachments);
    }
  }
})

//create a function to send a message with text and or attachments to the slack webhook
async function sendToWebhook(server, channel, author_name, message_content, message_attachments) {
  const axios = require('axios');
  newDate = new Date().toLocaleString();
  try {
    if (message_content === "") {
      data = {
        'text': ">" + newDate + "\n>`Discord:` New message in `" + server + ": #" + channel + " by " + author_name + "`\n`Attachments:`\n" + message_attachments
      };
    } else if (message_attachments === "") {
      data = {
        'text': ">" + newDate + "\n>`Discord:` New message in `" + server + ": #" + channel + " by " + author_name + "`\n`Message Content:`\n```" + message_content + "```"
      };
    } else {
      data = {
        'text': ">" + newDate + "\n>`Discord:` New message in `" + server + ": #" + channel + " by " + author_name + "`\n`Message Content:`\n```" + message_content + "```\n`Attachments:`\n" + message_attachments
      };
    }
    await axios.post(webhook, data);
    console.log("Message sent successfully!");
  } catch (error) {
    console.error("Failed to send message:", error);
  }
}

client.login(token);