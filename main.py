from __future__ import absolute_import, division, print_function, unicode_literals

from globals import * #Import globals.py like this in every file you need to access the global variables/use the libraries imported there

import os
os.system('cls')

rust_chunk = rust2py.RustChunk(0,0)
rust_chunk.set_block_id(0,0,0,2)
print(rust_chunk.get_block_id(0,0,0))
# print(rust_chunk.set_section(section_id, section_block_array))

colorama.init()
with colorama.colorama_text() :
    print(colorama.Fore.GREEN + "COSbot")
    print(colorama.Fore.WHITE + "By Luuk van Oijen")

bot = Player("77.251.242.236", 25565)

while True :
    bot.fixed_update()
    time.sleep(TICK_S)
