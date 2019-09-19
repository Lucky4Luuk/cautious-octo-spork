LIB_NAME = "rust2py"

import subprocess
import shutil
import os

subprocess.Popen(["cargo", "build"], cwd="rust-chunk/").communicate()
shutil.copyfile(os.getcwd() + "\\rust-chunk\\target\\debug\\{}.dll".format(LIB_NAME), os.getcwd() + "\\{}.pyd".format(LIB_NAME))
os.system("cls")
print("Done! Scroll up for potential errors!")
