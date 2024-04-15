## Discord Watchdog
 This script is used to monitor a specific channel in a discord server for Message Contents, IP addresses, Domains, Email Addresses, and Attachments, then send them to a slack webhook.
 NOTE: Normal Discord bots have not been tested with the code in this project, your mileage may vary
### Dependencies
 First, install `node.js`
 Go to the directory with the code and run `npm i` in a command line (will install discord.js-selfbot-v13 by default)
 * Or manually install either `discord.js` if you are using a normal bot or a discord self bot library such as `discord.js-selfbot-v13` if you are using a user account (best for OSINT but against Discord's TOS you may get the user account banned)
### How to use
 To make it work, create a discord account or bot and a slack workspace.
 Then, create a webhook in the slack workspace and get the discord account or bot in the discord server.

 Also create a `config.json` file with the following content:
 ```json
 {
  "token": "your_discord_bot_token",
  "webhook": "your_slack_webhook_url",
  "channelId": "your_discord_channel_id"
 }
 ```

 Run `node .` in the terminal to start the script and it will start monitoring the channel.

 ## Website Watchdog
 This script is used to monitor a specific website page for Email Addresses and Domains and send the results to a slack webhook. It will also generate a wordlist of the site and send that to a slack webhook too.
 ### Dependencies
 First install the latest version of [Python](https://www.python.org/).
 Then run `pip install -r requirements.txt` in your preferred command line.
 ### How to use
 First find a website and page of that website to monitor (no recursive scraping yet).
 Then, put the url into the url variable.
 Run the code.
 Note: the webhook data is taken from the `config.json` that is also used by the Discord Watchdog