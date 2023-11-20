from ctypes import cast, POINTER
import ctypes
from comtypes import CoInitialize, CoUninitialize, CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import win32api
import psutil
import os


def name_process_audio():
    # Chiamare CoInitialize per inizializzare la libreria COM
    CoInitialize()
    
    try:
        process = []
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume1 = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process:
                process.append(session.Process.name())
        
        return process
    
    finally:
        # Chiamare CoUninitialize per rilasciare le risorse COM alla fine della funzione
        CoUninitialize()

def volume_process_control(application_name, volume_control):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume1= session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == application_name:
            volume1.SetMasterVolume(volume_control, None)

def get_volume_process(application_name):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume1= session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == application_name:
            app_volume = volume1.GetMasterVolume()
            return app_volume