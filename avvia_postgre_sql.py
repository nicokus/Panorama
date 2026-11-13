import os
import subprocess

os.chdir("20_Docker")
subprocess.run(["docker", "compose", "up", "-d"])