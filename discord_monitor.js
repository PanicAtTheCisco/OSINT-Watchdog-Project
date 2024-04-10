const { Client } = require('discord.js-selfbot-v13');
const client = new Client();

const { token } = require('./config.json');
const { webhook } = require('./config.json');
const { channelId } = require('./config.json');

client.on('ready', async () => {
  console.log(`${client.user.username} is ready!`);
})

client.on('messageCreate', async (message) => {
  if (message.channel.id === channelId) {
    author_name = message.author.username;
    server = message.guild.name;
    channel_name = message.channel.name;

    if (message.content === "") {
      content = "";
    } else {
      content = "```" + message.content + "```";
    }

    if (message.attachments.first()) {
      attachments = message.attachments.map(attachment => "```" + attachment.name + " - " + attachment.contentType + ":\n" + attachment.url + "```").join('\n');
      await sendToWebhook(server, channel_name, author_name, content, attachments);
    } else {
      attachments = "";
      await sendToWebhook(server, channel_name, author_name, content, attachments);
    }
  }
})

//create a function to send a message with text and or attachments to the slack webhook
async function sendToWebhook(server, channel, author_name, message_content, message_attachments) {
  const axios = require('axios');
  const { isIP } = require('net');
  newDate = new Date().toLocaleString();
  ips = "";
  domains = "";

  const ipRegex = /\b(?:\d{1,3}\.){3}\d{1,3}\b/g;
  const ipArray = message_content.match(ipRegex) || [];
  const validIpArray = ipArray.filter(ip => {
    const parts = ip.split('.');
    return parts.every(part => parseInt(part, 10) >= 1 && parseInt(part, 10) <= 255);
  });

  const domainRegex = /(?:[a-z]+\.[a-z]{2,})/gi;
  domainArray = message_content.match(domainRegex) || [];

  if (ipArray.length !== 0) {
    ips = "```" + validIpArray.join("\n") + "```";
  }
  if (domainArray.length !== 0) {
    domains = "```" + domainArray.join("\n") + "```";
  }

  try {
    data = {
      "text": "New message in Discord!",
      "blocks": [
        {
          "type": "section",
          "block_id": "header",
          'text': {
            "type": "mrkdwn",
            "text": ">" + newDate + "\n>`Discord:` New message in `" + server + ": #" + channel + " by " + author_name + "`"
          }
        },
        {
          "type": "section",
          "block_id": "content",
          "text": {
            "type": "mrkdwn",
            "text": "\n`Message Content:`\n" + message_content
          }
        },
        {
          "type": "section",
          "block_id": "ip",
          "text": {
            "type": "mrkdwn",
            "text": "\n`IP Addresses:`\n" + ips
          }
        },
        {
          "type": "section",
          "block_id": "domain",
          "text": {
            "type": "mrkdwn",
            "text": "\n`Domains:`\n" + domains
          }
        },
        {
          "type": "section",
          "block_id": "attachments",
          "text": {
            "type": "mrkdwn",
            "text": "\n`Attachments:`\n" + message_attachments
          }
        }
      ]
    };
    await axios.post(webhook, data);
    console.log("Message sent successfully!");
  } catch (error) {
    console.error("Failed to send message:", error);
  }
}

client.login(token);