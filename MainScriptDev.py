import warnings
import subprocess
import logging
import psutil
import time
import webbrowser
import tkinter as tk
from tkinter import ttk
import json
import os
# Suppress the specific SyntaxWarning from pywinauto
warnings.filterwarnings("ignore", category=SyntaxWarning, message="invalid escape sequence '\\;'")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define constants
FORZA_EDITIONS = {
    "Forza Horizon 4": {
        "process_names": ['forzahorizon4.exe', 'forza horizon 4.exe'],
        "steam_url": 'steam://rungameid/1293830'
    },
    "Forza Horizon 5": {
        "process_names": ['forzahorizon5.exe', 'forza horizon 5.exe'],
        "steam_url": 'steam://rungameid/1551360'
    },
    "Forza Motorsport": {
        "process_names": ['forzamotorsport.exe', 'forza motorsport.exe'],
        "steam_url": 'steam://rungameid/2440510'
    }
}

def execute_command(cmd, success_msg, error_msg):
    try:
        subprocess.run(cmd, check=True)
        logger.info(success_msg)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_msg}: {str(e)}")
        return False

def start_forza(edition):
    try:
        webbrowser.open(FORZA_EDITIONS[edition]["steam_url"])
        logger.info(f"{edition} start command executed via Steam")
        return True
    except Exception as e:
        logger.error(f"Error starting {edition}: {str(e)}")
        return False

def is_forza_running(edition):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in FORZA_EDITIONS[edition]["process_names"]:
            return True
    return False

def kill_explorer():
    return execute_command(["taskkill", "/f", "/im", "explorer.exe"], "Explorer.exe killed", "Failed to kill explorer.exe")

def start_explorer():
    return execute_command(["explorer.exe"], "Explorer.exe started", "Failed to start explorer.exe")

import tkinter as tk
from tkinter import messagebox

class ForzaLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Forza Launcher")
        master.geometry("300x150")
        master.resizable(False, False)

        ttk.Label(master, text="Select Forza Edition:").pack(pady=10)

        self.combo = ttk.Combobox(master, values=list(FORZA_EDITIONS.keys()), state="readonly")
        self.combo.pack(pady=10)

        self.launch_button = ttk.Button(master, text="Launch", command=self.launch_forza)
        self.launch_button.pack(pady=10)

    def launch_forza(self):
        edition = self.combo.get()
        self.master.withdraw()

        if edition not in FORZA_EDITIONS:
            self.show_error_message(f"Invalid Forza edition selected: {edition}")
            return

        try:
            if not start_forza(edition) or not self.wait_for_forza_start(edition):
                self.show_error_message(f"Failed to start {edition}")
                return

            if kill_explorer():
                logger.info("Forza launched successfully and Explorer killed")
            else:
                logger.warning("Failed to kill Explorer")

            self.monitor_forza(edition)

        except Exception as e:
            self.show_error_message(f"An unexpected error occurred: {str(e)}")

    def wait_for_forza_start(self, edition, timeout=60):
        for _ in range(timeout):
            if is_forza_running(edition):
                return True
            time.sleep(1)
        return False

    def monitor_forza(self, edition):
        while is_forza_running(edition):
            time.sleep(5)
        logger.info(f"{edition} process not found. Starting explorer.exe")
        start_explorer()
        logger.info("Exiting application")
        self.master.quit()

    def show_error_message(self, message):
        messagebox.showerror("Error", f"{message}\nThe application will now exit.")
        self.master.quit()

def main(edition):
    if edition not in FORZA_EDITIONS:
        logger.error(f"Invalid Forza edition selected: {edition}")
        print(f"Error: Invalid Forza edition selected: {edition}")
        return False

    try:
        # Start Forza
        if not start_forza(edition):
            print(f"Error: Failed to start {edition}")
            return False

        # Wait for Forza to start
        forza_started = False
        for _ in range(60):  # Wait up to 60 seconds
            if is_forza_running(edition):
                forza_started = True
                break
            time.sleep(1)

        if not forza_started:
            print(f"Error: {edition} did not start within the expected time")
            return False

        # Kill Explorer
        explorer_killed = kill_explorer()

        if explorer_killed and forza_started:
            msg = "Успешно"
        elif explorer_killed and not forza_started:
            msg = "Ошибка запуска приложения"
        elif not explorer_killed and forza_started:
            msg = "Ошибка завершения explorer.exe"
        else:
            msg = "Ни одна из частей не была выполнена"

        print(f"Status: {msg}")
        logger.info(f"Initial status: explorer_killed={explorer_killed}, forza_started={forza_started}")

        # Continuously check if Forza is running
        while True:
            if not is_forza_running(edition):
                logger.info(f"{edition} process not found. Starting explorer.exe")
                start_explorer()
                break
            time.sleep(5)

        return True

    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        print("Interrupted: Script execution was interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        print(f"Error: An unexpected error occurred: {str(e)}")

    return False

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # This line makes the window non-resizable
    app = ForzaLauncher(root)
    root.mainloop()