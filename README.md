# Lets Go
Let’s Go uses computer vision to track the positions of the black and white tokens in the popular board game Go. By representing a board state as a matrix, we can transform the Go board into a step sequencer and melody creator, allowing the two players to create music together that builds as the game progresses. OpenCV processes a live video stream of the Go board captured with an HD webcam, converting the picture to black and white to isolate the white go pieces, then inverting the frame to isolate the black.

We then use OpenCV’s blob detection algorithm to find the center of each game piece on the board. We can interpolate the location of each intersection on the board given the location of the four edges of the board and generate two 13x13 binary matrices representing the current game state. These matrices are sent to Max MSP using Open Sound Control(OSC). Within the Max patch, the matrix of black pieces was used to control a step sequencer of percussion sounds. The matrix of white pieces was split in half, where the left half controlled 7 drone sounds and the right half controlled 6 melody lines.

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
You'll need a webcam shooting an aerial view of the Go board to use as an input to OpenCV. Start up the python script with `python stream_analyze_game.py` and you'll be prompted to click on the four edges of the Go board. Click in the following order: upper left, upper right, lower left, lower right. Then press any key to start the video stream. Make sure the board doesn't move around during gameplay, as this could skew the position calculations. 

Start up the `Lets_Go_Sequencer.maxpat` and turn audio on to start the piece. As you place pieces on the game board, you should see and hear the sequencer in the max patch update accordingly. 
