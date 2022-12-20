# Objective
To recreate the browser based Wordle game for the CLI.

# Definitions
- "Word of the day" (WOTD) - the secret word the user is trying to guess.
- "Guess" - the user's attempt to guess the secret word
  
# Features
- Every day, the system MUST choose a new WOTD that is consistent across distributions of the application. The ability to compete against friends was a huge part of Wordle's success
- The system MUST accept guesses from the user
  - All guesses MUST be 5 letters
  - The system MUST prevent the user from providing more than 6 guesses
- The system MUST provide feedback to the user on how there guess compares to the WOTD. Feedback is similar to the game Mastermind.
  - Letters that are in the word AND in the correct position will be indicated in green
  - Letters that are in the word but NOT in the correct position will be indicated in yellow
  - Letters that are NOT in the word will have no styling
  - If the user guesses a word that repeats the letter, but the letter appears only once in the WOTD, only indicate it once. Ex. `WOTD=COUNT` and `guess=ATTIC`. The letter `T` appears in the guess twice in the wrong position, but only in the WOTD once. Only the first `T` should be indicated in yellow.
