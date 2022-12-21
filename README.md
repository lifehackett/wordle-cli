# Wordle
Welcome to the CLI version of Wordle! If you aren't familiar with the classic browser version, check out the [rules](./product_requirements_doc.md).

# How to Play
1. Install Python 3.11. Suggest using [pyenv](https://github.com/pyenv/pyenv)
   1. Note make sure you are actually using this version `python --version` and `which python` can help
2. Install [Poetry](https://python-poetry.org/docs/#installation)
3. `poetry shell`
4. `poetry install`
5. `poetry run wordle guess <YOUR_GUESS>`

# Contributing
## cli.py
This is the public interface of the application. Keep it lightweight and focused on receiving input and displaying output to the user. It uses the [Click library](https://click.palletsprojects.com/)

## wordle.py
This is where the business logic lives. It encapsulates the rules of the game.

## wordle_results.py
This is the persistence layer of the application

## Testing
`poetry run pytest` - run the tests

# Feature Enhancements
- Add support for streak metrics
- Add support for advanced mode
- Add check for invalid words (e.g. "ABCDE" is not a word)
- Sharing the results

# Acknowledgements
- Josh Wardle for creating the original game
- [arjvik](https://dagshub.com/arjvik/wordle-wordlist) For providing the wordlist
