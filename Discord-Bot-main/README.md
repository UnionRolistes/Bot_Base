# Discord-Bot
 [doc lib](https://discordpy.readthedocs.io/en/stable/api.html?highlight=on_message#discord.Guild.get_channel)

## Instalation

- Install [Docker](https://docs.docker.com/desktop/) (only need engine and compose)
- dowload repo


## first use (or if you want to change the token)

- [tuto](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to get your token
- change the token in the .env file

## use

- start : `docker-compose up --build -d` (in terminal in path of the project)
- log : `docker-compose logs -f` (in terminal in path of the project)
- stop : `docker-compose down` (in terminal in path of the project)

## use other repo to extend the bot

- go to parent folder of the bot
- clone repo needed
- merge docker-compose with `docker-compose -f docker-compose.yml -f ../repo-x/docker-compose.yml config > docker-compose-merge.yml`
  > add `-f repo-y/docker-compose.yml` for each repo
- start command here

## Commandes disponible dans le bot base

- `$help` : show all command available
- `$ping` : show pong and time to respond  ( test if bot is alive )
