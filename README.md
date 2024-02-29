## How to use
 * This script is used to monitor a specific channel in a discord server and send the messages to a slack webhook.  

 * First, install `node.js`
 * Install either `discord.js` or a discord self bot library (against Discord's TOS)  

 * To make it work, create a discord account or bot and a slack workspace.
 * Then, create a webhook in the slack workspace and get the discord account or bot in the discord server.  

 * Also create a `config.json` file with the following content:
 * {
 *  "token": "your_discord_bot_token",
 * "webhook": "your_slack_webhook_url",
 * "channelId": "your_discord_channel_id"
 * }  

 * Run `node .` in the terminal to start the script and it will start monitoring the channel.