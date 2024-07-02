import subprocess
import threading
import os
import time

def execute_command(path, command):
    print(f'Executing proceess {command}')
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, cwd=path)

    # Check for initial startup errors (not foolproof, as the process can still fail after startup)
    if process.poll():
        error = process.stderr.read().decode()
        print(f"Error: {error}")
        raise subprocess.CalledProcessError(process.returncode, command)

def execute_gazepoint():
    # Kill any running Gazepoint Control applications
    os.system("taskkill /IM Gazepoint.exe /F")
    # Start Gazepoint Control application
    execute_command("C:/Program Files (x86)/Gazepoint/Gazepoint/bin64/", "Gazepoint.exe")

def execute_lab_recorder(config_file=None):
    os.system("taskkill /IM LabRecorder.exe /F")

    
    command = "LabRecorder.exe"
    if config_file:
        command += f" -c {config_file}"
    execute_command("C:/Users/Cocudata/Desktop/LabRecorder", command)


# def execute_stream_viewer():
#     os.system("taskkill /IM lsl_viewer.exe /F")
#     # execute_command("C:/Users/cocud/anaconda3/Scripts/", "lsl_viewer.exe")
    
#     # execute_command("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/BrainVision/", "BrainVision LSL Viewer")
#     path  = "C:/Program Files/BrainVision LSL Viewer/"
#     execute_command(path, "python RunLSLViewer.py")



def execute_brainamp_connector(config_file=None):
    os.system("taskkill /IM BrainAmpSeries.exe /F")

    
    command = "BrainAmpSeries.exe"
    if config_file:
        command += f" -c {config_file}"
    execute_command("C:/Users/Cocudata/BrainAmpSeries/bin/", command)


def execute_eye_tracker_stream():


    # Start gp3-to-lsl.py Python script
    # execute_command("C:/Users/cocud/Documents/lsl-gp3/", "python gp3-to-lsl.py")
    
    command = "python gp3-to-lsl.py"
    path = "C:/Users/Cocudata/Documents/lsl-gp3/"
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd = path)
    output, error = process.communicate()
    

if __name__ == "__main__":
    try:
        #GPthread = threading.Thread(target=execute_gazepoint)
        LRthread = threading.Thread(target=execute_lab_recorder, args=("LabRecorder - Copy.cfg",))
        # SVthread = threading.Thread(target=execute_stream_viewer)
        #ETthread = threading.Thread(target=execute_eye_tracker_stream)
        BAthread = threading.Thread(target=execute_brainamp_connector, args=(["C:/Users/Cocudata/experiment_VR/mw_lsl_42chs.cfg"]))
        
        # Start the threads
        #GPthread.start()
        LRthread.start()

        time.sleep(5)
        BAthread.start()
        #ETthread.start()
        # SVthread.start()

        # No need to join the threads if you want the Python script to exit without waiting for the external processes
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
