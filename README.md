# Arena-Gladiator

This project is a bot designed to play **Magic: The Gathering Arena**, optimized for fast daily wins using a monocolor deck with creature-only spells.

## Features

- **Monocolor Decks Only**: The bot is designed to play monocolor decks that consist exclusively of creature spells, with no additional effects.
- **Simple Combat Strategy**: The bot doesn't block and only attacks with creatures that will, at minimum, trade 1-for-1 with the opponent's creatures.
- **Game Mode Automation**: It plays the last selected game mode and uses the last selected deck, looping until the specified number of wins is achieved, then shuts down (if this option is selected).
- **Error Handling**: If the bot can't correctly press a button, it could be due to resolution issues. This can be fixed by setting the game to **windowed mode** and adjusting the resolution to **1080p**.
- **Time-out to Prevent Bans**: If the bot is unable to resolve any requested action within 30 seconds, it will concede the match to avoid being flagged for inactivity. Therefore, it's recommended to use aggressive decks to win before reaching such requests.

## Recommended Setup

- **Recommended Game Mode**: The fastest way to earn daily wins is by using the **Brawl** mode with the following deck:
    Commander
    1 Marrow-Gnawer (J21) 59
    
    Deck
    54 Rat Colony (DAR) 101
    45 Swamp (GRN) 262

## Requirements

1. Enable **Detailed Logs** in the **Account** section of the game menu.
2. Start the bot from the **Home** menu of Magic Arena.
3. If you need to stop the bot, press **Esc** and then restart the application, otherwise errors may occur (this will be fixed in future updates).

## Known Issues

- The bot may have difficulty interacting with the game's buttons if the screen resolution is not set correctly. Make sure to use **windowed mode** at **1080p** for optimal performance.

## License

This project is licensed under **No Restrictions**. You are free to use, modify, and distribute this bot without any limitations.

## Disclaimer

I am not responsible for any potential consequences or issues caused by using this bot.

Enjoy the bot and feel free to report any bugs or suggest improvements!

## Dependencies

The bot uses the following Python libraries:
- `keyboard`
- `numpy`
- `opencv-python`
- `pillow`
- `PyDirectInput`
- `pynput`
- `pywin32`

To install all the required dependencies, you can use the provided `requirements.txt` file. Run the following command:

```bash
pip install -r requirements.txt
