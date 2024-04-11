## Discord Watchdog
 This script is used to monitor a specific channel in a discord server for Message Contents, IP addresses, Domains, Email Addresses, and Attachments, then send them to a slack webhook.
### Dependencies
 First, install `node.js`
 Install either `discord.js` or a discord self bot library (against Discord's TOS)
### How to use
 To make it work, create a discord account or bot and a slack workspace.
 Then, create a webhook in the slack workspace and get the discord account or bot in the discord server.

 Also create a `config.json` file with the following content:
 ```
 {
  "token": "your_discord_bot_token",
  "webhook": "your_slack_webhook_url",
  "channelId": "your_discord_channel_id"
 }
 ```

 Run `node .` in the terminal to start the script and it will start monitoring the channel.

 ## Website Watchdog
 This script is used to monitor a specific website page for Email Addresses and Domains and send the results to a slack webhook.
 ### Dependencies
 First install the latest version of [Python](https://www.python.org/).
 Then run 'pip install -r requirements.txt'
 ### How to use
 First find a website and page of that website to monitor (no recursice scraping yet).
 Then, put the url into the url variable.
 Run the code.
 Note: the webhook data is taken from the config.json that is also used by the Discord Watchdog