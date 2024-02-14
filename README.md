# DD2480_CI
## Overview
This repository provides Continuous Integration (CI) , where actions in a github repository are automatically tested and results are communicated via discord

## Requirements
- Python == 3.11
- Your ngrok account
   - If you have any other ways, you can use them.
   - However, this README assumes you use ngrok
   - Also, authenticating your ngrok agent on your PC is needed.
- Discord account and server
  - DM is not working.

## Installation
```
git clone https://github.com/lovisastrange/DD2480_CI.git

# Virtual environment if you want
python -m venv venv
source venv/bin/activate
pip install -r requirements
```

## Setup a webhook using GitHub
Go to the settings tab of the considered repository, and under Webhooks, click on “Add webhook”, then enter the payload URL (like https://<YOUR_URL>/server/webhook - you can get an url with ngrok) and set the content type to “application/json”. Choose a webhook secret for request verification and select the relevant events.

### YOUR_URL with ngrok
- You can get your own url from domain page.

## Setting up the environment
Make a `.env` file at the root of the project directory, containing three keys:
- the webhook secret chosen when creating the webhook on GitHub, with name `WEBHOOK_SECRET`
- a GitHub API token, to send build statuses to GitHub (you can get one by going to your GitHub profile settings > developer settings > personal access tokens > tokens (classic) and generate new token (classic)), with name `GITHUB_TOKEN`
- a Discord API token, to send notifications using the discord bot, with name `DISCORD_WEBHOOK`
   - [Reference](https://www.svix.com/resources/guides/how-to-make-webhook-discord/)

## Launching the server
To launch the server, run this command from the src/ folder (for the port, 5000 is restricted on macOS, making it difficult to make it work with ngrok):
```
# Logs can be seen on the terminal window used to run this command.
cd src
flask --app main run --port <PORT>

# example
flask --app main run --port 8000
``` 

Then, if using ngrok, the server can be made accessible using the command (on a different terminal window)
```
ngrok http --domain=<YOUR_URL> <PORT>

# example
ngrok http --domain=<YOUR_URL> 8000
```

Accessing the front-end:
To see the build history on the web browser, go to: “https://<YOUR_URL>/server/”

![front-end.png]

## Assessment of way of working
We still feel like our way of working fulfills the “In place” level of the checklist. The tools that we are using, for example GitHub issues and pull requests, are still working well. More than last time, we have tried to split up larger issues into smaller sub-issues, which has given us some more structure for working on large parts of the projects. To get to the “Working well”-level, we still need to become more comfortable with the way of working that we are using. We would also need to do even more evaluating and adjusting of how we are using the tools we have to best help us work together. For example, before the next assignment, we should evaluate our use of sub-issues to see if they helped our workflow, and if we should continue to use them.

## Statement of contributions
* Eloi Dieme: Initialized the Flask app, the repo directory structure and the test fixtures. Configured logging, documentation generation and GitHub Actions on the repo. Implemented the front-end for build history, reviewed code and merged pull requests. Participated in writing the README file.

* Hugo Malmberg: Implemented webhook handler class to verify and parse data. Implemented a discord bot to handle notifications and later replaced said bot with a webhook.
 
* Olivia Aronsson: 

* Lovisa Strange: Set up and implemented syntax checking for the code and corresponding tests. Wrote code and tests for automatically running tests on the code that did not end up being used due to accidentally double assigning an issue. Participated in reviewing code by other group members and in writing README file and wrote assessment of way of working.

* Yuta Ojima: Implemented Database to store history log, Refactoring, Organized this README file.

