# Importaciones estándar
import os
import sys
import time
import socket
import threading
import subprocess
import argparse

# Importaciones de terceros
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pylsl import StreamInfo, StreamOutlet
import pyautogui

# Funciones de ejecución de procesos

def execute_command(path, command):
    """Ejecuta un comando en un directorio específico y maneja errores."""
    print(f'Executing process {command}')
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, cwd=path)

    if process.poll():
        error = process.stderr.read().decode()
        print(f"Error: {error}")
        raise subprocess.CalledProcessError(process.returncode, command)


def execute_lab_recorder(config_file=None):
    """Ejecuta el LabRecorder con un archivo de configuración opcional."""
    os.system("taskkill /IM LabRecorder.exe /F")
    command = "LabRecorder.exe"
    if config_file:
        command += f" -c {config_file}"
    execute_command("C:/Users/Cocudata/Desktop/LabRecorder", command)


def execute_game_controller():
    """Ejecuta el GameController."""
    os.system("taskkill /IM GameController.exe /F")
    execute_command("C:/Users/Cocudata/GameController/", "GameController.exe")


def execute_brainamp_connector(config_file=None):
    """Ejecuta el BrainAmpSeries con un archivo de configuración opcional."""
    os.system("taskkill /IM BrainAmpSeries.exe /F")
    command = "BrainAmpSeries.exe"
    if config_file:
        command += f" -c {config_file}"
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, 
                               cwd="C:/Users/Cocudata/BrainAmpSeries/bin/")
    if process.poll():
        error = process.stderr.read().decode()
        print(f"Error: {error}")
        raise subprocess.CalledProcessError(process.returncode, command)
    return process

# Funciones de configuración y grabación

def setup_lsl_outlet():
    """Configura y devuelve un StreamOutlet para LSL."""
    info = StreamInfo(name='markers', type='Markers', channel_count=1,
                      channel_format='string', source_id='vr-markers')
    return StreamOutlet(info)


def create_bids_folders(info_dict):
    """Crea las carpetas necesarias para almacenar los resultados en formato BIDS."""
    results_folder = "C:/Users/Cocudata/experiment_VR/results"
    subject_folder = os.path.join(results_folder, f"sub-{info_dict['ID']}")
    os.makedirs(subject_folder, exist_ok=True)
    session_folder = os.path.join(subject_folder, f"ses-{info_dict['session']}")
    os.makedirs(session_folder, exist_ok=True)
    physio_folder = os.path.join(session_folder, "physio")
    os.makedirs(physio_folder, exist_ok=True)
    audio_folder = os.path.join(session_folder, "audio")
    os.makedirs(audio_folder, exist_ok=True)
    return physio_folder, audio_folder


def initialize_lsl_recording(info_dict, physio_file_name):
    """Inicializa la grabación LSL con los parámetros proporcionados."""
    try:
        # Conectar con Lab Recorder
        s = socket.create_connection(("localhost", 22345))
        
        # Construir el nombre del archivo XDF y su ruta
        save_path = os.path.join(
            "C:/Users/Cocudata/experiment_VR/results",
            f"sub-{info_dict['ID']}",
            f"ses-{info_dict['session'].lower()}",
            "physio"
        )
        
        # Asegurar que el directorio existe
        os.makedirs(save_path, exist_ok=True)

        # Contador para los runs
        run_count = len([name for name in os.listdir(save_path) if name.endswith('.xdf')]) + 1
        
        # Configurar Lab Recorder con los parámetros correctos
        s.sendall(b"select all\n")
        
        # Configurar el nombre del archivo con el día incluido
        filename = f"sub-{info_dict['ID']}_ses-{info_dict['session'].lower()}_day-{info_dict['day'].lower()}_task-{info_dict['block'].lower()}_run-{run_count:03d}_eeg.xdf"
        filename_cmd = f"filename {os.path.join(save_path, filename)}\n"
        s.sendall(filename_cmd.encode())
        
        # Configurar los parámetros BIDS
        s.sendall(f"participant {info_dict['ID']}\n".encode())
        s.sendall(f"session {info_dict['session'].lower()}\n".encode())
        s.sendall(f"day {info_dict['day'].lower()}\n".encode())  # Añadir día como parámetro BIDS
        s.sendall(f"task {info_dict['block'].lower()}\n".encode())
        s.sendall(b"run 001\n")
        s.sendall(b"modality eeg\n")
        
        # Actualizar y comenzar la grabación
        s.sendall(b"update\n")
        s.sendall(b"start\n")
        
        print(f"Iniciando grabación LSL en: {os.path.join(save_path, filename)}")
        return s, filename
    except Exception as e:
        print(f"Error al iniciar Lab Recorder: {e}")
        return None, None

# Funciones de interfaz de usuario

