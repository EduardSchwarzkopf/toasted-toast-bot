# Toasted Toast B(r)ot 🍞

This is a Discord bot built using the discord.py library. It serves as a case-study and a boilerplate bot for people who want to get started with building their own Discord bots.

## Features

The bot currently supports the following features:

1. Loading, unloading, and reloading bot extensions on the fly. Extensions are a way to enhance your bot's capabilities without making significant changes to the main bot code. You need to be the owner of the bot to use these commands.

2. The bot uses the command decorator model for easy command creation and management.

3. The bot logs activity to a specific Discord channel. The ID of this channel is set with the `LOGGING_CHANNEL_ID` environment variable.

## Setup without Docker

1. Make sure you have Python 3.8 or later installed on your machine. You can verify this by running `python --version` or `python3 --version`.

2. Install the required libraries by running `pip install -r requirements.txt`.

3. Set up a bot on the Discord developer portal, get the bot token, and add the bot to your server.

4. In the root directory of the project, create a `.env` file and add your bot token and logging channel ID like this: 

```
DISCORD_TOKEN=your-bot-token
LOGGING_CHANNEL_ID=your-logging-channel-id
```

5. Run `python bot.py` to start the bot.

## Setup with Docker

1. Make sure you have Docker installed on your machine. You can verify this by running `docker --version`.

2. Build the Docker image by running `docker build -t toasted-toast-bot .`.

3. Run the Docker image with your bot token and logging channel ID: 
   ``` 
   docker run \
    -e DISCORD_TOKEN=your-bot-token \
    -e LOGGING_CHANNEL_ID=your-logging-channel-id \
    toasted-toast-bot
   ```

## Contributing

Feel free to use this bot as a starting point for your own projects. If you make any improvements or add any interesting features, consider making a pull request to share them.

## License

This project is licensed under the MIT License.