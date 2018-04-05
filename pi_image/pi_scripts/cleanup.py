import os

os.system("sudo sh makeclean.sh")
os.system("sudo pkill -9 station")
os.system("sudo rm -rf ~/.start")
os.system("sudo rm -rf ~/.connection_string.dat")
os.system("sudo rm -rf ~/.interval.dat")
