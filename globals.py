#Put global variables here, as well as libraries you need in every file

################################################################################
##  Misc libraries
################################################################################
import colorama
import json
import ast
import math
import time

################################################################################
##  Global variables
################################################################################
login_details = {} #Possibly not needed, but for clarity's sake
with open("login_details.json") as file :
    login_details = json.load(file)
next_available_player_index = 0
TICK_S = 0.05 #20 ticks per second, so 1 tick = 0.05 seconds
TOTAL_TIME = 0
DELTA_TIME = 0

################################################################################
##  Machine learning related libraries
################################################################################

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt


################################################################################
##  Minecraft related libraries
################################################################################
import getpass
import sys
import re
from optparse import OptionParser

from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.networking import types
from minecraft.compat import input

from mc_control import Player