def get_participant_info():
    """Obtiene la información del participante y maneja la interfaz de grabación."""
    def start_recording():
        try:
            id_num = int(id_entry.get())
            if 0 <= id_num <= 99:
                info['ID'] = f"{id_num:02d}"
                info['session'] = session_var.get()
                info['day'] = day_var.get()  # Guardar el día seleccionado
                info['block'] = block_var.get()
                info['exp_name'] = f"Experiment_{info['block']}"
                start_actual_recording()
                id_entry.config(state='disabled')
                session_dropdown.config(state='disabled')
                day_dropdown.config(state='disabled')  # Deshabilitar el dropdown de día
                block_dropdown.config(state='disabled')
                start_btn.grid_forget()
                stop_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')
                status_label.config(text="Grabando...", fg="green")
                root.recording_active = True
            else:
                error_label.config(text="Error: ID debe ser un número entre 00 y 99")
                return
        except ValueError:
            error_label.config(text="Error: ID debe ser un número entre 00 y 99")
            return

    def start_actual_recording():
        physio_folder, audio_folder = create_bids_folders(info)
        root.physio_folder = physio_folder
        root.audio_folder = audio_folder
        root.outlet = setup_lsl_outlet()
        
        if not args.test:
            root.brainamp_process = execute_brainamp_connector(
                "C:/Users/Cocudata/experiment_VR/mw_lsl_42chs.cfg")
            
            GCthread = threading.Thread(target=execute_game_controller)
            GCthread.start()
            
            link_instructions_label = tk.Label(root, 
                text="Por favor, realiza las siguientes acciones y marca las casillas cuando estén listas:")
            link_instructions_label.grid(row=6, column=0, columnspan=2, pady=5)
            
            brainamp_var = tk.BooleanVar()
            brainamp_check = tk.Checkbutton(root, 
                text="He hecho clic en 'Link' en BrainAmp", 
                variable=brainamp_var)
            brainamp_check.grid(row=7, column=0, columnspan=2, pady=2)
            
            gamecontroller_var = tk.BooleanVar()
            gamecontroller_check = tk.Checkbutton(root, 
                text="He hecho clic en 'Link' en GameController", 
                variable=gamecontroller_var)
            gamecontroller_check.grid(row=8, column=0, columnspan=2, pady=2)
            
            lslviewer_var = tk.BooleanVar()
            lslviewer_check = tk.Checkbutton(root, 
                text="He hecho clic en 'Connect' en Brain Vision LSL Viewer", 
                variable=lslviewer_var)
            lslviewer_check.grid(row=9, column=0, columnspan=2, pady=2)
            
            start_btn.config(state='disabled')
            
            def on_links_confirmed():
                if brainamp_var.get() and gamecontroller_var.get() and lslviewer_var.get():
                    link_instructions_label.grid_remove()
                    brainamp_check.grid_remove()
                    gamecontroller_check.grid_remove()
                    lslviewer_check.grid_remove()
                    confirm_links_btn.grid_remove()
                    
                    try:
                        # Iniciar Lab Recorder
                        LRthread = threading.Thread(target=execute_lab_recorder, 
                                                 args=("LabRecorder - Copy.cfg",))
                        LRthread.start()
                        time.sleep(5)  # Esperar a que Lab Recorder se inicie
                        
                        # Iniciar grabación LSL
                        root.s, root.xdf_filename = initialize_lsl_recording(info, 
                            f"sub-{info['ID']}_ses-{info['session']}_task-{info['exp_name']}_physio")
                        
                        if root.s is None:
                            status_label.config(text="Error al iniciar Lab Recorder", fg="red")
                            return
                        
                        # Configurar interfaz
                        id_entry.config(state='disabled')
                        session_dropdown.config(state='disabled')
                        day_dropdown.config(state='disabled')
                        block_dropdown.config(state='disabled')
                        start_btn.grid_forget()
                        stop_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')
                        status_label.config(text="Grabando...", fg="green")
                        
                        # Iniciar grabación
                        root.recording_active = True
                        root.outlet.push_sample([f"BLOCK_{info['session']}_START"])
                        
                        # Configurar grabación de audio
                        root.samplerate = 44100
                        root.channels = 1
                        root.max_dur = 7200
                        root.recording = sd.rec(int(root.samplerate * root.max_dur),
                                              samplerate=root.samplerate,
                                              channels=root.channels,
                                              dtype='float64',
                                              blocking=False)
                        root.recording_start_time = time.time()
                        
                    except Exception as e:
                        status_label.config(text=f"Error al iniciar la grabación: {str(e)}", fg="red")
                        print(f"Error al iniciar la grabación: {str(e)}")
                else:
                    status_label.config(
                        text="Por favor, confirma los tres Links antes de continuar", 
                        fg="red")
            
            confirm_links_btn = tk.Button(root, 
                text="Confirmar y Continuar", 
                command=on_links_confirmed)
            confirm_links_btn.grid(row=10, column=0, columnspan=2, pady=5)

    def stop_recording():
        if root.recording_active:
            try:
                # Detener la grabación de audio
                recording_duration = time.time() - root.recording_start_time
                root.outlet.push_sample([f"SUPRABLOCK_{info['session']}_END"])
                
                # Detener Lab Recorder usando socket
                try:
                    if hasattr(root, 's') and root.s:
                        print("Deteniendo grabación LSL...")
                        root.s.sendall(b"stop\n")
                        time.sleep(2)  # Esperar a que Lab Recorder procese el comando
                        root.s.close()
                    
                    # Esperar a que el archivo se guarde
                    time.sleep(3)
                    
                    # Verificar que el archivo XDF existe
                    if hasattr(root, 'xdf_filename'):
                        expected_path = os.path.join(
                            "C:/Users/Cocudata/experiment_VR/results",
                            f"sub-{info['ID']}",
                            f"ses-{info['session'].lower()}",
                            "physio",
                            root.xdf_filename
                        )
                        
                        if os.path.exists(expected_path):
                            print(f"Archivo XDF guardado correctamente en: {expected_path}")
                        else:
                            print(f"ADVERTENCIA: No se encontró el archivo XDF en: {expected_path}")
                            # Buscar el archivo en ubicaciones alternativas
                            possible_locations = [
                                "C:/Users/Cocudata/Documents/CurrentStudy",
                                os.path.dirname(expected_path)
                            ]
                            
                            for location in possible_locations:
                                for root_dir, dirs, files in os.walk(location):
                                    for file in files:
                                        if file.endswith('.xdf'):
                                            found_path = os.path.join(root_dir, file)
                                            print(f"Se encontró un archivo XDF en: {found_path}")
                                            # Intentar mover el archivo a la ubicación correcta
                                            try:
                                                os.rename(found_path, expected_path)
                                                print(f"Archivo XDF movido a la ubicación correcta: {expected_path}")
                                            except Exception as move_error:
                                                print(f"No se pudo mover el archivo: {move_error}")
                except Exception as e:
                    print(f"Error al detener Lab Recorder: {e}")
                
                # Guardar grabación de audio
                actual_samples = int(recording_duration * root.samplerate)
                trimmed_recording = root.recording[:actual_samples]
                
                # Contador para los archivos de audio
                audio_run_count = len([name for name in os.listdir(root.audio_folder) if name.endswith('.wav')]) + 1
                
                # Incluir el día en el nombre del archivo de audio
                audio_file_name = f"sub-{info['ID']}_ses-{info['session'].lower()}_day-{info['day'].lower()}_task-{info['block'].lower()}_audio_run-{audio_run_count:03d}.wav"
                audio_path = os.path.join(root.audio_folder, audio_file_name)
                write(audio_path, root.samplerate, np.int16(trimmed_recording * 32767))
                print(f"Grabación de audio guardada en {audio_path}")
                
                # Cerrar procesos
                os.system("taskkill /IM LabRecorder.exe /F")
                os.system("taskkill /IM BrainAmpSeries.exe /F")
                os.system("taskkill /IM GameController.exe /F")
                
            except Exception as e:
                print(f"Error durante el proceso de detención: {e}")
            
            root.recording_active = False
            root.quit()

    root = tk.Tk()
    root.title("Configuración de la sesión")
    root.recording_active = False
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    info = {}
    # ID
    tk.Label(root, text="ID (00-99):").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(root)
    id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
    
    # Sesión
    tk.Label(root, text="Sesión:").grid(row=1, column=0, padx=5, pady=5)
    session_var = tk.StringVar(value="VR")
    session_dropdown = ttk.Combobox(root, textvariable=session_var, 
                                  values=["VR", "2D"], 
                                  state="readonly")
    session_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
    
    # Día (nuevo)
    tk.Label(root, text="Día:").grid(row=2, column=0, padx=5, pady=5)
    day_var = tk.StringVar(value="A")
    day_dropdown = ttk.Combobox(root, textvariable=day_var, 
                              values=["A", "B"], 
                              state="readonly")
    day_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
    
    # Bloque (ahora en la fila 3)
    tk.Label(root, text="Bloque:").grid(row=3, column=0, padx=5, pady=5)
    block_var = tk.StringVar(value="PRACTICE")
    block_dropdown = ttk.Combobox(root, textvariable=block_var, 
                                values=["PRACTICE", "01", "02", "03", "04"], 
                                state="readonly")
    block_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
    
    error_label = tk.Label(root, text="", fg="red")
    error_label.grid(row=4, column=0, columnspan=2, pady=5)
    
    status_label = tk.Label(root, text="", fg="green")
    status_label.grid(row=5, column=0, columnspan=2, pady=5)
    
    start_btn = tk.Button(root, text="Comenzar Grabación", command=start_recording)
    start_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky='nsew')
    stop_btn = tk.Button(root, text="Detener Grabación", command=stop_recording, bg="red", fg="white")
    root.mainloop()
    return info, root.recording_active

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Run in test mode without hardware connections')
    args = parser.parse_args()
    info_dict, recording_active = get_participant_info()
    if not recording_active:
        print("Grabación finalizada")
        sys.exit()
