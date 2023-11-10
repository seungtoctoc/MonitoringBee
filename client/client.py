import subprocess
import time

time.sleep(5)

process = subprocess.Popen(["python3", "/home/stt-pi/shut_down.py"])
process = subprocess.Popen(["python3", "/home/stt-pi/client_capture.py"])
process = subprocess.Popen(["python3", "/home/stt-pi/client_upload.py"])