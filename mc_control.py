#I wanted to name this minecraft.py, but the library is imported under the name 'minecraft' so I couldn't :(

from globals import *

# Using info from: https://github.com/ammaraskar/pyCraft/commit/9a715a72b868edf5ad4785f1965b4fee9e155ada
def translate_color_code(c) :
    if   c == "0": return colorama.Style.RESET_ALL + colorama.Fore.BLACK # black
    elif c == "1": return colorama.Style.DIM + colorama.Fore.BLUE # dark blue
    elif c == "2": return colorama.Style.DIM + colorama.Fore.GREEN # dark green
    elif c == "3": return colorama.Style.DIM + colorama.Fore.CYAN # dark cyan
    elif c == "4": return colorama.Style.DIM + colorama.Fore.RED # dark red
    elif c == "5": return colorama.Style.DIM + colorama.Fore.MAGENTA # purple
    elif c == "6": return colorama.Style.RESET_ALL + colorama.Fore.YELLOW # gold
    elif c == "7": return "\x1b[37m\x1b[21m" # gray
    elif c == "8": return "\x1b[30m\x1b[1m"  # dark gray
    elif c == "9": return "\x1b[34m\x1b[1m"  # blue
    elif c == "a": return "\x1b[32m\x1b[1m"  # bright green
    elif c == "b": return "\x1b[36m\x1b[1m"  # cyan
    elif c == "c": return "\x1b[31m\x1b[1m"  # red
    elif c == "d": return "\x1b[35m\x1b[1m"  # pink
    elif c == "e": return "\x1b[33m\x1b[1m"  # yellow
    elif c == "f": return "\x1b[37m\x1b[1m"  # white
    elif c == "k": return "\x1b[5m"          # random
    elif c == "l": return "\x1b[1m"          # bold
    elif c == "m": return "\x1b[9m"          # strikethrough (escape code not widely supported)
    elif c == "n": return "\x1b[4m"          # underline
    elif c == "o": return "\x1b[3m"          # italic (escape code not widely supported)
    elif c == "r": return "\x1b[0m"          # reset

    return ""

def translate_color_codes(msg) :
    return re.sub(r"\xa7([0-9a-zA-Z])", translate_color_code, s) + colorama.Fore.RESET

def extract_chat_data(chat_data) :
    json_data = json.loads(chat_data)
    result_data = {}
    tmp_data = json_data["with"]
    #tmp_data (from my testing at least) always has 2 items, 1 is a dict and the other one is a string
    #The order of these 2 items is unknown, so we simply test the type of the first item to determine which is what
    data_index = 1
    if type(tmp_data[0]) == type({}) :
        data_index = 0

    text = tmp_data[data_index]["hoverEvent"]["value"]["text"].replace("'", "").replace("name", "\"name\"").replace("id", "\"id\"").replace("type", "\"type\"")
    text = json.loads(text)

    result_data["username"] = text["name"]["text"]
    result_data["uuid"]     = text["id"]
    result_data["color"]    = colorama.Fore.RESET

    try :
        result_data["msg"]  = tmp_data[abs(data_index-1)]
    except Exception as e :
        result_data["msg"]  = json_data["translate"]

    try :
        if json_data["color"] == "yellow" : result_data["color"] = colorama.Fore.YELLOW
    except Exception :
        pass

    return result_data

