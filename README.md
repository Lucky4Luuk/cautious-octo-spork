# COSbot
A basic Minecraft bot, made using Machine Learning.

## AI
The AI will be curiosity driven. Death will be the main punishment.

## To Do
This can be found on my Trello board: https://trello.com/b/gF0f5gXj/cosbot


## Requirements
Python 3.7
Rust (see <b>Compiling the Rust library</b>)

 - Future
 - PyCraft
 - TensorFlow
 - Colorama
 - NBT
 - Quarry
 - Matplotlib
 - Requests

All these except for PyCraft (and Python) can be installed using `pip install -r requirements.txt`.

## Compiling the Rust library
Install the latest version of Rust (preferably using rustup, also install cargo) and make sure you can run Python 3.7 from the terminal using either `python` or `python3`.
If that doesn't work, edit your path to point towards Python. You can find instructions for this online.
After you've done this, open the terminal in the `rust-chunk` folder and run `cargo build`. The compiled library can be found in `rust-chunk/target/debug/`.
The default name is `rust2py.dll`. Copy this file to the root folder of the bot and rename it to `rust2py.pyd`.

Alternatively, you could use `compile.py` script to do this for you. Simply open the terminal in the root folder of the bot and type `python compile.py`.
The downside to this method is that the Rust error might not be fully printed. It seems to get cut off at a certain point, but I will look into this in the future.
