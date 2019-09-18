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

        #Player info
        self.is_connected = False
        self.health = 20
        self.velocity = types.PositionAndLook()
        self.pos_look = types.PositionAndLook()
        self.target_pos_look = types.PositionAndLook() #Only using the position of this, because we can set look instantly, but we can't teleport :p
        self.move_speed = 1 #In Blocks Per Second (BPS)
        self.ready_to_move = False
        self.dimension = 0
        self.entity_id = -1
        self.on_ground = False

        #Client settings
        self.client_settings = serverbound.play.ClientSettingsPacket()
        self.client_settings.locale = "en_GB"
        self.client_settings.view_distance = 4
        self.client_settings.chat_mode = 0
        self.client_settings.chat_colors = True
        self.client_settings.displayed_skin_parts = 0x7F
        self.client_settings.main_hand = 1

        #Initialize velocity
        self.velocity.x = 0
        self.velocity.y = 0
        self.velocity.z = 0
        self.velocity.yaw = 0
        self.velocity.pitch = 0

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
        self.world = World()
        self.chunk_queu = []

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

    def is_on_ground(self) :
        global REGISTRY
        try :
            chunk_x = int(self.pos_look.x / 16)
            chunk_z = int(self.pos_look.z / 16)
            if self.pos_look.x < 0 :
                chunk_x -= 1
            if self.pos_look.z < 0 :
                chunk_z -= 1
            cur_chunk = self.world.get_chunk(chunk_x, chunk_z)
            if cur_chunk :
                local_x = int(self.pos_look.x % 16)
                local_y = int(self.pos_look.y - 0.85) #-0.85 instead of -1 so that it wont glitch out when the y is ever so slightly inside the block
                local_z = int(self.pos_look.z % 16)

                block = cur_chunk.get_block_id(local_x, local_y, local_z)
                print("Cur position: {}; {}; {} - {} - Chunk {}; {}".format(local_x, local_y, local_z, REGISTRY.decode_block(val=block), chunk_x, chunk_z))
                if block > 0 :
                    self.pos_look.y = int(self.pos_look.y)
                    print("true")
                    return True
                else :
                    return False
            else :
                print("No chunk at location {}; {}".format(chunk_x, chunk_z))
        except Exception as e :
            print(e)

        return False

    def fixed_update(self) :
        if self.is_connected and len(self.chunk_queu) :
            self.process_chunk_column_data()
        else :
            self.ready_to_move = True

        if self.is_connected and self.ready_to_move :
            chunk_x = int(self.pos_look.x / 16)
            chunk_z = int(self.pos_look.z / 16)

            self.on_ground = self.is_on_ground()

            self.move_forward(self.move_speed)
            self.set_look(45,0)
            self.calculate_gravity()
            self.apply_velocity()

            packet = serverbound.play.PositionAndLookPacket(position_and_look=self.pos_look, on_ground=self.on_ground)
            self.connection.write_packet(packet)

    def on_player_join_game(self, uuid, playername, gamemode, ping, display_name) :
        #print("Player {} connected.")
        self.world.add_player(uuid, playername, gamemode, ping)
        self.send_chat_packet("Welcome {}! There are currently {} players online".format( playername, self.world.get_player_count() ))

    def on_player_leave_game(self, uuid) :
        playername = self.world.get_player(uuid)["name"]
        self.world.remove_player(uuid)
        self.send_chat_packet("Goodbye {}!".format(playername))

    def on_join_game(self, join_game_packet) :
        print("Connected to a server")
        self.is_connected = True
        self.entity_id = join_game_packet.entity_id
        self.connection.write_packet(self.client_settings, force=True)
        self.connection.register_packet_listener(self.on_chunk_column_data, custom_packets.ChunkColumnDataPacket)
        self.connection.register_packet_listener(self.on_block_change, clientbound.play.BlockChangePacket)

    def on_chat_message(self, chat_packet) :
        #position can tell you if it's from a player, a command or if it's game_info (displayed above the hotbar)
        #TODO: Take a look at the docs
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
            self.on_player_leave_game(action.uuid)
        elif playerlist_item_packet.action_type == clientbound.play.PlayerListItemPacket.Action :
            print("Unknown player action")

    def on_health_update(self, health_packet) :
        self.health = health_packet.health
        # self.send_chat_packet("My health is currently {}".format(self.health))
        if self.health < 1 :
            self.send_chat_packet("I died!")
            self.send_respawn_packet()

    def on_server_difficulty_update(self, difficulty_packet) :
        global DIFFICULTY_LOOKUP
        print("Server difficulty is {}".format(DIFFICULTY_LOOKUP[difficulty_packet.difficulty]))
        self.difficulty = difficulty_packet.difficulty

    def on_disconnect(self, disconnect_packet) :
        print("[#{}] I have been disconnected from the server!".format(self.id))
        print("[#{}] Attempting to reconnect...".format(self.id))
        self.join_game(self.ip, self.port)

    def on_player_pos_look(self, pos_look_packet) :
        # print("pos_look_packet")
        id = pos_look_packet.teleport_id
        self.pos_look.x = pos_look_packet.x
        self.pos_look.y = pos_look_packet.y
        self.pos_look.z = pos_look_packet.z

        #Code below might be needed for teleporting using pearls or something
        # teleport_confirm_packet = serverbound.play.TeleportConfirmPacket()
        # teleport_confirm_packet.teleport_id = id
        # self.connection.write_packet(teleport_confirm_packet)

    def on_chunk_column_data(self, chunk_column_data_packet) :
        self.chunk_queu.append(chunk_column_data_packet)

    def process_chunk_column_data(self) :
        global REPORTS_FOLDER, RENDER_DISTANCE
        chunk_column_data_packet = self.chunk_queu[0]

        raw_data = chunk_column_data_packet.file_object.read()
        buf = Buffer(data=raw_data)
        buf.save()
        x,z, full = buf.unpack("ii?")
        bitmask = buf.unpack_varint()
        heightmap = buf.unpack_nbt()
        size = buf.unpack_varint()

        chunk = Chunk(x, z)

        try :
            for sectionY in range(16) :
                if (bitmask & (1 << sectionY)) != 0 :
                    section = buf.unpack_chunk_section()
                    chunk.set_section(sectionY, section)
        except Exception as e :
            print(e)

        self.world.set_chunk(x, z, chunk)

        self.chunk_queu.pop(0)

    #This shouldn't send data to player, so this is broken
    def on_entity_velocity(self, entity_velocity_packet) :
        if entity_velocity_packet.entity_id == self.entity_id :
            self.velocity.x = entity_velocity_packet.velocity_x
            self.velocity.y = entity_velocity_packet.velocity_y
            self.velocity.z = entity_velocity_packet.velocity_z
            # new_x = self.pos_look.x + entity_velocity_packet.velocity_x
            # new_y = self.pos_look.y + entity_velocity_packet.velocity_y
            # new_z = self.pos_look.z + entity_velocity_packet.velocity_z
            #
            # # send an acknowledgement to the server
            # position_response = serverbound.play.PositionAndLookPacket()
            # position_response.x = new_x
            # position_response.feet_y = new_y
            # position_response.z = new_z
            # position_response.yaw = self.pos_look.yaw
            # position_response.pitch = self.pos_look.pitch
            # position_response.on_ground = self.on_ground
            # self.connection.write_packet(position_response)
            #
            # self.pos_look.x = new_x
            # self.pos_look.y = new_y
            # self.pos_look.z = new_z

    def on_block_change(self, block_change_packet) :
        block = REGISTRY.decode_block(block_change_packet.block_state_id)
        block_x = block_change_packet.location.x
        block_y = block_change_packet.location.y
        block_z = block_change_packet.location.z
        chunk_x = int(block_x / 16)
        chunk_z = int(block_z / 16)
        try :
            self.world.chunk_set_block_id(chunk_x, chunk_z, block_x % 16, block_y, block_z % 16, block_change_packet.block_state_id)
        except Exception as e :
            print(e)
        #print("Block changed: {};{};{} ({};{}) - {}".format( block_x % 16, block_y, block_z % 16, chunk_x, chunk_z, block ))

    #TODO: multi block change
    def on_multi_block_change(self, multi_block_change_packet) :
        return

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
        # self.connection.register_packet_listener(self.on_entity_velocity, clientbound.play.EntityVelocityPacket)

        self.connection.connect()

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
        #Moves forward with <speed> BPS for 1 tick
        look_y_rad = (self.pos_look.yaw + 90) / 180 * math.pi #+90 is forward, sick math
        self.pos_look.x += speed * TICK_S * math.cos(look_y_rad)
        self.pos_look.z += speed * TICK_S * math.sin(look_y_rad)

    def move_backwards(self, speed) :
        global TICK_S
        #Moves backwards with <speed> BPS for 1 tick
        look_y_rad = (self.pos_look.yaw - 90) / 180 * math.pi #-90 is backwards, sick math
        self.pos_look.x += speed * TICK_S * math.cos(look_y_rad)
        self.pos_look.z += speed * TICK_S * math.sin(look_y_rad)

    def strafe_left(self, speed) :
        global TICK_S
        #Strafes left with <speed> BPS for 1 tick
        look_y_rad = (self.pos_look.yaw) / 180 * math.pi #0 is left, sick math
        self.pos_look.x += speed * TICK_S * math.cos(look_y_rad)
        self.pos_look.z += speed * TICK_S * math.sin(look_y_rad)

    def strafe_right(self, speed) :
        global TICK_S
        #Strafes right with <speed> BPS for 1 tick
        look_y_rad = (self.pos_look.yaw + 180) / 180 * math.pi #=180 is left, sick math
        self.pos_look.x += speed * TICK_S * math.cos(look_y_rad)
        self.pos_look.z += speed * TICK_S * math.sin(look_y_rad)

    def calculate_gravity(self) :
        if self.on_ground :
            self.velocity.y = 0
        else :
            self.velocity.y -= 0.08
            self.velocity.y *= 0.98
            # self.velocity.y = max(self.velocity.y, -3.92) #3.92 blocks per tick is the terminal velocity of the player

    def apply_velocity(self) :
        self.pos_look.x += self.velocity.x
        self.pos_look.y += self.velocity.y
        self.pos_look.z += self.velocity.z
