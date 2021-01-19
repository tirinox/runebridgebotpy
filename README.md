# runebridgebotpy

Rune ETH Bridge info bot for Telegram

## Commands

```/start``` – start and subscribe

```/stop``` – unsubscribe

```/info``` – request current bridge info

## Installation

0. Clone this repo
1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Copy `example.env` to `.env`
3. Edit `REDIS_PASSWORD` in `.env`
4. Copy `example_config.yaml` to `config.yaml`
5. Edit there the parameter: `telegram.bot.token` (get it from @BotFather)
6. Edit any other parameters if you like
7. Run `make start` and wait until the bot is build and run inside Docker

In brief:
```
cp example.env .env
nano .env
cp example_config.yaml config.yaml
nano config.yaml
make start
```