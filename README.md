# Lets Go
Let’s Go uses computer vision to track the positions of the black and white tokens in the popular board game Go. By representing a board state as a matrix, we can transform the Go board into a step sequencer and melody creator, allowing the two players to create music together that builds as the game progresses.

## Depencies
* Numpy
* OpenCV
* [Open Sound Control](https://osc.readthedocs.io/en/latest/)
* [Max MSP](https://cycling74.com/)

## Repo Layout
### sounds/
Audio sources for sequencer. Samples for each instrument are combined into a single audio file. Individual samples are then referenced by timestamp in the Max patch.
### stream_analyze_game.py
Python code that analyzes the video stream of the Go game, mapping the game state to two matrices of black and white piece locations. 
### Lets_Go_Sequencer.maxpat
Percussion and melody sequencer. Receives OSC messages of game piece positions from Python to update the sequencer

### How to Use
You'll need a webcam shooting an aerial view of the Go board to use as an input to OpenCV. Start up the python script with `python stream_analyze_game.py` and you'll be prompted to click on the four edges of the Go board. Make sure the board doesn't move around during gameplay, as this could skew the position calculations. 

Start up the `Lets_Go_Sequencer.maxpat` and turn audio on to start the piece. As you place pieces on the game board, you should see and hear the sequencer in the max patch update accordingly. 
