import subprocess
import time

processes = []

time.sleep(5)

process = subprocess.Popen(["python3", "/home/stt-pi/client_capture.py"])
processes.append(process)

time.sleep(5)

process = subprocess.Popen(["python3", "/home/stt-pi/shut_down.py"])
processes.append(process)

process = subprocess.Popen(["python3", "/home/stt-pi/client_upload.py"])
processes.append(process)

# 각 프로세스가 실행 완료될 때까지 대기
for process in processes:
    process.wait()