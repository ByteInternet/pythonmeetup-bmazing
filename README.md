# Python meetup - bmazing challenge
On the Python meetup on 26-04-2017 Byte has launched a bmazing challenge!
You can write your own player and send your github repository to meetup-bmazing@byte.nl.

## Rules
* The player that solves the maze in the least steps wins the game.
* Participants can deliver a single file player by email.
* The start and finish can be anywhere in the field.
* The package is delivered with a standard maze. At the python meetup we will use another maze.
* Byte employees are free to deliver a player but are excluded from winning.
* It is not allowed to access the mazefield object or file. The only way to discover the maze is walk through it and save the surroundings.

## How to use
1. Install requirements:
`pip install -r requirements/play.txt`
1. Write your own player in `./players/{your_playername}.py`.
1. Start the maze to test your player:
`python bmazing.py --player={yourname} --maze={mazename}`

## The Player
The player has one method that is called on every turn, which is called `turn`:
The game will pass te surroundings to this method of the current position in the maze.
The player should be able to walk through the maze with the information of the surroundings.
In each step you gather more information of the layout of the maze.
Your task is to write the best strategy to walk though the maze using Python!

The player is allowed to save previous turns into a data collection to analyse on every turn to decide which way the player walks.

The turn method must return a move (up, down, left or right) to move the player around.
Returning something different or raising an exception will cause that the player will stay on its current position.

## Surroundings
This object has the properties `left`, `right`, `up` and `down`, containing a maze_attribute. 
The attributes can be found in the module `game.mazefield_attributes` and can be used by the player.

## Moves
The moves can be imported from `game.moves` or you could return the string 'up', 'down', 'right' or 'left' to move the player around

## Mazefield Attributes
### Path
The player is allowed to walk over the path

### Wall
This bound the player to the path

### Start
This is the start point of the maze

### Finish
This is the target, and will end the game when the player reaches this attribute
