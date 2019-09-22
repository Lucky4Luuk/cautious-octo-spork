#Put global variables here, as well as libraries you need in every file

################################################################################
##  Misc libraries
################################################################################
import colorama
import json
import ast
import math
import time
from collections import namedtuple
import nbt
import sys
import random

import rust2py#; rust2py.initialize()

################################################################################
##  Global variables
################################################################################
login_details = {} #Possibly not needed, but for clarity's sake
with open("login_details.json") as file :
    login_details = json.load(file)
next_available_player_index = 0
TICK_S = 0.01 #0.05 #20 ticks per second, so 1 tick = 0.05 seconds. 0.01 seconds at the start because chunk loading is faster then
TOTAL_TIME = 0
DELTA_TIME = 0
RENDER_DISTANCE = 10 #In chunks
REPORTS_FOLDER = "reports"
DIFFICULTY_LOOKUP = ["PEACEFUL", "EASY", "NORMAL", "HARD"]
OWNER_UUID = "a96278ec-207c-469b-b927-f463e294497d"

################################################################################
##  Machine learning related libraries
################################################################################
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import gym
import pandas as pd

import artificial_intelligence as ai


################################################################################
##  Minecraft related libraries
################################################################################
import getpass
import sys
import re
from optparse import OptionParser

from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection, PlayingReactor
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.networking import types
from minecraft.compat import input
from quarry.types.chunk import BlockArray
from quarry.types.buffer import *
from quarry.types.registry import Registry, LookupRegistry; REGISTRY = LookupRegistry.from_json(REPORTS_FOLDER)
import custom_packets
from chunk import Chunk
from world import World

from mc_control import Player
