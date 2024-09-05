# Remind

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

A discord bot that sends reminders for future contests using [clist](https://clist.by/) API, fully based on [Remind me](https://github.com/prabh1601/Remind-Me).

## Installation

> **Use Python 3.7 or later.**

(upd : the current code will break on with version >= 3.10 due to usage of recordtype)

Clone the repository:

```bash
git clone https://github.com/prabh1601/Remind-Me
```

### Dependencies

Now all dependencies need to be installed.

Dependencies are listed in [requirements.txt](requirements.txt).

```bash
pip install -r requirements.txt
```

### Final steps

To start `remind`, fill up the variables in [env_file_variables.txt](env_file_variables.txt) and rename it to `.env`.

You will need to setup a bot on your server before continuing. Follow the directions [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token). Following this, you should have your bot appearing in your server and you should have the Discord bot token.

You will need [clist.by](https://clist.by/) api key for updation of contest list. You can find it [here](https://clist.by/api/v1/doc/) after creating an account.

You can also setup a logger channel that logs warnings by assigning the enviornment variable `LOGGING_COG_CHANNEL_ID`. But this is optional.

After following above procedure, fire up the bot with this command in directory

```bash
./run.sh
```

### Deployment

<details>
<summary> As a systemd Service</summary>

Using Systemd Service is very easy method to deploy.

> Please note that you need admin access to the system
> on which you are going deploy the bot. Also this options requires managing services, please only consider this option
> if you know what you are doing.

1. Complete the Above procedure till [Final steps](#Final-steps) and then cd to `etc/systemd/service`
2. Create a file name `remind.service` and paste the below content in it

```
[Unit]
Description=Remind Bot

[Service]
ExecStart=<absolute-path-to-your-bot-directory>/run.sh

[Install]
WantedBy=multi-user.target
```

3. Save the file and run following commands

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now remind
```

4. Upon Success, check the status of bot with `sudo systemctl status remind`.
5. If everything went well, you should be seeing running status of bot.
</details>

<details>
<summary> With Docker </summary>

If you want to just host bot using docker, then you can skip installing dependencies and just follow [Final steps](#Final-steps) and just install Docker [Dockerfile](Dockerfile) will take care of rest.

</details>

### Credits

Shoutout to [TLE](https://github.com/cheran-senthil/TLE) developers for the inspirations. The former used to give updates only for codeforces contest which was expanded to much more sites in this bot.