class Player() :
    def __init__(self, ip, port) :
        global RENDER_DISTANCE
        self.authenticate()
        print("Logged in as %s..." % self.auth_token.username)

        #self.buf = Buffer()
        self.reg = LookupRegistry.from_json(REPORTS_FOLDER)

        #Player info
        self.is_connected = False
        self.health = 20
        self.pos_look = types.PositionAndLook()
        self.target_pos_look = types.PositionAndLook() #Only using the position of this, because we can set look instantly, but we can't teleport :p
        self.move_speed = 1 #In Blocks Per Second (BPS)
        self.ready_to_move = False
        self.dimension = 0

        #Client settings
        self.client_settings = serverbound.play.ClientSettingsPacket()
        self.client_settings.locale = "en-US"
        self.client_settings.view_distance = RENDER_DISTANCE
        self.client_settings.chat_mode = 0
        self.client_settings.chat_colors = True
        self.client_settings.displayed_skin_parts = 1
        self.client_settings.main_hand = 0

        #Initialize pos_look
        self.pos_look.x = 0
        self.pos_look.y = 0
        self.pos_look.z = 0
        self.pos_look.yaw = 0
        self.pos_look.pitch = 0

        #Initialize target_pos_look
        self.target_pos_look.x = 0
        self.target_pos_look.y = 0
        self.target_pos_look.z = 0
        self.target_pos_look.yaw = 0
        self.target_pos_look.pitch = 0

        #Server info
        self.difficulty = 0

        #World info
        self.chunks = []
        for i in range(RENDER_DISTANCE) :
            self.chunks.append([])

        self.ip = ip
        self.port = port
        self.join_game(ip, port)

        print("Player {} initialized".format(self.id))

    def authenticate(self) :
        global next_available_player_index, login_details
        self.auth_token = authentication.AuthenticationToken()
        try :
            self.auth_token.authenticate(login_details[next_available_player_index]["email"], login_details[next_available_player_index]["passwd"])
            self.id = next_available_player_index
            self.email = login_details[next_available_player_index]["email"]
            self.passwd = login_details[next_available_player_index]["passwd"]
            next_available_player_index += 1
        except YggdrasilError as e :
            print(e)
            print("Trying next account...")
            next_available_player_index += 1
            self.authenticate()
        except Exception as e :
            print(e)
            sys.exit()

    def fixed_update(self) :
        self.move_forward(self.move_speed)
        self.set_look(0,0)

        self.apply_gravity()

    def update(self) :
        return

    def on_player_join_game(self, uuid, playername, gamemode, ping, display_name) :
        #print("Player {} connected.")
        self.send_chat_packet("Welcome {}".format(playername))

    def on_join_game(self, join_game_packet) :
        print("Connected to a server!")

    def on_chat_message(self, chat_packet) :
        #position can tell you if it's from a player, a command or if it's game_info (displayed above the hotbar)
        #Take a look at the docs
        if chat_packet.position == 0 :
            data = extract_chat_data(chat_packet.json_data)
            msg = data["msg"]
            print("{2}<{0}> {1}".format(data["username"], msg, data["color"]))

    def on_playerlist_info(self, playerlist_item_packet) :
        action = playerlist_item_packet.actions[0] # I haven't found a single instance yet where multiple actions were sent at the same time

        if playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.AddPlayerAction :
            self.on_player_join_game(action.uuid, action.name, action.gamemode, action.ping, action.display_name)
        elif playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.UpdateGameModeAction :
            print("Player updated gamemode")
        elif playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.UpdateLatencyAction :
            print("Player updated ping")
        elif playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.UpdateDisplayNameAction :
            print("Player updated display name")
        elif playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.RemovePlayerAction :
            print("Player left game")
        elif playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.Action :
            print("Unknown player action")

    def on_health_update(self, health_packet) :
        self.health = health_packet.health
        #self.send_chat_packet("My health is currently {}".format(self.health))
        if self.health < 1 :
            self.send_chat_packet("I died!")
            self.send_respawn_packet()

    def on_server_difficulty_update(self, difficulty_packet) :
        print("Server difficult is {}".format(difficulty_packet.difficulty))
        self.difficulty = difficulty_packet.difficulty

    def on_disconnect(self, disconnect_packet) :
        print("[#{}] I have been disconnected from the server!".format(self.id))
        print("[#{}] Attempting to reconnect...".format(self.id))
        self.join_game(self.ip, self.port)

    def on_player_pos_look(self, pos_look_packet) :
        pos_look_packet.apply(self.pos_look)
        self.ready_to_move = True

    def on_chunk_section_data(self, chunk_section_data_packet) :
        #print("Received chunk data for chunk {};{}".format(chunk_data_packet.x, chunk_data_packet.z))
        return

    def on_chunk_column_data(self, chunk_column_data_packet) :
        global REPORTS_FOLDER
        raw_data = chunk_column_data_packet.file_object.read()
        buf = Buffer(data=raw_data)
        buf.save()
        x,z, full = buf.unpack("ii?")
        bitmask = buf.unpack_varint()
        heightmap = buf.unpack_nbt()
        size = buf.unpack_varint()
        try :
            block_array = buf.unpack_chunk_section()
            for i in range(len(block_array)) :
                try :
                    if block_array[i] > 0 :
                        print(block_array[i])
                        block = self.reg.decode_block(val=block_array[i])
                        print(block)
                    #if block == block_array[i] :
                    #    print("useless")
                except Exception as e :
                    print(e)
                    #print("block_array[{}] was empty".format(i))
                    pass
        except Exception as e :
            #print(e)
            pass

    def join_game(self, ip, port) :
        self.connection = Connection(
            ip, port, auth_token=self.auth_token)

        self.connection.register_packet_listener(self.on_join_game, clientbound.play.JoinGamePacket)
        self.connection.register_packet_listener(self.on_chat_message, clientbound.play.ChatMessagePacket)
        self.connection.register_packet_listener(self.on_playerlist_info, clientbound.play.PlayerListItemPacket)
        self.connection.register_packet_listener(self.on_health_update, clientbound.play.UpdateHealthPacket)
        self.connection.register_packet_listener(self.on_server_difficulty_update, clientbound.play.ServerDifficultyPacket)
        self.connection.register_packet_listener(self.on_disconnect, clientbound.play.DisconnectPacket)
        self.connection.register_packet_listener(self.on_player_pos_look, clientbound.play.PlayerPositionAndLookPacket)
        # self.connection.register_packet_listener(self.on_chunk_section_data, custom_packets.ChunkSectionDataPacket)
        self.connection.register_packet_listener(self.on_chunk_column_data, custom_packets.ChunkColumnDataPacket)

        self.connection.connect()

        self.is_connected = True

        self.connection.write_packet(self.client_settings)

    def send_respawn_packet(self) :
        packet = serverbound.play.ClientStatusPacket()
        packet.action_id = serverbound.play.ClientStatusPacket.RESPAWN
        self.connection.write_packet(packet)

    def send_chat_packet(self, msg) :
        packet = serverbound.play.ChatPacket()
        packet.message = msg
        self.connection.write_packet(packet)

    def move_relative(self, x,y,z) :
        self.target_pos_look = self.pos_look
        self.target_pos_look.x += x
        self.target_pos_look.y += y
        self.target_pos.look.z += z

    def set_look(self, x, y) :
        if self.is_connected and self.ready_to_move :
            self.pos_look.look = x, y #0, 0 is forward facing North
            packet = serverbound.play.PositionAndLookPacket(position_and_look=self.pos_look, on_ground=True)
            self.connection.write_packet(packet)

################################################################################
    def move_forward(self, speed) :
        global TICK_S
        if self.is_connected and self.ready_to_move :
            #Moves forward with <speed> BPS for 1 tick
            look_y_rad = (self.pos_look.yaw - 90) / 180 * math.pi
            self.pos_look.x += speed * TICK_S * math.cos(look_y_rad)
            self.pos_look.z += speed * TICK_S * math.sin(look_y_rad)

            packet = serverbound.play.PositionAndLookPacket(position_and_look=self.pos_look, on_ground=True)
            self.connection.write_packet(packet)

    def apply_gravity(self) :
        print("nope")
