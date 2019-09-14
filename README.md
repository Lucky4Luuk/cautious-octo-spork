# COSbot
A basic Minecraft bot, made using Machine Learning.

## Basic idea
The basic idea behind the AI improving over time is the following:
 - AI starts off doing random things. All it has is a list of things it can do, ex: press W, move mouse, etc.
 - AI gets a score based on certain factors (see point below).
 - If the AI dies, we stop the AI. If the score doesn't increase a lot, we should probably stop the AI as well.
 - Once the AI has been stopped, we use it's + the score it achieved + world data to train the model again (see point below).
 - Based on the model, the next generation will start.

## To Do
PyCraft-related:
 - [ ] Implement basic server connection
 - [ ] Implement player movement/rotation
 - [ ] Implement block placing/breaking
 - [ ] Implement getting chunk data

AI-related:
 - [ ] Figure out the method of data/training
 - [ ] Record training data
 - [ ] Implement model

## Ideas
Some ideas I still need to think about:
 - It might be best to train several AI at once per generation, and train the model based on the best performing AI.
 - Simply based on random actions, it probably won't get very far. Perhaps train it based on video of people playing Minecraft? It would need to somehow figure out what inputs to execute to do whatever it wants to do. Perhaps I could record my own video footage and also record my inputs and world data. That would require a custom client however (or at least a way to record world data and input and link it to the actual footage), and a lot of playtime on my end.
 - Another way to train the AI could be using player data + world data. It wouldn't need to figure out any inputs, nor do it based on video footage. The outputs could simply be changes it wants to make to the player data, and we could then use some code to figure out what it needs to do to reach the desired player data (ex: AI wants to go from x=50 to x=51, so we would need to figure out how to move to that location)

## Requirements
 - PyCraft
 - TensorFlow
 - Colorama
All these except for PyCraft can be installed using `pip install -r requirements.txt`.
