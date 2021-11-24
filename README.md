# py-sudoku

This sudoku game consists of an update with some added resources of a previously working version.

Initially, the game was modified to come included with only the base game, without any of the original features. Now featuring matplotlib and numpy python libraries, the game was included with:

- A saving option, prompted when exiting an ongoing session;
- A loading prompt will be shown at the start of the game if there's an stored saved game from the last session played;
- A logging service, which all player's moves and session's played in three different files - each has a different purpose;
- An initial prompt appears when initializing the game, asking for the player's name, which is used to store it's stats;
- The stats mentioned can be accessed through the main game interface, showing every move made by the player, including valid, invalid and repeated moves made throught every session stored;
- The stats are shown in two different graphics for a better visualization;

DISCLAIMER: 
main logic imported from https://github.com/packetsss/Sudoku-Solver
